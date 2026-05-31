# Compact CLI + Marker Summary v0 Report

## Summary

Implemented compact default output for `build-hit-bounce-candidates`. The service continues to
return rich diagnostics internally, while the CLI now formats the default response for operator
review: run ids, replay URL, counts, active versions, warnings, and a deterministic marker summary.

## Output Modes

- Default: compact response with `marker_summary`, no `observation_ids`, no full
  `candidate_summary`.
- `--include-observation-ids`: adds the persisted observation id list to compact output.
- `--diagnostic-summary full`: adds the full `candidate_summary`.
- `--diagnostic-summary none`: keeps only run/replay/count/warning essentials.
- `--verbose`: returns the full legacy-style result.

The Makefile default remains compact. `make tom-v1-hit-bounce-candidates-verbose` opts into verbose
diagnostics.

## Local Smoke

Command:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-hit-bounce-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  BALL_TRAJECTORY_RUN_ID=2e16f3d1-e252-497a-b688-d81890645ab7 \
  COURT_PROJECTION_RUN_ID=82498799-490f-44df-9222-0157356c5ff7
```

Default compact result:

- `event_candidate_run_id`: `8a4a3229-0958-4dc1-b2e2-cc6454b8c6e4`
- output size: 6,558 bytes
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `marker_summary`: 6 final visible markers
- omitted `observation_ids`
- omitted full `candidate_summary`

Verbose comparison:

- `event_candidate_run_id`: `3a86acbe-fabe-4618-a20c-44fa82f02fe8`
- output size: 58,238 bytes
- includes `observation_ids`
- includes full `candidate_summary`

Makefile `VERBOSE=1` alias smoke also returned full diagnostics:

- `event_candidate_run_id`: `03f72875-2087-4d28-8305-33ab4664e649`
- output size: 60,358 bytes
- includes `observation_ids`
- includes full `candidate_summary`

## Validation

Completed validation:

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q`: 45 passed
- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py tests/test_tom_v1_bridge_helpers.py -q`: 47 passed
- `.venv/bin/python -m pytest -q`: 325 passed
- `ruff check apps/worker/cli.py tests/test_hit_bounce_candidates.py`: passed
- `ruff check .`: passed
- `git diff --check`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

## Boundaries

This milestone changes CLI presentation only. It does not modify hit/bounce classification,
marker-level arbitration, replay behavior, persisted diagnostic data, truth status, scoring,
in/out, or adjudication.
