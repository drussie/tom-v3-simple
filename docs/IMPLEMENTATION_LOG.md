# TOM v3 Simple - Implementation Log

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
