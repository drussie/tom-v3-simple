# TOM v3 Simple Control Room

This is the canonical repo-memory and status document for TOM v3 Simple.

## Mission

TOM v3 Simple is a local observation/evidence platform. It records media-backed observations, lineage, artifacts, review annotations, exports, and provenance checks.

It is not TOM v2, and it does not decide official tennis meaning.

## Current Completion Status

- Blueprint 1: COMPLETE
- Blueprint 2: COMPLETE
- Blueprint 3: COMPLETE
- Blueprint 4: COMPLETE
- Blueprint 5: COMPLETE
- Blueprint 6: COMPLETE
- Blueprint 7: COMPLETE
- Blueprint 8: IN PROGRESS
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

The completed TOM v3 Simple baseline remains intentionally non-decisive about tennis meaning. The fixture path does not require real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, real stream ingestion, or TOM v2-style adjudication.

Blueprint 6 Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Future real live ingestion and future tennis intelligence must begin as new blueprints.

Blueprint 7 Status: COMPLETE

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Court/camera/homography evidence now proceeds in Blueprint 8.

Blueprint 8 Status: IN PROGRESS

Blueprint 8 starts the court/camera/homography evidence layer. Milestone 8A adds court keypoint, court line, camera/view, homography candidate, and projection diagnostic schema contracts, typed storage tables, writer persistence support, a normalized court template registry, lineage constants, tests, and docs. Milestone 8B adds a deterministic fixture court evidence adapter that writes court keypoint, court line, and camera/view observations with model/runtime/run provenance. Milestone 8C makes camera/view observations queryable and inspectable as geometry context evidence with summary and evidence-bundle read models. Milestone 8D persists homography candidate observations from court keypoint, court line, and camera/view source evidence with lineage. Milestone 8E renders persisted court keypoints, court lines, camera/view evidence, and homography candidates in the replay workstation.

8E is still geometry evidence only. Homography overlays are display-only candidate layers, not court truth. 8E does not add projection diagnostics, real court model inference, ball/player court-space projection, stream ingestion, or tennis-event interpretation.

## Canonical Local Demo

Run:

```bash
make demo
make completion-audit
```

The fixture demo path is:

```text
media
-> fixture gameplay
-> fixture detections
-> frame artifacts
-> candidate tracklets
-> fixture pose observations
-> review annotations
-> pose and tracklet review exports
-> viewer URLs
-> provenance audit
```

The fixture demo does not require YOLO weights, real pose weights, GPU runtime, or network access.

## Observation-Only Invariant

TOM v3 Simple records evidence. It does not decide official tennis meaning.

An observation means an adapter, fixture, model output, or review workflow produced a record at a media-owned frame/time or interval.

An observation does not mean the output is correct, a tennis event happened, a subject identity is known, or a score exists.

## Completed Capabilities

- Local media indexing with ffprobe metadata, checksum, local copy/register modes, and frame/time summaries.
- Observation spine with typed detail rows.
- Fixture gameplay and detection adapters.
- Optional YOLO runtime probe, model registration, normalization, and guarded detection persistence path.
- Deterministic candidate tracklet builder from persisted detections.
- Tracklet evidence bundles, query, annotations, and TOM-native export.
- Pose schema, COCO17 skeleton registry, normalization, fixture persistence, lineage, overlay viewer, query, annotations, evidence bundles, and TOM-native export.
- Evidence Viewer with detection overlays, pose overlays, tracklet evidence, lineage, artifacts, annotations, and export summaries.
- Canonical fixture demo path and local runbook.
- Structural provenance audit for the demo path.
- Replay/operator workstation with Replay Mode, Stream Proxy Mode, synchronized detection/tracklet/pose evidence overlays, evidence timeline lanes, click-to-seek, and click-to-select persisted evidence.
- Optional real YOLO detection replay runs that persist real model-output detection observations for replay overlays.
- Replay run selectors and selected detection detail can distinguish real model-output detection runs from fixture/demo detection runs.
- Real-detection-derived candidate tracklet runs that preserve source detection ids and lineage.
- Optional real pose replay runs that persist real `player_pose_observation` rows with COCO17 keypoint evidence.
- Real pose crop mode can preserve lineage from source player detections to pose observations.
- Court/camera/homography evidence decision gate with a Blueprint 8 candidate contract.
- Blueprint 7 completion review and final perception orchestration runbook.
- Court/camera/homography schema, typed persistence foundation, fixture court evidence adapter, camera/view evidence read layer, homography candidate persistence, and replay court overlays for Blueprint 8.

## Explicitly Absent Capabilities

- Movement interpretation or biomechanics conclusions.
- Stroke classification.
- Confirmed homography, court truth, or court-space reasoning.
- Projection diagnostics and ball/player court-space projection.
- Real camera/view model inference.
- Bounce detection.
- Hit detection.
- Rally segmentation.
- Point reconstruction.
- Scoring.
- Production deployment, auth, cloud workflow, real stream ingestion, or multi-camera reasoning.

## Optional YOLO Path

YOLO is optional. The base environment remains lightweight.

Use:

```bash
make yolo-probe
make yolo-smoke
make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=./model_assets/yolo/<model>.pt
```

Real YOLO use requires optional dependencies and local weights. YOLO-origin detections are still observations, not final tennis meaning.

See [OPTIONAL_YOLO.md](OPTIONAL_YOLO.md).

## Known Limitations

The main limitation registry is [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

Short version:

- Fixture output is deterministic demo evidence.
- Optional YOLO quality depends on local runtime, weights, model classes, and source media.
- Optional real pose quality depends on local runtime, pose weights, source detections or frame sampling, and source media.
- Court/camera/homography evidence now proceeds in Blueprint 8 with schema persistence, fixture adapter foundations, camera/view query/bundle read models, homography candidate persistence, and replay court overlays.
- Candidate tracklets can be wrong or incomplete.
- Exports are TOM-native review datasets.
- Storage lifecycle is local/demo-oriented.

## Blueprint 5 Status

Milestones complete:

- 5A: Local Demo / Runbook Completion Path
- 5B: Viewer / Product Polish
- 5C: Final Evidence / Provenance Audit
- 5D: Docs / Control-Room Consolidation
- 5E: Final Completion Review

Remaining TOM v3 Simple milestones: none.

## Blueprint 6 Status

Status: COMPLETE

Milestone 6A added the replay workstation foundation:

```text
indexed media
-> browser video endpoint
-> replay info payload
-> /replay/<media_id>
-> current timestamp/frame display
-> timeline shell
-> selected run context
```

Milestone 6B adds the first synchronized observation overlay layer:

```text
current replay timestamp/frame
-> detection overlay chunk lookup
-> persisted ball/player bbox overlays
-> click-to-select detection observation detail
```

Milestone 6C adds candidate tracklet and pose evidence replay layers:

```text
current replay timestamp/frame
-> persisted candidate track points/paths
-> persisted pose keypoints/skeletons
-> click-to-select evidence detail
```

Milestone 6D adds evidence timeline navigation:

```text
replay timeline endpoint
-> detection observation ticks
-> tracklet candidate spans
-> pose observation ticks
-> review annotation markers
-> click-to-seek/select persisted evidence
```

6D deferred stream proxy mode, live stream ingestion, and tennis-event interpretation.

Milestone 6E adds Stream Proxy Mode:

```text
indexed local video
-> video-as-live operator mode
-> live-like edge
-> hidden future overlays
-> hidden future timeline evidence
-> pause/review state
-> return to live edge
```

6E still defers real live stream ingestion, streaming protocols, model scheduling, and tennis-event interpretation.

Milestone 6F closes Blueprint 6 with a completion review, final status updates, final validation, and explicit future blueprint boundaries.

Remaining Blueprint 6 milestones: none.

## Blueprint 7 Status

Status: COMPLETE

Milestone 7A adds real YOLO detection replay:

```text
indexed media
-> optional YOLO runtime / weights
-> media-owned frame sampling
-> explicit class mapping
-> persisted atomic detection observations
-> replay URL with detectionRunId
```

Milestone 7B validates real detection overlays in replay:

```text
real detection run
-> replay-info source metadata
-> source-aware run selector label
-> overlay/timeline source metadata
-> selected detection source/runtime/model/config detail
```

Milestone 7C builds candidate tracklets from real detection observations:

```text
real model-output detections
-> existing tracklet builder
-> candidate tracklet observations
-> track point candidates
-> lineage to source real detections
-> replay URL with detectionRunId and trackletRunId
```

Milestone 7D adds real pose keypoint replay:

```text
indexed media
-> optional pose runtime / weights
-> crop-from-player-detection or full-frame pose inference
-> persisted player_pose_observation rows
-> lineage to source player detections when available
-> replay URL with poseRunId
```

7A/7B/7C/7D do not add movement interpretation, stroke classification, biomechanics conclusions, homography, stream ingestion, tennis-event interpretation, or adjudication.

Milestone 7E is a court/homography decision gate:

```text
Blueprint 7 scope review
-> court/camera/homography evidence contract
-> Blueprint 8 candidate
-> no runtime implementation
```

7E decides that court/camera/homography belongs in Blueprint 8. It does not add schema migrations, runtime, replay court overlays, coordinate transforms, event interpretation, stream ingestion, or adjudication.

Milestone 7F closes Blueprint 7:

```text
fixture-safe demo
-> optional real detection
-> optional real-detection-derived tracklets
-> optional real pose
-> replay workstation URLs
-> Blueprint 8 boundary
```

7F adds completion review docs, consolidates the final local runbook, marks Blueprint 7 complete, and preserves the court/homography deferral. It adds no new runtime, schema, replay, stream, or tennis-event capability.

Remaining Blueprint 7 milestones: none.

## Blueprint 8 Status

Status: IN PROGRESS

Milestone 8A adds the court evidence schema contract:

```text
observation_family = court
-> court keypoint observations
-> court line observations
-> camera/view observations
-> homography candidates
-> projection diagnostics
-> normalized court template registry
```

8A adds database schema, typed Pydantic contracts, storage models, observation writer support, lineage relationship constants, schema/persistence tests, and docs. It does not add a court model adapter, homography computation, replay court overlay, ball/player court projection, event interpretation, stream ingestion, or adjudication.

Milestone 8B adds fixture court evidence:

```text
indexed media
-> fixture court evidence adapter
-> court keypoint observations
-> court line observations
-> camera/view observations
-> model/runtime/run provenance
```

8B adds worker `run-fixture-court`, Makefile `court-fixture`, deterministic media-owned frame sampling, and tests for adapter persistence. It does not add homography computation, projection diagnostics, replay court overlays, real court inference, ball/player court-space projection, event interpretation, stream ingestion, or adjudication.

Milestone 8C hardens camera/view evidence:

```text
fixture court run
-> camera_view_observation rows
-> camera/view query service
-> summary read model
-> evidence bundle
-> /court/camera-view API
```

8C adds read-only query, summary, and bundle APIs for camera/view geometry context evidence. It does not add homography computation, projection diagnostics, replay court overlays, real camera/court inference, ball/player court-space projection, event interpretation, stream ingestion, or adjudication.

Milestone 8D adds homography candidate persistence:

```text
fixture court run
-> court keypoint observations
-> court line observations
-> camera/view observations
-> homography candidate builder
-> homography_candidate_observation rows
-> source evidence lineage
```

8D adds worker `build-homography-candidates`, Makefile `homography-candidates`, candidate matrix computation, model/runtime/run/step provenance, and lineage from source keypoints, lines, and camera/view context. It does not add projection diagnostics, replay court overlays, real court inference, ball/player court-space projection, event interpretation, stream ingestion, or adjudication.

Milestone 8E adds court overlays in the replay workstation:

```text
courtRunId + homographyRunId
-> replay overlay API
-> court keypoint overlays
-> court line overlays
-> camera/view lane or badge
-> homography candidate display overlay
```

8E adds replay URL support for `courtRunId` and `homographyRunId`, overlay payloads for court keypoints, court lines, camera/view evidence, and homography candidates, frontend court layer toggles, selected evidence detail, and timeline lanes. It does not add projection diagnostics, real court inference, ball/player court-space projection, event interpretation, stream ingestion, or adjudication.

## Future Blueprint Candidates

Future work should be separate from TOM v3 Simple completion:

- Real live stream ingestion.
- Tracklet quality/evaluation workflows.
- Pose quality/evaluation workflows.
- Event candidate layers for bounce/hit/rally/point work.
- Product deployment, auth, storage lifecycle, and collaboration workflows.
- Larger-scale evaluation and model-quality workflows.

## Do-Not-Add-To-Simple List

Do not add these to TOM v3 Simple without explicitly starting a new blueprint:

- real pose inference
- movement interpretation
- stroke classification
- serve or hit conclusions
- bounce detection
- rally or point reconstruction
- scoring
- homography
- production auth/cloud/real stream ingestion
- adjudication
