# Human-in-the-Loop (HITL) Checkpoints

This document defines **mandatory orchestration stop-points** where automation must halt for explicit human decision before the workflow can continue.

## Checkpoint HC-00: Submission integrity triage

- **Automation stop condition**: Submission Integrity agent emits `HIGH` or `CRITICAL` confidence for duplicate floods, missingness/schema anomalies, or suspicious pattern bursts.
- **Approver role(s)**:
  - Data Lead (required)
  - Platform Lead (required)
  - Safety/Privacy Lead (required for CRITICAL tier)
- **Required context bundle**:
  - Run metadata: `run_id`, ruleset version/hash, execution timestamp, and source node.
  - Integrity signal bundle: per-signal scores, triggered thresholds, and confidence tier rationale.
  - Affected scope: submission IDs (or cluster IDs), cohort/locale concentration, and time-window burst stats.
  - Remediation options: hold/replay list, rule-tuning proposal, and expected analyst workload impact.
- **Decision options**:
  - `APPROVE_TRIAGE_AND_CONTINUE`
  - `REQUEST_RESCAN_OR_RULE_TUNE`
  - `ESCALATE_AND_HALT`
- **Audit log schema**:

```json
{
  "checkpoint_id": "HC-00",
  "decision_id": "uuid",
  "run_id": "string",
  "requested_at": "ISO-8601",
  "decided_at": "ISO-8601",
  "integrity_confidence_tier": "HIGH|CRITICAL",
  "approvers": [
    {"role": "Data Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Platform Lead", "id": "string", "outcome": "approve|reject|abstain"}
  ],
  "decision": "APPROVE_TRIAGE_AND_CONTINUE|REQUEST_RESCAN_OR_RULE_TUNE|ESCALATE_AND_HALT",
  "rationale": "string",
  "artifacts": ["uri"],
  "schema_version": "1.0"
}
```

- **Expiry/revalidation window**:
  - Decision expires after **72 hours** or immediately if ruleset version or schema version changes.

## Checkpoint HC-01: Pre-publication of disparity signals

- **Automation stop condition**: Any run step that attempts to publish or externally expose a disparity signal (dashboard publication state change, export, or API share).
- **Approver role(s)**:
  - Data Lead (required)
  - Safety/Privacy Lead (required)
  - Product Lead (optional, required for high-severity cases)
- **Required context bundle**:
  - Run metadata: `run_id`, pipeline version/hash, execution timestamp, environment.
  - Fairness evidence: cohort definitions, sample sizes, significance outputs, confidence intervals.
  - Data quality report: missingness, duplication, drift status, and known caveats.
  - Harm assessment: potential misuse vectors and affected populations.
  - Proposed publication payload: exact figures/claims and destination channels.
- **Decision options**:
  - `APPROVE_PUBLISH`
  - `REQUIRE_REVIEW` (returns to analyst remediation queue)
  - `REJECT_PUBLISH`
- **Audit log schema**:

```json
{
  "checkpoint_id": "HC-01",
  "decision_id": "uuid",
  "run_id": "string",
  "requested_at": "ISO-8601",
  "decided_at": "ISO-8601",
  "approvers": [
    {"role": "Data Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Safety/Privacy Lead", "id": "string", "outcome": "approve|reject|abstain"}
  ],
  "decision": "APPROVE_PUBLISH|REQUIRE_REVIEW|REJECT_PUBLISH",
  "rationale": "string",
  "artifacts": ["uri"],
  "signature": "detached-signature",
  "schema_version": "1.0"
}
```

- **Expiry/revalidation window**:
  - Approval expires after **14 days** or any change in source data, cohort logic, or statistical method—whichever comes first.

## Checkpoint HC-02: Externally shared policy red-flag claims

- **Automation stop condition**: Any run step that marks policy/procurement red-flag claims for external sharing (briefing, report, regulator handoff, press, or partner bulletin).
- **Approver role(s)**:
  - Policy Analyst Lead (required)
  - Legal/Compliance Reviewer (required)
  - Safety/Privacy Lead (required for refugee/conflict contexts)
- **Required context bundle**:
  - Source document lineage: document ID, version, extraction method, language.
  - Claim evidence pack: flagged clause text, translation notes, confidence score, and competing interpretations.
  - Jurisdiction profile: governing legal context and uncertainty notes.
  - Harm forecast: potential retaliation, stigmatization, or political misuse risks.
  - Intended external audience and distribution channel.
- **Decision options**:
  - `APPROVE_EXTERNAL_CLAIM`
  - `APPROVE_WITH_QUALIFIERS`
  - `HOLD_FOR_FACT_CHECK`
  - `REJECT_EXTERNAL_CLAIM`
- **Audit log schema**:

```json
{
  "checkpoint_id": "HC-02",
  "decision_id": "uuid",
  "claim_id": "string",
  "document_id": "string",
  "requested_at": "ISO-8601",
  "decided_at": "ISO-8601",
  "approvers": [
    {"role": "Policy Analyst Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Legal/Compliance Reviewer", "id": "string", "outcome": "approve|reject|abstain"}
  ],
  "decision": "APPROVE_EXTERNAL_CLAIM|APPROVE_WITH_QUALIFIERS|HOLD_FOR_FACT_CHECK|REJECT_EXTERNAL_CLAIM",
  "qualifiers": ["string"],
  "rationale": "string",
  "artifacts": ["uri"],
  "schema_version": "1.0"
}
```

- **Expiry/revalidation window**:
  - Decision expires after **30 days**, or immediately upon source document update, translation revision, or legal-context change.

## Checkpoint HC-03: Fairness gate overrides

- **Automation stop condition**: Any request to bypass a failed fairness/quality gate for promotion, publication, or downstream automation.
- **Approver role(s)**:
  - Data Lead (required)
  - Safety/Privacy Lead (required)
  - Executive Sponsor or Program Director (required)
- **Required context bundle**:
  - Failed gate report: metric values, thresholds, failing cohorts, and confidence intervals.
  - Justification memo: operational urgency, expected impact, and compensating controls.
  - Rollback plan: trigger conditions, owner, and maximum exposure window.
  - Monitoring plan: intensified post-override checks and alert thresholds.
- **Decision options**:
  - `APPROVE_OVERRIDE_TIMEBOXED`
  - `DENY_OVERRIDE`
  - `DEFER_PENDING_MITIGATION`
- **Audit log schema**:

```json
{
  "checkpoint_id": "HC-03",
  "decision_id": "uuid",
  "gate_id": "string",
  "requested_at": "ISO-8601",
  "decided_at": "ISO-8601",
  "approvers": [
    {"role": "Data Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Safety/Privacy Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Program Director", "id": "string", "outcome": "approve|reject|abstain"}
  ],
  "decision": "APPROVE_OVERRIDE_TIMEBOXED|DENY_OVERRIDE|DEFER_PENDING_MITIGATION",
  "expires_at": "ISO-8601",
  "compensating_controls": ["string"],
  "rollback_plan_uri": "uri",
  "schema_version": "1.0"
}
```

- **Expiry/revalidation window**:
  - Maximum override validity is **7 days** and cannot be renewed without a fresh full checkpoint review.

## Checkpoint HC-04: Retention/deletion policy exceptions

- **Automation stop condition**: Any workflow request to retain data longer than policy, restore deleted data, or exempt records from scheduled deletion.
- **Approver role(s)**:
  - Safety/Privacy Lead (required)
  - Legal/Compliance Reviewer (required)
  - Data Steward (required)
- **Required context bundle**:
  - Record scope: dataset/case IDs, jurisdiction, sensitivity class.
  - Baseline policy mapping: standard retention/deletion rule and exception delta.
  - Necessity and proportionality statement.
  - Data subject risk analysis and notification obligations.
  - Technical controls: storage location, access restrictions, and deletion follow-up schedule.
- **Decision options**:
  - `APPROVE_EXCEPTION_TIMEBOXED`
  - `APPROVE_PARTIAL_SCOPE`
  - `DENY_EXCEPTION`
- **Audit log schema**:

```json
{
  "checkpoint_id": "HC-04",
  "decision_id": "uuid",
  "request_id": "string",
  "requested_at": "ISO-8601",
  "decided_at": "ISO-8601",
  "approvers": [
    {"role": "Safety/Privacy Lead", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Legal/Compliance Reviewer", "id": "string", "outcome": "approve|reject|abstain"},
    {"role": "Data Steward", "id": "string", "outcome": "approve|reject|abstain"}
  ],
  "decision": "APPROVE_EXCEPTION_TIMEBOXED|APPROVE_PARTIAL_SCOPE|DENY_EXCEPTION",
  "exception_scope": ["case_or_dataset_id"],
  "expires_at": "ISO-8601",
  "follow_up_actions": ["string"],
  "schema_version": "1.0"
}
```

- **Expiry/revalidation window**:
  - Exception expires at **90 days max** (or sooner per jurisdiction); automatic revalidation request must be raised **7 days** before expiry.
