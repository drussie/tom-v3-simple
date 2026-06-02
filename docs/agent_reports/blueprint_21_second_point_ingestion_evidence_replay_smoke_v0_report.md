# Blueprint 21 Second Point Ingestion / Evidence Replay Smoke v0 Report

Status: implemented

Branch: `codex/blueprint-21-second-point-ingestion-evidence-replay-smoke-v0`

## Summary

Blueprint 21 adds a controlled second-point ingestion and replay smoke path. It validates a local
media path, indexes the media through the existing TOM v3 media indexing path, and returns a Replay
Workstation URL for that new media asset.

This milestone does not run or change event candidate logic, marker arbitration, 3D candidate
generation, 3D diagnostics, review annotations, truth, in/out, score, or adjudication.

## Created

- `apps/worker/services/second_point_smoke.py`
- `tests/test_second_point_smoke.py`
- `docs/blueprints/blueprint_21_second_point_ingestion_evidence_replay_smoke_v0.md`
- `docs/reviews/second_point_ingestion_smoke_v0.md`
- `docs/agent_reports/blueprint_21_second_point_ingestion_evidence_replay_smoke_v0_report.md`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`

## CLI / Make Helper

Added CLI command:

```text
python -m apps.worker.cli ingest-second-point-smoke
```

Added Make target:

```text
make tom-v1-ingest-second-point-smoke
```

The command returns clear `ok:false` statuses for missing or nonexistent media paths:

- `missing_second_point_media_path`
- `second_point_media_path_not_found`

## Replay Behavior

The smoke output includes a Replay Workstation URL for the indexed media. A second point with no
event candidates or 3D candidates is valid for Blueprint 21; replay read models return empty
candidate lists and no selected 3D debug run instead of failing.

## Local Smoke

No distinct second-point video was supplied in this handoff, so the local command smoke used the
available `demo_assets/sample_point.mp4` path as a stand-in media file for command validation only.
This does not claim that a real second tennis point has been reviewed.

Smoke result:

- `media_id`: `2a26f0f9-03c2-4a6b-9337-7308bb07c242`
- `replay_url`: `http://127.0.0.1:3000/replay/2a26f0f9-03c2-4a6b-9337-7308bb07c242`
- `duration_ms`: 7133
- `frame_count`: 214
- `fps`: 30.0
- `width`: 1920
- `height`: 1080
- `not_truth`: true
- `not_generalization_claim`: true
- `does_not_change_sample_point`: true

The focused replay read-model test covers a newly indexed media asset with no event candidates and
no 3D candidates.

## sample_point Gate

The protected `sample_point` baseline gate still passes:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

## Boundaries Preserved

- no event candidate logic changes
- no marker arbitration changes
- no hit/bounce generation changes
- no 3D candidate generation changes
- no 3D diagnostic generation changes
- no `sample_point` baseline mutation
- no truth/in-out/score/adjudication
- no multi-point generalization claim

## Validation

Focused tests:

```text
.venv/bin/python -m pytest tests/test_second_point_smoke.py -q
4 passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
388 passed

ruff check .
passed

git diff --check
passed

cd apps/web && npm run lint
passed

cd apps/web && npm run build
passed

cd apps/web && npm audit --omit=dev
found 0 vulnerabilities
```

Fixture demo and audit:

```text
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_21_second_point_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_21_second_point_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
