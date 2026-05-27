# Milestone 8D Agent Report - Homography Candidate Persistence

## Summary

Milestone 8D adds homography candidate persistence for Blueprint 8. TOM can now consume persisted fixture court keypoint, court line, and camera/view evidence, compute candidate image-pixels-to-court-template transforms, persist `homography_candidate_observation` rows, and preserve lineage back to the source geometry evidence.

## Files Created

- `apps/worker/services/homography_candidate_builder.py`
- `docs/court/homography_candidate_persistence_v0.md`
- `docs/milestones/milestone_8d_homography_candidate_persistence.md`
- `docs/handoffs/milestone_8d_homography_candidate_persistence_handoff.md`
- `docs/agent_reports/milestone_8d_homography_candidate_persistence_report.md`
- `tests/test_homography_candidate_builder.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
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
- `docs/court/camera_view_evidence_layer_v0.md`
- `docs/court/court_evidence_schema_v0.md`
- `docs/court/fixture_court_evidence_adapter_v0.md`

## Homography Candidate Builder Decisions

The builder reads `court_keypoint_observation` rows from a source court run, finds optional same-frame court line and camera/view rows, creates model/runtime/run/step provenance, persists `homography_candidate_observation` rows through `ObservationWriter`, and writes source evidence lineage.

## Matrix Computation Decisions

The v0 matrix method is a lightweight axis-aligned affine fit from image pixels to `tennis_court_template_normalized_v0`. It requires at least four usable source keypoints and stores reprojection metrics, source counts, template metadata, matrix direction, inverse matrix, and confidence. The method is suitable for deterministic fixture geometry and is explicitly candidate evidence, not court truth.

## Source Evidence / Lineage Decisions

Each candidate links to the source court keypoint observation. When available, it also links to same-frame court line and camera/view observations. Lineage uses `homography_from_court_keypoints_candidate`, `homography_from_court_lines_candidate`, and `camera_context_for_homography_candidate`.

## Persistence Decisions

Homography candidates use the existing observation spine with `observation_family = court`, `observation_type = homography_candidate_observation`, media-owned frame/time, `coordinate_space = court_template_2d`, and geometry-evidence-only payload metadata. No parallel geometry store was added.

## CLI / Makefile Decisions

8D adds worker CLI `build-homography-candidates` and Makefile `homography-candidates`. Both support the source media id and court run id; the CLI also supports frame filtering, minimum keypoint confidence, viewer base URL, and plan-only mode.

## Tests Run

- `.venv/bin/python -m pytest tests/test_homography_candidate_builder.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- fixture demo and completion audit smoke
- `run-fixture-court` smoke against the fixture demo media
- `build-homography-candidates --plan-only`
- `build-homography-candidates` smoke against the fixture court run

## Validation Results

- Focused homography tests: passed, `7 passed`.
- Full Python tests: passed, `231 passed`.
- Ruff: passed.
- Web lint/build/audit: passed, `0 vulnerabilities`.
- Alembic smoke: passed through `0003_court_evidence_observations`.
- Synthetic viewer smoke: passed.
- Fixture demo: passed with `demo_assets/sample_point.mp4`, media `75094c0a-fd5e-4ff5-b148-51fe65092be0`.
- Completion audit: passed after the fixture demo.
- Court fixture smoke: passed for court run `beaae410-5371-4ede-b7da-eff5ee0c323f`, producing 8 `court_keypoint_observation`, 8 `court_line_observation`, and 8 `camera_view_observation` rows.
- Homography plan-only smoke: passed.
- Homography candidate smoke: passed for homography run `bd96ecff-7af7-4fe1-b8d0-137359b457a7`, producing 8 `homography_candidate_observation` rows with 8 keypoint, 8 line, and 8 camera/view source counts.

## Known Limitations

- The v0 builder is designed for fixture court evidence and is not a real court model.
- Homography candidates are not replayed visually yet.
- Projection diagnostics are not created yet.
- Ball/player court-space projection is not implemented.

## Non-Goals Preserved

8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Branch `codex/m8d-homography-candidate-persistence` and tag `tom-v3-m8d-homography-candidate-persistence` pushed after final validation.

## Recommended Next Handoff

Milestone 8E - Court Overlay in Replay Workstation.
