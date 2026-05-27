# BOO-70 — HANDBUCH Anhang P: Deployment-Szenarien (Solo-Mac / Solo-VPS / Multi-User-VPS / Team-Server)

## Summary

HANDBUCH-Anhang P "Deployment-Szenarien" (DE+EN): vier Setup-Patterns vom Solo-Mac bis zur Multi-User-VPS-Coding-Factory. Pro Szenario: Operator-Profil, Setup-Schritte, Skill-Installation zentral vs. pro-Projekt, Secrets-Trennung, User-Isolation, Backup-Strategie, Tradeoffs. Plus Decision-Matrix "Welches Szenario passt zu welchem Use-Case". Im `/bootstrap` selbst nur 1 zusaetzliche Frage mit Default Solo-Mac + Verweis auf Anhang P — keine Aufblaehung des Bootstrap-Skills.

## Why

Heute hat HANDBUCH §8d "Coding-Umgebungen Mac/VPS/CI" technische Unterscheidung, aber **keine Deployment-Szenarien** (= wer benutzt es wie). Operator-Feedback (Martin, 2026-05-27): unklar wie eine Coding-Factory auf VPS aufgebaut wird, ob Skills zentral oder pro Projekt installiert werden, was vorab abgeklaert werden muss. BOO-83 hat das Multi-User-VPS-Pattern technisch definiert (siehe Memory `project_vps_multi_user`), aber nicht als gelebte Best-Practice-Doku.

Konsequenzen ohne diese Story:

- Neue Operatoren wissen nicht, ob Solo-Mac/VPS/Team-Server fuer ihren Use-Case passt
- Skill-Installation-Frage (zentral vs. pro-Projekt) bleibt undokumentiert
- VPS-Multi-User-Pattern aus BOO-83 ist nur in Commit-History und Memory, nicht im HANDBUCH
- "Coding-Factory aufbauen" bleibt ein Beratungs-Thema statt selbst-bedienbarem Setup

## What

- **HANDBUCH-Anhang P "Deployment-Szenarien"** (DE+EN), Sektionen:
  - **Decision-Matrix am Anfang:** Operator-Profil → empfohlenes Szenario (Tabelle)
  - **Szenario 1 — Solo-Mac** (Standard heute, fuer ~80% der Operatoren): Setup-Schritte, Skill-Pool zentral in `~/.claude/skills/`, Secrets in `~/.claude/.env`, Backup via Time Machine, Tradeoffs (kein 24/7, nicht mobile)
  - **Szenario 2 — Solo-VPS** (BOO-9-Pattern, fuer Mobile-Worker und 24/7-Background-Tasks): VPS-Provider-Wahl, SSH-Setup, Skill-Sync von Mac, Secrets-Trennung, Backup-Strategie (Hetzner Storage Box), Tradeoffs (Setup-Aufwand, Single Point of Failure)
  - **Szenario 3 — Multi-User-VPS-Coding-Factory** (BOO-83-Pattern, fuer Teams + geteilte Skill-Sammlung): User-Setup, Skill-Pool global vs. pro-User, Secrets pro User, Repository-Worktrees pro User, Backup-Strategie, Tradeoffs (Wartungsaufwand, User-Isolation kritisch)
  - **Szenario 4 — Team-mit-Coding-Server** (Hybrid: Mac-Frontend + VPS-Backend fuer 2-5 Operatoren): VS Code Remote/SSH-Setup, geteilter Backlog, Secrets pro Operator, Tradeoffs (komplex, brauchbar bei verteiltem Team)
  - **Pro Szenario:** Operator-Profil, 5-10 Setup-Schritte, Skill-Installation-Pattern, Secrets-Trennung, User-Isolation (wo relevant), Backup-Strategie, Tradeoffs-Block
- **`/bootstrap` Block A.x neue Frage:** "Deployment-Szenario: a) Solo-Mac (Default) b) anders → siehe HANDBUCH Anhang P". Bei "b)" wird nur ein Hinweis-Block ausgegeben (kein Setup-Code im Bootstrap, kein Interview-Fork)
- **Cross-Reference im HANDBUCH-Inhaltsverzeichnis** DE+EN
- **Release Notes:** Eintrag in `docs/releases/wave-k-deployment-scenarios.md` (gemeinsam mit BOO-71 als Wave K)
- **Skill-Versions-Bump bootstrap** (Minor wegen neuer Frage)

## Constraints

- **KEINE Aufblaehung des Bootstrap-Skills:** pro Szenario kein eigener Setup-Pfad, kein Interview-Stack — nur Verweis auf Anhang
- Bootstrap bleibt fuer Solo-Mac als Default frictionless (existierender Workflow unveraendert)
- DE + EN konsistent
- Keine technischen Anleitungen erfinden — nur etablierte Patterns dokumentieren (BOO-9 + BOO-83 als Quellen)
- Backup-Empfehlungen pro Szenario explizit (Hetzner Storage Box / Backblaze B2 / Time Machine) statt vage "macht ein Backup"

## Decisions

1. **Bootstrap stellt 1 Frage, nicht 4 Szenarien** — pragmatische Trennung: Operator-Entscheidung kommt aus Handbuch, Bootstrap macht Default-Setup
2. **Decision-Matrix als Einstieg im Anhang** — Operator findet sein Szenario via Profil-Match, nicht via Lesen aller 4
3. **Backup-Strategie pro Szenario explizit** statt einer generischen "macht Backups"-Sektion
4. **Solo-Mac bleibt Default** auch im neuen Bootstrap-Verhalten — Trampelpfad-Schutz

## Agent-Pattern

**Gewaehltes Pattern:** linear oder 1 Sub-Agent.

**Begruendung:** Reine Schreibarbeit, abgegrenzter Scope (1 Anhang DE+EN), keine Code-Aenderungen ausserhalb des HANDBUCHs (+ 1 Bootstrap-Frage). Sub-Agent-Overhead nur dann sinnvoll, wenn Lead parallel andere Stories bearbeitet (z.B. BOO-71 gleichzeitig).

## Validation

- HANDBUCH-Anhang P (DE) hat alle 4 Szenarien + Decision-Matrix
- HANDBUCH-Anhang P (EN) inhaltlich konsistent (gleiche Anzahl Szenarien, gleiche Tabellen)
- Bootstrap-Lauf zeigt neue Frage, Default-Setup bei "Solo-Mac"-Wahl unveraendert
- Cross-Reference im Inhaltsverzeichnis DE+EN
- Manueller Smoke-Test: HANDBUCH-Render im IDE-Preview zeigt Anhang P korrekt

## Acceptance Criteria

- [ ] HANDBUCH-Anhang P (DE) mit 4 Szenarien + Decision-Matrix + pro-Szenario-Standard-Sektionen
- [ ] HANDBUCH-Anhang P (EN) konsistent
- [ ] HANDBUCH-Inhaltsverzeichnis aktualisiert (DE+EN)
- [ ] `/bootstrap` Block A.x mit 1 neuer Frage + Verweis-Block bei "anders"
- [ ] Skill-Versions-Bump bootstrap
- [ ] Release Notes `docs/releases/wave-k-deployment-scenarios.md` (gemeinsam mit BOO-71)

## Dependencies

- Keine Hard-Dependencies. BOO-9 (VPS-Rollout) und BOO-83 (VPS-Multi-User-Pattern) liefern Input-Material, sind aber nicht blockierend.
- Kann gemeinsam mit BOO-71 in Wave K released werden.

## Session-Referenz

Spec geschrieben in Session 2026-05-27 nach Operator-Feedback Martin. Daily Note: SecondBrain 05 Daily Notes/2026-05-27.md. Linear: <https://linear.app/owlist/issue/BOO-70/>

## Rollout

Kein Feature-Flag noetig — reine Doku-Story plus 1 Bootstrap-Frage. Bestands-Projekte unveraendert.
