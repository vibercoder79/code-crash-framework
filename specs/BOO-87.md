# BOO-87 — dpo-Kontrollkatalog + Audit-Report (deterministischer AUDIT-Modus)

## Summary

Den AUDIT-Modus des `dpo`-Skills von prosaischer LLM-Bewertung zu deterministischen, versionierten YAML-Kontrollkatalogen aufwerten. Code/Projekt wird Control-fuer-Control gegen den Katalog geprueft; Ergebnis ist ein reproduzierbarer Pass/Gap/Review-Needed-Report (auditor-ready, OSCAL-Export optional als spaetere Ausbaustufe). Der Katalog liegt als YAML im Git — **KEINE Datenbank**. Das Pattern stammt aus `agentic-security` (JSON-Control-Kataloge + OSCAL), nachgebaut und um nDSG erweitert; es wird **KEIN Code uebernommen** (PolyForm-Lizenz).

## Why

`dpo` liefert heute eine `PRIVACY.md` als Fliesstext: eine Meinung, nicht reproduzierbar, nicht an eine Control-ID gebunden, nicht maschinell pruefbar, nicht auditor-exportierbar. Zwei identische Laeufe koennen unterschiedliche Formulierungen liefern. Die Zielgruppe (Schweizer Banken/Versicherer, FINMA/BaFin-reguliert) braucht reproduzierbare, belegbare Evidenz pro Control — kein KI-Aufsatz.

Konsequenzen ohne diese Story:

- Compliance-Aussage bleibt KI-Aufsatz — im Audit-Gespraech schwach, weil nicht an eine pruefbare Control-ID gebunden
- Keine Reproduzierbarkeit: zwei Laeufe liefern unterschiedliche Formulierungen, kein belastbarer Nachweis "welche Regel galt wann"
- Keine maschinenlesbare Evidenz fuer Auditoren — kein Export-Pfad Richtung OSCAL
- nDSG-Alleinstellung (Schweizer Datenschutzrecht, von `agentic-security` NICHT abgedeckt) bleibt ungenutzt
- Asymmetrie zu `security-architect`-Tiefe bleibt — Privacy bleibt das schwaechere Standbein

## What

- **Kontrollkataloge als YAML:** `dpo/controls/ndsg.yml` (Schweizer nDSG — CH-Alleinstellung, `agentic-security` deckt das NICHT ab), `dpo/controls/gdpr.yml` (DSGVO), optional `dpo/controls/nist-ai-600.yml` (NIST AI 600-1).
- **Control-Schema (YAML) pro Eintrag:**
  - `id` (z.B. `GDPR-Art32-001`, `NDSG-Art8-001`)
  - `titel` (Klartext-Bezeichnung)
  - `evidenz` (geforderter Nachweis)
  - `pruefung` (mechanischer Check vs. Urteils-Check — explizit markiert)
  - `mapsTo` (Verweis auf konkreten Check/Artefakt, z.B. einen REVIEW-Check oder eine `PRIVACY.md`-Sektion)
  - `ergebnis` (`PASS` | `GAP` | `REVIEW-NEEDED`, beim Lauf gesetzt)
  - `quelle` (Herkunft: DSGVO-Artikel / nDSG-Artikel / NIST-Control-ID) — jedes Control traegt seine Herkunft
- **AUDIT-Modus arbeitet den Katalog ab → Report-Paar:**
  - `dpo/reports/<date>_audit.md` — menschenlesbare Pass/Gap-Tabelle, pro Luecke der konkrete Fix-Befehl
  - `dpo/reports/<date>_audit.json` — maschinenlesbares Pendant
  - OSCAL-Export als **optionale spaetere Ausbaustufe** explizit benannt (nicht Teil dieser Story)
- **Ehrlicher Determinismus:** Mechanische Checks (grep/Tool: Datei existiert? TLS-Config? Secret im Code? PII in Logs?) sind echt reproduzierbar → `PASS`/`GAP`. Urteils-Checks (z.B. Zweckbindung, Verhaeltnismaessigkeit) → `REVIEW-NEEDED` (Mensch bestaetigt). KLAR dokumentieren, dass nicht alles 100% automatisch ist — kein Vortaeuschen von Voll-Automatik.
- **Projekt-Overlay (BYO-Framework):** projekteigene Controls moeglich, z.B. `.claude/dpo/controls/<id>/controls.json` — ueberlebt Framework-Updates.
- **Integration:**
  - `/sprint-review` Schritt 7b/7c Audit nutzt den Katalog (statt Freitext-Bewertung)
  - `PRIVACY.md`-Querverweis auf den Audit-Report
  - `dpo/SKILL.md` AUDIT-Modus-Sektion umbauen (Katalog-Logik statt Prosa-Workflow)
- **HANDBUCH-Anhang O (Privacy by Design) erweitern (DE+EN):** Abschnitt "Deterministischer Kontrollkatalog" — was es ist, warum keine DB, wie man den Report liest.
- **Migration:** `migrate_boo_87()` (idempotent, additiv); migration-checklist §BOO-87 (DE+EN); Release Notes; `dpo`-Versions-Bump (1.1.0 → 1.2.0).

## Constraints

- **KEINE Datenbank.** Determinismus und Audit-Versionierung kommen aus der Git-versionierten YAML-Datei: mit-versioniert, diff-bar, beantwortet "welche Regel galt bei welchem Commit". Eine DB waere veraenderlicher State ausserhalb des Repos plus zusaetzliche Betriebs- und DSGVO-Last.
- **KEINE Runtime-Privacy-Engine** — keine PII-Detection-Library, kein Routing. Reine Compliance-Doku-/Evidenz-Schicht, kein Runtime-Privacy-Layer.
- **Katalog kuratiert aus offiziellen Quellen** (DSGVO-Text, nDSG, NIST AI 600-1) mit Herkunft pro Control.
- **KEIN Code aus `agentic-security`** (PolyForm-Lizenz) — Pattern nachgebaut, nichts uebernommen.
- DE + EN konsistent.
- **Pragma-Check:** Operator bekommt einen reproduzierbaren Report, statt selbst zu argumentieren; YAML statt DB-Setup — kein zusaetzlicher Betriebs-Overhead.
- **Security-/Compliance-Check:** auditor-ready Evidenz fuer FINMA/BaFin-regulierte Zielgruppe — belegbar, reproduzierbar, an Control-ID gebunden.
- **Mittelweg-Begruendung:** Leichter Mittelweg — erst Markdown/JSON-Report (schlank, sofort nutzbar), OSCAL optional spaeter. Keine enterprise-grade Compliance-Plattform, aber auch keine Compliance-Luecke.

## Decisions

1. **Katalog als YAML im Git statt DB** — Determinismus und Versionierung aus dem Repo selbst; DB waere veraenderlicher State ausserhalb des Repos plus Betriebs-/DSGVO-Last.
2. **Status-Trichotomie `PASS` / `GAP` / `REVIEW-NEEDED`** (ehrlicher Determinismus) — mechanische Checks liefern PASS/GAP, Urteils-Checks liefern REVIEW-NEEDED; kein Vortaeuschen von Voll-Automatik.
3. **nDSG-Katalog als CH-Alleinstellung** — Schweizer Datenschutzrecht, von `agentic-security` nicht abgedeckt; bedient die Kern-Zielgruppe.
4. **AUDIT-Modus erweitern statt neuer Skill** — der Katalog ist eine Tiefen-Aufwertung des bestehenden Modus, kein neues Werkzeug; weniger Skill-Drift.
5. **OSCAL nur optionaler spaeterer Ausbau** — erst Markdown/JSON, OSCAL-Export folgt bei Bedarf; Mittelweg statt Over-Engineering.
6. **Projekt-Overlay (BYO-Framework)** — projekteigene Controls unter `.claude/dpo/controls/` ueberleben Framework-Updates; Operator kann den Katalog erweitern, ohne den Framework-Katalog zu forken.
7. **Kein Code aus `agentic-security`** — PolyForm-Lizenz; Pattern wird nachgebaut, Herkunft pro Control dokumentiert.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Mehrere abgegrenzte Brocken (Katalog-Dateien `ndsg.yml`/`gdpr.yml`/`nist-ai-600.yml`, AUDIT-Modus-Umbau in `dpo/SKILL.md`, Report-Generator md+json, `/sprint-review`-Integration 7b/7c, HANDBUCH/Doku DE+EN, Migration). Pro Brocken ein fokussierter Sub-Agent. Hard-Constraints fuer jeden Sub-Agent: **"keine Rechtsberatung erfinden — der Skill stellt Pruef-Fragen, der Operator entscheidet"** (Memory feedback_subagent_spec_fabrication) und **"kein Code aus agentic-security uebernehmen"** (PolyForm-Lizenz). EN-Pass nicht im selben Sub-Agent wie der DE-Inhalt (Memory feedback_subagent_long_heredoc_timeout) — separater Pass pro Datei.

## Validation

- Alle Katalog-YAML-Dateien (`ndsg.yml`, `gdpr.yml`, optional `nist-ai-600.yml`) sind syntaktisch valide
- AUDIT-Lauf erzeugt `<date>_audit.md` + `<date>_audit.json` reproduzierbar — zweimaliger Lauf auf identischem Stand liefert identisches Ergebnis
- Mechanischer Check liefert `PASS`/`GAP`; Urteils-Check liefert `REVIEW-NEEDED`
- Overlay-Control aus `.claude/dpo/controls/` wird im Lauf beruecksichtigt
- Jedes Control hat eine `quelle` (Herkunft)
- `/sprint-review` Schritt 7b nutzt den Katalog statt Freitext-Bewertung
- HANDBUCH-Anhang O erweitert, DE+EN konsistent, im Inhaltsverzeichnis verlinkt
- `migrate_boo_87()` idempotent (zweiter Lauf aendert nichts)
- `git diff --check` clean

## Acceptance Criteria

- [ ] `dpo/controls/ndsg.yml` (CH-Alleinstellung) existiert, valide, jedes Control mit `quelle`
- [ ] `dpo/controls/gdpr.yml` existiert, valide, jedes Control mit `quelle`
- [ ] `dpo/controls/nist-ai-600.yml` (optional) vorhanden oder als spaeterer Ausbau dokumentiert
- [ ] Control-Schema vollstaendig (`id`, `titel`, `evidenz`, `pruefung`, `mapsTo`, `ergebnis`, `quelle`)
- [ ] AUDIT-Modus erzeugt `dpo/reports/<date>_audit.md` + `<date>_audit.json`
- [ ] Report reproduzierbar — zweimaliger Lauf = identisches Ergebnis
- [ ] Mechanische Checks liefern PASS/GAP, Urteils-Checks liefern REVIEW-NEEDED (ehrlicher Determinismus dokumentiert)
- [ ] Pro GAP steht der konkrete Fix-Befehl im md-Report
- [ ] Projekt-Overlay `.claude/dpo/controls/<id>/controls.json` wird beruecksichtigt
- [ ] `dpo/SKILL.md` AUDIT-Modus-Sektion auf Katalog-Logik umgebaut
- [ ] `/sprint-review` Schritt 7b/7c nutzt den Katalog
- [ ] `PRIVACY.md`-Querverweis auf Audit-Report
- [ ] HANDBUCH-Anhang O erweitert (DE+EN)
- [ ] `migrate_boo_87()` implementiert (idempotent, additiv)
- [ ] migration-checklist Eintrag §BOO-87 (DE+EN)
- [ ] Release Notes
- [ ] `dpo`-Versions-Bump (1.1.0 → 1.2.0)
- [ ] OSCAL-Export als optionale spaetere Ausbaustufe benannt (nicht implementiert)

## Dependencies

- **Baut auf BOO-69** (DPO als Standalone-Skill, `PRIVACY.md`-Template, `/implement` Schritt 5.5b Personal-Data-Paths-Gate, `/sprint-review` Schritt 7b DPO-Audit) auf
- **Quellbasis:** `dpo/references/` (ndsg-schweiz.md, verarbeitungsverzeichnis.md, dpia-template.md, privacy-patterns.md, betroffenenrechte.md) als kuratierte Grundlage fuer die Katalog-Controls
- **Muster (kein Code):** `agentic-security` (JSON-Control-Kataloge + OSCAL) als Architektur-Vorbild, PolyForm-lizenziert — nur Pattern, kein uebernommener Code

## Session-Referenz

Spec geschrieben in Session 2026-05-31 (Auswertung von `agentic-security`). Meeting + ADR analog BOO-86. Linear: <https://linear.app/owlist/issue/BOO-87/>. Hinweis: zunaechst als BOO-84 angelegt, storniert wegen Nummern-Drift, neu als BOO-87 gefuehrt.

## Rollout

Additiv und optional — Bestands-Projekte koennen via `migrate_boo_87()` upgegradet werden (idempotent, additiv). Die Katalog-Pflege laeuft ueber Framework-Versionen: neue/geaenderte Controls werden mit dem Katalog mit-versioniert und sind diff-bar pro Commit.
