# TOM v3 Simple - Current State

## Project

- Project name: TOM v3 Simple
- Repo: drussie/tom-v3-simple
- Current phase: Blueprint 39 complete; gameplay-gated downstream routing plans added
- Current goal: Preserve the BP22-BP36 structural expansion freeze, keep protected regression
  gates intact, and route future downstream evidence workflows through Blueprint 38 gameplay
  segment candidate windows without executing heavy inference by default

## Mission

A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation, including gameplay/non-gameplay state, and makes the evidence queryable and visually replayable without deciding official tennis meaning.

## Implementation Status

- Implementation status: complete lightweight local observation/evidence platform with persisted ball/player observations, candidate tracklets, pose schema/normalization/persistence/lineage/viewer/query/review/export foundations, canonical fixture demo, coherent evidence/candidate viewer, TOM-native exports, structural provenance audit, canonical docs, and final completion review
- Model integration status: fixture gameplay and fixture detection adapters implemented for deterministic dev/test output
- TOM v1 gameplay detector: local `model_assets/tom_v1/view_classifier_gameplay.pt` asset is
  inspected/hashed by the Blueprint 38 gameplay segment gate; candidate segment exports remain
  evidence-only and do not create tennis truth
- YOLO/YOLO26: optional runtime probe, model weights registration, YOLO-like output normalization, frame-level inference persistence bridge, and local real-YOLO smoke helper implemented; runtime/assets are not required in the base environment
- TOM v1 model assets bridge: local-only guardrails, TOM v1 model inventory, Makefile helpers, and runbook commands added for optional ball detection, player detection, real-detection-derived tracklets, pose smoke, and Blueprint 38 gameplay segment gate provenance through existing TOM v3 commands
- Database: initial SQLAlchemy models and Alembic migration implemented
- API: FastAPI backend foundation implemented
- Media indexing: implemented for local files via ffprobe, sha256 checksum, local storage copy/register mode, and frame/time summary
- Gameplay adapter: implemented with `BaseGameplayAdapter`, fixture adapter, TOM v1 unavailable stub, worker service, and worker CLI
- Detection adapter: implemented with `BaseDetectionAdapter`, fixture adapter, guarded YOLO frame inference path, worker service, worker CLI, and `run-real-detection` replay command for optional real YOLO output
- Tracklet builder: implemented with deterministic candidate grouping, first-class track observations, track point observations, and lineage from persisted detections
- Tracklet evidence bundle: implemented as a dynamic API/viewer path for cross-run tracklet evidence inspection
- Tracklet query/review: implemented with structured query filters, annotation summaries, and viewer review controls
- Tracklet review dataset export: implemented with JSON export artifacts, evidence artifact metadata, optional query result memory, API endpoint, and worker CLI
- Blueprint 2 status: complete; temporal evidence can be built, inspected, queried, reviewed, and exported as candidate evidence
- Blueprint 3 status: complete; optional YOLO runtime environment boundary, dependency probe, device resolver, weights validation, class mapping, model registry helper, YOLO output normalization, frame-level persistence bridge, local real-YOLO smoke workflow, completion review, and invariant audit are implemented
- Blueprint 4 status: complete; pose observation schema, COCO17 skeleton registry, keypoint validation, typed pose persistence, synthetic pose insertion, pose normalization, worker pose persistence, source detection lineage, pose overlay viewer, pose query/review/export integration, completion review, and pose runtime/config metadata contracts are implemented
- Blueprint 5 status: complete; local demo, viewer polish, provenance audit, docs/control-room consolidation, and final completion review are complete
- Blueprint 6 status: complete; video replay timeline foundation, replay info, local video serving, frame/time mapping, frontend replay route, synchronized detection observation overlay playback, tracklet candidate overlay playback, pose keypoint overlay playback, evidence timeline lanes, Stream Proxy Mode, and completion review are complete
- Blueprint 7 status: complete; optional real YOLO detection replay, real-vs-fixture labeling, candidate tracklets from real detection observations, optional real pose keypoint observations, court/camera/homography deferral, and final perception orchestration closeout are complete
- Blueprint 37 status: complete; tracked expansion completion freeze manifest, validator, and next-phase readiness report are implemented without creating new evidence, labels, tennis conclusions, or adjudication
- Blueprint 38 status: complete; tracked gameplay segment gate contract, classifier asset inspection,
  candidate segment export, validation, report, and replay timeline artifact are implemented
  without downstream perception execution, truth labels, scoring, player identity, or adjudication
- Blueprint 39 status: complete; tracked gameplay-gated routing contract, routing plan,
  validation, report, and replay timeline artifact are implemented without downstream evidence
  execution, truth labels, scoring, player identity, or adjudication
- Observation writer: implemented with typed extension rows, lineage, artifacts, and idempotency
- Worker synthetic seeder: implemented
- Visual evidence viewer: implemented in `apps/web` with detection bbox overlay, pose keypoint/skeleton overlay, frame artifact image support, run evidence summary, clearer empty states, candidate/evidence wording, readable lineage context, and review/export metadata display
- Replay workstation: Milestones 6A/6B/6C/6D/6E/6F implemented `/replay/<media_id>` with indexed local video playback, current timestamp/frame display, selected run context, persisted detection overlay chunks, candidate tracklet overlays, pose keypoint/skeleton overlays, layer toggles, run selectors, evidence timeline lanes, click-to-seek/select evidence details, Stream Proxy Mode for video-as-live review, and Blueprint 6 closeout docs; Milestones 7A/7B/7C/7D make real detection runs, real-detection-derived tracklet runs, and real pose runs compatible and source-labeled through `detectionRunId`, `trackletRunId`, and `poseRunId`; Milestones 8E/8F add court keypoint, court line, camera/view, homography candidate, and projection diagnostic replay layers through `courtRunId`, `homographyRunId`, and `projectionDiagnosticRunId`
- Pose observation foundation: implemented with a typed `pose_observation` table, COCO17 skeleton registry, keypoint summary statistics, fake/serialized pose output normalization, crop projection, worker fixture pose persistence, optional real pose replay persistence, source detection candidate lineage, pose overlay viewer, pose-specific query filters, review annotations, and TOM-native review dataset export; pose observations remain keypoint evidence only
- Court/homography evidence: Blueprint 8 has started; Milestone 8A adds typed schema contracts, storage models, migration, court template registry, writer persistence support, and fake persistence tests; Milestone 8B adds fixture court keypoint, court line, and camera/view evidence persistence; Milestone 8C adds camera/view query, summary, bundle, and `/court/camera-view` API read models; Milestone 8D adds homography candidate persistence with source court evidence lineage; Milestone 8E adds replay overlays for persisted court keypoints, court lines, camera/view evidence, and homography candidates; Milestone 8F adds projection diagnostic persistence, replay payload/detail support, and court review export, but no real camera/court inference or ball/player court-space projection exists yet
- Local TOM v1 asset policy: model files under `model_assets/tom_v1/` remain ignored local assets; `best_ball_v2_1280.pt`, `yolo26x.pt`, `yolo26n.pt`, and `yolo26s.pt` are candidate inputs for existing real detection smoke; `yolo26x-pose.pt` is a candidate input for existing real pose smoke; `view_classifier_gameplay.pt` is inspected/hashed by the Blueprint 38 gameplay segment gate; `keypoints_model.pth` still requires a future TOM v1-specific adapter
- Local fixture demo: implemented with worker `run-demo`, Makefile `demo` targets, deterministic media fallback, fixture gameplay/detection/tracklet/pose path, seeded review annotations, pose and tracklet review exports, summary IDs/counts/viewer URLs, and canonical `docs/RUNBOOK_LOCAL.md`
- Viewer product polish: implemented with shared frontend evidence copy helpers, run evidence summary, detection/tracklet/pose/detail panel wording cleanup, lineage relationship descriptions, artifact/export metadata display, annotation/keypoint metadata display, and viewer payload regression coverage
- Completion/provenance audit: implemented with worker `completion-audit`, Makefile `completion-audit`, PASS/WARN/FAIL JSON, demo completeness checks, media/run/step/observation/typed-row/lineage/artifact/annotation/export integrity checks, and tests proving the audit passes after `make demo`
- Docs/control-room consolidation: implemented with concise canonical docs for repo memory, architecture, observation contracts, blueprint status, known limitations, optional YOLO, exports, and final completion checklists
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

## Milestone 4C Result

Status: complete

Milestone 4C adds pose observation persistence and lineage. The worker `run-pose-adapter` command creates a pose processing run and step, normalizes fixture pose output, persists first-class `pose` observation spine rows plus typed `pose_observation` rows through `ObservationWriter`, and writes `pose_from_subject_detection_candidate` lineage when linked to source `player_detection` observations. It does not add real pose inference, a pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 4D Result

Status: complete

Milestone 4D adds pose overlay support to the existing Evidence Viewer. Viewer run payloads now include typed pose detail, the frontend renders persisted COCO17 keypoints and skeleton edges from image-pixel coordinates, missing keypoints remain visible as missing evidence in the keypoint table, selected pose metadata is inspectable, and source association candidate context is displayed when present. It does not add real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 4E Result

Status: complete

Milestone 4E adds pose query, review, and export integration. Pose observations can now be searched with pose-specific filters, assembled into evidence bundles, annotated through the generic human annotation path with keypoint-level metadata, and exported as TOM-native JSON review dataset artifacts with checksums, evidence artifact metadata, and query result memory. It does not add real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 4F Result

Status: complete

Milestone 4F closes Blueprint 4 with a completion review, invariant audit, runbook cleanup, documentation/index updates, and validation pass. Blueprint 4 is now complete: TOM v3 can persist pose model output as observation evidence using a first-class pose schema, COCO17 skeleton registry, keypoint validation, normalization, processing-run persistence, source-evidence lineage, viewer overlay, pose-specific query filters, review annotation support, evidence bundles, and TOM-native review dataset export. It does not add real pose inference, movement interpretation, stroke classification, serve/hit/split-step/biomechanics analysis, homography, bounce, hit, rally, point, scoring, or adjudication.

## Milestone 5A Result

Status: complete

Milestone 5A starts Blueprint 5 with a canonical local fixture demo and runbook. TOM v3 Simple now has `make demo` and worker `run-demo` paths that index media, run fixture gameplay and detection adapters, extract frame artifacts, build candidate tracklets, run fixture pose observations, seed review annotations, export pose and tracklet review datasets, and print a summary with IDs, counts, export paths, warnings, and viewer URLs. The default path does not require YOLO weights, real pose weights, GPU runtime, or network access. Fixture output remains demo evidence only and does not add movement interpretation, tennis-event inference, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5B Result

Status: complete

Milestone 5B polishes the viewer and product surface for the local demo path. The Evidence Viewer now includes a run evidence summary, clearer empty states, consistent observation/evidence/candidate wording, readable lineage relationship descriptions, improved artifact and review export metadata display, and annotation rows that expose notes, review-only flags, demo-seeded flags, and keypoint-level metadata when present. It does not add new model/runtime capability, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5C Result

Status: complete

Milestone 5C adds a final structural provenance audit for the local fixture demo path. TOM v3 Simple now has `run_completion_audit`, worker `completion-audit`, Makefile `completion-audit`, strict/non-strict modes, demo-only/all-data scopes, PASS/WARN/FAIL JSON, and focused tests covering successful demo audit plus broken media/run, typed-row, lineage, artifact, and annotation references. The audit checks evidence structure and provenance integrity only; it does not add model/runtime capability, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5D Result

Status: complete.

Milestone 5D consolidates repo memory into a concise canonical documentation set. The README now points to `docs/RUNBOOK_LOCAL.md`, `docs/CONTROL_ROOM.md`, `docs/ARCHITECTURE.md`, `docs/OBSERVATION_CONTRACT.md`, `docs/BLUEPRINT_STATUS.md`, `docs/KNOWN_LIMITATIONS.md`, `docs/OPTIONAL_YOLO.md`, `docs/EXPORTS.md`, `docs/PROVENANCE_AUDIT.md`, and `docs/COMPLETION_CHECKLIST.md`. Older milestone docs remain accessible as history, while the canonical docs describe the current product state, local demo path, optional YOLO boundary, evidence/export contracts, limitations, and final completion checklist without adding new product capability.

## Milestone 5E Result

Status: complete.

Milestone 5E closes TOM v3 Simple with a final completion review, final agent report, final status updates, and final validation pass. TOM v3 Simple is complete as a lightweight local observation/evidence platform that can index media, run fixture gameplay/detection/pose paths, optionally smoke-test YOLO detection when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit. It does not add real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, production deployment, auth, real stream ingestion, or adjudication.

## Milestone 6A Result

Status: complete.

Milestone 6A starts Blueprint 6 with a video replay timeline foundation. TOM now exposes replay info for indexed media, serves local indexed media files to the browser, maps playback time to TOM media-owned frame/time, and provides a `/replay/<media_id>` workstation route with an HTML video player, timestamp/frame telemetry, a timeline shell, selected run context, and an overlay placeholder for future evidence layers. It does not add detection/tracklet/pose overlay playback, live stream ingestion, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 6B Result

Status: complete.

Milestone 6B adds detection overlay playback to the replay workstation. TOM now exposes `GET /replay/overlays` for media/time-window detection chunks, normalizes persisted `ball_detection` and `player_detection` observations into image-pixel bbox overlay payloads, and renders those boxes over `/replay/<media_id>` with detection layer controls, detection run selection, loaded-chunk timeline ticks, and click-to-select observation detail. It does not add tracklet/pose overlay playback, live stream ingestion, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 6C Result

Status: complete.

Milestone 6C adds tracklet candidate and pose keypoint overlay playback to the replay workstation. `GET /replay/overlays` now supports tracklet and pose layers, run filtering, persisted candidate track points/paths, persisted pose keypoints/skeleton edges, and click-to-select evidence details for detections, tracklets, track points, and pose observations. It does not add full evidence timeline lanes, stream ingestion, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 6D Result

Status: complete.

Milestone 6D adds timeline lanes and evidence scrubbing to the replay workstation. `GET /replay/timeline` now returns detection observation ticks, tracklet candidate spans, pose observation ticks, and review annotation markers for selected media/run context. The replay page renders evidence lanes with a current playhead, and clicking lane items seeks video playback and selects persisted evidence detail. It does not add stream proxy mode, live ingestion, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 6E Result

Status: complete.

Milestone 6E adds Stream Proxy Mode to the replay workstation. `/replay/<media_id>?mode=stream_proxy` treats the indexed local video as a live-like source, starts at t=0, advances a live edge with playback, hides future overlay and timeline evidence until available, displays available evidence counts and pause/review state, and can return the operator to the current live-like edge. It does not add real live ingestion, streaming protocols, websocket updates, model scheduling, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 6F Result

Status: complete.

Milestone 6F closes Blueprint 6 with a completion review, final agent report, final status updates, and final validation pass. Blueprint 6 is complete: TOM v3 can open indexed video in Replay Mode or Stream Proxy Mode, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, support click-to-seek/select persisted evidence, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it. It does not add real live ingestion, streaming protocols, websocket updates, model scheduling, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 7A Result

Status: complete.

Milestone 7A starts Blueprint 7 with optional real YOLO detection replay. TOM can sample indexed media frames from media-owned timing, validate optional YOLO runtime and weights, register model metadata, apply explicit class mapping, persist mapped real model-output `ball_detection` and `player_detection` observations through the existing atomic detection contract, and print a replay URL with the real `detectionRunId`. It does not add tracklets from real detections, real pose inference, homography, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7B Result

Status: complete.

Milestone 7B validates real detection overlays in the replay workstation. Replay-info run summaries, detection overlay chunks, detection timeline items, and selected detection detail now expose optional source/runtime/model/config/class metadata so operators can distinguish real model-output evidence from fixture demo evidence. It does not add tracklets from real detections, real pose inference, court/homography evidence, model-quality claims, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7C Result

Status: complete.

Milestone 7C builds candidate tracklets from real detection observations using the existing tracklet builder. Tracklet runs, runtime configs, processing steps, tracklet observations, track point candidates, lineage rows, replay-info summaries, and replay overlay payloads now preserve source detection evidence metadata so operators can inspect real-detection-derived candidate tracks alongside the source real detection run. It does not add real pose inference, court/homography evidence, advanced tracking, smoothing/interpolation as evidence, stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7D Result

Status: complete.

Milestone 7D adds optional real pose replay runtime. TOM can validate local pose weights, probe optional runtime dependencies, register pose model metadata, run crop-from-player-detection or full-frame pose inference, normalize COCO17 keypoints, persist real `player_pose_observation` rows, preserve source player detection lineage when available, and expose real pose run metadata in replay-info, overlay chunks, timeline items, and selected pose detail. It does not add movement interpretation, stroke classification, biomechanics conclusions, court/homography evidence, bounce/hit/rally/point/scoring, real stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7E Result

Status: complete.

Milestone 7E is a court/homography evidence decision gate. It decides that court/camera/homography evidence belongs in Blueprint 8, not hidden inside Blueprint 7. It documents the future court evidence family, court keypoint observation contract, court line observation contract, camera/view observation contract, homography candidate contract, lineage ideas, replay integration, review/export ideas, and risks. It does not add a database migration, court runtime, homography computation, replay court overlay, coordinate transform service, bounce/hit/rally/point/scoring, real stream ingestion, tennis-event interpretation, or adjudication.

## Milestone 7F Result

Status: complete.

Milestone 7F closes Blueprint 7 with a completion review, final agent report, final status updates, and final local runbook orchestration. Blueprint 7 is complete: TOM v3 can run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation. Court/camera/homography evidence remains deferred to Blueprint 8. 7F does not add new runtime behavior, schema changes, court/homography implementation, movement/stroke interpretation, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Milestone 8A Result

Status: complete.

Milestone 8A starts Blueprint 8 with the court evidence schema contract. TOM now has Pydantic contracts, a normalized court template registry, storage models, Alembic migration, observation writer support, lineage relationship constants, and tests for court keypoint observations, court line observations, camera/view observations, homography candidates, and projection diagnostics. Court evidence remains geometry evidence only. 8A does not add a court detector, homography computation, replay court overlay, ball/player court projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, or adjudication.

## Milestone 8B Result

Status: complete

Milestone 8B makes the 8A schema operational with a deterministic fixture court evidence adapter. TOM can now run `run-fixture-court` or `make court-fixture` for an indexed media asset, sample media-owned frames, create fixture court model/runtime/run/step provenance, and persist `court_keypoint_observation`, `court_line_observation`, and `camera_view_observation` rows through `ObservationWriter`. 8B does not add real court inference, homography computation, projection diagnostics, replay court overlays, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, or adjudication.

## Milestone 8C Result

Status: complete

Milestone 8C hardens `camera_view_observation` rows as queryable geometry context evidence. TOM now has a camera/view query service, summary read model, evidence bundle service, and `/court/camera-view` API endpoints for query, summary, and bundle inspection. 8C does not add homography computation, projection diagnostics, replay court overlays, real camera/court inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, or adjudication.

## Milestone 8D Result

Status: complete

Milestone 8D adds homography candidate persistence. TOM can now run `build-homography-candidates` or `make homography-candidates` for a source court run, compute candidate image-pixels-to-court-template transforms from persisted court keypoint observations, attach optional court line and camera/view context, persist `homography_candidate_observation` rows through `ObservationWriter`, and write lineage from source keypoints, lines, and camera/view evidence. 8D does not add projection diagnostics, replay court overlays, real court inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, or adjudication.

## Milestone 8E Result

Status: complete

Milestone 8E adds replay overlays for persisted court geometry evidence. TOM can now open `/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>` and inspect court keypoint evidence, court line evidence, camera/view evidence, and homography candidate overlays synchronized to media-owned frame/time. 8E is display-only: it does not create projection diagnostics, project ball/player observations into court space, add real court inference, infer bounce/hit/in-out/rally/point/scoring, or adjudicate geometry.

## Milestone 8F Result

Status: complete

Milestone 8F adds projection diagnostics and court review export. TOM can now run `build-projection-diagnostics` or `make projection-diagnostics` for a homography run, project the normalized court template back into image-pixel space, persist `projection_diagnostic_observation` rows through `ObservationWriter`, and link diagnostics back to source homography candidates. Replay payloads and the workstation can include projection diagnostics through `projectionDiagnosticRunId`. TOM can also run `export-court-review-dataset` or `make court-review-export` to package selected court keypoint, court line, camera/view, homography, projection diagnostic, lineage, artifact, and annotation evidence into a TOM-native JSON export. 8F does not project ball/player observations into court space, add accepted/rejected court lifecycle state, infer bounce/hit/in-out/rally/point/scoring, or adjudicate geometry.

## Naming Transition

The implementation branch/file names may reference "1F" because the milestone was originally planned as a Blueprint 1 extension. After Blueprint 1 was declared complete, the same work was reclassified as Blueprint 2A because temporal grouping begins a new conceptual layer.

## Future Blueprints

TOM v3 Simple is complete. Blueprint 6 is complete as the replay/operator layer. Blueprint 7 is complete as the real perception replay runtime layer. Blueprint 8 is in progress as the court/camera/homography evidence layer, with 8A schema contracts, 8B fixture court evidence persistence, 8C camera/view evidence read models, 8D homography candidate persistence, 8E replay court overlays, and 8F projection diagnostics/review export complete.

Possible future blueprint candidates:

- Bounce / Hit Candidate Evidence
- Movement / Stroke Evidence Candidates
- Real Live Stream Ingestion
- Product Deployment Blueprint
