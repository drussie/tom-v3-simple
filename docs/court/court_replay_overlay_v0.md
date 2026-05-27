# Court Replay Overlay v0

Milestone 8E renders persisted court geometry evidence in the existing replay workstation.

The 8E flow is:

```text
indexed media
-> run-fixture-court
-> courtRunId
-> build-homography-candidates
-> homographyRunId
-> /replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>
-> court keypoint, court line, camera/view, and homography candidate evidence overlays
```

Court overlays are display-only evidence. They do not create projection diagnostic observations, project ball/player observations into court space, infer bounce/hit/in-out, or confirm court truth.

## Replay API

`GET /replay/overlays` accepts:

- `court_run_id`
- `homography_run_id`
- `layers=court_keypoints,court_lines,camera_view,homography_candidates`

The payload adds:

- `court_keypoints`
- `court_lines`
- `camera_view`
- `homography_candidates`

Existing detection, tracklet, and pose payload fields are unchanged.

`GET /replay/timeline` accepts the same court run ids and adds lanes:

- Court keypoint evidence
- Court line evidence
- Camera/view evidence
- Homography candidates

## Workstation Behavior

The replay workstation adds toggles and run selectors for court evidence and homography candidates. When selected, it can draw:

- persisted court keypoint evidence in image-pixel coordinates
- persisted court line evidence in image-pixel coordinates
- camera/view evidence as a current-frame badge and timeline lane
- homography candidate template geometry by applying the stored inverse matrix to the normalized court template

The homography overlay is display-only. It does not write projection diagnostics or court-space ball/player projections.

## Selected Detail

Selected court evidence detail shows source observation ids, run/model/runtime/config context, frame/time, confidence, source lineage ids where available, and evidence-only warnings.

Use labels such as:

- Court keypoint evidence
- Court line evidence
- Camera/view evidence
- Homography candidate
- Candidate geometry evidence only

Avoid labels such as:

- confirmed court
- true homography
- verified geometry
- in/out
- bounce location
- point result

## Non-Goals

8E does not add:

- projection diagnostics
- ball/player court-space projection
- real court model inference
- bounce/hit/in-out/rally/point/scoring
- real stream ingestion
- adjudication
