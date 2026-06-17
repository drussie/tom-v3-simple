# Blueprint 22 Second Point Evidence Parity / Protected Baseline Gate v0 Report

Status: implemented

Branch: `codex/blueprint-22-second-point-evidence-parity-baseline-gate-v0`

## Summary

Blueprint 22 adds a controlled second-point evidence parity command. It validates and indexes one
operator-provided local media file, returns a Replay Workstation URL, records which evidence layers
exist for that media asset, and writes a local baseline manifest for the second-point evidence
profile.

This milestone does not run or change event candidate logic, marker arbitration, 3D candidate
generation, 3D diagnostics, review annotations, truth, in/out, score, or adjudication.

## Created

- `apps/worker/services/second_point_evidence_parity.py`
- `tests/test_second_point_evidence_parity.py`
- `docs/blueprints/blueprint_22_second_point_evidence_parity_baseline_gate_v0.md`
- `docs/reviews/second_point_evidence_parity_v0.md`
- `docs/agent_reports/blueprint_22_second_point_evidence_parity_baseline_gate_v0_report.md`

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
python -m apps.worker.cli build-second-point-evidence-parity
```

Added Make target:

```text
make tom-v1-build-second-point-evidence-parity
```

The command returns clear `ok:false` statuses for missing or nonexistent media paths:

- `missing_second_point_media_path`
- `second_point_media_path_not_found`

## Manifest

Default output:

```text
.data/baselines/second_point_evidence_parity.baseline_manifest.json
```

The manifest is generated local evidence metadata and should not be committed.

## Local Smoke

No distinct second-point video was supplied in this handoff. Command validation used the available
`demo_assets/sample_point.mp4` path as a stand-in media file only. This does not claim that a real
second tennis point has been reviewed or that TOM has generalized.

Smoke result:

- `media_id`: `082abb50-5348-4069-98a1-0458b4560e9a`
- `replay_url`: `http://127.0.0.1:3000/replay/082abb50-5348-4069-98a1-0458b4560e9a`
- `manifest_output`: `.data/baselines/second_point_evidence_parity.baseline_manifest.json`
- `event_candidates_available`: false
- `trajectory_3d_candidates_available`: false
- `review_annotations_available`: false

## Protected sample_point Gate

The protected `sample_point` baseline gate must still pass:

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

```text
.venv/bin/python -m pytest tests/test_second_point_evidence_parity.py tests/test_second_point_smoke.py -q
10 passed

.venv/bin/python -m pytest -q
394 passed

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
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_22_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_22_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
