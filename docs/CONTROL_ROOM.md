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
- Blueprint 7: IN PROGRESS
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

It remains intentionally non-decisive about tennis meaning. It does not include real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, real stream ingestion, or TOM v2-style adjudication.

Blueprint 6 Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Future real live ingestion and future tennis intelligence must begin as new blueprints.

Blueprint 7 Status: IN PROGRESS

Blueprint 7 starts the real perception runtime for the replay workstation. Milestones 7A and 7B add optional real YOLO detection replay and validate it in the operator UI: indexed media frames are sampled from media-owned timing, mapped real YOLO outputs are persisted as atomic `ball_detection` and `player_detection` observations, and the existing replay workstation displays them through `detectionRunId` with source/runtime/model/config context.

Blueprint 7 still records evidence only. Real model output is not confirmed tennis state.

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

## Explicitly Absent Capabilities

- Real pose inference.
- Movement interpretation or biomechanics conclusions.
- Stroke classification.
- Homography or court-space reasoning.
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
- Real pose inference is not included.
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

Status: IN PROGRESS

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

7A/7B do not add tracklet generation from real detections, real pose inference, homography, stream ingestion, tennis-event interpretation, or adjudication.

## Future Blueprint Candidates

Future work should be separate from TOM v3 Simple completion:

- Real live stream ingestion.
- Real pose runtime integration.
- Real tracklet candidate generation from real detection runs.
- Homography / court-space evidence.
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
