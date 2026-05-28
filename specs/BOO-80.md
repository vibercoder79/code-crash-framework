# BOO-80 — HANDBUCH Anhang U: Multi-Projekt-Betrieb (Projekt 2..N + bestehendes Projekt)

## Summary

Neuer HANDBUCH-Anhang U (DE+EN) beantwortet "mehrere Projekte auf einer Maschine — pro Projekt bootstrappen oder Basis-schon-da-Pfad?". Trennt Maschinen-Ebene (einmal) von Projekt-Ebene (jedes Mal) und beschreibt drei Onboarding-Wege. Plus Sketch. Reine Doku.

## Why

Operator-Frage (Tobias, 2026-05-28): unklar, ob jedes Projekt den vollen Bootstrap braucht oder ob es einen leichtgewichtigen Pfad gibt, wenn Tools + globaler Skill-Pool schon installiert sind. Bisher implizit (Bootstrap Block B erkennt Infra), aber nirgends als Multi-Projekt-Anleitung dokumentiert.

## What

- **HANDBUCH Anhang U** (DE+EN) mit Sketch `docs/assets/multi-project-onboarding.png`:
  - Maschinen-Ebene (einmal: Tools, globaler Skill-Pool, ~/.claude) vs. Projekt-Ebene (jedes Mal: CLAUDE.md, Git-Hooks pro Repo, environment.json, specs/, Doku-SSoT) — Verweis Anhang S.
  - **Drei Onboarding-Wege:** (1) Neues Projekt von Null = voller /bootstrap; (2) Projekt 2..N = Bootstrap-Schnellpfad (Block B erkennt Basis, Phase 5 Skip, nur Projekt-Ebene); (3) Bestehendes Projekt = bootstrap Merge-Modus + migrate-to-v2.sh (kein neuer Skill).
  - Pro-Projekt-Minimal-Checkliste (CLAUDE.md / Hooks / environment.json / Doku-SSoT / verify-setup.sh).
- `migrate_boo_80` (Doku-only Hinweis) + Migration-Checklist §BOO-80.

## Constraints

- Reine Doku, kein Code-Change. Existing-Project bleibt dokumentierter Pfad (kein neuer Skill — bootstrap Merge + migrate decken es ab). DE+EN. 1 Sketch.

## Acceptance Criteria

- [x] HANDBUCH Anhang U (DE+EN): 3 Onboarding-Wege + Maschinen-vs-Projekt-Ebene + Minimal-Checkliste
- [x] Sketch `docs/assets/multi-project-onboarding.png` eingebettet
- [x] Cross-Verweise Anhang S / T / P / Bootstrap Block B + Phase 5
- [x] migrate_boo_80 + Migration-Checklist (DE+EN) + Release Notes + v0.2.0-overview

## Dependencies

- Anhang S (BOO-76, was einmal vs pro Projekt), Anhang T (BOO-79, verify), Bootstrap Block B + Phase 5, migrate-to-v2.sh.

## Session-Referenz

Session 2026-05-28. Operator-Frage Tobias. Linear: <https://linear.app/owlist/issue/BOO-80/>
