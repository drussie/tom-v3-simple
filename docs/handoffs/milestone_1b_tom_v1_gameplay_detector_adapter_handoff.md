# TOM v3 Simple - Milestone 1B Handoff

## Summary

Milestone 1B adds the gameplay adapter seam and the first persisted gameplay/view-state adapter path.

TOM v1 portable source/assets were not available in this repo/environment, so the milestone uses:

- `BaseGameplayAdapter` as the TOM v3 contract
- `FixtureGameplayAdapter` for deterministic dev/test output
- `TomV1GameplayAdapter` as a clear integration stub
- worker service and CLI commands that persist gameplay observations through `ObservationWriter`

## Implemented

- `packages/model_adapters/tom_v3_model_adapters/gameplay.py`
- `apps/worker/services/gameplay_adapter.py`
- `python -m apps.worker.cli run-gameplay-adapter`
- `python -m apps.worker.cli index-and-run-gameplay`
- tests in `tests/test_gameplay_adapter.py`
- model adapter docs and TOM v1 portability assessment

## Core Contract

Gameplay classification is an observation.

Each gameplay segment writes:

- `observation_family=gameplay`
- `observation_type=view_state`
- `granularity=frame_range`
- media/run/model/config ids
- frame and timestamp ranges
- confidence
- typed `gameplay_observation`

Media indexing owns frame/time. The fixture adapter derives timestamps from indexed media FPS using TOM v3 video utilities.

## Worker Commands

Run adapter on indexed media:

```bash
python -m apps.worker.cli run-gameplay-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

Index and run:

```bash
python -m apps.worker.cli index-and-run-gameplay \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

The command output includes `run_id`, which can be opened in the existing viewer:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

## TOM v1 Integration Status

Real TOM v1 integration remains blocked until a portable source path, weights, preprocessing contract, and callable entrypoint are supplied.

See:

```text
docs/model_adapters/tom_v1_gameplay_adapter_assessment.md
```

## Recommended Next Handoff

Milestone 1C - YOLO26 Ball/Player Observation Adapter.

If TOM v1 assets become available first, an alternate handoff can complete `TomV1GameplayAdapter.run()` without changing the TOM v3 persistence contract.
