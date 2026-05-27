# Milestone 8B Handoff - Court Keypoint / Line Evidence Adapter

Status: COMPLETE

Milestone 8B implemented the fixture court evidence adapter for Blueprint 8.

## Completed

- Added `apps/worker/services/court_adapter.py`.
- Added worker CLI command `run-fixture-court`.
- Added Makefile helper `court-fixture`.
- Added deterministic fixture court keypoints, court lines, and camera/view observations.
- Persisted all evidence through `ObservationWriter` and the 8A typed court tables.
- Created model registry, runtime config, processing run, and processing step provenance.
- Added service and CLI tests.
- Added docs and runbook updates.

## Next Handoff

Recommended next milestone:

```text
Milestone 8C - Camera / View Evidence Layer
```

8C should harden/query/expose camera/view evidence as its own geometry context layer. It should not duplicate the fixture camera rows added in 8B.

## Boundaries

No homography candidate builder, projection diagnostic builder, replay court overlay, real court model, ball/player court-space projection, or tennis-event interpretation was added.
