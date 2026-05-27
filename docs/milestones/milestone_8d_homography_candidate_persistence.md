# Milestone 8D - Homography Candidate Persistence

Status: COMPLETE

Milestone 8D adds candidate homography persistence to Blueprint 8.

## Result

TOM can now build homography candidate observations from persisted court evidence:

```text
indexed media
-> run-fixture-court
-> court keypoint observations
-> court line observations
-> camera/view observations
-> build-homography-candidates
-> homography_candidate_observation rows
-> source evidence lineage
```

## What Was Added

- `apps.worker.services.homography_candidate_builder`
- worker CLI `build-homography-candidates`
- Makefile `homography-candidates`
- candidate matrix computation from persisted court keypoints
- model registry, runtime config, processing run, and processing step provenance
- `homography_candidate_observation` persistence through `ObservationWriter`
- lineage from source keypoints, source lines, and camera/view context
- tests for plan mode, candidate computation, persistence, insufficient source evidence, CLI handler, and lineage

## Evidence Boundary

Homography candidates remain candidate geometry evidence. They do not confirm a court model, validate camera geometry, project ball/player observations into court space, or imply tennis-event meaning.

## Non-Goals Preserved

8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, stream ingestion, or adjudication.
