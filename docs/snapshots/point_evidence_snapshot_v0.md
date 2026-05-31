# Point Evidence Snapshot v0

Status: implemented

Point Evidence Snapshot v0 creates a compact, durable report for a media/event-candidate run. It
records the replay URL, source run ids, observation counts, active hit/bounce candidate versions,
final visible marker summary, warnings, and known limitations.

This is reporting and traceability only. It does not change hit/bounce generation, marker-level
arbitration, replay marker behavior, truth status, score, in/out, or adjudication.

## CLI

```bash
.venv/bin/python -m apps.worker.cli build-point-evidence-snapshot \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --viewer-base-url http://127.0.0.1:3000
```

Make helper:

```bash
make tom-v1-point-evidence-snapshot \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>
```

JSON is the default output. Markdown can be attached or written with:

```bash
make tom-v1-point-evidence-snapshot \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  POINT_SNAPSHOT_FORMAT=markdown \
  POINT_SNAPSHOT_OUTPUT=.data/exports/point_snapshot.md
```

## Snapshot Contents

The snapshot includes:

- `snapshot_type: point_evidence_snapshot`
- `snapshot_version: v0`
- `media_id`
- `event_candidate_run_id`
- `source_run_ids`
- `replay_url`
- hit/bounce/rejection observation counts
- active candidate versions
- compact final marker summary
- candidate-only warnings
- known limitations

The marker summary lists final visible `hit_candidate` and `bounce_candidate` rows only. It excludes
rejection diagnostics and full observation id dumps by default.

## Boundary

Snapshots are candidate evidence reports. They are useful for operator review, regression
comparison, and sharing the current run state, but they do not create hit truth, bounce truth,
in/out, score, player identity, accepted/rejected lifecycle, or adjudication.
