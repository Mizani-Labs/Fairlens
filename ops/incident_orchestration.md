# Incident Orchestration Runbook

This runbook defines coordinated incident response for **fairness**, **privacy**, and **localization harm** events.

## Incident Coordinator Agent Assignment

- **Assigned agent:** `Incident Coordinator` (IC)
- **Role:** Owns incident command from declaration to closure; coordinates triage owner actions, status updates, containment verification, and resume authorization workflow.
- **Coverage:** 24/7 on-call rotation.
- **Handoff rule:** If IC is unavailable for 10 minutes, escalation auto-assigns backup IC from ML Ops leadership rotation.

## Global Response Clock

- **T0:** Alert or escalation received and incident declared.
- **T0 + 10m:** IC confirms severity and assigns triage owner.
- **T0 + 30m:** Immediate containment actions completed or explicit blocker logged.
- **T0 + 60m:** Initial impact assessment shared in incident channel.

---

## 1) Fairness Harm Event

### Trigger conditions

Any one of the following:
- Monitored cohort disparity exceeds approved gate threshold for two consecutive intervals.
- Fairness audit finds materially disparate outcomes that were not detected by monitors.
- Partner/user escalation shows pattern of discriminatory outcomes by protected or policy-monitored cohort.

### Immediate containment actions

1. Pause publication/routing for impacted model route, cohort segment, or policy path.
2. Quarantine outputs since earliest suspected onset timestamp.
3. Roll back to last known-good model/policy checkpoint.
4. Enable stricter fairness fallback guardrails (lower release threshold, additional manual review).

### Triage owner and response SLA

- **Triage owner:** Fairness On-Call Reviewer.
- **IC support owner:** ML Ops Incident Coordinator.
- **SLA:**
  - Owner assigned: **10 minutes** from T0.
  - Blast-radius assessment: **60 minutes** from T0.
  - Interim mitigation plan posted: **120 minutes** from T0.

### Evidence collection checklist

- [ ] Alert metadata (metric IDs, thresholds, trigger times, cohorts).
- [ ] Cohort-wise metrics (baseline vs incident window).
- [ ] Sample decisions with model confidence and adjudication notes.
- [ ] Model/policy/feature snapshot IDs and rollout ring.
- [ ] Quarantine and pause audit logs (actor, time, scope).
- [ ] Incident timeline and stakeholder notifications.

### Resume criteria

- Reprocessed/rollback outputs meet fairness acceptance thresholds across required cohorts.
- Two consecutive monitoring intervals are within control bounds.
- Dual sign-off from Fairness owner and IC.

### Post-incident review artifacts

- Incident timeline with detection-to-containment durations.
- Root-cause analysis and fairness failure taxonomy.
- User/partner impact quantification by cohort.
- Corrective action plan with owners and due dates.
- Monitor/guardrail change log and validation results.

---

## 2) Privacy Harm Event (Suspected Re-identification or Leakage)

### Trigger conditions

Any one of the following:
- PII/linkage-risk detector breach above SEV-1 threshold.
- Confirmed report of potentially identifying content in outputs/logs.
- Security/partner escalation indicating unauthorized exposure path.

### Immediate containment actions

1. Immediately pause affected endpoints, exports, and partner sync jobs.
2. Quarantine incident-window data and enforce restricted access partition.
3. Revoke or rotate affected credentials/tokens.
4. Freeze deletion-retention jobs that could destroy forensic evidence.

### Triage owner and response SLA

- **Triage owner:** Privacy/Security Incident Response Lead.
- **IC support owner:** ML Ops Incident Coordinator.
- **SLA:**
  - Owner assigned: **5 minutes** from T0.
  - Initial exposure assessment: **30 minutes** from T0.
  - Containment completeness confirmation: **60 minutes** from T0.

### Evidence collection checklist

- [ ] Detector payloads, confidence scores, and trigger timestamps.
- [ ] Sanitized samples of suspected leaking outputs.
- [ ] Access/auth/export logs and endpoint traces.
- [ ] Token/credential rotation records.
- [ ] Data lineage and storage location map for impacted records.
- [ ] Legal/compliance notification decision log.

### Resume criteria

- Leak vector is confirmed blocked with no active exposure path.
- Required legal/compliance review and required notifications are complete.
- Privacy regression tests pass in staging/canary.
- Security Lead + Legal/Compliance + IC sign-off completed.

### Post-incident review artifacts

- Breach classification memo (suspected vs confirmed).
- Forensic summary and exploitability assessment.
- Exposure scope report and impacted entity counts.
- Containment/eradication validation report.
- Preventive controls backlog and implementation dates.

---

## 3) Localization Harm Event

### Trigger conditions

Any one of the following:
- Translation quality/safety monitor detects source-target meaning divergence above threshold.
- Multilingual QA confirms harmful mistranslation (e.g., slur insertion, negation loss, context inversion).
- Regional partner/user escalation reports locale-specific harmful output pattern.

### Immediate containment actions

1. Pause impacted language pairs/locales/model versions.
2. Quarantine suspect translated outputs and halt downstream syndication.
3. Route traffic to approved fallback path (prior model or human-reviewed glossary mode).
4. Hard-block high-risk terms/entities list pending fix validation.

### Triage owner and response SLA

- **Triage owner:** Localization Quality On-Call.
- **IC support owner:** ML Ops Incident Coordinator.
- **SLA:**
  - Owner assigned: **15 minutes** from T0.
  - Locale impact assessment: **90 minutes** from T0.
  - Fallback/remediation plan posted: **180 minutes** from T0.

### Evidence collection checklist

- [ ] Source text, translated text, and back-translation comparisons.
- [ ] Language pair/locale, model version, prompt/glossary config.
- [ ] Harm labels and reviewer adjudication notes.
- [ ] Publication pause/quarantine logs.
- [ ] Complaint references and response timeline.
- [ ] Regional escalation and communications record.

### Resume criteria

- Validation set for impacted locales passes safety and semantic fidelity thresholds.
- Human QA spot-check passes for high-risk term/entity set.
- Localization owner + Trust & Safety + IC sign-off completed.

### Post-incident review artifacts

- Locale-specific failure taxonomy and recurrence risk score.
- Root-cause report (model, glossary, prompt, or data contribution).
- Impact report by language/region.
- Remediation pack (dataset/glossary updates, guardrail changes, reviewer playbook updates).
- Verification report showing fixes in canary before full restore.

---

## Communication and Closure Requirements (All Incident Types)

- IC posts status updates at least every 30 minutes until containment, then hourly until closure.
- Closure requires:
  - All resume criteria met.
  - Post-incident review artifacts drafted within 2 business days.
  - Follow-up owners assigned for every corrective action.
