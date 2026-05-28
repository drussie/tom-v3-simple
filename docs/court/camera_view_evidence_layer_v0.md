# Camera / View Evidence Layer v0

Milestone 8C makes `camera_view_observation` rows queryable and inspectable as geometry context evidence.

8B already writes fixture camera/view observations. 8C does not duplicate those writes. It adds a read layer:

```text
fixture court run
-> persisted camera_view_observation rows
-> camera/view query service
-> camera/view summary read model
-> camera/view evidence bundle
-> /court/camera-view API endpoints
```

Camera/view evidence remains observation-only. It is not a confirmed camera state, a confirmed court model, a homography decision, or tennis-event interpretation.

## API

Query rows:

```text
GET /court/camera-view?media_id=<media_id>&run_id=<court_run_id>
```

Supported filters:

- `media_id`
- `run_id`
- `start_ms` / `end_ms`
- `frame_start` / `frame_end`
- `view_label`
- `camera_motion_hint`
- `min_view_confidence`
- `limit` / `offset`

Summary:

```text
GET /court/camera-view/summary?media_id=<media_id>&run_id=<court_run_id>
```

Bundle:

```text
GET /court/camera-view/<camera_view_observation_id>/bundle
```

## Query Rows

Rows expose:

- observation id
- media id
- run id
- frame/time
- view label
- view confidence
- camera motion hint
- stability score
- cut likelihood
- model id
- runtime config id
- frame time owner
- metadata
- fixture/evidence-only flags

## Summary

The summary read model reports:

- observation count
- view label counts
- motion hint counts
- frame/time range
- mean view confidence
- mean stability score
- max cut likelihood
- non-binding homography context hints
- evidence-only warnings

The homography context is a candidate context hint only. 8C does not compute or validate a homography. Milestone 8D may link camera/view observations as context for persisted homography candidates, but those candidates remain geometry evidence only. Milestone 8E can display camera/view evidence as replay context. Milestone 8F projection diagnostics may package that context through homography lineage and review export, but camera/view evidence still does not confirm camera state or geometry correctness.

## Evidence Bundle

The bundle returns:

- observation spine
- typed camera/view detail
- media context
- processing run context
- runtime config
- model registry metadata
- lineage rows
- artifacts
- annotations
- annotation summary
- evidence-only warnings

## Non-Goals

8C does not add:

- homography computation
- projection diagnostics
- replay court overlays
- real camera/view model inference
- real court model inference
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- adjudication
