# BOO-86 — Layer-0 PreToolUse-Bodyguard-Hook (Security ab Erzeugung)

## Summary

Neuer Claude-Code-PreToolUse-Hook, der auf `Edit|Write` feuert und unsichere Patterns (Secrets, `eval`, abgeschaltete TLS-Pruefung, SQL-Konkatenation) abfaengt, **bevor** der Code ueberhaupt geschrieben wird. Das ist ein neuer **"Layer 0"** vor Layer 2 (CLI-Linter vor Commit) und Layer 3 (CI). Geschwister-Hook zum bestehenden `spec-gate.sh` (der auf `Bash`/`git commit` feuert). Das Pattern wurde aus `agentic-security` ("pre-edit-bodyguard") nachgebaut — **kein Code uebernommen** (PolyForm-Lizenz), nur die Idee.

## Why

Heute pruefen Linter erst **nach** der Implementierung (Layer 2: CLI-Linter vor Commit) bzw. in CI (Layer 3). Die **Erzeugungs-Luecke** — der Moment, in dem unsicherer Code ueberhaupt erst entsteht — bleibt offen. Schraders Kern ist aber "sicher ab Erzeugung", nicht "sicher ab Commit". Der Bodyguard schliesst genau diese Luecke: er sitzt vor dem Schreib-Vorgang der KI und blockiert/warnt, bevor das Muster auf der Platte landet.

Konsequenzen ohne diese Story:

- Secrets und Unsafe-Patterns laufen bis zum Commit-Gate (Layer 2/3) durch — der unsichere Code existiert bis dahin bereits im Working Tree
- Teurer Rueckbau: ein bereits geschriebenes Secret muss erkannt, entfernt und ggf. rotiert werden, statt gar nicht erst zu entstehen
- USP "Security ab Generierung" fehlt — das Framework waere nur so sicher wie jedes andere Commit-Gate-Tool und verliert seine Differenzierung gegen schlankere Alternativen

## What

- **`hooks/pre-edit-bodyguard.sh`** (oder `.py`) — PreToolUse-Hook auf `Edit|Write`. Liest JSON via stdin (`tool_input` mit `file_path` + `content`), Exit 1 = blockiert, Exit 0 = erlaubt; bei Block wird die Begruendung an Claude zurueckgegeben, damit die KI das Muster korrigiert statt blind zu wiederholen.
- **Muster-Katalog `hooks/bodyguard/patterns/`:**
  - `_universal.yml` — Secrets, sprachunabhaengig (API-Keys, Tokens, Private Keys)
  - `javascript.yml`, `python.yml`, `java.yml`, `c-cpp.yml` — sprachspezifische Muster
  - Sprachauswahl anhand der Datei-Endung der zu schreibenden Datei (`.py`, `.js`, `.java`, `.c`/`.cpp`/`.h`)
- **Muster-Schema** pro Eintrag: `name`, `pattern` (Regex), `sprache`, `quelle` (CWE/OWASP/gitleaks/Semgrep-Registry — Herkunfts-Beleg pro Muster, Pflicht fuer Audit), `action: block | warn`.
- **`hooks/bodyguard/SOURCES.md`** — Quellen, Versionen, Update-Konvention, Begruendung der Kuratierung (warum genau diese Muster, warum diese Auswahl klein bleibt).
- **Schichtung Basis + Overlay:** Framework-Basis-Satz + Projekt-Overlay `.claude/bodyguard.local.yml` (Kunde erweitert/uebersteuert, ueberlebt Framework-Updates) — analog `tracked-paths.json`-Muster (Vertrags-Default + lokaler Override).
- **Bootstrap-Integration:** Hook installieren + in `settings.json` registrieren (im Phase-4.4-Bereich, wo schon Hooks gesetzt werden); `hooks-setup.md` (DE+EN) um Abschnitt **"Layer 0 / Edit-Bodyguard"** erweitern (inkl. Layer-Tabelle KI-Runtime-Hook/Git-Hook/CI-Gate); `CONVENTIONS.md`-Gate-Eintrag "Layer 0".
- **Optional `sync-bodyguard-patterns.sh`:** gleicht gegen Upstream-Quellen (Semgrep-Registry, gitleaks) ab und **schlaegt** neue Muster **vor** — Mensch entscheidet, **kein Auto-Merge** (Supply-Chain-Schutz: kein ungeprueftes Pattern aus externer Quelle in den aktiven Hook).
- **Shift-Left auf Prompt-Ebene (ergaenzend):** Secure-Coding-Hinweise im `/implement`-Skill-Prompt, damit die KI proaktiv sicherer schreibt. Hook = deterministischer Backstop, Prompt = proaktive Fuehrung.
- **HANDBUCH-Anhang (DE+EN)** "Layer 0 Edit-Bodyguard": wann/warum, Verhaeltnis zu Layer 2/3, Muster-Schichtung, Pflege.
- **`migrate_boo_86()`** (idempotent, additiv) in `migrate-to-v2.sh`; **migration-checklist** §BOO-86 (DE+EN); **Release Notes** `docs/releases/wave-*-layer0-bodyguard.md`; **bootstrap-Versions-Bump**.

## Constraints

- **Leichtgewichtig:** nur wenige, schnelle, hochsichere Muster — **kein** voller Semgrep-Lauf pro Edit (das wuerde jeden KI-Schreibvorgang ausbremsen und Operatoren zum Abschalten treiben).
- **Warnung + Eskalation statt Hard-Block-Zwang:** kuratiert, low-false-positive. Bei zu vielen Fehlalarmen entsteht Alarm-Muedigkeit → Operatoren schalten den Hook ab → Schutz auf null. Default ist deshalb Warnung; Hard-Block nur opt-in (`--strict`).
- **Pragma-Check:** wenig Operator-Overhead — der Hook laeuft automatisch im Schreib-Pfad, kein manueller Aufruf, kein Setup-Aufwand pro Edit.
- **Security-Check:** schliesst die Erzeugungs-Luecke (Layer 0) — Secrets/Unsafe-Patterns werden vor dem Schreiben abgefangen, nicht erst vor dem Commit.
- **Mittelweg-Begruendung:** Reflex statt Tiefenpruefung. Layer 0 ist ein schneller, deterministischer Reflex auf eine kleine kuratierte Muster-Menge; die **Tiefe** (vollstaendiger Scan, Datenfluss, Semgrep) bleibt bei Layer 2/3. Kein Ueber-Engineering im heissen Schreib-Pfad.
- **DE + EN konsistent** (Hook-Doku, HANDBUCH-Anhang, migration-checklist).
- **Kein Code aus `agentic-security`** (PolyForm-Lizenz) — nur das Pattern nachgebaut. Hard-Constraint fuer jeden Sub-Agent.

## Decisions

1. **Hook-Typ = PreToolUse auf `Edit|Write`** (Geschwister zu `spec-gate.sh`, das auf `Bash`/`git commit` feuert) — gleiche Infrastruktur, gleiche Aktivierungs-Logik in `settings.json`, konsistentes Doku-Bild.
2. **Muster sprachgeschichtet** (universal + per-Sprache) statt monolithisch — `_universal.yml` fuer Secrets, plus sprachspezifische Dateien, Auswahl per Datei-Endung. Weniger Fehlalarme, klarere Pflege.
3. **Schichtung Basis + Overlay** (`.claude/bodyguard.local.yml`) — Kunde erweitert/uebersteuert, Overlay ueberlebt Framework-Updates (analog `tracked-paths.json`).
4. **Quelle pro Muster ist Pflicht** (`quelle`-Feld: CWE/OWASP/gitleaks/Semgrep-Registry) — Audit-Nachweis, jedes Muster ist herkunftsbelegt, keine "magischen" Regexe.
5. **Warnung-Default statt Hard-Block** — Default ist `warn`, Hard-Block (`block`/`--strict`) ist opt-in. Verhindert Alarm-Muedigkeit und Abschalten, ohne den Schutz aufzugeben.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Mehrere klar abgegrenzte Brocken (Hook-Skript, Muster-Kataloge, Bootstrap-Integration, HANDBUCH/Doku, Migration). Pro Brocken ein fokussierter Sub-Agent. **Hard-Constraint pro Sub-Agent: "kein `agentic-security`-Code"** — nur Pattern nachbauen, PolyForm-Lizenz nicht verletzen (Memory feedback_subagent_spec_fabrication). EN-Pass nicht im selben Sub-Agent (Memory feedback_subagent_long_heredoc_timeout) — separater Pass durch Lead oder dediziertes EN-Sub-Agent pro Datei.

## Validation

- Hook blockiert (bzw. warnt) bei einem Test-Secret in einer `.py`- und einer `.js`-Datei
- Hook laesst sauberen Code ohne Treffer durch (Exit 0)
- Sprachauswahl per Datei-Endung greift (`.py` → `python.yml`, `.js` → `javascript.yml`, etc.)
- Overlay `.claude/bodyguard.local.yml` uebersteuert die Basis (lokaler Eintrag schlaegt Framework-Default)
- Jedes Muster im Katalog hat ein ausgefuelltes `quelle`-Feld
- Bootstrap registriert den Hook in `settings.json` (und Fallback `settings.local.json`)
- HANDBUCH-Anhang DE+EN im Inhaltsverzeichnis verlinkt
- `migrate_boo_86()` idempotent (zweiter Lauf erzeugt keine Diffs)
- `git diff --check` clean

## Acceptance Criteria

- [ ] `hooks/pre-edit-bodyguard.sh` (oder `.py`) liest JSON via stdin, Exit 1 = blockiert, Exit 0 = erlaubt, Begruendung an Claude bei Block
- [ ] Muster-Katalog `hooks/bodyguard/patterns/` mit `_universal.yml` + `javascript.yml` + `python.yml` + `java.yml` + `c-cpp.yml`
- [ ] Muster-Schema (`name`, `pattern`, `sprache`, `quelle`, `action`) eingehalten; jedes Muster hat `quelle`
- [ ] Sprachauswahl per Datei-Endung implementiert
- [ ] Schichtung Basis + Overlay (`.claude/bodyguard.local.yml`) funktioniert, Overlay uebersteuert Basis
- [ ] `hooks/bodyguard/SOURCES.md` mit Quellen, Versionen, Update-Konvention
- [ ] Bootstrap installiert + registriert Hook in `settings.json` (Phase 4.4)
- [ ] `hooks-setup.md` (DE+EN) um Abschnitt "Layer 0 / Edit-Bodyguard" erweitert
- [ ] `CONVENTIONS.md`-Gate-Eintrag "Layer 0"
- [ ] `sync-bodyguard-patterns.sh` schlaegt Muster vor (kein Auto-Merge) — optional
- [ ] Secure-Coding-Hinweise im `/implement`-Skill-Prompt ergaenzt
- [ ] HANDBUCH-Anhang "Layer 0 Edit-Bodyguard" (DE+EN)
- [ ] `migrate_boo_86()` implementiert (idempotent, additiv)
- [ ] migration-checklist Eintrag §BOO-86 (DE+EN)
- [ ] Release Notes `docs/releases/wave-*-layer0-bodyguard.md`
- [ ] bootstrap-Versions-Bump
- [ ] Default aktiv-als-Warnung; `--strict`/Hard-Block opt-in
- [ ] Manueller Smoke-Test: Test-Secret in `.py`/`.js` wird abgefangen, sauberer Code laeuft durch

## Dependencies

- **Baut auf:** bestehender Hook-Infrastruktur (`spec-gate.sh`, `hooks-setup.md`) — gleiche PreToolUse-Mechanik, gleiche `settings.json`-Aktivierung, Geschwister-Hook auf `Edit|Write` statt `Bash`.
- **Soft-Bezug:** Drei-Layer-Quality-Gate-ADR (2026-04-27) — der Bodyguard ist der neue **Layer 0** vor den dort definierten Layer 2 (CLI-Linter) und Layer 3 (CI).

## Session-Referenz

Spec geschrieben in Session 2026-05-31 (agentic-security-Auswertung). Meeting: `02 Projekte/Code-Crash Framework/Meetings/2026-05-31 agentic-security-Auswertung + Layer-0-Bodyguard + dpo-Katalog.md`. ADR: `02 Projekte/Code-Crash Framework/Decisions/2026-05-31 agentic-security-Adoption Bodyguard + dpo-Katalog.md`. Linear: <https://linear.app/owlist/issue/BOO-86/>. Hinweis: zunaechst als BOO-83 angelegt, storniert wegen Nummern-Drift, neu als BOO-86 angelegt.

## Rollout

Additiv und optional. Bestands-Projekte werden via `migrate_boo_86()` upgegradet (idempotent, additiv). Default ist **aktiv als Warnung** (low-false-positive, keine Alarm-Muedigkeit); `--strict`/Hard-Block ist opt-in fuer Projekte mit hoeherem Compliance-Druck.
