# BOO-78 — Doku-Aktualisierung: README v0.2.0-Stand + Anhang S Toolchain-Sektion

## Summary

README spiegelte nicht den v0.2.0-Stand (Waves J-O) — wichtigster Fehler: `dpo` fehlte, `security-architect` stand noch als externer Companion-Skill statt als Framework-Bundle-Skill (BOO-74). Plus: Anhang S bekommt die Sektion "Was einmal installieren, was pro Projekt?" als Antwort auf die wiederkehrende Toolchain-Frage. Reine Doku.

## Why

Operator-Beobachtung (Tobias, 2026-05-28): README veraltet + Toolchain-Frage "Linter/Tools nur einmal pro VPS, richtig?". Doku-Drift gefaehrdet die Glaubwuerdigkeit (neuer Nutzer liest README zuerst).

## What

**README.md (EN+DE):**
- `security-architect` + `dpo` als **Spezialisten-Bundle-Skills** im Framework-Repo gelistet (vendored, BOO-74) — eigene Tabelle; aus der Companion-Liste entfernt; `dpo` neu.
- HANDBUCH-Beschreibung: Split `HANDBUCH.md` (DE) + `HANDBUCH.en.md` (EN), ~190/165 KB, Anhaenge A-S benannt.
- "Was ist neu (v0.2.0)"-Verweis auf `docs/releases/v0.2.0-overview.md`.
- Governance-Gates-Liste ergaenzt: sensitive-paths (BOO-18), personal-data-paths (BOO-69), post-merge Vault-Harvest (BOO-77).
- "Operating at scale / Im Team"-Hinweis auf Anhaenge P/Q/R/S/O.

**HANDBUCH Anhang S (EN+DE):**
- Neue Sektion "Was einmal installieren, was pro Projekt?" mit Matrix: System-Tools (einmal) / Projekt-Dev-Deps (pro Projekt) / Skills (einmal global) / **Git-Hooks (PRO REPO — `.git/hooks/` wird nicht geklont)** / environment.json (pro Projekt). Faustregel + `core.hooksPath`-Ausnahme.

## Constraints

- Reine Doku, kein Skill-Code-Change → kein bootstrap-Versions-Bump.
- DE + EN konsistent.

## Acceptance Criteria

- [x] README EN+DE: dpo + security-architect als Bundle, HANDBUCH-Desc, v0.2.0-Verweis, Gates-Liste, Scale-Hinweis
- [x] HANDBUCH Anhang S: Toolchain-Sektion (DE+EN)
- [x] Release Notes + v0.2.0-overview-Update

## Session-Referenz

Session 2026-05-28. Operator-Beobachtung Tobias. Linear: <https://linear.app/owlist/issue/BOO-78/>
