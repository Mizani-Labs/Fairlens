# AGENT_CONTRACTS

This file defines execution contracts for the agent layer referenced in Section 12 and applies the Class A/B/C data handling mapping from Section 11.3.

## 1) Security class mapping (Section 11.3 alignment)

| Class | Description | Examples in FairLens | Handling baseline |
|---|---|---|---|
| Class A | Highly sensitive, directly identifying or safety-critical data | Raw testimonies, voice-note metadata that can identify a reporter, key material | Encrypt at rest/in transit, strict least-privilege access, audited access logs |
| Class B | Operationally sensitive but less identifying | Aggregated case features, internal model/rule outputs, partner-internal dashboards | Role-based access, encrypted transport, retention-limited storage |
| Class C | Low-sensitivity metadata/public artifacts | Run status, anonymized system health counters, public release notes | Integrity checks and provenance, broad read access permitted |

---

## 2) Agent contracts (Section 12)

### 2.1 Inception Safeguards Agent (Milestone 0)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `program.kickoff`, `safety.review.requested`.<br>**Schedule:** Daily 02:00 UTC until Milestone 0 close.<br>**Manual approval points:** Threat-model sign-off by Safety/Privacy lead before closure. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:0)`; `threat_inputs:array<object>(minItems=1)`; `legal_context:string(min=2)`; `locales:array<string>(must include "en" and "ar")`; `approver_ids:array<string>(minItems=1)`.<br>Validation: JSON schema strict mode (`additionalProperties=false`), no nulls in required fields. |
| Output schema | `artifacts:{harm_taxonomy_uri:string, threat_model_uri:string, data_min_matrix_uri:string, governance_charter_uri:string}`; `status:{state:string(enum:success|partial|failed), code:string, message:string}`; `confidence:{score:number[0,1], rationale:string}`; `error:{retryable:boolean, category:string, details:string|null}`. |
| SLA/SLO | Max run time: 20 min.<br>Retry policy: exponential backoff (30s, 2m, 5m), max 3 retries for retryable errors.<br>Timeout handling: mark `failed` with `code=TIMEOUT`, emit escalation event. |
| Failure semantics | Retryable: transient storage/network/schema fetch errors.<br>Terminal: missing required approvals, invalid locale baseline, policy conflict.<br>Escalation target: Safety/Privacy lead. |
| Security classification | Inputs: Class A/B mix (threat inputs may include sensitive narratives).<br>Outputs: Class B artifacts, with summarized Class C status envelope. |

### 2.2 Evidence Capture Agent (Milestone 1)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `client.capture.started`, `localization.pack.updated`.<br>**Schedule:** On-demand + hourly batch validation.<br>**Manual approval points:** UX parity approval for Arabic scenario before release gate. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:1)`; `intake_payload:object`; `locale:string(enum:en,ar,fr,pt,sw)`; `offline_mode:boolean`; `schema_version:string(regex:^v[0-9]+\.[0-9]+$)`.<br>Validation: required prompts complete, pseudonymous ID present, no direct PII field unless encrypted blob. |
| Output schema | `artifacts:{capture_record_uri:string, localization_report_uri:string, encryption_check_uri:string}`; `status:{state,code,message}`; `confidence:{score,rationale}`; `error:{retryable,category,details}`. |
| SLA/SLO | Max run time: 10 min per submission, 99% < 3 min.<br>Retry: local queue retry every 60s up to 10 attempts when offline sync blocked.<br>Timeout: persist checkpoint locally and return `partial`. |
| Failure semantics | Retryable: storage lock contention, temporary encryption service unavailability.<br>Terminal: malformed intake schema, missing pseudonymous ID, failed integrity hash.<br>Escalation: Platform lead + Field partner liaison. |
| Security classification | Inputs: Class A (report payload), Class B (localization metadata).<br>Outputs: Class A encrypted capture artifact; Class B QA report; Class C status summary. |

### 2.3 Secure Sync Agent (Milestone 2)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `queue.sync.requested`, `connectivity.restored`.<br>**Schedule:** Every 5 min with jitter when queue non-empty.<br>**Manual approval points:** Key-rotation baseline approval before production enablement. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:2)`; `queue_batch:array<object>(minItems=1,maxItems=500)`; `node_id:string`; `key_version:string`; `network_state:string(enum:online,intermittent,offline)`.<br>Validation: dedupe key required; payload envelope signatures valid. |
| Output schema | `artifacts:{sync_manifest_uri:string, conflict_report_uri:string, retry_queue_uri:string}`; `status:{state,code,message,synced_count:int,conflict_count:int}`; `confidence:{score,rationale}`; `error:{retryable,category,details}`. |
| SLA/SLO | Max run time: 15 min per batch.<br>Retry: exponential with full jitter, max 8 attempts over 24h.<br>Timeout: split batch and reschedule child jobs. |
| Failure semantics | Retryable: transport failure, remote node unavailable, nonce collision recoverable.<br>Terminal: signature verification failure, key mismatch, replay attack detection.<br>Escalation: Platform lead + Security on-call. |
| Security classification | Inputs: Class A encrypted queue payloads + Class B routing metadata.<br>Outputs: Class B sync manifests, Class A conflict payload references, Class C run metrics. |

### 2.4 Disparity Analytics Agent (Milestone 3)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `dataset.window.closed`, `analysis.manual.run`.<br>**Schedule:** Nightly 01:00 UTC and pre-release gate run.<br>**Manual approval points:** Human analyst review required before externalizing claims. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:3)`; `aggregated_dataset_uri:string`; `cohort_config_uri:string`; `min_cell_size:int(>=20)`; `tests:array<string>(allowed:DIR,ZTEST,FISHER,TPR_GAP,CALIBRATION)`.<br>Validation: no raw direct identifiers, cohort definitions versioned. |
| Output schema | `artifacts:{fairness_report_uri:string, metric_bundle_uri:string, dashboard_snapshot_uri:string}`; `status:{state,code,message}`; `confidence:{score,rationale,interval:string}`; `error:{retryable,category,details}`. |
| SLA/SLO | Max run time: 30 min.<br>Retry: 2 retries for compute/transient warehouse failures.<br>Timeout: emit partial metrics with `state=partial` and blocked tests list. |
| Failure semantics | Retryable: compute capacity exhaustion, temporary data warehouse timeout.<br>Terminal: cohort schema mismatch, below-minimum sample across all cohorts, PII leakage detection.<br>Escalation: Data lead. |
| Security classification | Inputs: Class B aggregated data.<br>Outputs: Class B analytic artifacts; Class C high-level KPI summary. |

### 2.5 Policy Review Agent (Milestone 4)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `policy.doc.ingested`, `heuristics.updated`.<br>**Schedule:** Every ingestion + weekly backfill audit.<br>**Manual approval points:** Reviewer sign-off for high-risk clause flags. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:4)`; `document_uri:string`; `doc_type:string`; `language:string`; `heuristic_pack_version:string`; `linkage_context_uri:string|null`.<br>Validation: supported doc type, OCR confidence >= configured threshold, language normalization complete. |
| Output schema | `artifacts:{flagged_clauses_uri:string, linkage_map_uri:string, reviewer_packet_uri:string}`; `status:{state,code,message,flag_count:int}`; `confidence:{score,rationale}`; `error:{retryable,category,details}`. |
| SLA/SLO | Max run time: 25 min per document.<br>Retry: 3 retries for parser/OCR transient errors.<br>Timeout: produce partial extraction and queue human review. |
| Failure semantics | Retryable: OCR service timeout, parser crash, temporary glossary fetch failure.<br>Terminal: unsupported format, corrupted source, critical heuristic pack integrity failure.<br>Escalation: Product lead + Field partner liaison. |
| Security classification | Inputs: Class B policy documents (Class A if attached testimonies).<br>Outputs: Class B flagged-clause artifacts, Class C status envelope. |

### 2.6 Integrated Validation Agent (Milestone 5)

| Contract Area | Specification |
|---|---|
| Trigger conditions | **Events:** `milestone5.demo.requested`, `release.candidate.created`.<br>**Schedule:** Weekly dry-run + mandatory run at release candidate cut.<br>**Manual approval points:** CSO acceptance and program lead go/no-go approval. |
| Required input schema | `run_id:string(uuid)`; `milestone:int(enum:5)`; `scenario_bundle_uri:string`; `connectivity_profile:string(enum:good,intermittent,poor)`; `required_checks:array<string>(minItems=1)`; `stakeholder_signoff_matrix_uri:string`.<br>Validation: includes Arabic parity scenario, offline-to-sync path present, analyst dashboard checks included. |
| Output schema | `artifacts:{demo_run_log_uri:string, validation_report_uri:string, deployment_playbook_uri:string}`; `status:{state,code,message}`; `confidence:{score,rationale}`; `error:{retryable,category,details}`. |
| SLA/SLO | Max run time: 45 min full end-to-end.<br>Retry: one automatic retry for environment flake, otherwise manual rerun.<br>Timeout: fail run and block release promotion. |
| Failure semantics | Retryable: infra flake, transient test harness failure.<br>Terminal: failed offline journey, failed sync under poor connectivity, unmet CSO usefulness criterion.<br>Escalation: Program steering group. |
| Security classification | Inputs: Class A/B scenario data.<br>Outputs: Class B validation evidence, Class C deployment summary. |

---

## 3) Cross-agent dependency map (strict order, Milestones 0–5)

| Order | Milestone | Agent | Depends on | Blocking condition to proceed |
|---|---|---|---|---|
| 1 | M0 | Inception Safeguards Agent | None | Threat model + governance artifacts approved |
| 2 | M1 | Evidence Capture Agent | M0 complete | Offline capture + Arabic parity pass successful |
| 3 | M2 | Secure Sync Agent | M1 complete | Intermittent-connectivity sync and dedupe baseline met |
| 4 | M3 | Disparity Analytics Agent | M2 complete | Seeded disparity signal detected without analyst PII leakage |
| 5 | M4 | Policy Review Agent | M3 complete | Clause detection above agreed threshold |
| 6 | M5 | Integrated Validation Agent | M0–M4 complete | End-to-end demo validated by CSO and release sign-off |

**Execution rule:** No downstream agent may start unless upstream milestone status is `success` (not `partial`).
