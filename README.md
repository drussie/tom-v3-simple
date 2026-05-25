# TOM v3 Simple

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Observation-Only Boundary

TOM v3 Simple is not TOM v2.

It does not adjudicate truth. It records observations, lineage, artifacts, and annotations.

The core invariant:

> TOM v3 records what was observed, not what was proven.

## Core Pillars

1. Observation Store
2. Lineage / Evidence Index
3. Visual Evidence Viewer

## Current Milestone

Current phase: Milestone 0A - Repo Memory + Architecture / Schema Foundation.

This milestone creates the repo-backed memory, architecture documentation, schema direction, and handoff structure future agents should follow.

No real model pipeline, YOLO integration, TOM v1 integration, bounce detection, or full frontend is implemented in this milestone.

## Docs Entrypoint

Start with [docs/CONTROL_ROOM_INDEX.md](docs/CONTROL_ROOM_INDEX.md).

## Basic Repo Structure

```text
apps/
  api/       Placeholder for the future backend API.
  worker/    Placeholder for future processing and seeding workers.
  web/       Placeholder for the future visual evidence viewer.
packages/
  schema/          Shared schema contracts.
  storage/         Storage adapters and persistence helpers.
  video/           Media indexing and video utilities.
  observations/    Observation vocabulary and helpers.
  visualization/   Viewer-oriented utilities.
migrations/        Future database migrations.
tests/             Future test coverage.
docs/              Durable project memory and architecture contracts.
```
