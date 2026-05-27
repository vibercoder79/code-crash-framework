---
name: dpo
description: |
  Data Protection Officer: Privacy by Design for the development process.
  3 modes: ASSESS (legal basis and DPIA at planning), REVIEW (privacy check on
  code/feature changes), AUDIT (Records of Processing Activities and compliance status).
  Covers GDPR/DSGVO (EU), BDSG (DE), and nDSG (CH).
  Use when the user says "datenschutz", "DSGVO", "GDPR", "privacy", "DPIA",
  "personal data", "personenbezogene Daten", "consent", "Einwilligung",
  "Records of Processing", "Verarbeitungsverzeichnis", "data subject rights",
  "Betroffenenrechte", "deletion policy", "Loeschkonzept", "/dpo" — or automatically
  when other skills plan or implement features with personal data.
version: 1.1.0
recommended_model: opus  # BOO-69 — compliance-critical, audit-relevant
language: en
metadata:
  hermes:
    category: governance
    tags: [privacy, gdpr, dsgvo, ndsg, compliance]
    requires_toolsets: [terminal]
    related_skills: [security-architect, architecture-review]
---

# Data Protection Officer

Privacy by Design for Claude Code — from data collection to deletion.

## Principles (Art. 5 GDPR)

Every processing of personal data MUST satisfy these principles:

| Principle | Meaning | Probing Question |
|---------|-----------|------------|
| **Lawfulness** | Legal basis required | Which Art. 6(1) letter applies? |
| **Purpose Limitation** | Only for the specified purpose | What exactly are the data collected for? |
| **Data Minimisation** | Only what is necessary | Do we really need ALL these fields? |
| **Accuracy** | Data must be correct | Are there update mechanisms? |
| **Storage Limitation** | Delete when no longer necessary | When are the data deleted? |
| **Integrity & Confidentiality** | Appropriate protection (→ Security Architect) | Are TOMs defined? |
| **Accountability** | Must be able to demonstrate compliance | Is everything documented? |

---

## 3 Modes

### Mode Selection (automatic)

```
User plans new feature with data?         → ASSESS
User changes code with data processing?   → REVIEW
User says "privacy audit"?                → AUDIT
Another skill calls DPO?                  → ASSESS or REVIEW (depending on phase)
```

---

### ASSESS Mode (Data Protection Impact Assessment)

**When:** At ideation, planning, new features — BEFORE personal data are processed.

**Workflow:**

1. **Data flow analysis**
   - Which personal data are collected?
   - Determine categories:

   | Category | Examples | Sensitivity |
   |-----------|-----------|---------------|
   | Master Data | Name, address, date of birth | Standard |
   | Contact Data | E-mail, phone | Standard |
   | Usage Data | IP, logs, click behaviour | Standard |
   | Financial Data | IBAN, credit card, transactions | Elevated |
   | Health Data | Diagnoses, medication | Special (Art. 9) |
   | Biometric Data | Fingerprint, face recognition | Special (Art. 9) |
   | Location Data | GPS, movement profiles | Elevated |
   | Minors | Data of under-16s | Special (Art. 8) |

   - Where do the data come from? (Directly from user, from third parties, automatically collected)
   - Where do they flow? (Internal, processor, third countries)

2. **Determine legal basis (Art. 6(1) GDPR)**

   | Letter | Legal Basis | Typical Use |
   |-----------|----------------|-------------------|
   | a) | **Consent** | Newsletter, tracking, cookies |
   | b) | **Contract performance** | Order processing, account management |
   | c) | **Legal obligation** | Tax retention, reporting obligations |
   | d) | **Vital interests** | Emergency contact (rare) |
   | e) | **Public interest** | Authorities, research |
   | f) | **Legitimate interest** | Fraud protection, direct marketing (with balancing test!) |

   For Art. 9 data (special categories): additionally check Art. 9(2).

3. **Conduct DPIA (Art. 35 GDPR)**
   DPIA MANDATORY when:
   - Scoring/profiling with legal effect
   - Automated decisions
   - Systematic monitoring of public areas
   - Processing special categories on a large scale
   - Combining datasets
   - Data of vulnerable persons (children, employees)
   - New technologies (AI, biometrics)

   → [references/dpia-template.en.md](references/dpia-template.en.md)

4. **Check third country transfer**
   - Data to USA/UK/other third countries?
   - Adequacy decision in place? (e.g. EU-US Data Privacy Framework)
   - If not: Standard Contractual Clauses (SCCs) + Transfer Impact Assessment
   - Cloud providers: where are the servers?

**Output:** Privacy assessment with:
- Data inventory (what data, what category)
- Legal basis per processing purpose
- DPIA (if required)
- Third country transfer assessment
- Concrete requirements for implementation

---

### REVIEW Mode (Privacy Check on Code Changes)

**When:** On code changes that affect personal data.

**Workflow:**

1. **Check data minimisation**
   - Are only the fields collected that are needed for the purpose?
   - Are data aggregated/pseudonymised where possible?
   - No unnecessary storage in logs, caches, analytics?

2. **Check consent implementation** (if consent = legal basis)
   ```
   Checklist:
   - [ ] Consent obtained BEFORE data collection
   - [ ] Freely given (no coupling-prohibition violation)
   - [ ] Informed (purpose, recipients, duration named)
   - [ ] Specific (for each purpose separately)
   - [ ] Withdrawable (as easy as granting)
   - [ ] Provable (timestamp + version stored)
   - [ ] No pre-checked checkbox
   - [ ] Double opt-in for e-mail marketing
   ```

3. **Check data subject rights**
   → [references/betroffenenrechte.en.md](references/betroffenenrechte.en.md)

   | Right | Art. | Implemented? |
   |-------|------|----------------|
   | Access | 15 | Can the user export all their data? |
   | Rectification | 16 | Can the user change their data? |
   | Erasure | 17 | Can the user request deletion? |
   | Restriction | 18 | Can processing be restricted? |
   | Data portability | 20 | Export in machine-readable format (JSON/CSV)? |
   | Objection | 21 | Opt-out for legitimate interest? |
   | Automated decisions | 22 | Right to human review? |

4. **Check deletion policy**
   - Are there defined retention periods?
   - Are data automatically deleted after expiry?
   - Are backups considered in the deletion policy?
   - Are derived data (analytics, ML models) also deleted?

5. **Privacy by Design Patterns**
   → [references/privacy-patterns.en.md](references/privacy-patterns.en.md)

**Output:** Privacy review report

```
### Privacy Review: [Feature/Change]

| # | Finding | Severity | Regulation | Recommendation |
|---|--------|---------|-----------|------------|
| 1 | E-mail logged without consent | HIGH | Art. 5/6 GDPR | Remove logging or obtain consent |
| 2 | No deletion mechanism for user data | HIGH | Art. 17 GDPR | Implement DELETE endpoint |
| 3 | Missing privacy notice for new feature | MEDIUM | Art. 13 GDPR | Update notice |

**Compliance Status:** NOT COMPLIANT / PARTIALLY COMPLIANT / COMPLIANT
**Blocker:** Yes (HIGH findings must be resolved before release)
```

---

### AUDIT Mode (Compliance Audit)

**When:** On demand ("/dpo audit"), before releases, periodically, on supervisory authority requests.

**Workflow:**

1. **Create/check Records of Processing Activities (Art. 30)**
   → [references/verarbeitungsverzeichnis.en.md](references/verarbeitungsverzeichnis.en.md)

   For each processing activity document:
   - Designation and purpose
   - Categories of data subjects and data
   - Recipients (internal + external)
   - Third country transfers
   - Retention periods
   - TOMs (reference to Security Architect)

2. **Apply all REVIEW checks** to the entire project

3. **Check information duties (Art. 13/14)**
   - Privacy notice complete and up to date?
   - All processing purposes listed?
   - Legal bases named?
   - Data subject rights explained?
   - Contact details of controller/DPO?

4. **Check processor agreements (Art. 28)**
   - All service providers with DPA captured?
   - Sub-processors documented?
   - Instruction-bound nature ensured?

5. **TOM check (Art. 32)**
   Reference to Security Architect for technical measures:
   - Encryption (at rest + in transit)
   - Pseudonymisation
   - Access control
   - Backup & recovery
   - Regular testing of measures

**Output:** Compliance audit report with:
- Records of Processing Activities (summary)
- Compliance status per processing activity
- Open measures prioritised
- Positive findings

---

## Country-Specific Regulations

### GDPR/DSGVO (EU) — Baseline

GDPR is the foundation. All checks are based primarily on it.

### BDSG (Germany) — Additions

| Topic | BDSG Particularity |
|-------|-------------------|
| DPO obligation | From 20 persons with regular data processing (§ 38) |
| Employee data protection | § 26 BDSG — own legal basis |
| Video surveillance | § 4 BDSG — stricter rules |
| Scoring | § 31 BDSG — additional requirements |
| Fines | Up to EUR 50,000 for administrative offences (in addition to GDPR) |

### nDSG (Switzerland) — Differences

→ [references/ndsg-schweiz.en.md](references/ndsg-schweiz.en.md)

| Topic | nDSG Particularity |
|-------|-------------------|
| Scope | Effects principle — also applies to Swiss data abroad |
| DPIA | "Datenschutz-Folgenabschaetzung" — similar, but DPO can be consulted instead of authority |
| Reporting obligation | "As soon as possible" to EDOEB (no 72h limit like GDPR) |
| Criminal law | Fines up to CHF 250,000 against **natural persons** (not companies!) |
| Right of access | Within 30 days (GDPR: "without undue delay", in practice 1 month) |
| Profiling | "Profiling with high risk" requires consent or law |
| Data transfer | Country list by Federal Council (not EU adequacy decisions) |

---

## Integration with Other Skills

| Calling Skill | DPO Mode | What Happens |
|-------------------|-----------|-------------|
| **Ideation** | ASSESS | Privacy assessment parallel to the story |
| **Implement** | REVIEW | Check data processing in code |
| **Security Architect** | Bidirectional | Security → provides TOMs; DPO → defines protection requirement |
| **Sprint Review** | AUDIT | Periodic privacy compliance check |

### Interplay Security Architect ↔ DPO

```
Security Architect                    DPO
       |                               |
  "What protection level?" ←──────── "Art. 9 data = HIGH"
       |                               |
  "TOMs: AES-256, RBAC,    ────────→ "TOMs for Art. 32
   Backup, Monitoring"                 documented ✓"
```

---

## References

| Document | Content |
|----------|--------|
| [dpia-template.en.md](references/dpia-template.en.md) | DPIA template per Art. 35, threshold analysis, risk assessment |
| [betroffenenrechte.en.md](references/betroffenenrechte.en.md) | Art. 15-22 in detail, deadlines, implementation patterns |
| [privacy-patterns.en.md](references/privacy-patterns.en.md) | Privacy by Design code patterns, pseudonymisation, consent flows |
| [verarbeitungsverzeichnis.en.md](references/verarbeitungsverzeichnis.en.md) | Art. 30 template, example entries, mandatory fields |
| [ndsg-schweiz.en.md](references/ndsg-schweiz.en.md) | Swiss nDSG particularities, comparison with GDPR, EDOEB |
