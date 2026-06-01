# Blueprint 10 - Benchmark / Evaluation Harness v0

Blueprint 10 adds a read-only evaluation harness for point candidate review runs.

The harness summarizes:

- generated final hit/bounce candidate markers
- rejection diagnostic observation counts
- Blueprint 9 operator review labels
- Blueprint 9 missing-candidate notes
- reviewed-marker coverage
- reviewed-only label fractions

It does not create hit truth, bounce truth, in/out decisions, score, point state, player identity,
accepted/rejected lifecycle, automatic correction, or adjudication.

## Command

```bash
.venv/bin/python -m apps.worker.cli evaluate-point-candidates \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --viewer-base-url http://127.0.0.1:3000
```

The Make helper is:

```bash
make tom-v1-evaluate-point-candidates \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>
```

Optional output controls:

```bash
make tom-v1-evaluate-point-candidates \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  FORMAT=markdown \
  OUTPUT=tmp_reports/point_candidate_review.md
```

## Output Contract

The evaluation payload includes:

- `candidate_counts`
- `review_summary`
- `review_coverage`
- `reviewed_only_rates`
- `candidate_type_breakdown`
- `marker_evaluation_summary`
- `missing_candidate_notes`
- candidate-only warnings

Reviewed-only rates are descriptive summaries of operator metadata. They are not dataset-level
benchmark metrics and must not be used as adjudication.

## Boundary

Evaluation reports are review summaries only. They do not mutate generated candidate observations,
review annotations, source evidence, marker arbitration, replay display state, or model output.

