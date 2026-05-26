# TOM v3 Simple - Current State

## Project

- Project name: TOM v3 Simple
- Repo: drussie/tom-v3-simple
- Current phase: Milestone 1E
- Current goal: detection artifact / frame extraction foundation

## Mission

A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Implementation Status

- Implementation status: persisted ball/player observations can be inspected over coordinate overlays and extracted frame artifacts
- Model integration status: fixture gameplay and fixture detection adapters implemented for deterministic dev/test output
- TOM v1 gameplay detector: known asset, portable source/assets not available in this repo/environment; integration stub documented
- YOLO/YOLO26: runtime/assets not available in this repo/environment; unavailable stub documented
- Database: initial SQLAlchemy models and Alembic migration implemented
- API: FastAPI backend foundation implemented
- Media indexing: implemented for local files via ffprobe, sha256 checksum, local storage copy/register mode, and frame/time summary
- Gameplay adapter: implemented with `BaseGameplayAdapter`, fixture adapter, TOM v1 unavailable stub, worker service, and worker CLI
- Detection adapter: implemented with `BaseDetectionAdapter`, fixture adapter, YOLO unavailable stub, worker service, and worker CLI
- Observation writer: implemented with typed extension rows, lineage, artifacts, and idempotency
- Worker synthetic seeder: implemented
- Visual evidence viewer: implemented in `apps/web` with detection bbox overlay and frame artifact image support
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

## Next Milestone

Recommended next handoff: Milestone 1F - Tracklet Foundation from Persisted Detections, unless YOLO26 runtime/assets become available and real detector integration is prioritized.
