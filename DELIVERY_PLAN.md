# FairLens Delivery Plan (Unified PoC → Program)

## 1) Mission framing
FairLens is an **offline-first, safety-first, multilingual public-interest accountability platform** to detect discriminatory effects from:
- algorithmic systems (e.g., risk scoring models), and
- policy/rule systems (eligibility criteria, regulations, administrative workflows).

The PoC demonstrates one end-to-end slice:
**English-first intake and analyst workflow → exclusion report captured offline → secure sync → CSO-facing disparity signal**, with Arabic refugee scenario validation as a required test case.

Language baseline for PoC and near-term rollout is **English as the system anchor language**, with supported operational locales: Arabic, French, Portuguese, and Swahili, plus dialect/community-pack extension support for conflict and displacement corridors.

---

## 2) Delivery principles (harness-engineering aligned)
1. **Harness over model**: reliability, safety, observability, and governance are first-class.
2. **Planning artifacts + decomposition**: auditable vertical slices with explicit PLAN → IMPLEMENT → VERIFY artifacts.
3. **Verification loops by default**: functional, safety, and abuse-case checks for each feature.
4. **Determinism for high-risk logic**: consent, encryption, sync conflict handling, and retention workflows should be explicit and testable.
5. **Least privilege**: strict access boundaries and metadata minimization.
6. **State governance**: separate ephemeral session data from governed case evidence.
7. **Human oversight**: no automated accusation/enforcement; alerts are analyst-decision support.

---

## 3) Unified PoC scope
### In scope
- English-first intake flow (text + optional voice-note metadata) optimized for low-literacy users.
- Arabic scenario parity for refugee-use-case validation before each release.
- i18n foundation for English anchor + 4 additional launch locales (Arabic, French, Portuguese, Swahili), including RTL support and locale fallback.
- Translation governance (community glossary, reviewer sign-off, terminology freeze per release).
- Anonymous reporter identity via on-device pseudonymous ID.
- Offline encrypted local queue + delayed sync to partner node.
- CSO dashboard for clustered exclusions and disparity indicators.
- Policy/procurement document ingestion prototype with red-flag extraction.

### Out of scope (PoC)
- Full multi-country legal template library.
- Complete coverage of all target languages/dialects.
- Full mesh networking stack beyond offline queue + resilient retry sync.
- Automated legal determinations.

---

## 4) Workstreams, milestones, and exit criteria
### Milestone 0 — Inception & safeguards (Week 1–2)
**Deliverables**: harm taxonomy, threat model, data-minimization matrix, governance charter.
**Exit criteria**: threat model signed off; English-default UX validated; Arabic refugee welfare exclusion scenario approved as parity test case.

### Milestone 1 — Evidence capture client (Week 3–6)
**Deliverables**: low-literacy English-default intake UX, Arabic localization pack, pseudonymous ID module, encrypted offline persistence.
**Exit criteria**: complete report without internet; data survives restart.

### Milestone 2 — Secure sync & federation slice (Week 5–8)
**Deliverables**: store-and-forward sync, merge/conflict handling, node encryption/key-rotation baseline.
**Exit criteria**: successful sync after intermittent connectivity; duplicate handling meets baseline precision.

### Milestone 3 — Pattern detection & CSO analytics (Week 7–10)
**Deliverables**: outcome-auditing aggregation service, paired-testing schema, trend/cluster dashboards.
**Exit criteria**: seeded disparate-impact signal detected; no analyst-surface PII leakage.

### Milestone 4 — Policy/document review (Week 9–11)
**Deliverables**: one doc-type ingest pipeline, exclusion/red-flag heuristics, linkage to lived reports.
**Exit criteria**: benchmark seeded clauses detected above agreed threshold.

### Milestone 5 — Integrated demo & validation (Week 12)
**Deliverables**: end-to-end scenario demo, validation report, partner deployment playbook.
**Exit criteria**: demo succeeds under poor-connectivity simulation; CSO validates advocacy usefulness.

### Cross-milestone orchestration gate — `localization_gate`
**Owners**: Offline Client Agent + Field Partner Liaison (joint accountability).
**Purpose**: block milestone promotion and deployment unless language gates pass.
**Required checks**:
- English baseline checks: all mandatory flows complete.
- Arabic parity checks for the refugee scenario: RTL rendering, terminology validation, and workflow completion parity.
**Required artifacts**:
- glossary diff,
- reviewer sign-off,
- parity test report.
**Gate policy**: any parity regression blocks deployment until remediation and re-validation are complete.

---

## 5) AIOps/MLOps + bias-busting assurance (integrated)
### Fairness/bias statistical tests
- Disparate Impact Ratio (80% rule) by key cohorts and proxy segments.
- Difference-in-proportions tests (z-test; Fisher exact fallback for small samples).
- Equal opportunity gap (TPR/FNR deltas) when labeled outcomes are available.
- Group calibration checks for score-based systems.
- Intersectional slicing (e.g., language × gender × status) with minimum-cell-size controls.

### Drift, quality, and regression controls
- Distribution drift checks for intake/population shifts.
- Data-quality gates: schema integrity, missingness spikes, duplicate bursts.
- Golden synthetic scenario replay per release to detect regressions, including English-baseline and Arabic-refugee parity verification.

### Operability and release policy
- Versioned pipeline artifacts (schema/model/rule hash + test bundle).
- Staging-to-prod promotion only when fairness, quality, and `localization_gate` language checks pass.
- Shadow-mode rollout for new detection logic.
- On-call incident playbook for harmful false-positive/false-negative alerts.
- Mandatory human review before externalizing high-risk claims.

---

## 6) Autonomous delivery artefact contract (required)
All architecture and governance documentation is part of delivery, not optional reference material.

Autonomous delivery is mandatory: milestone promotion is executed by orchestration policy only when required artefacts are present, fresh, and policy-validated.

| Delivery domain | Required artefact(s) | Minimum acceptance |
|---|---|---|
| Program planning | `DELIVERY_PLAN.md` | Scope, milestones, and DoD are current and approved. |
| Architecture definition | `PROJECT_ARCHITECTURE.md` | Logical layers, principles, and artefact mapping are defined. |
| Agent operating model | `AGENT_CONTRACTS.md` | Agent responsibilities and boundaries are explicit. |
| Governance controls | `governance/*` | Gates, checklists, and HITL controls are reviewable and versioned. |
| Delivery orchestration | `orchestration/*` | Milestone progression path is machine-readable. |
| Operational safety | `ops/*` | Incident and escalation procedures are documented. |

A milestone cannot be marked delivered if any required artefact is missing, stale, unreviewed, or fails autonomous policy checks.

---

## 7) Operating model and cadence
- **Product lead**: community-grounded problem framing.
- **Safety/privacy lead**: threat model, anonymity controls, incident response.
- **Data lead**: fairness metrics, statistical quality, schema governance.
- **Platform lead**: offline sync reliability, federation ops, encryption controls.
- **Field partner liaison**: localization quality and contextual usability.

Cadence:
- Weekly milestone review.
- Bi-weekly safety/red-team review.
- Monthly partner feedback and reprioritization checkpoint.

---

## 8) KPIs and acceptance metrics
### Product utility
- % reports completed offline.
- Median guided submission time.
- CSO reviewer usefulness score.

### Equity signal quality
- Precision/recall for seeded disparate-impact detections.
- False-positive rate for policy/document red-flag extraction.

### Safety and trust
- Re-identification risk checks passed.
- Duress/rapid-exit behavior tests passed.
- Zero plaintext sensitive payloads in transport/storage logs.

### Resilience
- Sync success rate under network disruption.
- Recovery time after node restart/failure.

---

## 9) Top risks and mitigations
1. **Retaliation risk** → anonymity defaults, delayed sync options, duress UX.
2. **Manipulated/low-quality submissions** → structured reporting, confidence scoring, reviewer triage.
3. **Translation/misinterpretation harm** → glossary governance + community QA.
4. **Severe connectivity limits** → strict offline-first architecture and resilient queueing.
5. **Jurisdictional legal exposure** → configurable retention/deletion + localized policy templates.

---

## 10) Immediate 30-day plan
1. Finalize threat model and schema v0.
2. Ship English-first intake + pseudonymous ID module, and complete Arabic parity pass.
3. Implement encrypted local queue and sync endpoint.
4. Stand up analyst summary dashboard with seeded test data.
5. Run fairness/statistical harness checks and publish PoC readiness review.

---

## 11) Definition of Done (PoC)
PoC is complete when a non-technical field tester can:
1. submit an English exclusion report fully offline (with Arabic parity available),
2. sync under intermittent connectivity,
3. and enable a CSO analyst to review aggregated disparity signals linked to testimonies/policy flags,
while preserving reporter anonymity by default,
and all required delivery artefacts in Section 6 are present, approved, and pass autonomous delivery policy checks.
