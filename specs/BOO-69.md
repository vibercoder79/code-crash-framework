# BOO-69 — Privacy by Design als Standard-Skill im Bundle (DPO-Adoption)

## Summary

DPO-Skill aus dem globalen Skill-Pool (`~/.claude/skills/dpo/`) als 12. Skill ins Code-Crash-Bundle adoptieren. Privacy-Add-on im `/bootstrap` von Doku-Skelett zu echtem Skill-Pfad aufwerten: bei Aktivierung werden DPO + `PRIVACY.md`-Template + Privacy-Hook installiert. 1:1 Spiegelung des bereits etablierten Security-by-Design-Patterns (security-architect + SECURITY.md + security_report_gate.py).

## Why

Heute hat `architecture-review §9 Privacy/DSGVO` nur 5 Bullet-Points und Privacy ist nur ein Multi-Select-Add-on mit Doku-Stub. Das ist **Asymmetrie zu Security** (das ist als voller Skill-Pfad verankert). Operator-Feedback (Martin, 2026-05-27): bei Beratungsarbeit mit personenbezogenen Daten (SAP SuccessFactors, AWS Bedrock Frankfurt) brauchen Code-Crash-Nutzer Privacy by Design als **verbindlichen Standard**, nicht als Best-Effort-Hinweis. Plus: DPO-Skill existiert bereits eigenstaendig — Adoption ist Standardisierung, nicht Neuentwicklung.

Konsequenzen ohne diese Story:

- Privacy-Add-on bleibt Doku-Stub ohne operative Tiefe
- Operator muss DPO-Logik bei jedem Privacy-Projekt manuell zusammenklicken
- Verkaufsargument "Code-Crash deckt Privacy by Design ab" stimmt halb (nur Add-on-Label, kein Skill)
- Asymmetrie zu Security bleibt — wirkt unsauber im Audit-Gespraech

## What

- **DPO-Skill ins Bundle:** `dpo/SKILL.md` + `dpo/SKILL.en.md` + `dpo/references/` (DSGVO/BDSG/nDSG-Templates, betroffenenrechte.md, dpia-template.md, privacy-patterns.md, verarbeitungsverzeichnis.md)
- **Frontmatter normalisiert:** `recommended_model: opus` (Compliance-kritisch, Audit-relevant), `metadata.hermes`-Block, Skill-Version 1.0.0 (neu im Bundle, eigenstaendige Versionierung)
- **`/bootstrap` Phase A.4 Privacy-Add-on aufwerten:** bei Aktivierung wird DPO + `PRIVACY.md`-Template + `.codex/hooks/privacy_report_gate.py` installiert (analog Security-Hook). Operator-Output zeigt "Privacy by Design aktiv" mit drei konkreten Folge-Effekten
- **Neues Template `bootstrap/references/privacy-md-template.md` (DE+EN):** Verarbeitungsverzeichnis-Sektion, Rechtsgrundlagen-Tabelle nach Art. 6 DSGVO, Loeschkonzept, Betroffenenrechte-Block, Loeschfristen pro Datenkategorie
- **`/ideation` Pre-Flight-Check Schritt 0c:** Story-Frontmatter um `personal_data: true|false` erweitert; bei `true` triggert ideation automatisch `dpo --mode assess` mit DPIA-Output-Verweis
- **`/implement` Schritt 5.5b "Personal-Data-Paths-Gate"** (analog 5.5 Sensitive-Paths): wenn Story-Spec `personal_data: true` und Code-Aenderung in Privacy-relevantem Pfad → `dpo --mode review`-Sub-Schritt
- **`/sprint-review` Schritt 7b:** `dpo --mode audit` alle N Sprints (konfigurierbar via `environment.json.audit_cadence`), Verarbeitungsverzeichnis-Diff im Sprint-Report
- **HANDBUCH-Anhang O "Privacy by Design"** (DE+EN): wann brauche ich Privacy-Modus, was macht der DPO-Skill (3 Modi: ASSESS/REVIEW/AUDIT), Verhaeltnis zu security-architect, Migrations-Hinweise fuer Bestands-Projekte
- **`migrate_boo_69()` in `migrate-to-v2.sh`:** bei aktivem Privacy-Add-on PRIVACY.md + Hook + dpo-Skill-Kopie idempotent nachziehen
- **migration-checklist Eintrag** §BOO-69 (DE+EN)
- **Release Notes** `docs/releases/wave-j-privacy-by-design.md`

## Constraints

- DPO-Skill bleibt **GLEICHZEITIG** im globalen Skill-Pool nutzbar (nicht-destruktive Adoption — globale Datei bleibt unveraendert)
- Privacy-Add-on bleibt OPTIONAL (kein Hard-Block fuer Operator, die keine personenbezogenen Daten verarbeiten)
- DE + EN konsistent
- Keine Privacy-Engine selbst implementieren (keine Anonymisierung, keine PII-Detection-Library, kein Routing) — das ist Compliance-Doku-Schicht, kein Runtime-Privacy-Layer; Runtime-Layer = BOO-71 Hook-Punkt
- Keine Empfehlung welche Rechtsgrundlage operativ "richtig" ist — Skill macht Pruef-Fragen, Operator entscheidet

## Decisions

1. **DPO im Bundle** statt nur Cross-Reference: Privacy-by-Design ist Framework-Garantie, nicht Best-Effort. Konsistenz mit security-architect-Pattern.
2. **DPO bleibt GLEICHZEITIG global** verfuegbar — nicht-destruktive Adoption (DPO ist auch in Nicht-Code-Crash-Projekten nuetzlich).
3. **`recommended_model: opus`** fuer DPO (Compliance-kritisch, analog architecture-review/cloud-system-engineer).
4. **Privacy-Add-on bleibt optional** — kein Aufzwingen fuer Projekte ohne personenbezogene Daten.
5. **Hook heisst `privacy_report_gate`** (analog `security_report_gate`) statt etwas Generisches wie `dpo_gate` — Symmetrie macht Doku konsistent.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell, max 3 Brocken parallel).

**Begruendung:** Mehrere abgegrenzte Brocken (Bundle-Adoption, Bootstrap-Erweiterung, Pipeline-Hooks in ideation+implement+sprint-review, HANDBUCH-Anhang). Pro Brocken ein fokussierter Sub-Agent mit Hard-Constraint "DPO-Funktionalitaet nicht erfinden, nur integrieren" (Memory feedback_subagent_spec_fabrication). EN-Pass nicht im selben Sub-Agent (Memory feedback_subagent_long_heredoc_timeout) — separater Pass durch Lead oder dediziertes EN-Sub-Agent pro Datei.

## Validation

- Beide DPO-Files (DE+EN) syntaktisch valid YAML-Frontmatter
- Bootstrap-Lauf mit Privacy-Add-on = "ja" erzeugt PRIVACY.md + Hook + dpo-Kopie im Projekt
- Bootstrap-Lauf ohne Privacy-Add-on bleibt unveraendert (Idempotenz)
- `/ideation` Pre-Flight `personal_data: false` skippt DPO-Aufruf
- `/implement` Personal-Data-Paths-Gate aktiv bei `personal_data: true` + Code-Aenderung in `pii/`-Pfad
- HANDBUCH-Anhang O verlinkt in Inhaltsverzeichnis DE+EN
- `migrate_boo_69()` idempotent
- `git diff --check` clean

## Acceptance Criteria

- [ ] `dpo/` im Bundle verfuegbar (SKILL.md + SKILL.en.md + references DE+EN), Frontmatter normalisiert
- [ ] DPO bleibt unveraendert im globalen Skill-Pool (`~/.claude/skills/dpo/`)
- [ ] `/bootstrap` Privacy-Add-on installiert PRIVACY.md + Hook + DPO bei Aktivierung
- [ ] `bootstrap/references/privacy-md-template.md` (DE+EN) existiert
- [ ] `/ideation` Schritt 0c Privacy-Pre-Flight (personal_data-Frage) eingebaut
- [ ] `/implement` Schritt 5.5b Personal-Data-Paths-Gate eingebaut
- [ ] `/sprint-review` Schritt 7b DPO-Audit eingebaut
- [ ] HANDBUCH-Anhang O Privacy-by-Design (DE+EN)
- [ ] `migrate_boo_69()` implementiert
- [ ] migration-checklist Eintrag (DE+EN)
- [ ] Skill-Versions-Bumps: bootstrap, ideation, implement, sprint-review, plus dpo neu (v1.0.0 im Bundle)
- [ ] Release Notes `docs/releases/wave-j-privacy-by-design.md`
- [ ] Manueller Smoke-Test: `/bootstrap` mit Privacy=ja im Demo-Projekt erfolgreich

## Dependencies

- **Erfuellt:** BOO-84 (Token-Effizienz-Policy) — DPO bekommt `recommended_model: opus` aus dem Tier-Mapping in `model-tiers.json`
- **Soft-Dependency:** security-architect-Pattern als Vorlage (bereits etabliert seit Wave F)

## Session-Referenz

Spec geschrieben in Session 2026-05-27 nach Operator-Feedback Martin. Daily Note: SecondBrain 05 Daily Notes/2026-05-27.md. Fact-Sheet: `02 Projekte/Code-Crash Framework/assets/fact-sheet-privacy-by-design_1.docx`. Linear: <https://linear.app/owlist/issue/BOO-69/>

## Rollout

Privacy-Add-on bleibt optional, also kein Feature-Flag noetig. Bestands-Projekte koennen via `migrate_boo_69()` upgegradet werden — Migration ist idempotent und additiv.
