# TOM v3 Simple - Milestone 1A Handoff

## Summary

Milestone 1A implements the first real media indexing layer.

The repo can now register a real local video file, extract metadata with ffprobe, calculate a sha256 checksum, optionally copy the file into local durable storage, persist a `media_asset`, and expose the result through both API and worker CLI paths.

## Implemented

- Local storage adapter under `packages/storage/tom_v3_storage/local_media.py`
- Shared media indexing service under `packages/storage/tom_v3_storage/media_indexer.py`
- Video probing utilities under `packages/video/tom_v3_video/`
- Frame/time mapping utilities under `packages/video/tom_v3_video/time_index.py`
- API request schema `MediaRegisterFileRequest`
- API endpoint `POST /media/register-file`
- Worker service `apps/worker/services/media_indexer.py`
- Worker CLI command `index-media`
- Tests in `tests/test_media_indexing.py`
- Media indexing docs and updated runbooks

## Core Contract

Media indexing owns frame/time.

Future gameplay/model adapters should reference:

- `media_asset.id`
- `media_asset.fps`
- `media_asset.frame_count`
- `media_asset.duration_ms`
- `media_asset.metadata_jsonb.frame_time_index`

Downstream observations should not invent independent time.

## Commands

Index a real local video:

```bash
python -m apps.worker.cli index-media \
  --source-path /path/to/video.mp4 \
  --copy-to-storage
```

Register by API:

```bash
curl -X POST http://127.0.0.1:8000/media/register-file \
  -H "Content-Type: application/json" \
  -d '{"source_path":"/path/to/video.mp4","copy_to_storage":true}'
```

## What Remains Synthetic

Milestone 1A does not produce gameplay, tracking, homography, pose, or candidate observations from real media.

The synthetic seeder and viewer remain the proof path for visual observation replay until real adapters are added.

## Recommended Next Handoff

Milestone 1B - TOM v1 Gameplay Detector Adapter.

The next adapter should read indexed media records, use the shared frame/time mapping, and write gameplay/view-state observations through the existing observation writer.
