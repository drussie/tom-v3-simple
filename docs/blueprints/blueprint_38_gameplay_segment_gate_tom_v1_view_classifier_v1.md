# Blueprint 38 - Gameplay Segment Gate / TOM v1 View Classifier Integration v1

Status: implemented.

Blueprint 38 adds a gameplay observation suitability gate around the existing local TOM v1
gameplay classifier asset. The gate records classifier asset provenance, exports a durable
contract, builds candidate gameplay/non-gameplay segment artifacts from explicit media input, and
emits a replay-visible timeline structure for future downstream gating.

## Scope

Blueprint 38 proves:

```text
explicit media path
-> local TOM v1 gameplay classifier asset provenance
-> frame/window gameplay suitability candidates
-> temporal smoothing / hysteresis
-> gameplay segment candidates
-> replay timeline lane artifact
-> structural downstream gate statuses
```

The tracked contract lives at:

```text
.data/contracts/gameplay_segment_gate_contract_v1.json
```

Generated local exports live at:

```text
.data/exports/gameplay_classifier_asset_inspection.current.json
.data/exports/gameplay_segment_candidates.current.json
.data/exports/gameplay_segment_candidates.validation.json
.data/exports/gameplay_segment_report.current.json
```

## Commands

```bash
make tom-v1-export-gameplay-segment-gate-contract PYTHON=.venv/bin/python
make tom-v1-inspect-gameplay-classifier-asset PYTHON=.venv/bin/python
make tom-v1-build-gameplay-segment-candidates \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_MEDIA_PATH=demo_assets/sample_point.mp4 \
  GAMEPLAY_SEGMENT_MEDIA_ID=sample_point_gameplay_segment_gate_smoke
make tom-v1-validate-gameplay-segment-candidates \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_CANDIDATES=.data/exports/gameplay_segment_candidates.current.json
make tom-v1-build-gameplay-segment-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_CANDIDATES=.data/exports/gameplay_segment_candidates.current.json
```

## Boundary

This is a gameplay observation suitability gate only. It uses candidate/evidence language and
structural downstream gate statuses such as `allowed_for_downstream_observation`,
`blocked_from_downstream_observation`, and `requires_human_review`.

Blueprint 38 does not decide tennis truth, in/out, score, point winner, player identity, rally
state, server/receiver state, line-call truth, point truth, event truth, marker arbitration,
accepted/rejected lifecycle, coaching/tactical conclusions, betting/prediction outcomes,
generalization, automatic correctness, training truth, production truth, or adjudication. It does
not mutate model assets, commit weights, silently ingest media, auto-discover media folders, run
detections, build tracklets, run pose/court/3D jobs, or mutate protected regression baselines.
