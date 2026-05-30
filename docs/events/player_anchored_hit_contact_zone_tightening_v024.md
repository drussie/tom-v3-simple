# Player-Anchored Hit Contact-Zone Tightening v0.2.4

Status: implemented

This repair tightens the v0.2.3 player-anchored hit recall pass. The output remains candidate
evidence only: it is not hit truth, bounce truth, in/out, rally, point, score, player identity,
accepted/rejected lifecycle, or adjudication.

## Repair Goal

v0.2.3 recovered sparse hit candidates by anchoring a main player projection to the closest ball
trajectory point in a wide window. That improved recall, but it could also attach a hit candidate to
an open-court landing point that overlapped a bounce candidate.

v0.2.4 keeps the wide-window recall path but requires a player contact-zone anchor and suppresses
player-anchored hits that overlap bounce candidates in the same time/space cluster.

## Contact-Zone Gate

Player-anchored hit candidates now include `player_anchor_contact_zone` metadata:

```json
{
  "track_role_candidate": "far_player_track_candidate",
  "side_matches_player_track": true,
  "distance_template_units": 0.08,
  "distance_threshold": 0.24,
  "strong_distance_threshold": 0.18,
  "in_contact_zone": true,
  "strong_contact_zone": true,
  "open_court_landing_zone": false
}
```

Rejected anchors can now report:

- `not_player_contact_zone`
- `open_court_landing_zone_anchor`
- `side_mismatch_player_track`

## Bounce-Overlap Suppression

After side-zone sequence classification, v0.2.4 checks player-anchored hit candidates against final
bounce candidates. If a player-anchored hit overlaps a bounce candidate within the configured time
and court-distance window, the hit candidate is suppressed and a diagnostic is written.

Default overlap threshold:

```text
event_overlap_distance_template = 0.08
candidate_dedupe_ms = 500
```

Suppression diagnostics include:

```json
{
  "overlaps_bounce_candidate": true,
  "overlap_distance_template": 0.01588,
  "overlap_time_delta_ms": 133,
  "suppressed": true,
  "reason": "bounce_candidate_overlap_without_strong_contact_zone"
}
```

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `5280daf4-78f5-4d80-a011-fdac5d263d39`
- `hit_candidate`: 2
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 655
- `player_anchor_suppressed_overlap_count`: 1

The far-side player-anchored hit that overlapped the far-side bounce was suppressed. The far-side
bounce remained, and the final candidate set stayed candidate-only.

## Boundaries

This repair improves candidate quality and review diagnostics only. It does not add hit truth,
bounce truth, in/out, rally/point/score logic, player identity, server/receiver logic,
accepted/rejected lifecycle, or adjudication.
