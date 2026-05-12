# Incident Orchestration Runbook

This runbook defines scenario-driven incident response flows for high-risk operational events in the Fairlens pipeline.

## Severity and SLA Defaults

- **SEV-1 (Critical):** Ongoing or likely user harm, privacy breach risk, or broad policy impact.  
  - Acknowledge in **15 minutes**.  
  - Containment started in **30 minutes**.
- **SEV-2 (High):** Material quality, safety, or fairness degradation with limited spread.  
  - Acknowledge in **30 minutes**.  
  - Containment started in **60 minutes**.
- **SEV-3 (Medium):** Isolated issue, no active downstream propagation.  
  - Acknowledge in **4 hours**.  
  - Containment started in **1 business day**.

## 1) False-Positive Harm Event Flow

A false-positive harm event occurs when benign content is incorrectly flagged as harmful, leading to unnecessary suppression or disruption.

### Detection sources

- Automated monitor alerts (spike in harm classifications with stable external baselines).
- Analyst report identifying over-blocking patterns.
- Partner escalation citing unjustified suppression outcomes.

### Immediate containment actions by agent

1. **Pause publication** for impacted segments, policy class, or model version.
2. **Quarantine outputs** from the suspect window into an incident bucket; prevent downstream consumption.
3. Switch to last known-good decision policy/model checkpoint.
4. Mark current model/policy as **investigation-locked** to block retraining or deployment promotion.

### Triage ownership and max response times

- **Primary owner:** On-call Trust & Safety Analyst.
- **Secondary owner:** ML Ops Incident Commander.
- **Support:** Fairness Reviewer, Partner Success lead (if partner-impacting).
- **Max response targets:**
  - Owner assignment: **15 minutes** from alert.
  - Initial impact assessment: **60 minutes**.
  - Mitigation plan posted: **2 hours**.

### Required evidence logs

- Alert metadata (rule ID, threshold, trigger timestamps, impacted cohorts).
- Sampling of false-positive cases with rationale and confidence values.
- Model/policy version, feature store snapshot ID, and rollout ring.
- Publication pause and quarantine action logs (actor, timestamp, scope).
- Communication trail (incident channel summary, partner notices if sent).

### Post-incident review template

- Incident ID, severity, start/end timestamps.
- Detection path and time-to-detect.
- Root cause analysis (taxonomy drift, threshold miscalibration, data shift, rule conflict).
- User/partner impact quantification.
- What worked / what failed in detection and response.
- Corrective actions with owners and due dates.
- Guardrail updates (monitor thresholds, canary checks, rollback automation).

### Conditions to resume normal pipeline execution

- False-positive rate returns within accepted control bounds for **two consecutive monitoring intervals**.
- Manual spot-check by Trust & Safety approves release candidate.
- Incident commander signs off on rollback/patch validation.
- Partner notification complete when external impact occurred.

---

## 2) False-Negative / Undetected Disparity Event Flow

A false-negative/undetected disparity event occurs when harmful or disparate outcomes are not flagged and continue through the pipeline.

### Detection sources

- Automated monitor drift alarms (outcome disparity delta beyond threshold).
- Analyst report from fairness audits or retrospective sampling.
- Partner escalation reporting missed harmful/disparate outcomes.

### Immediate containment actions by agent

1. **Pause publication** for affected model route, region, language, or cohort.
2. **Quarantine outputs** generated since earliest suspected onset.
3. Enable stricter fallback policy (higher sensitivity, lower release threshold).
4. Trigger backfill analysis job on impacted time range for reclassification.

### Triage ownership and max response times

- **Primary owner:** Fairness On-Call Reviewer.
- **Secondary owner:** ML Ops Incident Commander.
- **Support:** Trust & Safety Analyst, Data Science lead.
- **Max response targets:**
  - Owner assignment: **15 minutes** from alert/escalation.
  - Disparity blast radius assessment: **90 minutes**.
  - Interim mitigation + reprocessing plan: **3 hours**.

### Required evidence logs

- Disparity metrics by cohort (pre-incident baseline vs incident window).
- Confusion-matrix slices and threshold state at detection time.
- Data lineage: input sources, feature versions, transformations.
- Quarantine scope and reprocessing job identifiers.
- Decision log for temporary policy tightening and rollback criteria.

### Post-incident review template

- Incident metadata and affected protected/monitored cohorts.
- Detection gap analysis (why monitor or reviewer missed early signals).
- Root cause (instrumentation gap, metric blind spot, data latency, model regression).
- Scope and downstream effect analysis.
- Remediation tasks (monitor additions, fairness constraints, retraining plan).
- Verification criteria for completion.
- Follow-up review date.

### Conditions to resume normal pipeline execution

- Reprocessed outputs pass fairness acceptance thresholds across required cohorts.
- Enhanced monitor rules deployed and tested in canary.
- Dual approval from Fairness owner and Incident Commander.
- Stakeholder communication completed for impacted partners/users.

---

## 3) Suspected Re-Identification / Privacy Breach Event Flow

A suspected re-identification/privacy breach event occurs when outputs may reveal personal or linkable identity information beyond policy allowances.

### Detection sources

- Automated privacy monitor alerts (PII leakage, linkage-risk score spikes).
- Analyst report from privacy review or red-team testing.
- Partner escalation reporting potential exposure of sensitive identities.

### Immediate containment actions by agent

1. **Pause publication immediately** across all potentially impacted endpoints.
2. **Quarantine outputs** and lock access to incident-relevant storage partitions.
3. Revoke/rotate active access tokens for affected service paths if leakage vector uncertain.
4. Freeze data export and partner sync jobs until investigation scope is constrained.

### Triage ownership and max response times

- **Primary owner:** Privacy/Security Incident Response Lead.
- **Secondary owner:** ML Ops Incident Commander.
- **Support:** Legal/Compliance, Trust & Safety, Platform Security.
- **Max response targets:**
  - Owner assignment: **5 minutes** from detection (default SEV-1).
  - Initial exposure assessment: **30 minutes**.
  - Containment completeness confirmation: **60 minutes**.

### Required evidence logs

- Privacy alert payloads and detector confidence details.
- Sample affected outputs (sanitized access-controlled copies only).
- Access logs (read/write/export), token usage, and endpoint invocation traces.
- Data retention and deletion control events during incident window.
- Timeline of containment actions and notification decisions.

### Post-incident review template

- Incident classification (suspected vs confirmed breach).
- Legal/compliance decision points and notification obligations.
- Root cause and exploitability assessment.
- Exposure scope and impacted entities.
- Containment and eradication actions completed.
- Preventive controls added (privacy filters, access boundaries, audits).
- Sign-off from Security + Legal + Incident Commander.

### Conditions to resume normal pipeline execution

- Security confirms leak vector blocked and no active exposure path remains.
- Required legal/compliance reviews and notifications completed.
- Privacy regression tests pass in staging and canary.
- Executive incident authority formally approves service restoration.

---

## 4) Translation-Induced Harm Event Flow

A translation-induced harm event occurs when translation introduces semantic distortion that creates harmful, biased, or policy-violating outcomes.

### Detection sources

- Automated monitor alerts on translation quality/safety divergence (source vs translated intent mismatch).
- Analyst report from multilingual QA review.
- Partner escalation from locale teams or end-user complaint channels.

### Immediate containment actions by agent

1. **Pause publication** for impacted language pair(s), locale(s), or translation model version.
2. **Quarantine outputs** from suspect translation components and prevent syndication.
3. Route traffic to approved fallback translation path (human-reviewed glossary mode or previous model).
4. Flag high-risk terms/entities list for hard-block pending correction.

### Triage ownership and max response times

- **Primary owner:** Localization Quality On-Call.
- **Secondary owner:** Trust & Safety Analyst.
- **Support:** ML Ops Incident Commander, Regional Partner Manager.
- **Max response targets:**
  - Owner assignment: **20 minutes**.
  - Harm and locale impact assessment: **90 minutes**.
  - Fallback + remediation plan: **3 hours**.

### Required evidence logs

- Source text, translated text, and back-translation comparisons.
- Language pair, model version, glossary/prompt configuration.
- Harm label(s) assigned and reviewer adjudication notes.
- Quarantine and publication-pause audit logs.
- Partner/user complaint references and response timestamps.

### Post-incident review template

- Affected locales and language pairs.
- Translation failure mode taxonomy (negation loss, politeness shift, slur mistranslation, context truncation).
- Root cause and model/prompt/data contributors.
- Impact and recurrence risk scoring.
- Remediation actions (dataset fixes, glossary updates, safety constraints, reviewer playbook).
- Validation results across representative locale test sets.

### Conditions to resume normal pipeline execution

- Corrected translation path passes multilingual safety and fidelity gates.
- Critical term/entity regression suite passes for affected locale pairs.
- Localization owner + Trust & Safety sign-off completed.
- Monitoring thresholds tuned to detect recurrence and verified live.

---

## Cross-Incident Evidence Retention

- Preserve incident artifacts for a minimum retention window defined by policy.
- Store all evidence in access-controlled incident workspace.
- Maintain immutable timeline entries for every containment and recovery action.
