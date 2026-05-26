# TOM v3 Simple - Milestone 1A Real Media Indexing

## Goal

Implement the first real media ingestion and indexing layer for TOM v3 Simple.

Target flow:

```text
video file
-> media registration
-> optional local storage copy
-> ffprobe metadata
-> sha256 checksum
-> frame/time summary
-> media_asset persistence
```

## Scope

Milestone 1A adds:

- local media storage adapter
- ffprobe metadata extraction
- sha256 checksum calculation
- shared media indexing service
- `POST /media/register-file`
- worker `index-media` command
- centralized frame/time mapping utilities
- media indexing docs and tests

## Time Ownership

Media indexing owns frame/time.

All future observation-producing adapters must reference the indexed media frame/time mapping. They must not create independent time semantics.

## Non-Goals

- No YOLO integration.
- No TOM v1 gameplay detector integration.
- No gameplay classification.
- No real tracking implementation.
- No real homography calculation.
- No pose processing.
- No real bounce detection.
- No streaming ingestion.
- No production object storage.
- No production auth.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1A is complete because:

- real local media indexing exists
- ffprobe metadata extraction exists
- sha256 checksum persistence exists
- local storage copy and register-only modes exist
- media records include duration, FPS, frame count, dimensions, and checksum
- frame/time mapping utilities exist
- worker `index-media` exists
- API `POST /media/register-file` exists
- tests cover the media indexing path
- docs and runbooks are updated

## Ready For Next

Recommended next milestone: Milestone 1B - TOM v1 Gameplay Detector Adapter.

Reason: the media substrate now provides stable identity, metadata, checksum, storage URI, and frame/time mapping for future observation-producing adapters.
