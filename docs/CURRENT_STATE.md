# TOM v3 Simple - Current State

## Project

- Project name: TOM v3 Simple
- Repo: drussie/tom-v3-simple
- Current phase: Blueprint 4 in progress
- Current goal: Prepare pose observation persistence and lineage while preserving the TOM v3 observation-only runtime contract

## Mission

A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Implementation Status

- Implementation status: persisted ball/player observations can be inspected visually, grouped into candidate tracklets, and complemented by first-class pose schema and normalization foundations
- Model integration status: fixture gameplay and fixture detection adapters implemented for deterministic dev/test output
- TOM v1 gameplay detector: known asset, portable source/assets not available in this repo/environment; integration stub documented
- YOLO/YOLO26: optional runtime probe, model weights registration, YOLO-like output normalization, frame-level inference persistence bridge, and local real-YOLO smoke helper implemented; runtime/assets are not required in the base environment
- Database: initial SQLAlchemy models and Alembic migration implemented
- API: FastAPI backend foundation implemented
- Media indexing: implemented for local files via ffprobe, sha256 checksum, local storage copy/register mode, and frame/time summary
- Gameplay adapter: implemented with `BaseGameplayAdapter`, fixture adapter, TOM v1 unavailable stub, worker service, and worker CLI
- Detection adapter: implemented with `BaseDetectionAdapter`, fixture adapter, guarded YOLO frame inference path, worker service, and worker CLI
- Tracklet builder: implemented with deterministic candidate grouping, first-class track observations, track point observations, and lineage from persisted detections
- Tracklet evidence bundle: implemented as a dynamic API/viewer path for cross-run tracklet evidence inspection
- Tracklet query/review: implemented with structured query filters, annotation summaries, and viewer review controls
- Tracklet review dataset export: implemented with JSON export artifacts, evidence artifact metadata, optional query result memory, API endpoint, and worker CLI
- Blueprint 2 status: complete; temporal evidence can be built, inspected, queried, reviewed, and exported as candidate evidence
- Blueprint 3 status: complete; optional YOLO runtime environment boundary, dependency probe, device resolver, weights validation, class mapping, model registry helper, YOLO output normalization, frame-level persistence bridge, local real-YOLO smoke workflow, completion review, and invariant audit are implemented
- Blueprint 4 status: in progress; pose observation schema, COCO17 skeleton registry, keypoint validation, typed pose persistence, synthetic pose insertion, pose normalization, and pose runtime/config metadata contracts are implemented
- Observation writer: implemented with typed extension rows, lineage, artifacts, and idempotency
- Worker synthetic seeder: implemented
- Visual evidence viewer: implemented in `apps/web` with detection bbox overlay and frame artifact image support
- Pose observation foundation: implemented with a typed `pose_observation` table, COCO17 skeleton registry, keypoint summary statistics, fake/serialized pose output normalization, crop projection, and synthetic/fake pose observation insertion; no real pose inference or pose overlay viewer exists yet
- Synthetic data: baseline scenario creates viewer-ready observations, tracklets, gaps, candidates, lineage, and artifacts
- Local setup: documented with `.env.example`, Makefile, and dev runbooks
- Branch/default branch: `main` is restored as the GitHub default branch

## Milestone 0A Result

Status: complete

Milestone 0A establishes the repo documentation spine, architecture contracts, observation-store schema direction, milestone docs, handoff memory, agent report, and placeholder project skeleton.

## Milestone 0B Result

Status: complete

Milestone 0B establishes the FastAPI backend foundation, database models, initial Alembic migration, Pydantic schema contracts, central observation writer, query/detail/lineage/artifact/annotation APIs, dev-only synthetic persistence path, and backend tests.

## Milestone 0C Result

Status: complete

Milestone 0C establishes the worker CLI, reusable rich synthetic seeding pipeline, baseline tennis scenario, explicit missingness/coverage metadata, homography placeholders, derived candidates, lineage, artifact metadata, verification helper, and worker tests.

## Milestone 0D Result

Status: complete

Milestone 0D establishes the first visual evidence viewer foundation in `apps/web`, a thin viewer run API in `GET /viewer/runs/{run_id}`, timeline rows for view state, track coverage, homography availability, candidate markers, detail/lineage/artifact panels, and frontend build validation.

## Milestone 0E Result

Status: complete

Milestone 0E consolidates Milestone 0 with local setup docs, a local demo runbook, `.env.example`, Makefile commands, a synthetic viewer smoke script, integration smoke test coverage, updated project memory, and branch/default-branch cleanup guidance.

## Milestone 1A Result

Status: complete

Milestone 1A establishes real local media registration and indexing with ffprobe metadata extraction, sha256 checksums, local storage copy/register modes, frame/time mapping utilities, `POST /media/register-file`, worker `index-media`, tests, and media indexing docs.

## Milestone 1B Result

Status: complete

Milestone 1B establishes the gameplay adapter interface, TOM v1 portability assessment, fixture gameplay adapter, TOM v1 unavailable stub, worker `run-gameplay-adapter`, worker `index-and-run-gameplay`, persisted gameplay observations through `ObservationWriter`, and viewer-compatible gameplay bands.

## Milestone 1C Result

Status: complete

Milestone 1C establishes the detection adapter interface, YOLO26 portability assessment, fixture detection adapter, YOLO unavailable stub, worker `run-detection-adapter`, worker `index-and-run-detection`, persisted ball/player atomic observations through `ObservationWriter`, optional scoped lineage to gameplay observations, and query/viewer-compatible detection evidence.

## Milestone 1D Result

Status: complete

Milestone 1D establishes the detection overlay viewer transform, coordinate-space bbox overlay components, selected frame behavior, selected detection highlighting, detection timeline row, safe empty states for missing media dimensions or bbox payloads, and docs/tests for the overlay contract.

## Milestone 1E Result

Status: complete

Milestone 1E establishes ffmpeg-based frame extraction, worker `extract-frame-artifacts`, local `.data/artifacts` storage, persisted `frame_image` and `detection_frame_image` artifact metadata, a local artifact content route, and viewer support for displaying extracted frame imagery behind persisted detection bboxes.

## Milestone 1F Result

Status: complete

Milestone 1F establishes a deterministic tracklet builder that consumes persisted detection observations, creates a new tracklet-builder processing run, persists candidate `tracklet` and `track_point` rows, links track points back to source detection observations, and exposes tracklet evidence through the existing viewer/query paths.

## Milestone 2A Result

Status: complete

Milestone 2A repairs the tracklet persistence contract on the existing 1F branch. Tracklet candidates and track point candidates now have their own observation spine rows, `tracklet.observation_id` and `track_point.observation_id` point to those track observations, and source detections are connected with `tracked_from` and `grouped_from` `observation_lineage` rows.

## Milestone 2B Result

Status: complete

Milestone 2B adds a dynamic `GET /tracklets/{tracklet_id}/evidence-bundle` endpoint and viewer panel that connect a tracklet candidate to track point candidates, source detection observations, matched frame artifacts, lineage rows, and run/config/model metadata across the tracklet builder and source detection runs.

## Milestone 2C Result

Status: complete

Milestone 2C adds structured `POST /tracklets/query`, review annotation summaries in evidence bundles, and viewer controls for adding review annotations to tracklet candidate observations, track point candidate observations, and source detection observations without mutating the underlying evidence.

## Milestone 2D Result

Status: complete

Milestone 2D adds `POST /tracklets/export-review-dataset`, worker `export-tracklet-review-dataset`, JSON review dataset artifacts under `.data/exports`, persisted `tracklet_review_dataset_export` artifact metadata, optional query result rows for query-based exports, and docs/tests for packaging candidate tracklet evidence without mutating observations.

## Milestone 2E Result

Status: complete

Milestone 2E closes Blueprint 2 with a completion review, invariant audit, naming transition documentation, runbook cleanup, and validation pass. Blueprint 2 is now complete: persisted detections can become candidate tracklets with source lineage, multi-run evidence bundles, structured query, review annotations, and review dataset exports.

## Milestone 3A Result

Status: complete

Milestone 3A starts Blueprint 3 with an optional YOLO runtime environment path. The base `tom_v3` environment stays lightweight; `requirements-yolo.txt`, `probe_yolo_runtime`, `resolve_yolo_device`, clear unavailable diagnostics, worker `yolo-runtime-probe`, model weights ignore rules, tests, and docs prepare for future real YOLO observation adapters without persisting real YOLO detections yet.

## Milestone 3B Result

Status: complete

Milestone 3B adds YOLO model weights validation, safe local root checks, sha256 and file-size fingerprinting, default ball/player class mapping validation, optional model metadata probing, model registry registration/reuse, and worker `register-yolo-model`. It registers model asset metadata only; it does not run inference, create processing runs, or persist YOLO detections.

## Milestone 3C Result

Status: complete

Milestone 3C adds YOLO-like output normalization. Serialized/fake frame results with `xyxy`, confidence, class id/name, and frame/time values can be normalized into TOM v3-compatible `ball_detection` and `player_detection` payloads. It includes class-map matching by name/id, bbox/center conversion, unmapped/invalid input accounting, and YOLO adapter skeleton normalization methods. It does not run real inference or persist YOLO detections.

## Milestone 3D Result

Status: complete

Milestone 3D connects frame-level YOLO-style outputs to persisted TOM v3 observations. It adds a YOLO frame inference provider interface, fake provider for tests, guarded Ultralytics provider, media-owned frame sampling, registered model metadata/weights validation for YOLO runs, worker `run-detection-adapter --adapter yolo --model-registry-id ...`, and mocked YOLO persistence tests proving `ball_detection` / `player_detection` atomic observations remain viewer/query compatible. Real local runtime smoke remains optional and depends on local YOLO packages and weights.

## Milestone 3E Result

Status: complete

Milestone 3E adds the local real-YOLO smoke and viewer validation foundation. It adds worker `smoke-real-yolo-local`, `scripts/smoke_real_yolo_local.py`, plan-only mode, structured skip behavior for missing runtime/weights/media, docs for runtime probe, weights registration, media indexing, YOLO detection runs, frame artifacts, viewer overlay inspection, and optional tracklet/evidence-bundle compatibility. The default suite still runs without real YOLO dependencies or weights.

## Milestone 3F Result

Status: complete

Milestone 3F closes Blueprint 3 with a completion review, invariant audit, runbook cleanup, documentation/index updates, and validation pass. Blueprint 3 is now complete: TOM v3 can safely keep YOLO runtime optional, validate/register local model weights, normalize YOLO-like outputs, persist YOLO-origin atomic ball/player detections through the existing detection pipeline, inspect them through the existing viewer/frame artifact path, and feed the existing Blueprint 2 tracklet/review/export flow without adding tracking mode, pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 4A Result

Status: complete

Milestone 4A starts Blueprint 4 with a pose runtime/schema foundation. TOM v3 now has a first-class `pose_observation` typed table, COCO17 skeleton registry, keypoint schema validation helpers, pose schema models, fixture pose model/runtime metadata, and a synthetic pose insertion helper that writes observation spine rows plus typed pose rows using media-owned frame/time. It does not add real pose inference, a pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 4B Result

Status: complete

Milestone 4B adds pose adapter normalization. Fake or serialized pose frame results can now be normalized into `PoseObservationCreate`-compatible payloads using COCO17 names/indices from the skeleton registry. The normalizer preserves missing keypoints, computes summary statistics, converts bbox context, projects crop-local keypoints to full-frame coordinates, passes through subject association candidate fields, and returns a pose adapter result with normalization-only diagnostics. It does not add real pose inference, a pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Naming Transition

The implementation branch/file names may reference "1F" because the milestone was originally planned as a Blueprint 1 extension. After Blueprint 1 was declared complete, the same work was reclassified as Blueprint 2A because temporal grouping begins a new conceptual layer.

## Next Milestone

Recommended next milestone: Milestone 4C - Pose Observation Persistence and Lineage.
