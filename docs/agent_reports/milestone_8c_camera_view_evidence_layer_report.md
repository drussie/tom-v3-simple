# Milestone 8C Agent Report - Camera / View Evidence Layer

## Summary

Milestone 8C makes camera/view observations queryable and inspectable as geometry context evidence. 8B continues to own fixture camera/view writes; 8C adds the read service, summary read model, bundle, and `/court/camera-view` API endpoints.

## Files Created

- `apps/api/routers/court.py`
- `apps/api/services/camera_view_evidence.py`
- `docs/court/camera_view_evidence_layer_v0.md`
- `docs/milestones/milestone_8c_camera_view_evidence_layer.md`
- `docs/handoffs/milestone_8c_camera_view_evidence_layer_handoff.md`
- `docs/agent_reports/milestone_8c_camera_view_evidence_layer_report.md`
- `tests/test_camera_view_evidence.py`

## Files Modified

- `README.md`
- `apps/api/main.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OBSERVATION_CONTRACT.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`
- `docs/court/court_evidence_schema_v0.md`
- `docs/court/fixture_court_evidence_adapter_v0.md`
- `packages/schema/tom_v3_schema/court.py`

## Camera / View Query Decisions

The query layer is read-only and consumes existing `camera_view_observation` rows. It requires `media_id` and supports optional filters for run, time range, frame range, view label, camera motion hint, minimum confidence, limit, and offset.

## Summary Read Model Decisions

The summary reports observation count, label counts, motion hint counts, frame/time range, mean confidence, mean stability, max cut likelihood, and candidate-only homography context hints. It does not compute or validate homography.

## Evidence Bundle Decisions

The bundle includes observation spine, typed camera/view detail, media context, processing run context, runtime config, model registry, lineage, artifacts, annotations, annotation summary, and evidence-only warnings.

## API / CLI Decisions

8C adds backend API endpoints under `/court/camera-view`. It does not add a CLI summary command because the service/API path is sufficient for the milestone and avoids duplicating read-model surface area.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- fixture demo and completion audit smoke
- `run-fixture-court` smoke against the fixture demo media
- `run-fixture-court --plan-only`
- API smoke for `/court/camera-view`, `/court/camera-view/summary`, and `/court/camera-view/{observation_id}/bundle`

## Validation Results

- Python tests: passed, `224 passed`.
- Ruff: passed.
- Web lint/build/audit: passed, `0 vulnerabilities`.
- Alembic smoke: passed through `0003_court_evidence_observations`.
- Synthetic viewer smoke: passed.
- Fixture demo: passed with `demo_assets/sample_point.mp4`.
- Completion audit: passed after the fixture demo.
- Court fixture smoke: passed for media `0a2ea19b-9908-4e30-8bcf-23c17b635cfe`, producing 8 `court_keypoint_observation`, 8 `court_line_observation`, and 8 `camera_view_observation` rows.
- API smoke: passed for court run `a26edb80-4394-41ad-8e4c-41c4fbffeed0`; query returned 8 camera/view rows, summary counted 8 `broadcast_hardcam` / `stable` rows, and bundle returned the selected camera/view evidence with evidence-only warnings.

## Known Limitations

- Camera/view evidence is fixture evidence in the default path.
- The read model provides context hints only; it does not decide homography eligibility.
- No replay court overlay exists yet.
- No real camera/view model exists yet.

## Non-Goals Preserved

8C does not add homography computation, projection diagnostics, replay court overlays, real camera/court inference, ball/player court projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Handoff

Milestone 8D - Homography Candidate Persistence.
