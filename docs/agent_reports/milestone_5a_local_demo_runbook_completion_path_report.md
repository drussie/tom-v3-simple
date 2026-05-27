# Milestone 5A Agent Report - Local Demo / Runbook Completion Path

## Summary

Milestone 5A starts Blueprint 5 by adding a canonical local fixture demo path for TOM v3 Simple.

The demo is repeatable in the base environment and does not require YOLO weights, real pose weights, GPU runtime, or network access. It indexes media, creates fixture gameplay and detection evidence, extracts frame artifacts, builds candidate tracklets, creates fixture pose observations, seeds small review annotations, exports pose and tracklet review datasets, and prints IDs, counts, export paths, warnings, and viewer URLs.

## Files Created

- `apps/worker/services/local_demo.py`
- `tests/test_local_demo.py`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_5_simple_completion_product_hardening.md`
- `docs/milestones/milestone_5a_local_demo_runbook_completion_path.md`
- `docs/handoffs/milestone_5a_local_demo_runbook_completion_path_handoff.md`
- `docs/agent_reports/milestone_5a_local_demo_runbook_completion_path_report.md`

## Files Modified

- `Makefile`
- `apps/worker/cli.py`
- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/dev/local_demo_runbook.md`
- `docs/blueprints/tom_v3_blueprint_4_completion_review.md`

## Demo Orchestration Decisions

The implementation uses a lightweight Python service, `run_local_fixture_demo`, rather than a large shell script. The service calls existing TOM v3 worker/API services so the demo uses the same persistence contracts as normal local workflows.

The user-facing path is:

```bash
make demo
```

The direct worker path is:

```bash
python -m apps.worker.cli run-demo
```

## Media Fallback Decisions

The demo resolves media in this order:

1. explicit `--source-path` or `DEMO_MEDIA_PATH`
2. `demo_assets/tennis_fixture.mp4`
3. generated `.data/demo/media/synthetic_demo_media.mp4`

Generated media is explicitly marked as synthetic demo media. It is a placeholder for proving persistence, viewer, lineage, review, and export plumbing.

## Annotation And Export Decisions

The demo seeds three review annotations:

- one detection review annotation
- one tracklet review annotation
- one pose keypoint review annotation

All are marked with:

```text
created_by = tom-v3-demo
```

They do not mutate observations.

The demo exports:

- pose review dataset
- tracklet review dataset

Both create local JSON outputs and persisted evidence artifact metadata.

## Makefile / CLI Decisions

The Makefile now includes:

- `demo`
- `demo-fixture`
- `demo-plan`
- `demo-reset`
- `demo-export`
- `demo-open`
- `completion-check`
- `yolo-probe`
- `yolo-smoke`

`demo-reset` is intentionally non-destructive. It prints safe guidance instead of deleting database rows or arbitrary local artifacts.

## Runbook Decisions

`docs/RUNBOOK_LOCAL.md` is now the canonical local runbook. The older `docs/dev/local_demo_runbook.md` points to the canonical runbook and keeps historical milestone-specific notes.

## Tests Run

- `pytest tests/test_local_demo.py -q`
- `ruff check apps/worker/services/local_demo.py apps/worker/cli.py tests/test_local_demo.py --fix`
- `python -m apps.worker.cli run-demo --plan-only`
- `make demo-plan PYTHON=.venv/bin/python`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5a_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `pytest -q`
- `ruff check .`
- `python scripts/smoke_synthetic_viewer_data.py`
- `make yolo-probe PYTHON=.venv/bin/python`
- `make yolo-smoke PYTHON=.venv/bin/python`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`

## Validation Results

- Focused local demo tests: passed, `3 passed`.
- Full Python suite: passed, `150 passed`.
- Ruff: passed.
- Synthetic viewer smoke: passed.
- Demo plan: passed.
- Fixture demo smoke: passed with generated synthetic media, fixture gameplay/detection/tracklet/pose runs, seeded review annotations, pose review export, tracklet review export, and viewer URLs.
- YOLO runtime probe: passed with safe unavailable diagnostics in the base environment.
- YOLO smoke plan: passed in plan-only mode.
- Web lint: passed.
- Web build: passed.
- Web audit: passed, `0 vulnerabilities`.
- Alembic smoke: passed against `tmp_migration_check.db`.

## Known Limitations

- The fixture demo proves product plumbing, not real tennis understanding.
- Generated synthetic media is a placeholder when no local video is supplied.
- Real YOLO smoke remains optional and locally gated.
- Real pose inference is not implemented.
- `demo-reset` is non-destructive by design.

## Non-goals Preserved

Milestone 5A did not add:

- real pose inference
- movement interpretation
- stroke classification
- serve detection
- hit detection
- bounce detection
- rally or point reconstruction
- scoring
- homography
- adjudication
- production streaming
- auth
- cloud deployment
- multi-camera reasoning

## Recommended Next Handoff

Milestone 5B - Viewer / Product Polish
