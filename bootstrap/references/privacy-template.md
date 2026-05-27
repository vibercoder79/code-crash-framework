# Privacy Template

> Wird von `/bootstrap` als `PRIVACY.md` im Zielprojekt gerendert, wenn das Privacy-Add-on aktiviert ist.
> Keine echten personenbezogenen Daten in dieses Dokument schreiben.

# {{PROJECT_NAME}} — Privacy

**Version:** {{VERSION_START}} | **Stand:** {{TODAY}}

## 1. Privacy-Grundsatz

Datenschutz ist ein laufender Projektvertrag, kein Abschluss-Check. Verankert nach Art. 25 DSGVO (Privacy by Design and by Default). Jede Story mit personenbezogenen Daten benennt ihren `personal_data: true`-Status; jede relevante Aenderung dokumentiert ihre Datenschutz-Bewertung.

Operative Schicht: der `dpo`-Skill mit drei Modi — ASSESS (Story-Planung), REVIEW (Code-Aenderung), AUDIT (Sprint-Pflege).

## 2. Rechtsgrundlagen (Art. 6 Abs. 1 DSGVO)

| Buchstabe | Rechtsgrundlage | Pruef-Frage fuer dieses Projekt |
|-----------|-----------------|----------------------------------|
| a) | Einwilligung | Liegt eine freiwillige, informierte, spezifische, widerrufbare Einwilligung vor? |
| b) | Vertragserfuellung | Ist die Verarbeitung fuer die Erfuellung eines Vertrags mit der betroffenen Person erforderlich? |
| c) | Rechtliche Verpflichtung | Welche Rechtsnorm (HGB, AO, GwG, etc.) verlangt die Verarbeitung? |
| d) | Lebenswichtige Interessen | Geht es um Schutz von Leben oder koerperlicher Unversehrtheit? |
| e) | Oeffentliches Interesse | Hoheitliche Aufgabe oder oeffentlicher Auftrag? |
| f) | Berechtigtes Interesse | Welches berechtigte Interesse besteht — und ueberwiegt es die Interessen der Betroffenen? Interessenabwaegung dokumentiert? |

**Hinweis Art. 9 DSGVO:** Bei besonderen Kategorien (Gesundheit, Biometrie, Religion, sexuelle Orientierung, etc.) ist zusaetzlich Art. 9 Abs. 2 zu pruefen — Einwilligung oder spezifische gesetzliche Grundlage erforderlich.

Pro Verarbeitungstaetigkeit ist die gewaehlte Rechtsgrundlage im Verarbeitungsverzeichnis (§ 3) zu dokumentieren.

## 3. Verarbeitungsverzeichnis (Art. 30 DSGVO)

Skelett-Tabelle. Pflege via `dpo --mode audit`.

| Verarbeitung | Zweck | Rechtsgrundlage | Datenkategorien | Empfaenger | Loeschfrist | TOMs-Verweis |
|--------------|-------|-----------------|-----------------|------------|-------------|--------------|
| {{EXAMPLE_PROCESSING}} | {{PURPOSE}} | Art. 6(1)({{LIT}}) | {{CATEGORIES}} | {{RECIPIENTS}} | {{DELETION_PERIOD}} | → SECURITY.md §TOMs |

Vollstaendiges Verzeichnis: siehe `dpo`-Skill References (`verarbeitungsverzeichnis.md`). Pflicht ab 250 Mitarbeitenden, in der Praxis quasi immer empfohlen.

## 4. Loeschkonzept

Loeschfristen pro Datenkategorie. Aufbewahrungsfristen aus Branchenrecht zitieren, nicht erfinden.

| Datenkategorie | Aufbewahrungsfrist | Rechtsgrundlage der Frist | Loesch-Mechanismus | Verifikation |
|----------------|---------------------|----------------------------|---------------------|--------------|
| Handelsbriefe | 6 Jahre | § 257 HGB | {{MECHANISM}} | {{VERIFICATION}} |
| Buchungsbelege / Rechnungen | 10 Jahre | § 257 HGB, § 147 AO, § 14b UStG | {{MECHANISM}} | {{VERIFICATION}} |
| Bewerbungsunterlagen | 6 Monate | AGG-Frist | {{MECHANISM}} | {{VERIFICATION}} |
| Lohnabrechnungen | 6 Jahre | § 257 HGB | {{MECHANISM}} | {{VERIFICATION}} |
| Vertragsdaten | 3 Jahre nach Vertragsende | § 195 BGB | {{MECHANISM}} | {{VERIFICATION}} |
| Server-Logs (mit IP) | Max. 7 Tage | Berechtigtes Interesse | Automatisches Log-Rotation | {{VERIFICATION}} |
| Marketing-Profile | Bis Widerruf | Einwilligung (Art. 6(1)(a)) | Sofort nach Opt-Out | {{VERIFICATION}} |
| {{OTHER_CATEGORY}} | siehe Branchen-Spezifikation | {{LAW}} | {{MECHANISM}} | {{VERIFICATION}} |

Backups: in den Loesch-Zyklus einbeziehen. Abgeleitete Daten (Analytics, ML-Modelle) mitloeschen.

## 5. Betroffenenrechte (Art. 15-22 DSGVO)

| Recht | Artikel | Frist (Art. 12) | Prozess | Verantwortlicher |
|-------|---------|-----------------|---------|------------------|
| Auskunft | 15 | 1 Monat | {{ACCESS_PROCESS}} | {{ROLE}} |
| Berichtigung | 16 | Unverzueglich | {{RECTIFICATION_PROCESS}} | {{ROLE}} |
| Loeschung | 17 | Unverzueglich | {{ERASURE_PROCESS}} | {{ROLE}} |
| Einschraenkung | 18 | Unverzueglich | {{RESTRICTION_PROCESS}} | {{ROLE}} |
| Datenuebertragbarkeit | 20 | 1 Monat | {{PORTABILITY_PROCESS}} | {{ROLE}} |
| Widerspruch | 21 | Unverzueglich | {{OBJECTION_PROCESS}} | {{ROLE}} |

Antrag-Eingangsweg: {{INTAKE_CHANNEL}} (z.B. E-Mail an `privacy@{{PROJECT_DOMAIN}}`).

Identitaetspruefung: vor Auskunft erforderlich, aber nicht uebertrieben (verhaeltnismaessig).

## 6. Personal-Data-Paths

Code-Pfade, die personenbezogene Daten verarbeiten, werden in einer separaten JSON-Datei als Pattern hinterlegt — analog zu Sensitive Paths in `SECURITY.md`.

Bootstrap kann eine Datei `.claude/personal-data-paths.json` und/oder `.codex/personal-data-paths.json` erzeugen. Bei Code-Aenderung in solchen Pfaden ist `/implement` Schritt 5.5b HARD GATE.

Beispiele:

```json
{
  "patterns": [
    "**/user*",
    "**/customer*",
    "**/profile*",
    "**/*pii*",
    "**/auth/profile/**",
    "**/billing/**",
    "**/onboarding/**",
    "db/migrations/*personal*"
  ]
}
```

Operator-Pflege: Pattern erweitern bei jeder neuen Personal-Data-Verarbeitung.

## 7. Privacy-by-Design-Ablauf

Der `dpo`-Skill liefert drei Modi, jeder mit klarem Trigger-Punkt in der Pipeline:

| Modus | Trigger | Pipeline-Stelle | Output |
|-------|---------|------------------|--------|
| ASSESS | Story plant neue Verarbeitung personenbezogener Daten | `/ideation` Schritt 0e (`personal_data: true`) | `dpia/DPIA-<feature>.md` aus Template, Rechtsgrundlage gewaehlt |
| REVIEW | Code-Aenderung trifft personal-data-paths | `/implement` Schritt 5.5b (Personal-Data-Paths-Gate) | Privacy-Findings inline + `journal/reports/local/<date>_<story>/privacy.md` |
| AUDIT | Alle N Sprints (Default 4, konfigurierbar) | `/sprint-review` Schritt 7c | Verarbeitungsverzeichnis-Diff im Sprint-Report, offene Compliance-Punkte |

Ablauf einer Story mit `personal_data: true`:

1. `/ideation` Schritt 0e erkennt Personal-Data-Bezug → triggert `dpo --mode assess`
2. DPO ASSESS schreibt DPIA-Entwurf oder verweist auf vorhandene DPIA
3. `/implement` Schritt 5.5b prueft bei Code-Aenderung in personal-data-paths → triggert `dpo --mode review`
4. DPO REVIEW dokumentiert Befunde, blockiert bei HOCH-Findings
5. `/implement` Schritt 6e ergaenzt Privacy-Findings zur Security-Findings-Doku
6. `/sprint-review` Schritt 7c (alle N Sprints) triggert DPO AUDIT fuer Verarbeitungsverzeichnis-Pflege

## 8. Incident-Notiz (Datenschutz-Vorfall)

Bei einer Datenschutzverletzung (Art. 4 Nr. 12 DSGVO — unbeabsichtigte oder unrechtmaessige Vernichtung, Verlust, Veraenderung, unbefugte Offenlegung oder Zugriff):

Meldepflicht-Schwellen:
- **Art. 33 DSGVO:** Meldung an Aufsichtsbehoerde innerhalb **72 Stunden** ab Kenntnis, wenn Risiko fuer Rechte und Freiheiten besteht
- **Art. 34 DSGVO:** Benachrichtigung der Betroffenen bei **hohem Risiko**
- **nDSG Art. 24:** Meldung an EDOEB "so rasch als moeglich" (keine fixe Frist)

Incident-Block (auszufuellen pro Vorfall):

```
- Was ist passiert? [Kurzbeschreibung der Verletzung]
- Wann (Erkenntnis-Zeitpunkt)? [Datum + Uhrzeit]
- Welche Daten / Datenkategorien? [Liste]
- Anzahl Betroffener (ungefaehr)? [Zahl]
- Risikobewertung: niedrig / mittel / hoch [Begruendung]
- Sofortmassnahmen: [Was wurde getan]
- Folge-Massnahmen: [Was wird getan]
- Meldung an Behoerde: [Ja/Nein, Datum, Aktenzeichen]
- Benachrichtigung Betroffene: [Ja/Nein, Datum, Kanal]
- Lessons Learned: [Eintrag in journal/ + sprint-review]
```

Verweis: `SECURITY.md` §Incident-Notiz fuer Security-spezifische Vorfaelle. Bei Privacy-Incident sind beide Inputs noetig — DPO bewertet rechtlich, Security-Architect technisch.
