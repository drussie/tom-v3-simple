# TOM v3 Simple - Milestone 2B Handoff

## Mission

Implement the first tracklet viewer / multi-run evidence bundle for TOM v3 Simple.

The bundle connects:

```text
tracklet candidate
-> track point candidates
-> source detection observations
-> frame artifacts
-> lineage
```

## Implementation Summary

- Add a dynamic evidence bundle service.
- Add a read-only API endpoint for a tracklet id.
- Add viewer support for selecting tracklet candidates and track point candidates.
- Display source detection evidence and frame artifacts when available.
- Preserve observation-only vocabulary.

## Non-Goals

- No new tracking algorithm.
- No pose or court homography.
- No bounce or hit detection.
- No rally or point reconstruction.
- No scoring.
- No adjudication.

## Validation

Required validation:

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- Alembic SQLite smoke
- synthetic viewer smoke
- local media / detection / frame artifact / tracklet / evidence bundle smoke
