# Gameplay / View-State Layer v0

## Purpose

Gameplay/non-gameplay classification is itself an observation.

TOM v3 must persist view-state output as gameplay_observation records with frame/time ranges, confidence, source model or process metadata, runtime configuration, and lineage.

## Supported States

The layer should support:

- gameplay
- non_gameplay
- uncertain

## Optional Subtypes

Optional subtypes may include:

- active_point
- between_points
- serve_setup
- changeover
- replay
- scoreboard
- camera_cut
- closeup
- crowd_shot
- broadcast_graphic
- unknown

## Processing Contract

Gameplay classification scopes downstream processing, but it does not become adjudicated truth.

Examples:

- A worker may choose to run expensive ball tracking only over gameplay ranges.
- The viewer should still display non_gameplay and uncertain ranges.
- Later runs may emit different gameplay observations for the same media.
- Human review should create human_annotation records rather than mutating prior observations.

## Payload Direction

A gameplay_observation payload should include:

- `view_state`
- `view_state_subtype`
- `confidence`
- `source`
- `frame_start`
- `frame_end`
- `timestamp_start_ms`
- `timestamp_end_ms`
- optional `reason_codes`
- optional `region_refs`
- optional `debug_artifact_refs`

## TOM v1 Relationship

TOM v1 already has a strong gameplay/not-gameplay detector.

TOM v3 should reuse it only if it can be wrapped cleanly behind a TOM v3 interface.

If it is entangled with TOM v1 infrastructure, TOM v3 should preserve the interface and rebuild the implementation.

The TOM v3 interface should emit gameplay_observation records and evidence artifacts instead of hiding the classification as control flow.
