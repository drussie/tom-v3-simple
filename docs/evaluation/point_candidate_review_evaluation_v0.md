# Point Candidate Review Evaluation v0

Point Candidate Review Evaluation v0 is a CLI/reporting layer over existing event candidate runs
and Blueprint 9 review annotations.

## Inputs

- `media_id`
- `event_candidate_run_id`
- optional `viewer_base_url`

The evaluator reads the final visible marker summary from the event candidate run and review rows
from `event_candidate_review_annotation`.

## Output

The JSON output includes candidate counts, review summary counts, reviewed/unreviewed marker
coverage, reviewed-only label fractions, per-candidate-type breakdowns, reviewed marker rows, and
missing-candidate notes.

Markdown output is available for operator reports and writes the same information in a compact
table format.

## Review Labels

Candidate marker labels remain operator metadata:

- `useful`
- `wrong`
- `unclear`
- `needs_review`

Missing-candidate note labels remain operator metadata:

- `missing_hit_candidate`
- `missing_bounce_candidate`
- `missing_event_candidate`

These labels do not change generated candidates, final markers, source evidence, replay overlays,
in/out state, score, point state, or adjudication.

## Known Limits

This v0 harness is intentionally modest. It does not compare against an adjudicated reference set,
does not compute dataset-level statistical measures, and does not promote any reviewed label into
truth.

The evaluator is useful for operator review summaries and regression comparison between candidate
runs.

