[🇬🇧 English](#english) · [🇩🇪 Deutsch](#deutsch)

---

<a name="english"></a>

# Security Architect — Claude Code Skill

> **Security by Design** for the entire development process — from first idea to production code.
> A Claude Code skill that brings professional security engineering into every session.

**Version:** 1.1.0 | **License:** MIT | **Platform:** Claude Code (Anthropic)

---

## What This Skill Does

The Security Architect skill turns Claude Code into a full security engineering partner. Instead of treating security as an afterthought, it integrates threat modeling, code review, and auditing directly into your development workflow — automatically triggered at the right moments.

**The core problem it solves:** Most developers either skip security entirely or run a checklist at the end. This skill makes security a natural part of how you build — before code is written, while it's being written, and before it ships.

### New in v1.1.0: SKILL-SCAN Mode
Before installing skills from GitHub or other external sources, the SKILL-SCAN mode checks them for **prompt injection attacks** — malicious instructions hidden in SKILL.md files that could hijack Claude's behavior, exfiltrate your credentials, or manipulate your system configuration.

---

## Four Operating Modes

```
User is planning / brainstorming?        → DESIGN   (Threat Modeling)
User is writing / changing code?         → REVIEW   (Code Security Check)
User says "audit" / "scan"?              → AUDIT    (Full Security Scan)
User wants to install a skill/plugin?    → SKILL-SCAN (Prompt Injection Check)
```

### Mode 1: DESIGN — Threat Modeling

Triggered **before** code is written, during planning and architecture decisions.

**What happens:**
1. System scope is defined: data flows, trust boundaries, external interfaces
2. STRIDE analysis for each component and interface
3. DREAD risk scoring (1–10) for every identified threat
4. Concrete security requirements are formulated for implementation

**STRIDE Framework:**

| Threat | Question | Countermeasure |
|--------|----------|----------------|
| **S**poofing | Can someone impersonate another entity? | Strong auth, MFA |
| **T**ampering | Can data be manipulated? | Integrity checks, signatures |
| **R**epudiation | Can someone deny their actions? | Audit logs, digital signatures |
| **I**nformation Disclosure | Can confidential data leak? | Encryption, access controls |
| **D**enial of Service | Can the service be disabled? | Rate limiting, redundancy |
| **E**levation of Privilege | Can someone gain unauthorized rights? | RBAC, least privilege |

**DREAD Scoring:** Each threat rated 1–10 across Damage, Reproducibility, Exploitability, Affected Users, Discoverability.

**Output:** Threat model report with threat table, risk scores, and prioritized security requirements.

---

### Mode 2: REVIEW — Code Security Check

Triggered automatically **while code is being changed**, or on demand.

**What happens:**
1. Risk classification of the change (HIGH / MEDIUM / LOW)
2. OWASP Top 10:2025 quick check against the diff
3. Language-specific secure code patterns verified
4. Secrets check (no API keys, passwords, or tokens in code)
5. Security headers audit (for web applications)

**OWASP Top 10:2025 Checks:**

| # | Vulnerability | Check |
|---|---------------|-------|
| A01 | Broken Access Control | Auth on every endpoint? Deny by default? |
| A02 | Security Misconfiguration | Secure defaults? Debug disabled? |
| A03 | Supply Chain Failures | Versions locked? Integrity checked? |
| A04 | Cryptographic Failures | TLS 1.2+? AES-256-GCM? Argon2/bcrypt? |
| A05 | Injection | Parameterized queries? Input validation? |
| A06 | Insecure Design | Threat model present? Rate limiting? |
| A07 | Auth Failures | MFA? Breached-password check? |
| A08 | Integrity Failures | Signed packages? SRI for CDN? |
| A09 | Logging Failures | Security events logged? Alerting? |
| A10 | Exception Handling | Fail-closed? No internals exposed? |

**Output format:**
```
### Security Review: [change description]

| # | Finding | Severity | File:Line | Recommendation |
|---|---------|----------|-----------|----------------|
| 1 | SQL query with string concat | HIGH | api.py:42 | Use parameterized query |
| 2 | Missing rate limiting | MEDIUM | auth.py:15 | Add rate limiter middleware |

Risk Assessment: MEDIUM
Blocker: Yes (HIGH findings = blocker)
```

---

### Mode 3: AUDIT — Full Security Scan

Triggered on demand (`/security audit`), before releases, or periodically.

**What happens:**
1. All REVIEW checks applied to the entire codebase
2. Dependency analysis — known vulnerabilities, abandoned packages, unnecessary dependencies
3. Configuration review — production settings, CORS, database permissions, secrets management
4. Attack surface mapping — all public endpoints, which accept user input, which modify state

**Also covers Agentic AI Security (OWASP ASI01–ASI10)** for projects that use AI agents, MCP servers, or tool-calling systems.

**Output:** Complete audit report with overall risk rating (Low / Medium / High / Critical), findings sorted by severity, action plan with priorities, and positive findings.

---

### Mode 4: SKILL-SCAN — Prompt Injection Check for Skills

Triggered **before installing any external skill** from GitHub or other sources.

This mode addresses a specific threat in the Claude Code ecosystem: a malicious SKILL.md file could contain hidden instructions that hijack Claude's behavior, read your credentials, modify your global settings, or perform destructive operations — without you ever noticing.

**What happens:**
1. **Metadata check** — do name, description, and actual content match? Unknown author / no versioning / missing repo → elevated scrutiny
2. **Prompt injection scan** — 8 attack categories checked (see reference file)
3. **Scope check** — does the skill do more than its description promises?
4. **False-positive filter** — legitimate skills often contain security examples, CLAUDE.md read access, or shell commands that are documented and scoped

**8 Attack Categories:**

| Category | What's Checked |
|----------|----------------|
| Override / Hijacking | Instructions attempting to override Claude's behavior |
| Exfiltration | Access to sensitive files, API keys, credentials |
| Privilege Escalation | Claimed permissions that were never granted |
| Destructive Actions | `rm -rf`, `git reset --hard`, mass deletion |
| Settings Manipulation | Writes to `CLAUDE.md`, `settings.json` |
| Indirect Injection | External URLs that could load instructions |
| Hidden Instructions | HTML comments, Unicode tricks, invisible text |
| Social Engineering | Fake metadata, impersonation, urgency framing |

**Severity scale:** `CRITICAL` → `HIGH` → `MEDIUM` → `NOTE`

**Output format:**
```
### SKILL-SCAN: my-skill v1.0.0

| # | Category | Severity | Line | Finding |
|---|----------|----------|------|---------|
| 1 | Exfiltration | CRITICAL | 42 | Reads ~/.ssh/id_rsa and transmits content |
| 2 | Override | HIGH | 15 | "Ignore all previous instructions" |

Overall Assessment: DANGEROUS
Recommendation: Do not install

Reason: Two critical findings indicate intentional malicious behavior.
```

---

## Supported Languages (Code Patterns)

JavaScript / TypeScript · Python · Go · Rust · Java · PHP · C / C++ · Bash

---

## Standards & References

| Standard | Coverage |
|----------|----------|
| OWASP Top 10:2025 | All 10 categories, every REVIEW and AUDIT run |
| OWASP ASVS 5.0 | 3 levels: all apps / sensitive data / critical systems |
| OWASP LLM Top 10 | LLM01 Prompt Injection, supply chain for AI systems |
| OWASP Agentic AI (ASI01–ASI10) | Agent security, tool misuse, memory attacks |
| STRIDE / DREAD | Threat modeling framework for DESIGN mode |
| MITRE ATLAS | AML.T0054 Prompt Injection (SKILL-SCAN reference) |

---

## Interfaces with Other Skills

Other skills can call Security Architect directly:

```
"Check the security aspects of this change"   → triggers REVIEW
"Create a threat model for this feature"      → triggers DESIGN
"Run a security audit"                        → triggers AUDIT
"Scan this skill before I install it"         → triggers SKILL-SCAN
```

| Calling Skill | Security Mode | Result |
|---------------|---------------|--------|
| `ideation` | DESIGN | Threat model created in parallel with user story |
| `implement` | REVIEW | Code changes reviewed before commit |
| `architecture-review` | DESIGN + AUDIT | Architecture extended with security dimension |
| `sprint-review` | AUDIT | Periodic security health check |
| `skill-creator` | SKILL-SCAN | Prompt-injection check before installing external skills |

---

## Trigger Phrases

The skill activates automatically when you say:

- `/security`, `security`, `sicherheit`
- `threat model`, `threat modeling`
- `security review`, `security audit`
- `is this secure?`, `ist das sicher?`
- `OWASP`, `ASVS`
- `scan this skill`, `scanne diesen skill`
- `skill-scan`, `pruefe diesen skill`

---

## File Structure

```
security-architect/
├── README.md                              ← This file
├── SKILL.md                               ← Skill definition (loaded by Claude Code)
└── references/
    ├── threat-modeling.md                 ← STRIDE/DREAD details, auth patterns, Zero Trust
    ├── owasp-checklist.md                 ← OWASP Top 10:2025, ASVS 5.0, ASI01-ASI10
    ├── secure-code-patterns.md            ← Secure vs. insecure patterns per language
    ├── supply-chain.md                    ← Dependency analysis, risk scoring, audit tools
    └── prompt-injection-patterns.md       ← 8 attack categories for SKILL-SCAN mode
```

**SKILL.md** is the file Claude Code reads and executes. It contains the router logic, all four mode workflows, and references to the detail files in `references/`.

**Reference files** are loaded on demand — only when the specific mode needs them. This keeps the context window lean.

---

## Installation

### Option A: From this repository
```bash
cp -r security-architect ~/.claude/skills/security-architect
```

### Option B: Clone the full skills collection
```bash
git clone https://github.com/<your-repo>/claudecodeskills ~/Documents/GitHub/claudecodeskills
cp -r ~/Documents/GitHub/claudecodeskills/security-architect ~/.claude/skills/security-architect
```

### Verify installation
```bash
ls ~/.claude/skills/security-architect/
# Should show: README.md  SKILL.md  references/
```

After installation, Claude Code picks up the skill automatically on the next session start. No configuration needed.

---

## Design Principles

The skill is built on five non-negotiable principles:

1. **Defense in Depth** — Never rely on a single security measure
2. **Fail Closed** — On errors, deny access rather than allow it
3. **Least Privilege** — Grant only the minimum permissions needed
4. **Assume Breach** — Always assume attackers are already in the system
5. **Evidence-Based** — Every finding includes a concrete reason and line number

These principles guide every recommendation the skill makes.

---

## Security Note on This Skill Itself

This skill follows its own SKILL-SCAN criteria:

- It does **not** read files outside its own directory (except CLAUDE.md for global rules, read-only)
- It does **not** make external network requests
- It does **not** modify any system configuration
- All shell command examples are clearly labeled as examples, not executable instructions
- The `references/` directory contains documentation only, no executable code

You can verify this by running `/security` and providing this skill's own SKILL.md as input.

---

## Changelog

### v1.1.0 — 2026-03-10
- **Added: SKILL-SCAN mode** — Prompt injection check for external skills before installation
- **Added: `references/prompt-injection-patterns.md`** — 8 attack categories with concrete patterns, false-positive filter, and sources (OWASP LLM Top 10, MITRE ATLAS, Simon Willison)
- Fixed: Removed unsupported `version` field from SKILL.md frontmatter
- Updated: Decision tree in SKILL.md includes SKILL-SCAN triggers

### v1.0.0 — 2026-03-09
- Initial release
- DESIGN mode: STRIDE/DREAD threat modeling
- REVIEW mode: OWASP Top 10:2025, secure code patterns, secrets check
- AUDIT mode: full project scan including dependency and configuration review
- 4 reference files: threat-modeling, owasp-checklist, secure-code-patterns, supply-chain
- Language support: JS/TS, Python, Go, Rust, Java, PHP, C/C++, Bash

---

## License

MIT License — free to use, modify, and distribute.

---

*Built for [Claude Code](https://claude.ai/claude-code) by Anthropic.*

---

---

<a name="deutsch"></a>

# Security Architect — Claude Code Skill

> **Security by Design** fuer den gesamten Entwicklungsprozess — von der ersten Idee bis zum Produktivcode.
> Ein Claude-Code-Skill, der professionelles Security-Engineering in jede Session bringt.

**Version:** 1.1.0 | **Lizenz:** MIT | **Plattform:** Claude Code (Anthropic)

---

## Was der Skill tut

Der Security-Architect-Skill macht Claude Code zum vollwertigen Security-Engineering-Partner. Statt Security als Nachgedanken zu behandeln, integriert er Threat Modeling, Code Review und Auditing direkt in den Entwicklungs-Workflow — automatisch zum richtigen Zeitpunkt ausgeloest.

**Das Kernproblem:** Die meisten Entwickler ueberspringen Security komplett oder laufen am Ende eine Checkliste durch. Der Skill macht Security zum natuerlichen Teil des Bauens — bevor Code geschrieben wird, waehrend er geschrieben wird und bevor er ausgeliefert wird.

### Neu in v1.1.0: SKILL-SCAN-Modus
Bevor Skills aus GitHub oder anderen externen Quellen installiert werden, prueft der SKILL-SCAN-Modus sie auf **Prompt-Injection-Attacken** — bösartige Anweisungen, die in SKILL.md-Dateien versteckt sein koennten, um Claudes Verhalten zu kapern, Zugangsdaten abzugreifen oder Systemkonfiguration zu manipulieren.

---

## Vier Betriebsmodi

```
Nutzer plant / brainstormt?                 → DESIGN   (Threat Modeling)
Nutzer schreibt / aendert Code?             → REVIEW   (Code-Security-Check)
Nutzer sagt "Audit" / "Scan"?               → AUDIT    (Voller Security-Scan)
Nutzer will Skill/Plugin installieren?      → SKILL-SCAN (Prompt-Injection-Check)
```

### Modus 1: DESIGN — Threat Modeling

Ausgeloest **bevor** Code geschrieben wird, waehrend Planung und Architektur-Entscheidungen.

**Was passiert:**
1. System-Scope wird definiert: Datenfluesse, Trust-Grenzen, externe Interfaces
2. STRIDE-Analyse pro Komponente und Interface
3. DREAD-Risk-Scoring (1–10) fuer jeden identifizierten Threat
4. Konkrete Security-Requirements fuer die Implementation formuliert

**STRIDE-Framework:**

| Threat | Frage | Gegenmassnahme |
|--------|-------|----------------|
| **S**poofing | Kann jemand eine andere Identitaet vortaeuschen? | Strong Auth, MFA |
| **T**ampering | Koennen Daten manipuliert werden? | Integrity Checks, Signaturen |
| **R**epudiation | Kann jemand Aktionen abstreiten? | Audit Logs, digitale Signaturen |
| **I**nformation Disclosure | Koennen vertrauliche Daten leaken? | Verschluesselung, Access Controls |
| **D**enial of Service | Kann der Service lahmgelegt werden? | Rate Limiting, Redundanz |
| **E**levation of Privilege | Kann jemand unberechtigte Rechte bekommen? | RBAC, Least Privilege |

**DREAD-Scoring:** Jeder Threat 1–10 bewertet in Damage, Reproducibility, Exploitability, Affected Users, Discoverability.

**Output:** Threat-Model-Report mit Threat-Tabelle, Risiko-Scores und priorisierten Security-Requirements.

---

### Modus 2: REVIEW — Code-Security-Check

Ausgeloest automatisch **waehrend Code-Aenderungen**, oder auf Abruf.

**Was passiert:**
1. Risiko-Klassifikation der Aenderung (HIGH / MEDIUM / LOW)
2. OWASP Top 10:2025 Quick-Check gegen den Diff
3. Sprachspezifische Secure-Code-Patterns verifiziert
4. Secrets-Check (keine API-Keys, Passwoerter, Tokens im Code)
5. Security-Headers-Audit (fuer Web-Apps)

**OWASP Top 10:2025 Checks:**

| # | Schwachstelle | Check |
|---|---------------|-------|
| A01 | Broken Access Control | Auth auf jedem Endpoint? Deny by Default? |
| A02 | Security Misconfiguration | Secure Defaults? Debug aus? |
| A03 | Supply Chain Failures | Versions-Pinning? Integritaet geprueft? |
| A04 | Cryptographic Failures | TLS 1.2+? AES-256-GCM? Argon2/bcrypt? |
| A05 | Injection | Parameterisierte Queries? Input Validation? |
| A06 | Insecure Design | Threat Model vorhanden? Rate Limiting? |
| A07 | Auth Failures | MFA? Breached-Password-Check? |
| A08 | Integrity Failures | Signierte Packages? SRI fuer CDN? |
| A09 | Logging Failures | Security-Events geloggt? Alerting? |
| A10 | Exception Handling | Fail-Closed? Keine Internals exponiert? |

**Output-Format:**
```
### Security Review: [Beschreibung der Aenderung]

| # | Finding | Severity | File:Line | Empfehlung |
|---|---------|----------|-----------|------------|
| 1 | SQL-Query mit String-Concat | HIGH | api.py:42 | Parameterisierte Query nutzen |
| 2 | Rate Limiting fehlt | MEDIUM | auth.py:15 | Rate-Limiter-Middleware hinzufuegen |

Risk Assessment: MEDIUM
Blocker: Ja (HIGH findings = Blocker)
```

---

### Modus 3: AUDIT — Voller Security-Scan

Ausgeloest auf Abruf (`/security audit`), vor Releases, oder periodisch.

**Was passiert:**
1. Alle REVIEW-Checks auf die gesamte Codebase angewendet
2. Dependency-Analyse — bekannte Schwachstellen, verlassene Packages, unnoetige Dependencies
3. Konfigurations-Review — Produktions-Settings, CORS, DB-Permissions, Secrets-Management
4. Attack-Surface-Mapping — alle public Endpoints, welche User-Input akzeptieren, welche State aendern

**Deckt auch Agentic AI Security (OWASP ASI01–ASI10)** fuer Projekte mit KI-Agents, MCP-Servern oder Tool-Calling-Systemen.

**Output:** Kompletter Audit-Report mit Gesamt-Risiko-Rating (Low / Medium / High / Critical), Findings nach Severity sortiert, Action Plan mit Prioritaeten, und positive Findings.

---

### Modus 4: SKILL-SCAN — Prompt-Injection-Check fuer Skills

Ausgeloest **bevor ein externer Skill installiert wird** aus GitHub oder anderen Quellen.

Dieser Modus adressiert einen spezifischen Threat im Claude-Code-Oekosystem: Eine boesartige SKILL.md-Datei koennte versteckte Anweisungen enthalten, die Claudes Verhalten kapern, Credentials lesen, globale Settings aendern oder destruktive Operationen ausfuehren — ohne dass du es bemerkst.

**Was passiert:**
1. **Metadaten-Check** — passen Name, Description und tatsaechlicher Inhalt zusammen? Unbekannter Autor / keine Versionierung / fehlendes Repo → erhoehte Skepsis
2. **Prompt-Injection-Scan** — 8 Angriffs-Kategorien geprueft (siehe Referenzdatei)
3. **Scope-Check** — macht der Skill mehr als seine Description verspricht?
4. **False-Positive-Filter** — legitime Skills enthalten oft Security-Beispiele, CLAUDE.md-Read-Zugriff oder dokumentierte, scopierte Shell-Commands

**8 Angriffs-Kategorien:**

| Kategorie | Was geprueft wird |
|-----------|-------------------|
| Override / Hijacking | Anweisungen die Claudes Verhalten ueberschreiben |
| Exfiltration | Zugriff auf sensible Dateien, API-Keys, Credentials |
| Privilege Escalation | Behauptete Berechtigungen die nie gewaehrt wurden |
| Destructive Actions | `rm -rf`, `git reset --hard`, Massen-Deletion |
| Settings Manipulation | Writes auf `CLAUDE.md`, `settings.json` |
| Indirect Injection | Externe URLs die Instructions laden koennten |
| Hidden Instructions | HTML-Kommentare, Unicode-Tricks, unsichtbarer Text |
| Social Engineering | Fake-Metadaten, Impersonation, Urgency-Framing |

**Severity-Skala:** `CRITICAL` → `HIGH` → `MEDIUM` → `NOTE`

**Output-Format:**
```
### SKILL-SCAN: my-skill v1.0.0

| # | Kategorie | Severity | Zeile | Finding |
|---|-----------|----------|-------|---------|
| 1 | Exfiltration | CRITICAL | 42 | Liest ~/.ssh/id_rsa und uebertraegt Inhalt |
| 2 | Override | HIGH | 15 | "Ignore all previous instructions" |

Gesamtbewertung: DANGEROUS
Empfehlung: Nicht installieren

Grund: Zwei kritische Findings deuten auf intentional boesartiges Verhalten hin.
```

---

## Unterstuetzte Sprachen (Code-Patterns)

JavaScript / TypeScript · Python · Go · Rust · Java · PHP · C / C++ · Bash

---

## Standards & Referenzen

| Standard | Abdeckung |
|----------|-----------|
| OWASP Top 10:2025 | Alle 10 Kategorien, jeder REVIEW- und AUDIT-Lauf |
| OWASP ASVS 5.0 | 3 Levels: alle Apps / sensible Daten / kritische Systeme |
| OWASP LLM Top 10 | LLM01 Prompt Injection, Supply Chain fuer KI-Systeme |
| OWASP Agentic AI (ASI01–ASI10) | Agent-Security, Tool-Misuse, Memory-Attacks |
| STRIDE / DREAD | Threat-Modeling-Framework fuer DESIGN-Modus |
| MITRE ATLAS | AML.T0054 Prompt Injection (SKILL-SCAN-Referenz) |

---

## Schnittstellen zu anderen Skills

Andere Skills koennen Security Architect direkt aufrufen:

```
"Pruef die Security dieser Aenderung"          → triggert REVIEW
"Erstell ein Threat Model fuer dieses Feature" → triggert DESIGN
"Fuehr ein Security-Audit aus"                 → triggert AUDIT
"Scan diesen Skill bevor ich ihn installiere"  → triggert SKILL-SCAN
```

| Aufrufender Skill | Security-Modus | Ergebnis |
|-------------------|----------------|----------|
| `ideation` | DESIGN | Threat Model parallel zur Story erstellt |
| `implement` | REVIEW | Code-Aenderungen vor Commit reviewed |
| `architecture-review` | DESIGN + AUDIT | Architektur um Security-Dimension erweitert |
| `sprint-review` | AUDIT | Periodischer Security-Gesundheits-Check |
| `skill-creator` | SKILL-SCAN | Prompt-Injection-Check vor Installation externer Skills |

---

## Trigger-Phrasen

Der Skill aktiviert sich automatisch bei:

- `/security`, `security`, `sicherheit`
- `threat model`, `threat modeling`
- `security review`, `security audit`
- `is this secure?`, `ist das sicher?`
- `OWASP`, `ASVS`
- `scan this skill`, `scanne diesen skill`
- `skill-scan`, `pruefe diesen skill`

---

## Dateistruktur

```
security-architect/
├── README.md                              ← Diese Datei
├── SKILL.md                               ← Skill-Definition (wird von Claude Code geladen)
└── references/
    ├── threat-modeling.md                 ← STRIDE/DREAD-Details, Auth-Patterns, Zero Trust
    ├── owasp-checklist.md                 ← OWASP Top 10:2025, ASVS 5.0, ASI01-ASI10
    ├── secure-code-patterns.md            ← Secure vs. Insecure Patterns pro Sprache
    ├── supply-chain.md                    ← Dependency-Analyse, Risk-Scoring, Audit-Tools
    └── prompt-injection-patterns.md       ← 8 Angriffs-Kategorien fuer SKILL-SCAN-Modus
```

**SKILL.md** ist die Datei die Claude Code liest und ausfuehrt. Enthaelt die Router-Logik, alle vier Mode-Workflows und Referenzen zu Detail-Dateien in `references/`.

**Referenz-Dateien** werden on-demand geladen — nur wenn der jeweilige Mode sie braucht. Haelt das Context-Window schlank.

---

## Installation

### Option A: Aus diesem Repo
```bash
cp -r security-architect ~/.claude/skills/security-architect
```

### Option B: Gesamte Skills-Sammlung klonen
```bash
git clone https://github.com/<dein-repo>/claudecodeskills ~/Documents/GitHub/claudecodeskills
cp -r ~/Documents/GitHub/claudecodeskills/security-architect ~/.claude/skills/security-architect
```

### Installation verifizieren
```bash
ls ~/.claude/skills/security-architect/
# Sollte zeigen: README.md  SKILL.md  references/
```

Nach Installation wird der Skill bei der naechsten Session automatisch erkannt. Keine Config noetig.

---

## Design-Prinzipien

Der Skill baut auf fuenf non-negotiable Prinzipien:

1. **Defense in Depth** — Nie auf eine einzige Security-Massnahme verlassen
2. **Fail Closed** — Bei Fehlern Zugriff verweigern, nicht erlauben
3. **Least Privilege** — Nur minimale noetige Permissions vergeben
4. **Assume Breach** — Immer annehmen Angreifer sind schon im System
5. **Evidence-Based** — Jedes Finding mit konkretem Grund und Zeilen-Nummer

Diese Prinzipien leiten jede Empfehlung des Skills.

---

## Security-Hinweis zum Skill selbst

Der Skill folgt seinen eigenen SKILL-SCAN-Kriterien:

- Er liest **keine** Dateien ausserhalb seines eigenen Ordners (ausser CLAUDE.md fuer globale Regeln, read-only)
- Er macht **keine** externen Netzwerk-Requests
- Er aendert **keine** System-Konfiguration
- Alle Shell-Command-Beispiele sind klar als Beispiele markiert, nicht als ausfuehrbare Anweisungen
- Der `references/` Ordner enthaelt nur Dokumentation, keinen ausfuehrbaren Code

Verifizierbar: `/security` ausfuehren und die eigene SKILL.md als Input geben.

---

## Changelog

### v1.1.0 — 2026-03-10
- **Neu: SKILL-SCAN-Modus** — Prompt-Injection-Check fuer externe Skills vor Installation
- **Neu: `references/prompt-injection-patterns.md`** — 8 Angriffs-Kategorien mit konkreten Patterns, False-Positive-Filter und Quellen (OWASP LLM Top 10, MITRE ATLAS, Simon Willison)
- Fix: Unsupported `version`-Feld aus SKILL.md-Frontmatter entfernt
- Update: Decision-Tree in SKILL.md enthaelt SKILL-SCAN-Trigger

### v1.0.0 — 2026-03-09
- Initial Release
- DESIGN-Mode: STRIDE/DREAD Threat Modeling
- REVIEW-Mode: OWASP Top 10:2025, Secure-Code-Patterns, Secrets-Check
- AUDIT-Mode: kompletter Projekt-Scan inkl. Dependency- und Config-Review
- 4 Referenz-Dateien: threat-modeling, owasp-checklist, secure-code-patterns, supply-chain
- Sprachen: JS/TS, Python, Go, Rust, Java, PHP, C/C++, Bash

---

## Lizenz

MIT-Lizenz — frei nutzbar, modifizierbar, weiterverteilbar.

---

*Gebaut fuer [Claude Code](https://claude.ai/claude-code) von Anthropic.*
