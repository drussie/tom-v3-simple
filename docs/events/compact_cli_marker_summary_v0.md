# Compact CLI + Marker Summary v0

Status: implemented

This workflow cleanup makes `build-hit-bounce-candidates` operator-focused by default. The
hit/bounce builder still persists the same candidate evidence and rich diagnostics internally, but
the default CLI response now prints a compact summary instead of the full diagnostic tree.

This milestone does not change hit/bounce candidate generation, marker-level arbitration, replay
behavior, or persisted evidence. It does not add hit truth, bounce truth, in/out, score,
rally/point truth, player identity, accepted/rejected lifecycle, or adjudication.

## Default Output

By default, `make tom-v1-hit-bounce-candidates` prints:

- `ok`, `status`, message, run ids, processing step id, runtime config id
- replay URL
- observation counts
- active version summary
- one `marker_summary` row per final visible `hit_candidate` / `bounce_candidate`
- compact summary counts
- candidate-only warnings

The default output omits:

- `observation_ids`
- full nested `candidate_summary`
- full rejection reason maps
- full historical recall diagnostics

## Marker Summary

`marker_summary` is sorted by timestamp, frame, and candidate type. Each row is a final visible
marker, not a rejection diagnostic:

```json
{
  "index": 1,
  "candidate_type": "hit_candidate",
  "frame": 10,
  "timestamp_ms": 333,
  "source_method": "trajectory_player_proximity_hit_candidate_v0",
  "arbitration_decision": "keep_hit",
  "arbitration_reason": "final_hit_candidate_marker",
  "court_x": 0.34,
  "court_y": 0.16,
  "image_x": 787.14,
  "image_y": 755.09,
  "confidence": 0.66
}
```

The summary is for operator review only. It does not confirm hits, bounces, in/out, point state, or
score.

## Verbose / Diagnostic Flags

Use these flags when deep diagnostics are needed:

```bash
.venv/bin/python -m apps.worker.cli build-hit-bounce-candidates ... --verbose
.venv/bin/python -m apps.worker.cli build-hit-bounce-candidates ... --include-observation-ids
.venv/bin/python -m apps.worker.cli build-hit-bounce-candidates ... --diagnostic-summary full
.venv/bin/python -m apps.worker.cli build-hit-bounce-candidates ... --diagnostic-summary none
```

Makefile support:

```bash
make tom-v1-hit-bounce-candidates VERBOSE=1
make tom-v1-hit-bounce-candidates HIT_BOUNCE_VERBOSE=true
make tom-v1-hit-bounce-candidates INCLUDE_OBSERVATION_IDS=true
make tom-v1-hit-bounce-candidates DIAGNOSTIC_SUMMARY=full
make tom-v1-hit-bounce-candidates-verbose
```

`--verbose` returns the full legacy-style result. `--diagnostic-summary full` keeps compact framing
but includes the full `candidate_summary`. `--include-observation-ids` adds the persisted
observation id list to compact output.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Default compact output:

- `event_candidate_run_id`: `8a4a3229-0958-4dc1-b2e2-cc6454b8c6e4`
- output size: about 6.5 KB
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `marker_summary`: 6 final markers
- no `observation_ids`
- no full `candidate_summary`

Verbose output:

- `event_candidate_run_id`: `3a86acbe-fabe-4618-a20c-44fa82f02fe8`
- output size: about 58 KB
- includes `observation_ids`
- includes full `candidate_summary`

## Boundaries

This is a CLI presentation cleanup. It makes TOM easier to operate without reducing stored
diagnostics or changing candidate decisions. The output remains candidate evidence only.
