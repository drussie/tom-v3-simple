# TOM v3 Simple - Implementation Log

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
