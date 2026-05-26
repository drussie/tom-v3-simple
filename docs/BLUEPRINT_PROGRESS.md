# TOM v3 Simple - Blueprint Progress

## Current Progress Gauge

Current: ~25% through the MVP+ temporal-evidence extension

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
