# Tracklet Review Dataset Export v0

## Purpose

Tracklet Review Dataset Export v0 packages candidate tracklet evidence into a portable JSON artifact.

It answers:

```text
Can TOM v3 export candidate tracklets, track points, source detections, frame artifact metadata, lineage, and human annotations for later review or evaluation without changing the source evidence?
```

## Export Modes

### By Tracklet Ids

```json
{
  "tracklet_ids": ["..."],
  "include_frame_artifacts": true,
  "include_annotations": true,
  "format": "json"
}
```

### By Query Filters

```json
{
  "query": {
    "track_family": "ball",
    "has_annotation": true
  },
  "include_frame_artifacts": true,
  "include_annotations": true,
  "format": "json"
}
```

Query mode reuses the `POST /tracklets/query` service. Export logic does not duplicate tracklet filtering.

## API

```text
POST /tracklets/export-review-dataset
```

The endpoint writes an export file and returns artifact metadata:

```json
{
  "export_id": "...",
  "artifact_id": "...",
  "uri": "file:///...",
  "path": "...",
  "checksum": "...",
  "tracklet_count": 1,
  "tracklet_ids": ["..."],
  "query_result_id": "...",
  "warnings": {
    "candidate_evidence_only": true,
    "annotations_are_reviews_not_truth": true,
    "no_adjudication": true
  }
}
```

## Worker CLI

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --tracklet-id <TRACKLET_ID> \
  --output-root .data/exports
```

Query export:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"track_family":"ball","has_annotation":true}' \
  --output-root .data/exports
```

Optional flags:

- `--include-frame-artifacts` / `--no-include-frame-artifacts`
- `--include-annotations` / `--no-include-annotations`
- `--query-name`
- `--created-by`

## Storage

Local JSON exports are written to:

```text
.data/exports/tracklets/{export_id}/tracklet_review_dataset.json
```

Each export persists an `evidence_artifact` row:

```text
artifact_type = tracklet_review_dataset_export
uri = file://...
checksum = sha256(export file)
```

The current `evidence_artifact` schema requires `media_id`, so multi-media exports record `media_scope` in metadata and attach the artifact row to one media id represented by the export. This is a storage-shape limitation, not a claim that all export entries are from one media asset.

## Export Contents

Each export includes:

- export version and generated timestamp
- query spec
- selected tracklet ids
- media summaries
- tracklet and source detection run summaries
- runtime config summaries
- model summaries
- tracklet evidence bundle entries
- annotations when requested
- frame artifact metadata when requested
- lineage rows
- provenance metadata

Required warning fields:

```json
{
  "candidate_evidence_only": true,
  "annotations_are_reviews_not_truth": true,
  "no_adjudication": true
}
```

## Query Result

When exporting by query, TOM v3 persists a `query_result` row that records:

- query name
- export request spec
- selected tracklet ids
- selected tracklet candidate observation ids
- export artifact id and URI

This row is a memory bridge for the export. It does not persist the full export payload.

## Non-Goals

- No frame image file copying.
- No training label generation.
- No reviewer identity or auth system.
- No pose, homography, bounce, hit, rally, point, or scoring logic.
- No adjudication.

## Rule

An export is a portable evidence package. It is not a source of adjudicated labels.
