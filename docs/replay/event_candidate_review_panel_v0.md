# Event Candidate Review Panel v0

Status: implemented

Event Candidate Review Panel v0 adds an ordered operator-review list for final visible
`hit_candidate` and `bounce_candidate` markers in replay. The panel uses the replay API
`marker_summary` rows introduced for the Replay Marker Inspector, so it lists final markers only
and excludes rejection diagnostics by default.

This is replay UI and read-model work only. It does not change hit/bounce candidate generation,
marker-level arbitration, source observations, truth status, score, in/out, or adjudication.

## UI Behavior

The replay side panel now includes `Event Candidate Review`.

Each row shows:

- marker index
- marker type
- frame and timestamp
- source method
- marker-level arbitration decision
- confidence

Clicking a row seeks replay to the marker timestamp, selects the corresponding event marker, and
updates the Replay Marker Inspector. The selected row is highlighted so the operator can review the
final marker order without visually hunting across the video and mini-map.

## Data Source

The panel consumes `ReplayTimeline.marker_summary`, falling back to the overlay chunk summary while
timeline data loads. Ordering is the same deterministic order used by the replay API:

1. `timestamp_ms`
2. `frame`
3. `candidate_type`
4. `observation_id`

Only final `hit_candidate` and `bounce_candidate` rows are listed. Rejection diagnostics remain
available through deeper evidence surfaces and are not part of the compact review list.

## Boundary

Rows are candidate evidence navigation aids. They are not hit truth, bounce truth, in/out, score,
player identity, accepted/rejected lifecycle, or adjudication.
