# Blueprint 9 Manual Candidate Review Annotation v0 Report

## Summary

Implemented manual review metadata for event candidate markers and missing-candidate notes.

This is a review annotation layer only. It does not mutate generated event candidates, does not add hit/bounce truth, and does not introduce in/out, score, point state, accepted/rejected lifecycle, or adjudication.

## Added

- `event_candidate_review_annotation` table and migration
- `tom_v3_schema.event_candidate_reviews` request/response models
- FastAPI replay review endpoints
- Next replay review proxy routes
- Replay Marker Inspector review controls
- Event Candidate Review panel badges and summary counts
- Missing Candidate Note panel for current replay frame/time
- Point evidence snapshot review summary and compact annotations

## Review Labels

Marker reviews:

- `useful`
- `wrong`
- `unclear`
- `needs_review`

Missing-candidate notes:

- `missing_hit_candidate`
- `missing_bounce_candidate`
- `missing_event_candidate`

## Guardrails

Truth-like labels such as `confirmed_hit` are rejected.

Review payloads are marked:

- `review_metadata_only`
- `candidate_evidence_preserved`
- `not_truth`
- `no_adjudication`

## Validation

Validation passed:

```bash
.venv/bin/python -m pytest tests/test_event_candidate_review_annotations.py -q
.venv/bin/python -m pytest -q
ruff check .
git diff --check
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_9_review_annotation_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_9_review_annotation_fixture.db \
make completion-audit PYTHON=.venv/bin/python
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_9_migration_check.db \
.venv/bin/alembic upgrade head
```

Results:

- focused review tests: 3 passed
- full pytest: 331 passed
- ruff: passed
- web lint/build/audit: passed, 0 vulnerabilities
- fixture demo: passed
- completion audit: passed
- migration smoke: passed

No local browser smoke was run in this pass.
