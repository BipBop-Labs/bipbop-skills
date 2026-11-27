---
name: privacy-tyc-review
description: "Audit code against the Privacy Policy and the Terms and Conditions that apply to the repository. Use when the user asks to review a diff, PR, or module for privacy or T&C compliance (\"audita esto contra la política de privacidad\", \"¿cumple los T&C?\", \"privacy review\"), and when a change touches personal data, external providers, logs, retention or deletion, cookies, sign-up, user emails, or AI flows, also if nobody names the policy."
---

# Privacy and T&C review

Each item below turns a type of legal commitment into a signal that you can find in the code. The items tell you where to look. They do not require a finding in each category. The real commitments (providers, retention periods, roles, minimum age, excluded purposes) come from the documents of the repository, not from this skill.

## 1. Find the documents that apply

The documents in force are the truth. Different repositories can have different documents, and some have none: an internal tool, an infrastructure repo, or a product without published terms is not covered by the policy of another product of the same organization.

1. Read `AGENTS.md`, `CLAUDE.md`, and `README.md`. Look for a section that names the Privacy Policy and the T&C, and a summary of them.
2. If there is no such section, search the acceptance points in the code:

   ```
   grep -ril "privacidad\|privacy\|terminos-y-condiciones\|terms\|CookieConsent" .
   ```

If you find documents, read them (and the summary, if there is one). Before you start, write down what they declare:

- the providers that can receive personal data, and the function of each one;
- the regions where data can go;
- the categories of personal data that the product collects;
- the purposes that the product excludes;
- the retention periods and the deletion rules;
- the processing roles (controller, processor) and the data for each role;
- the user profiles, the minimum age, and the sign-up conditions;
- which document prevails for personal data.

If you find no documents, reply with this line only, and stop:

> No encontré T&C en este repo.

Do not report privacy findings. Do not audit by analogy against the documents of a different repository. Do not assume that the documents of a different product apply because the repository belongs to the same organization. If the user tells you which documents apply, audit against those.

If the summary in the repo has a different version or date than the document in force, the summary is out of date. Say so, and check each finding against the document in force before you report it.

If you have only a diff and no repository, ask which documents apply.

## 2. Procedure

1. Do the check in section 1.
2. Triage: does the change touch personal data, external services, logging, retention or deletion, cookies, auth or sign-up, emails to users, or AI flows? If not, say so in one line and stop. Inside a review that combines this skill with other guides, say nothing.
3. Go through the categories below only for what the change touches. Follow the full data flow (where the data comes from and where it goes), not only the lines in the diff.
4. Report each finding with `file:line`, the commitment that the code breaks, the document it comes from, and a specific fix.

## 3. Categories

### Data outputs and providers

- Compare each new dependency, SDK, endpoint, or webhook that sends data out of your own infrastructure with the declared providers. A new provider that receives personal data (analytics, error tracking, a different LLM, transactional email) needs a processing contract and a Policy update **before** it reaches production.
- A declared provider used for a different function than the declared one is also a finding (for example, document content sent to a metrics service).
- A new cloud resource outside the declared regions is an undeclared international transfer.
- Send to a provider only the data that its function needs. Do not send the full document when an ID is sufficient.

### Excluded purposes

If the Policy says that the product does not do something, code that does it is a blocker. Typical exclusions:

- Mass marketing, commercial ads, or third-party promotions with personal data.
- Profiling with significant legal effects.
- Automated decisions with legal effects on users (see "AI as a support tool").
- Sale, rent, or trade of personal databases.
- Use of user content to train your own models or third-party models. Make sure that the AI provider settings do not allow training on the data that you send.

### Minimization and new data

- Compare each new model or form field that collects personal data with the declared categories. A new category (location, biometrics, structured job data) needs a Policy update before you collect it.
- Do not ask for or push users to give sensitive data (health, economic situation, beliefs) if the Policy does not declare it. A new flow that collects it on purpose is a blocker. If it can arrive inside documents, keep it under the same controls as the rest of the content.
- Use technical data (logs, metrics) only for the declared purposes, usually security, audit, monitoring, error detection, and service improvement.

### Data of third parties (processor role)

This applies when the Policy says that the product processes some data on behalf of a different controller (a customer, an institution).

- Code that reads that data for the product's own purposes (product statistics, model improvements, features for other users) breaks the processing contract. A processor cannot reuse the data or decide its purposes.
- Keep controller data and processor data apart. Look for joins, exports, or pipelines that mix account data with customer content without need.

### Retention and deletion

- The declared periods are a maximum. Account deletion must delete, anonymize, or block the related data within that period, and keep a record of the deletion.
- If the Policy lets you delete inactive accounts after a notice, an automatic cleanup without that notice is a finding.
- Derived data (embeddings, vectors, extracted text, caches): a flow that deletes the source document and leaves its derived data behind is a finding.
- Do not keep data forever "just in case" in new tables, buckets, or logs without a legal obligation.

### Data subject rights

- No change can make access, correction, deletion, objection, blocking, or portability impossible. Signals: personal data in stores with no delete path (logs with no retention limit, caches with no expiry, copies that account deletion does not reach), or personal IDs embedded where you cannot delete them later.
- The product must answer an access request. You must find the data of one person by that person, not spread with no index.

### AI as a support tool

This applies when the T&C present AI as support, not as a decision.

- A model output must not cause administrative or legal effects without human review. Signal: a flow where a model output starts an act with effect on a user or a third party (approve, reject, send as final) with no human review step.
- The UI shows results as support that a person reviews, not as a decision.
- Automated processes keep a trace (prompts, responses, runs) in the declared channels, not in new undeclared channels.

### Logs and traceability

- Declared traceability (access, uploads, important operations) is a commitment. Do not remove audit logging without a replacement.
- Logs contain only what is necessary. Do not write document content, full prompts, or contact data to logs when an ID is sufficient. New personal data in application logs is a finding.

### Security

- If the documents declare encryption in transit and at rest: no http endpoints, public buckets, or new unencrypted storage.
- Keep the declared profiles apart. New endpoints check the role, and one profile cannot reach data that the Policy keeps for a different profile.
- Credentials are personal. Do not add shared accounts, long-lived tokens with no owner, or auth bypasses.
- Do not weaken existing controls (remove an auth check, widen CORS, open a port) without an explicit reason in the PR.

### Sign-up, account, and emails

- If sign-up requires acceptance of the T&C and the Policy, a new onboarding flow without that acceptance is a blocker. Record the accepted version.
- Respect the declared minimum age. Do not add flows for minors.
- If the documents give a way to close the account, do not break it or hide it.
- Non-essential emails (newsletters, announcements) need an unsubscribe option. Classify new emails: operational (no opt-out needed) or informative (opt-out needed).

### Cookies and frontend

- Without consent, use only technical cookies (session, settings). Measurement, personalization, or third-party cookies need consent first, through the product's existing consent mechanism. An analytics script that loads before consent is a finding.
- Links to the Policy and the T&C must keep working. If a PR changes those routes or URLs, make sure that every acceptance point links to the version in force.

### Incidents

- Do not hide security errors. Empty catch blocks or silenced alerts on unauthorized access break the duty to report incidents. The trace to rebuild an incident (who, what, when) must exist.

## 4. Report

Use three levels:

- **Blocker**: the code contradicts an explicit commitment of the Policy or the T&C (an excluded purpose, sensitive data requested, an automated decision with no human, personal data sent to an undeclared provider).
- **Needs legal**: the code is reasonable, but it adds a new processing, provider, purpose, or data category. The Policy needs an update, or a processing contract needs a signature, before the change reaches production. This is not a bug. It is a prerequisite.
- **Warning**: a risk or a debt (retention with no limit, a log with more personal data than necessary, orphaned derived data) that you must fix soon.

A finding is something that a person must do before the merge. Do not report:

- Code that complies or improves compliance. If everything complies, the full report is one line: `Sin hallazgos de privacidad.`
- Requests to "confirm that the Policy covers X" when you did not check. Compare with the declared data categories first.
- Risks that are not about privacy (context propagation, test coverage, design).
- Cases that the code already handles. Read the full function before you say that a check is missing.

Format: one line for each finding, `**[level]** file:line — broken commitment (source) — what to do`. Maximum 5. No intro, no summary of the change, no greeting. Inside a review that combines guides, follow the rule of that review: one list and one limit for all.

Always cite the source commitment ("Policy §4.2 — excluded purposes", "T&C ch. III.1 — limited license"), so that a person can check and discuss the finding with the document.
