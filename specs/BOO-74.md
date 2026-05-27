# BOO-74 — DPO + security-architect ins Framework-Bundle aufnehmen (Vendored-Kopien)

## Naming / Decision-Korrektur-Hinweis

> **ID-Hinweis:** Diese Story wurde lokal als "BOO-73" geplant; Linear vergab beim Anlegen die naechste freie ID **BOO-74** (analog BOO-68, das urspruenglich als BOO-74 geplant war). Massgeblich ist die Linear-ID **BOO-74** — Spec-Datei, Migration-Funktion (`migrate_boo_74`) und Release-Notes folgen ihr.

Diese Spec **korrigiert** die Wave-J-Decision aus `specs/BOO-69.md` §"Wichtige Klarstellung" ("DPO bleibt Standalone analog security-architect"). Begruendung der Korrektur: wenn das Framework **Privacy-by-Design garantieren** will (Anhang O), muss der DPO-Skill aus dem Framework-Repo installierbar sein, nicht aus einem Nachbar-Repo. Gleiche Logik fuer `security-architect` — wenn Bootstrap-Frage A.4 "Security-Dimension" aktiviert, muss der Skill aus dem Framework kommen. Operator-Entscheidung (Tobias, 2026-05-27 post-Wave-L): beide Skills werden Vendored-Bundle-Skills im Framework-Repo, der Master bleibt aber `claudecodeskills`.

## Summary

DPO und security-architect werden als **vendored Bundle-Skills** ins `code-crash-framework`-Repo aufgenommen — analog zu `bootstrap/`, `ideation/`, `implement/`, etc. Master-Repo bleibt `claudecodeskills` (gepflegt via `publish_skill.py`), Framework-Repo bekommt 1:1-Kopien (inkl. References DE+EN). Bootstrap Phase 5 wird umgestellt: clont **nur** das Framework-Repo, installiert Skills aus diesem statt aus `claudecodeskills`. Bootstrap Phase 4.4n (Privacy-Setup) wird umformuliert von "Standalone installieren" auf "aus Framework-Bundle installieren". HANDBUCH Anhang O wird entsprechend angepasst. Sync-Konvention wird in der Bootstrap-Doku festgehalten: bei jedem Update von DPO/security-architect in `claudecodeskills` muss der Vendor-Mirror im Framework-Repo nachgezogen werden.

## Why

Operator-Feedback Tobias (2026-05-27 post-Wave-L): "Der DPO-Skill muss ja ins Framework mit rein. Das ist doch sinnvoll. Der Bootstrap-Prozess muss diesen Skill aus dem Code-Crash-Framework installieren, sonst macht das fuer mich keinen Sinn. Und der Security-Architekt muesste natuerlich auch ins Framework rein."

Ehrliche Bestandsaufnahme der heutigen Inkonsistenz:

- **HANDBUCH Anhang O (Wave J):** beschreibt Privacy-by-Design als Framework-Garantie ("Aktiviert Privacy-Add-on → DPO installiert"). Aber DPO selbst liegt im **Nachbar-Repo** `claudecodeskills`, nicht im Framework-Repo.
- **Bootstrap Phase 4.4n:** sagt "Skill von Code-Crash-Framework oder Skill-Repo installieren" — Operator muss selbst rausfinden, welches Repo gemeint ist.
- **Bootstrap Phase 5:** clont `claudecodeskills` und holt Skills von dort. Bundle aus Sub-Folder `code-crash-framework/`, Standalone aus Top-Level. Das setzt voraus, dass der Operator `claudecodeskills` als bestehendes Repo akzeptiert.
- **Operator-Sicht:** "Code-Crash Framework" = Framework-Repo. Wenn Privacy-Add-on aktiviert wird, sollte alles aus dem Framework-Repo kommen — nicht aus einem anderen Repo, das zufaellig denselben Maintainer hat.

Konsequenzen ohne BOO-74:

- Inkonsistente Skill-Quelle (Bundle aus Framework-Repo, Privacy/Security aus Nachbar-Repo)
- Vertriebs-Hindernis: "Wo liegt der DPO-Skill?" hat heute zwei Antworten
- Standalone-Use ohne Framework funktioniert weiter via `claudecodeskills` (das bleibt erhalten), Framework-Use bekommt aber ein konsistentes Bundle

## What

### Vendoring-Architektur

- **Master-Repo:** `vibercoder79/claudecodeskills` bleibt **Single Source of Truth** fuer DPO und security-architect. `publish_skill.py` push'd dorthin.
- **Mirror-Repo:** `vibercoder79/code-crash-framework` bekommt 1:1-Kopien unter:
  - `dpo/` (parallel zu `bootstrap/`, `ideation/`, etc.)
  - `security-architect/` (parallel zu `bootstrap/`, `ideation/`, etc.)
- **Inhalt der Vendored-Kopien:** SKILL.md, SKILL.en.md, references/* (alle DE+EN), README.md (falls vorhanden), Excalidraw-Overview-Diagramme (falls vorhanden).
- **Sync-Konvention:** bei jedem `publish_skill.py dpo` oder `publish_skill.py security-architect` muss der Framework-Repo-Mirror manuell nachgezogen werden. Ein optionales `sync_framework_mirror.sh`-Skript ist Folge-Story (BOO-74 oder spaeter), nicht Bestandteil von BOO-74.

### Bootstrap Phase 5 — Umstellung der Skill-Quelle

Heute:

```bash
SKILL_SRC=$(mktemp -d)
git clone --depth 1 https://github.com/vibercoder79/claudecodeskills "$SKILL_SRC"
# Bundle aus $SKILL_SRC/code-crash-framework/<skill>/
# Standalone aus $SKILL_SRC/<skill>/
```

Neu:

```bash
SKILL_SRC=$(mktemp -d)
git clone --depth 1 https://github.com/vibercoder79/code-crash-framework "$SKILL_SRC"
# Alle Bundle-Skills + dpo + security-architect direkt aus $SKILL_SRC/<skill>/
```

Vorteile:

- 1 Repo statt 2
- Konsistente Skill-Versionen (Framework-Tag = Skill-Tag)
- `git clone --depth 1` ist kleiner (claudecodeskills enthaelt viele Skills, Framework-Repo nur die relevanten)

Nachteile:

- Nicht-Framework-Skills wie `research`, `design-md-generator`, `setup-checklist`, `skill-creator` muessen Operator manuell installieren (oder optional via `claudecodeskills` ergaenzen). Bootstrap-Frage in Phase 5: "Zusaetzliche optionale Skills aus claudecodeskills nachziehen? [ja/nein]". Bei "ja" wird claudecodeskills ergaenzend gecloned.

### Bootstrap Phase 4.4n — Wording-Update

Heute (siehe `bootstrap/SKILL.md` Zeile 928-961):

> **Privacy-Add-on (BOO-69):** Bei `[x] Privacy / DSGVO` installiert Bootstrap zusaetzlich den `dpo`-Skill als **Standalone (analog `security-architect`)** ...
>
> 1. **DPO-Skill als Standalone installieren** (analog `security-architect`): ... wenn nicht vorhanden, Operator-Hinweis: "Installiere via `git clone` aus dem Skill-Repo oder kopiere aus dem Code-Crash-Framework".

Neu:

> **Privacy-Add-on (BOO-69, Wave M):** Bei `[x] Privacy / DSGVO` installiert Bootstrap zusaetzlich den `dpo`-Skill **aus dem Framework-Bundle** ...
>
> 1. **DPO-Skill aus Framework-Bundle installieren**: Pfad: `~/.claude/skills/dpo/` (global). Bootstrap kopiert aus `$SKILL_SRC/dpo/` (Framework-Repo) — keine externe Repo-Wahl mehr.

### HANDBUCH Anhang O — Wording-Update

Heute beschreibt Anhang O DPO als "Standalone-Skill analog security-architect". Update auf "Bundle-Skill im Framework-Repo" mit Hinweis dass `claudecodeskills` weiterhin den Master fuer Solo-Operatoren bereitstellt.

### Spec-Akzeptanz-Kriterien

- [ ] `dpo/` als Top-Level-Folder im Framework-Repo (1:1-Kopie aus `claudecodeskills/dpo/`, inkl. SKILL.md, SKILL.en.md, references/* DE+EN)
- [ ] `security-architect/` als Top-Level-Folder im Framework-Repo (1:1-Kopie aus `claudecodeskills/security-architect/`)
- [ ] Bootstrap Phase 5 Skill-Quelle umgestellt: `git clone` von `vibercoder79/code-crash-framework` statt `claudecodeskills`
- [ ] Bootstrap Phase 5 Optionen-Block aktualisiert: dpo + security-architect sind im Standard-Set, `research`/`design-md-generator`/`setup-checklist`/`skill-creator` werden via optional-zusatz-Frage ergaenzt
- [ ] Bootstrap Phase 4.4n umformuliert: "aus Framework-Bundle installieren" (DE+EN)
- [ ] HANDBUCH Anhang O Wording-Update (DE+EN): DPO als Bundle-Skill, claudecodeskills bleibt fuer Standalone-Use
- [ ] `migrate_boo_74()` in `migrate-to-v2.sh`: idempotent, prueft ob DPO + security-architect bereits unter `~/.claude/skills/` liegen; falls nicht, kopiert aus Framework-Repo
- [ ] Migration-Checklist §BOO-74 (DE+EN)
- [ ] Sync-Konvention in `bootstrap/references/skills-setup.md` dokumentiert: Master vs. Mirror, Operator-Pflicht bei Updates
- [ ] Release Notes `docs/releases/wave-m-bundle-adoption-dpo-security.md`
- [ ] Skill-Versions-Bump bootstrap auf 3.29.0 (Skill-Quelle umgestellt)

## Constraints

- **Master bleibt `claudecodeskills`** — `publish_skill.py` aendert sich nicht. Framework-Repo ist Mirror.
- **Bestehende DPO/security-architect-Installationen werden NICHT ueberschrieben.** Idempotente Migration: nur kopieren wenn nicht vorhanden.
- **Solo-Operatoren ohne Framework verlieren NICHT den Zugang.** `claudecodeskills` bleibt vollstaendig und konsumierbar.
- **DPO + security-architect inhaltlich unveraendert** — kein Versions-Bump dieser Skills durch BOO-74, nur Vendoring. (Versions-Bumps kommen wenn das Framework dort etwas inhaltlich aendert, was unwahrscheinlich ist.)
- **Sync-Aufwand ist Operator-Pflicht** — bei jedem `publish_skill.py dpo` muss der Framework-Mirror manuell aktualisiert werden. Sync-Skript ist Folge-Story, nicht Bestandteil.

## Decisions

1. **Vendoring statt Submodule** — Git-Submodule sind operationsschwer (`git submodule init`, `update`), Vendoring ist ein normales File-Copy. Bei diesem Scope (2 Skills, je ~10 Dateien) ist Vendoring leichter.
2. **Master bleibt claudecodeskills** — der Solo-Use-Case (Operator hat DPO/security-architect ohne Framework) bleibt erhalten. Wave-J-Designentscheid "Standalone-Skills sind ohne Framework nutzbar" gilt weiter — nur die Bootstrap-Installation kommt jetzt aus dem Framework-Repo.
3. **Bootstrap clont nur Framework-Repo** — die optionalen Skills wie `research`/`design-md-generator` brauchen einen separaten Pfad. Bootstrap fragt eine zusaetzliche Ja/Nein-Frage, ob claudecodeskills ergaenzend gecloned werden soll.
4. **Kein automatischer Sync** — `sync_framework_mirror.sh` ist Folge-Story. BOO-74 setzt die Mirror-Struktur einmalig auf; Updates sind Operator-Pflicht bis das Sync-Skript existiert.
5. **HANDBUCH Anhang O wird angepasst, NICHT neu geschrieben** — Wave-J-Inhalt bleibt, nur das "Standalone"-Wording wird auf "Bundle" umgestellt. Privacy-Add-on-Trigger und 3-Modi-Mapping bleiben 1:1.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell). 1 Sub-Agent fuer Vendoring (File-Copy von `claudecodeskills/dpo/` und `/security-architect/` ins Framework-Repo, mit Verifikation). Lead macht den Bootstrap-Skill-Edit (Phase 5 + Phase 4.4n), HANDBUCH-Wording-Update, Migration-Funktion, Release Notes — alles inhaltlich klar definiert, kein Sub-Agent noetig.

## Validation

- Vendoring-Test: `diff -r ~/Documents/GitHub/claudecodeskills/dpo/ ~/Documents/GitHub/code-crash-framework/dpo/` → keine Diff (ausser ggf. `.git`-Ignores).
- Bootstrap-Lauf gegen ein Test-Projekt: Phase 5 clont Framework-Repo, Phase 4.4n installiert DPO aus Framework. Smoke-Test gegen `/tmp/demo-wave-m-test`.
- HANDBUCH-Anhang-O-Diff: vorher "Standalone-Skill", nachher "Bundle-Skill". Privacy-Mechanik unveraendert.
- `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-74 --dry-run` → meldet Vendored-Pfad-Check + Operator-Hinweise.

## Acceptance Criteria

Siehe §"What" → "Spec-Akzeptanz-Kriterien" oben.

## Dependencies

- **Vorausgesetzt:** BOO-69 (Privacy-by-Design) — DPO-Skill existiert.
- **Soft-Dependency:** BOO-72 (Anhang R) — Skill-Pool-Governance referenziert dort wartungs-Owner-Rolle, Wave M passt die Wartungs-Quelle an.
- **Folge-Story (geplant, nicht in BOO-74):** Sync-Skript `sync_framework_mirror.sh` automatisiert das Mirror-Update.

## Session-Referenz

Spec geschrieben in Session 2026-05-27 nach Wave-L-Release (Commit `0eeda02`). Operator-Korrektur Tobias zur Wave-J-Decision. Daily Note: SecondBrain `05 Daily Notes/2026-05-27.md`. Linear: <https://linear.app/owlist/issue/BOO-74/>

## Rollout

Kein Feature-Flag. Bestehende Operatoren mit DPO/security-architect in `~/.claude/skills/` bleiben unveraendert. Neue Bootstrap-Laeufe nutzen die neue Skill-Quelle. Migration-Skript `migrate_boo_74()` ist idempotent und nicht-destruktiv.
