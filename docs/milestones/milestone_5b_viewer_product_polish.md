# Milestone 5B - Viewer / Product Polish

## Status

Status: complete.

## Goal

Polish the existing TOM v3 Simple viewer and product surface so the local fixture demo is easier to understand, inspect, and explain.

This milestone does not add model runtime capability or tennis interpretation. It makes persisted detection observations, tracklet candidates, pose observations, lineage, artifacts, annotations, and review exports clearer in the existing Evidence Viewer.

## What Changed

- Added a shared frontend wording helper for observation names, source runtime, frame-time ownership, relationship descriptions, annotation labels, keypoint annotation metadata, and review export artifact summaries.
- Added a run evidence summary panel that shows processing-run context, observation counts, lineage counts, annotation counts, runtime config, and visible review export artifacts.
- Added clearer empty states for missing observations, detection overlays, pose overlays, tracklet bundles, lineage, artifacts, annotations, and review exports.
- Updated detection, tracklet, pose, lineage, artifact, annotation, and detail panels to use observation/evidence/candidate language.
- Made tracklet relationships more readable while keeping raw relationship types visible as technical detail.
- Made annotation rows show review-only context, notes, demo/review flags, and keypoint-level metadata when present.
- Added focused viewer payload assertions to the local demo test so detection, tracklet, pose, lineage, artifact, annotation, and export payloads remain available to the viewer.

## Viewer Path

```text
demo run ids
-> viewer run payload
-> run evidence summary
-> observation list
-> detection / tracklet / pose panels
-> lineage / artifact / annotation panels
-> review export summaries when present
```

## Evidence Boundary

The viewer describes outputs as observations, evidence, candidates, source context, and review annotations.

Fixture and model outputs are not presented as tennis understanding. This milestone does not add real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Validation

Milestone 5B adds focused coverage that the demo viewer payload still includes:

- detection observations, frame artifacts, and annotations
- tracklet candidate observations, lineage, annotations, and export artifacts
- pose observations, typed pose detail, annotations, and export artifacts

Full project validation is recorded in the 5B agent report.
