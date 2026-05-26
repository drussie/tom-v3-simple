# Tracklet Foundation v0

## Purpose

Tracklet Foundation v0 groups already-persisted detection observations into candidate temporal groupings.

Target flow:

```text
persisted ball/player detections
-> deterministic tracklet builder
-> tracklet rows
-> track_point rows
-> source links back to detection observations
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
- `max_center_distance_px` is recorded in config/metadata for future use, but the first implementation does not run a sophisticated tracker.

## Persistence

Each candidate writes a `tracklet` row:

- `track_family = ball | player`
- `subject_ref = ball | near_player | far_player | player_unknown`
- `frame_start`
- `frame_end`
- `confidence`
- `observation_id` as representative source detection observation
- `metadata_jsonb.track_status = candidate`
- `metadata_jsonb.identity_status = unverified`
- `metadata_jsonb.frame_time_owner = media_indexing`
- `metadata_jsonb.source_detection_run_id`
- `metadata_jsonb.source_observation_count`

Each source detection writes a `track_point` row:

- `observation_id = source detection observation id`
- `frame_number = source observation frame_start`
- `timestamp_ms = source observation timestamp_start_ms`
- `x/y` from detection center
- `width/height` from detection bbox
- `confidence` from source observation confidence
- `payload_jsonb.source_observation_id`
- `payload_jsonb.frame_time_owner = media_indexing`

## Source Links

The current schema does not provide a direct lineage table for `tracklet` or `track_point` rows because `observation_lineage` links observation rows only.

Milestone 1F therefore uses:

- `tracklet.observation_id` for a representative source detection
- `track_point.observation_id` for exact source detection linkage
- `track_point.payload_jsonb.source_observation_id`
- `tracklet.metadata_jsonb.source_detection_run_id`

This is explicit source linkage, but not a full lineage graph for tracklets yet.

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

The viewer shows tracklet coverage rows and track points because `GET /viewer/runs/{run_id}` already includes tracklets for the selected run.

Source detection observations can be queried through:

```json
{
  "tracklet_id": "<TRACKLET_ID>"
}
```

Known limitation: the viewer is still a single-run view. It shows the tracklet run's tracklets and points, but does not yet combine the source detection run observations, frame artifacts, and tracklet run into one evidence bundle.

## Non-Goals

- No sophisticated multi-object tracking.
- No optical flow.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally or point reconstruction.
- No scoring.
