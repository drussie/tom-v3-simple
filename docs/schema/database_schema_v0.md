# Database Schema v0

## Purpose

Database Schema v0 turns the observation-store contract into SQLAlchemy models and an Alembic migration.

The database stores observations, lineage, artifacts, and annotations as operational evidence.

## Migration

Initial migration:

```text
migrations/versions/0001_observation_store.py
```

The ORM source is:

```text
packages/storage/tom_v3_storage/db_models.py
```

## Core Tables

Implemented tables:

- `media_asset`
- `model_registry`
- `runtime_config`
- `processing_run`
- `processing_step`
- `observation`
- `gameplay_observation`
- `atomic_observation`
- `derived_observation`
- `tracklet`
- `track_point`
- `observation_lineage`
- `evidence_artifact`
- `human_annotation`
- `query_result`

Optional v0 architecture tables not yet implemented:

- `frame_index`
- `pose_observation`
- `court_observation`
- `homography_observation`

## Observation Spine

The central table is `observation`:

```text
id
media_id
run_id
observation_family
observation_type
granularity
frame_start
frame_end
timestamp_start_ms
timestamp_end_ms
confidence
model_id
runtime_config_id
coordinate_space
schema_version
payload_jsonb
idempotency_key
created_at
```

## Typed Extensions

`gameplay_observation` stores:

- `observation_id`
- `view_state`
- `view_state_subtype`
- `payload_jsonb`

`atomic_observation` stores:

- `observation_id`
- `atomic_kind`
- `payload_jsonb`

`derived_observation` stores:

- `observation_id`
- `derived_kind`
- `derivation_payload_jsonb`

## Lineage and Evidence

`observation_lineage` links child observations to parent observations with relationship types such as:

- derived_from
- tracked_from
- scoped_by
- projected_using
- rendered_from
- grouped_with

`evidence_artifact` stores artifact metadata and optional target observation links.

`human_annotation` stores review notes and labels without mutating observations.

## Index Direction

Implemented query indexes include:

- `media_id`
- `run_id`
- `(media_id, run_id)`
- `observation_family`
- `observation_type`
- `(media_id, run_id, observation_type)`
- `(frame_start, frame_end)`
- `(timestamp_start_ms, timestamp_end_ms)`
- unique `idempotency_key`

## Immutability Rule

Observations are append-only.

A later model run creates new observations.
Human review creates annotations.
Nothing important is silently overwritten.
