# TOM v3 Simple - Current State

## Project

- Project name: TOM v3 Simple
- Repo: drussie/tom-v3-simple
- Current phase: Milestone 0B
- Current goal: backend/API foundation

## Mission

A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Implementation Status

- Implementation status: backend/API foundation exists; no real pipeline yet
- Model integration status: none
- TOM v1 gameplay detector: known asset, not integrated yet
- YOLO/YOLO26: not integrated yet
- Database: initial SQLAlchemy models and Alembic migration implemented
- API: FastAPI backend foundation implemented
- Observation writer: implemented with typed extension rows, lineage, artifacts, and idempotency
- Frontend: not implemented yet
- Worker: not implemented yet; dev-only synthetic insertion path exists in API

## Milestone 0A Result

Status: complete

Milestone 0A establishes the repo documentation spine, architecture contracts, observation-store schema direction, milestone docs, handoff memory, agent report, and placeholder project skeleton.

## Milestone 0B Result

Status: complete

Milestone 0B establishes the FastAPI backend foundation, database models, initial Alembic migration, Pydantic schema contracts, central observation writer, query/detail/lineage/artifact/annotation APIs, dev-only synthetic persistence path, and backend tests.

## Next Milestone

Recommended next handoff: Milestone 0C - Worker + Synthetic Observation Seeder.
