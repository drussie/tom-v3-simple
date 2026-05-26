# Tracklet Foundation v0

## Purpose

Tracklet Foundation v0 is the Milestone 2A implementation for candidate temporal grouping from persisted detection observations.

Target flow:

```text
persisted ball/player detections
-> deterministic tracklet builder
-> tracklet candidate observation rows
-> track_point candidate observation rows
-> tracklet rows
-> track_point rows
-> observation_lineage rows
-> viewer/query inspection
```

A TOM v3 tracklet means:

```text
A grouping algorithm associated these persisted detections over time.
```

It does not mean the identity is proven, the grouping is correct, or any bounce/hit/rally state exists.

## Worker Service

The worker service lives at:

```text
apps/worker/services/tracklet_builder.py
```

It consumes a source detection run and creates a new processing run for tracklet building. The source detection run is not mutated.

## Grouping Policy

The first policy is intentionally deterministic and simple:

- Ball detections are grouped in frame order.
- Player detections are grouped by source label when available:
  - `near_player`
  - `far_player`
  - `player_unknown`
- If a frame gap exceeds `max_gap_frames`, a new tracklet candidate starts.
- `max_center_distance_px` is recorded in config/metadata for future use, but this implementation does not run a sophisticated tracker.

## Observation Spine Contract

Every tracklet candidate is represented by a new `observation` row:

- `observation_family = track`
- `observation_type = ball_tracklet_candidate | player_tracklet_candidate`
- `granularity = tracklet`
- `coordinate_space = image_pixels`
- `frame_start/frame_end` from source detection frame range
- `timestamp_start_ms/timestamp_end_ms` from source detection timestamps
- `confidence` from mean source confidence
- `payload_jsonb.track_status = candidate`
- `payload_jsonb.identity_status = unverified`
- `payload_jsonb.frame_time_owner = media_indexing`

The `tracklet.observation_id` field points to this new tracklet candidate observation. It does not point directly to a source detection observation.

Every track point is also represented by a new `observation` row:

- `observation_family = track`
- `observation_type = track_point_candidate`
- `granularity = frame`
- `coordinate_space = image_pixels`
- `frame_start/frame_end` from the source detection observation
- `timestamp_start_ms/timestamp_end_ms` from the source detection observation
- `confidence` from the source detection confidence
- `payload_jsonb.source_detection_observation_id`
- `payload_jsonb.sequence_index`
- `payload_jsonb.is_interpolated = false`
- `payload_jsonb.track_status = candidate`
- `payload_jsonb.identity_status = unverified`
- `payload_jsonb.frame_time_owner = media_indexing`

The `track_point.observation_id` field points to this new track point candidate observation. It does not point directly to a source detection observation.

## Tracklet Rows

Each candidate writes a `tracklet` row:

- `track_family = ball | player`
- `subject_ref = ball | near_player | far_player | player_unknown`
- `frame_start`
- `frame_end`
- `confidence`
- `observation_id = tracklet candidate observation id`
- `metadata_jsonb.track_status = candidate`
- `metadata_jsonb.identity_status = unverified`
- `metadata_jsonb.frame_time_owner = media_indexing`
- `metadata_jsonb.source_detection_run_id`
- `metadata_jsonb.source_observation_count`
- `metadata_jsonb.track_point_count`
- `metadata_jsonb.gap_count`
- `metadata_jsonb.max_gap_frames_observed`

## Track Point Rows

Each source detection writes a `track_point` row:

- `observation_id = track_point_candidate observation id`
- `frame_number = source observation frame_start`
- `timestamp_ms = source observation timestamp_start_ms`
- `x/y` from detection center
- `width/height` from detection bbox
- `confidence` from source observation confidence
- `payload_jsonb.source_detection_observation_id`
- `payload_jsonb.source_observation_type`
- `payload_jsonb.source_label`
- `payload_jsonb.sequence_index`
- `payload_jsonb.frame_time_owner = media_indexing`

## Lineage

Milestone 2A repairs tracklet provenance by writing explicit `observation_lineage` rows:

1. Source detection to track point:

```text
parent_observation_id = source detection observation id
child_observation_id = track_point_candidate observation id
relationship_type = tracked_from
```

2. Track point to tracklet:

```text
parent_observation_id = track_point_candidate observation id
child_observation_id = tracklet_candidate observation id
relationship_type = grouped_from
```

The current schema does not have a `sequence_index` column on `observation_lineage`, so sequence indexes are stored in `payload_jsonb.sequence_index`.

## Worker CLI

Build candidate tracklets from a detection run:

```bash
python -m apps.worker.cli build-tracklets \
  --detection-run-id <DETECTION_RUN_ID> \
  --max-gap-frames 30
```

Useful options:

```text
--run-name tracklet-builder-run
--max-gap-frames 30
--max-center-distance-px 120
--grouping-method simple-frame-gap
--include-ball / --no-include-ball
--include-players / --no-include-players
```

The command prints:

- media id
- source detection run id
- tracklet builder run id
- runtime config id
- processing step id
- tracklet count
- track point count
- tracklets by family
- tracklet ids

## Viewer / Query Behavior

Open the tracklet builder run in the existing viewer:

```text
http://127.0.0.1:3000/runs/<TRACKLET_RUN_ID>
```

The viewer shows tracklet coverage rows, track point candidate observations, and lineage for the selected track run because `GET /viewer/runs/{run_id}` includes observations, tracklets, points, and lineage for the selected run.

Observations for a tracklet can be queried through:

```json
{
  "tracklet_id": "<TRACKLET_ID>"
}
```

That query returns the tracklet candidate observation and track point candidate observations. Source detection observations are reachable through `observation_lineage` and `track_point.payload_jsonb.source_detection_observation_id`.

Known limitation: the viewer is still a single-run view. It shows the tracklet run's candidate observations, tracklets, points, and lineage, but does not yet combine the source detection run observations, frame artifacts, and tracklet run into one evidence bundle.

Milestone 2B adds that cross-run inspection through:

```text
GET /tracklets/{tracklet_id}/evidence-bundle
```

The evidence bundle keeps the viewer opened on the tracklet builder run while showing source detection observations and frame artifacts from the source detection run in a focused panel.

Milestone 2C adds structured query and review on top of these candidate rows:

```text
POST /tracklets/query
```

The query endpoint can filter by run, source run, family, subject, frame range, confidence, point count, gap count, and review labels. Review annotations target observation ids and do not change tracklet, track point, source detection, lineage, or artifact rows.

## Non-Goals

- No sophisticated multi-object tracking.
- No optical flow.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally or point reconstruction.
- No scoring.
