# TOM v3 Simple Exports

Exports package TOM v3 evidence for review and downstream analysis.

They are review datasets, not official tennis results.

## Why Exports Exist

Exports preserve a portable snapshot of observations, lineage, artifacts, annotations, model/runtime context, and selection criteria.

They are useful for review, debugging, and later dataset preparation.

## Tracklet Review Export

Worker command:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"tracklet_run_id":"<tracklet_run_id>","limit":500}' \
  --output-root .data/exports
```

Export path:

```text
.data/exports/tracklets/{export_id}/tracklet_review_dataset.json
```

Records include:

- tracklet candidates
- track point candidates
- source detections
- lineage
- frame artifact metadata
- review annotations
- run/model/runtime context

## Pose Review Export

Worker command:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --run-id <pose_run_id> \
  --output-root .data/exports
```

Export path:

```text
.data/exports/pose/{export_id}/pose_review_dataset.json
```

Records include:

- pose observations
- full keypoint JSON
- subject association candidate context
- lineage
- artifacts
- review annotations
- run/model/runtime context

## Evidence Artifact Rows

Each export writes an `evidence_artifact` row with:

- artifact type
- media/run context
- file URI
- checksum
- export metadata

Current artifact types:

- `tracklet_review_dataset_export`
- `pose_review_dataset_export`

## Query Result Memory

Query-driven exports can create a `query_result` row. It stores the query spec, selected ids, and export artifact id/URI.

This is memory for how the export was selected. It is not a replacement for the export file.

## Annotation Inclusion

Exports include review annotations when requested. Annotations remain separate review evidence and do not mutate observations.

## Artifact Inclusion

Tracklet exports can include frame artifact metadata. Pose exports can include pose/source artifact metadata.

Exports reference artifacts; they do not redesign artifact storage.

## What Exports Are Not

Exports are not:

- official tennis labels
- scoring data
- event adjudication
- YOLO or pose training format in v0
- model-quality certification
