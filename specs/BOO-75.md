# BOO-75 — Vault-Harvest-Pattern: Repo-Docs + persoenlicher Vault (Phase 1 Doku)

## Summary

Multi-Person-Teams koennen den Obsidian-Vault nicht als geteilte Doku-SSoT nutzen (Vault ist persoenlich). Loesung: Doku lebt im GitHub-Repo (`docs/`), ein optionaler einseitiger Harvest spiegelt ausgewaehlte Docs in den **persoenlichen** Vault jedes Operators. Phase 1 dokumentiert das Pattern im Framework (HANDBUCH Anhang R Layer 3 + Bootstrap-Option + Config-Scaffold), vendored aber **keinen** Engine-Code — die Referenz-Implementierung bleibt in Stefans `StefanWeimarPRODOC/project-template`.

## Why

Operator-Feedback Stefan (2026-05-27): Wave-H-Doku-SSoT-Profil "Obsidian" geht von einem geteilten Vault aus — das gibt es im Team nicht. Wer ueber mehrere Projekte arbeitet, will Cross-Project-Insights trotzdem im eigenen Vault. Bestehender Gap: HANDBUCH Anhang R Layer 3 sagte nur "Vault wird zum persoenlichen Brainstorming-Tool" — zu wegwerfend, das strukturierte Harvest-Muster fehlte.

## What

- **HANDBUCH Anhang R Layer 3** (DE+EN): "Obsidian = Solo, nicht Enterprise" als scharfer Grundsatz; 2-Fluss-Modell (Fluss 1 normales Git bidirektional, Fluss 2 Harvest einseitig Repo→Vault via `git post-merge`-Hook); Sketch `docs/assets/vault-harvest-solo-vs-team.png`; Eigenschaften + DocSync-Abgrenzung.
- **Bootstrap Block B.3** (DE+EN): 5. Doku-SSoT-Option `[e] Repo-Docs + persoenlicher Vault-Harvest`; Inline-Hinweis (Solo→Obsidian, Team→Repo, Team-mit-Obsidian→Harvest) als doppelte Absicherung beim Installieren; `[e]`-Handling (DocSync=nein, Onboarding-Schritt, Verweis auf Scaffold + Stefans Repo). Version 3.29.0 → 3.30.0.
- **Config-Scaffold** `bootstrap/references/vault-sync-pattern.md` (+ `.en.md`): Team-Vertrag `tracked-paths.json` (4 Defaults), `local.json`-Schema, Mechanik-Beschreibung, Kernregeln. Engine-Verweis auf Stefans Repo.

## Constraints

- **KEIN Engine-Nachbau.** Stefans `vault-sync.py` etc. werden NICHT reimplementiert (Erfindungs-Risiko). Nur die von ihm woertlich genannten Defaults/Schemas werden dokumentiert.
- **Reine Doku + Config-Scaffold**, kein generierter Sync-Code im Bootstrap (Phase 1).
- DE + EN konsistent.

## Decisions

1. **Gestaffelt: Pattern jetzt (Phase 1), Engine spaeter (Phase 2)** — passt zum Leitsatz "Tiefe ins HANDBUCH, nicht ins Framework, solange kein zweiter Bedarf".
2. **5. Wave-H-Option als dokumentierte Wahl** — verweist auf Stefans Referenz-Repo, generiert keinen Code.
3. **Doppelte Absicherung** — Inline-Hinweis im Bootstrap (Install-Zeit) zusaetzlich zur HANDBUCH-Doku.
4. **DocSync-Abgrenzung explizit** — DocSync solo/bidirektional, Harvest team/einseitig; im Team-Modus DocSync=nein.

## Acceptance Criteria

- [x] HANDBUCH Anhang R Layer 3 (DE+EN): Obsidian=Solo geschaerft + 2-Fluss-Modell + Sketch eingebettet
- [x] Bootstrap Block B.3 (DE+EN): 5. Option + Inline-Hinweis + `[e]`-Handling
- [x] Config-Scaffold `bootstrap/references/vault-sync-pattern.md` (DE+EN)
- [x] Sketch `docs/assets/vault-harvest-solo-vs-team.png`
- [x] Bootstrap-Version-Bump 3.29.0 → 3.30.0

## Phase 2 (separate Story, blockiert)

Vendoring der Sync-Engine ins Framework. **Blocker:** `StefanWeimarPRODOC/project-template` nicht zugaenglich (gh "Could not resolve"). Voraussetzung: Stefan teilt Code → `security-architect --mode SKILL-SCAN` → Master/Mirror-Disziplin analog BOO-74.

## Dependencies

- Soft: BOO-72 (Anhang R existiert), BOO-74 (Master/Mirror-Pattern als Vorbild fuer Phase 2).

## Session-Referenz

Spec + Umsetzung Session 2026-05-28. Operator-Feedback Stefan. Diskussion: SecondBrain `02 Projekte/Code-Crash Framework/Decisions/2026-05-28 Vault-Sync fuer Multi-Person-Projekte (Stefan).md`. Linear: <https://linear.app/owlist/issue/BOO-75/>
