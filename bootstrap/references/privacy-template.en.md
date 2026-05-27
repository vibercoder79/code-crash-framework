# Privacy Template

> Rendered by `/bootstrap` as `PRIVACY.md` in the target project when the Privacy add-on is active.
> Do not write real personal data into this document.

# {{PROJECT_NAME}} — Privacy

**Version:** {{VERSION_START}} | **As of:** {{TODAY}}

## 1. Privacy Principle

Privacy is an ongoing project contract, not a final check. Anchored in Art. 25 GDPR (Privacy by Design and by Default). Every story with personal data declares its `personal_data: true` status; every relevant change documents its privacy assessment.

Operational layer: the `dpo` skill with three modes — ASSESS (story planning), REVIEW (code change), AUDIT (sprint maintenance).

## 2. Legal Bases (Art. 6(1) GDPR)

| Letter | Legal Basis | Probing Question for this Project |
|--------|-------------|------------------------------------|
| a) | Consent | Is there a freely given, informed, specific, withdrawable consent? |
| b) | Contract Performance | Is the processing necessary for performing a contract with the data subject? |
| c) | Legal Obligation | Which legal norm (HGB, AO, GwG, etc.) requires the processing? |
| d) | Vital Interests | Is it about protection of life or physical integrity? |
| e) | Public Interest | Sovereign task or public mandate? |
| f) | Legitimate Interest | What legitimate interest exists — and does it outweigh the interests of the data subject? Balancing test documented? |

**Note Art. 9 GDPR:** For special categories (health, biometrics, religion, sexual orientation, etc.) Art. 9(2) must additionally be checked — consent or specific legal basis required.

Per processing activity, the chosen legal basis must be documented in the Records of Processing (§ 3).

## 3. Records of Processing Activities (Art. 30 GDPR)

Skeleton table. Maintenance via `dpo --mode audit`.

| Processing | Purpose | Legal Basis | Data Categories | Recipients | Retention | TOMs Reference |
|------------|---------|-------------|------------------|------------|-----------|----------------|
| {{EXAMPLE_PROCESSING}} | {{PURPOSE}} | Art. 6(1)({{LIT}}) | {{CATEGORIES}} | {{RECIPIENTS}} | {{DELETION_PERIOD}} | → SECURITY.md §TOMs |

Full record: see `dpo` skill references (`verarbeitungsverzeichnis.en.md`). Mandatory from 250 employees, in practice almost always recommended.

## 4. Deletion Policy

Retention periods per data category. Cite retention periods from sector law — do not invent.

| Data Category | Retention Period | Legal Basis of Period | Deletion Mechanism | Verification |
|---------------|------------------|------------------------|---------------------|--------------|
| Commercial letters | 6 years | § 257 HGB | {{MECHANISM}} | {{VERIFICATION}} |
| Accounting vouchers / Invoices | 10 years | § 257 HGB, § 147 AO, § 14b UStG | {{MECHANISM}} | {{VERIFICATION}} |
| Application documents | 6 months | AGG deadline | {{MECHANISM}} | {{VERIFICATION}} |
| Payroll records | 6 years | § 257 HGB | {{MECHANISM}} | {{VERIFICATION}} |
| Contract data | 3 years after end | § 195 BGB | {{MECHANISM}} | {{VERIFICATION}} |
| Server logs (with IP) | Max. 7 days | Legitimate interest | Automatic log rotation | {{VERIFICATION}} |
| Marketing profiles | Until withdrawal | Consent (Art. 6(1)(a)) | Immediately after opt-out | {{VERIFICATION}} |
| {{OTHER_CATEGORY}} | see sector specification | {{LAW}} | {{MECHANISM}} | {{VERIFICATION}} |

Backups: include in deletion cycle. Derived data (analytics, ML models) also deleted.

## 5. Data Subject Rights (Art. 15-22 GDPR)

| Right | Article | Deadline (Art. 12) | Process | Responsible |
|-------|---------|---------------------|---------|--------------|
| Access | 15 | 1 month | {{ACCESS_PROCESS}} | {{ROLE}} |
| Rectification | 16 | Without undue delay | {{RECTIFICATION_PROCESS}} | {{ROLE}} |
| Erasure | 17 | Without undue delay | {{ERASURE_PROCESS}} | {{ROLE}} |
| Restriction | 18 | Without undue delay | {{RESTRICTION_PROCESS}} | {{ROLE}} |
| Data portability | 20 | 1 month | {{PORTABILITY_PROCESS}} | {{ROLE}} |
| Objection | 21 | Without undue delay | {{OBJECTION_PROCESS}} | {{ROLE}} |

Request intake channel: {{INTAKE_CHANNEL}} (e.g. e-mail to `privacy@{{PROJECT_DOMAIN}}`).

Identity verification: required before disclosure, but not excessively (proportionate).

## 6. Personal Data Paths

Code paths that process personal data are stored as patterns in a separate JSON file — analogous to Sensitive Paths in `SECURITY.md`.

Bootstrap can create a file `.claude/personal-data-paths.json` and/or `.codex/personal-data-paths.json`. On code changes in such paths, `/implement` Step 5.5b is a HARD GATE.

Examples:

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

Operator maintenance: extend patterns with every new personal data processing.

## 7. Privacy-by-Design Process

The `dpo` skill provides three modes, each with a clear trigger point in the pipeline:

| Mode | Trigger | Pipeline Position | Output |
|------|---------|--------------------|--------|
| ASSESS | Story plans new processing of personal data | `/ideation` Step 0e (`personal_data: true`) | `dpia/DPIA-<feature>.md` from template, legal basis chosen |
| REVIEW | Code change hits personal-data-paths | `/implement` Step 5.5b (Personal-Data-Paths-Gate) | Privacy findings inline + `journal/reports/local/<date>_<story>/privacy.md` |
| AUDIT | Every N sprints (default 4, configurable) | `/sprint-review` Step 7c | Records-of-Processing diff in sprint report, open compliance items |

Flow of a story with `personal_data: true`:

1. `/ideation` Step 0e detects personal-data reference → triggers `dpo --mode assess`
2. DPO ASSESS writes DPIA draft or references existing DPIA
3. `/implement` Step 5.5b checks on code change in personal-data-paths → triggers `dpo --mode review`
4. DPO REVIEW documents findings, blocks on HIGH findings
5. `/implement` Step 6e adds privacy findings to security-findings documentation
6. `/sprint-review` Step 7c (every N sprints) triggers DPO AUDIT for records-of-processing maintenance

## 8. Incident Note (Privacy Breach)

For a personal data breach (Art. 4(12) GDPR — accidental or unlawful destruction, loss, alteration, unauthorised disclosure or access):

Notification thresholds:
- **Art. 33 GDPR:** notification to supervisory authority within **72 hours** of becoming aware, if risk to rights and freedoms exists
- **Art. 34 GDPR:** notification of data subjects in case of **high risk**
- **nDSG Art. 24:** notification to EDOEB "as soon as possible" (no fixed deadline)

Incident block (to be filled in per incident):

```
- What happened? [Brief description of the breach]
- When (point of awareness)? [Date + time]
- Which data / data categories? [List]
- Approximate number of data subjects? [Number]
- Risk assessment: low / medium / high [Reasoning]
- Immediate measures: [What was done]
- Follow-up measures: [What will be done]
- Notification to authority: [Yes/No, date, reference number]
- Notification of data subjects: [Yes/No, date, channel]
- Lessons learned: [Entry in journal/ + sprint-review]
```

Reference: `SECURITY.md` §Incident Note for security-specific incidents. For a privacy incident, both inputs are needed — DPO assesses legally, security-architect technically.
