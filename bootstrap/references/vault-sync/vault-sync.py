#!/usr/bin/env python3
"""vault-sync.py — Framework-native Vault-Harvest-Engine (BOO-77, BOO-82).

Einseitiger Sync: GitHub-Repo -> persoenlicher Obsidian-Vault. NIE zurueck.
Liest .vault-sync/tracked-paths.json (versionierter Team-Vertrag) und
.vault-sync/local.json (pro Mitarbeiter, gitignored). Spiegelt ausgewaehlte
docs/-Dateien in den persoenlichen Vault, ergaenzt vault_sync_*-Frontmatter.

Designprinzipien (HANDBUCH Anhang R Layer 3 / vault-sync-pattern.md):
- Einseitig: schreibt NUR in den Vault, NIE ins Repo.
- Pfad-Containment: jedes Vault-Ziel muss innerhalb von vault_path liegen.
- Idempotent, kein Netzwerk, keine Secrets, nur Python-Stdlib.
- Fehlt local.json oder enabled=false: still exit 0 (null Reibung).

Ziel-Aufloesung (BOO-82):
- Der Team-Vertrag liefert pro Eintrag ein default_vault_subdir (Default-Layout
  fuer alle). local.json path_mappings sind eine OPTIONALE Ueberschreibung pro
  Mitarbeiter und haben Vorrang. Platzhalter {project_slug} und {slug} werden
  beide ersetzt.

Aufruf: python3 scripts/vault-sync.py [--dry-run] [--since <sha>]
- --since <sha>: nur Dateien syncen, die seit <sha> geaendert wurden
  (git diff --name-only <sha>..HEAD). Inkrementeller Sync fuer grosse Repos.
Wird normal vom .git/hooks/post-merge-Wrapper nach jedem git pull getriggert.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path

VAULT_SYNC_DIR = ".vault-sync"
CONTRACT_FILE = "tracked-paths.json"
LOCAL_FILE = "local.json"
NS = "vault_sync_"  # Frontmatter-Namespace


def _log(msg: str) -> None:
    print(f"[vault-sync] {msg}")


def _repo_root() -> Path:
    """Repo-Root = Verzeichnis, in dem .vault-sync/ liegt (vom CWD aufwaerts)."""
    cur = Path.cwd().resolve()
    for cand in [cur, *cur.parents]:
        if (cand / VAULT_SYNC_DIR / CONTRACT_FILE).exists():
            return cand
    return cur


def _load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        _log(f"WARN: {path} ist kein gueltiges JSON ({exc}). Uebersprungen.")
        return None


def _git_head(repo: Path) -> str:
    """Aktueller Commit-SHA ohne Subprozess-Pflicht — liest .git direkt."""
    head = repo / ".git" / "HEAD"
    try:
        ref = head.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"
    if ref.startswith("ref:"):
        ref_path = repo / ".git" / ref.split(" ", 1)[1].strip()
        try:
            return ref_path.read_text(encoding="utf-8").strip()[:12]
        except OSError:
            return "unknown"
    return ref[:12]


def _split_frontmatter(text: str) -> tuple[list[str], str]:
    """Trennt YAML-Frontmatter (--- ... ---) vom Body. Sehr einfacher Parser
    (zeilenbasiert) — kein YAML-Dependency, reicht fuer flache Properties."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def _has_key(fm_lines: list[str], key: str) -> bool:
    return any(ln.lstrip().startswith(f"{key}:") for ln in fm_lines)


def _build_frontmatter(
    fm_lines: list[str], *, project: str, rel_path: str, commit: str,
    inject_type: str | None,
) -> str:
    """Ergaenzt vault_sync_*-Felder (idempotent: ueberschreibt eigene Keys) und
    optional 'type:' (nur wenn Quelle keinen hat). Quell-Properties bleiben."""
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    managed = {
        f"{NS}project": project,
        f"{NS}path": rel_path,
        f"{NS}commit": commit,
        f"{NS}at": now,
    }
    kept = [ln for ln in fm_lines if not ln.lstrip().startswith(NS)]
    if inject_type and not _has_key(kept, "type"):
        kept.append(f"type: {inject_type}")
    out = ["---"]
    out.extend(kept)
    for key, val in managed.items():
        out.append(f"{key}: {val}")
    out.append("---")
    return "\n".join(out)


def _is_contained(target: Path, base: Path) -> bool:
    """True wenn target (nach realpath) innerhalb base liegt. Schutz gegen
    Pfad-Traversal und Symlink-Ausbruch aus dem Vault."""
    try:
        target_r = target.resolve()
        base_r = base.resolve()
    except OSError:
        return False
    return base_r == target_r or base_r in target_r.parents


def _subst_slug(dest: str, slug: str) -> str:
    """Ersetzt beide Platzhalter-Schreibweisen fuer den Projekt-Slug."""
    return dest.replace("{project_slug}", slug).replace("{slug}", slug)


def _map_target(
    rel_path: str, mappings: dict, slug: str, vault: Path,
    default_subdir: str | None,
) -> Path | None:
    """Mappt einen Repo-relativen Pfad auf einen Vault-Pfad.

    Reihenfolge (BOO-82): zuerst eine passende local.json path_mappings-
    Ueberschreibung (laengstes Praefix gewinnt), sonst das default_vault_subdir
    des Team-Vertrags. Ohne beides -> None (Datei wird uebersprungen)."""
    best_prefix = ""
    best_dest = None
    for prefix, dest in mappings.items():
        norm = prefix.rstrip("/")
        if (rel_path == norm or rel_path.startswith(norm + "/")) and len(norm) > len(best_prefix):
            best_prefix = norm
            best_dest = dest
    if best_dest is not None:
        remainder = rel_path[len(best_prefix):].lstrip("/")
        return vault / _subst_slug(best_dest, slug) / remainder
    if default_subdir:
        # Vertrags-Default: nur der Dateiname landet im Default-Unterordner.
        return vault / _subst_slug(default_subdir, slug) / Path(rel_path).name
    return None


def _changed_since(repo: Path, sha: str) -> set[str] | None:
    """Repo-relative Pfade, die seit <sha> bis HEAD geaendert wurden.
    None = git nicht verfuegbar/ungueltiger sha -> Aufrufer faellt auf
    Voll-Sync zurueck (kein stiller Datenverlust)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "diff", "--name-only", f"{sha}..HEAD"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        _log(f"WARN: --since {sha} fehlgeschlagen ({exc}). Voll-Sync.")
        return None
    return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}


def _iter_tracked(repo: Path, tracked: list[dict], changed: set[str] | None):
    """Liefert (abs_path, rel_path, inject_type, default_subdir) je Quelldatei.
    Ueberspringt .notes.md-Sidecars (Annotationen, nie angefasst). Ist 'changed'
    gesetzt (--since), werden nur darin enthaltene Pfade geliefert."""
    for entry in tracked:
        glob = entry.get("glob")
        if not glob:
            continue
        inject_type = entry.get("type")
        default_subdir = entry.get("default_vault_subdir")
        for match in sorted(repo.glob(glob)):
            if not match.is_file():
                continue
            if match.name.endswith(".notes.md"):
                continue
            rel = match.relative_to(repo).as_posix()
            if changed is not None and rel not in changed:
                continue
            yield match, rel, inject_type, default_subdir


def _arg_value(argv: list[str], flag: str) -> str | None:
    """Liest --flag <wert> oder --flag=<wert> aus argv. None wenn nicht gesetzt."""
    for i, tok in enumerate(argv):
        if tok == flag and i + 1 < len(argv):
            return argv[i + 1]
        if tok.startswith(flag + "="):
            return tok.split("=", 1)[1]
    return None


def _process_file(
    abs_path: Path, rel_path: str, target: Path, *, vault: Path, slug: str,
    commit: str, inject_type: str | None, mode: str,
) -> str:
    """Verarbeitet eine Quelldatei und liefert den Status:
    'written' | 'skipped' | 'blocked'. Kapselt Containment-Gate, Frontmatter-
    Aufbau und Schreib-/Dry-Run-/Ask-Logik (haelt main() flach)."""
    if not _is_contained(target, vault):
        _log(f"BLOCK {rel_path}: Ziel {target} liegt ausserhalb des Vaults — uebersprungen.")
        return "blocked"

    fm_lines, body = _split_frontmatter(abs_path.read_text(encoding="utf-8"))
    new_fm = _build_frontmatter(
        fm_lines, project=slug, rel_path=rel_path, commit=commit,
        inject_type=inject_type,
    )
    body = body.rstrip("\n")
    new_text = f"{new_fm}\n{body}\n" if body else f"{new_fm}\n"

    if mode == "dry-run":
        _log(f"[dry-run] wuerde schreiben: {target}")
        return "written"
    if mode == "ask":
        ans = input(f"[vault-sync] {rel_path} -> {target} schreiben? [y/N] ").strip().lower()
        if ans not in ("y", "yes", "j", "ja"):
            return "skipped"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(new_text, encoding="utf-8")
    return "written"


def main(argv: list[str]) -> int:
    cli_dry_run = "--dry-run" in argv
    since = _arg_value(argv, "--since")
    repo = _repo_root()
    sync_dir = repo / VAULT_SYNC_DIR

    contract = _load_json(sync_dir / CONTRACT_FILE)
    local = _load_json(sync_dir / LOCAL_FILE)

    # Null-Reibung: keine local.json oder deaktiviert -> still exit 0.
    if local is None:
        return 0
    if not local.get("enabled", False):
        _log("local.json vorhanden, aber enabled=false — Sync uebersprungen.")
        return 0
    if not contract or not contract.get("tracked_paths"):
        _log("Kein tracked-paths.json / keine tracked_paths — nichts zu tun.")
        return 0

    vault_raw = (local.get("vault_path") or "").strip()
    slug = (local.get("project_slug") or "").strip()
    mappings = local.get("path_mappings") or {}
    mode = "dry-run" if cli_dry_run else (local.get("mode") or "dry-run")

    if not vault_raw:
        _log("WARN: vault_path leer in local.json — abgebrochen.")
        return 1
    vault = Path(os.path.expanduser(vault_raw))
    if not vault.is_dir():
        _log(f"WARN: vault_path existiert nicht: {vault} — abgebrochen.")
        return 1

    commit = _git_head(repo)
    written = skipped = blocked = 0

    changed = _changed_since(repo, since) if since else None
    if since and changed is not None:
        _log(f"--since {since}: {len(changed)} geaenderte Datei(en) im Diff.")

    counts = {"written": 0, "skipped": 0, "blocked": 0}
    for abs_path, rel_path, inject_type, default_subdir in _iter_tracked(
        repo, contract["tracked_paths"], changed
    ):
        target = _map_target(rel_path, mappings, slug, vault, default_subdir)
        if target is None:
            _log(f"SKIP {rel_path}: kein path_mapping und kein default_vault_subdir.")
            counts["skipped"] += 1
            continue
        status = _process_file(
            abs_path, rel_path, target, vault=vault, slug=slug, commit=commit,
            inject_type=inject_type, mode=mode,
        )
        counts[status] += 1
    written, skipped, blocked = counts["written"], counts["skipped"], counts["blocked"]

    # last_sync_commit aktualisieren (nur bei echtem Schreiben, idempotent)
    if mode not in ("dry-run",) and written:
        local["last_sync_commit"] = commit
        (sync_dir / LOCAL_FILE).write_text(
            json.dumps(local, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    _log(
        f"Fertig (mode={mode}, commit={commit}): {written} geschrieben/geplant, "
        f"{skipped} uebersprungen, {blocked} blockiert."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
