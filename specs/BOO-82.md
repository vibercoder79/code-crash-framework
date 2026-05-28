# BOO-82 — Vault-Sync-Engine: `default_vault_subdir` im Team-Vertrag + inkrementeller `--since`-Sync

## Summary

Zwei Komfort-/Skalierungs-Verbesserungen an der framework-nativen Vault-Harvest-Engine (BOO-77), inspiriert von Stefans `project-template` (jetzt zugaenglich, reviewt). **Keine** Uebernahme von Stefans Code — beide Ideen framework-nativ nachgebaut:

1. **`default_vault_subdir` im Team-Vertrag** (`tracked-paths.json`): das Default-Vault-Layout steht zentral im versionierten Vertrag, nicht mehr pro Mitarbeiter in `local.json` wiederholt. `local.json path_mappings` wird zur **optionalen Ueberschreibung**.
2. **Inkrementeller `--since <sha>`-Sync**: spiegelt nur seit `<sha>` geaenderte Dateien (`git diff --name-only <sha>..HEAD`) — fuer grosse Repos.

## Why

Operator-Review von `StefanWeimarPRODOC/project-template` (Tobias, 2026-05-28): zwei genuine Verbesserungen identifiziert. Bisher musste **jeder** Mitarbeiter das komplette `path_mappings` in seiner `local.json` pflegen — Reibung und Drift-Risiko bei jedem Onboarding. Mit `default_vault_subdir` reicht im Normalfall ein leeres `path_mappings: {}`; das Layout ist Team-Konvention. Der `--since`-Sync vermeidet den vollen Glob-Walk bei jedem Lauf, wenn nur wenige Dateien neu sind.

## What

**`vault-sync.py` (Engine):**

- `_map_target()` Ziel-Aufloesung in Reihenfolge: (1) passendes `path_mappings`-Praefix aus `local.json` (laengstes gewinnt, Override), (2) `default_vault_subdir` aus dem Team-Vertrag, (3) kein Treffer → `SKIP`. Nur der Dateiname landet im `default_vault_subdir`.
- Platzhalter `{project_slug}` **und** `{slug}` werden beide ersetzt (rueckwaerts-kompatibel mit alten `{slug}`-Mappings).
- `_iter_tracked()` liefert zusaetzlich `default_vault_subdir` pro Eintrag und akzeptiert ein optionales `changed`-Set.
- `--since <sha>` Flag + `_changed_since()` (git diff). Ungueltiger SHA / kein git → WARN + Voll-Sync (kein stiller Datenverlust).
- Per-File-Logik in `_process_file()` ausgelagert (haelt `main()` flach).

**`tracked-paths.json` (Team-Vertrag):** `version: 1`, `_comment`, `default_vault_subdir` pro 4 Eintraegen mit `{project_slug}`-Platzhalter.

**`install-vault-sync.sh`:** `local.json`-Vorlage setzt `path_mappings: {}` (optionale Ueberschreibung) + erklaerendes `_comment`.

Engine-Template-Aenderung — **kein** Bootstrap-Versions-Bump noetig (Bootstrap kopiert nur die aktualisierten Files). Doku: HANDBUCH Anhang R + `vault-sync-pattern.md` (DE+EN).

## Backward-Compatibility

- Alte `local.json` mit gefuelltem `path_mappings` (auch `{slug}`) funktioniert unveraendert — Override-Pfad bleibt erste Prioritaet.
- Alte `tracked-paths.json` ohne `default_vault_subdir`: Engine faellt fuer Eintraege ohne Default auf `path_mappings` zurueck; ohne beides → `SKIP` (wie bisher).
- Pfad-Containment-Check (`realpath` gegen `vault_path`) bleibt unveraendert aktiv.

## Validation (Smoke-Test, alle gruen)

1. **`default_vault_subdir` ohne `path_mappings`** (`{}`): 3 Dateien an die Vertrags-Default-Pfade gespiegelt. ✓
2. **`path_mappings`-Override gewinnt**: Components via Override-Pfad, Rest via Default. ✓
3. **`--since <sha>`**: nur die eine seit `<sha>` geaenderte Datei gesynct. ✓
4. **Containment**: `path_mapping` mit `../ausbruch` → BLOCK, 0 Dateien ausserhalb des Vaults; Rest via Default geschrieben. ✓
5. **Frontmatter**: `type:` nur injiziert wenn fehlend, vorhandener `type:`/`title:` bleibt, `vault_sync_*` ergaenzt. ✓
6. **Ungueltiger `--since`-SHA**: WARN + Voll-Sync-Fallback. ✓
7. **Keine `local.json`**: still `exit 0`. ✓
8. **`py_compile`**: OK. ✓

## Acceptance Criteria

- [x] `default_vault_subdir` im Team-Vertrag (`tracked-paths.json`), `{project_slug}` + `{slug}` Platzhalter
- [x] `path_mappings` als optionale Ueberschreibung; `install-vault-sync.sh` Vorlage `path_mappings: {}`
- [x] `--since <sha>` inkrementeller Sync + Voll-Sync-Fallback bei ungueltigem SHA
- [x] Rueckwaerts-kompatibel (alte local.json / alte tracked-paths.json)
- [x] Lokaler Smoke-Test (8 Faelle gruen)
- [x] HANDBUCH Anhang R + `vault-sync-pattern.md` (DE+EN)
- [x] Spec + Release Notes + v0.2.0-overview

## Constraints

- Reine Python-Stdlib + Bash, keine externen Dependencies (Mac + Linux/VPS).
- Stefans Code wird **nicht** uebernommen — nur die zwei Ideen, framework-nativ implementiert.

## Dependencies

- BOO-77 (framework-native Engine). BOO-82 erweitert diese, ersetzt sie nicht.

## Session-Referenz

Spec + Umsetzung Session 2026-05-28. Operator-Review Stefans Template, Operator-Entscheidung Tobias (zwei Ideen uebernehmen, Code nicht). Linear: <https://linear.app/owlist/issue/BOO-82/>
