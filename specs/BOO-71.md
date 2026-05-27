# BOO-71 — HANDBUCH Anhang Q: Souveraenitaets-Stack-Guide + LLM-Proxy-Hook

## Summary

HANDBUCH-Anhang Q "Souveraenitaets-Stack-Guide" (DE+EN): vollstaendige Tabelle EU-konformer Alternativen fuer alle Stack-Komponenten (Code-Hosting, Vault-Sync, LLM-Endpoints, Issue-Tracker, CI), plus Migrations-Anleitungen pro Komponente. Im `environment.json` ein einzelner Hook-Punkt `llm_proxy_url`, der Operatoren erlaubt, einen Anonymisierungs- oder Souveraenitaets-Proxy davorzuschalten (z.B. Microsoft Presidio, AWS Bedrock-Proxy). **KEINE Anonymisierungs-Engine im Framework selbst.**

## Why

Operator-Feedback (Martin, 2026-05-27): bei Beratungsarbeit in regulierten Branchen ist die Default-Stack-Zusammensetzung (GitHub, Anthropic USA, iCloud) nicht souveraenitaetskonform. Heute fehlt im Framework und HANDBUCH jeglicher Hinweis auf EU-konforme Alternativen oder einen Proxy-Hook-Punkt. Pragmatische Loesung: Inspirations-Schicht im HANDBUCH + 1 Config-Feld fuer Operator-Override. Keine Anonymisierungs-Engine im Framework — das ist Runtime-Infrastruktur, nicht Governance.

Konsequenzen ohne diese Story:

- Operatoren mit Souveraenitaets-Anforderungen finden im HANDBUCH keine Orientierung
- Anonymisierungs-Proxy-Pattern (z.B. Presidio) hat keinen Hook-Punkt im Framework → muss komplett ausserhalb laufen, ohne Cost-Tracking-Integration
- US-Cloud-Default ist alternativlos dokumentiert → wirkt unsensibel bei Audit/Kunde

## What

- **HANDBUCH-Anhang Q "Souveraenitaets-Stack-Guide"** (DE+EN), Sektionen:
  - **Tabelle EU-konforme Alternativen** (Komponente, US-Default, EU-Alternative, Tradeoff):
    - Code-Hosting: GitHub → Codeberg (Forgejo), GitLab Self-hosted
    - Vault-Sync: iCloud / Obsidian Sync → Syncthing, Hetzner Storage Box + Git-Sync
    - LLM: Anthropic / OpenAI USA → Mistral La Plateforme EU, AWS Bedrock Frankfurt (mit CLOUD-Act-Restrisiko), Ollama lokal
    - Issue-Tracker: Linear → Plane (self-hosted), GitLab Issues
    - CI: GitHub Actions → Forgejo Actions, Drone CI auf Hetzner
  - **Pro Komponente:** Migrations-Anleitung (kurze Schritt-fuer-Schritt-Liste, kein vollstaendiger Setup-Guide; Verweis auf externe Dokumentation)
  - **Decision-Matrix:** "Wann lohnt der Souveraenitaets-Switch?" (regulierte Branche / Behoerden-Auftrag / personenbezogene Daten Tier 3 / NIS-2-Pflichtsektor)
  - **LLM-Proxy-Hook-Punkt:** Erklaerung was `llm_proxy_url` macht, Beispiel-Setup mit Microsoft Presidio als Anonymisierungs-Proxy (read-only Doku, kein Setup-Skript im Framework)
- **`environment.json` Schema-Erweiterung:** neues optionales Feld `llm_proxy_url: <url>` (Default: null = direkter LLM-Call); Doku-Verweis auf Anhang Q
- **`bootstrap` Generator** beruehrt Feld NUR wenn bereits vorhanden (kein neuer Pflicht-Schritt im Bootstrap)
- **`/implement` Doku-Block:** wie `llm_proxy_url` interpretiert wird (read-only Erklaerung — real-routing-Implementation ist Operator-Aufgabe; Framework bietet nur den Hook und den Verlauf-Output)
- **HANDBUCH-Inhaltsverzeichnis** aktualisiert
- **Release Notes** Eintrag in `docs/releases/wave-k-deployment-scenarios.md` (gemeinsam mit BOO-70)
- **migration-checklist Eintrag** §BOO-71 (DE+EN): neues optionales Feld in environment.json

## Constraints

- **KEINE Anonymisierungs-Engine im Framework** — nur Hook-Punkt
- **KEINE LLM-Provider-spezifische Implementation** (kein Mistral-/AWS-/Ollama-Client-Code) — nur Doku
- Bootstrap aendert sich NICHT (kein neuer Interview-Schritt) — `llm_proxy_url` ist Power-User-Feld
- DE + EN konsistent
- Migrations-Anleitungen pro Komponente kurz halten (kein vollstaendiger Setup-Guide; Operator soll auf externe Docs/Tutorials verwiesen werden)

## Decisions

1. **1 Hook-Punkt statt Engine** — Anonymisierung ist Runtime-Infrastruktur, gehoert nicht ins Framework
2. **Bootstrap unangefasst** — Souveraenitaets-Stack ist Operator-Wahl, nicht Standard-Pfad
3. **HANDBUCH als Inspirations-Schicht**, nicht als Voll-Setup-Guide — Operator entscheidet pro Komponente und folgt externen Setup-Anleitungen
4. **Microsoft Presidio als Beispiel-Proxy** im Anhang erwaehnt, NICHT als Pflicht-Empfehlung — andere Tools (spaCy, eigene Lambda) gleichwertig
5. **Wave K = BOO-70 + BOO-71 zusammen released** — beide adressieren Operator-Wahl bei Setup, thematisch verwandt

## Agent-Pattern

**Gewaehltes Pattern:** linear.

**Begruendung:** Reine Doku-Story mit klar abgegrenztem Scope. 1 HANDBUCH-Anhang DE+EN, 1 Config-Feld-Erweiterung. Sub-Agent-Overhead nicht gerechtfertigt.

## Validation

- HANDBUCH-Anhang Q (DE+EN) hat alle 5 Komponenten in der Tabelle + pro-Komponente-Sektion
- `environment.json`-Schema dokumentiert `llm_proxy_url`-Feld als optional
- `/implement` Doku erwaehnt das Feld + Verweis auf Anhang Q
- Cross-Reference im Inhaltsverzeichnis DE+EN
- Manueller Smoke-Test: `environment.json` mit `llm_proxy_url: "http://localhost:8000"` wird vom Bootstrap-Generator nicht ueberschrieben

## Acceptance Criteria

- [ ] HANDBUCH-Anhang Q (DE) mit Tabelle + Pro-Komponente-Migrations-Anleitungen + Decision-Matrix + LLM-Proxy-Hook-Sektion
- [ ] HANDBUCH-Anhang Q (EN) konsistent
- [ ] HANDBUCH-Inhaltsverzeichnis aktualisiert (DE+EN)
- [ ] `bootstrap/references/environment-json-schema.md` (oder Pendant) um `llm_proxy_url`-Feld erweitert
- [ ] `/implement` Doku-Block: wie `llm_proxy_url` interpretiert wird (Read-only-Erklaerung, kein Routing-Code)
- [ ] Release Notes `docs/releases/wave-k-deployment-scenarios.md` (gemeinsam mit BOO-70 in Wave K)
- [ ] migration-checklist Eintrag (neues optionales Feld in environment.json)

## Dependencies

- Keine Hard-Dependencies. BOO-70 (Deployment-Szenarien) ist verwandt und kann gemeinsam in Wave K released werden.
- **Soft-Dependency:** BOO-84 (Token-Effizienz-Policy) — `model_overrides:` und `llm_proxy_url` koennten konzeptionell zusammen in einer CLAUDE.md-Sektion stehen.

## Session-Referenz

Spec geschrieben in Session 2026-05-27 nach Operator-Feedback Martin. Daily Note: SecondBrain 05 Daily Notes/2026-05-27.md. Linear: <https://linear.app/owlist/issue/BOO-71/>

## Rollout

Kein Feature-Flag noetig — reines optionales Config-Feld + Doku. Bestands-Projekte unveraendert (Default `llm_proxy_url: null` = direkter LLM-Call wie bisher).
