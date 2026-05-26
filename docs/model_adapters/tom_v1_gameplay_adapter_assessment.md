# TOM v3 Simple - TOM v1 Gameplay Adapter Assessment

## Summary

Status: portable TOM v1 integration is not available in this repo/environment.

Milestone 1B therefore implements:

- a TOM v3 gameplay adapter interface
- a deterministic fixture adapter for tests and development
- a `TomV1GameplayAdapter` integration stub with a clear unavailable error
- docs describing the integration path once TOM v1 source/assets are supplied

It does not claim that the real TOM v1 gameplay detector is running.

## Where Is The TOM v1 Gameplay Detector Located?

Not located in `drussie/tom-v3-simple`.

Local search found no TOM v1 gameplay detector source, weights, or callable entrypoint in the TOM v3 repo. Nearby tennis-analysis directories exist on the workstation, but they do not expose the TOM v1 gameplay/not-gameplay detector described by the TOM v3 blueprint.

## What Inputs Does It Need?

Unknown from the available repo state.

The TOM v3 adapter expects the future TOM v1 wrapper to accept at least:

- local video path or frame/window input
- FPS
- frame count
- duration
- frame/time summary owned by TOM v3 media indexing
- runtime config values such as window and stride

## What Outputs Does It Produce?

Unknown from the available repo state.

The TOM v3 contract requires output to be convertible to segment rows:

- `gameplay`
- `non_gameplay`
- `uncertain`

Each segment must include frame range, timestamp range, confidence, optional subtype, and metadata.

## Does It Require TOM v1 Database Or Pipeline State?

Unknown. No portable TOM v1 code was available to inspect.

If the detector requires TOM v1 database state or pipeline globals, it should not be imported directly into TOM v3. The preferred integration would be a small TOM v1-side CLI or function that emits TOM v3-compatible segment JSON.

## Does It Need Model Weights?

Unknown. No TOM v1 weights were available in this repo/environment.

If weights are required, their path/version/checksum should be recorded in `model_registry.metadata_jsonb`.

## Are Those Weights Available?

No TOM v1 gameplay detector weights were found during this milestone.

## Can It Be Called As A Function?

Not currently. No function entrypoint is available in this repo/environment.

## Can It Be Called As A CLI/Subprocess?

Not currently. No stable TOM v1 gameplay detector CLI is available in this repo/environment.

## What Preprocessing Does It Require?

Unknown.

Future integration must document preprocessing, including:

- frame sampling
- resizing
- color conversion
- temporal windowing
- smoothing
- confidence thresholds

Those values should be captured in `runtime_config.payload_jsonb`.

## Recommended Integration Mode

Keep TOM v3 stable and narrow:

```text
TOM v3 GameplayAdapter interface
-> TOM v1 portable function or CLI
-> segment JSON
-> ObservationWriter
-> gameplay_observation rows
```

Do not import broad TOM v1 pipeline state into TOM v3.

When TOM v1 assets are supplied, implement `TomV1GameplayAdapter.run()` so it maps TOM v1 output into `GameplaySegmentObservation` values and preserves TOM v3 media frame/time ownership.

## Current Developer Path

Use the fixture adapter:

```bash
python -m apps.worker.cli run-gameplay-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

The fixture path proves persistence and viewer compatibility without representing itself as real gameplay classification.
