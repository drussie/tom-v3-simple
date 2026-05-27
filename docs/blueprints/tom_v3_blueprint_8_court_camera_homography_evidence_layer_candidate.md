# TOM v3 Blueprint 8 Candidate - Court / Camera / Homography Evidence Layer

Status: IN PROGRESS

Blueprint 7 is complete. Blueprint 8 has started with Milestone 8A schema/contract work and Milestone 8B fixture court evidence persistence.

## Mission

Persist court, camera, and homography model-output evidence as replayable observations, including court keypoints, court lines, camera/view state, homography candidates, projection diagnostics, and optional court-space coordinate transform candidates, without turning geometry evidence into tennis-event or court-position conclusions.

## Why This Is Blueprint 8

Court and homography work is a geometry evidence layer. It should not be hidden inside Blueprint 7 because it introduces a new evidence family, new diagnostics, new replay layers, and new risk of accidental tennis-event interpretation.

Blueprint 7 activates real perception for replay:

```text
real detections
-> real-detection-derived candidate tracklets
-> real pose keypoint evidence
```

Blueprint 7 closes before implementing court/camera/homography runtime, schema, API, or replay overlays. That boundary keeps Blueprint 8 focused on geometry evidence instead of folding court work into the real detection/pose runtime.

Blueprint 8 should deliberately design:

```text
court/camera evidence
-> homography candidates
-> projection diagnostics
-> replay inspection
```

## Candidate Milestones

### 8A - Court Evidence Schema / Contract

Define court observation family, typed rows, keypoint schemas, line classes, camera/view labels, lineage, audit expectations, and TOM-native export contracts.

Status: COMPLETE.

8A adds typed contracts, storage models, Alembic migration, observation writer support, lineage constants, a normalized court template registry, schema/persistence tests, and docs. It does not add court runtime, homography computation, replay court overlays, or ball/player court projections.

### 8B - Court Keypoint / Line Evidence Adapter

Add an adapter boundary for court keypoint and court line model output. Preserve media-owned frame/time and image-pixel coordinates.

Status: COMPLETE.

8B adds a deterministic fixture court evidence adapter, worker `run-fixture-court`, Makefile `court-fixture`, model/runtime/run/step provenance, and persisted court keypoint, court line, and camera/view observations. It does not add a real court model, homography computation, projection diagnostics, replay court overlays, or ball/player court projections.

### 8C - Camera / View Evidence Layer

Harden camera/view evidence as its own geometry context layer. 8B already writes fixture camera/view rows; 8C should query/expose/review camera/view evidence without duplicating the fixture camera row contract.

Status: COMPLETE.

8C adds camera/view query, summary, and evidence-bundle read models plus `/court/camera-view` API endpoints. It does not add a real camera model, homography computation, projection diagnostics, replay court overlays, or ball/player court projections.

### 8D - Homography Candidate Persistence

Persist homography candidates from source court keypoint/line evidence with candidate status, confidence, reprojection diagnostics, and lineage.

### 8E - Court Overlay In Replay Workstation

Render court keypoint evidence, court line evidence, and homography candidate context as toggleable replay layers.

### 8F - Projection Diagnostics / Review Export

Persist projection diagnostics and export TOM-native review datasets with lineage, artifacts, and annotations.

### 8G - Completion Review

Close Blueprint 8 with validation, limitations, final status updates, and future blueprint boundaries for bounce/hit/rally/point/scoring work.

## Proposed Observation Family

```text
observation_family = court
```

Potential observation types:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

8A implements these as typed tables connected to the existing observation spine.

## Evidence Invariants

- Frame/time is owned by media indexing.
- Coordinates are explicit about image-pixel and court-template spaces.
- Homography rows are candidates.
- Projection rows are candidates.
- Review annotations do not mutate observations.
- Court evidence does not create bounce/hit/rally/point/scoring conclusions.

## Replay Integration

Future replay layers should be toggleable:

- court keypoint evidence
- court line evidence
- homography candidate
- projection diagnostic

Selected detail should show model/runtime/config, frame/time, confidence, source keypoints/lines, matrix, reprojection error, lineage, artifacts, annotations, and candidate-only wording.

## Non-goals

Blueprint 8 should not automatically add bounce detection, hit detection, stroke classification, rally segmentation, point reconstruction, scoring, real stream ingestion, production deployment, or TOM v2-style adjudication.

Those layers should remain future blueprint decisions.
