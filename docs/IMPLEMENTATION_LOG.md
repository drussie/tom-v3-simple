# TOM v3 Simple - Implementation Log

## Blueprint 65 Controlled Runtime Calibration Blocked Execution Resolution Packet v1

Status: complete

### Goal

Package the unresolved BP64/BP62 blocked execution state into a durable resolution packet without
creating operator signoff, selecting a candidate, rerunning the final gate, executing application,
or writing runtime config.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_blocked_execution_resolution_packet`
- worker CLI commands for contract export, input build/validation, packet build/validation,
  blocker checklist, operator action plan, candidate requirements, final-gate rerun plan, and
  reexecution readiness plan
- matching `tom-v1-*controlled-runtime-calibration-blocked-execution-resolution*` Make helpers
- `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_v1.json`
  tracked frozen packet
- generated inputs, validations, checklists, plans, requirements, and readiness plans under
  `.data/exports/`
- focused tests for contract stability, BP64 blocked execution resolution, plan builders, and
  forbidden token rejection

Blueprint 65 preserves the current blocked state: `operator_signoff_required`,
`selected_candidate_required`, `final_gate_rerun_required`, and
`reexecution_not_ready_blockers_unresolved`. It does not modify model weights, replace baselines,
create production config, or mutate runtime config.

## Blueprint 61 Controlled Runtime Calibration Pre-Application Final Gate v1

Status: complete

### Goal

Create the final pre-application safety gate for controlled gameplay gate calibration without
performing runtime application.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_pre_application_final_gate`
- worker CLI commands for contract export, inputs, input validation, final gate build, final gate
  validation, readiness report, blocker report, artifact checklist, and regression checklist
- matching `tom-v1-*controlled-runtime-calibration-pre-application-final-gate*` Make helpers
- `.data/contracts/controlled_runtime_calibration_pre_application_final_gate_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_pre_application_final_gate_v1.json` tracked
  frozen final gate
- generated inputs, validations, readiness reports, blocker reports, artifact checklists, and
  regression checklists under `.data/exports/`
- focused tests for contract stability, final gate readiness, blocked candidate/signoff behavior,
  report builders, and forbidden runtime application terms

Blueprint 61 final gate artifacts preserve `no_runtime_mutation`, `not_updated` runtime config,
`not_created` production config, `not_replaced` baseline state, `not_modified` model state, and
`future_blueprint_required_for_runtime_application: true`. It does not apply threshold, smoothing,
or hysteresis changes; does not update runtime config; does not mutate model weights; does not
replace baselines; does not create production config; and does not approve or reject candidates.

## Review-Guided Gameplay Calibration Evaluation Sandbox v1

Status: complete when accepted

### Goal

Evaluate review-guided gameplay calibration proposal candidates offline without creating labels,
classifier correctness/accuracy claims, automatic relabeling, threshold changes, smoothing
changes, hysteresis changes, runtime config changes, model tuning, baseline mutation, tennis
truth, reviewer scoring, production readiness, generalization, or adjudication.

### Outcome

The milestone adds:

- a tracked review-guided gameplay calibration evaluation sandbox contract
- CLI and Make targets to export the contract, build/validate evaluation inputs, run the offline
  sandbox, validate sandbox reports, and build summaries
- candidate setting snapshots derived from BP49 proposal items with blocked/ready/informational
  statuses and read-only current gate settings
- offline sandbox reports with candidate evaluations, blocked candidate summaries, drift
  summaries, review-data limitations, decision-support statuses, warning, and non-claim summaries
- post-Codex validation coverage for the BP50 smoke path using temporary outputs
- focused tests for contract stability, input generation, fixture-only blocking, validation
  guardrails, offline reports, report rejection, and summary structure

### Non-goals

- No classifier training, classifier scoring, classifier correctness claim, or classifier accuracy
  claim.
- No model asset mutation, committed weights, threshold change, smoothing change, hysteresis
  change, model tuning, runtime config change, baseline replacement, or regression baseline
  mutation.
- No truth labels, point detection claim, line-call claim, score, player identity, or
  adjudication.
- No automatic relabeling, reviewer ranking/scoring, production-readiness claim, or
  generalization claim.

## Review-Guided Gameplay Gate Calibration Proposal v1

Status: complete when accepted

### Goal

Summarize real-broadcast gameplay review metrics into calibration input snapshots and
future-evaluation proposal reports without creating labels, classifier correctness/accuracy
claims, automatic relabeling, threshold changes, smoothing changes, hysteresis changes, runtime
config changes, model tuning, baseline mutation, tennis truth, reviewer scoring, production
readiness, generalization, or adjudication.

### Outcome

The milestone adds:

- a tracked review-guided gameplay calibration proposal contract
- CLI and Make targets to export the contract, build/validate calibration inputs, build/validate
  proposals, and build proposal reports
- review coverage, ambiguity, boundary case, missing review data, source context, current gate
  setting, model provenance, warning, and non-claim summaries
- proposal items that remain future-evaluation-only with candidate settings marked not applied,
  non-runtime-writing, and non-baseline-affecting
- post-Codex validation coverage for the BP49 smoke path using temporary outputs
- focused tests for contract stability, input generation, validation guardrails, proposal
  generation, runtime-change rejection, and proposal report structure

### Non-goals

- No classifier training, classifier scoring, classifier correctness claim, or classifier accuracy
  claim.
- No model asset mutation, committed weights, threshold change, smoothing change, hysteresis
  change, model tuning, runtime config change, or regression baseline mutation.
- No truth labels, point detection claim, line-call claim, score, player identity, or
  adjudication.
- No automatic relabeling, reviewer ranking/scoring, production-readiness claim, or
  generalization claim.

## Real Broadcast Gameplay Review Metrics / QA Dashboard v1

Status: complete when accepted

### Goal

Summarize the real-broadcast gameplay review loop into review operations metrics, QA dashboard
data, and next-review actions without creating labels, classifier correctness/accuracy claims,
automatic relabeling, threshold changes, model tuning, tennis truth, reviewer scoring,
production readiness, generalization, or adjudication.

### Outcome

The milestone adds:

- a tracked real broadcast gameplay review metrics contract
- CLI and Make targets to export the contract, build/validate metrics reports, build
  dashboard-ready QA data, and build next-review actions reports
- review coverage, status distribution, downstream review, confidence, ambiguity, missing-field,
  readiness, corpus coverage, replay context, model provenance, warning, and next-action metrics
- post-Codex validation coverage for the BP48 smoke path using temporary outputs
- focused tests for contract stability, metrics generation, validation guardrails, dashboard data,
  and next-actions reports

### Non-goals

- No classifier training, classifier scoring, or classifier accuracy claim.
- No model asset mutation, committed weights, threshold change, smoothing change, model tuning, or
  regression baseline mutation.
- No truth labels, point detection claim, line-call claim, score, player identity, or
  adjudication.
- No automatic relabeling, reviewer ranking/scoring, production-readiness claim, or
  generalization claim.

## Real Broadcast Gameplay Review Loop v1

Status: complete when accepted

### Goal

Create the first structured human review metadata loop over real-broadcast gameplay gate corpus
outputs without creating labels, classifier correctness/accuracy claims, automatic relabeling,
tennis truth, reviewer scoring, production readiness, generalization, or adjudication.

### Outcome

The milestone adds:

- a tracked real broadcast gameplay review loop contract
- CLI and Make targets to export the contract, build/validate review bundle templates, build a
  review-loop report, and build a human review readiness report
- review entries derived from existing BP46/BP44 artifacts with replay URLs, timestamps,
  classifier evidence, routing/execution context, baseline context, expected broadcast tags, and
  blank/not-assessed human review metadata
- post-Codex validation coverage for the BP47 smoke path using temporary outputs
- focused tests for contract stability, bundle generation, validation guardrails, reporting, and
  readiness

### Non-goals

- No classifier training, classifier scoring, or classifier accuracy claim.
- No model asset mutation, committed weights, or regression baseline mutation.
- No truth labels, point detection claim, line-call claim, score, player identity, or
  adjudication.
- No automatic relabeling, reviewer ranking/scoring, production-readiness claim, or
  generalization claim.

## Real Broadcast Gameplay Gate Corpus Run v1

Status: complete when accepted

### Goal

Create the first controlled real-broadcast gameplay gate corpus run over explicit local media
entries without training or mutating the classifier, silently scanning folders, creating labels,
claiming classifier correctness/accuracy, proving generalization, deciding tennis truth, or
adjudicating evidence.

### Outcome

The milestone adds:

- a tracked real broadcast gameplay corpus run contract
- CLI and Make targets to export the contract, build/validate explicit manifests, run the corpus
  path, and build a human review readiness report
- safe run modes with `dry_run` as the default and explicit real-data modes for processing
- expected broadcast content tags that are preserved as operator context only
- per-entry structural artifacts for gameplay segment candidates, routing, execution planning,
  replay timeline, and review dataset export
- post-Codex validation coverage for the BP46 fixture-mode corpus path using temporary outputs
- focused tests for manifest/run/report guardrails

### Non-goals

- No classifier training, classifier scoring, or classifier accuracy claim.
- No model asset mutation, committed weights, or regression baseline mutation.
- No truth labels, point detection claim, line-call claim, score, player identity, or
  adjudication.
- No silent folder scan, arbitrary media ingestion, production-readiness claim, or generalization
  claim.

## Gameplay Gate Pathway Completion Freeze v1

Status: complete when accepted

### Goal

Freeze the BP38-BP44 gameplay gate pathway as a structural completion contract without adding
new gameplay capability, model inference, labels, classifier correctness/accuracy claims,
production readiness, generalization, or adjudication.

### Outcome

The milestone adds:

- a tracked gameplay gate pathway completion freeze manifest
- CLI and Make targets to build the freeze, validate it, and build the next-phase readiness
  report
- validation for tracked gameplay contracts, protected gameplay baseline, earlier TOM v3 freeze,
  generated export tracking, clean contract/baseline refs, and the local gameplay model asset
- a Blueprint 46 controlled real broadcast corpus run recommendation without implementing it
- post-Codex validation coverage for the BP45 smoke path using temporary outputs
- focused service tests for stable freeze build, tracked ref validation, forbidden claim
  rejection, model asset guardrails, and readiness report generation

### Non-goals

- No new classifier, model inference, or gameplay evidence semantics.
- No review label creation, automatic relabeling, or reviewer ranking/scoring.
- No classifier correctness/accuracy, true gameplay, production-readiness, or generalization
  claim.
- No model asset mutation, committed weights, training truth, or adjudication.

## Gameplay Gate Review Dataset Export v1

Status: complete when accepted

### Goal

Export gameplay gate segment candidates and their structural context as a human-review dataset
without creating classifier correctness, point-detection, scoring, line-call, label, or
adjudication claims.

### Outcome

The milestone adds:

- a tracked gameplay gate review dataset export contract
- CLI and Make targets to export the contract, build the review dataset, validate it, and report
  on it
- review entries with replay URLs, timestamp windows, source paths, routing/execution/timeline
  context, regression context, neutral human review fields, provenance status, warnings, and
  non-claims
- post-Codex validation coverage for the BP44 smoke path using temporary outputs
- focused service tests for contract stability, dataset build/validation, forbidden metadata
  rejection, replay URL preservation, and report generation

### Non-goals

- No model asset mutation or committed weights.
- No review label creation or automatic relabeling.
- No point detection, line-call, scoring, player identity, or production-readiness proof.
- No training truth, generalization claim, classifier correctness claim, or adjudication.

## Gameplay Gate Regression Baseline v1

Status: complete when accepted

### Goal

Freeze the fixture-safe gameplay gate stack as a structural regression baseline without creating
classifier correctness, point-detection, scoring, line-call, or adjudication claims.

### Outcome

The milestone adds:

- a tracked gameplay gate regression baseline contract
- a tracked frozen baseline for the fixture-only BP38-BP42 output profile
- CLI and Make targets to export, build, verify, and report on the baseline
- drift and breaking-drift reporting for structural count/config/contract changes
- post-Codex validation coverage for the BP43 gate using temporary outputs
- focused service tests for contract stability, baseline build, verification, drift detection, and
  report generation

### Non-goals

- No model asset mutation or committed weights.
- No GPU/model inference by default.
- No point detection, line-call, scoring, player identity, or production-readiness proof.
- No training truth, generalization claim, or adjudication.

## Replay Marker Inspector v0

Status: complete when accepted

### Goal

Let replay operators click visible hit/bounce candidate markers and inspect compact candidate
evidence without opening terminal/debug JSON.

### Outcome

The milestone adds:

- replay API `marker_summary` rows on timeline and event overlay responses
- deterministic marker ordering by timestamp, frame, candidate type, and observation id
- compact marker rows with source method, confidence, marker-level arbitration decision/reason,
  image coordinates, court coordinates, and candidate-only warning flags
- `ReplayMarkerInspector` in the replay side panel
- empty-state guidance when no marker is selected
- selected marker display for video, mini-map, or timeline selections

### Non-goals

- No hit/bounce candidate logic changes.
- No marker-level arbitration changes.
- No persisted source evidence mutation.
- No hit truth or bounce truth.
- No in/out, rally, point, or score.
- No accepted/rejected lifecycle.
- No adjudication.

## Compact CLI + Marker Summary v0

Status: complete when accepted

### Goal

Make hit/bounce candidate CLI output compact and operator-focused by default while preserving full
diagnostics behind explicit flags.

### Outcome

The cleanup adds:

- compact default formatting for `build-hit-bounce-candidates`
- `marker_summary` as the primary operator-facing list of final visible markers
- active version compaction into a single `active_versions` block
- `--verbose`, `--include-observation-ids`, and `--diagnostic-summary` flags
- Makefile variables for verbose/full diagnostics and a `tom-v1-hit-bounce-candidates-verbose`
  helper
- tests for compact defaults, deterministic marker ordering, verbose output, full diagnostics, and
  observation id opt-in

### Non-goals

- No hit/bounce candidate logic changes.
- No replay behavior changes.
- No hit truth or bounce truth.
- No in/out, rally, point, or score.
- No accepted/rejected lifecycle.
- No adjudication.

## Marker-Level Event Arbitration v0.3.1

Status: complete when accepted

### Goal

Resolve visible hit/bounce marker conflicts after universal hit validity guard v0.3.0 without
adding event truth or sequence hard gates.

### Outcome

The repair adds:

- marker-level arbitration after the universal guard
- `marker_level_arbitration` payload metadata on final event candidates and diagnostics
- co-located hit/bounce conflict handling that prefers the bounce marker unless the hit has strong
  independent contact evidence
- fly-through/transit hit suppression into `event_candidate_rejection_diagnostic`
- CLI summary counts for marker-level decisions, conflicts resolved to bounce, fly-through hits
  suppressed, and far-side recall preservation
- replay selected-evidence fields for marker-level arbitration decisions and the
  `hit_requires_prior_bounce = false` / `sequence_is_hard_gate = false` flags
- focused regression tests for overlap resolution, independent contact preservation, and
  fly-through suppression

### Non-goals

- No hit truth or bounce truth.
- No in/out, rally, point, or score.
- No player identity, scoreboard OCR, or server/receiver logic.
- No accepted/rejected lifecycle.
- No adjudication.

## Net-Axis Reversal Hit Recall v0.2.5

Status: complete when accepted

### Goal

Recover sparse hit-candidate markers from ball-first court-template net-axis reversals without
requiring a matching player projection, while preserving bounce-overlap protections.

### Outcome

The repair adds:

- `net_axis_reversal_hit_candidate_v025`
- configurable ball-first lookback/lookahead windows around trajectory anchor points
- `net_axis_reversal_recall` metadata on candidates and diagnostics
- CLI and Makefile controls for the recall path
- replay selected-evidence fields for whether player proximity was required and which frames formed
  the reversal context
- weak-overlap suppression for ball-first hits near bounce candidates
- focused tests for no-player recall, proximity confidence support, monotonic non-recall, and
  overlap suppression

### Non-goals

- No hit truth or bounce truth.
- No in/out, rally, point, or score.
- No player identity, scoreboard OCR, or server/receiver logic.
- No accepted/rejected lifecycle.
- No adjudication.

## Hit/Bounce Physics Heuristic Repair v0.2

Status: complete when accepted

### Goal

Improve first-pass event candidate quality by replacing generic trajectory bend reliance with
tennis-specific candidate physics diagnostics.

### Outcome

The repair adds:

- player-proximate `court_y` net-axis reversal as the primary hit-candidate feature
- source image-y descending-to-ascending proxy as the primary bounce vertical-motion feature
- speed reduction as a required bounce-candidate diagnostic
- persisted source `ball_court_projection_candidate.image_point` loading for event builder logic
- CLI and Makefile threshold knobs for net-axis, image-y, and speed-reduction gates
- replay selected-evidence fields for `net_axis_reversal`, `vertical_motion_proxy`, and
  `speed_reduction`
- focused tests for player-proximate hit priority, bounce proxy gates, source image point loading,
  replay payload exposure, and no-truth boundaries

### Non-goals

- No hit truth or bounce truth.
- No in/out, rally, point, or score.
- No player identity, scoreboard OCR, or server/receiver logic.
- No accepted/rejected lifecycle.
- No adjudication.

## TOM v1 Court Keypoints + Homography Adapter

Status: complete when accepted

### Goal

Bridge `model_assets/tom_v1/keypoints_model.pth` into the TOM v3 court evidence system so court geometry can be generated from real model output instead of only fixture geometry.

### Outcome

The repair bridge adds:

- `tom-v1-court-keypoints-probe` for local model inspection
- `run-real-court-keypoints` for real court keypoint observation persistence
- a TOM v1 ResNet50 fc28 keypoint adapter with fixed 224x224 preprocessing
- v0 mapping from 14 TOM v1 raw points to TOM v3's 12-point `tennis_court_v0` schema
- derived court line candidates when required keypoints are present
- replay metadata that distinguishes fixture court evidence from real court keypoint model output
- homography source metadata that preserves whether source court evidence came from real keypoints
- focused tests using a fake court keypoint provider, with no model-file requirement

### Non-goals

- No court truth or accepted/rejected lifecycle.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No player names, scoreboard OCR, or server/receiver logic.
- No adjudication.

## Main Player Track Assignment v0.1 Replay Labels and Locking

Status: complete when accepted

### Goal

Make the near/far main player track candidates visible in replay and reduce ball kid / wall-side leakage by treating track assignment as a persistent visual lock rather than simple frame-local grouping.

### Outcome

The repair adds:

- `main_player_track_assignment_v01` as the current assignment method
- stronger seed selection for near/far visual track candidates
- center-jump, bbox-area-change, and edge/wall rejection for per-frame assignments
- gap allowance when a candidate looks implausible
- `main_player_tracks` replay overlay and timeline payloads
- `mainPlayerTrackRunId` replay query support
- selectable `NEAR TRACK` and `FAR TRACK` labels in the replay workstation
- selected evidence details for track candidate id, role, score, source subject candidate, source detection, and candidate-only warnings

### Non-goals

- No raw detection mutation or deletion.
- No confirmed player identity, player names, or server/receiver truth.
- No scoreboard OCR or side-change identity logic.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication or accepted/rejected lifecycle.

## Main Player Track Assignment v0

Status: complete when accepted

### Goal

Add persistent candidate visual tracks for the two primary tennis-player subjects so pose can run from stable near/far track candidates instead of only frame-local subject candidates.

### Outcome

The repair bridge adds:

- `main_player_track_candidate` observation spine rows under the existing `tracking` family
- `main_player_track_assignment_candidate` per-frame assignment rows
- `near_player_track_candidate` and `far_player_track_candidate` roles
- lineage from subject candidates, source detections, and track candidates to assignment rows
- `run-real-pose --source-track-run-id` support for track-filtered crop-mode pose
- lineage from track assignment candidates to `player_pose_observation` rows
- replay pose metadata for track candidate ids, roles, and assignment observations
- Makefile helpers for TOM v1 main player track assignment and track-filtered pose

### Non-goals

- No raw detection mutation or deletion.
- No confirmed player identity, player names, or server/receiver truth.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication or accepted/rejected lifecycle.

## Main Tennis Player Subject Filter v0

Status: complete when accepted

### Goal

Reduce TOM v1 player-detection pose noise by selecting at most two tennis-player subject candidates per frame before crop-mode pose inference.

### Outcome

The repair bridge adds:

- `main_player_subject_candidate` observation spine rows under the existing `tracking` family
- `near_player_candidate` and `far_player_candidate` roles
- deterministic v0 scoring from image-relative bbox features
- model registry, runtime config, processing run, and processing step provenance
- lineage from raw `player_detection` rows to subject candidates
- `run-real-pose --source-subject-run-id` support for filtered crop-mode pose
- lineage from selected subject candidates to `player_pose_observation` rows
- Makefile helpers for TOM v1 main subject selection and filtered pose

### Non-goals

- No raw detection mutation or deletion.
- No confirmed player identity.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication or accepted/rejected lifecycle.

## TOM v1 Pose Runtime + Replay Display Policy Repair

Status: complete when accepted

### Goal

Repair runtime bridge issues discovered during TOM v1 local model smoke and make dense replay overlays visually reviewable by default.

### Outcome

The repair adds:

- Ultralytics detection and pose prediction calls that omit unset optional kwargs instead of passing `None`
- safe crop-mode pose frame-bound filtering when frame start/end are omitted
- TOM v1 helper defaults for `--allowed-root` and known model image sizes
- replay display modes for current-only, short-trail, and full-trail review
- optional tracklet trail/path rendering, off by default
- focused regression tests for runtime kwargs, pose frame bounds, TOM v1 helpers, and replay display policy wiring

### Non-goals

- No model files committed.
- No persisted observation semantics changed.
- No real court keypoint or gameplay classifier adapter.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication.

## TOM v1 Model Assets + Perception Bridge

Status: complete when accepted

### Goal

Add guardrails and runbook support for using local TOM v1 model assets as optional TOM v3 observation sources.

### Outcome

The bridge adds:

- local model asset ignore guardrails, including `*.torchscript`
- TOM v1 model inventory docs
- Makefile helpers for TOM v1 YOLO runtime probe, ball detection, player detection, tracklet building, and pose smoke
- runbook commands for local TOM v1 smoke
- class mapping risk notes

### Non-goals

- No model files committed.
- No mandatory YOLO runtime in CI.
- No TOM v1-specific court keypoint or gameplay classifier adapter.
- No tracking quality claim.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication.

## Milestone 8C - Camera / View Evidence Layer

Status: complete

### Goal

Make persisted `camera_view_observation` rows queryable and inspectable as geometry context evidence.

### Outcome

Milestone 8C created:

- `apps.api.services.camera_view_evidence` query, summary, and bundle helpers.
- `/court/camera-view` query endpoint.
- `/court/camera-view/summary` summary endpoint.
- `/court/camera-view/{observation_id}/bundle` evidence bundle endpoint.
- Camera/view read-model schema contracts.
- Service and API tests using 8B fixture camera/view rows.
- Camera/view evidence docs, milestone doc, handoff, and agent report.

8C final path:

```text
fixture court run
-> camera_view_observation rows
-> query / summary / bundle read models
-> /court/camera-view API
```

### Non-goals

- No homography computation.
- No projection diagnostics.
- No replay court overlay.
- No real camera/court model.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No stream ingestion.
- No adjudication.

## Milestone 8B - Court Keypoint / Line Evidence Adapter

Status: complete

### Goal

Make the 8A court evidence schema operational with deterministic fixture court evidence.

### Outcome

Milestone 8B created:

- `apps.worker.services.court_adapter.run_fixture_court_adapter`.
- Worker CLI `run-fixture-court`.
- Makefile `court-fixture`.
- Deterministic fixture court keypoint generation from the normalized template.
- Fixture court line generation from template line definitions.
- Fixture camera/view observation generation.
- Model registry, runtime config, processing run, and processing step provenance.
- Service and CLI tests.
- Fixture court adapter docs and runbook updates.

8B final path:

```text
indexed media
-> fixture court evidence adapter
-> court keypoint observations
-> court line observations
-> camera/view observations
```

### Non-goals

- No real court model.
- No homography computation.
- No projection diagnostics.
- No replay court overlay.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No stream ingestion.
- No adjudication.

## Milestone 8A - Court Evidence Schema / Contract

Status: complete

### Goal

Start Blueprint 8 by implementing the schema and persistence foundation for court/camera/homography evidence.

### Outcome

At 8A, Blueprint 8 entered progress.

Milestone 8A created:

- Court evidence schema contract docs.
- Court template registry docs.
- `tom_v3_schema.court` contracts.
- Typed storage models for court keypoints, court lines, camera/view evidence, homography candidates, and projection diagnostics.
- Alembic migration `0003_court_evidence_observations`.
- Observation writer support for typed court evidence rows.
- Lineage relationship constants for homography/projection provenance.
- Schema and persistence tests for fake court evidence.

8A final path:

```text
observation spine
-> court typed detail row
-> lineage when derived
-> artifacts / annotations through existing evidence system
```

### Non-goals

- No court runtime.
- No homography computation.
- No replay court overlay.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No stream ingestion.
- No adjudication.

## Milestone 7F - Perception Run Orchestration and Completion Review

Status: complete

### Goal

Close Blueprint 7 without adding new runtime capability.

### Outcome

Blueprint 7 is complete.

Milestone 7F created:

- Blueprint 7 completion review.
- Milestone 7F closeout doc.
- Milestone 7F handoff.
- Milestone 7F agent report.
- Final runbook orchestration for fixture baseline, optional real detection, optional real-detection-derived tracklets, and optional real pose replay.
- Canonical status updates marking Blueprint 7 COMPLETE.

Blueprint 7 final ladder:

```text
indexed media
-> optional real YOLO detection observations
-> optional candidate tracklets from real detections
-> optional real pose keypoint observations
-> replay workstation overlays and selected evidence details
```

### Non-goals

- No new runtime behavior.
- No court/homography implementation.
- No database migration.
- No movement/stroke interpretation.
- No bounce/hit/rally/point/scoring.
- No real stream ingestion.
- No TOM v2-style adjudication.

## Milestone 7E - Court / Homography Evidence Decision Gate

Status: complete

### Goal

Decide whether court/camera/homography evidence belongs inside Blueprint 7 or should become a separate blueprint.

### Decision

Court/camera/homography evidence should be deferred to Blueprint 8.

### Non-goals

- No court/homography database migration.
- No court/homography runtime.
- No court keypoint or line detector.
- No homography computation service.
- No replay court overlay implementation.
- No production court-space coordinate transforms.
- No bounce/hit/rally/point/scoring.
- No real stream ingestion.
- No tennis-event interpretation.
- No adjudication.

### Notes

Milestone 7E created:

- `docs/court/court_homography_evidence_decision_v0.md`.
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`.
- Milestone doc, handoff, and agent report.
- Canonical status updates documenting the Blueprint 8 deferral.

The decision note proposes future court keypoint, court line, camera/view, homography candidate, lineage, replay, review, and export contracts. No runtime or schema implementation was added.

## Milestone 7D - Real Pose Runtime for Replay Workstation

Status: complete

### Goal

Add optional real pose replay runtime so indexed media can produce persisted `player_pose_observation` keypoint evidence for the existing replay workstation.

### Non-goals

- No movement interpretation.
- No stroke classification.
- No serve, split-step, or biomechanics conclusions.
- No court/homography implementation.
- No bounce/hit/rally/point/scoring.
- No real stream ingestion.
- No tennis-event interpretation.
- No adjudication.

### Notes

Milestone 7D created:

- `apps/worker/services/real_pose_replay.py`.
- `packages/model_adapters/tom_v3_model_adapters/pose_inference.py`.
- Worker CLI `run-real-pose`.
- Makefile `real-pose`.
- Real pose replay docs under `docs/perception/`.
- Milestone doc, handoff, and agent report.
- Tests proving fake real-run pose output persists pose observations and source detection lineage without optional runtime or weights.

The command reuses optional runtime probing, local weights validation, model registry metadata, COCO17 pose normalization, and existing pose observation persistence. Real pose model output remains keypoint evidence only.

## Milestone 7A - Real YOLO Detection Replay Run

Status: complete

### Goal

Start Blueprint 7 with an optional real YOLO detection replay command that persists mapped model-output detections as atomic observations for the existing replay workstation.

### Non-goals

- No tracklet generation from real detections.
- No real pose inference.
- No homography or court-space implementation.
- No stream ingestion or live model scheduling.
- No tennis-event interpretation.
- No scoring or adjudication.

### Notes

Milestone 7A created:

- `apps/worker/services/real_detection_replay.py`.
- Worker CLI `run-real-detection`.
- Makefile `real-detection`.
- Real detection replay docs under `docs/perception/`.
- Blueprint 7 status docs, milestone doc, handoff, and agent report.
- Tests proving fake real-run YOLO output persists atomic observations without optional runtime or weights.

The command reuses existing runtime probe, weights validation, model registry, YOLO normalization, frame inference, and detection persistence paths. Real model output remains observation evidence only.

## Milestone 6F - Blueprint 6 Completion Review

Status: complete

### Goal

Close Blueprint 6 with final status updates, completion review documentation, validation, and future blueprint boundaries.

### Non-goals

- No new frontend replay behavior.
- No new backend replay behavior.
- No real live stream ingestion.
- No HLS/RTSP/HDMI/camera capture.
- No stream backend/session tables.
- No websocket live updates.
- No model scheduling.
- No real pose inference.
- No tennis-event interpretation.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

### Notes

Milestone 6F created:

- `docs/blueprints/tom_v3_blueprint_6_completion_review.md`.
- `docs/milestones/milestone_6f_blueprint_6_completion_review.md`.
- `docs/handoffs/milestone_6f_blueprint_6_completion_review_handoff.md`.
- `docs/agent_reports/milestone_6f_blueprint_6_completion_review_report.md`.
- Canonical docs updates marking Blueprint 6 COMPLETE.
- Explicit future blueprint candidates for real live ingestion, real pose runtime, court-space evidence, event candidates, movement/stroke evidence, and deployment.

## Milestone 6E - Stream Proxy Mode

Status: complete

### Goal

Add a live-like Stream Proxy Mode to the replay workstation using indexed local video and already-persisted TOM evidence.

### Non-goals

- No real live stream ingestion.
- No HLS/RTSP/HDMI/camera capture.
- No websocket live updates.
- No model scheduling.
- No real pose inference.
- No tennis-event interpretation.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

### Notes

Milestone 6E created:

- Replay / Stream Proxy mode toggle in `/replay/<media_id>`.
- `mode=stream_proxy` query parameter support.
- Stream Proxy live-like edge tracking.
- Future overlay filtering for detection observations, tracklet candidates, and pose observations.
- Future timeline filtering for detections, tracklets, poses, and review annotations.
- Available evidence counts, live-edge lag, paused-review state, and return-to-live-edge control.
- Makefile `replay-open` support for stream proxy URLs and selected run IDs.
- Docs, milestone, handoff, and agent report updates.

## Milestone 0A - Repo Memory + Architecture / Schema Foundation

Status: complete

### Goal

Create the repo-backed project memory, architecture documentation, and observation-store schema foundation.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No bounce detection.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

TOM v3 is observation-only. GitHub is the durable project memory.

Milestone 0A created:

- Documentation navigation and current-state files.
- Architecture docs for the platform blueprint, observation store, gameplay/view-state layer, visual evidence viewer, and GitHub-as-memory workflow.
- Milestone 0 and Milestone 0A docs.
- A Milestone 0A handoff and agent report.
- Placeholder tracked directories for future API, worker, web, package, migration, and test work.

## Milestone 0B - Backend / API Foundation

Status: complete

### Goal

Convert the observation-store contract into an initial backend service, database migration, schema models, observation writer, and query API.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No real video processing.
- No real bounce detection.
- No frontend evidence viewer.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 0B created:

- FastAPI backend app with health, media, model, runtime config, run, step, observation, artifact, annotation, and dev synthetic endpoints.
- SQLAlchemy storage models for the required observation-store tables.
- Alembic migration `0001_observation_store`.
- Pydantic schema contracts and vocabulary enums.
- Central observation writer used by single and batch observation endpoints.
- Query endpoint with media, run, type, frame, timestamp, confidence, gameplay label, and tracklet filters.
- Tests covering core persistence and API behavior.

## Milestone 0C - Worker + Rich Synthetic Observation Seeder

Status: complete

### Goal

Create a worker-side synthetic pipeline that produces enough persisted evidence for the future visual evidence viewer.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No real video decoding.
- No real ffprobe media indexing.
- No real homography calculation.
- No real bounce detection.
- No real player tracking.
- No frontend evidence viewer.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 0C created:

- Worker CLI commands `seed-synthetic-run` and `verify-synthetic-run`.
- Baseline synthetic tennis scenario.
- Shared rich seeding code reused by the worker and API dev route.
- Viewer-ready gameplay, non-gameplay, and uncertain view-state bands.
- Ball, near-player, and far-player tracklets with track points and coverage gaps.
- Homography placeholder observations, including a missing interval.
- Derived bounce, tracking-gap, and hit candidates.
- Lineage links from candidates to supporting observations.
- Placeholder evidence artifact metadata.
- Tests covering worker seeding and queryability.

## Milestone 0D - Visual Evidence Viewer Foundation

Status: complete

### Goal

Build the first frontend surface that can load a TOM v3 run and show persisted evidence visually.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No real video processing.
- No real tracking implementation.
- No real homography calculation.
- No real bounce detection.
- No production auth.
- No deployment work.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 0D created:

- Next.js web app under `apps/web`.
- Thin backend viewer endpoint `GET /viewer/runs/{run_id}` that composes existing run, media, observation, tracklet, lineage, artifact, and annotation rows.
- Timeline rendering for gameplay/non_gameplay/uncertain view-state bands.
- Track coverage rows for ball, near-player, and far-player tracklets.
- Homography valid/missing row from persisted placeholder observations.
- Clickable candidate markers for derived candidates.
- Observation detail, lineage, artifact, and annotation panels.
- Tests covering the viewer API composition route.
- Frontend lint/build validation.

## Milestone 0E - Integration / QA / Repo Consolidation

Status: complete

### Goal

Consolidate TOM v3 Simple Milestone 0 into a coherent, runnable foundation.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No real video decoding.
- No real ffprobe media indexing.
- No real tracking implementation.
- No real homography calculation.
- No real bounce detection.
- No streaming ingestion.
- No production auth.
- No deployment work.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 0E created:

- Local environment setup docs.
- Local demo runbook.
- Branch/default-branch hygiene guidance.
- `.env.example`.
- Root Makefile for common commands.
- Synthetic viewer smoke script.
- Milestone 0 integration smoke test.
- Updated README, docs index, current state, blueprint progress, implementation log, milestone docs, handoff, and report.

## Milestone 1A - Real Media Indexing + Video Upload / Registration

Status: complete

### Goal

Implement the first real media ingestion and indexing layer for TOM v3 Simple.

### Non-goals

- No YOLO integration.
- No TOM v1 integration.
- No gameplay classification.
- No real tracking implementation.
- No real homography calculation.
- No pose processing.
- No real bounce detection.
- No streaming ingestion.
- No production object storage.
- No production auth.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1A created:

- Local filesystem media storage adapter.
- sha256 checksum calculation.
- ffprobe metadata wrapper with clear missing-ffprobe errors.
- Frame/time mapping utilities and persisted media frame/time summary.
- Shared media indexing service.
- `POST /media/register-file`.
- Worker CLI command `index-media`.
- Tests for checksum, storage copy/register modes, ffprobe parsing/errors, frame/time utilities, API registration, and worker media indexing service.
- Media indexing docs, milestone doc, handoff, and report.

## Milestone 1B - TOM v1 Gameplay Detector Adapter

Status: complete

### Goal

Implement the first gameplay/view-state adapter seam and persist adapter output as TOM v3 observations.

### Non-goals

- No YOLO integration.
- No ball tracking.
- No player tracking.
- No pose tracking.
- No court homography.
- No real bounce detection.
- No point/rally reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1B created:

- Gameplay adapter interface in `tom_v3_model_adapters.gameplay`.
- Deterministic fixture gameplay adapter for dev/test output.
- TOM v1 adapter stub that clearly reports unavailable portable assets/source.
- TOM v1 portability assessment doc.
- Worker gameplay adapter service that creates runtime config, model registry, processing run, processing step, and typed gameplay observations.
- Worker commands `run-gameplay-adapter` and `index-and-run-gameplay`.
- Viewer compatibility tests for gameplay adapter runs.

## Milestone 1C - YOLO26 Ball / Player Observation Adapter

Status: complete

### Goal

Implement the first ball/player detector adapter seam and persist detector output as TOM v3 atomic observations.

### Non-goals

- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1C created:

- Detection adapter interface in `tom_v3_model_adapters.detection`.
- Deterministic fixture detection adapter for dev/test output.
- YOLO adapter stub that clearly reports unavailable runtime/assets.
- YOLO26/Ultralytics portability assessment doc.
- Worker detection adapter service that creates runtime config, model registry, processing run, processing step, and typed atomic observations.
- Worker commands `run-detection-adapter` and `index-and-run-detection`.
- Optional scoped lineage from detections to gameplay/view-state observations.
- Query and viewer payload compatibility tests for detection adapter runs.

## Milestone 1D - Detection Overlay / Visual Observation Layer

Status: complete

### Goal

Make persisted ball/player detection observations visually inspectable in the existing TOM v3 viewer.

### Non-goals

- No real YOLO inference.
- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No production streaming.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1D created:

- Detection overlay transform in `apps/web/src/lib/detections.ts`.
- Detection overlay panel, canvas, and legend components.
- Coordinate-space bbox rendering from persisted `ball_detection` and `player_detection` payloads.
- Selected frame behavior for detection observations.
- Highlighting for the selected detection bbox.
- Detection timeline row using persisted frame numbers.
- Safe empty states for missing media dimensions and missing bbox payloads.
- Viewer contract test coverage for detection bbox payloads and frame/time ownership.
- Detection overlay docs, milestone doc, handoff, and agent report.

## Milestone 1E - Detection Artifact / Frame Extraction Foundation

Status: complete

### Goal

Add frame image artifacts so persisted detection observations can be inspected over real extracted frame imagery.

### Non-goals

- No real YOLO inference.
- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No production object storage.
- No streaming.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1E created:

- ffmpeg frame extraction primitive in `tom_v3_video.frame_extract`.
- Worker frame artifact extraction service.
- Worker command `extract-frame-artifacts`.
- Local `.data/artifacts/media/{media_id}/frames` storage layout.
- Shared `frame_image` and targeted `detection_frame_image` artifact rows.
- Metadata with frame number, timestamp, frame-time owner, extraction method/version, source media, output path, image format, and checksum.
- Local API content route `GET /artifacts/{artifact_id}/content`.
- Viewer frame artifact matching and image display behind persisted bboxes.
- Coordinate canvas fallback when no frame artifact exists.
- Tests covering extraction, metadata, artifact content, and viewer payload behavior.

## Milestone 1F - Tracklet Foundation From Persisted Detections

Status: complete

### Goal

Create candidate temporal groupings from already-persisted ball/player detection observations.

### Non-goals

- No sophisticated tracking.
- No optical flow.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 1F created:

- Deterministic tracklet builder service in `apps.worker.services.tracklet_builder`.
- Worker command `build-tracklets`.
- Tracklet-builder runtime config, model registry, processing run, and processing step records.
- Ball tracklet candidates from persisted `ball_detection` observations.
- Player tracklet candidates from persisted `player_detection` observations grouped by source labels.
- `tracklet` rows with candidate/unverified metadata.
- Initial `track_point` rows linked to source detection observation ids.
- Viewer/query compatibility tests for tracklet builder runs.
- Tracklet foundation docs, milestone doc, handoff, and report.

## Milestone 2A - Tracklet / Track Point Observation Spine + Lineage Repair

Status: complete

### Goal

Repair the tracklet builder persistence contract so tracklet candidates and track point candidates are first-class observations with explicit lineage to source detections.

### Non-goals

- No complex tracker logic.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No real YOLO runtime integration.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 2A repaired:

- Tracklet candidate observation spine rows with `observation_family = track`.
- Track point candidate observation spine rows with `observation_family = track`.
- `tracklet.observation_id` now points to the tracklet candidate observation.
- `track_point.observation_id` now points to the track point candidate observation.
- Source detection observation ids are stored in track point payload metadata.
- `tracked_from` lineage links source detections to track point candidate observations.
- `grouped_from` lineage links track point candidate observations to tracklet candidate observations.
- Tests now assert the observation spine and lineage contract directly.

## Milestone 2B - Tracklet Viewer / Multi-Run Evidence Bundle

Status: complete

### Goal

Make tracklet candidate evidence inspectable across the tracklet builder run and the source detection run.

### Non-goals

- No new tracking algorithm.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No real YOLO runtime integration.
- No production object storage.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 2B created:

- Dynamic tracklet evidence bundle service.
- API endpoint `GET /tracklets/{tracklet_id}/evidence-bundle`.
- Source detection lookup through `tracked_from` lineage and track point payload metadata.
- Track point to tracklet lookup through `grouped_from` lineage.
- Frame artifact matching for targeted and same-frame artifacts.
- Web Tracklet Evidence panel in the existing run viewer.
- Viewer drilldown from tracklet candidate to track point candidate to source detection.
- Tests covering bundle service, endpoint shape, lineage reconstruction, and artifact availability.

## Milestone 2C - Tracklet Query and Review

Status: complete

### Goal

Make candidate tracklets searchable and reviewable with human annotations while preserving observation immutability.

### Non-goals

- No new tracking algorithm.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No real YOLO runtime integration.
- No production review queue or auth.
- No adjudication.
- No truth/fact/promotion/refusal concepts.

### Notes

Milestone 2C created:

- Structured tracklet query service.
- API endpoint `POST /tracklets/query`.
- Query filters for media, tracklet run, source detection run, family, subject, frame/timestamp ranges, confidence, track point count, gap count, and annotation labels.
- Tracklet query summaries by family, subject, annotation label, and gap state.
- Annotation summary helpers for review labels.
- Evidence bundle annotation summaries for tracklet candidates, track point candidates, and source detections.
- Viewer review controls in the Tracklet Evidence panel.
- Same-origin web proxy for creating annotations from the viewer.
- Tests covering query filters, endpoint shape, annotations, and evidence bundle refresh behavior.

## Milestone 2D - Tracklet Evidence Export / Review Dataset Foundation

Status: complete

### Goal

Package selected candidate tracklet evidence into durable local export artifacts without mutating observations or treating review annotations as adjudicated labels.

### Non-goals

- No model training.
- No data labeling platform.
- No reviewer identity/auth system.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No real YOLO runtime integration.
- No adjudication.

### Notes

Milestone 2D created:

- Tracklet review dataset export request/response schemas.
- Export service that accepts explicit tracklet ids or structured tracklet query filters.
- Reuse of the Milestone 2C tracklet query service for query-based exports.
- JSON export files under `.data/exports/tracklets/{export_id}/`.
- Persisted `tracklet_review_dataset_export` evidence artifact rows with checksums.
- Optional `query_result` rows for query-based exports.
- API endpoint `POST /tracklets/export-review-dataset`.
- Worker command `export-tracklet-review-dataset`.
- Tests covering direct exports, query exports, warning fields, artifact metadata, annotation/frame-artifact inclusion controls, API, and worker handler behavior.

## Milestone 2E - Blueprint 2 Completion Review / Temporal Evidence Hardening

Status: complete

### Goal

Close Blueprint 2 with a completion review, invariant audit, naming cleanup, runbook validation, and final documentation pass.

### Non-goals

- No real YOLO runtime integration.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No production deployment or auth.
- No adjudication.

### Notes

Milestone 2E completed:

- Blueprint 2 completion review doc.
- Blueprint 2 status update to complete.
- Invariant audit mapping temporal evidence guarantees to existing tests.
- Focused cross-flow invariant test proving query/review/export do not mutate source detection observations.
- 1F to 2A naming transition documentation.
- Current state, progress, control room, README, runbook, and tracklet/viewer docs updates.
- Final validation pass for backend, worker, web, migrations, synthetic smoke, and local Blueprint 2 smoke path.

## Milestone 3A - YOLO Runtime Environment / Runtime Probe Foundation

Status: complete

### Goal

Start Blueprint 3 by adding a safe optional YOLO runtime environment boundary, runtime probe, and device resolver without adding real inference or persistence.

### Non-goals

- No real YOLO detection persistence.
- No model weights loading.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3A created:

- `requirements-yolo.txt` for optional Ultralytics/OpenCV runtime dependencies.
- YOLO runtime import guard, availability diagnostics, and clear unavailable exceptions.
- Device resolver for `auto`, `cpu`, `mps`, `cuda`, `cuda:0`, and `0`.
- Worker command `yolo-runtime-probe`.
- Git ignore rules for model assets and weight formats.
- Blueprint 3, runtime environment, milestone, handoff, and report docs.
- Tests using mocked imports/devices so base `tom_v3` stays independent from Ultralytics, Torch, OpenCV, CUDA, and MPS.

## Milestone 3B - YOLO Model Registry and Weights Validation

Status: complete

### Goal

Validate local YOLO weights and register model metadata without running inference or persisting detections.

### Non-goals

- No full YOLO detection adapter.
- No real detection persistence.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3B created:

- YOLO weights validation utility with safe local root checks.
- sha256 and file-size fingerprinting for local weights.
- Required checksum validation.
- Default ball/player class mapping and validation.
- Optional model metadata probe for class names when Ultralytics runtime is available.
- Worker service for registering/reusing YOLO model registry rows.
- Worker command `register-yolo-model`.
- Makefile helper for local model registration.
- Docs for local weights placement, registry metadata, and the future runtime config preview.
- Tests covering weights validation, class mapping, registry metadata, optional probe behavior, and CLI handler safety.

## Milestone 3C - YOLO Detection Adapter Normalization Foundation

Status: complete

### Goal

Normalize YOLO-like frame outputs into TOM v3-compatible detection payloads without running real inference or persisting real detections.

### Non-goals

- No full YOLO video inference.
- No real detection persistence.
- No tracklet generation from YOLO output.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3C created:

- YOLO normalization utility for serialized/fake frame result dictionaries.
- Class mapping by normalized class name or source class id.
- `xyxy` to bbox/center conversion.
- Unmapped class accounting.
- Invalid bbox and invalid confidence warnings.
- Out-of-range confidence warnings.
- Normalized detection payload dataclasses and summary result.
- Adapter result conversion for existing detection persistence contracts.
- YOLO adapter skeleton methods for normalization-only behavior.
- Tests covering mapping, bbox conversion, invalid input, summary counts, metadata, and adapter skeleton compatibility.

## Milestone 3D - YOLO Frame Inference / Observation Persistence

Status: complete

### Goal

Connect frame-level YOLO-style outputs to the existing TOM v3 detection persistence path.

### Non-goals

- No optimized video-stream inference.
- No YOLO tracking mode.
- No tracklet generation inside YOLO.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3D created:

- YOLO frame inference provider and frame source interfaces.
- `FakeYoloResultProvider` for deterministic tests without optional runtime packages.
- Guarded `UltralyticsYoloResultProvider` and OpenCV frame source for optional real runtime use.
- Media-owned frame sampling shared with the detection adapter contract.
- YOLO adapter `run()` implementation that uses 3C normalization.
- Worker detection adapter support for registered YOLO model metadata, weights checksum validation, IoU/max-det settings, and model registry ids.
- Payload enrichment for source runtime, model registry id, weights sha256, and inference settings.
- Worker CLI options for `--model-registry-id`, `--iou-threshold`, and `--max-det`.
- Tests proving mocked YOLO outputs persist as atomic `ball_detection` and `player_detection` observations through the existing worker service.
- Failure tests proving unavailable YOLO runs do not persist fallback detections.

## Milestone 3E - Real YOLO Runtime Local Smoke / Viewer Validation

Status: complete

### Goal

Create an optional local real-YOLO smoke workflow and viewer validation path without making real YOLO dependencies required by the default test suite.

### Non-goals

- No new inference algorithms.
- No YOLO tracking mode.
- No tracklet generation inside YOLO.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3E created:

- Real YOLO smoke helper service.
- Worker command `smoke-real-yolo-local`.
- Script wrapper `scripts/smoke_real_yolo_local.py`.
- Plan-only mode for local workflow inspection without runtime/assets.
- Structured skip behavior for missing runtime, weights, or source media.
- Optional tracklet-builder compatibility step after YOLO detection.
- Docs for runtime probe, weights registration, media indexing, YOLO detection, frame artifacts, viewer overlay inspection, tracklet compatibility, and evidence bundle inspection.
- Tests covering smoke plan and skip behavior without real YOLO packages or weights.

## Milestone 3F - Blueprint 3 Completion Review / Real Model Runtime Hardening

Status: complete

### Goal

Close Blueprint 3 with a completion review, invariant audit, documentation cleanup, validation pass, and next-blueprint recommendation.

### Non-goals

- No new inference algorithms.
- No YOLO tracking mode.
- No tracklet generation inside YOLO.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 3F created:

- Blueprint 3 completion review doc.
- Milestone 3F milestone, handoff, and agent report docs.
- Completion statement declaring Blueprint 3 complete.
- Invariant audit mapping runtime, weights, normalization, persistence, failure, smoke, viewer, and tracklet compatibility coverage to existing tests.
- Runbook and README updates for the complete optional YOLO runtime flow.
- Control-room index, current-state, blueprint-progress, and model adapter docs updates.

Blueprint 3 is complete. It closes with optional YOLO runtime support, local weights validation, model registry metadata, YOLO-like output normalization, frame-level provider persistence, local smoke/viewer validation, and Blueprint 2 compatibility while preserving the observation-only boundary.

## Milestone 4A - Pose Runtime / Schema Foundation

Status: complete

### Goal

Start Blueprint 4 by adding typed pose observation persistence, skeleton/keypoint schema contracts, and synthetic pose fixture insertion without adding real pose inference or movement interpretation.

### Non-goals

- No real pose runtime or adapter inference.
- No pose overlay viewer.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4A created:

- Blueprint 4, pose schema, skeleton registry, runtime config, milestone, handoff, and report docs.
- COCO17 skeleton registry with keypoint names, indices, edges, and validation helpers.
- Pose schema helpers for named keypoints, summary statistics, typed pose creation, and runtime config payloads.
- `pose_observation` typed table migration and SQLAlchemy model.
- Observation writer support for a pose typed extension under `observation_family = pose`.
- Synthetic pose insertion helper that creates fixture model/runtime/run/step records and writes first-class pose observation spine rows plus typed pose rows.
- Tests covering skeleton validation, keypoint validation, pose persistence, media-owned frame/time, keypoint summary statistics, unassociated subject mode, model/runtime metadata, and existing observation query/detail compatibility.

## Milestone 4B - Pose Adapter Normalization Foundation

Status: complete

### Goal

Normalize fake or serialized pose model output into TOM v3 pose observation payloads without running real pose inference or interpreting movement.

### Non-goals

- No real pose runtime or adapter inference.
- No pose observation worker persistence pipeline.
- No pose overlay viewer.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4B created:

- Pose normalization module in `tom_v3_model_adapters`.
- `NormalizedPoseObservation`, `PoseNormalizationResult`, and `PoseAdapterResult`.
- `PoseNormalizationAdapter` and `FixturePoseAdapter` skeletons.
- COCO17 keypoint normalization using the skeleton registry.
- Missing keypoint preservation and keypoint summary computation.
- Bbox normalization with explicit invalid-bbox warnings that keep valid keypoints.
- Pose/keypoint/bbox confidence handling.
- Crop-local to full-frame coordinate projection.
- Subject association candidate passthrough.
- Focused tests covering normalization behavior and `PoseObservationCreate` compatibility.

## Milestone 4C - Pose Observation Persistence and Lineage

Status: complete

### Goal

Persist normalized pose payloads through a worker pose processing-run path and connect pose observations to source subject evidence when candidate context is supplied.

### Non-goals

- No real pose runtime or adapter inference.
- No pose overlay viewer.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4C created:

- Pose adapter worker service in `apps/worker/services/pose_adapter.py`.
- Worker command `run-pose-adapter`.
- Fixture pose model registry metadata for persistence runs.
- Pose runtime config payloads with frame sampling and source detection linkage metadata.
- Pose `processing_run` and `processing_step` records.
- Persistence of normalized fixture pose payloads through `ObservationWriter`.
- First-class `pose` observation spine rows plus typed `pose_observation` rows.
- `pose_from_subject_detection_candidate` lineage from source `player_detection` observations to pose observations.
- Reserved relationship enum values for candidate tracklet and track point pose context.
- Tests for unassociated fixture pose persistence, source detection lineage, invalid explicit source ids, and CLI smoke behavior.

## Milestone 4D - Pose Overlay Viewer

Status: complete

### Goal

Make persisted pose observations visually inspectable in the existing Evidence Viewer without adding real pose inference or movement interpretation.

### Non-goals

- No real pose runtime or adapter inference.
- No pose review UI.
- No pose export integration.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4D created:

- Viewer payload serialization for typed pose detail in `GET /viewer/runs/{run_id}`.
- Frontend pose types and overlay extraction helpers.
- COCO17 skeleton edge helpers for the web viewer.
- Pose overlay panel and SVG canvas for persisted keypoint evidence.
- Selected pose metadata, source association candidate context, and keypoint confidence table.
- A pose observations timeline row.
- Tests proving viewer payloads include pose detail for overlay rendering.

## Milestone 4E - Pose Query / Review / Export Integration

Status: complete

### Goal

Make persisted pose evidence searchable, reviewable, and exportable without adding pose inference or movement interpretation.

### Non-goals

- No real pose runtime or adapter inference.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4E created:

- Pose query schema and service for typed `pose_observation` filters.
- API endpoints for pose query, pose evidence bundle, and pose review export.
- Pose evidence bundle service with pose detail, source candidate context, lineage, artifacts, annotations, model, and runtime config summaries.
- Pose review label vocabulary and keypoint-level annotation metadata support through the generic `human_annotation` table.
- TOM-native pose review dataset export service with local JSON output, checksum, `evidence_artifact` metadata, and query result memory.
- Worker command `export-pose-review-dataset`.
- Focused tests for pose query filters, bundle content, annotation immutability, and export artifacts.

## Milestone 4F - Blueprint 4 Completion Review / Pose Evidence Hardening

Status: complete

### Goal

Close Blueprint 4 with a completion review, invariant audit, documentation cleanup, validation pass, and next-blueprint recommendation.

### Non-goals

- No real pose runtime or adapter inference.
- No movement interpretation.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 4F created:

- Blueprint 4 completion review doc.
- Milestone 4F milestone, handoff, and agent report docs.
- Completion statement declaring Blueprint 4 complete.
- Invariant audit mapping pose schema, normalization, persistence, lineage, viewer, query, review, and export coverage to existing tests and viewer contracts.
- Runbook and README updates for the complete fixture pose evidence path.
- Control-room index, current-state, blueprint-progress, and pose docs updates.

Blueprint 4 is complete. It closes with pose schema, COCO17 skeleton registry, normalization, persistence, lineage, viewer overlay, pose query, review annotation support, and TOM-native export while preserving the observation-only boundary and keeping real pose inference and movement interpretation out of scope.

## Milestone 5A - Local Demo / Runbook Completion Path

Status: complete

### Goal

Start Blueprint 5 by adding a deterministic local fixture demo path and canonical runbook that proves the completed TOM v3 Simple evidence loop without optional YOLO weights or real pose weights.

### Non-goals

- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.
- No production streaming, auth, cloud deployment, or multi-camera reasoning.

### Notes

Milestone 5A created:

- `apps/worker/services/local_demo.py` as a lightweight orchestration layer over existing worker/API services.
- Worker command `run-demo`.
- Makefile targets for `demo`, `demo-fixture`, `demo-plan`, `demo-reset`, `demo-export`, `demo-open`, `completion-check`, `yolo-probe`, and `yolo-smoke`.
- Media fallback that prefers explicit media, then `demo_assets/tennis_fixture.mp4`, then generated synthetic placeholder media marked as synthetic demo media.
- A fixture demo path covering media indexing, fixture gameplay, fixture detections, frame artifacts, candidate tracklets, fixture pose observations, seeded review annotations, pose review export, tracklet review export, and viewer URL summary.
- Focused tests for media resolution, stage planning, temporary SQLite demo execution, seeded annotations, export artifacts, and summary contents.
- Canonical `docs/RUNBOOK_LOCAL.md`, Blueprint 5 doc, 5A milestone, handoff, and agent report docs.

The demo output is explicitly fixture/demo evidence only. It proves persistence, lineage, viewer, review, and export plumbing, not tennis understanding.

## Milestone 5B - Viewer / Product Polish

Status: complete

### Goal

Polish the existing Evidence Viewer and product surface so the local fixture demo is understandable to a new developer or reviewer.

### Non-goals

- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 5B created:

- Shared frontend evidence wording helpers in `apps/web/src/lib/evidenceCopy.ts`.
- A run evidence summary panel with processing-run context, observation counts, lineage count, annotation count, runtime config, and review export artifact metadata when present.
- Clearer empty states for missing observations, detection overlays, frame artifacts, tracklet bundles, pose observations, lineage, artifacts, annotations, and export summaries.
- Detection, tracklet, pose, detail, lineage, artifact, and annotation panel copy updates using observation/evidence/candidate wording.
- Human-readable lineage relationship descriptions while preserving raw relationship types.
- Annotation panel support for keypoint metadata, review-only flags, demo-seeded flags, and notes.
- Focused local demo viewer payload assertions for detection, tracklet, pose, lineage, artifacts, annotations, and exports.
- Milestone 5B milestone, handoff, viewer product polish, and agent report docs.

The viewer polish makes existing evidence easier to inspect. It does not create new tennis interpretation capability.

## Milestone 5C - Final Evidence / Provenance Audit

Status: complete

### Goal

Add a final structural audit layer that checks whether local fixture demo evidence is internally coherent across media, runs, processing steps, observations, typed rows, lineage, artifacts, annotations, and review exports.

### Non-goals

- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 5C created:

- `apps/worker/services/completion_audit.py` with `run_completion_audit`.
- Worker command `completion-audit`.
- Makefile target `completion-audit`.
- Optional `TOM_V3_AUDIT_REQUIRED=true make completion-check` integration.
- PASS/WARN/FAIL-style JSON with summary counts, check diagnostics, warnings, failures, and observation-only flags.
- Demo completeness checks for media, fixture runs, detections, candidate tracklets, track points, pose observations, artifacts, annotations, and pose/tracklet exports.
- Focused tests for a passing fixture demo audit and several broken-reference cases.
- Provenance audit docs and milestone/handoff/agent report entries.

The audit checks structure and provenance only. It does not judge model output quality or tennis meaning.

## Milestone 5D - Docs / Control-Room Consolidation

Status: complete

### Goal

Consolidate TOM v3 Simple repo memory into a clear canonical documentation set that explains the platform, local demo, evidence contract, optional YOLO path, exports, provenance audit, known limitations, and final completion checklist.

### Non-goals

- No new backend behavior.
- No new frontend behavior.
- No new database schema.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 5D created:

- Concise README oriented around the local demo, audit, viewer, optional YOLO path, and canonical docs.
- `docs/CONTROL_ROOM.md` as the canonical current repo-memory/status document.
- `docs/ARCHITECTURE.md` as a high-level system overview.
- `docs/OBSERVATION_CONTRACT.md` as the evidence contract for observations, candidates, lineage, artifacts, annotations, and exports.
- `docs/BLUEPRINT_STATUS.md` as a compact blueprint completion summary.
- `docs/KNOWN_LIMITATIONS.md` as an explicit limitation registry.
- `docs/OPTIONAL_YOLO.md` as the optional real-runtime guide.
- `docs/EXPORTS.md` as the TOM-native review export guide.
- `docs/COMPLETION_CHECKLIST.md` as the final demo/viewer/audit/docs/boundary checklist.
- Milestone 5D milestone, handoff, and agent report docs.
- Cross-link cleanup in current-state, progress, implementation log, control-room index, runbook, historical dev runbook, and Blueprint 5 docs.

The consolidation keeps milestone docs as history while making the current state easier to understand without adding product capability.

## Milestone 5E - Final Completion Review

Status: complete

### Goal

Close TOM v3 Simple as a complete lightweight local observation/evidence platform.

### Non-goals

- No new product capability.
- No new backend behavior.
- No new frontend behavior.
- No new database schema.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 5E created:

- `docs/blueprints/tom_v3_simple_final_completion_review.md`.
- Milestone 5E milestone, handoff, and agent report docs.
- Final completion statements in README, Control Room, Blueprint Status, Current State, Blueprint Progress, Blueprint 5 docs, and Completion Checklist.
- Control-room index entries for the final completion review.
- Final validation reporting.

TOM v3 Simple is complete. The recommended next step is to stop building TOM v3 Simple and use/demo it. Future work should begin as a separate blueprint only if deliberately chosen.

## Milestone 6A - Video Replay Timeline Foundation

Status: complete

### Goal

Start Blueprint 6 with a replay workstation foundation that can load indexed local media into a browser video player and synchronize playback time to TOM media-owned frame/time.

### Non-goals

- No detection overlay playback yet.
- No tracklet overlay playback yet.
- No pose overlay playback yet.
- No stream ingestion.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 6A created:

- Replay backend service with frame/time mapping helpers and available run grouping.
- `GET /media/{media_id}/replay-info`.
- `GET /media/{media_id}/video` for local indexed media playback.
- `/replay/[mediaId]` web route.
- `ReplayVideoPlayer` with native video controls, current timestamp, nearest frame, and timeline shell.
- Overlay placeholder text that keeps detection/tracklet/pose playback deferred to later milestones.
- `make replay-open MEDIA_ID=<media_id>`.
- `docs/REPLAY_WORKSTATION.md`, Blueprint 6 docs, milestone docs, handoff, and agent report.

Blueprint 6 is now in progress. TOM v3 Simple remains complete.

## Milestone 6B - Detection Overlay Playback

Status: complete

### Goal

Add synchronized detection observation overlays to the replay workstation.

### Non-goals

- No tracklet overlay playback yet.
- No pose overlay playback yet.
- No stream ingestion.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 6B created:

- `GET /replay/overlays` for media/time-window detection overlay chunks.
- Replay overlay service helpers that normalize persisted `ball_detection` and `player_detection` observations into image-pixel bbox payloads.
- Detection run and display-only confidence filtering for overlay chunks.
- Frontend replay overlay chunk fetching and caching.
- `ReplayDetectionOverlay` with contained-video coordinate scaling, detection layer toggle, and click-to-select bbox behavior.
- Replay workstation selected detection detail and loaded-chunk detection timeline ticks.
- Tests for replay overlay API behavior.
- Milestone 6B docs, handoff, and agent report.

Detection boxes remain persisted detection observations. They are not confirmed objects or tennis events.

## Milestone 6C - Tracklet / Pose Overlay Playback

Status: complete

### Goal

Add synchronized candidate tracklet and pose keypoint evidence overlays to the replay workstation.

### Non-goals

- No full evidence timeline lanes yet.
- No stream proxy mode.
- No live stream ingestion.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 6C created:

- `GET /replay/overlays` support for tracklet candidate and pose keypoint overlay payloads.
- `tracklet_run_id`, `pose_run_id`, and display-only `min_pose_confidence` replay overlay filters.
- Backend replay helpers for persisted candidate tracklet points/paths and persisted pose observations.
- Frontend replay tracklet and pose overlay layers that reuse contained-video coordinate scaling.
- Layer toggles and run selectors for detection observations, tracklet candidates, and pose observations.
- Click-to-select detail for detection observations, tracklet candidates, track point candidates, and pose observations.
- Tests for backend tracklet/pose overlay payloads and filtering.
- Milestone 6C docs, handoff, and agent report.

Tracklet paths remain candidate temporal groupings. Pose skeletons remain keypoint evidence. They are not tennis-event interpretations.

## Milestone 6D - Timeline Lanes / Evidence Scrubber

Status: complete

### Goal

Add temporal navigation to the replay workstation so operators can see persisted evidence over time and click timeline items to seek/select evidence.

### Non-goals

- No stream proxy mode.
- No live stream ingestion.
- No new model/runtime capability.
- No real pose runtime or adapter inference.
- No movement interpretation.
- No stroke classification.
- No serve, hit, split-step, or biomechanics conclusions.
- No court homography.
- No bounce detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

### Notes

Milestone 6D created:

- `GET /replay/timeline` for media/run-scoped evidence lanes.
- Backend timeline helpers for detection observation ticks, tracklet candidate spans, pose observation ticks, and review annotation markers.
- Frontend timeline payload fetching and proxy route.
- `ReplayEvidenceTimeline` with current playhead, lane empty states, and click-to-seek/select behavior.
- Timeline selection detail support for detection observations, tracklet candidates, pose observations, and review annotations.
- Tests for backend timeline lanes, filters, empty lanes, and missing media handling.
- Milestone 6D docs, handoff, and agent report.

Timeline lanes are evidence navigation only. They do not interpret tennis events or adjudicate model correctness.

## Milestone 7A - Real YOLO Detection Replay Run

Status: complete

### Goal

Run optional real YOLO detection over indexed media and persist mapped real model output as replay-compatible atomic detection observations.

### Notes

Milestone 7A created:

- worker `run-real-detection`
- Makefile `real-detection`
- real detection replay service with plan-only mode
- optional runtime and weights validation reuse
- media-owned frame sampling for YOLO inference
- explicit class mapping into `ball_detection` / `player_detection`
- processing run/step summaries
- replay URL output with real `detectionRunId`
- fake-provider tests that do not require local YOLO weights

7A does not add tracklets from real detections, real pose inference, homography, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7B - Real Detection Overlay Validation

Status: complete

### Goal

Make real detection runs clear and inspectable in the replay workstation.

### Notes

Milestone 7B created:

- replay-info source metadata for available runs
- detection run selector labels that distinguish real model output from fixture demo evidence
- optional source/runtime/model/config/class fields in detection overlay payloads
- detection timeline labels with source metadata
- selected detection detail fields for source runtime, model registry, runtime config, class id/label, and frame/time owner
- `run-real-detection` stream-proxy replay URL and local command hints
- tests for fixture and fake real detection source metadata

7B does not add real-detection-derived tracklets, real pose inference, court/homography evidence, model-quality claims, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7C - Real Detection Tracklet Generation

Status: complete

### Goal

Build candidate tracklets from persisted real model-output detection observations while preserving source detection lineage and evidence-only language.

### Notes

Milestone 7C created:

- source detection run validation for `build-tracklets`
- tracklet builder source metadata for real model-output detection runs
- processing run, processing step, runtime config, tracklet, track point, and lineage metadata describing the source detection evidence
- replay-info labels for real-detection-derived tracklet runs
- replay tracklet and track point overlay metadata for source detection run/runtime/evidence source
- replay workstation selected tracklet and track point details showing source detection context
- `build-tracklets` replay URL output with both `detectionRunId` and `trackletRunId`
- Makefile support for passing tracklet run name and viewer base URL
- tests covering fake real detection observations, tracklet metadata, lineage metadata, replay-info metadata, and overlay metadata
- Milestone 7C docs, handoff, and agent report

7C does not add a new tracking algorithm, smoothing, interpolation, real pose inference, court/homography evidence, stream ingestion, tennis-event interpretation, or adjudication. Tracklets remain candidate temporal groupings.

## Milestone 8D - Homography Candidate Persistence

Status: complete

### Goal

Persist candidate homography observations from source court keypoint, court line, and camera/view evidence while preserving geometry-only language and lineage.

### Notes

Milestone 8D created:

- `apps.worker.services.homography_candidate_builder`
- worker `build-homography-candidates`
- Makefile `homography-candidates`
- plan-only homography candidate output
- candidate matrix computation from persisted court keypoints
- reprojection metrics, source counts, template metadata, and builder confidence
- model registry, runtime config, processing run, and processing step provenance
- `homography_candidate_observation` persistence through `ObservationWriter`
- lineage from source court keypoints, court lines, and camera/view context
- focused tests for candidate computation, persistence, insufficient source evidence, lineage, CLI plan mode, and no projection diagnostics
- Milestone 8D docs, handoff, and agent report

8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 8E - Court Overlay in Replay Workstation

Status: complete

### Goal

Render persisted court keypoint, court line, camera/view, and homography candidate evidence in the replay workstation without creating new geometry observations or tennis conclusions.

### Notes

Milestone 8E created:

- replay URL support for `courtRunId` and `homographyRunId`
- replay overlay payloads for court keypoints, court lines, camera/view evidence, and homography candidates
- replay-info summaries for court and homography runs
- timeline lanes for court keypoint, court line, camera/view, and homography candidate evidence
- frontend `ReplayCourtOverlay` rendering for image-pixel keypoints/lines and display-only homography candidate template projection
- court layer toggles and selected court evidence detail in the replay workstation
- tests for court replay payloads, run filtering, homography filtering, and timeline lanes
- Milestone 8E docs, handoff, and agent report

8E does not add projection diagnostics, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 8F - Projection Diagnostics / Review Export

Status: complete

### Goal

Persist projection diagnostic observations from homography candidates and export court geometry review datasets while preserving the observation-only geometry boundary.

### Notes

Milestone 8F created:

- `apps.worker.services.projection_diagnostic_builder`
- worker `build-projection-diagnostics`
- Makefile `projection-diagnostics`
- projected court template keypoint and line payloads
- diagnostic metrics for persisted homography candidates
- `projection_diagnostic_observation` persistence through `ObservationWriter`
- lineage from homography candidates to projection diagnostics
- replay payload, timeline, and selected-detail support for `projectionDiagnosticRunId`
- `apps.worker.services.court_review_export`
- worker `export-court-review-dataset`
- Makefile `court-review-export`
- TOM-native `court_review_dataset_v0` JSON export artifacts
- focused tests for diagnostics, lineage, replay payloads, export contents, and no ball/player source parents
- Milestone 8F docs, handoff, and agent report

8F does not add ball/player court-space projection, real court model inference, accepted/rejected court lifecycle, bounce/hit/in-out/rally/point/scoring, stream ingestion, tennis-event interpretation, or adjudication.

## Repair - TOM v1 Court Keypoint Visual Calibration Audit v0

Status: complete

### Goal

Expose raw TOM v1 court keypoint model output separately from TOM v3 mapped keypoints so court/homography misalignment can be diagnosed before geometry repair.

### Notes

This repair adds:

- explicit `preprocessing_mode = full_frame_resize_224`
- explicit `coordinate_interpretation = output_as_pixels_224`
- clear failure for unsupported calibration modes
- raw TOM v1 keypoint payloads scaled into image pixels
- replay payload fields for `raw_tom_v1_keypoints` and mapped keypoints
- replay toggles for raw TOM v1 keypoints and mapped TOM v3 keypoints
- optional `tom_v1_court_keypoint_calibration_debug_json` artifacts
- uncalibrated TOM v1 keypoint mapping warnings on court and homography evidence
- docs for the calibration audit workflow

This repair does not make court geometry correct. It makes the current court error inspectable without adding court truth, accepted/rejected lifecycle, ball/player court projection, bounce/hit/in-out/rally/point/scoring, player identity, scoreboard OCR, or adjudication.

## Repair - Court Geometry Temporal Persistence v0

Status: complete

### Goal

Keep sparse court geometry evidence visually stable in replay by carrying the latest candidate geometry forward until the next source observation or a bounded max-gap window.

### Notes

This repair adds:

- `court_temporal_persistence=off|carry_forward` on `GET /replay/overlays`
- `court_persistence_max_gap_ms`, defaulting to `1500`
- replay/read-model carry-forward for court keypoints, court lines, homography candidates, and projection diagnostics
- overlay metadata for source observation id, source frame/time, active display window, carry boundary, and `not_court_truth`
- replay controls for temporal persistence mode and max gap
- a visible carried-forward candidate geometry badge in the court overlay
- selected evidence details for source frame/time and active display window
- regression tests for carry-forward, stale geometry, and disabled persistence

This repair creates no new persisted court observations and does not make court geometry true. It does not add court truth, accepted/rejected lifecycle, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, identity, OCR, or adjudication.

## Motion Smoothing / Stable Replay Candidates v0

Status: complete

### Goal

Create derived, stable replay candidate overlays for ball position, near/far main-player boxes, and
pose keypoints while preserving raw observations unchanged.

### Notes

This milestone adds:

- worker `smooth-motion-candidates`
- Makefile `tom-v1-motion-smoothing`
- `smoothed_ball_position_candidate` observations
- `smoothed_main_player_box_candidate` observations
- `smoothed_pose_candidate` observations
- lineage from source ball detection/track point, main-player track assignment, and pose rows
- replay `motionSmoothingRunId` support
- replay layers for `smoothed_ball`, `smoothed_player_boxes`, and `smoothed_pose`
- a `smoothed_motion` timeline lane
- selected evidence detail for smoothing method, source observations, and warning metadata
- tests for smoothing persistence, long-gap behavior, lineage, replay payloads, and helper commands

This milestone does not add bounce/hit/in-out, rally/point/score, player identity, scoreboard OCR,
server/receiver logic, court-space projection, accepted/rejected lifecycle, or adjudication.

## Motion Smoothing Replay Current-Only Display Fix

Status: complete

### Goal

Repair smoothed replay display policy so the default motion-smoothing overlay is a stable current
candidate view instead of a hold-window trail.

### Notes

The original smoothed overlay helper returned every candidate within the active hold window. That
made one frame show multiple `SMOOTH BALL` markers and stacked near/far smoothed labels. The repair
adds a shared smoothed motion display mode:

- `current_only`: one nearest current ball, one near box, one far box, and one pose per active track
- `short_trail`: neighboring candidates for debug review
- `full_trail`: full chunk/window debug display

Current-only selection prefers exact frame matches, then nearest timestamp, then confidence, then
deterministic observation id ordering. This remains a replay/read-model display policy; smoothed
candidate observations stay immutable and evidence-only.

## Pose Limb-Only Sided Replay Visuals

Status: complete

### Goal

Repair replay pose rendering so raw and smoothed pose evidence defaults to limb lines only, with
side-colored limbs and optional debug joint markers.

### Notes

The replay workstation now has a shared pose visual style control:

- `Limbs only`
- `Limbs + joints`
- `Joints only/debug`

`Limbs only` is the default. Left-side limbs render blue, right-side limbs render red, and neutral
torso/head/cross-body edges render subtly. The repair changes only the SVG replay presentation; pose
observations, smoothed pose candidates, lineage, and evidence semantics are unchanged.

No forehand/backhand classification, stroke detection, hit detection, bounce detection, scoring,
player identity, biomechanics truth, accepted/rejected lifecycle, or adjudication was added.

## Object-to-Court Projection Candidates v0

Status: complete

### Goal

Project existing smoothed image-space ball and main-player candidate evidence into normalized
court-template coordinates using existing homography candidate rows, while preserving evidence-only
semantics.

### Notes

This milestone adds:

- worker `project-objects-to-court`
- Makefile `tom-v1-object-court-projection`
- `ball_court_projection_candidate` observations
- `main_player_court_projection_candidate` observations
- `observation_family = projection`
- lineage from source smoothed object observations and source homography candidates
- replay `courtProjectionRunId` support
- replay layers for `ball_court_projection` and `main_player_court_projection`
- a `court_projection` timeline lane
- a normalized court-template mini-map for current ball/near/far projection candidates
- selected evidence detail for source image point/anchor, court point, homography match policy, and
  no-adjudication warnings
- tests for projection math, homography matching, persistence, lineage, replay payloads, and plan
  mode

The projected points are candidate template coordinates only. This milestone does not add bounce,
hit, in/out, rally/point/score, player identity, scoreboard OCR, server/receiver logic,
accepted/rejected lifecycle, or adjudication.

## Operator View Default Layer Presets v0

Status: complete

### Goal

Make replay open in a clean operator view when full run ids are present, while preserving a busy
debug/audit preset and all manual layer controls.

### Notes

This repair adds:

- `ReplayLayerPreset = operator | debug`
- `viewPreset=operator|debug` URL support
- deterministic `applyLayerPreset(...)` layer defaults
- a replay view preset select in the overlay controls
- operator defaults that show smoothed ball/player/pose, mapped court keypoints, court lines, court
  carry-forward, and court projection mini-map when the matching runs exist
- operator defaults that keep raw TOM v1 keypoints, homography overlays, projection diagnostics,
  camera/view evidence, raw pose, and raw trails off until manually enabled
- debug/audit defaults that enable raw and geometry-debug layers when their run ids exist

Preset changes are UI/read-model display policy only. They do not mutate observations, change model
outputs, accept/reject geometry, or add bounce/hit/in-out/rally/point/scoring, identity, OCR, or
adjudication.

## Ball Trajectory Court Candidate v0

Status: complete

### Goal

Build a derived court-template ball trajectory candidate from existing ball court projection
candidate observations, with velocity/direction/gap diagnostics and no tennis-event truth.

### Notes

This milestone adds:

- worker `build-ball-court-trajectory`
- Makefile `tom-v1-ball-court-trajectory`
- `ball_trajectory_court_candidate` observations
- `observation_family = trajectory`
- segment-level ordered court-template trajectory payloads
- kinematic diagnostics for consecutive projected points
- gap, short-segment, out-of-template, and homography carry-forward diagnostics
- lineage from source `ball_court_projection_candidate` rows
- replay `ballTrajectoryRunId` support
- replay `ball_court_trajectory` layer and `ball_trajectory` timeline lane
- a court projection mini-map trajectory path

The trajectory is derived candidate evidence only. It does not add bounce, hit, in/out,
rally/point/score, player identity, scoreboard OCR, server/receiver logic, accepted/rejected
lifecycle, or adjudication.

## Hit/Bounce Candidate Evidence v0

Status: complete

### Goal

Create first-pass `hit_candidate` and `bounce_candidate` evidence markers from court-space ball
trajectory candidates and main-player court projection candidates without adding truth,
adjudication, in/out, point, or score logic.

### Notes

This milestone adds:

- worker `build-hit-bounce-candidates`
- Makefile `tom-v1-hit-bounce-candidates`
- `hit_candidate` observations
- `bounce_candidate` observations
- `observation_family = event_candidate`
- deterministic trajectory direction/speed diagnostics
- main-player proximity context for hit candidates
- away-from-player and inside/near-template context for bounce candidates
- v0.2 physics repair diagnostics for net-axis reversal, image-y proxy, and speed reduction
- candidate deduplication by time window
- lineage from ball trajectory, ball court projection, and main-player court projection parents
- replay `eventCandidateRunId` support
- replay `event_candidates` timeline lane
- court projection mini-map markers labeled `HIT CANDIDATE` and `BOUNCE CANDIDATE`

The candidates are derived evidence only. They are not confirmed hits, confirmed bounces, in/out
decisions, rally/point/score logic, identity, OCR, accepted/rejected lifecycle, or adjudication.

## Event Candidate Video Overlay v0.1

Status: complete

### Goal

Make existing `hit_candidate` and `bounce_candidate` evidence visible on the broadcast video overlay
without changing event-candidate generation or truth semantics.

### Notes

This repair adds:

- event candidate replay payload `image_point`
- event candidate replay payload `image_marker_source`
- source image-point resolution from `ball_court_projection_candidate.payload.image_point`
- `ReplayEventCandidateVideoOverlay`
- broadcast video markers labeled `HIT CANDIDATE` and `BOUNCE CANDIDATE`
- selected evidence details for image point and marker source
- docs for video overlay behavior and limitations

If the source image point is unavailable, replay keeps the candidate available for timeline and
mini-map review and returns `image_marker_source = unavailable`. The video marker remains candidate
visualization only; it is not hit truth, bounce truth, in/out, point, score, or adjudication.

## Event Candidate Display + Classification Repair v0.1

Status: complete

### Goal

Keep event candidate markers visible across the point/video and prioritize player-proximate
trajectory changes as `hit_candidate` before bounce consideration.

### Notes

This repair adds:

- persistent event candidate video markers
- persistent event candidate mini-map markers
- active/inactive/selected marker states
- selected evidence details for classification priority and player proximity gates
- `hit_first_when_player_proximate` candidate classification priority
- `player_proximity_gate` diagnostics
- `candidate_decision` diagnostics
- focused tests for hit-first priority and persistent marker helper behavior

The markers and classifications remain derived candidate evidence only. They are not hit truth,
bounce truth, in/out, rally/point/score, player identity, accepted/rejected lifecycle, or
adjudication.

## Hit/Bounce Recall Diagnostics + Header Layout Repair v0.2.1

Status: complete

### Goal

Preserve near-side event candidates, recover missing far-side candidates where evidence supports
them, explain rejected contexts, and fix the replay header layout collapse.

### Notes

This repair adds:

- `event_candidate_rejection_diagnostic` observations
- rejection-reason counts in candidate summaries
- `player_proximate_speed_reduction_hit_candidate_fallback_v021`
- configurable `HIT_PLAYER_TIME_WINDOW_MS`
- configurable hit/bounce fallback thresholds
- compact replay header layout
- ellipsized `.replay-media-id`

The local bridge smoke run produced 2 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 29 rejection diagnostics for the sample point. Candidate diagnostics explain
missing or suppressed contexts; they are not truth, in/out, score, or adjudication.

## Hit/Bounce Side-Zone + Sequence Classification Repair v0.2.2

Status: complete

### Goal

Preserve the v0.2.1 event candidate recall while correcting two visible sample-point label errors
with bounded side-zone and sequence context.

### Notes

This repair adds:

- `court_side_zone`
- `player_contact_zone`
- `court_landing_zone`
- `candidate_reclassification`
- `candidate_sequence`
- CLI summary fields for raw counts, final counts, reclassification counts, and
  `physics_heuristic_version = v0.2.2`

The local bridge smoke run produced 2 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 29 rejection diagnostics. It reclassified one raw hit candidate to a
`bounce_candidate` and one raw bounce candidate to a `hit_candidate`.

The side-zone sequence pass is candidate-label repair only. It does not add hit truth, bounce truth,
in/out, rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Player-Anchored Hit Recall v0.2.3

Status: complete

### Goal

Recover obvious hit candidates that local trajectory triples miss when the ball trajectory has a
sparse gap near a main player contact zone.

### Notes

This repair adds:

- `player_anchored_net_axis_reversal_hit_candidate_v023`
- player-anchored hit recall diagnostics in event candidate payloads
- player-anchored rejection diagnostics in `event_candidate_rejection_diagnostic`
- CLI/Makefile thresholds for bounded player-anchored lookback/lookahead windows
- selected evidence display for `player_anchored_hit_recall`
- dedupe behavior that preserves one pre-anchor fallback candidate for side-zone sequence
  classification

The local bridge smoke run produced 3 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 433 rejection diagnostics. Two final hit candidates came from the player-anchored
recall method, including a far-player anchored hit that used a wide-window `court_y` reversal.

This repair improves candidate recall only. It does not add hit truth, bounce truth, in/out,
rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Image-Space Net-Axis Hit Recall v0.2.6

Status: complete

### Goal

Recover airborne far-side hit candidates that are visible in broadcast image space but not cleanly
represented by court-plane `court_y` homography projection.

### Notes

This repair adds:

- `image_space_net_axis_reversal_hit_candidate_v026`
- `broadcast_image_y_axis_fallback_v026`
- `image_space_net_axis_reversal_recall` payload and rejection diagnostics
- direct image-space recall from `ball_court_projection_candidate.image_point` rows when available
- CLI/Makefile controls for the image-space lookback/lookahead, pixel delta, and dedupe distance

The local bridge smoke run produced 4 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 796 rejection diagnostics. One final hit was recovered by the image-space recall
path at frame 54, using incoming frame 34 and outgoing frame 66. Existing bounce candidates
remained present and no image-space hit was suppressed by bounce overlap.

This repair improves candidate recall only. Broadcast image-y is a camera-space fallback, not true
ball height or calibrated court geometry. It does not add hit truth, bounce truth, in/out,
rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Image-Space Direction-Change Hit Recall v0.2.7

Status: complete

### Goal

Recover the remaining visually obvious far-side hit candidate using full 2D broadcast-image
direction change, rather than requiring a clean image-y sign reversal.

### Notes

This repair adds:

- `image_space_direction_change_hit_candidate_v027`
- `broadcast_image_2d_vector_direction_change_v027`
- `image_space_direction_change_recall` payload and rejection diagnostics
- CLI/Makefile controls for the image-space direction lookback/lookahead, vector length, angle
  threshold, pre/post gap, and dedupe distance
- weak pre-bounce overlap suppression for image-space direction-change hits

The local bridge smoke run produced 5 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 870 rejection diagnostics. One final hit was recovered by the image-space
direction-change path at frame 164. One weak image-direction candidate immediately before the frame
81 bounce was suppressed, preserving the false hit-over-bounce protection.

This repair improves candidate recall only. Full 2D broadcast image direction is still camera-space
evidence, not calibrated contact truth. It does not add hit truth, bounce truth, in/out,
rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Local-Evidence Event-Type Classification v0.2.8

Status: complete

### Goal

Classify image-space direction-change candidates with local evidence instead of a hard
hit/bounce alternation assumption.

### Notes

This repair adds:

- `local_evidence_event_type` event candidate payload metadata
- `local_evidence_direction_change_bounce_candidate_v028`
- explicit `sequence_is_hard_gate = false` and `hit_requires_prior_bounce = false` sequence metadata
- selected-evidence replay details for local event-type classification

The local bridge smoke run produced 7 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 868 rejection diagnostics. Two image-space direction-change candidates were
classified locally: one stayed a `hit_candidate`, and one was reclassified to `bounce_candidate`
because it was a court landing-zone direction change without player-contact support.

This repair improves candidate labeling only. A hit candidate does not require a prior bounce, and
sequence is weak diagnostic context only. The repair does not add hit truth, bounce truth, in/out,
rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Universal Hit Candidate Validity Guard v0.2.9

Status: complete

### Goal

Apply a final validity guard to every `hit_candidate` source after the local event-type classifier
and overlap suppressors.

### Notes

This repair adds:

- `universal_hit_validity_guard` event candidate payload metadata
- `universal_hit_guard_bounce_candidate_v029`
- candidate-summary guard counts for evaluated, kept, reclassified, and suppressed hits
- selected-evidence replay details for the final guard decision

The local bridge smoke run produced 7 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 868 rejection diagnostics. The guard evaluated 7 final hit candidates and kept
all 7 in that real sample run. Synthetic tests cover unsupported landing-like hit reclassification
to `bounce_candidate` and fly-through suppression into diagnostics.

The guard is still candidate evidence only. A hit candidate still does not require a prior bounce,
and sequence remains weak diagnostic context. The repair does not add hit truth, bounce truth,
in/out, rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Universal Hit Validity Guard Tightening v0.3.0

Status: complete

### Goal

Tighten the v0.2.9 universal hit-candidate guard so it actively corrects the real sample output
instead of keeping every hit marker.

### Notes

This repair adds:

- `physics_heuristic_version` / guard version `v0.3.0`
- `universal_hit_guard_bounce_candidate_v030`
- hard reversal assessment split into court-y net-axis support, image-y axis support, and weaker
  image-direction support
- reclassification of bounce-like fallback landing hits
- suppression of midcourt image-direction-only fly-through/transit hits

The local bridge smoke run produced 5 `hit_candidate` observations, 3 `bounce_candidate`
observations, and 869 rejection diagnostics. The guard evaluated 7 final hit candidates and
reported `{"keep_as_hit": 5, "reclassify_to_bounce": 1, "suppress_as_diagnostic": 1}`.

The guard is still candidate evidence only. A hit candidate still does not require a prior bounce,
and sequence remains weak diagnostic context. The repair does not add hit truth, bounce truth,
in/out, rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Player-Anchored Hit Contact-Zone Tightening v0.2.4

Status: complete

### Goal

Tighten the v0.2.3 player-anchored hit recall path so it remains anchored to candidate player
contact zones and does not create a hit candidate on top of an open-court bounce/landing marker.

### Notes

This repair adds:

- `player_anchored_contact_zone_net_axis_reversal_hit_candidate_v024`
- `player_anchor_contact_zone` payload and diagnostic metadata
- post-sequence bounce-overlap suppression for player-anchored hit candidates
- `overlap_suppression` payload and diagnostic metadata
- `event_overlap_distance_template`
- `player_anchor_suppressed_overlap_count` candidate summary fields
- selected evidence display for contact-zone and overlap-suppression diagnostics

The local bridge smoke run produced 2 `hit_candidate` observations, 2 `bounce_candidate`
observations, and 655 rejection diagnostics. The frame-34 far-side player-anchored hit that
overlapped the frame-30 far-side bounce was suppressed with
`suppressed_by_bounce_candidate_overlap` and `open_court_landing_zone_anchor` diagnostics.

This repair improves candidate quality only. It does not add hit truth, bounce truth, in/out,
rally/point/score logic, player identity, accepted/rejected lifecycle, or adjudication.

## Event Candidate Review Panel v0

Status: complete

### Goal

Add a compact ordered replay side panel for final visible event markers so operators can review
hit/bounce candidates in sequence.

### Notes

This milestone adds:

- `ReplayEventCandidateReviewPanel`
- chronological marker rows sourced from replay `marker_summary`
- row click-to-seek and click-to-select behavior wired to the existing event-candidate timeline
  selection path
- selected-row highlighting

The panel lists final `hit_candidate` and `bounce_candidate` markers only. It excludes rejection
diagnostics by default and leaves the Replay Marker Inspector plus selected evidence panel as the
detail surfaces.

This is an operator navigation surface only. It does not change hit/bounce generation,
marker-level arbitration, truth status, in/out, score, player identity, accepted/rejected lifecycle,
or adjudication.

## Point Evidence Snapshot v0

Status: complete

### Goal

Create a compact, durable point/run snapshot for operator review and regression comparison.

### Notes

This milestone adds:

- `build-point-evidence-snapshot` worker CLI command
- `tom-v1-point-evidence-snapshot` Make helper
- JSON snapshot output by default
- optional markdown report body/file output
- replay URL, source run ids, counts, active versions, final marker summary, warnings, and known
  limitations

The snapshot reads existing event candidate runs and final marker summaries. It does not change
hit/bounce generation, marker-level arbitration, replay marker behavior, persisted source evidence,
truth status, in/out, score, player identity, accepted/rejected lifecycle, or adjudication.

## Blueprint 8 Completion Review / Freeze v0

Status: complete

### Goal

Freeze the current replay evidence workstation as a coherent, documented, reproducible
candidate-evidence milestone.

### Notes

This milestone adds:

- Blueprint 8 completion review / freeze documentation
- final sample-point reproducibility commands and expected counts
- runbook workflow cleanup for event candidate review and point snapshots
- known limitation freeze language
- control-room/status/progress pointers for the frozen milestone

The sample bridge smoke produced 3 `hit_candidate` observations, 3 `bounce_candidate` observations,
6 final marker-summary rows, and 871 rejection diagnostics for event candidate run
`9cfe4e3a-fad9-4434-b542-37555f9c03b2`. The point evidence snapshot for that run returned the
same marker profile, source run ids, active versions, replay URL, candidate-only warnings, and known
limitations.

This freeze changes documentation only. It does not change hit/bounce candidate generation,
marker-level arbitration, replay behavior, point snapshots, persisted source evidence, truth status,
in/out, score, player identity, accepted/rejected lifecycle, or adjudication.

## Blueprint 9 Manual Candidate Review Annotation v0

Status: complete

### Goal

Allow an operator to attach review metadata to visible event candidate markers and missing-candidate
moments without mutating generated evidence or creating truth.

### Notes

This milestone adds:

- `event_candidate_review_annotation` persistence and migration
- replay API endpoints for list/create/update/delete review annotations
- Replay Marker Inspector controls for `useful`, `wrong`, `unclear`, and `needs_review`
- Event Candidate Review panel badges and summary counts
- Missing Candidate Note panel at the current replay frame/time
- point evidence snapshot `review_summary` and `review_annotations`

The review layer is metadata only. It does not change event candidate generation, candidate counts,
marker-level arbitration, truth status, in/out, score, player identity, accepted/rejected lifecycle,
or adjudication.

## Blueprint 10 Benchmark / Evaluation Harness v0

Status: complete

### Goal

Summarize generated point candidate markers and Blueprint 9 operator review metadata in a compact
CLI/report artifact.

### Notes

This milestone adds:

- `evaluate-point-candidates` worker CLI command
- `tom-v1-evaluate-point-candidates` Make helper
- JSON evaluation output by default
- optional markdown report output
- reviewed/unreviewed final marker coverage
- reviewed-only label fractions
- candidate-type breakdowns
- missing-candidate note summaries

The evaluation harness is read-only. It does not change event candidate generation, marker-level
arbitration, review annotations, source evidence, truth status, in/out, score, player identity,
accepted/rejected lifecycle, automatic correction, or adjudication. It does not compute
precision/recall in v0.

## Blueprint 11 3D Readiness / Camera Geometry Evidence Layer v0

Status: complete

### Goal

Persist explicit camera/court geometry declarations so future 3D evidence work has inspectable
assumptions and no hidden truth upgrades.

### Notes

This milestone adds:

- `camera_geometry_evidence` persistence and migration
- `tom_v3_schema.camera_geometry`
- `declare-camera-geometry` worker CLI command
- `tom-v1-declare-camera-geometry` Make helper
- replay info `camera_geometry_summary`
- replay Camera Geometry readiness panel
- point evidence snapshot `camera_geometry_summary`
- point candidate evaluation `geometry_readiness`

The geometry layer is metadata/readiness only. It does not create true camera calibration, 3D ball
trajectories, hit/bounce truth, in/out, score, player identity, accepted/rejected lifecycle,
automatic correction, or adjudication.

## Blueprint 12 3D Ball Trajectory Candidate Evidence v0

Status: complete

### Goal

Persist provisional 3D ball trajectory candidate evidence from existing 2D court trajectory points
and Blueprint 11 camera geometry declarations.

### Notes

This milestone adds:

- `ball_trajectory_3d_candidate` persistence and migration
- `tom_v3_schema.ball_trajectory_3d`
- `build-3d-ball-trajectory-candidates` worker CLI command
- `tom-v1-build-3d-ball-trajectory-candidates` Make helper
- replay info `trajectory_3d_summary`
- replay 3D Trajectory Candidates side panel
- point evidence snapshot `trajectory_3d_summary`
- point candidate evaluation `trajectory_3d_readiness`

The v0 builder derives metric court-plane x/y candidates from declared court dimensions and keeps
height unknown by default. It does not create true 3D reconstruction, verified ball height,
hit/bounce truth, in/out, score, accepted/rejected lifecycle, automatic correction, or
adjudication.

## Blueprint 13 3D-Assisted Event Candidate Diagnostics v0

Status: complete

### Goal

Attach diagnostic-only 3D context to final visible hit/bounce event candidate markers.

### Notes

This milestone adds:

- `event_candidate_3d_diagnostic` persistence and migration
- `tom_v3_schema.event_candidate_3d_diagnostic`
- `build-event-candidate-3d-diagnostics` worker CLI command
- `tom-v1-build-event-candidate-3d-diagnostics` Make helper
- replay compact diagnostics attached to marker summaries
- point evidence snapshot `event_candidate_3d_diagnostic_summary`
- point candidate evaluation `event_candidate_3d_diagnostics`

The diagnostics link each final marker to nearby 3D trajectory samples when available. They do not
change hit/bounce classification, marker arbitration, candidate counts, review annotations, 3D
trajectory rows, in/out, score, accepted/rejected lifecycle, or adjudication.

## Blueprint 14 3D Trajectory Debug View v0

Status: complete

### Goal

Add a display-only Replay Workstation debug view for existing 3D trajectory candidate evidence.

### Notes

This milestone adds:

- replay `trajectory_3d_debug` payloads for selected `trajectory3dRunId`
- TypeScript types for 3D debug court dimensions and candidate points
- Replay Workstation 3D Debug View SVG panel
- selected-marker nearest 3D sample highlighting from Blueprint 13 diagnostics
- replay API tests for available and unavailable debug payload states

The debug view renders court-plane candidate x/y samples only. It does not draw fake 3D arcs,
claim ball height, change hit/bounce candidates, create in/out, score, accepted/rejected lifecycle,
or adjudication.

## Blueprint 15 3D Debug Selection / Timeline Coupling v0

Status: complete

### Goal

Couple the display-only 3D Debug View to replay time, selected markers, and point selection.

### Notes

This milestone adds:

- current-time nearest 3D sample highlighting
- local ±250ms time-window emphasis
- click/keyboard selection for 3D candidate samples
- replay seek requests from clicked 3D samples
- selected 3D sample metadata
- selected-marker nearest 3D diagnostic highlighting
- legend entries for all/local/current/marker-linked samples

The 3D Debug View may request seek/select behavior through existing replay controls, but it does
not own playback time. It does not change event candidates, marker arbitration, review annotations,
in/out, score, accepted/rejected lifecycle, or adjudication.

## Blueprint 16 3D Debug Review Annotations v0

Status: complete

### Goal

Let operators attach review metadata to 3D Debug View evidence without changing generated
evidence.

### Notes

This milestone adds:

- `trajectory_3d_debug_review_annotation` persistence and migration
- `tom_v3_schema.trajectory_3d_debug_review`
- replay API GET/POST/PATCH endpoints for 3D debug reviews
- 3D sample review controls in Replay Workstation
- marker-linked 3D diagnostic review controls
- missing 3D sample notes at current replay time
- point evidence snapshot `trajectory_3d_debug_review_summary`
- point candidate evaluation `trajectory_3d_debug_reviews`

The reviews are operator metadata only. They do not mutate 3D samples, 3D diagnostics, event
candidates, marker arbitration, in/out, score, accepted/rejected lifecycle, or adjudication.

## Blueprint 17 Reviewed 3D Debug Dataset Export v0

Status: complete

### Goal

Export reviewed 3D debug evidence into deterministic offline JSON/Markdown dataset artifacts.

### Notes

This milestone adds:

- `apps.worker.services.reviewed_3d_debug_dataset_export`
- `export-reviewed-3d-debug-dataset` worker CLI command
- `tom-v1-export-reviewed-3d-debug-dataset` Make helper
- JSON export with media/run IDs, replay URL, camera geometry summary, 3D trajectory summary,
  event marker summary, 3D candidate rows, 3D diagnostic rows, 3D debug reviews, event marker
  reviews, warnings, and limitations
- Markdown export with compact summary tables and examples

The export is dataset/export metadata only. It does not mutate live observations, event candidates,
marker arbitration, 3D candidates, 3D diagnostics, review annotations, in/out, score, or
adjudication. Review labels are not training truth.

## Blueprint 18 Reviewed 3D Debug Dataset Regression v0

Status: complete

### Goal

Compare reviewed 3D debug dataset exports and report deterministic drift.

### Notes

This milestone adds:

- `apps.worker.services.reviewed_3d_debug_dataset_regression`
- `compare-reviewed-3d-debug-dataset` worker CLI command
- `tom-v1-compare-reviewed-3d-debug-dataset` Make helper
- JSON regression reports with summary count drift, section drift, row drift, and warning drift
- Markdown regression reports with compact count and drift tables
- strict mode that returns `failed_regression` when drift is detected

The report is export-to-export comparison metadata only. Baseline exports are not truth or training
truth. Drift does not mutate live observations, event candidates, marker arbitration, 3D candidates,
3D diagnostics, review annotations, in/out, score, or adjudication.

## Blueprint 19 Reviewed 3D Debug Baseline Freeze v0

Status: complete

### Goal

Freeze the current sample-point reviewed 3D debug export profile and provide a repeatable local
regression gate against that baseline.

### Notes

This milestone adds:

- `apps.worker.services.reviewed_3d_debug_baseline`
- `freeze-reviewed-3d-debug-baseline` worker CLI command
- `verify-reviewed-3d-debug-baseline` worker CLI command
- `tom-v1-freeze-reviewed-3d-debug-baseline` Make helper
- `tom-v1-verify-reviewed-3d-debug-baseline` Make helper
- local baseline JSON/Markdown export and manifest workflow
- local current export plus regression report gate workflow

The baseline and gate are regression metadata only. The baseline is not truth or training truth.
The gate does not mutate live observations, event candidates, marker arbitration, 3D candidates,
3D diagnostics, review annotations, in/out, score, or adjudication.

## Blueprint 20 sample_point Completion Review / Expansion Readiness v0

Status: complete

### Goal

Document the current `sample_point` completion state and freeze the expansion readiness gate before
introducing a second point.

### Notes

This milestone adds:

- `docs/reviews/sample_point_completion_review_v0.md`
- `docs/reviews/sample_point_expansion_readiness_v0.md`
- `docs/agent_reports/blueprint_20_sample_point_completion_review_expansion_readiness_v0_report.md`
- a runbook section for the sample-point expansion readiness gate

The review confirms six event markers, three hit candidates, three bounce candidates, 68 provisional
3D trajectory candidates with unknown height, six event candidate 3D diagnostics, one event-marker
review, zero 3D debug reviews, and a no-drift reviewed 3D debug baseline gate. It changes no
candidate generation, marker arbitration, 3D candidate generation, 3D diagnostics, review
annotations, replay UI, in/out, score, or adjudication.

## Blueprint 21 Second Point Ingestion / Evidence Replay Smoke v0

Status: complete

### Goal

Introduce one additional local point/video as an isolated evidence sample and prove it can open in
Replay Workstation without changing the protected `sample_point` baseline.

### Notes

This milestone adds:

- `apps.worker.services.second_point_smoke`
- `ingest-second-point-smoke` worker CLI command
- `tom-v1-ingest-second-point-smoke` Make helper
- `docs/blueprints/blueprint_21_second_point_ingestion_evidence_replay_smoke_v0.md`
- `docs/reviews/second_point_ingestion_smoke_v0.md`
- `docs/agent_reports/blueprint_21_second_point_ingestion_evidence_replay_smoke_v0_report.md`

The smoke path validates an operator-provided local video path, indexes it with existing media
ingestion/probe/storage code, and returns a replay URL. A second point with no event candidates and
no 3D candidates is valid. This milestone changes no hit/bounce logic, marker arbitration, 3D
candidate generation, 3D diagnostics, review annotations, replay semantics, in/out, score, or
adjudication.

## Blueprint 22 Second Point Evidence Parity / Protected Baseline Gate v0

Status: complete

### Goal

Convert the second-point ingestion smoke into a protected second-point evidence parity checkpoint
with a local baseline manifest.

### Notes

This milestone adds:

- `apps.worker.services.second_point_evidence_parity`
- `build-second-point-evidence-parity` worker CLI command
- `tom-v1-build-second-point-evidence-parity` Make helper
- `.data/baselines/second_point_evidence_parity.baseline_manifest.json` generated manifest path
- `docs/blueprints/blueprint_22_second_point_evidence_parity_baseline_gate_v0.md`
- `docs/reviews/second_point_evidence_parity_v0.md`
- `docs/agent_reports/blueprint_22_second_point_evidence_parity_baseline_gate_v0_report.md`

The parity service orchestrates existing media ingestion/replay read-model behavior only. It records
whether event candidates, 3D candidates, and review annotations exist for the second media asset.
It does not generate candidates, modify marker arbitration, generate 3D evidence, create reviews,
mutate the protected `sample_point` baseline, decide in/out, score, or adjudicate evidence.

## Blueprint 23 Point Manifest / Evidence Provenance Contract v0

Status: complete

### Goal

Create a durable point-level manifest/provenance contract for describing an evidence point without
creating truth, adjudication, scoring, player identity, event generation, or 3D generation.

### Notes

This milestone adds:

- `apps.worker.services.point_manifest`
- `build-point-manifest` worker CLI command
- `tom-v1-build-point-manifest` Make helper
- `.data/manifests/<point_manifest_id>.json` generated manifest path
- `docs/blueprints/blueprint_23_point_manifest_evidence_provenance_contract_v0.md`
- `docs/reviews/point_manifest_evidence_provenance_contract_v0.md`
- `docs/agent_reports/blueprint_23_point_manifest_evidence_provenance_contract_v0_report.md`

The manifest service reads existing media and evidence tables, records availability booleans and
profile counts, and writes one local JSON manifest. It does not generate evidence, change review
metadata, mutate protected baselines, decide in/out, score, identify players, determine a winner,
or adjudicate evidence.

## Blueprint 24 Multi-Point Replay Navigation / Review Surface v0

Status: complete

### Goal

Make point manifests usable as replay navigation/review units without creating truth, scoring,
player identity, event generation, 3D generation, or adjudication.

### Notes

This milestone adds:

- `apps.worker.services.multi_point_replay_index`
- `build-multi-point-replay-index` worker CLI command
- `tom-v1-build-multi-point-replay-index` Make helper
- `.data/manifests/multi_point_replay_index.json` generated index path
- `GET /replay/point-manifests`
- Replay Workstation point navigator
- `docs/blueprints/blueprint_24_multi_point_replay_navigation_review_surface_v0.md`
- `docs/reviews/multi_point_replay_navigation_review_surface_v0.md`
- `docs/agent_reports/blueprint_24_multi_point_replay_navigation_review_surface_v0_report.md`

The index service reads existing point manifest JSON, preserves replay run-ID context, reports
evidence availability/profile counts, and labels protected sample-point or second-point stand-in
contexts only when inferable from manifest provenance. It does not generate evidence, change review
metadata, mutate protected baselines, decide in/out, score, identify players, determine a winner,
or adjudicate evidence.

## Blueprint 25 Multi-Point Regression Matrix / Baseline Expansion v0

Status: complete

### Goal

Turn manifest-backed replay points into a regression-protected evidence matrix without creating
truth, scoring, player identity, event generation, 3D generation, or adjudication.

### Notes

This milestone adds:

- `apps.worker.services.multi_point_regression_matrix`
- `build-multi-point-regression-matrix` worker CLI command
- `compare-multi-point-regression-matrix` worker CLI command
- `verify-multi-point-regression-matrix` worker CLI command
- `tom-v1-build-multi-point-regression-matrix` Make helper
- `tom-v1-compare-multi-point-regression-matrix` Make helper
- `tom-v1-verify-multi-point-regression-matrix` Make helper
- `.data/baselines/multi_point_regression_matrix.baseline.json` local baseline path
- `.data/exports/multi_point_regression_matrix.current.json` local current path
- `.data/exports/multi_point_regression_matrix.regression.json` local regression path
- `.data/exports/multi_point_regression_matrix.regression.md` local Markdown path
- `docs/blueprints/blueprint_25_multi_point_regression_matrix_baseline_expansion_v0.md`
- `docs/reviews/multi_point_regression_matrix_baseline_expansion_v0.md`
- `docs/agent_reports/blueprint_25_multi_point_regression_matrix_baseline_expansion_v0_report.md`

The matrix service reads the Blueprint 24 replay index and associated Blueprint 23 point manifest
files, preserves replay/run/evidence/profile/warning context, and compares baseline/current matrix
artifacts. Added manifest-backed points are non-breaking by default. Protected sample-point drift
and matrix warning/type/version contract failures are breaking. The service does not generate
evidence, change review metadata, mutate protected baselines, decide in/out, score, identify
players, determine a winner, claim generalization, or adjudicate evidence.

## Blueprint 26 Observation Quality Taxonomy v1

Status: complete

### Goal

Create a versioned observation-quality taxonomy and conservative profile builder without creating
truth, scoring, player identity, event generation, 3D generation, or adjudication.

### Notes

This milestone adds:

- `apps.worker.services.observation_quality_taxonomy`
- `export-observation-quality-taxonomy` worker CLI command
- `build-observation-quality-profile` worker CLI command
- `tom-v1-export-observation-quality-taxonomy` Make helper
- `tom-v1-build-observation-quality-profile` Make helper
- `.data/contracts/observation_quality_taxonomy_v1.json` local contract path
- `.data/exports/observation_quality_profile.current.json` local profile path
- `docs/blueprints/blueprint_26_observation_quality_taxonomy_v1.md`
- `docs/reviews/observation_quality_taxonomy_v1.md`
- `docs/agent_reports/blueprint_26_observation_quality_taxonomy_v1_report.md`

The taxonomy defines neutral quality dimensions and allowed values for review support. The profile
service reads the Blueprint 24 replay index only, preserves point/replay/run/evidence/profile
context, marks visual quality as `unknown` when media context exists, marks missing evidence as
`unavailable`, and flags dimensions that require human review. It does not inspect video, generate
evidence, change review metadata, mutate protected baselines, decide in/out, score, identify
players, determine a winner, claim generalization, or adjudicate evidence.

## Blueprint 27 Structured Review Label Schema v1

Status: complete

### Goal

Create a versioned structured review label schema for future human-provided labels without creating
truth, scoring, player identity, event generation, 3D generation, correctness claims, or
adjudication.

### Notes

This milestone adds:

- `apps.worker.services.review_label_schema`
- `export-review-label-schema` worker CLI command
- `build-review-label-template` worker CLI command
- `validate-review-label-bundle` worker CLI command
- `tom-v1-export-review-label-schema` Make helper
- `tom-v1-build-review-label-template` Make helper
- `tom-v1-validate-review-label-bundle` Make helper
- `.data/contracts/review_label_schema_v1.json` local contract path
- `.data/exports/review_label_template.current.json` local template path
- `.data/exports/review_label_bundle.validation.json` local validation path
- `docs/blueprints/blueprint_27_structured_review_label_schema_v1.md`
- `docs/reviews/structured_review_label_schema_v1.md`
- `docs/agent_reports/blueprint_27_structured_review_label_schema_v1_report.md`

The schema defines neutral human-review label families, label definitions, value sets, provenance
requirements, validation rules, and warnings. The template builder emits blank `not_assessed`
entries and does not infer labels. The validator checks bundle structure, known label keys, allowed
values, forbidden fields, and human-only flags. It does not generate evidence, create labels,
change review semantics, mutate protected baselines, decide in/out, score, identify players,
determine a winner, claim generalization, validate correctness, or adjudicate evidence.

## Blueprint 28 Reviewer Confidence / Ambiguity Capture v1

Status: complete

### Goal

Create a versioned reviewer confidence and ambiguity metadata schema for future human-provided
review uncertainty without creating truth, scoring, player identity, event generation, 3D
generation, correctness claims, automatic confidence scoring, or adjudication.

### Notes

This milestone adds:

- `apps.worker.services.reviewer_confidence_schema`
- `export-reviewer-confidence-schema` worker CLI command
- `build-reviewer-confidence-template` worker CLI command
- `validate-reviewer-confidence-bundle` worker CLI command
- `tom-v1-export-reviewer-confidence-schema` Make helper
- `tom-v1-build-reviewer-confidence-template` Make helper
- `tom-v1-validate-reviewer-confidence-bundle` Make helper
- `tom-v1-post-codex-validate` Make helper
- `.data/contracts/reviewer_confidence_ambiguity_schema_v1.json` local contract path
- `.data/exports/reviewer_confidence_ambiguity_template.current.json` local template path
- `.data/exports/reviewer_confidence_ambiguity.validation.json` local validation path
- `docs/blueprints/blueprint_28_reviewer_confidence_ambiguity_capture_v1.md`
- `docs/reviews/reviewer_confidence_ambiguity_capture_v1.md`
- `docs/agent_reports/blueprint_28_reviewer_confidence_ambiguity_capture_v1_report.md`

The schema defines neutral human-review confidence, ambiguity, ambiguity reason,
evidence-sufficiency, additional-review, time-spent, and review-context metadata. The template
builder emits blank `not_assessed` entries and does not infer confidence or ambiguity. The validator
checks bundle structure, allowed values, optional Blueprint 27 label keys, forbidden fields, and
human-only flags. It does not generate evidence, create labels, change review semantics, mutate
protected baselines, decide in/out, score, identify players, determine a winner, claim
generalization, validate correctness, score confidence automatically, or adjudicate evidence.

## Blueprint 29 Multi-Reviewer / Disagreement Foundation v1

Status: complete

### Goal

Create a versioned multi-reviewer review-set and disagreement-report foundation for multiple
human-provided review inputs without creating truth, scoring, player identity, event generation,
3D generation, reviewer ranking, reviewer scoring, disagreement resolution, correctness claims, or
adjudication.

### Notes

This milestone adds:

- `apps.worker.services.multi_reviewer_disagreement`
- `export-multi-reviewer-disagreement-schema` worker CLI command
- `build-multi-reviewer-review-set-template` worker CLI command
- `validate-multi-reviewer-review-set` worker CLI command
- `build-reviewer-disagreement-report` worker CLI command
- `tom-v1-export-multi-reviewer-disagreement-schema` Make helper
- `tom-v1-build-multi-reviewer-review-set-template` Make helper
- `tom-v1-validate-multi-reviewer-review-set` Make helper
- `tom-v1-build-reviewer-disagreement-report` Make helper
- `.data/contracts/multi_reviewer_disagreement_schema_v1.json` local contract path
- `.data/exports/multi_reviewer_review_set_template.current.json` local template path
- `.data/exports/multi_reviewer_review_set.validation.json` local validation path
- `.data/exports/reviewer_disagreement_report.current.json` local report path
- `docs/blueprints/blueprint_29_multi_reviewer_disagreement_foundation_v1.md`
- `docs/reviews/multi_reviewer_disagreement_foundation_v1.md`
- `docs/agent_reports/blueprint_29_multi_reviewer_disagreement_foundation_v1_report.md`

The schema defines pseudonymous reviewer identity policy, reviewer entry definitions,
disagreement dimensions, disagreement values, provenance requirements, validation rules, and
warnings. The template builder emits blank reviewer entries and does not infer reviewer input. The
validator checks review-set structure, reviewer IDs, forbidden fields, disallowed reviewer identity
fields, human-only flags, and referenced Blueprint 27/28 bundles when paths are present. The report
builder compares human-provided values structurally. It does not generate evidence, create labels,
change review semantics, mutate protected baselines, decide in/out, score, identify players,
determine a winner, claim generalization, validate correctness, rank reviewers, score reviewers,
resolve disagreement, or adjudicate evidence.

## Blueprint 30 INTENNSE Label Alignment Contract v1

Status: complete

### Goal

Create a versioned alignment contract between TOM observation/review/provenance structures and
future INTENNSE expert interpretation label references without importing labels, creating labels,
deciding truth, resolving disagreement, scoring reviewers, producing coaching/tactical conclusions,
or adjudicating evidence.

### Notes

This milestone adds:

- `apps.worker.services.intennse_label_alignment`
- `export-intennse-label-alignment-contract` worker CLI command
- `build-intennse-alignment-template` worker CLI command
- `validate-intennse-alignment-bundle` worker CLI command
- `build-intennse-alignment-report` worker CLI command
- `tom-v1-export-intennse-label-alignment-contract` Make helper
- `tom-v1-build-intennse-alignment-template` Make helper
- `tom-v1-validate-intennse-alignment-bundle` Make helper
- `tom-v1-build-intennse-alignment-report` Make helper
- `.data/contracts/intennse_label_alignment_contract_v1.json` local contract path
- `.data/exports/intennse_alignment_template.current.json` local template path
- `.data/exports/intennse_alignment_bundle.validation.json` local validation path
- `.data/exports/intennse_alignment_report.current.json` local report path
- `docs/blueprints/blueprint_30_intennse_label_alignment_contract_v1.md`
- `docs/reviews/intennse_label_alignment_contract_v1.md`
- `docs/agent_reports/blueprint_30_intennse_label_alignment_contract_v1_report.md`

The contract defines TOM schema refs for Blueprints 26 through 29, alignment entities, alignment
fields, neutral value sets, provenance requirements, validation rules, and warning flags. The
template builder emits blank human-provided alignment entries. The validator checks contract
shape, TOM contract references, allowed entities/values, forbidden fields, and human-only flags.
The report summarizes reference presence and provenance issues structurally. It does not generate
evidence, create TOM or INTENNSE labels, change review semantics, mutate protected baselines,
decide in/out, score, identify players, determine a winner, claim generalization, validate
correctness, resolve disagreement, produce INTENNSE coaching/tactical/match-outcome conclusions,
or adjudicate evidence.

## Blueprint 31 Versioned Dataset Corpus v1

Status: complete

### Goal

Create a versioned dataset corpus contract and manifest/report layer that packages existing TOM
evidence, provenance, review-support structures, reviewer confidence/ambiguity, multi-reviewer
disagreement structure, INTENNSE alignment references, and regression context without creating
truth, training truth, labels, correctness claims, tennis outcomes, reviewer scoring, disagreement
resolution, or adjudication.

### Notes

This milestone adds:

- `apps.worker.services.versioned_dataset_corpus`
- `export-versioned-dataset-corpus-contract` worker CLI command
- `build-versioned-dataset-corpus-manifest` worker CLI command
- `validate-versioned-dataset-corpus-manifest` worker CLI command
- `build-versioned-dataset-corpus-report` worker CLI command
- `tom-v1-export-versioned-dataset-corpus-contract` Make helper
- `tom-v1-build-versioned-dataset-corpus-manifest` Make helper
- `tom-v1-validate-versioned-dataset-corpus-manifest` Make helper
- `tom-v1-build-versioned-dataset-corpus-report` Make helper
- `.data/contracts/versioned_dataset_corpus_contract_v1.json` local contract path
- `.data/exports/versioned_dataset_corpus_manifest.current.json` local manifest path
- `.data/exports/versioned_dataset_corpus_manifest.validation.json` local validation path
- `.data/exports/versioned_dataset_corpus_report.current.json` local report path
- `docs/blueprints/blueprint_31_versioned_dataset_corpus_v1.md`
- `docs/reviews/versioned_dataset_corpus_v1.md`
- `docs/agent_reports/blueprint_31_versioned_dataset_corpus_v1_report.md`

The contract defines corpus scope, corpus entities, corpus entry fields, neutral split/status value
sets, versioning policy, provenance requirements, validation rules, and refs for Blueprints 23,
25, and 26 through 30. The manifest builder reads existing replay-index and regression-matrix
artifacts, preserves replay/run/evidence/profile context, and records missing optional
review/INTENNSE/export refs as provenance gaps. The validator checks structure and referenced
contract versions. The report summarizes corpus entries and provenance coverage structurally. It
does not generate evidence, create labels, change review semantics, mutate protected baselines,
decide in/out, score, identify players, determine a winner, claim generalization, validate
correctness, score reviewers, resolve disagreement, produce INTENNSE coaching/tactical/match
outcome conclusions, create training truth, or adjudicate evidence.

## Blueprint 32 Coverage-Driven Sampling Strategy v1

Status: complete

### Goal

Create a versioned coverage-driven sampling strategy contract and report layer that identifies
structural evidence, provenance, review, and alignment coverage gaps for future dataset expansion
without executing sampling, ingesting media, creating observations, creating labels, deciding
truth, scoring correctness, claiming generalization, resolving disagreement, or adjudicating
evidence.

### Notes

This milestone adds:

- `apps.worker.services.coverage_driven_sampling_strategy`
- `export-coverage-sampling-strategy-contract` worker CLI command
- `build-coverage-sampling-profile` worker CLI command
- `validate-coverage-sampling-profile` worker CLI command
- `build-coverage-sampling-report` worker CLI command
- `tom-v1-export-coverage-sampling-strategy-contract` Make helper
- `tom-v1-build-coverage-sampling-profile` Make helper
- `tom-v1-validate-coverage-sampling-profile` Make helper
- `tom-v1-build-coverage-sampling-report` Make helper
- `.data/contracts/coverage_sampling_strategy_contract_v1.json` local contract path
- `.data/exports/coverage_sampling_profile.current.json` local profile path
- `.data/exports/coverage_sampling_profile.validation.json` local validation path
- `.data/exports/coverage_sampling_report.current.json` local report path
- `docs/blueprints/blueprint_32_coverage_driven_sampling_strategy_v1.md`
- `docs/reviews/coverage_driven_sampling_strategy_v1.md`
- `docs/agent_reports/blueprint_32_coverage_driven_sampling_strategy_v1_report.md`

The contract defines coverage scope, source contract refs, coverage axes, coverage gap types,
sampling priority values, candidate fields, allowed next-action values, provenance requirements,
validation rules, and warnings. The profile builder reads the existing dataset corpus manifest,
preserves replay/run/evidence/profile context, and records missing optional review/INTENNSE refs as
coverage gaps. The validator checks structure and referenced contract versions. The report
summarizes coverage axes, gaps, priorities, missing optional refs, and candidate counts
structurally. It does not generate evidence, create labels, change review semantics, mutate
protected baselines, decide in/out, score, identify players, determine a winner, claim
generalization, validate correctness, score reviewers, resolve disagreement, produce INTENNSE
coaching/tactical/match outcome conclusions, create training truth, ingest media, execute
sampling, or adjudicate evidence.

## Blueprint 33 Many-Point Evidence Ingestion Gate v1

Status: complete

### Goal

Create a controlled many-point evidence ingestion gate that validates, plans, and optionally
indexes explicitly supplied local point/video files as replayable evidence assets without creating
truth, event generation, 3D generation, scoring, adjudication, review labels, or generalization
claims.

### Notes

This milestone adds:

- `apps.worker.services.many_point_ingestion_gate`
- `export-many-point-ingestion-gate-contract` worker CLI command
- `build-many-point-ingestion-manifest-template` worker CLI command
- `validate-many-point-ingestion-manifest` worker CLI command
- `build-many-point-ingestion-plan` worker CLI command
- `run-many-point-ingestion-gate` worker CLI command
- `tom-v1-export-many-point-ingestion-gate-contract` Make helper
- `tom-v1-build-many-point-ingestion-manifest-template` Make helper
- `tom-v1-validate-many-point-ingestion-manifest` Make helper
- `tom-v1-build-many-point-ingestion-plan` Make helper
- `tom-v1-run-many-point-ingestion-gate` Make helper
- `.data/contracts/many_point_ingestion_gate_contract_v1.json` local contract path
- `.data/exports/many_point_ingestion_manifest.template.json` local template path
- `.data/exports/many_point_ingestion_manifest.validation.json` local validation path
- `.data/exports/many_point_ingestion_plan.current.json` local plan path
- `.data/exports/many_point_ingestion_gate.current.json` local gate report path
- `docs/blueprints/blueprint_33_many_point_evidence_ingestion_gate_v1.md`
- `docs/reviews/many_point_evidence_ingestion_gate_v1.md`
- `docs/agent_reports/blueprint_33_many_point_evidence_ingestion_gate_v1_report.md`

The contract defines ingestion scope, source contract refs, manifest schema, entry fields,
requested action values, disallowed requested actions, execution modes, output contracts,
provenance requirements, validation rules, and warnings. The validator checks explicit local media
paths, file existence, duplicate path/checksum conflicts, requested actions, expected media type,
and forbidden fields. Dry-run planning and gate reports do not persist media. Explicit write modes
reuse existing media indexing and point-manifest behavior only when selected. The gate does not
generate evidence, create labels, change review semantics, mutate protected baselines, decide
in/out, score, identify players, determine a winner, claim generalization, validate correctness,
score reviewers, resolve disagreement, produce INTENNSE coaching/tactical/match outcome
conclusions, create training truth, silently ingest media, discover media automatically, run event
generation, run 3D generation, or adjudicate evidence.

## Blueprint 34 Review Operations Metrics / Label Throughput Dashboard v1

Status: complete

### Goal

Create a read-only review-operations metrics contract, structural report, report validation, and
dashboard-data JSON layer that summarizes review artifact coverage and missing operational refs
without changing evidence, labels, truth, scoring, ingestion, sampling, or adjudication behavior.

### Notes

This milestone adds:

- `apps.worker.services.review_ops_metrics`
- `export-review-ops-metrics-contract` worker CLI command
- `build-review-ops-metrics-report` worker CLI command
- `validate-review-ops-metrics-report` worker CLI command
- `build-review-ops-dashboard-data` worker CLI command
- `tom-v1-export-review-ops-metrics-contract` Make helper
- `tom-v1-build-review-ops-metrics-report` Make helper
- `tom-v1-validate-review-ops-metrics-report` Make helper
- `tom-v1-build-review-ops-dashboard-data` Make helper
- `.data/contracts/review_ops_metrics_contract_v1.json` local contract path
- `.data/exports/review_ops_metrics_report.current.json` local report path
- `.data/exports/review_ops_metrics_report.validation.json` local validation path
- `.data/exports/review_ops_dashboard_data.current.json` local dashboard-data path
- `docs/blueprints/blueprint_34_review_ops_metrics_dashboard_v1.md`
- `docs/reviews/review_ops_metrics_dashboard_v1.md`
- `docs/agent_reports/blueprint_34_review_ops_metrics_dashboard_v1_report.md`

The contract defines metrics scope, source contract refs, metric groups, dashboard-card schema,
report schema, allowed structural status values, provenance requirements, validation rules, and
warnings. The report builder reads existing dataset corpus, coverage sampling, and ingestion gate
outputs where available, then summarizes structural counts and gaps. The validator checks contract
shape, report shape, dashboard-card schema, allowed status values, and referenced contract
versions. Dashboard data is derived read-only JSON. It does not generate evidence, create labels,
change review semantics, mutate protected baselines, decide in/out, score, identify players,
determine a winner, claim generalization, validate correctness, score or rank reviewers, resolve
disagreement, produce INTENNSE coaching/tactical/match outcome conclusions, create training truth,
ingest media, execute sampling, or adjudicate evidence.

## Blueprint 35 Label Feedback Loop into Evaluation Harness v1

Status: complete

### Goal

Create a safe label-feedback evaluation bridge from TOM review artifacts into the evaluation
harness without creating labels, truth, adjudication, automatic model behavior changes, or tennis
conclusions.

### Notes

This milestone adds:

- `apps.worker.services.label_feedback_evaluation`
- `export-label-feedback-evaluation-contract` worker CLI command
- `build-label-feedback-evaluation-inputs` worker CLI command
- `validate-label-feedback-evaluation-inputs` worker CLI command
- `build-label-feedback-evaluation-report` worker CLI command
- `tom-v1-export-label-feedback-evaluation-contract` Make helper
- `tom-v1-build-label-feedback-evaluation-inputs` Make helper
- `tom-v1-validate-label-feedback-evaluation-inputs` Make helper
- `tom-v1-build-label-feedback-evaluation-report` Make helper
- `.data/contracts/label_feedback_evaluation_contract_v1.json` local contract path
- `.data/exports/label_feedback_evaluation_inputs.current.json` local inputs path
- `.data/exports/label_feedback_evaluation_inputs.validation.json` local validation path
- `.data/exports/label_feedback_evaluation_report.current.json` local report path
- `docs/blueprints/blueprint_35_label_feedback_loop_evaluation_harness_v1.md`
- `docs/reviews/label_feedback_loop_evaluation_harness_v1.md`
- `docs/agent_reports/blueprint_35_label_feedback_loop_evaluation_harness_v1_report.md`

The contract defines feedback scope, source contract refs, feedback input entities/fields,
evaluation signal/action/status values, provenance requirements, validation rules, and warnings.
The input builder reads existing dataset corpus, review-ops, coverage sampling, and multi-point
regression matrix outputs where available, then emits structural feedback entries. The validator
checks contract shape, input shape, allowed signal/status/action values, forbidden fields/values,
and referenced contract versions. The report summarizes structural feedback entries, missing
review artifacts, provenance gaps, coverage gaps, and regression context. It does not generate
evidence, create labels, change review semantics, mutate protected baselines, decide in/out,
score, identify players, determine a winner, claim generalization, score or rank reviewers,
resolve disagreement, produce INTENNSE coaching/tactical/match outcome conclusions, create
training truth, retrain models, ingest media, execute sampling, or adjudicate evidence.

## Blueprint 36 Camera Geometry Confidence / Calibration Provenance v1

Status: complete

### Goal

Create a read-only camera geometry / calibration provenance layer that summarizes structural
readiness, provenance completeness, review needs, and diagnostic coverage for camera geometry,
court geometry, homography, projection, replay, and review evidence.

### Notes

This milestone adds:

- `apps.worker.services.camera_geometry_calibration_provenance`
- `export-camera-geometry-calibration-provenance-contract` worker CLI command
- `build-camera-geometry-calibration-profile` worker CLI command
- `validate-camera-geometry-calibration-profile` worker CLI command
- `build-camera-geometry-calibration-report` worker CLI command
- `tom-v1-export-camera-geometry-calibration-provenance-contract` Make helper
- `tom-v1-build-camera-geometry-calibration-profile` Make helper
- `tom-v1-validate-camera-geometry-calibration-profile` Make helper
- `tom-v1-build-camera-geometry-calibration-report` Make helper
- `.data/contracts/camera_geometry_calibration_provenance_contract_v1.json` local contract path
- `.data/exports/camera_geometry_calibration_profile.current.json` local profile path
- `.data/exports/camera_geometry_calibration_profile.validation.json` local validation path
- `.data/exports/camera_geometry_calibration_report.current.json` local report path
- `docs/blueprints/blueprint_36_camera_geometry_confidence_calibration_provenance_v1.md`
- `docs/reviews/camera_geometry_confidence_calibration_provenance_v1.md`
- `docs/agent_reports/blueprint_36_camera_geometry_confidence_calibration_provenance_v1_report.md`

The contract defines calibration scope, source contract refs, camera geometry entities, profile
schema, report schema, confidence/evidence/provenance/review status values, provenance
requirements, validation rules, and warnings. The profile builder reads existing replay index,
multi-point regression matrix, versioned corpus, and label-feedback inputs where available, then
emits structural camera-geometry calibration profiles. The validator checks contract shape, profile
shape, allowed status values, forbidden fields/values, and referenced contract versions. The report
summarizes camera geometry evidence presence, missing projection diagnostics, partial provenance,
review needs, human-review readiness, and regression-protected context. It does not generate
camera geometry, homography, projection diagnostics, event candidates, 3D candidates, labels,
training truth, in/out, score, player identity, winner, tactical conclusions, reviewer ranking,
reviewer scoring, or adjudication.

## Blueprint 37 TOM v3 Expansion Completion Freeze / Next-Phase Readiness v1

Status: complete

### Goal

Freeze the completed TOM v3 expansion path from Blueprint 22 through Blueprint 36 as a tracked
provenance/readiness contract and record the recommended first next-phase capability without
adding evidence generation, truth, scoring, adjudication, or gameplay classifier wiring.

### Notes

This milestone adds:

- `apps.worker.services.tom_v3_expansion_completion_freeze`
- `build-tom-v3-expansion-completion-freeze` worker CLI command
- `validate-tom-v3-expansion-completion-freeze` worker CLI command
- `build-tom-v3-next-phase-readiness-report` worker CLI command
- `tom-v1-build-tom-v3-expansion-completion-freeze` Make helper
- `tom-v1-validate-tom-v3-expansion-completion-freeze` Make helper
- `tom-v1-build-tom-v3-next-phase-readiness-report` Make helper
- `.data/contracts/tom_v3_expansion_completion_freeze_v1.json` tracked freeze path
- `.data/exports/tom_v3_expansion_completion_freeze.validation.json` local validation path
- `.data/exports/tom_v3_next_phase_readiness_report.current.json` local report path
- `docs/blueprints/blueprint_37_tom_v3_expansion_completion_freeze_v1.md`
- `docs/reviews/tom_v3_expansion_completion_freeze_v1.md`
- `docs/agent_reports/blueprint_37_tom_v3_expansion_completion_freeze_v1_report.md`

The freeze manifest records completed BP22-BP36 milestones, 11 frozen contract refs, protected
baseline refs, required regression gates, capability summary, non-claims, known limitations,
validation summary, and warnings. The validator checks shape, expected tracked refs, generated
export tracking, frozen contract cleanliness, and forbidden claim tokens. The readiness report
records Gameplay Segment Gate / TOM v1 View Classifier Integration v1 as the recommended first
next phase with `model_assets/tom_v1/view_classifier_gameplay.pt`. It does not generate evidence,
ingest media, execute sampling, create labels, mutate baselines, retrain models, wire gameplay
classification, decide in/out, score, identify players, determine winners, make coaching/tactical
conclusions, make betting/prediction claims, claim generalization, or adjudicate evidence.

## Blueprint 38 Gameplay Segment Gate / TOM v1 View Classifier Integration v1

Status: complete

### Goal

Add a candidate-only gameplay observation suitability gate around the existing local TOM v1
gameplay classifier asset without creating tennis truth, scoring, adjudication, downstream
perception execution, or model asset mutations.

### Notes

This milestone adds:

- `apps.worker.services.gameplay_segment_gate`
- `export-gameplay-segment-gate-contract` worker CLI command
- `inspect-gameplay-classifier-asset` worker CLI command
- `build-gameplay-segment-candidates` worker CLI command
- `validate-gameplay-segment-candidates` worker CLI command
- `build-gameplay-segment-report` worker CLI command
- `tom-v1-export-gameplay-segment-gate-contract` Make helper
- `tom-v1-inspect-gameplay-classifier-asset` Make helper
- `tom-v1-build-gameplay-segment-candidates` Make helper
- `tom-v1-validate-gameplay-segment-candidates` Make helper
- `tom-v1-build-gameplay-segment-report` Make helper
- `.data/contracts/gameplay_segment_gate_contract_v1.json` tracked contract path
- `.data/exports/gameplay_classifier_asset_inspection.current.json` local asset inspection path
- `.data/exports/gameplay_segment_candidates.current.json` local candidate path
- `.data/exports/gameplay_segment_candidates.validation.json` local validation path
- `.data/exports/gameplay_segment_report.current.json` local report path
- `docs/blueprints/blueprint_38_gameplay_segment_gate_tom_v1_view_classifier_v1.md`
- `docs/reviews/gameplay_segment_gate_tom_v1_view_classifier_v1.md`
- `docs/agent_reports/blueprint_38_gameplay_segment_gate_tom_v1_view_classifier_v1_report.md`

The contract defines gate scope, model asset provenance, classification output schema, temporal
segment schema, smoothing/hysteresis defaults, downstream gate status values, validation rules,
provenance requirements, and warnings. The candidate builder reads explicit media input only,
hashes the local classifier asset when present, emits candidate classification rows, groups them
into candidate segments, and includes a replay timeline lane. The validator checks contract shape,
asset provenance shape, candidate shape, allowed statuses, required hashes when the asset exists,
and forbidden fields/values. The report summarizes structural gate output only. Blueprint 38 does
not decide gameplay truth, in/out, score, point winner, player identity, line calls, model
correctness, training truth, production truth, or adjudication, and it does not run detections,
tracklets, pose, court, event, or 3D jobs.

## Blueprint 39 Gameplay-Gated Evidence Pipeline Routing v1

Status: complete

### Goal

Turn Blueprint 38 gameplay segment candidates into structural downstream routing plans without
running downstream evidence generation, creating tennis truth, mutating model assets, or mutating
regression baselines.

### Notes

This milestone adds:

- `apps.worker.services.gameplay_gated_pipeline_routing`
- `export-gameplay-gated-routing-contract` worker CLI command
- `build-gameplay-gated-routing-plan` worker CLI command
- `validate-gameplay-gated-routing-plan` worker CLI command
- `build-gameplay-gated-routing-report` worker CLI command
- `tom-v1-export-gameplay-gated-routing-contract` Make helper
- `tom-v1-build-gameplay-gated-routing-plan` Make helper
- `tom-v1-validate-gameplay-gated-routing-plan` Make helper
- `tom-v1-build-gameplay-gated-routing-report` Make helper
- `.data/contracts/gameplay_gated_pipeline_routing_contract_v1.json` tracked contract path
- `.data/exports/gameplay_gated_routing_plan.current.json` local plan path
- `.data/exports/gameplay_gated_routing_plan.validation.json` local validation path
- `.data/exports/gameplay_gated_routing_report.current.json` local report path
- `docs/blueprints/blueprint_39_gameplay_gated_evidence_pipeline_routing_v1.md`
- `docs/reviews/gameplay_gated_evidence_pipeline_routing_v1.md`
- `docs/agent_reports/blueprint_39_gameplay_gated_evidence_pipeline_routing_v1_report.md`

The contract defines routing scope, source contract refs, gameplay gate refs, routing plan schema,
downstream stage schema, skip reasons, override policy, validation rules, provenance
requirements, and warnings. The plan builder reads Blueprint 38 gameplay segment candidates and
emits allowed, blocked, and review-required windows plus routing entries for downstream stages.
The validator checks contract shape, plan shape, allowed routing modes, allowed decisions, skip
reasons, override statuses, referenced gameplay segment gate contract version, and forbidden
fields/values. The report summarizes structural routing output only. Blueprint 39 does not run
detections, tracklets, pose, court, event, 3D, replay, or corpus jobs; it does not create labels,
training truth, gameplay truth, line-call conclusions, scoring, player identity, production
readiness claims, or adjudication.

## Blueprint 40 Gameplay-Gated Perception Execution Hook v1

Status: complete

### Goal

Turn Blueprint 39 routing plans into perception-stage execution constraints without running heavy
perception inference by default, creating tennis truth, mutating model assets, or mutating
regression baselines.

### Notes

This milestone adds:

- `apps.worker.services.gameplay_gated_perception_execution`
- `export-gameplay-gated-perception-execution-contract` worker CLI command
- `build-gameplay-gated-perception-execution-plan` worker CLI command
- `validate-gameplay-gated-perception-execution-plan` worker CLI command
- `build-gameplay-gated-perception-execution-report` worker CLI command
- `tom-v1-export-gameplay-gated-perception-execution-contract` Make helper
- `tom-v1-build-gameplay-gated-perception-execution-plan` Make helper
- `tom-v1-validate-gameplay-gated-perception-execution-plan` Make helper
- `tom-v1-build-gameplay-gated-perception-execution-report` Make helper
- `.data/contracts/gameplay_gated_perception_execution_contract_v1.json` tracked contract path
- `.data/exports/gameplay_gated_perception_execution_plan.current.json` local plan path
- `.data/exports/gameplay_gated_perception_execution_plan.validation.json` local validation path
- `.data/exports/gameplay_gated_perception_execution_report.current.json` local report path
- `docs/blueprints/blueprint_40_gameplay_gated_perception_execution_hook_v1.md`
- `docs/reviews/gameplay_gated_perception_execution_hook_v1.md`
- `docs/agent_reports/blueprint_40_gameplay_gated_perception_execution_hook_v1_report.md`

The contract defines execution scope, source contract refs, routing plan contract refs, perception
stage schema, execution plan schema, skipped window schema, execution summary schema, validation
rules, provenance requirements, and warnings. The plan builder reads Blueprint 39 routing plans
and emits allowed execution windows, skipped windows, review-required windows, and execution
entries for perception stages. The validator checks contract shape, plan shape, allowed execution
modes, allowed decisions, skip reasons, provenance statuses, referenced routing plan/contract
versions, and forbidden fields/values. The report summarizes structural execution constraints
only. Blueprint 40 does not run detections, tracklets, pose, court, 3D, or GPU/model inference by
default; it does not write observations by default, create labels, training truth, gameplay truth,
line-call conclusions, scoring, player identity, production readiness claims, or adjudication.

## Blueprint 41 Gameplay Segment Replay Timeline / Operator Review v1

Status: complete

### Goal

Make gameplay segment candidates, gameplay-gated routing windows, and gameplay-gated perception
execution windows visible as replay-review timeline lanes without creating tennis truth, mutating
model assets, or mutating regression baselines.

### Notes

This milestone adds:

- `apps.worker.services.gameplay_segment_replay_review`
- `export-gameplay-segment-replay-review-contract` worker CLI command
- `build-gameplay-segment-replay-timeline` worker CLI command
- `validate-gameplay-segment-replay-timeline` worker CLI command
- `build-gameplay-segment-review-template` worker CLI command
- `validate-gameplay-segment-review-bundle` worker CLI command
- `build-gameplay-segment-review-report` worker CLI command
- `tom-v1-export-gameplay-segment-replay-review-contract` Make helper
- `tom-v1-build-gameplay-segment-replay-timeline` Make helper
- `tom-v1-validate-gameplay-segment-replay-timeline` Make helper
- `tom-v1-build-gameplay-segment-review-template` Make helper
- `tom-v1-validate-gameplay-segment-review-bundle` Make helper
- `tom-v1-build-gameplay-segment-review-report` Make helper
- `.data/contracts/gameplay_segment_replay_review_contract_v1.json` tracked contract path
- `.data/exports/gameplay_segment_replay_timeline.current.json` local timeline path
- `.data/exports/gameplay_segment_replay_timeline.validation.json` local validation path
- `.data/exports/gameplay_segment_review_template.current.json` local review template path
- `.data/exports/gameplay_segment_review_bundle.validation.json` local bundle validation path
- `.data/exports/gameplay_segment_review_report.current.json` local review report path
- `docs/blueprints/blueprint_41_gameplay_segment_replay_timeline_review_v1.md`
- `docs/reviews/gameplay_segment_replay_timeline_review_v1.md`
- `docs/agent_reports/blueprint_41_gameplay_segment_replay_timeline_review_v1_report.md`

The contract defines replay review scope, source contract refs, timeline lane schema, review
template schema, review bundle schema, validation rules, provenance requirements, and warnings.
The timeline builder reads Blueprint 38 candidate segments plus optional Blueprint 39 routing and
Blueprint 40 execution plans. The validator checks contract shape, timeline shape, allowed lane
types, allowed review statuses, provenance statuses, referenced source artifacts, and forbidden
fields/values. The review template records optional human metadata only. Blueprint 41 does not
run perception jobs, write observations, create labels, training truth, gameplay truth, line-call
conclusions, scoring, player identity, production readiness claims, or adjudication.

## Blueprint 42 Gameplay-Gated Many-Point Ingestion Smoke v1

Status: complete

### Goal

Create a safe end-to-end gameplay-gated many-point smoke workflow that starts from explicit media
entries and composes the Blueprint 33 and Blueprint 38-41 structural contracts without creating
truth, labels, inference side effects, model asset changes, or baseline changes.

### Notes

This milestone adds:

- `apps.worker.services.gameplay_gated_many_point_smoke`
- `export-gameplay-gated-many-point-smoke-contract` worker CLI command
- `build-gameplay-gated-many-point-smoke-manifest-template` worker CLI command
- `validate-gameplay-gated-many-point-smoke-manifest` worker CLI command
- `run-gameplay-gated-many-point-smoke` worker CLI command
- `build-gameplay-gated-many-point-smoke-report` worker CLI command
- `tom-v1-export-gameplay-gated-many-point-smoke-contract` Make helper
- `tom-v1-build-gameplay-gated-many-point-smoke-manifest-template` Make helper
- `tom-v1-validate-gameplay-gated-many-point-smoke-manifest` Make helper
- `tom-v1-run-gameplay-gated-many-point-smoke` Make helper
- `tom-v1-build-gameplay-gated-many-point-smoke-report` Make helper
- `.data/contracts/gameplay_gated_many_point_smoke_contract_v1.json` tracked contract path
- `.data/exports/gameplay_gated_many_point_smoke_manifest.template.json` local manifest path
- `.data/exports/gameplay_gated_many_point_smoke_manifest.validation.json` local validation path
- `.data/exports/gameplay_gated_many_point_smoke.current.json` local smoke output path
- `.data/exports/gameplay_gated_many_point_smoke_report.current.json` local report path
- `docs/blueprints/blueprint_42_gameplay_gated_many_point_ingestion_smoke_v1.md`
- `docs/reviews/gameplay_gated_many_point_ingestion_smoke_v1.md`
- `docs/agent_reports/blueprint_42_gameplay_gated_many_point_ingestion_smoke_v1_report.md`

The contract defines smoke scope, source contract refs, smoke manifest schema, smoke entry schema,
smoke report schema, validation rules, provenance requirements, and warnings. The smoke runner
reads an explicit manifest, runs the Blueprint 33 many-point ingestion gate in dry-run mode, and
then builds Blueprint 38 gameplay segment candidates, Blueprint 39 routing plans, Blueprint 40
execution plans, and Blueprint 41 replay timelines for each entry using safe structural defaults.
Blueprint 42 does not run GPU/model inference by default, write observations, mutate model assets,
mutate baselines, create labels, training truth, gameplay truth, line-call conclusions, scoring,
player identity, production readiness claims, or adjudication.

## Blueprint 54 Real Broadcast Gameplay Calibration Decision Phase Freeze v1

Status: complete

### Goal

Freeze the completed Blueprint 46 through Blueprint 53 real broadcast gameplay calibration
decision-support phase and record next-phase readiness without applying runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.real_broadcast_gameplay_calibration_decision_phase_freeze`
- `build-real-broadcast-gameplay-calibration-decision-phase-freeze` worker CLI command
- `validate-real-broadcast-gameplay-calibration-decision-phase-freeze` worker CLI command
- `build-real-broadcast-gameplay-calibration-next-phase-readiness-report` worker CLI command
- `tom-v1-build-real-broadcast-gameplay-calibration-decision-phase-freeze` Make helper
- `tom-v1-validate-real-broadcast-gameplay-calibration-decision-phase-freeze` Make helper
- `tom-v1-build-real-broadcast-gameplay-calibration-next-phase-readiness-report` Make helper
- `.data/contracts/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.json`
  tracked freeze artifact
- `.data/exports/real_broadcast_gameplay_calibration_decision_phase_freeze.validation.json`
  local validation path
- `.data/exports/real_broadcast_gameplay_calibration_next_phase_readiness_report.current.json`
  local readiness report path
- `docs/blueprints/blueprint_54_real_broadcast_gameplay_calibration_decision_phase_freeze_v1.md`
- `docs/reviews/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.md`
- `docs/agent_reports/blueprint_54_real_broadcast_gameplay_calibration_decision_phase_freeze_v1_report.md`

The phase freeze records completed phase blueprints, frozen contract refs, protected baseline refs,
required regression gates, capability summary, decision-support summary, manual approval summary,
non-claims, known limitations, validation summary, and Blueprint 55 as a future controlled
runtime-calibration change-request phase. Blueprint 54 does not apply threshold, smoothing, or
hysteresis changes; does not update runtime config; does not mutate model weights; does not replace
baselines; does not create production config; does not approve or reject candidates; and does not
claim tennis truth, classifier correctness, classifier accuracy, production readiness, or
generalization.

## Blueprint 60 Controlled Runtime Calibration Runtime Application Staging v1

Status: complete

### Goal

Create a controlled runtime application staging package for a future gameplay gate calibration
runtime application blueprint, without applying any runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_runtime_application_staging`
- ten worker CLI commands for contract export, inputs, input validation, staging build, staging
  validation, staged config delta build/validation, pre-apply manifest, staged rollback report, and
  staged post-application verification report
- matching `tom-v1-*controlled-runtime-calibration-runtime-application-staging*` Make helpers
- `.data/contracts/controlled_runtime_calibration_runtime_application_staging_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_runtime_application_staging_v1.json` tracked
  frozen staging artifact
- generated inputs, validations, staged config delta, pre-apply manifest, rollback, and
  verification report paths under `.data/exports/`
- `docs/blueprints/blueprint_60_controlled_runtime_calibration_runtime_application_staging_v1.md`
- `docs/reviews/controlled_runtime_calibration_runtime_application_staging_v1.md`
- `docs/agent_reports/blueprint_60_controlled_runtime_calibration_runtime_application_staging_v1_report.md`

The committed staging artifact records `staging_status: staging_blocked_unresolved_blockers`
because the BP59 source plan still carries unresolved blocker context and no selected candidate.
It preserves `runtime_application_status: staged_not_applied`, `mutation_status:
no_runtime_mutation`, `runtime_config_status: not_updated`, `production_config_status:
not_created`, `baseline_update_status: not_replaced`, `model_update_status: not_modified`, and
`future_blueprint_required_for_runtime_application: true`.

Blueprint 60 does not apply threshold, smoothing, or hysteresis changes; does not update runtime
config; does not mutate model weights; does not replace baselines; does not create production
config; does not approve or reject candidates; and does not perform runtime application.

## Blueprint 59 Controlled Runtime Calibration Application Plan v1

Status: complete

### Goal

Create the formal future application plan for controlled runtime calibration without applying
runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_application_plan`
- eight worker CLI commands for contract export, input build, input validation, plan build, plan
  validation, pre-application gate report build, rollback plan report build, and post-application
  verification plan build
- matching `tom-v1-*controlled-runtime-calibration-application-plan*` Make helpers
- `.data/contracts/controlled_runtime_calibration_application_plan_contract_v1.json` tracked
  contract
- `.data/contracts/controlled_runtime_calibration_application_plan_v1.json` tracked application
  plan
- generated inputs, validation, pre-application gate, rollback, and verification paths under
  `.data/exports/`
- `docs/blueprints/blueprint_59_controlled_runtime_calibration_application_plan_v1.md`
- `docs/reviews/controlled_runtime_calibration_application_plan_v1.md`
- `docs/agent_reports/blueprint_59_controlled_runtime_calibration_application_plan_v1_report.md`

Blueprint 59 application plans preserve `runtime_application_status: not_applied`,
`mutation_status: no_runtime_mutation`, `production_config_status: not_created`,
`baseline_update_status: not_replaced`, `model_update_status: not_modified`, and
`future_blueprint_required_for_runtime_application: true`. The current plan is
`application_plan_blocked_unresolved_blockers`, with rollback and post-application verification
plans defined for future use only. It does not apply threshold, smoothing, or hysteresis changes;
does not update runtime config; does not mutate model weights; does not replace baselines; does
not create production config; does not auto approve or auto reject candidates; and does not perform
runtime application.

## Blueprint 58 Controlled Runtime Calibration Human Approval Gate v1

Status: complete

### Goal

Create the formal human/operator approval gate for controlled runtime calibration without applying
runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_human_approval_gate`
- seven worker CLI commands for contract export, input build, input validation, gate build, gate
  validation, human approval summary build, and future application readiness report build
- matching `tom-v1-*controlled-runtime-calibration-human-approval*` Make helpers
- `.data/contracts/controlled_runtime_calibration_human_approval_gate_contract_v1.json` tracked
  contract
- `.data/contracts/controlled_runtime_calibration_human_approval_gate_v1.json` tracked approval
  gate
- generated inputs, validation, summary, and future-readiness report paths under `.data/exports/`
- `docs/blueprints/blueprint_58_controlled_runtime_calibration_human_approval_gate_v1.md`
- `docs/reviews/controlled_runtime_calibration_human_approval_gate_v1.md`
- `docs/agent_reports/blueprint_58_controlled_runtime_calibration_human_approval_gate_v1_report.md`

Blueprint 58 approval gates preserve `runtime_application_status: not_applied`,
`mutation_status: no_runtime_mutation`, `production_config_status: not_created`,
`baseline_update_status: not_replaced`, `model_update_status: not_modified`,
`human_operator_signoff_required: true`, and
`future_blueprint_required_for_runtime_application: true`. The current gate is
`approval_gate_blocked_unresolved_blockers` because the BP57 source review packet still carries
unresolved blocker context. It does not apply threshold, smoothing, or hysteresis changes; does not
update runtime config; does not mutate model weights; does not replace baselines; does not create
production config; does not auto approve or auto reject candidates; and does not claim tennis truth,
classifier correctness, classifier accuracy, production readiness, or generalization.

## Blueprint 57 Controlled Runtime Calibration Dry-Run Review Packet v1

Status: complete

### Goal

Package Blueprint 56 controlled dry-run execution reports into a human-operator review packet before
any future runtime calibration request.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_dry_run_review_packet`
- seven worker CLI commands for contract export, input build, input validation, packet build,
  packet validation, summary build, and operator checklist build
- matching `tom-v1-*controlled-runtime-calibration-dry-run-review*` Make helpers
- `.data/contracts/controlled_runtime_calibration_dry_run_review_packet_contract_v1.json` tracked
  contract
- `.data/contracts/controlled_runtime_calibration_dry_run_review_packet_v1.json` tracked review
  packet
- generated inputs, validation, summary, and operator checklist paths under `.data/exports/`
- `docs/blueprints/blueprint_57_controlled_runtime_calibration_dry_run_review_packet_v1.md`
- `docs/reviews/controlled_runtime_calibration_dry_run_review_packet_v1.md`
- `docs/agent_reports/blueprint_57_controlled_runtime_calibration_dry_run_review_packet_v1_report.md`

Blueprint 57 review packets preserve `runtime_application_status: not_applied`, `mutation_status:
no_runtime_mutation`, `production_config_status: not_created`, `baseline_update_status:
not_replaced`, `model_update_status: not_modified`, `operator_review_required: true`, and
`future_blueprint_required_for_runtime_application: true`. The current packet is
`review_packet_informational_only` because no selected candidate is present in the dry-run context.
It does not apply threshold, smoothing, or hysteresis changes; does not update runtime config; does
not mutate model weights; does not replace baselines; does not create production config; does not
approve or reject candidates; and does not claim tennis truth, classifier correctness, classifier
accuracy, production readiness, or generalization.

## Blueprint 55 Controlled Runtime Calibration Change Request v1

Status: complete

### Goal

Create a controlled runtime calibration change-request mechanism for gameplay gate calibration
candidates without applying any runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_change_request`
- eight worker CLI commands for contract export, inputs, validation, request build, request
  validation, dry-run, dry-run validation, and report build
- matching `tom-v1-*controlled-runtime-calibration-change-request*` Make helpers
- `.data/contracts/controlled_runtime_calibration_change_request_contract_v1.json` tracked contract
- `.data/contracts/controlled_runtime_calibration_change_request_v1.json` tracked frozen request
- generated inputs, validation, dry-run, and report paths under `.data/exports/`
- `docs/blueprints/blueprint_55_controlled_runtime_calibration_change_request_v1.md`
- `docs/reviews/controlled_runtime_calibration_change_request_v1.md`
- `docs/agent_reports/blueprint_55_controlled_runtime_calibration_change_request_v1_report.md`

The committed request records `candidate_config_status: no_candidate_selected`, so its request
status is `informational_only`. Blueprint 55 requires human approval, dry-run planning, rollback
planning, and regression gates, while leaving runtime state `not_applied`.

## Blueprint 56 Controlled Runtime Calibration Dry-Run Execution v1

Status: complete

### Goal

Execute Blueprint 55 controlled runtime calibration change requests in dry-run mode only without
applying runtime calibration.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_dry_run_execution`
- seven worker CLI commands for contract export, inputs, input validation, dry-run execution,
  report validation, summary build, and rollback readiness report build
- matching `tom-v1-*controlled-runtime-calibration-dry-run*` Make helpers
- `.data/contracts/controlled_runtime_calibration_dry_run_execution_contract_v1.json` tracked
  contract
- generated inputs, validation, execution report, summary, and rollback readiness report paths
  under `.data/exports/`
- `docs/blueprints/blueprint_56_controlled_runtime_calibration_dry_run_execution_v1.md`
- `docs/reviews/controlled_runtime_calibration_dry_run_execution_v1.md`
- `docs/agent_reports/blueprint_56_controlled_runtime_calibration_dry_run_execution_v1_report.md`

Blueprint 56 dry-run reports preserve `runtime_application_status: not_applied`, `mutation_status:
no_runtime_mutation`, `production_config_status: not_created`, `baseline_update_status:
not_replaced`, and `model_update_status: not_modified`. It does not apply threshold, smoothing, or
hysteresis changes; does not update runtime config; does not mutate model weights; does not replace
baselines; does not create production config; does not approve or reject candidates; and does not
claim tennis truth, classifier correctness, classifier accuracy, production readiness, or
generalization.

## Blueprint 62 Controlled Runtime Calibration Application Execution v1

Status: complete

### Goal

Create the first controlled runtime calibration application execution path, limited to an explicit
local runtime config artifact and protected by BP61 final-gate, rollback, readback, and post-apply
verification requirements.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_application_execution`
- worker CLI commands for contract export, input build/validation, controlled execution,
  validation, runtime readback, audit reporting, rollback package build, post-apply verification,
  and runtime config target creation
- matching `tom-v1-*controlled-runtime-calibration-application*` Make helpers
- tracked BP62 contract, execution artifact, explicit controlled runtime config target, and
  rollback package
- generated input, validation, runtime readback, audit, and post-apply verification outputs under
  `.data/exports/`
- focused tests for the blocked frozen path and successful passed-gate fixture path

The current frozen execution is blocked because the BP61 final gate is blocked. No staged delta is
applied to the committed runtime config target. The successful path is covered by tests and writes
only the explicit controlled runtime config artifact using atomic replace plus readback
verification.

## Blueprint 64 Controlled Runtime Calibration Application Execution Review Packet v1

Status: complete

### Goal

Package Blueprint 62 application execution results into a post-execution review packet without
performing runtime application.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_application_execution_review_packet`
- worker CLI commands for contract export, inputs, input validation, packet build, packet
  validation, summary, blocker report, operator checklist, and next-action report
- matching `tom-v1-*controlled-runtime-calibration-application-execution-review*` Make helpers
- `.data/contracts/controlled_runtime_calibration_application_execution_review_packet_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_application_execution_review_packet_v1.json`
  tracked review packet
- generated input, validation, summary, blocker, checklist, and next-action paths under
  `.data/exports/`
- focused tests for blocked execution review, controlled-application-shaped review, report
  generation, and forbidden runtime application terms

The committed review packet records the BP62 blocked execution as safe and unchanged:
`review_packet_created_for_blocked_execution`,
`application_blocked_safely_before_runtime_mutation`, matching runtime config target sha256 values,
and `resolve_operator_signoff_before_reapplying`.

## Blueprint 65 Controlled Runtime Calibration Blocked Execution Resolution Packet v1

Status: complete

### Goal

Package the BP64/BP62 blocked execution state into explicit resolution requirements without
creating operator signoff, selecting a candidate, rerunning the final gate, or performing runtime
application.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_blocked_execution_resolution_packet`
- worker CLI commands for contract export, inputs, input validation, packet build, packet
  validation, blocker checklist, operator action plan, candidate requirements, final-gate rerun
  plan, and reexecution readiness plan
- matching `tom-v1-*controlled-runtime-calibration-blocked-execution-resolution*` Make helpers
- `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_v1.json`
  tracked resolution packet
- generated input, validation, checklist, plan, and readiness paths under `.data/exports/`

The committed resolution packet records
`resolution_packet_created_for_blocked_execution`, `operator_signoff_required`,
`selected_candidate_required`, `final_gate_rerun_required`, and
`reexecution_not_ready_blockers_unresolved`.

## Blueprint 66 Controlled Runtime Calibration Operator Signoff Candidate Selection Packet v1

Status: complete

### Goal

Create the operator signoff and candidate selection packet mechanism required after BP65 while
leaving both requirements pending unless explicit refs are supplied.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_operator_signoff_candidate_selection_packet`
- worker CLI commands for contract export, inputs, input validation, packet build, packet
  validation, operator signoff requirements, candidate options, candidate validation, and
  resolution readiness
- matching `tom-v1-*controlled-runtime-calibration-operator-signoff-candidate-selection*` Make
  helpers
- `.data/contracts/controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_operator_signoff_candidate_selection_packet_v1.json`
  tracked packet
- generated input, validation, signoff requirements, candidate option, candidate validation, and
  readiness paths under `.data/exports/`
- focused tests for the pending default path and invalid explicit candidate rejection

The committed packet records
`packet_created_pending_operator_signoff_and_candidate_selection`, `operator_signoff_required`,
`selected_candidate_required`, `final_gate_rerun_required`,
`reexecution_not_ready_blockers_unresolved`, `runtime_config_changed: false`, and
`no_runtime_mutation_due_to_blocker`.

## Blueprint 67 Controlled Runtime Calibration Explicit Operator Signoff Artifact v1

Status: complete

### Goal

Create the explicit operator signoff artifact mechanism required after BP66 while leaving signoff
pending unless real operator input is supplied.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_explicit_operator_signoff_artifact`
- worker CLI commands for contract export, inputs, input validation, artifact build, artifact
  validation, operator signoff requirements report, operator attestation template, and operator
  signoff readiness report
- matching `tom-v1-*controlled-runtime-calibration-explicit-operator-signoff-artifact*` Make
  helpers
- `.data/contracts/controlled_runtime_calibration_explicit_operator_signoff_artifact_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_explicit_operator_signoff_artifact_v1.json`
  tracked artifact
- generated input, validation, requirements report, attestation template, and readiness report
  paths under `.data/exports/`
- focused tests for the pending default path and incomplete explicit signoff rejection

The committed artifact records
`signoff_artifact_created_pending_explicit_operator_input`, `operator_signoff_required`,
`operator_attestation_required`, `operator_identity_required`, `operator_timestamp_required`,
`selected_candidate_required`, `final_gate_rerun_required`,
`reexecution_not_ready_blockers_unresolved`, `runtime_application_status: not_executed`,
`runtime_config_changed: false`, and `no_runtime_mutation_due_to_blocker`.

## Blueprint 68 Controlled Runtime Calibration Explicit Selected Candidate Artifact v1

Status: complete

### Goal

Create the explicit selected candidate artifact mechanism required after BP67 while leaving the
selected candidate pending unless real operator selection input is supplied.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_explicit_selected_candidate_artifact`
- worker CLI commands for contract export, inputs, input validation, artifact build, artifact
  validation, candidate option inventory report, candidate selection requirements report, and
  selected candidate readiness report
- matching `tom-v1-*controlled-runtime-calibration-explicit-selected-candidate-artifact*` Make
  helpers
- `.data/contracts/controlled_runtime_calibration_explicit_selected_candidate_artifact_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_explicit_selected_candidate_artifact_v1.json`
  tracked artifact
- generated input, validation, inventory report, requirements report, and readiness report paths
  under `.data/exports/`
- focused tests for the pending default path and invalid explicit selected candidate rejection

The committed artifact records
`selected_candidate_artifact_created_pending_explicit_candidate_input`,
`selected_candidate_required`, `candidate_selection_pending_explicit_input`,
`operator_signoff_required`, `final_gate_rerun_required`,
`reexecution_not_ready_blockers_unresolved`, `runtime_application_status: not_executed`,
`runtime_config_changed: false`, and `no_runtime_mutation_due_to_blocker`.

## Blueprint 69 Controlled Runtime Calibration Human Resolution Input Packet v1

Status: complete

### Goal

Create the combined human resolution input packet required after BP68/BP67 while leaving human
resolution pending unless real operator signoff and selected candidate inputs are supplied.

### Notes

This milestone adds:

- `apps.worker.services.controlled_runtime_calibration_human_resolution_input_packet`
- worker CLI commands for contract export, inputs, input validation, packet build, packet
  validation, human resolution requirements report, input template, readiness report, and
  final-gate rerun prerequisite report
- matching `tom-v1-*controlled-runtime-calibration-human-resolution*` Make helpers
- `.data/contracts/controlled_runtime_calibration_human_resolution_input_packet_contract_v1.json`
  tracked contract
- `.data/contracts/controlled_runtime_calibration_human_resolution_input_packet_v1.json` tracked
  packet
- generated input, validation, requirements report, input template, readiness report, and
  final-gate rerun prerequisite report paths under `.data/exports/`
- focused tests for the pending default path, report/template generation, and invalid explicit
  human-resolution input rejection

The committed packet records `human_resolution_input_required`, `operator_signoff_required`,
`operator_attestation_required`, `operator_identity_required`, `operator_timestamp_required`,
`selected_candidate_required`, `candidate_selection_pending_explicit_input`,
`final_gate_rerun_required`, `reexecution_not_ready_blockers_unresolved`,
`runtime_application_status: not_executed`, `runtime_config_changed: false`, and
`no_runtime_mutation_due_to_blocker`.
