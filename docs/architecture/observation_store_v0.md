# Observation Store v0

## Purpose

The observation store is the durable spine of TOM v3 Simple. It persists model output, derived candidates, gameplay/view-state ranges, tracks, artifacts, annotations, and lineage as queryable evidence.

The store records what was observed, where it was observed, how it was produced, and what evidence or parent observations it depends on.

## Core Immutability Rule

Observations are append-only.

A later model run creates new observations.
Human review creates annotations.
Nothing important is silently overwritten.

Corrections, alternative interpretations, review notes, and later model outputs should be represented as new observations, annotations, or lineage-linked records.

## Observation Spine

Every specific observation type should connect to the central `observation` record.

```text
observation
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

### Field Intent

- `id`: stable observation identifier.
- `media_id`: media asset this observation belongs to.
- `run_id`: processing run that produced this observation.
- `observation_family`: broad grouping such as gameplay, pose, court, tracking, homography, candidate, annotation, or artifact-linked observation.
- `observation_type`: concrete type within the family.
- `granularity`: frame, frame_range, track_point, tracklet, segment, video, or run-level scope.
- `frame_start`: inclusive starting frame when frame-based scope is known.
- `frame_end`: inclusive ending frame when frame-based scope is known.
- `timestamp_start_ms`: inclusive starting timestamp when time scope is known.
- `timestamp_end_ms`: inclusive ending timestamp when time scope is known.
- `confidence`: model or process confidence when available.
- `model_id`: source model registry entry when model-produced.
- `runtime_config_id`: runtime configuration used for this observation.
- `coordinate_space`: source coordinate system such as image_pixels, normalized_frame, court_plane, world_estimate, or none.
- `schema_version`: payload contract version.
- `payload_jsonb`: structured payload for the concrete observation type.
- `idempotency_key`: stable key used to prevent duplicate writes for the same run/output scope.
- `created_at`: creation timestamp.

## Tables and Concepts

### media_asset

Represents uploaded or referenced media.

Expected fields:

- id
- source_uri
- media_type
- duration_ms
- frame_count
- fps
- width
- height
- checksum
- metadata_jsonb
- created_at

### frame_index

Maps frame numbers to timestamps and optional extraction artifacts.

Expected fields:

- id
- media_id
- frame_number
- timestamp_ms
- image_artifact_id
- metadata_jsonb

### model_registry

Records models or model-like processes that emit observations.

Expected fields:

- id
- name
- version
- model_family
- source
- metadata_jsonb
- created_at

### runtime_config

Records parameters, thresholds, feature flags, and environment details for a processing run or step.

Expected fields:

- id
- config_name
- config_version
- payload_jsonb
- created_at

### processing_run

Represents one processing attempt over a media asset.

Expected fields:

- id
- media_id
- run_name
- run_status
- started_at
- completed_at
- runtime_config_id
- metadata_jsonb

### processing_step

Represents a stage within a run, such as indexing, gameplay classification, tracking, pose, court, homography, candidate generation, artifact extraction, or synthetic seeding.

Expected fields:

- id
- run_id
- step_name
- step_status
- started_at
- completed_at
- runtime_config_id
- metadata_jsonb

### observation

The central append-only spine for all observations.

Specific tables may extend this spine with typed fields while keeping the spine queryable across the platform.

### gameplay_observation

Represents gameplay, non_gameplay, or uncertain ranges.

Expected fields:

- observation_id
- view_state
- view_state_subtype
- payload_jsonb

### atomic_observation

Represents the smallest persisted model or process output that future stages may use.

Expected fields:

- observation_id
- atomic_kind
- payload_jsonb

### pose_observation

Represents detected or estimated player pose data.

Expected fields:

- observation_id
- subject_ref
- keypoints_jsonb
- bbox_jsonb
- pose_model_metadata_jsonb

### tracklet

Represents a contiguous track segment for a subject or object.

Expected fields:

- id
- media_id
- run_id
- track_family
- subject_ref
- frame_start
- frame_end
- confidence
- observation_id
- metadata_jsonb

### track_point

Represents one point in a tracklet.

Expected fields:

- id
- tracklet_id
- observation_id
- frame_number
- timestamp_ms
- x
- y
- width
- height
- confidence
- payload_jsonb

### court_observation

Represents court lines, court keypoints, regions, or court geometry estimates.

Expected fields:

- observation_id
- court_geometry_jsonb
- coordinate_space
- payload_jsonb

### homography_observation

Represents image-to-court or court-to-image transform estimates and validity ranges.

Expected fields:

- observation_id
- transform_jsonb
- source_coordinate_space
- target_coordinate_space
- validity_payload_jsonb

### derived_observation

Represents a higher-level candidate or signal derived from one or more observations.

Expected fields:

- observation_id
- derived_kind
- derivation_payload_jsonb

### observation_lineage

Links observations to parent observations, processing steps, artifacts, and derivation context.

Expected fields:

- id
- child_observation_id
- parent_observation_id
- relationship_type
- processing_step_id
- payload_jsonb
- created_at

### evidence_artifact

Represents media snippets, frame crops, overlay images, JSON payloads, logs, or other evidence artifacts.

Expected fields:

- id
- media_id
- run_id
- artifact_type
- uri
- frame_start
- frame_end
- timestamp_start_ms
- timestamp_end_ms
- checksum
- metadata_jsonb
- created_at

### human_annotation

Represents human review notes, labels, comments, or corrections attached to observations, artifacts, frames, or ranges.

Expected fields:

- id
- media_id
- observation_id
- evidence_artifact_id
- frame_start
- frame_end
- timestamp_start_ms
- timestamp_end_ms
- annotation_type
- payload_jsonb
- created_by
- created_at

### query_result

Represents reusable or saved query outputs for review sessions, exports, or UI state.

Expected fields:

- id
- query_name
- query_payload_jsonb
- result_payload_jsonb
- created_by
- created_at

## Schema Direction

Milestone 0B should convert this contract into initial database migrations and API shapes. The initial implementation can use a compact subset, but it should preserve the observation spine and append-only behavior from the start.
