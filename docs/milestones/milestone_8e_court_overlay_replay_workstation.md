# Milestone 8E - Court Overlay in Replay Workstation

Status: complete

## Summary

Milestone 8E renders persisted Blueprint 8 court geometry evidence inside the existing replay workstation.

It adds replay API payloads and frontend layers for:

- court keypoint evidence
- court line evidence
- camera/view evidence
- homography candidates

The milestone remains observation-only. It does not compute projection diagnostics, project ball/player observations into court space, infer bounce/hit/in-out, or add tennis-event interpretation.

## Flow

```text
indexed media
-> run-fixture-court
-> build-homography-candidates
-> /replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>
-> court evidence overlays and timeline lanes
```

## Acceptance Notes

- `courtRunId` and `homographyRunId` are supported by replay URL/query wiring.
- Replay info exposes court and homography run groups.
- Replay overlays return court keypoints, court lines, camera/view rows, and homography candidates.
- The frontend renders image-pixel court keypoints/lines and display-only homography candidate template geometry.
- Stream Proxy Mode filters future court evidence the same way it filters existing replay evidence.
- Detection, tracklet, and pose replay behavior remains unchanged.

## Non-Goals Preserved

- No projection diagnostics.
- No real court model.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication.
