# Milestone 0C - Worker + Rich Synthetic Observation Seeder

## Goal

Implement the first worker layer and rich synthetic observation seeding flow for TOM v3 Simple.

The target loop:

```text
worker synthetic seed -> persisted observations -> queryable evidence -> viewer-ready timeline/coverage/candidate data
```

## Scope

Milestone 0C includes:

- worker CLI entrypoint
- baseline synthetic scenario definition
- shared synthetic seeding function reused by worker and API dev route
- media fixture registration
- runtime config and synthetic model registry records
- processing run and processing steps
- gameplay/non-gameplay/uncertain view-state segments
- ball and player observations
- tracklets and track points
- track coverage gaps and low-confidence ranges
- homography placeholder observations
- derived bounce_candidate, tracking_gap_candidate, and hit_candidate placeholders
- lineage links
- evidence artifact metadata
- query verification helper
- tests
- docs updates and agent report

## Non-goals

- No YOLO integration.
- No TOM v1 gameplay detector integration.
- No real video decoding.
- No real ffprobe media indexing.
- No real homography calculation.
- No real bounce detection.
- No real player tracking.
- No frontend visual evidence viewer.
- No streaming ingestion.
- No production auth.
- No cloud deployment.
- No TOM v2 adjudication.

## Acceptance Status

Status: complete.

Milestone 0C acceptance criteria are satisfied by:

- worker package in `apps/worker`
- CLI command in `apps/worker/cli.py`
- baseline scenario in `apps/worker/scenarios/baseline_tennis_clip.py`
- shared seeding logic in `packages/observations/tom_v3_observations/synthetic.py`
- API dev route reuse of the shared seeding function
- worker tests in `tests/test_worker_synthetic.py`
- updated API tests in `tests/test_backend_api.py`
- worker docs in `docs/worker`

## Rerun Behavior

Default behavior creates a new processing run each time.

Observation idempotency keys are scoped to the generated run id, so retries within the same run would be safe, while normal CLI reruns intentionally create fresh synthetic evidence.

## Next Handoff

Milestone 0D - Visual Evidence Viewer Foundation.
