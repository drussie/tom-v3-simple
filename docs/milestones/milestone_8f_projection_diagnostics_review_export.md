# Milestone 8F - Projection Diagnostics / Review Export

Status: complete

## Summary

Milestone 8F adds projection diagnostic persistence and TOM-native court review export support for Blueprint 8 geometry evidence.

Projection diagnostics project the persisted court template geometry from homography candidates back into image-pixel space for review. Court review exports package court keypoint, court line, camera/view, homography candidate, projection diagnostic, lineage, artifact, and annotation evidence.

The milestone remains observation-only. It does not project ball/player observations into court space, infer bounce/hit/in-out, add scoring, or create accepted/rejected court lifecycle state.

## Flow

```text
indexed media
-> run-fixture-court
-> build-homography-candidates
-> build-projection-diagnostics
-> export-court-review-dataset
-> reviewable geometry evidence package
```

## Acceptance Notes

- `build-projection-diagnostics` validates media and homography run inputs.
- Projection diagnostic rows use `observation_family = court` and `observation_type = projection_diagnostic_observation`.
- Diagnostic rows preserve media-owned frame/time, projected template keypoints, projected template lines, metrics, and geometry-only metadata.
- Lineage links each projection diagnostic to its source homography candidate.
- No ball/player observations are diagnostic parents.
- `export-court-review-dataset` creates a TOM-native JSON export and evidence artifact.
- Replay payloads and the replay workstation can include projection diagnostics through `projectionDiagnosticRunId`.

## Non-Goals Preserved

- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No accepted/rejected court lifecycle.
- No real court model inference.
- No adjudication.
