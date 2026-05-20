# Existing-Infra-Check — Block B

Goal: **respect existing infrastructure**. The bootstrap skill should plug into what's already there, not blindly create new.

## The 5 questions (one at a time, not batch)

### B.1 — Project directory

```
Do you already have a project directory?
  a) Yes, exists — absolute path?
  b) No, create new — where? (absolute path)
```

**Skill behavior:**
- `a`: Validate path (exists, is folder). If already contains files → merge-mode question (see below).
- `b`: Check parent folder, `mkdir -p` after confirmation.

### B.2 — GitHub repo

```
GitHub repo for this project?
  a) Yes, exists — URL? (e.g. github.com/user/repo)
  b) No, create later (no remote now)
  c) No GitHub wanted
```

**Skill behavior:**
- `a`: Validate remote URL (optional: `git ls-remote` with timeout). `git remote add origin` if not yet set locally.
- `b`: No `git remote add`. Hint: "Remote later via `git remote add origin <url>`".
- `c`: No remote setup.

### B.3 — Documentation SSoT

```
Where should project documentation be maintained authoritatively?
  a) Obsidian vault (best practice) + absolute vault path
  b) Repo docs under docs/project/
  c) External DMS (SharePoint/Confluence/Notion/Drive/...) + entry point
  d) Undecided (repo fallback + TODO + postflight WARN)
```

**Skill behavior:**
- `a`: Validate vault path. Check if `02 Projekte/` folder exists (if not → create with confirmation). Check project folder `02 Projekte/{PROJECT_NAME}/` (if exists → merge-mode question). Create `docs/project/README.md` as repo reference file.
- `b`: Use `docs/project/` as documentation SSoT. Block C is switched to "all project docs in repo".
- `c`: Document the external DMS as documentation SSoT. Locally create only `docs/project/README.md` with DMS name, entry point, link convention, and standard artifact list. Do not duplicate DMS content.
- `d`: Create repo fallback `docs/project/`, mark `TODO: finalize documentation SSoT`, postflight `WARN`.

Contract details: `project-documentation-ssot.en.md`.

### B.4 — Backlog system

```
Which backlog system do you use?
  a) Linear + team slug (e.g. JAR)
  b) Microsoft 365 Planner
  c) GitHub Issues
  d) None (specs only in repo)
```

**Skill behavior:**
- `a`: Linear MCP / API key check. Skill can create labels (Block A add-ons determine which).
- `b`: M365 MCP check. Manual label hint.
- `c`: GitHub CLI (`gh`) available? Labels via `gh label create`.
- `d`: No backlog integration, only `specs/` in repo.

### B.5 — .env status

```
Do you already have a .env file for this project?
  a) Yes, exists with keys
  b) No, .env.example is enough
```

**Skill behavior:**
- `a`: Don't touch `.env`, use `.env.example` only for reference. Check `.env` is in `.gitignore`.
- `b`: Only create `.env.example`. Operator is prompted in Phase 4.7 to fill keys.

## Merge mode

If `PROJECT_PATH` or `OBSIDIAN_VAULT/02 Projekte/{PROJECT_NAME}/` already contains files:

```
Warning: {PROJECT_PATH} already contains files:
  {FILE_LIST}

How to proceed?
  a) Create backup ({PROJECT_PATH}.bak.{TIMESTAMP}) + continue bootstrap (overwrites)
  b) Only add missing governance files (merge — existing files stay)
  c) Abort
```

**Skill behavior:**
- `a`: `cp -R {PROJECT_PATH} {PROJECT_PATH}.bak.{TIMESTAMP}`, then normal flow.
- `b`: Only create missing files (`if [ ! -f ... ]` pattern). Don't overwrite existing. Operator may need to merge manually.
- `c`: Abort. No changes.

## Output — EXISTING_INFRA dictionary

At the end of Block B, a structure is remembered for Phase 4-7:

```yaml
EXISTING_INFRA:
  project_path: /Users/tobi/projects/myproject
  project_path_existed: true
  merge_mode: "merge"  # or "new", "backup"
  github_repo: "github.com/user/myproject"
  github_remote_set: false  # not yet set locally
  obsidian_vault: /Users/tobi/Obsidian/MyVault
  obsidian_project_path: "02 Projekte/MyProject"
  obsidian_project_existed: false
  documentation_ssot:
    mode: "obsidian"  # obsidian | repo-docs | external-dms | undecided
    primary_path: /Users/tobi/Obsidian/MyVault/02 Projekte/MyProject
    repo_reference_path: docs/project/README.md
    external_system: null
    external_entrypoint: null
    fallback_active: false
    postflight_status: "PASS"
  backlog_tool: "linear"
  backlog_team: "MYP"
  backlog_labels_creatable: true  # Linear API available
  env_exists: false
  env_gitignored: true
```

## Safety notes

- **Never** overwrite files without confirmation. Backup mode is mandatory if merge is not desired.
- **Never** read or display secrets from `.env`. Only check existence.
- If permissions on `PROJECT_PATH` are missing → abort with clear error.
