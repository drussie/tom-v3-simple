# Milestone 7C Agent Report - Real Detection Tracklet Generation

## Summary

Milestone 7C extends the existing candidate tracklet builder so real YOLO detection replay runs can feed candidate temporal groupings. The implementation preserves source detection metadata through runtime config, processing run, processing step, tracklet observations, track point candidates, lineage, replay-info, and replay overlay payloads.

## Files Created

- `docs/milestones/milestone_7c_real_detection_tracklet_generation.md`
- `docs/handoffs/milestone_7c_real_detection_tracklet_generation_handoff.md`
- `docs/agent_reports/milestone_7c_real_detection_tracklet_generation_report.md`

## Files Modified

- `README.md`
- `Makefile`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `apps/worker/services/tracklet_builder.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md`
- `docs/perception/real_detection_replay_v0.md`
- `tests/test_tracklet_builder.py`

## Tracklet Builder Decisions

7C reuses the existing deterministic tracklet builder. It adds source metadata and validation around the existing command instead of introducing a new tracker or changing grouping semantics.

## Source Detection Validation Decisions

The builder validates that the source run exists, has media, and contains atomic ball/player detection observations with frame/time and typed atomic detail rows. Source evidence metadata is derived from persisted detection payloads and runtime config metadata.

## Lineage Decisions

Existing `tracked_from` and `grouped_from` lineage rows remain the canonical provenance path. 7C adds source detection evidence metadata to the `tracked_from` lineage payload for easier audit and replay inspection.

## Replay Metadata Decisions

Replay-info can now label tracklet runs as real-detection-derived candidate tracklets when the source detection run came from real model output. Replay tracklet and track point overlay payloads include source detection run/runtime/evidence metadata when available.

## Replay Workstation Label/Detail Decisions

The replay workstation shows source detection run id, source evidence type, and source runtime for selected tracklet candidates and track point candidates. Copy remains candidate/evidence-only.

## Optional Real YOLO + Tracklet Smoke Result

Optional real YOLO + tracklet smoke was not run because no local YOLO weights were found under `model_assets/` or `weights/`.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7c_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7c_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`

## Validation Results

- Full Python suite: passed, 190 tests.
- Ruff: passed.
- Web lint: passed after rerun. The first lint attempt overlapped with `next build` and hit a transient `.next` generated-types file before build completion.
- Web build: passed.
- Web audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed.
- Completion audit: passed with `status = passed`.
- Optional real YOLO + tracklet smoke: not run; no local weights found.

## Known Limitations

- Tracklets are deterministic candidate groupings from source detections.
- Real-detection-derived tracklets inherit YOLO model and class-mapping limitations.
- No smoothing, interpolation, identity proof, court reasoning, or tennis-event interpretation is added.
- No real pose inference or stream ingestion is added.

## Non-goals Preserved

7C does not add real pose inference, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, official results, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Handoff

Milestone 7D - Real Pose Runtime for Replay Workstation.
