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
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

It remains intentionally non-decisive about tennis meaning. It does not include real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, streaming, or TOM v2-style adjudication.

Future work should start as a new blueprint.

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
- Production deployment, auth, cloud workflow, streaming, or multi-camera reasoning.

## Optional YOLO Path

YOLO is optional. The base environment remains lightweight.

Use:

```bash
make yolo-probe
make yolo-smoke
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

## Future Blueprint Candidates

Future work should be separate from TOM v3 Simple completion:

- Real pose runtime integration.
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
- production auth/cloud/streaming
- adjudication
