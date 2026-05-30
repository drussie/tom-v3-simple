# Hit/Bounce Candidate Evidence v0

Status: implemented

Hit/Bounce Candidate Evidence v0 derives first-pass tennis-event candidate markers from persisted
court-space ball trajectory candidates and main-player court projection candidates.

The pipeline is:

```text
ball_trajectory_court_candidate
+ main_player_court_projection_candidate
-> trajectory/player proximity diagnostics
-> hit_candidate and bounce_candidate observations
```

These observations are candidate evidence only. They are not hit truth, bounce truth, in/out,
point, score, or adjudication.

## Observation Types

The builder persists generic observation-spine rows:

- `observation_family = event_candidate`
- `observation_type = hit_candidate`
- `observation_type = bounce_candidate`
- `granularity = frame`
- `coordinate_space = court_template_2d`

Each payload includes:

- source ball trajectory run and observation ids
- source court projection run id
- source ball court projection observation id
- nearest main-player court projection context when used
- court-template candidate point
- direction/speed trajectory context
- reason codes
- confidence
- evidence-only warning flags

## Hit Candidate Method

The original v0 method proposed a hit candidate from generic trajectory direction change near a
main-player projection candidate. Hit/Bounce Physics Heuristic Repair v0.2 updates this to
`net_axis_reversal_player_proximity_hit_candidate_v02`, which proposes a hit candidate when:

- the ball reverses the candidate net-axis direction, currently `court_y`
- the ball trajectory context remains near a main-player court projection candidate
- the nearest player projection is within the configured template-distance threshold
- the player and ball candidate times are within the configured window
- direction or speed-change diagnostics support the candidate

Reason codes include:

- `near_main_player_projection`
- `net_axis_reversal`
- `trajectory_direction_change`
- `speed_change_candidate`
- `within_time_window`
- `player_proximate_event_priority`

The confidence score is deterministic and capped for v0. It is a candidate score, not a truth
probability.

Event Candidate Display + Classification Repair v0.1 adds an explicit
`hit_first_when_player_proximate` priority. A player-proximate trajectory change is evaluated as a
`hit_candidate` before any bounce consideration for the same context. Payloads include
`player_proximity_gate` and `candidate_decision` diagnostics for review.

## Bounce Candidate Method

The original v0 method proposed a bounce candidate from generic trajectory direction change away
from players. Hit/Bounce Physics Heuristic Repair v0.2 updates this to
`image_vertical_proxy_speed_reduction_bounce_candidate_v02`, which proposes a bounce candidate
when:

- source image-y motion descends into the candidate and ascends after it
- court-template speed decreases after the candidate
- the candidate is away from main-player court projection candidates
- the point is inside or near the normalized court template

Reason codes include:

- `descending_to_ascending_image_proxy`
- `speed_reduction_candidate`
- `away_from_main_player_projection`
- `inside_or_near_court_template`
- `trajectory_direction_change`
- `local_motion_discontinuity`

Because v0 has 2D template trajectory only and no true ball height, the image-y vertical signal is
recorded as a camera-space proxy. Bounce candidates are intentionally conservative derived markers.

## Deduplication

The builder dedupes candidate clusters by a configurable time window:

- hit candidates dedupe by track-role candidate plus time window
- bounce candidates dedupe by time window
- the highest-confidence candidate is kept

v0 does not force tennis alternation, rally order, or point structure.

## Replay

Replay accepts:

```text
eventCandidateRunId=<event_candidate_run_id>
```

Replay overlay layers are:

```text
hit_candidates
bounce_candidates
```

The timeline exposes one lane:

```text
event_candidates
```

The court projection mini-map draws `HIT CANDIDATE` and `BOUNCE CANDIDATE` markers in court-template
space. Event Candidate Display + Classification Repair v0.1 keeps those markers visible as
persistent review pins, with active and selected states.

Event Candidate Video Overlay v0.1 also draws candidate markers on the broadcast video when the
event candidate's source `ball_court_projection_candidate` contains an image-space `image_point`.
Those video markers are also persistent review pins in v0.1 and remain candidate visualizations
only.

## Boundaries

Hit/bounce candidates are derived evidence. They are not:

- confirmed hits
- confirmed bounces
- in/out decisions
- rally, point, or score logic
- player identity
- scoreboard OCR
- server/receiver logic
- accepted/rejected truth lifecycle
- adjudication

Raw detections, smoothed candidates, court projections, trajectories, homography candidates, and
court evidence are not mutated.
