# TOM v3 Simple - Gameplay Adapter v0

## Purpose

Gameplay Adapter v0 is the first model-adapter seam for TOM v3 Simple.

It turns adapter output into persisted `gameplay_observation` rows:

```text
indexed media_asset
-> gameplay adapter
-> gameplay / non_gameplay / uncertain segments
-> ObservationWriter
-> viewer gameplay timeline band
```

Gameplay classification is an observation. It is not adjudication.

## Package

Adapter interface:

```text
packages/model_adapters/tom_v3_model_adapters/gameplay.py
```

Worker persistence service:

```text
apps/worker/services/gameplay_adapter.py
```

## Adapter Contract

Primary classes:

- `GameplayAdapterInput`
- `GameplaySegmentObservation`
- `GameplayAdapterResult`
- `BaseGameplayAdapter`
- `FixtureGameplayAdapter`
- `TomV1GameplayAdapter`

Adapter input includes:

- media id
- source URI
- local path when available
- FPS
- frame count
- duration
- runtime config payload
- frame/time summary from media indexing

Adapter output includes:

- adapter name and version
- segment observations
- optional artifact metadata
- diagnostics

## Frame/Time Rule

Media indexing owns frame/time.

Gameplay adapters must use the indexed media FPS, frame count, duration, and frame/time summary. Segment timestamps must be derived from TOM v3 media metadata and `tom_v3_video.time_index` helpers.

## Fixture Adapter

`FixtureGameplayAdapter` is deterministic and development-only.

For indexed media with a frame count, it emits:

- gameplay: first 30 percent of the indexed frames
- non_gameplay: 30-40 percent
- uncertain: 40-45 percent
- gameplay: 45-90 percent

It is used for tests, local smoke validation, and viewer compatibility before a portable TOM v1 detector is available.

## TOM v1 Adapter Stub

`TomV1GameplayAdapter` exists behind the same interface but intentionally raises a clear unavailable error in this repo state.

The TOM v1 source, weights, preprocessing, and callable entrypoint are not present in the TOM v3 repo/environment, so 1B does not pretend to run the real TOM v1 detector.

See:

```text
docs/model_adapters/tom_v1_gameplay_adapter_assessment.md
```

## Persistence

The worker service creates:

- `runtime_config`
- `model_registry`
- `processing_run`
- `processing_step`
- one `observation` row per segment
- one typed `gameplay_observation` row per segment

Each observation stores:

- media id
- run id
- model id
- runtime config id
- frame range
- timestamp range
- confidence
- adapter metadata
- processing step id in payload metadata

The current lineage table links observations to parent observations. Gameplay adapter segments have no parent observation yet, so run/model/config/step provenance is stored on the observation spine and payload.

## Worker Commands

Run the fixture adapter for an indexed media asset:

```bash
python -m apps.worker.cli run-gameplay-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

Index a local file and run the adapter:

```bash
python -m apps.worker.cli index-and-run-gameplay \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

The command prints:

- media id
- run id
- model id
- runtime config id
- processing step id
- segment count
- counts by label
- observation ids

## Viewer Compatibility

The existing viewer route works unchanged:

```text
GET /viewer/runs/{run_id}
```

The viewer reads the persisted gameplay observations and renders the gameplay/non_gameplay/uncertain timeline band.

## Out of Scope

- YOLO inference
- ball/player tracking
- pose tracking
- court homography
- bounce detection
- point reconstruction
- scoring
- production deployment
