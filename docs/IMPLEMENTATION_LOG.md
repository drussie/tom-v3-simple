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
