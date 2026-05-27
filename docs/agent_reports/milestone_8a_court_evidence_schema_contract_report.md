# Milestone 8A Agent Report - Court Evidence Schema / Contract

## Summary

Milestone 8A starts Blueprint 8 by adding the foundational court/camera/homography evidence schema contract. It implements typed schema models, a normalized court template registry, storage models, an Alembic migration, observation writer support, lineage relationship constants, tests, and docs.

## Files Created

- `packages/schema/tom_v3_schema/court.py`
- `migrations/versions/0003_court_evidence_observations.py`
- `tests/test_court_schema.py`
- `tests/test_court_observation_persistence.py`
- `docs/court/court_evidence_schema_v0.md`
- `docs/court/court_template_registry_v0.md`
- `docs/milestones/milestone_8a_court_evidence_schema_contract.md`
- `docs/handoffs/milestone_8a_court_evidence_schema_contract_handoff.md`
- `docs/agent_reports/milestone_8a_court_evidence_schema_contract_report.md`

## Files Modified

- `packages/schema/tom_v3_schema/enums.py`
- `packages/schema/tom_v3_schema/observations.py`
- `packages/storage/tom_v3_storage/db_models.py`
- `packages/observations/tom_v3_observations/writer.py`
- `README.md`
- `docs/CONTROL_ROOM.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CURRENT_STATE.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OBSERVATION_CONTRACT.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`
- `docs/court/court_homography_evidence_decision_v0.md`

## Court Schema Decisions

All court/camera/homography evidence uses `observation_family = court` and one of five typed observation types: court keypoint, court line, camera/view, homography candidate, or projection diagnostic.

Each typed observation preserves media-owned frame/time and records `frame_time_owner = media_indexing`, `observation_only = true`, `no_adjudication = true`, and `geometry_evidence_only = true`.

## Court Template Registry Decisions

8A adds `tennis_court_template_normalized_v0` in `court_template_2d` coordinates. The template is normalized and versioned. Real court dimensions are deferred to a future template version.

## Storage / Migration Decisions

Migration `0003_court_evidence_observations` creates:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

Each table links back to the canonical `observation` spine row and uses existing media/run/model/runtime references.

## Lineage Decisions

8A adds relationship constants for:

- `homography_from_court_keypoints_candidate`
- `homography_from_court_lines_candidate`
- `camera_context_for_homography_candidate`
- `projection_diagnostic_for_homography_candidate`

Tests persist fake source court evidence, homography candidates, projection diagnostics, and lineage rows.

## Audit / Provenance Decisions

8A documents provenance expectations rather than expanding the completion audit runtime. Court evidence provenance uses existing observation spine rows, typed detail tables, lineage rows, artifacts, and generic annotations.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Fixture demo with `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4`
- Fixture completion audit on `tmp_tom_v3_8a_fixture_demo.db`

## Validation Results

- Python tests: passed, 212 tests.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: passed, 0 vulnerabilities.
- Alembic smoke: passed, including `0003_court_evidence_observations`.
- Synthetic viewer smoke: passed.
- Fixture demo: passed.
- Completion audit: passed.

## Known Limitations

- No court model adapter exists yet.
- No homography computation exists yet.
- No replay court overlay exists yet.
- Projection diagnostics do not project ball/player detections into court space.
- Court evidence remains candidate geometry evidence only.

## Non-goals Preserved

8A adds no court runtime, replay court overlay, homography computation, ball/player court projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Prepared for final commit, tag, and push on `codex/m8a-court-evidence-schema-contract`. The final response records the exact commit SHA, tag, and remote push confirmation.

## Recommended Next Handoff

Milestone 8B - Court Keypoint / Line Evidence Adapter.
