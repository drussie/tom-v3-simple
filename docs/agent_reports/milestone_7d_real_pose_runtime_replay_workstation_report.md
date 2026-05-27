# Milestone 7D Agent Report - Real Pose Runtime for Replay Workstation

## Summary

Milestone 7D adds optional real pose replay runtime support. TOM can now plan or run a real pose pass on indexed media, persist `player_pose_observation` rows with COCO17 keypoints, preserve source player detection lineage in crop mode, and expose real pose model-output metadata in replay-info, overlay chunks, timeline items, and selected pose detail.

## Files Created

- `apps/worker/services/real_pose_replay.py`
- `packages/model_adapters/tom_v3_model_adapters/pose_inference.py`
- `tests/test_real_pose_replay.py`
- `docs/perception/real_pose_replay_v0.md`
- `docs/milestones/milestone_7d_real_pose_runtime_replay_workstation.md`
- `docs/handoffs/milestone_7d_real_pose_runtime_replay_workstation_handoff.md`
- `docs/agent_reports/milestone_7d_real_pose_runtime_replay_workstation_report.md`

## Files Modified

- `README.md`
- `Makefile`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
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

## Real Pose Runtime Decisions

7D adds a new `run-real-pose` worker command rather than expanding fixture pose adapter behavior. The command supports plan-only mode, optional runtime probing, local weight validation, crop-from-player-detection mode, full-frame mode, and fake provider injection for tests.

## Pose Weights / Model Registry Decisions

Pose weights reuse the existing local weight validation policy. Model registry rows are pose-specific and record `model_family = pose`, `model_task = pose`, `source_runtime = ultralytics_pose`, COCO17 skeleton metadata, weight sha256, file size, and evidence-only flags.

## Crop / Full-Frame Mode Decisions

Crop-from-player-detection is the preferred mode because it preserves subject association candidate provenance and links each pose observation to a source `player_detection` observation. Full-frame mode remains available for media-only pose runs.

## Persistence Decisions

Real pose observations persist through the existing `player_pose_observation` contract. Frame/time comes from source detections in crop mode or indexed media sampling in full-frame mode. Keypoints are stored in full-frame image-pixel coordinates.

## Lineage Decisions

Crop mode writes `pose_from_subject_detection_candidate` lineage from source player detections to pose observations. This lineage is provenance and does not establish movement, identity, or tennis meaning.

## Replay Metadata Decisions

Replay-info pose run summaries, pose overlay payloads, and pose timeline items can now include `evidence_source = real_pose_model_output`, `source_runtime = ultralytics_pose`, model registry id, model name/version, runtime config id, and `is_real_model_output = true`.

## Optional Real Pose Smoke Result

Optional real pose smoke was not run because no local pose weights were found under `model_assets/` or `weights/`.

## Tests Run

- `.venv/bin/python -m pytest tests/test_real_pose_replay.py tests/test_pose_persistence_lineage.py tests/test_replay_api.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7d_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7d_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`
- `.venv/bin/python -m apps.worker.cli run-real-pose --media-id media-plan --weights model_assets/pose/model.pt --source-detection-run-id detection-plan --plan-only`

## Validation Results

- Focused real pose/replay tests: passed, 35 tests.
- Full Python suite: passed, 198 tests.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed with `demo_assets/sample_point.mp4`.
- Completion audit: passed with `status = passed`.
- Plan-only real pose smoke: passed with `status = planned`.
- Optional real pose smoke: not run; no local pose weights found.

## Known Limitations

- Real pose requires optional runtime dependencies and local pose weights outside git.
- Pose observations are model-output keypoint evidence only.
- Crop mode depends on source player detections and inherits their limitations.
- Full-frame mode can emit unassociated pose observations.
- No movement interpretation, stroke classification, court/homography evidence, event candidates, scoring, real stream ingestion, or adjudication is added.

## Non-goals Preserved

7D does not add movement interpretation, stroke classification, serve detection, split-step analysis, biomechanics conclusions, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Handoff

Milestone 7E - Court / Homography Evidence Decision Gate.
