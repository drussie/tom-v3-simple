# Milestone 0C Agent Report - Worker + Rich Synthetic Observation Seeder

## Summary

Status: complete.

Milestone 0C implemented the first worker CLI and rich shared synthetic observation seeder for TOM v3 Simple. The seeded baseline data is designed to feed the future visual evidence viewer without adding real ML or frontend code.

## Files Created

- `apps/worker/__init__.py`
- `apps/worker/config.py`
- `apps/worker/main.py`
- `apps/worker/cli.py`
- `apps/worker/pipelines/__init__.py`
- `apps/worker/pipelines/synthetic_seed.py`
- `apps/worker/scenarios/__init__.py`
- `apps/worker/scenarios/baseline_tennis_clip.py`
- `apps/worker/services/__init__.py`
- `apps/worker/services/media_builder.py`
- `apps/worker/services/run_builder.py`
- `tests/test_worker_synthetic.py`
- `docs/milestones/milestone_0c_worker_synthetic_observation_seeder.md`
- `docs/handoffs/milestone_0c_worker_synthetic_observation_seeder_handoff.md`
- `docs/worker/synthetic_seeder_v0.md`
- `docs/worker/synthetic_scenario_baseline_v0.md`

## Files Modified

- `README.md`
- `apps/worker/README.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/milestones/milestone_0_observation_store_visual_foundation.md`
- `docs/api/backend_api_v0.md`
- `packages/observations/tom_v3_observations/synthetic.py`
- `pyproject.toml`
- `tests/test_backend_api.py`

## Worker Decisions

- The worker CLI lives in `apps/worker/cli.py`.
- `seed-synthetic-run` creates local database tables by default for development smoke tests.
- `verify-synthetic-run` checks seeded evidence counts and returns structured JSON.
- The default seed behavior creates a new processing run each time.

## Synthetic Scenario Decisions

- The baseline scenario is named `baseline-tennis-clip`.
- The scenario does not require a real video file.
- The scenario creates pipeline steps that describe synthetic structure without real model work.
- The API dev route and worker CLI share `packages/observations/tom_v3_observations/synthetic.py`.

## Observation/Missingness Decisions

- Gameplay, non_gameplay, and uncertain bands are persisted as gameplay observations.
- Ball, near-player, and far-player tracks have tracklets and track points.
- Track gaps are represented in tracklet coverage metadata and as a derived tracking_gap_candidate.
- Homography is represented with atomic `homography_placeholder` observations because typed homography tables do not exist yet.
- Low confidence is represented on ball observations and track point payloads.

## Lineage/Artifact Decisions

- bounce_candidate has lineage to ball observations, a gameplay segment, and a homography placeholder.
- tracking_gap_candidate has lineage to ball observations before and after the gap and a gameplay segment.
- hit_candidate has lineage to ball, near-player, and far-player observations.
- Placeholder artifacts use `file:///dev/artifacts/synthetic/...` URIs.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db .venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db .venv/bin/python -m apps.worker.cli verify-synthetic-run --run-id <run_id>`
- `find docs -maxdepth 3 -type f | sort`
- `git status --short`

## Validation Results

- Pytest passed: 6 tests.
- Ruff passed.
- Alembic upgrade smoke test passed against SQLite.
- Worker CLI seed and verify smoke test passed.
- CLI verifier returned `ok: true`.

## Known Gaps

- No real media file is used.
- No actual artifact files are generated.
- No real homography calculation exists.
- No real tracking exists.
- No frontend viewer exists yet.
- Postgres integration tests remain future work.

## Non-goals Preserved

- No YOLO integration was added.
- No TOM v1 integration was added.
- No real video decoding was added.
- No real bounce detection was added.
- No real player tracking was added.
- No frontend evidence viewer was added.
- No adjudication system was added.

## Recommended Next Handoff

Milestone 0D - Visual Evidence Viewer Foundation.

The next agent should build the first viewer against this seeded data using existing API/query/detail/lineage/artifact contracts.
