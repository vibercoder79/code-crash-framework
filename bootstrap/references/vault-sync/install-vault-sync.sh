#!/usr/bin/env bash
# install-vault-sync.sh — interaktives Init des Vault-Harvest pro Mitarbeiter (BOO-77).
#
# Legt .vault-sync/local.json an (gitignored), traegt den Eintrag in .gitignore
# ein und installiert den post-merge-Hook als Symlink. Einseitig Repo -> Vault.
#
# Nutzung:
#   bash scripts/install-vault-sync.sh            # interaktives Init
#   bash scripts/install-vault-sync.sh --force    # bestehende local.json ueberschreiben
#   bash scripts/install-vault-sync.sh --uninstall # Hook + local.json entfernen
#
# Schreibt NIE in den Vault selbst — das macht ausschliesslich vault-sync.py.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SYNC_DIR="${REPO_ROOT}/.vault-sync"
LOCAL_JSON="${SYNC_DIR}/local.json"
HOOK_SRC="${REPO_ROOT}/.claude/hooks/post-merge.sh"
HOOK_DST="${REPO_ROOT}/.git/hooks/post-merge"

FORCE=0
UNINSTALL=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
  esac
done

if [[ "$UNINSTALL" -eq 1 ]]; then
  [[ -L "$HOOK_DST" || -f "$HOOK_DST" ]] && rm -f "$HOOK_DST" && echo "[install] post-merge-Hook entfernt."
  [[ -f "$LOCAL_JSON" ]] && rm -f "$LOCAL_JSON" && echo "[install] local.json entfernt."
  echo "[install] Vault-Harvest deinstalliert. tracked-paths.json (Team-Vertrag) bleibt."
  exit 0
fi

mkdir -p "$SYNC_DIR"

# --- .gitignore-Eintrag fuer die persoenliche local.json sicherstellen ---
GITIGNORE="${REPO_ROOT}/.gitignore"
if ! grep -qxF ".vault-sync/local.json" "$GITIGNORE" 2>/dev/null; then
  printf '\n# Persoenliche Vault-Harvest-Konfig (BOO-77) — nie committen\n.vault-sync/local.json\n' >> "$GITIGNORE"
  echo "[install] .vault-sync/local.json in .gitignore eingetragen."
fi

# --- local.json anlegen (gitignored, dry-run-Default) ---
if [[ -f "$LOCAL_JSON" && "$FORCE" -ne 1 ]]; then
  echo "[install] local.json existiert bereits — Skip (use --force zum Ueberschreiben)."
else
  read -r -p "Absoluter Pfad zu deinem Obsidian-Vault: " VAULT_PATH
  read -r -p "Projekt-Slug (Ordnername im Vault, z.B. mein-projekt): " PROJECT_SLUG
  read -r -p "Modus [dry-run/auto/ask] (Default dry-run): " MODE
  MODE="${MODE:-dry-run}"
  cat > "$LOCAL_JSON" <<JSON
{
  "_comment": "Persoenliche Vault-Harvest-Konfig (BOO-77/82). Das Vault-Ziel kommt standardmaessig aus tracked-paths.json (default_vault_subdir). path_mappings ist eine OPTIONALE Ueberschreibung: leer lassen = Team-Default verwenden; Eintraege wie 'docs/components': '02 Projekte/{project_slug}/Components' setzen nur, wenn du fuer dich abweichen willst.",
  "vault_path": "${VAULT_PATH}",
  "project_slug": "${PROJECT_SLUG}",
  "path_mappings": {},
  "last_sync_commit": "",
  "enabled": true,
  "mode": "${MODE}"
}
JSON
  echo "[install] ${LOCAL_JSON} angelegt (mode=${MODE}, enabled=true, Vault-Ziel via Team-Vertrag)."
fi

# --- post-merge-Hook als Symlink installieren ---
if [[ ! -f "$HOOK_SRC" ]]; then
  echo "[install] WARN: ${HOOK_SRC} fehlt — Hook nicht installiert. Bootstrap-Option [e] erneut laufen lassen."
else
  ln -sf "$HOOK_SRC" "$HOOK_DST"
  chmod +x "$HOOK_SRC" 2>/dev/null || true
  echo "[install] post-merge-Hook verlinkt: ${HOOK_DST} -> ${HOOK_SRC}"
fi

echo "[install] Fertig. Test: 'python3 scripts/vault-sync.py --dry-run' zeigt, was beim naechsten git pull gespiegelt wuerde."
