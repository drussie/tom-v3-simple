# TOM v3 Simple - Blueprint Progress

## Current Progress Gauge

Current: ~35-40% through Blueprint 3

## Current

- Repo exists.
- Mission is defined.
- Observation-only boundary is agreed.
- Persistence-first design is selected.
- Gameplay/non-gameplay layer is first-class.
- Visual evidence viewer is first-class.
- GitHub-as-memory workflow is selected.
- Backend app exists.
- Initial database migrations exist.
- Core schema models exist.
- Observation writer exists.
- Media, run, model, runtime config, observation, artifact, and annotation APIs exist.
- Synthetic/dev insertion path exists.
- Worker CLI exists.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Candidate observations have lineage and artifacts.
- Visual evidence viewer foundation exists.
- Viewer data is loaded from backend/API contracts.
- Milestone 0 local setup and demo runbooks exist.
- Makefile commands exist for common local workflows.
- Integration smoke validation exists for synthetic viewer data.
- Real local media file registration exists.
- ffprobe-based metadata extraction exists.
- Media checksum and local storage copy/register modes exist.
- Central frame/time mapping utilities exist.
- Worker `index-media` exists.
- Gameplay adapter interface exists.
- Fixture gameplay adapter produces persisted view-state observations.
- TOM v1 portability assessment exists.
- Worker `run-gameplay-adapter` exists.
- Existing viewer can show gameplay bands from adapter runs.
- Detection adapter interface exists.
- Fixture detection adapter produces persisted ball/player atomic observations.
- YOLO26/Ultralytics portability assessment exists.
- Worker `run-detection-adapter` exists.
- Query/viewer paths can inspect detection observations.
- Detection overlay viewer transform exists.
- Persisted ball/player bboxes are visually inspectable in the viewer.
- Detection observations can be selected and highlighted in the overlay.
- Frame extraction service exists.
- Worker `extract-frame-artifacts` exists.
- Frame image artifacts are persisted as evidence artifacts.
- Viewer can display frame artifacts behind persisted detection bboxes.
- Tracklet builder service exists.
- Persisted detections can be grouped into candidate tracklets.
- Tracklet and track point rows are persisted.
- Tracklet candidates have first-class observation spine rows.
- Track point candidates have first-class observation spine rows.
- Observation lineage links source detections to track points and track points to tracklets.
- Tracklet evidence bundle service exists.
- Viewer can inspect source detection evidence from a tracklet builder run.
- Tracklet query service exists.
- Candidate tracklets are searchable by run, source run, family, subject, frame range, confidence, gaps, point count, and review annotations.
- Tracklet evidence bundles include annotation summaries.
- Viewer review controls can add annotations to tracklet, track point, and source detection observations.
- Tracklet review dataset export service exists.
- Candidate tracklet evidence can be exported by tracklet ids or by structured query filters.
- Export artifacts are persisted as local JSON files with `evidence_artifact` metadata and checksums.
- Query-based exports can persist `query_result` memory.
- Blueprint 2 completion review exists.
- Temporal evidence invariants are documented and validated.
- Blueprint 2 is complete.
- Blueprint 3 has started.
- Base `tom_v3` does not require Ultralytics, Torch, or OpenCV imports.
- Optional YOLO dependency path exists in `requirements-yolo.txt`.
- YOLO runtime probe and device resolver exist.
- Worker `yolo-runtime-probe` reports optional dependency and device availability.
- Model weights and runtime assets are ignored by git.
- YOLO weights validation exists.
- Local weights are fingerprinted with sha256 and file size.
- Default ball/player YOLO class mapping exists and is validated.
- YOLO model registry helper exists.
- Worker `register-yolo-model` validates/registers weights without creating runs or observations.

## After Milestone 0A

Expected: ~30%

- Repo memory structure exists.
- Architecture docs exist.
- Observation-store schema direction exists.
- Future Codex agents have stable contracts.

## Milestone 0A Status

Status: complete.

The repo now has durable project memory, architecture docs, schema contracts, milestone docs, a handoff file, an agent report, and lightweight tracked skeleton directories for future implementation work.

## After Milestone 0B

Expected: ~40-45%

- Backend app exists.
- Initial database migrations exist.
- Core schema models exist.
- Observation writer exists.
- Media and run APIs exist.
- Observation query/detail APIs exist.
- Synthetic/dev insertion path exists.
- Worker CLI exists.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Candidate observations have lineage and artifacts.
- Docs and implementation log are updated.

## Milestone 0B Status

Status: complete.

The repo now has a tested backend/API foundation for media, runs, models, runtime configs, observations, lineage, artifacts, annotations, and dev synthetic persistence.

## After Milestone 0C

Expected: ~50-55%

- Worker package has executable entrypoints.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Gameplay/non-gameplay/uncertain bands are persisted.
- Candidate observations have lineage and artifacts.
- API dev route reuses shared seeding code.
- Tests validate the worker/seeder path.

## Milestone 0C Status

Status: complete.

The repo now has a worker CLI and shared synthetic seeder that creates viewer-ready baseline observations for Milestone 0D.

## After Milestone 0D

Expected: ~65%

- `apps/web` has a working visual evidence viewer foundation.
- The viewer can load a run by run id.
- The viewer shows gameplay/non-gameplay/uncertain bands.
- The viewer shows ball, near-player, and far-player track coverage rows.
- The viewer shows homography valid/missing intervals.
- The viewer shows candidate markers.
- The viewer shows observation detail, lineage, and artifact metadata.
- Missingness is visible.

## Milestone 0D Status

Status: complete.

The repo now has a backend-composed viewer run endpoint and a Next.js web app that renders persisted synthetic evidence without adding real ML or a frontend-only evidence model.

## After Milestone 0E

Expected: ~75-80%

- Milestone 0 is consolidated.
- Repo docs are current and easy to follow.
- Local environment setup is documented.
- Local demo commands are documented and tested.
- Backend, worker, and web validation passes.
- Branch/default-branch cleanup is explicitly documented.
- The next real media/model milestone is ready.

## Milestone 0E Status

Status: complete.

The repo now has one documented local setup path, one synthetic seed path, one backend API, one viewer path, one validation story, and exact branch/default-branch cleanup guidance.

## After Milestone 1A

Expected: ~85%

- Real local media file registration exists.
- ffprobe-based duration, FPS, frame count, dimensions, codec, and format extraction exists.
- Media checksum and storage path are persisted.
- Frame/time mapping ownership is centralized in media indexing utilities.
- Viewer/API can load real media metadata before observations exist.
- Future gameplay/model adapters have a stable media substrate.

## Milestone 1A Status

Status: complete.

The repo now has real media indexing for local files, durable media registration, storage metadata, checksum persistence, frame/time summaries, API/worker entrypoints, tests, and docs.

## After Milestone 1B

Expected: ~90%

- First gameplay/view-state adapter seam exists.
- TOM v1 portability status is documented.
- Fixture gameplay adapter provides deterministic dev/test output.
- Gameplay adapter runs create model, config, run, and step records.
- Gameplay adapter output persists typed gameplay observations.
- Existing viewer can display gameplay/non_gameplay/uncertain bands from adapter runs.

## Milestone 1B Status

Status: complete.

The repo now has a stable TOM v3 gameplay adapter interface, fixture adapter, TOM v1 unavailable stub, worker CLI commands, persistence flow, viewer compatibility tests, and model adapter docs.

## After Milestone 1C

Expected: ~95%

- First ball/player detection adapter seam exists.
- YOLO26/Ultralytics portability status is documented.
- Fixture detection adapter provides deterministic dev/test output.
- Detection adapter runs create model, config, run, and step records.
- Detection adapter output persists typed atomic observations.
- Query API can retrieve ball_detection and player_detection observations.
- Existing viewer payload includes detection observations.

## Milestone 1C Status

Status: complete.

The repo now has a TOM v3 detection adapter interface, fixture detector, YOLO unavailable stub, worker CLI commands, atomic observation persistence flow, query/viewer compatibility tests, and model adapter docs.

## After Milestone 1D

Expected: ~100% for the TOM v3 Simple observation-platform MVP loop

- Persisted ball/player detections are visually inspectable.
- Existing viewer can render detection bboxes on a coordinate-space media panel.
- Detection observations can be selected from the timeline/list and highlighted in the overlay.
- Missing video playback does not block inspection.
- TOM v3 remains observation-only.

## Milestone 1D Status

Status: complete.

The repo now has a data-driven detection overlay layer that renders persisted bbox observations from the viewer payload without adding tracking, event inference, or a frontend-only detection model.

## After Milestone 1E

Expected: ~105% / MVP+ foundation

- Selected detection frames can have real frame image artifacts.
- Frame extraction service exists.
- Frame artifact metadata is persisted as evidence artifact rows.
- Viewer displays real frame imagery when available.
- Coordinate canvas fallback still works.
- TOM v3 remains observation-only.

## Milestone 1E Status

Status: complete.

The repo now has ffmpeg-backed frame artifact extraction, local artifact metadata persistence, artifact file serving for local development, and viewer support for drawing persisted detection bboxes over extracted frame imagery.

## After Milestone 1F

Expected: ~15% through the MVP+ temporal-evidence extension

- Tracklet foundation exists.
- Persisted detections can be grouped into tracklet candidates.
- `tracklet` and `track_point` rows are created from source observations.
- Existing viewer can show basic tracklet coverage/evidence.
- TOM v3 still does not claim identity, bounce, hit, rally, or point state.

## Milestone 1F Status

Status: complete.

The repo now has a deterministic tracklet-builder run path that creates candidate temporal groupings from persisted detection observations without mutating the source detection run or adding higher-level tennis event interpretation.

## After Milestone 2A

Expected: ~25% through the MVP+ temporal-evidence extension

- Tracklet candidates have observation spine rows.
- Track point candidates have observation spine rows.
- `tracklet.observation_id` points to a tracklet candidate observation.
- `track_point.observation_id` points to a track point candidate observation.
- Source detections are linked through `tracked_from` lineage.
- Track points are linked to tracklets through `grouped_from` lineage.
- Viewer/query paths can inspect candidate track observations.

## Milestone 2A Status

Status: complete.

The existing 1F branch now satisfies the Blueprint 2 persistence contract: candidate tracklets and track points are first-class observations with lineage to source detections and grouping observations.

## After Milestone 2B

Expected: ~55-60% through Blueprint 2

- A tracklet evidence bundle combines tracklet run evidence with source detection run evidence.
- Viewer can inspect a tracklet candidate and see its source detections.
- Viewer can drill from tracklet to track point to source detection.
- Frame artifacts are shown when available.
- Multi-run evidence remains descriptive and observation-only.

## Milestone 2B Status

Status: complete.

The repo now has a dynamic tracklet evidence bundle endpoint and a lightweight viewer panel for tracklet candidate, track point candidate, source detection, frame artifact, and lineage inspection across runs.

## After Milestone 2C

Expected: ~75% through Blueprint 2

- Tracklet candidates can be queried with structured review filters.
- Query responses include tracklet summaries, counts, annotation summaries, and evidence bundle URLs.
- Evidence bundles include tracklet, track point, and source detection annotation summaries.
- Viewer review controls can create annotations on selected candidate evidence.
- Query/review remains descriptive and observation-only.

## Milestone 2C Status

Status: complete.

The repo now has structured tracklet candidate query, evidence-bundle annotation summaries, and a viewer review flow that writes human annotations without mutating source observations, candidate track points, candidate tracklets, lineage, or artifacts.

## After Milestone 2D

Expected: ~90% through Blueprint 2

- Tracklet evidence bundles can be exported into durable review dataset artifacts.
- Reviewed candidate evidence can be packaged for future evaluation or training workflows.
- Export rows preserve media, run, model, config, lineage, artifact, and annotation provenance.
- Export artifacts carry explicit candidate-only and no-adjudication warnings.
- Export does not mutate source observations.

## Milestone 2D Status

Status: complete.

The repo now has a JSON review dataset export path for candidate tracklet evidence, available through both worker CLI and API, with persisted export artifact metadata and optional query result memory for query-based exports.

## After Milestone 2E

Expected: 100% through Blueprint 2

- Blueprint 2 completion review exists.
- Blueprint 2 status is complete.
- The 1F to 2A naming transition is documented.
- Temporal evidence invariants are documented and validated.
- Local runbook includes the complete Blueprint 2 flow.
- Next blueprint boundary is clear.

## Milestone 2E Status

Status: complete.

Blueprint 2 is complete. TOM v3 can build candidate tracklets from persisted detections, preserve source lineage, inspect evidence across runs, query and review candidates, and export review datasets without adding pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## After Milestone 3A

Expected: ~15-20% through Blueprint 3

- Base `tom_v3` remains lightweight.
- Optional YOLO dependency install path exists.
- Runtime probe can report Ultralytics, Torch, OpenCV, CUDA, and MPS availability.
- Device resolver can choose `cpu`, `mps`, or `cuda:0` safely.
- Missing runtime dependencies produce clear actionable diagnostics.
- Documentation explains how to create and validate `tom_v3_yolo`.
- No real YOLO detections are persisted yet.

## Milestone 3A Status

Status: complete.

The repo now has a clean optional YOLO runtime boundary with `requirements-yolo.txt`, import guards, runtime diagnostics, device resolution, worker probe command, weights ignore policy, tests, and docs. Blueprint 3 is prepared for model registry and weights validation without adding real inference, pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## After Milestone 3B

Expected: ~35-40% through Blueprint 3

- YOLO model registry contract exists.
- YOLO weights can be validated from local filesystem paths.
- Weights are fingerprinted with sha256 and file size.
- Required checksum mismatches fail clearly.
- Safe local root policy exists for `model_assets/yolo` and `weights/yolo`.
- Default ball/player class mapping exists.
- Optional model metadata probe can capture class names when runtime is available.
- Model registry rows can be created or reused for validated weights.
- No real YOLO detections are persisted yet.

## Milestone 3B Status

Status: complete.

The repo now has a YOLO weights validation and model registry foundation. Local weights can be validated, fingerprinted, mapped to TOM v3 ball/player observation targets, and registered in `model_registry` without creating processing runs or observations.
