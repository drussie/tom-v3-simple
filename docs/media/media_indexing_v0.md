# TOM v3 Simple - Media Indexing v0

## Purpose

Milestone 1A makes the media substrate real before any model adapters are added.

The media indexing path turns a local video file into a durable `media_asset` with:

- source and stored URI metadata
- ffprobe-derived duration, FPS, frame count, width, and height
- sha256 checksum
- optional local storage copy under `.data/media/{media_id}/`
- centralized frame/time mapping summary

This prepares future gameplay, detection, tracking, pose, homography, and candidate adapters to reference one shared media timeline.

## Core Rule

Media indexing owns frame/time.

All downstream observations must reference the frame/time mapping owned by the indexed media record. A model runner should not invent an independent clock.

## Local Storage

The local storage adapter lives in `packages/storage/tom_v3_storage/local_media.py`.

Default storage layout:

```text
.data/
  media/
    {media_id}/
      original.mp4
```

`.data/` is ignored by git.

Two modes are supported:

- `copy_to_storage=true`: copy the source file into `.data/media/{media_id}/` and persist the stored URI as the media source URI.
- `copy_to_storage=false`: register the original local file URI without copying it.

The media metadata JSON stores the original source URI, stored URI, storage mode, storage root, checksum algorithm, ffprobe metadata, and frame/time summary.

## ffprobe Metadata

Video probing lives in `packages/video/tom_v3_video/probe.py`.

`probe_video(path_or_uri)` returns:

- `duration_ms`
- `frame_count`
- `fps`
- `width`
- `height`
- `codec`
- `format`
- `raw_probe`

`ffprobe` is required for real media indexing. If it is missing, the error is explicit:

```text
ffprobe is required for real media indexing. Install ffmpeg/ffprobe and retry.
```

The implementation uses ffprobe video stream metadata first. If `nb_frames` is unavailable, it derives a frame count from duration and FPS and records that source in metadata.

## Checksum

The storage package calculates sha256 checksums for local files.

Required behavior:

- the same file produces the same checksum
- missing files raise a clear error
- the checksum is persisted on `media_asset.checksum`
- metadata records `checksum_algorithm: sha256`

## Frame/Time Mapping

Frame/time helpers live in `packages/video/tom_v3_video/time_index.py`.

Available functions:

```text
frame_to_timestamp_ms(fps, frame_number)
timestamp_ms_to_frame(fps, timestamp_ms)
build_frame_time_summary(fps, frame_count, duration_ms)
```

Milestone 1A intentionally does not write dense per-frame rows. Instead, media records persist FPS, frame count, duration, and a compact `frame_time_index` summary in `metadata_jsonb`.

The summary includes:

- owner: `media_indexing`
- mapping type
- FPS
- frame count
- duration
- first frame timestamp
- final frame timestamp
- downstream ownership rule

## API

Register a local media file:

```http
POST /media/register-file
```

Request:

```json
{
  "source_path": "/path/to/video.mp4",
  "copy_to_storage": true,
  "media_name": "optional display name",
  "storage_root": ".data/media"
}
```

Response: the persisted `media_asset`.

Existing metadata-only registration remains available through:

```http
POST /media
GET /media/{media_id}
```

## Worker CLI

Index a local file:

```bash
python -m apps.worker.cli index-media \
  --source-path /path/to/video.mp4 \
  --copy-to-storage \
  --storage-root .data/media
```

Register without copying:

```bash
python -m apps.worker.cli index-media \
  --source-path /path/to/video.mp4 \
  --no-copy-to-storage
```

The command prints JSON with:

- `media_id`
- `source_uri`
- `stored_uri`
- `checksum`
- `fps`
- `frame_count`
- `duration_ms`
- `width`
- `height`
- `frame_time_summary`

## What Remains Out of Scope

Milestone 1A does not add model intelligence.

Still out of scope:

- YOLO inference
- TOM v1 gameplay detector integration
- gameplay classification
- real tracking
- real homography calculation
- pose processing
- bounce detection
- streaming ingestion
- production object storage
