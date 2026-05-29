# Event Candidate Video Overlay v0.1

Status: implemented

Event Candidate Video Overlay v0.1 makes existing `hit_candidate` and `bounce_candidate` evidence
visible on the broadcast video overlay.

The read-model path is:

```text
hit_candidate / bounce_candidate
-> source_ball_court_projection_observation_id
-> ball_court_projection_candidate.payload.image_point
-> broadcast video marker
```

This is replay visualization only. It does not change event candidate generation and does not
upgrade candidates into truth.

## Overlay Payload

Replay event candidate overlay and timeline payloads now include:

```json
{
  "image_point": { "x": 935.2, "y": 426.7 },
  "image_marker_source": "source_ball_court_projection_image_point"
}
```

If the source projection image point is unavailable, replay returns:

```json
{
  "image_point": null,
  "image_marker_source": "unavailable"
}
```

Missing image points do not fail the replay API.

## Video Markers

The video overlay draws:

- `HIT CANDIDATE` with a triangle/contact-style marker
- `BOUNCE CANDIDATE` with a ring marker

Labels must include `CANDIDATE`.

The marker appears near the candidate timestamp using a short display hold window so timeline-click
inspection is practical without making the marker look persistent or adjudicated.

## Mini-Map

The existing court projection mini-map remains unchanged:

- event candidates are shown in normalized court-template coordinates
- the video overlay uses image-space coordinates from the source ball court projection

## Boundaries

Video markers are candidate visualizations. They are not:

- hit truth
- bounce truth
- in/out
- point or score
- rally logic
- player identity
- accepted/rejected lifecycle
- adjudication
