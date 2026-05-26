# TOM v3 Simple - Current State

## Project

- Project name: TOM v3 Simple
- Repo: drussie/tom-v3-simple
- Current phase: Milestone 0E
- Current goal: integration, QA, local runbook, and repo consolidation

## Mission

A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Implementation Status

- Implementation status: Milestone 0 foundation consolidated; no real ML pipeline yet
- Model integration status: none
- TOM v1 gameplay detector: known asset, not integrated yet
- YOLO/YOLO26: not integrated yet
- Database: initial SQLAlchemy models and Alembic migration implemented
- API: FastAPI backend foundation implemented
- Observation writer: implemented with typed extension rows, lineage, artifacts, and idempotency
- Worker synthetic seeder: implemented
- Visual evidence viewer: implemented in `apps/web`
- Synthetic data: baseline scenario creates viewer-ready observations, tracklets, gaps, candidates, lineage, and artifacts
- Local setup: documented with `.env.example`, Makefile, and dev runbooks

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

## Next Milestone

Recommended next handoff: Milestone 1A - Real Media Indexing + Video Upload/Registration.
