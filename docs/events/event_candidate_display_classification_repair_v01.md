# Event Candidate Display + Classification Repair v0.1

Status: implemented

Event Candidate Display + Classification Repair v0.1 improves the replay behavior and first-pass
classification policy for existing `hit_candidate` and `bounce_candidate` evidence.

The repair keeps event candidates as derived evidence only. It does not create hit truth, bounce
truth, in/out decisions, point or score logic, accepted/rejected lifecycle, or adjudication.

## Display Policy

Replay now treats event candidates as persistent point-review markers when `eventCandidateRunId` is
present.

Video overlay and court mini-map behavior:

- all hit/bounce event candidates in the selected run remain visible as faint persistent pins
- the current marker is highlighted when playback is within the active window
- the selected marker receives the strongest highlight
- inactive marker shapes stay visible, while labels are de-emphasized to reduce clutter

Labels always include `CANDIDATE`:

- `HIT CANDIDATE`
- `BOUNCE CANDIDATE`

Persistent display is replay/read-model behavior only. It does not make a candidate true.

## Classification Priority

The builder now evaluates hit candidates before bounce candidates when a trajectory change is
player-proximate.

The v0.1 priority is:

```text
trajectory change near main-player projection
-> hit_candidate
-> suppress same-point bounce consideration

trajectory change away from main-player projection
-> bounce_candidate
```

The repaired payload includes review diagnostics:

```json
{
  "classification_priority": "hit_first_when_player_proximate",
  "player_proximity_gate": {
    "nearest_player_found": true,
    "distance_template_units": 0.322808,
    "time_delta_ms": 0,
    "threshold": 0.33,
    "away_from_player": false
  },
  "candidate_decision": {
    "selected_candidate_type": "hit_candidate",
    "suppressed_candidate_types": ["bounce_candidate"],
    "reason": "player_proximate_trajectory_change"
  }
}
```

Bounce candidates include the same gate shape with `away_from_player = true` when a player
projection is present but outside the bounce exclusion threshold.

## Replay Details

The selected evidence panel exposes:

- classification priority
- player proximity gate details
- selected candidate type
- suppressed candidate types
- decision reason
- source image point and court point
- reason codes and no-truth warnings

## Boundaries

Event candidate markers and classifications remain candidate evidence. They are not:

- confirmed hits
- confirmed bounces
- in/out decisions
- point or score
- player identity
- server/receiver logic
- accepted/rejected truth lifecycle
- adjudication

