# Milestone 0 - Observation Store + Visual Foundation

## Goal

Milestone 0 establishes the first working TOM v3 Simple foundation:

```text
media -> run -> persisted synthetic observations -> query -> visual replay
```

This milestone is still foundation work. It does not integrate real ML.

Status: complete after Milestone 0E.

## Scope

Milestone 0 should prove that the project can:

- register media metadata
- create a processing run
- persist synthetic observations
- query observations and lineage
- expose evidence artifacts
- render observations in a visual evidence viewer
- preserve missingness and uncertainty as inspectable evidence

## Sub-Milestones

### 0A: Repo Memory + Architecture / Schema Foundation

Create the documentation spine, architecture contracts, observation-store schema direction, handoff structure, and tracked skeleton directories.

### 0B: Backend / API Foundation

Create the first backend service, database migrations, schema types, and API routes for media, runs, observations, artifacts, lineage, and annotations.

Status: complete.

### 0C: Worker + Synthetic Observation Seeder

Create a worker path that seeds synthetic media/runs/observations/artifacts to exercise the store without real model integration.

Status: complete.

### 0D: Visual Evidence Viewer

Create the first web viewer that can query synthetic observations and display timeline bands, tracks, gaps, details, artifacts, and lineage.

Status: complete.

### 0E: QA / Integration / Docs Finalization

Run integration checks across backend, worker, and viewer. Update docs and handoffs for the next milestone.

Status: complete.

## Non-Goals

- No real ML integration in Milestone 0.
- No YOLO integration in Milestone 0.
- No TOM v1 integration in Milestone 0.
- No real bounce detection in Milestone 0.
- No adjudication system.

## Completion Signal

Milestone 0 is complete when synthetic data can move through:

```text
media -> run -> persisted synthetic observations -> query -> visual replay
```

and future agents can inspect that path through both APIs and the viewer.
