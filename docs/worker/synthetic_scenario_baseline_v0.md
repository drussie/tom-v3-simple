# Baseline Synthetic Scenario v0

## Scenario

Name: `baseline-tennis-clip`

Synthetic media fixture:

- source_uri: `file:///dev/synthetic-tennis-clip.mp4`
- media_type: `video`
- duration_ms: `120000`
- frame_count: `3600`
- fps: `30`
- width: `1920`
- height: `1080`
- checksum: `synthetic-dev`

No real video file is required.

## Processing Steps

The scenario creates these completed processing steps:

- synthetic_media_indexing
- synthetic_gameplay_classification
- synthetic_detection_generation
- synthetic_tracking_generation
- synthetic_homography_generation
- synthetic_candidate_generation
- synthetic_artifact_generation

These steps describe the synthetic pipeline structure. They do not represent real model work.

## View-State Bands

The scenario persists:

- gameplay, frames 100-800, subtype active_point
- non_gameplay, frames 801-950, subtype between_points
- uncertain, frames 951-1050, subtype camera_cut
- gameplay, frames 1051-1500, subtype active_point

## Viewer Rows Supported

Gameplay:

- gameplay / non_gameplay / uncertain bands

Ball track:

- tracked segment
- explicit gap from frames 501-580
- tracked segment after the gap
- low-confidence segment from frames 761-800

Near player:

- tracked segment
- explicit gap from frames 701-760
- tracked segment after the gap

Far player:

- late acquisition gap from frames 100-240
- tracked segments after acquisition

Homography:

- valid placeholder from frames 100-800
- missing placeholder from frames 801-950
- valid placeholder from frames 1051-1500

Candidates:

- bounce_candidate at frame 420
- tracking_gap_candidate from frames 501-580
- hit_candidate at frame 610

Artifacts:

- overlay_frame
- overlay_clip
- trajectory_plot
- debug_json
- timeline_export

## Homography Placeholder Direction

Because 0B did not add typed homography tables, the scenario uses the observation spine with:

```text
observation_family: atomic
observation_type: homography_placeholder
atomic_kind: homography_placeholder
```

The valid placeholder payload includes:

```json
{
  "homography_status": "valid",
  "matrix_3x3": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
  "court_space": "placeholder_court_2d",
  "note": "synthetic placeholder only"
}
```

The missing interval uses the same shape with `homography_status` set to `missing`.

## Lineage

Candidate observations include lineage to supporting observations:

- bounce_candidate derives from nearby ball observations, is scoped by a gameplay segment, and is projected using a homography placeholder.
- tracking_gap_candidate is linked to ball observations before and after the gap and scoped by gameplay.
- hit_candidate is linked to ball, near-player, and far-player observations.

## Missingness

Missingness is represented in two ways:

- tracklet `metadata_jsonb.coverage_segments`
- derived `tracking_gap_candidate` observations

The future viewer should show these gaps instead of hiding them.
