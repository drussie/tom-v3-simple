# TOM v3 Simple - Milestone 1B Agent Report

## Summary

Status: complete.

Milestone 1B implements the TOM v3 gameplay adapter interface, fixture adapter, TOM v1 integration stub, worker gameplay adapter service, CLI commands, persistence tests, and documentation. The fixture adapter writes gameplay, non_gameplay, and uncertain observations through the existing `ObservationWriter` and the existing viewer can load those observations.

## Files Created

- `apps/worker/services/gameplay_adapter.py`
- `docs/agent_reports/milestone_1b_tom_v1_gameplay_detector_adapter_report.md`
- `docs/handoffs/milestone_1b_tom_v1_gameplay_detector_adapter_handoff.md`
- `docs/milestones/milestone_1b_tom_v1_gameplay_detector_adapter.md`
- `docs/model_adapters/gameplay_adapter_v0.md`
- `docs/model_adapters/tom_v1_gameplay_adapter_assessment.md`
- `packages/model_adapters/README.md`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `packages/model_adapters/tom_v3_model_adapters/gameplay.py`
- `tests/test_gameplay_adapter.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/dev/local_demo_runbook.md`
- `docs/media/media_indexing_v0.md`
- `pyproject.toml`

## TOM v1 Portability Assessment

Portable TOM v1 detector source, weights, preprocessing code, and callable entrypoint were not available in this repo/environment.

Milestone 1B therefore does not claim real TOM v1 inference. It adds `TomV1GameplayAdapter` as an explicit unavailable stub and documents the future integration requirements.

## Adapter Interface Decisions

The adapter seam lives in `tom_v3_model_adapters.gameplay`.

The interface is intentionally small:

- `GameplayAdapterInput`
- `GameplaySegmentObservation`
- `GameplayAdapterResult`
- `BaseGameplayAdapter`

Adapter output is segment evidence only. Persistence remains owned by TOM v3 worker services and `ObservationWriter`.

## Fixture Adapter Decisions

The fixture adapter deterministically maps indexed frame count into:

- gameplay
- non_gameplay
- uncertain
- gameplay

It exists for tests and development and is clearly marked as fixture output, not real gameplay classification.

## Persistence Decisions

The gameplay adapter service creates:

- `runtime_config`
- `model_registry`
- `processing_run`
- `processing_step`
- `observation`
- `gameplay_observation`

The current lineage table links child observations to parent observations. Gameplay segments have no parent observation yet, so media/run/model/config provenance is stored on the observation spine and processing step provenance is stored in observation payload metadata.

## Worker / API Decisions

Worker commands were added:

- `run-gameplay-adapter`
- `index-and-run-gameplay`

No API endpoint was added in 1B. Gameplay runs are worker-driven for now, using the same service the API could call later.

## Tests Run

Passed:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `npm run lint` in `apps/web`
- `npm run build` in `apps/web`
- `npm audit --omit=dev` in `apps/web`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- generated a temporary 1-second MP4 with ffmpeg and ran `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_gameplay_adapter.db .venv/bin/python -m apps.worker.cli index-media --source-path tmp_gameplay_smoke/sample.mp4 --storage-root .data/media`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_gameplay_adapter.db .venv/bin/python -m apps.worker.cli run-gameplay-adapter --media-id 8e6aaeaa-6a46-493e-9350-ed4d06b0e70b --adapter fixture --output-debug-artifact`
- inspected `build_viewer_run_payload` for run `784921ff-be6e-48c9-ba39-e506249127bd`

## Validation Results

- Backend tests: 24 passed.
- Ruff: passed.
- Web lint/build/audit: passed with 0 production dependency vulnerabilities.
- Alembic SQLite smoke test: passed.
- Synthetic viewer smoke: passed.
- Real media indexing smoke: passed.
- Fixture gameplay adapter smoke: passed.
- Viewer payload inspection returned gameplay states `gameplay`, `non_gameplay`, `uncertain`, `gameplay` and 4 debug artifact metadata rows.

## Known Limitations

- Real TOM v1 integration is not complete because portable assets/source are unavailable.
- Fixture output is deterministic and metadata-driven; it is not model inference.
- No API trigger was added for gameplay runs.
- No debug artifacts are written unless `--output-debug-artifact` is used.
- No YOLO, tracking, pose, homography, or bounce logic is present.

## Non-Goals Preserved

- No YOLO integration.
- No ball tracking.
- No player tracking.
- No pose tracking.
- No court homography.
- No bounce detection.
- No point/rally reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.

## Recommended Next Handoff

Milestone 1C - YOLO26 Ball/Player Observation Adapter.

Reason: the repo now has real media indexing and a first adapter pattern for persisting model-output observations. The next useful adapter can write ball/player detections as atomic observations while keeping gameplay/view-state observations as processing scope evidence.
