# Milestone 2D - Tracklet Evidence Export / Review Dataset Foundation

## Goal

Create the first reusable export foundation for reviewed tracklet candidate evidence.

The milestone packages selected tracklet evidence bundles into durable JSON artifacts so candidate tracklets, track point candidates, source detections, frame artifact metadata, lineage, and human annotations can be reused outside the live API/viewer.

## Scope

- Tracklet review dataset export service.
- Export by explicit tracklet ids.
- Export by structured tracklet query filters.
- Reuse of the Milestone 2C tracklet query service.
- JSON export written to local filesystem storage.
- `evidence_artifact` row for the export artifact.
- Optional `query_result` row when exporting by query.
- Worker CLI command `export-tracklet-review-dataset`.
- Optional API endpoint `POST /tracklets/export-review-dataset`.
- Tests and docs.

## Non-Goals

- No model training.
- No label platform.
- No reviewer identity or auth system.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally, point, or scoring logic.
- No adjudication.

## Export Contract

The exported JSON uses:

```text
tracklet_review_dataset_export
```

Each export includes:

- export version and generated timestamp
- export id
- query spec and selected tracklet ids
- required warning fields
- media, run, runtime config, and model summaries
- tracklet evidence bundle entries
- annotations when requested
- referenced frame artifact metadata when requested
- tracked_from and grouped_from lineage rows
- provenance metadata

Required warning fields:

```json
{
  "candidate_evidence_only": true,
  "annotations_are_reviews_not_truth": true,
  "no_adjudication": true
}
```

## Storage

Local exports are written under:

```text
.data/exports/tracklets/{export_id}/tracklet_review_dataset.json
```

The JSON file is referenced by an `evidence_artifact` row:

```text
artifact_type = tracklet_review_dataset_export
```

The JSON payload is not stored in Postgres.

## Acceptance

Milestone 2D is complete when:

- Export by tracklet ids works.
- Export by query filters works.
- Export reuses the tracklet query service.
- Exports include evidence bundle data and warning fields.
- Exports include annotations and frame artifact metadata when requested.
- Exports succeed when frame artifacts are unavailable.
- Export JSON is written to local storage.
- Export artifact metadata and checksum are persisted.
- Worker CLI exists.
- API endpoint exists or worker-only behavior is documented.
- Existing tracklet query, evidence bundle, tracklet builder, frame artifact, detection, gameplay, media indexing, and synthetic smoke tests pass.

## Result

Status: complete.

Milestone 2D adds reusable review dataset exports for candidate tracklet evidence while preserving the observation-only boundary.
