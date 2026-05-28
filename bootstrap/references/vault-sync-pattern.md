# Vault-Harvest-Pattern — Config-Scaffold (BOO-75)

Repo-Docs + persoenlicher Vault-Harvest fuer Multi-Person-Teams mit Obsidian-Nutzern. Dieses Dokument ist das **Config-Scaffold** im Framework — es beschreibt den Daten-Vertrag und die Mechanik. Die **Sync-Engine selbst** (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`) liegt in Stefans Referenz-Implementierung `StefanWeimarPRODOC/project-template` (`docs/vault-sync.md`) und wird in Phase 1 **nicht** ins Framework vendored.

> **Schwesterdatei (Englisch):** [`vault-sync-pattern.en.md`](./vault-sync-pattern.en.md)
> **HANDBUCH-Hintergrund:** Anhang R Layer 3 (Vault-Harvest-Pattern, 2-Fluss-Modell).

## Wann dieses Pattern?

Ein Team arbeitet am selben GitHub-Repo (Doku lebt in `docs/`), **und** einzelne Operatoren wollen projektuebergreifende Insights weiterhin im persoenlichen Obsidian-Vault sehen. Obsidian ist ein Solo-Werkzeug — es gibt keinen geteilten Team-Vault. Das Pattern loest das ueber zwei getrennte Fluesse:

- **Fluss 1 (normales Git, alle, bidirektional):** `docs/` ↔ GitHub-Repo via `git push`/`git pull`. Team-SSoT.
- **Fluss 2 (Harvest, pro Person, einseitig):** `git post-merge`-Hook kopiert ausgewaehlte `docs/`-Dateien in den persoenlichen Vault — nie zurueck.

## Baustein 1 — Team-Vertrag `.vault-sync/tracked-paths.json` (versioniert)

Definiert, welche Repo-Pfade harvest-bar sind und welches `type:`-Frontmatter beim Mirror in den Vault ergaenzt wird. Vier Defaults (aus der Referenz-Implementierung):

```json
{
  "tracked_paths": [
    { "glob": "docs/components/*.md",        "type": "component" },
    { "glob": "docs/decisions/*.md",         "type": "decision" },
    { "glob": "docs/architecture-guidelines.md", "type": "architecture" },
    { "glob": "journal/sprint-*.md",         "type": "sprint-retro" }
  ]
}
```

`type:` wird nur gesetzt, wenn die Quelldatei noch keinen hat (Sprint-Retros bringen ihren eigenen `type:` mit). Diese Datei ist **versioniert** (committed) — sie ist der Team-Vertrag, worauf sich alle einigen.

## Baustein 2 — Persoenliche Konfig `.vault-sync/local.json` (gitignored)

Pro Mitarbeiter, **niemals committen** (gehoert in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<projekt-slug>",
  "path_mappings": {
    "docs/components": "02 Projekte/{slug}/Components",
    "journal": "04 Ressourcen/{slug}/sprints"
  },
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` PARA-konform: `02 Projekte/{slug}/...` fuer Komponenten/Decisions, `04 Ressourcen/{slug}/sprints/` fuer Sprint-Retros.
- `mode`: `auto` (still mirroren) | `dry-run` (nur anzeigen) | `ask` (pro Datei fragen).
- `enabled: false` deaktiviert den Harvest fuer diesen Operator ohne Deinstallation.

## Baustein 3 — Mechanik (in Stefans Referenz-Repo)

- `scripts/install-vault-sync.sh` — interaktives Init pro Mitarbeiter (`--force` / `--uninstall`).
- `scripts/vault-sync.py` — Sync-Engine (Python-Stdlib-only, Frontmatter-Merge, Pfad-Containment-Check, drei Modi).
- `.claude/hooks/post-merge.sh` — 3-Zeilen-Wrapper, via Symlink in `.git/hooks/post-merge`, feuert nach jedem `git pull`.

## Kernregeln

- **Einseitig Repo → Vault.** Der Vault wird NIE vom Sync zurueckgeschrieben.
- **Vault nie manuell veraendern,** wo der Sync hinschreibt — Annotationen laufen ueber `.notes.md`-Schwesterdateien, die der Sync nicht anfasst.
- **Frontmatter-Namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — kollisionsfrei mit Quell-Properties, in Obsidian-Bases filterbar.
- **Null Reibung:** Mitarbeiter ohne `local.json` → Hook `exit 0` stillschweigend.
- **Abgrenzung DocSync (Block D.2):** DocSync ist solo + bidirektional (Vault ↔ Repo). Vault-Harvest ist team + einseitig (Repo → Vault). Im Team-Modus daher **DocSync = nein** setzen.

## Aktivierung im Bootstrap

Bootstrap-Frage B.3, Option `[e] Repo-Docs + persoenlicher Vault-Harvest`. In Phase 1 generiert Bootstrap **keinen** Engine-Code, sondern: Doku-SSoT auf `docs/project/`, Hinweis-Block auf Stefans Repo + dieses Scaffold, Block D DocSync = nein, Onboarding-Schritt fuer `.vault-sync/local.json`.

## Phasen

- **Phase 1 (BOO-75):** Dokumentation + dieses Scaffold. Engine bleibt in Stefans Repo.
- **Phase 2 (Folge-Story, blockiert):** Engine ins Framework vendoren — sobald `StefanWeimarPRODOC/project-template` zugaenglich ist und die Scripts per `security-architect --mode SKILL-SCAN` geprueft sind. Dann Master/Mirror-Disziplin analog BOO-74.

## Quelle

Operator-Feedback Stefan, 2026-05-27. Referenz-Implementierung: `StefanWeimarPRODOC/project-template`, `docs/vault-sync.md`.
