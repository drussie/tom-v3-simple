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
