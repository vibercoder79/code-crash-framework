# INTENTRON — Q&A

Stand: 2026-05-20

Dieses Dokument sammelt operative Fragen, die beim Arbeiten mit INTENTRON entstehen. Es ergänzt das große `HANDBUCH.md`: Das Handbuch erklärt das System zusammenhängend, dieses Q&A beantwortet konkrete Praxisfragen.

## Umsetzung, Linter und Hooks

### Arbeitet die KI mit ESLint, SonarQube/SonarLint und Semgrep in Echtzeit?

Nicht im gleichen Sinn wie ein Mensch in VS Code mit roten Wellenlinien. Die KI sieht Editor-Plugins wie ESLint, SonarLint oder Error Lens normalerweise nicht live im UI. Sie arbeitet mit diesen Prüfern über eine kontrollierte Feedback-Schleife:

```text
Code schreiben
-> Linter / Tests / Semgrep / Security-Gates ausführen
-> Ergebnis lesen
-> Code korrigieren
-> erneut prüfen
-> bis grün oder sauber begründet
```

Das ist nicht permanente Live-Synchronisation, sondern die `Validate-Fix-Learn`-Schleife des Frameworks. Für den Operator wirkt es oft fast wie Echtzeit, technisch ist es aber eine nachgelagerte, sehr schnelle Iteration.

### Welche Rolle spielen die Hooks?

Hooks stellen sicher, dass die KI die Prüfungen nicht nur freiwillig erwähnt, sondern an verbindlichen Punkten daran vorbeikommt:

| Ebene | Zweck | Wirkung |
|---|---|---|
| Lokale Linter/Tester | ESLint, Ruff, Tests, Typecheck | KI führt sie aus, liest Fehler und korrigiert |
| Semgrep / Security Gates | SAST, Secrets-/Security-Regeln | Findings müssen behoben oder dokumentiert werden |
| Pre-Commit Hooks | z.B. Spec-Gate, Dependency-Check, Semgrep | blockieren Commits, wenn Pflichtbedingungen fehlen |
| Pre-Push / CI Gates | GitHub Actions, SonarQube, weitere Reports | verhindern, dass ungeprüfte Änderungen in die Cloud wandern |
| `/implement`-Protokoll | strukturierte Validierung vor Abschluss | dokumentiert Evidenz, offene Risiken und Doku-Impact |

Das Framework verlässt sich also nicht darauf, dass KI-Code "schon sauber" ist. Es zwingt den Arbeitsfluss durch objektive Prüfer.

### Kann die KI Fehler selbst korrigieren?

Ja, wenn sie die Tool-Ausgaben sehen kann. Der typische Ablauf ist:

1. KI ändert Code.
2. KI führt `npm run lint`, `npm test`, `semgrep` oder projektspezifische Checks aus.
3. KI liest konkrete Fehlermeldungen.
4. KI patcht die betroffenen Dateien.
5. KI führt die Checks erneut aus.

Erst wenn die Checks grün sind oder eine Ausnahme bewusst dokumentiert ist, darf die Story weiter Richtung Abschluss. Genau dafür existieren `/implement`, lokale Hooks und CI-Gates.

### Warum reicht es nicht, wenn die KI "guten Code" schreibt?

Die KI kann lint-freundlichen Code antizipieren, aber sie kennt den tatsächlichen Projektzustand erst nach Ausführung der lokalen Tools. Projektregeln, Versionen, lokale ESLint-/Ruff-Konfiguration, TypeScript-Settings, Semgrep-Regeln, Security-Hooks und CI-Verhalten können sich unterscheiden.

Darum gilt:

> KI kann erwartungsgemäß sauber schreiben, aber verlässlich sauber wird es erst durch ausgeführte Checks.

### Was bedeutet das für den Operator?

Der Operator muss nicht jede Linter-Regel selbst kennen. Wichtig ist, dass die Projektpipeline aktiv ist:

- lokale Checks sind installiert,
- Hooks sind registriert,
- CI läuft im GitHub-Repo,
- `/implement` dokumentiert die Validierung,
- Ausnahmen werden bewusst begründet.

Wenn diese Infrastruktur steht, arbeitet die KI nicht "blind", sondern iteriert gegen dieselben Qualitätsgates, die auch ein menschliches Engineering-Team nutzen würde.
