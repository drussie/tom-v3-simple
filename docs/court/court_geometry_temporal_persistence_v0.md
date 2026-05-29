# Court Geometry Temporal Persistence v0

Court geometry temporal persistence is a replay/read-model display policy for sparse court evidence.

It does not create new court observations. It does not mutate source court keypoint, court line, homography candidate, or projection diagnostic rows. It only lets replay carry the latest candidate geometry forward for a bounded time window so operators can inspect stable hardcam segments without court overlays flickering off between sampled frames.

## Problem

Real TOM v1 court keypoint runs may sample frames every 30 frames. The court evidence itself is useful at sampled frames, but replay previously treated each row like a single instant with a short display hold. Between samples, the raw/mapped keypoints, derived lines, homography candidate, and projection diagnostic could disappear.

## API Policy

`GET /replay/overlays` accepts:

```text
court_temporal_persistence=off|carry_forward
court_persistence_max_gap_ms=1500
```

The default is:

```text
court_temporal_persistence=carry_forward
court_persistence_max_gap_ms=1500
```

When carry-forward is enabled, court geometry layers include the latest previous source observation if it is still within the configured gap. The same policy applies to:

- `court_keypoints`
- `court_lines`
- `homography_candidates`
- `projection_diagnostics`

Camera/view rows already carry their own frame/time range and are not converted into court geometry.

## Payload Metadata

Carried-forward court items preserve the source observation and add display-policy metadata:

```json
{
  "temporal_display_mode": "carry_forward",
  "carried_forward": true,
  "active_from_ms": 5000,
  "active_until_ms": 6000,
  "source_observation_id": "...",
  "source_frame_number": 150,
  "source_observation_timestamp_ms": 5000,
  "court_persistence_max_gap_ms": 1500,
  "carry_forward_boundary": "next_observation_or_max_gap_ms",
  "camera_view_boundary_available": false,
  "temporal_display_candidate": true,
  "candidate_geometry_only": true,
  "not_court_truth": true
}
```

In v0, carry-forward stops at the next observation or `court_persistence_max_gap_ms`. Camera-cut boundaries are reserved for future real camera/view classifier work.

## Replay UI

Replay exposes:

- `Court geometry temporal persistence`: Off / Carry forward latest candidate
- `Court carry-forward max gap`
- a visible `carried-forward candidate geometry` badge when the active overlay is being displayed away from its source sample
- selected evidence detail for source frame/time, active window, current replay timestamp, carry boundary, and `not_court_truth`

## Boundary

Temporal persistence is not court truth. It does not confirm a court model, homography, line call, bounce location, player position, point, or score. It is a bounded display policy for candidate geometry evidence.
