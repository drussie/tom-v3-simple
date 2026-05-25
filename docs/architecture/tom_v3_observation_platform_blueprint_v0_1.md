# TOM v3 Observation Platform Blueprint v0.1

## 1. Mission

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

The platform records what was observed, the evidence attached to the observation, and the lineage connecting observations to media, models, runtime configuration, and downstream candidates.

## 2. Non-goals

- No YOLO integration in Milestone 0.
- No TOM v1 gameplay detector integration in Milestone 0A.
- No real bounce detection in Milestone 0A.
- No full frontend in Milestone 0A.
- No adjudication system.
- No decision layer that converts evidence into canonical outcomes.

## 3. Core Pillars

1. Observation Store
2. Lineage / Evidence Index
3. Visual Evidence Viewer

The three pillars must evolve together. Persistence without visual inspection is opaque. Visual overlays without durable observations are temporary. Lineage without queryable observations is hard to audit.

## 4. System Architecture

The intended platform path:

```text
video upload / future stream
  -> media indexing
  -> processing run
  -> gameplay / non-gameplay observations
  -> model observations
  -> tracking / pose / court / homography observations
  -> derived candidates
  -> lineage graph
  -> evidence artifacts
  -> query API
  -> visual evidence viewer / review UI
```

Primary components:

- `apps/api`: future query and write API for media, runs, observations, artifacts, and annotations.
- `apps/worker`: future processing runner and synthetic seeder.
- `apps/web`: future visual evidence viewer.
- `packages/schema`: shared schema contracts and generated types.
- `packages/storage`: database and artifact storage helpers.
- `packages/video`: media indexing and frame/time utilities.
- `packages/observations`: observation vocabulary and payload helpers.
- `packages/visualization`: viewer data-shaping helpers.
- `migrations`: future database migrations.
- `tests`: future contract, integration, and viewer tests.

## 5. Persistence-First Principle

Model output is operational evidence only after it is persisted in the observation store with its run, model, runtime configuration, frame/time scope, payload, and idempotency key.

The database is not a final answer store. It is an evidence ledger for observations, artifacts, lineage, and annotations.

## 6. Gameplay/Non-Gameplay as First-Class Observation

Gameplay state is not an external filter hidden from the system. It is recorded as an observation with a frame/time range, confidence, source model or process, payload, and lineage.

The core view-state labels are:

- gameplay
- non_gameplay
- uncertain

These observations scope downstream processing but do not become final conclusions.

## 7. Visual Evidence Viewer Requirement

TOM v3 must be visual from the beginning.

The viewer contract:

> The database says this observation exists. Show me the evidence.

The viewer must make visible what exists, what is missing, where tracks start and stop, where view-state changes occur, where confidence drops, and how each candidate links back to evidence.

## 8. Relationship to TOM v1 Gameplay Detector

TOM v1 already has a strong gameplay/not-gameplay detector.

TOM v3 should reuse it only if it can be wrapped cleanly behind a TOM v3 interface. If it is entangled with TOM v1 infrastructure, TOM v3 should preserve the interface and rebuild the implementation.

The TOM v3 interface should emit gameplay_observation records instead of hidden control-flow decisions.

## 9. Relationship to TOM v2 Adjudication System

TOM v3 Simple is not TOM v2.

TOM v2 centered on resolving higher-level tennis decisions. TOM v3 Simple centers on preserving observations, lineage, artifacts, annotations, and visual replayability.

TOM v3 may record candidates and derived observations, but it does not convert them into official outcomes.

## 10. Milestone Path

- 0A: Repo memory + architecture/schema foundation.
- 0B: Backend / API foundation.
- 0C: Worker + synthetic observation seeder.
- 0D: Visual evidence viewer.
- 0E: QA / integration / docs finalization.

Milestone 0 ends when a synthetic path exists:

```text
media -> run -> persisted synthetic observations -> query -> visual replay
```
