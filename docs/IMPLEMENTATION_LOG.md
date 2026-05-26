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
