# Blueprint 18 Reviewed 3D Debug Dataset Regression v0

Blueprint 18 compares two Blueprint 17 reviewed 3D debug dataset exports and produces a
deterministic drift report.

The comparison is file-to-file and read-only. It does not query or mutate live TOM evidence, event
candidates, marker arbitration, 3D candidates, 3D diagnostics, review annotations, in/out, score, or
adjudication.

## Command

```bash
.venv/bin/python -m apps.worker.cli compare-reviewed-3d-debug-dataset \
  --baseline .data/exports/reviewed_3d_debug_dataset_sample_point.baseline.json \
  --current .data/exports/reviewed_3d_debug_dataset_sample_point.current.json \
  --format json \
  --output .data/exports/reviewed_3d_debug_dataset_sample_point.regression.json
```

Make helper:

```bash
make tom-v1-compare-reviewed-3d-debug-dataset \
  BASELINE=.data/exports/reviewed_3d_debug_dataset_sample_point.baseline.json \
  CURRENT=.data/exports/reviewed_3d_debug_dataset_sample_point.current.json \
  FORMAT=json \
  OUTPUT=.data/exports/reviewed_3d_debug_dataset_sample_point.regression.json
```

## What It Compares

The regression report compares:

- export type and version
- summary counts
- required section presence
- warning keys and values
- event marker rows
- 3D trajectory candidate rows
- event-candidate 3D diagnostic rows
- 3D debug review rows
- event candidate review rows

ID-like fields are ignored by default through `allow_id_drift=true`, so regenerated UUIDs do not
create drift by themselves.

## Output

JSON reports include:

- `regression_type: reviewed_3d_debug_dataset_regression_report`
- `regression_version: v0`
- baseline/current paths
- comparison config
- baseline/current summary counts
- drift tables
- warnings
- known limitations

Markdown reports include compact counts, drift status, drift tables, warnings, and limitations.

## Boundaries

Baseline exports are comparison references only. They are not truth, not 3D truth, and not training
truth. Drift means the exports differ; it does not prove either export is correct or incorrect.

The regression harness does not change TOM live behavior.
