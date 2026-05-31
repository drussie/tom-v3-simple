# Replay Marker Inspector v0

Status: implemented

Replay Marker Inspector v0 adds an operator-facing evidence card for visible hit/bounce candidate
markers. It reuses the final event candidate rows already shown in replay and exposes a compact
`marker_summary` from the replay API so operators do not need terminal JSON to understand why a
marker exists.

This milestone is display and read-model work only. It does not change hit/bounce candidate
generation, marker-level arbitration, source observations, truth status, score, in/out, or
adjudication.

## Replay API

Replay timeline and event overlay responses now include:

```json
{
  "marker_summary": [
    {
      "index": 1,
      "observation_id": "...",
      "candidate_type": "hit_candidate",
      "frame": 54,
      "timestamp_ms": 1800,
      "source_method": "image_space_net_axis_reversal_hit_candidate_v026",
      "arbitration_decision": "keep_hit",
      "arbitration_reason": "local_event_evidence_supported_hit",
      "court_x": 0.489237,
      "court_y": 1.039032,
      "image_x": 952.795242,
      "image_y": 243.613194,
      "confidence": 0.7
    }
  ]
}
```

Rows are deterministic: timestamp, frame, candidate type, then observation id. The summary includes
final visible `hit_candidate` and `bounce_candidate` rows only, not
`event_candidate_rejection_diagnostic` rows.

## UI Behavior

The replay side panel now includes a Marker Inspector card.

When no marker is selected, it says:

```text
No marker selected. Click a hit or bounce marker to inspect candidate evidence.
```

When a marker is selected from the video overlay, mini-map, or timeline, the card shows:

- marker type
- frame and timestamp
- source method
- confidence
- marker-level arbitration decision and reason
- image coordinates
- court-template coordinates
- candidate-only warning

The full selected evidence panel remains available below the compact card for deeper diagnostics.

## Boundary

The inspector always labels this as candidate evidence only. It does not create hit truth, bounce
truth, in/out, score, player identity, accepted/rejected lifecycle, or adjudication.
