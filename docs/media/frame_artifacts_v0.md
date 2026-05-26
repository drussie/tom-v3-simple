# Frame Artifacts v0

## Purpose

Frame Artifacts v0 adds the first real frame image artifact path for TOM v3 Simple.

The goal is:

```text
persisted detection observation
-> indexed media frame/time
-> extracted frame image
-> evidence_artifact metadata
-> viewer displays frame image behind persisted bbox overlay
```

A frame artifact is evidence metadata. It does not make a detection correct, create a track, or infer an event.

## Storage Layout

Frame images are stored on the local filesystem:

```text
.data/
  artifacts/
    media/
      {media_id}/
        frames/
          frame_00000000.jpg
          frame_00000030.jpg
```

`.data/` is not committed.

## Extraction Service

Low-level frame extraction lives in:

```text
packages/video/tom_v3_video/frame_extract.py
```

Worker persistence lives in:

```text
apps/worker/services/frame_artifacts.py
```

The extractor uses `ffmpeg`, seeking by timestamp derived from the TOM v3 media frame/time utility:

```text
timestamp_ms = frame_to_timestamp_ms(media_asset.fps, frame_number)
```

If `ffmpeg` is unavailable, the error is explicit:

```text
ffmpeg is required for frame artifact extraction. Install ffmpeg and retry.
```

## Evidence Artifact Rows

The worker writes `evidence_artifact` rows with:

- `artifact_type = frame_image` for shared frame artifacts
- `artifact_type = detection_frame_image` for observation-targeted frame artifacts
- `media_id`
- `run_id`
- `target_observation_id` when targeted to a detection
- `uri = file://...`
- `frame_start = frame_end = frame_number`
- `timestamp_start_ms = timestamp_end_ms = timestamp_ms`
- `checksum`
- `metadata_jsonb.frame_time_owner = media_indexing`

Metadata includes:

- `frame_number`
- `timestamp_ms`
- `extraction_method`
- `extraction_version`
- `source_media_uri`
- `source_media_path`
- `output_path`
- `image_format`
- `placeholder = false`

## Worker CLI

Extract frame artifacts for a detection run:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --max-frames 2 \
  --output-root .data/artifacts
```

Limit to one observation:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --observation-id <OBSERVATION_ID>
```

Limit by type:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --observation-type ball_detection
```

The command prints extracted frame metadata, artifact ids, and counts.

## Artifact Serving

The API exposes a local development content route:

```text
GET /artifacts/{artifact_id}/content
```

This route serves the local file referenced by the artifact URI. It is for local/dev inspection and is not a production storage or auth design.

## Known Limitations

- No automatic extraction for every video frame.
- No production object storage.
- No CDN or authenticated artifact serving.
- No video playback overlay.
- No tracking, bounce, or hit inference.
