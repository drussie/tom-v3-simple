# Milestone 3F Handoff - Blueprint 3 Completion Review / Real Model Runtime Hardening

## Starting State

Milestone 3E was accepted and merged to main.

Blueprint 1 is complete.
Blueprint 2 is complete.
Blueprint 3 was approximately 90-95% complete before this handoff.

## Mission

Close Blueprint 3 with a completion review and hardening pass.

Do not add new model intelligence.

## Completed Work

- Created the Blueprint 3 completion review.
- Updated Blueprint 3 status to complete.
- Documented the invariant audit and mapped coverage to tests.
- Updated current state, blueprint progress, implementation log, README, control-room index, and runbook.
- Confirmed the full YOLO runtime flow:
  - optional environment,
  - runtime probe,
  - weights validation and registration,
  - YOLO-like normalization,
  - frame-level provider,
  - persisted atomic detections,
  - viewer validation,
  - Blueprint 2 tracklet compatibility.
- Preserved the observation-only boundary.

## Blueprint 3 Completion Statement

Blueprint 3 proved that TOM v3 can safely introduce optional real YOLO / Ultralytics runtime without contaminating the base environment, validate and register model weights, normalize YOLO-like outputs into TOM v3 detection payloads, persist YOLO-origin ball/player observations through the existing detection pipeline, document a real local YOLO smoke path, and keep downstream viewer, tracklet, review, and export contracts unchanged.

Blueprint 3 did not add pose, court homography, bounce detection, hit detection, rally or point reconstruction, scoring, identity proof, YOLO tracking mode, or adjudication.

## Validation

Run before accepting:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint
cd apps/web && npm run build
cd apps/web && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
python -m apps.worker.cli yolo-runtime-probe
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

Real local YOLO smoke remains optional and depends on local runtime packages, weights, and sample media.

## Non-Goals Preserved

- No YOLO tracking mode.
- No tracklets inside the YOLO adapter.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally, point, or scoring.
- No production GPU worker.
- No remote or automatic weights download.
- No adjudication.

## Recommended Next Blueprint

Blueprint 4 - Pose Observation / Movement Evidence Layer.

Pose should stay in Blueprint 4 and should use the same observation-only contract.
