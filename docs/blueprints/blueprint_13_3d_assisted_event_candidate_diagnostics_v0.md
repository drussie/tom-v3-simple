# Blueprint 13 - 3D-Assisted Event Candidate Diagnostics v0

Status: complete

## Goal

Connect final visible `hit_candidate` / `bounce_candidate` markers to nearby
`ball_trajectory_3d_candidate` rows so the operator can inspect 3D-readiness context for each
marker.

This blueprint is diagnostic-only. It does not change hit/bounce generation, marker arbitration,
review annotations, candidate counts, source evidence, in/out, score, or adjudication.

## Pipeline

```text
final hit/bounce marker
+ nearby 3D ball trajectory candidate samples
+ camera geometry evidence
-> event_candidate_3d_diagnostic
```

Each diagnostic records:

- event observation id and candidate type
- nearest 3D candidate sample, when available
- nearest time delta
- metric court-plane x/y, when available
- height status
- local sample counts before/after the marker
- local velocity availability and simple local direction diagnostic
- conservative diagnostic status/label

## Labels

Allowed diagnostic statuses:

- `not_evaluated`
- `evaluated`
- `cannot_evaluate`
- `insufficient_3d_evidence`
- `height_unknown`

Allowed diagnostic labels:

- `supports_candidate_context`
- `weakens_candidate_context`
- `neutral_context`
- `cannot_evaluate`
- `insufficient_evidence`
- `height_unknown`

Blueprint 13 v0 uses conservative labels. With Blueprint 12 default `none_unknown`, most useful
diagnostics should be `height_unknown` status and `neutral_context` label.

## Interfaces

CLI:

```bash
python -m apps.worker.cli build-event-candidate-3d-diagnostics \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --trajectory-3d-run-id <trajectory_3d_run_id> \
  --camera-geometry-id <camera_geometry_id> \
  --time-window-ms 250
```

Make:

```bash
make tom-v1-build-event-candidate-3d-diagnostics \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

Read-model integration:

- replay overlay/timeline responses include compact diagnostics and a summary
- marker summaries attach `event_candidate_3d_diagnostic` when available
- point evidence snapshots include `event_candidate_3d_diagnostic_summary`
- point candidate evaluations include `event_candidate_3d_diagnostics`

## Boundary

3D-assisted diagnostics are evidence/debug metadata only. They do not confirm or reject event
candidates, do not create 3D truth, do not decide in/out, do not create score, and do not
adjudicate.
