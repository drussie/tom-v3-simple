# TOM v3 Simple - Milestone 1A Agent Report

## Summary

Status: complete.

Milestone 1A adds real local media indexing for TOM v3 Simple. A local video can now be registered by API or worker CLI, probed with ffprobe, checksummed with sha256, optionally copied into `.data/media/{media_id}/`, persisted as a `media_asset`, and described with centralized frame/time mapping metadata.

## Files Created

- `apps/worker/services/media_indexer.py`
- `docs/agent_reports/milestone_1a_real_media_indexing_report.md`
- `docs/handoffs/milestone_1a_real_media_indexing_handoff.md`
- `docs/media/media_indexing_v0.md`
- `docs/milestones/milestone_1a_real_media_indexing.md`
- `packages/storage/tom_v3_storage/local_media.py`
- `packages/storage/tom_v3_storage/media_indexer.py`
- `packages/video/tom_v3_video/__init__.py`
- `packages/video/tom_v3_video/paths.py`
- `packages/video/tom_v3_video/probe.py`
- `packages/video/tom_v3_video/time_index.py`
- `tests/test_media_indexing.py`

## Files Modified

- `.gitignore`
- `Makefile`
- `README.md`
- `apps/api/routers/media.py`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/dev/local_demo_runbook.md`
- `docs/dev/local_environment_setup.md`
- `docs/dev/repo_branch_hygiene.md`
- `packages/schema/tom_v3_schema/media.py`
- `packages/storage/README.md`
- `packages/video/README.md`
- `pyproject.toml`

## Media Storage Decisions

The first storage adapter is local filesystem only. By default it stores copied media under:

```text
.data/media/{media_id}/original.{ext}
```

`.data/` is ignored by git. Register-only mode is also supported with `copy_to_storage=false`.

## ffprobe / Indexing Decisions

`ffprobe` is required for real media indexing. The wrapper fails with an actionable error if ffprobe is unavailable. Tests use mocked probe output so local codec availability does not make the test suite fragile.

The probe result persists core metadata on `media_asset` and stores codec, format, raw probe data, storage metadata, and frame/time summary in `metadata_jsonb`.

## Frame/Time Mapping Decisions

Milestone 1A uses a compact frame/time summary instead of dense per-frame rows.

Implemented utilities:

- `frame_to_timestamp_ms`
- `timestamp_ms_to_frame`
- `build_frame_time_summary`

The summary records `owner: media_indexing`, making the ownership contract explicit for future adapters.

## API Decisions

Existing manual metadata registration remains unchanged at `POST /media`.

New endpoint:

```text
POST /media/register-file
```

The endpoint delegates to the shared media indexing service so API and worker paths use the same behavior.

## Tests Run

Passed:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `npm run lint` in `apps/web`
- `npm run build` in `apps/web`
- `npm audit --omit=dev` in `apps/web`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli verify-synthetic-run --run-id 04341e8e-323b-4e93-bda8-d3396bd61fa0`
- Generated a temporary 1-second MP4 with ffmpeg and ran `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_media_index.db .venv/bin/python -m apps.worker.cli index-media --source-path tmp_media_smoke/sample.mp4 --storage-root .data/media`

## Validation Results

- Backend tests: 19 passed.
- Ruff: passed.
- Web lint/build/audit: passed with 0 production dependency vulnerabilities.
- Alembic SQLite smoke test: passed.
- Synthetic viewer smoke: passed.
- Worker seed/verify smoke: passed.
- Real media indexing smoke: passed.
- Generated media smoke output included `duration_ms=1000`, `fps=10.0`, `frame_count=10`, `width=160`, `height=90`, a sha256 checksum, and `storage_mode=copied`.

## Known Limitations

- Multipart upload is not implemented in 1A.
- Production object storage is not implemented.
- Dense `frame_index` rows are not written yet.
- Proxy video and thumbnail generation are not implemented.
- Real gameplay/model observation generation remains out of scope.

## Non-Goals Preserved

- No YOLO integration.
- No TOM v1 gameplay detector integration.
- No gameplay classification.
- No real tracking implementation.
- No real homography calculation.
- No pose processing.
- No real bounce detection.
- No streaming ingestion.
- No production auth.
- No adjudication.

## Recommended Next Handoff

Milestone 1B - TOM v1 Gameplay Detector Adapter.

Reason: media identity, metadata, checksum, storage URI, and frame/time mapping now exist. The next useful step is wrapping the known gameplay detector behind a TOM v3 adapter that writes gameplay/view-state observations through the existing observation writer.
