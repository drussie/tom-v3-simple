# Milestone 7B Agent Report - Real Detection Overlay Validation

## Summary

Milestone 7B makes real YOLO detection replay runs operationally clear in the replay workstation. Real detection runs and fixture demo runs now carry source metadata through replay-info, overlay chunks, timeline lanes, and selected detection detail display.

## Files Created

- `docs/milestones/milestone_7b_real_detection_overlay_validation.md`
- `docs/handoffs/milestone_7b_real_detection_overlay_validation_handoff.md`
- `docs/agent_reports/milestone_7b_real_detection_overlay_validation_report.md`

## Files Modified

- `README.md`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `apps/worker/services/real_detection_replay.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OPTIONAL_YOLO.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md`
- `docs/perception/real_detection_replay_v0.md`
- `tests/test_real_detection_replay.py`
- `tests/test_replay_api.py`

## Replay-info Metadata Decisions

Available run summaries keep their existing fields and add optional source metadata. Detection runs can now identify fixture demo evidence versus real model-output evidence without breaking older consumers.

## Overlay Payload Metadata Decisions

Detection overlay payloads include optional `real_model_output`, `model_output_not_truth`, `model_registry_id`, `runtime_config_id`, `class_id`, `class_label`, `frame_time_owner`, and evidence-source fields when available. These are display fields only.

## Replay Workstation Labeling Decisions

Run selectors now display source-aware labels, such as real model output or fixture demo evidence, alongside observation counts. The UI avoids object-confirmation language.

## Selected Detection Detail Decisions

Selected detection detail now shows source/runtime/model/config/class metadata when available and keeps the evidence-only warning visible.

## Optional Real YOLO Smoke Result

Not run. No local YOLO weight files were found under `model_assets/` or `weights/`.

## Tests Run

- `.venv/bin/python -m pytest tests/test_replay_api.py tests/test_real_detection_replay.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7b_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7b_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`
- `.venv/bin/python -m apps.worker.cli run-real-detection --media-id media-plan --weights model_assets/yolo/model.pt --plan-only`

## Validation Results

- Focused replay/real detection tests: passed, 30 tests.
- Full Python suite: passed, 189 tests.
- Ruff: passed.
- Web lint/TypeScript: passed.
- Web production build: passed.
- npm audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed.
- Completion audit: passed.
- Plan-only real detection smoke: passed.
- Optional real YOLO smoke: not run because no local weights were present.

## Known Limitations

- Real YOLO quality depends on local weights, runtime, class mapping, source video, and thresholds.
- General-purpose YOLO models may miss tennis balls or produce noisy player detections.
- No real-detection-derived tracklets are added in 7B.
- No real pose inference, court/homography layer, stream ingestion, or tennis-event interpretation is added.

## Non-goals Preserved

7B does not add tracklets from real detections, real pose inference, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, official results, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Handoff

Milestone 7C - Real Detection Tracklet Generation.
