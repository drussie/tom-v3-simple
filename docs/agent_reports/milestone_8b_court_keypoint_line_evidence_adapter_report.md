# Milestone 8B Agent Report - Court Keypoint / Line Evidence Adapter

## Summary

Milestone 8B adds a deterministic fixture court evidence adapter. TOM can now write fixture court keypoint observations, court line observations, and camera/view observations into the 8A court schema with model, runtime, run, and step provenance.

## Files Created

- `apps/worker/services/court_adapter.py`
- `docs/court/fixture_court_evidence_adapter_v0.md`
- `docs/milestones/milestone_8b_court_keypoint_line_evidence_adapter.md`
- `docs/handoffs/milestone_8b_court_keypoint_line_evidence_adapter_handoff.md`
- `docs/agent_reports/milestone_8b_court_keypoint_line_evidence_adapter_report.md`
- `tests/test_fixture_court_adapter.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OBSERVATION_CONTRACT.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`
- `docs/court/court_evidence_schema_v0.md`
- `docs/court/court_template_registry_v0.md`

## Fixture Court Adapter Decisions

The adapter is fixture-only and deterministic. It projects the normalized v0 court template into image pixels using simple image margins, then writes keypoints, line segments, and camera/view rows at sampled media-owned frames.

The service name is `run_fixture_court_adapter`, exposed through `run-fixture-court`.

## Frame Sampling Decisions

8B uses media-owned frame/time:

```text
sampled frame -> frame_to_timestamp_ms(media.fps, frame_number)
```

The adapter samples every `frame_sample_rate` frames up to `max_frames`.

## Persistence Decisions

Each sampled frame emits:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`

All observations use `observation_family = court`, typed 8A detail rows, `model_id`, `runtime_config_id`, and geometry-evidence-only metadata.

## CLI / Makefile Decisions

The CLI supports:

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id <media_id> \
  --frame-sample-rate 30 \
  --max-frames 30
```

The Makefile helper is:

```bash
make court-fixture MEDIA_ID=<media_id>
```

Plan-only mode is supported and does not touch the database.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- fixture demo and completion audit smoke
- `run-fixture-court` plan-only smoke
- `run-fixture-court` smoke against the fixture demo media

## Validation Results

- Python tests: passed, `217 passed`.
- Ruff: passed.
- Web lint/build/audit: passed, `0 vulnerabilities`.
- Alembic smoke: passed through `0003_court_evidence_observations`.
- Synthetic viewer smoke: passed.
- Fixture demo: passed with `demo_assets/sample_point.mp4`.
- Completion audit: passed after the fixture demo state was stable.
- Plan-only fixture court smoke: passed.
- Court fixture smoke: passed for media `5b2469c0-372e-414a-a6bf-71d62539606f`, producing 8 `court_keypoint_observation`, 8 `court_line_observation`, and 8 `camera_view_observation` rows.

## Known Limitations

- Fixture court evidence is deterministic schema plumbing, not a real court model.
- No homography candidates are computed in 8B.
- No projection diagnostics are computed in 8B.
- No replay court overlays are rendered in 8B.
- No ball/player detections are projected into court space.

## Non-Goals Preserved

8B does not add homography computation, projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Prepared for final commit, tag, and push.

## Recommended Next Handoff

Milestone 8C - Camera / View Evidence Layer.

8C should harden/query/expose camera/view evidence as its own geometry context layer, not duplicate the fixture camera rows written in 8B.
