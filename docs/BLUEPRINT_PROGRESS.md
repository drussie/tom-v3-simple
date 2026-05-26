# TOM v3 Simple - Blueprint Progress

## Current Progress Gauge

Current: ~85%

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
