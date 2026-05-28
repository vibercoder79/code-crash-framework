# BOO-79 — Projekt-Verification: verify-setup.sh + HANDBUCH Anhang T

## Summary

Beantwortet "Framework installiert — funktioniert auch alles?" in beiden Richtungen: ein read-only Bash-Skript `verify-setup.sh` (automatisiert) + HANDBUCH Anhang T (manuelle Checkliste). Bootstrap Phase 7.3b ruft das Skript am Ende auf. Loest den geparkten E2E-Smoke-Test-Gedanken (BOO-48).

## Why

Operator-Frage (Tobias, 2026-05-28): nach der Installation braucht es den **Proof**, dass das Geruest funktioniert — Linter erreichbar, Hooks feuern, Skills schreiben Artefakte, Artefakte existieren. Bisher verstreut (Anhang A Pre-Bootstrap, integration-test fuer Code-Aenderungen, BOO-48 geparkt). Kein konsolidierter Post-Install-Proof.

## What

- **`bootstrap/references/verify-setup.sh`** (Bash, BSD+Linux, kein jq): 6 Check-Gruppen — (1) environment.json, (2) Toolchain via `command -v` pro `tools_available: true`, (3) Git-Hooks pro Repo, (4) Kern-Artefakte (CONVENTIONS.md/ARCHITECTURE_DESIGN.md/specs/journal), (5) Privacy-Add-on falls aktiv, (6) Backlog-Adapter. Output PASS/WARN/FAIL + Summary. Exit 1 bei FAIL, `--strict` (WARN→FAIL), `--quiet`. Read-only.
- **HANDBUCH Anhang T** (DE+EN): manuelle 7-Punkte-Checkliste (inkl. Check 5 = manueller `/implement`-Probelauf, den ein Skript nicht abdecken kann), Skript-Doku, "Wann ausfuehren" (nach Bootstrap / nach jedem clone / CI-Gate).
- **Bootstrap Phase 7.3b** (DE+EN): kopiert + ruft `verify-setup.sh` vor dem finalen Commit. bootstrap v3.31.0 → v3.32.0.
- **`migrate_boo_79`** kopiert das Skript in Bestands-Projekte.

## Constraints

- Read-only, keine Projekt-Aenderung durch das Skript.
- Kein neuer Slash-Skill (Abgrenzung zu `/integration-test`): Skript + Checkliste + Bootstrap-Phase. Spaeter zu `/verify` promotebar.
- BSD+Linux-kompatibel, keine Dependencies.

## Validation (Smoke-Test)

- Leeres Git-Repo → 4 FAIL (environment.json, pre-commit, CONVENTIONS, ARCHITECTURE_DESIGN), Exit 1. ✓
- Minimal vollstaendiges Projekt → 12 PASS, Exit 0. ✓
- `--quiet` zeigt nur Summary + Exit-Code. ✓
- Test-Framework-Wert ohne Trailing-Quote (env_val-Whitespace-Trim). ✓

## Acceptance Criteria

- [x] `verify-setup.sh` mit 6 Check-Gruppen, PASS/WARN/FAIL, Exit-Codes, `--strict`/`--quiet`
- [x] Smoke-Test (leer → FAIL, vollstaendig → PASS)
- [x] HANDBUCH Anhang T (DE+EN)
- [x] Bootstrap Phase 7.3b ruft verify-setup.sh, v3.32.0
- [x] migrate_boo_79 + Migration-Checklist (DE+EN) + Release Notes + v0.2.0-overview

## Dependencies

- Loest BOO-48 (E2E-Smoke-Test). Bezug: environment.json (BOO-34), Hooks (BOO-4/29), Anhang S (was einmal vs pro Projekt — Hooks pro Repo).

## Session-Referenz

Session 2026-05-28. Operator-Frage Tobias. Linear: <https://linear.app/owlist/issue/BOO-79/>
