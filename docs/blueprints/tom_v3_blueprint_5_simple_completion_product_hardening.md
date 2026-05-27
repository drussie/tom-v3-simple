# TOM v3 Blueprint 5 - Simple Completion / Product Hardening

## Status

Status: COMPLETE

Blueprint 5 is complete. It was the final lightweight completion and product-hardening pass for TOM v3 Simple.

## Mission

Finish TOM v3 Simple as a coherent local observation platform by hardening the demo path, viewer, provenance, runbook, documentation, known limitations, and completion checklist without adding new tennis interpretation capability.

## Starting Point

Blueprints 1, 2, 3, and 4 are complete.

TOM v3 Simple can already:

```text
real media
-> persisted detections
-> candidate tracklets
-> optional YOLO-origin detections
-> pose observation evidence
-> viewer inspection
-> review annotations
-> TOM-native exports
```

## Blueprint 5 Goal

Blueprint 5 should make the complete local loop easy to run, inspect, explain, and validate.

The canonical fixture path is:

```text
index media
-> fixture gameplay observations
-> fixture detections
-> frame artifacts
-> candidate tracklets
-> fixture pose observations
-> review annotations
-> review exports
-> viewer URLs
-> completion checklist
```

Milestone 5B adds product polish around that path:

```text
viewer run payload
-> run evidence summary
-> clearer empty states
-> observation/evidence/candidate wording
-> readable lineage/source context
-> artifact, annotation, and review export clarity
```

Milestone 5C adds provenance auditing around the completed demo state:

```text
fixture demo evidence
-> completion audit
-> media/run/step/observation integrity checks
-> typed-row and lineage checks
-> artifact, annotation, and export checks
-> PASS/WARN/FAIL JSON
```

Milestone 5D consolidates docs and repo memory around the current product state:

```text
README
-> RUNBOOK_LOCAL
-> CONTROL_ROOM
-> ARCHITECTURE
-> OBSERVATION_CONTRACT
-> BLUEPRINT_STATUS
-> KNOWN_LIMITATIONS
-> OPTIONAL_YOLO
-> EXPORTS
-> PROVENANCE_AUDIT
-> COMPLETION_CHECKLIST
```

## Boundaries

Blueprint 5 does not add:

- real pose inference
- movement interpretation
- stroke classification
- serve, hit, split-step, or biomechanics conclusions
- homography
- bounce detection
- hit detection
- rally or point reconstruction
- scoring
- adjudication
- production streaming
- auth or user permissions
- cloud deployment
- multi-camera reasoning

## Milestones

- Milestone 5A - Local Demo / Runbook Completion Path
- Milestone 5B - Viewer / Product Polish
- Milestone 5C - Final Evidence / Provenance Audit
- Milestone 5D - Docs / Control-Room Consolidation
- Milestone 5E - Final Completion Review

Milestone 5E is expected to be a short completion review, not a new capability milestone.

## Final Completion Statement

TOM v3 Simple Status: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

It remains intentionally non-decisive about tennis meaning. It does not include real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, streaming, or TOM v2-style adjudication.

Future work should start as a new blueprint.

## Completion Criteria

Blueprint 5 is complete when a new developer can:

- install TOM v3 Simple locally
- run the fixture demo without optional model assets
- open the viewer for demo runs
- inspect detections, tracklets, and pose observations
- see lineage and artifacts
- add or inspect review annotations
- export review datasets
- understand optional YOLO runtime separately
- understand known limitations and non-goals
- run the validation checklist

The platform should remain honest: fixture/demo evidence proves plumbing, not tennis understanding.

## Milestone 5B Status

Status: complete.

The Evidence Viewer now has clearer empty states, a run evidence summary, candidate/evidence wording, readable lineage descriptions, artifact/export metadata display, and annotation rows that expose review context and keypoint metadata when present.

This is product polish only. It does not add real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5C Status

Status: complete.

TOM v3 Simple now has a structural completion/provenance audit with worker `completion-audit`, Makefile `completion-audit`, demo-only/all-data scopes, strict mode, PASS/WARN/FAIL JSON, and tests proving the audit passes after the canonical fixture demo and catches broken references.

The audit checks evidence structure and provenance integrity only. It does not add model/runtime capability, real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5D Status

Status: complete.

TOM v3 Simple now has a consolidated canonical documentation set. README is concise and practical, `docs/RUNBOOK_LOCAL.md` remains the copy/pasteable local demo path, `docs/CONTROL_ROOM.md` is the current repo-memory/status document, and the architecture, observation contract, blueprint status, known limitations, optional YOLO, exports, provenance audit, and completion checklist docs describe the current platform without requiring milestone archaeology.

This is documentation consolidation only. It does not add new product behavior, model/runtime capability, real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, or adjudication.

## Milestone 5E Status

Status: complete.

Milestone 5E closes TOM v3 Simple with a final completion review, final agent report, final status updates, and final validation pass.

This is closeout only. It does not add new product behavior, model/runtime capability, real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, or adjudication.
