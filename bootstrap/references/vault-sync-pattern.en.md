# Vault-Harvest Pattern — Config Scaffold (BOO-75)

Repo docs + personal vault harvest for multi-person teams with Obsidian users. This document is the **config scaffold** inside the framework — it describes the data contract and the mechanism. The **sync engine itself** (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`) lives in Stefan's reference implementation `StefanWeimarPRODOC/project-template` (`docs/vault-sync.md`) and is **not** vendored into the framework in Phase 1.

> **Sibling file (German):** [`vault-sync-pattern.md`](./vault-sync-pattern.md)
> **HANDBUCH background:** Appendix R Layer 3 (vault-harvest pattern, two-flow model).

## When to use this pattern

A team works on the same GitHub repo (docs live in `docs/`), **and** individual operators want to keep seeing cross-project insights in their personal Obsidian vault. Obsidian is a solo tool — there is no shared team vault. The pattern solves this via two separate flows:

- **Flow 1 (plain Git, all, bidirectional):** `docs/` ↔ GitHub repo via `git push`/`git pull`. Team SSoT.
- **Flow 2 (harvest, per person, one-way):** a `git post-merge` hook copies selected `docs/` files into the personal vault — never back.

## Building block 1 — team contract `.vault-sync/tracked-paths.json` (versioned)

Defines which repo paths are harvestable and which `type:` frontmatter is added when mirrored into the vault. Four defaults (from the reference implementation):

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

`type:` is only set when the source file does not have one yet (sprint retros bring their own `type:`). This file is **versioned** (committed) — it is the team contract everyone agrees on.

## Building block 2 — personal config `.vault-sync/local.json` (gitignored)

Per operator, **never commit** (belongs in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<project-slug>",
  "path_mappings": {
    "docs/components": "02 Projekte/{slug}/Components",
    "journal": "04 Ressourcen/{slug}/sprints"
  },
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` PARA-conform: `02 Projekte/{slug}/...` for components/decisions, `04 Ressourcen/{slug}/sprints/` for sprint retros.
- `mode`: `auto` (mirror silently) | `dry-run` (show only) | `ask` (ask per file).
- `enabled: false` disables the harvest for this operator without uninstalling.

## Building block 3 — mechanism (in Stefan's reference repo)

- `scripts/install-vault-sync.sh` — interactive init per operator (`--force` / `--uninstall`).
- `scripts/vault-sync.py` — sync engine (Python stdlib only, frontmatter merge, path-containment check, three modes).
- `.claude/hooks/post-merge.sh` — 3-line wrapper, symlinked into `.git/hooks/post-merge`, fires after each `git pull`.

## Core rules

- **One-way repo → vault.** The sync never writes back to the vault.
- **Never modify the vault manually** where the sync writes — annotations go into `.notes.md` sidecar files the sync does not touch.
- **Frontmatter namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — collision-free with source properties, filterable in Obsidian Bases.
- **Zero friction:** an operator without `local.json` → hook `exit 0` silently.
- **Delineation from DocSync (Block D.2):** DocSync is solo + bidirectional (vault ↔ repo). Vault harvest is team + one-way (repo → vault). In team mode therefore set **DocSync = no**.

## Activation in bootstrap

Bootstrap question B.3, option `[e] Repo docs + personal vault harvest`. In Phase 1 bootstrap generates **no** engine code, but: documentation SSoT set to `docs/project/`, hint block pointing to Stefan's repo + this scaffold, Block D DocSync = no, onboarding step for `.vault-sync/local.json`.

## Phases

- **Phase 1 (BOO-75):** documentation + this scaffold. The engine stays in Stefan's repo.
- **Phase 2 (follow-up story, blocked):** vendor the engine into the framework — once `StefanWeimarPRODOC/project-template` is accessible and the scripts are checked via `security-architect --mode SKILL-SCAN`. Then master/mirror discipline analogous to BOO-74.

## Source

Operator feedback Stefan, 2026-05-27. Reference implementation: `StefanWeimarPRODOC/project-template`, `docs/vault-sync.md`.
