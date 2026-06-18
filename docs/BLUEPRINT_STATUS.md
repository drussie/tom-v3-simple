# TOM v3 Simple Blueprint Status

## Overview

- Blueprint 1: COMPLETE
- Blueprint 2: COMPLETE
- Blueprint 3: COMPLETE
- Blueprint 4: COMPLETE
- Blueprint 5: COMPLETE
- Blueprint 6: COMPLETE
- Blueprint 7: COMPLETE
- Blueprint 8: COMPLETE / FROZEN
- Blueprint 9: COMPLETE
- Blueprint 10: COMPLETE
- Blueprint 11: COMPLETE
- Blueprint 12: COMPLETE
- Blueprint 13: COMPLETE
- Blueprint 14: COMPLETE
- Blueprint 15: COMPLETE
- Blueprint 16: COMPLETE
- Blueprint 17: COMPLETE
- Blueprint 18: COMPLETE
- Blueprint 19: COMPLETE
- Blueprint 20: COMPLETE
- Blueprint 21: COMPLETE
- Blueprint 22: COMPLETE
- Blueprint 23: COMPLETE
- Blueprint 24: COMPLETE
- Blueprint 25: COMPLETE
- Blueprint 26: COMPLETE
- Blueprint 27: COMPLETE
- Blueprint 28: COMPLETE
- Blueprint 29: COMPLETE
- Blueprint 30: COMPLETE
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. Blueprint 6 is complete as the visual replay/operator workstation layer. Blueprint 7 is complete as the real perception runtime layer for optional real detection, real-detection-derived candidate tracklets, and optional real pose keypoint evidence. Blueprint 8 is frozen as the visual evidence workstation milestone: real/fixture court evidence, smoothed motion candidates, court projection candidates, ball trajectory candidates, hit/bounce event candidates, marker-level arbitration, replay marker inspection, event candidate review, and point evidence snapshots remain candidate evidence only. Blueprint 9 is complete with manual candidate review annotations that attach operator metadata to candidate markers and missing-candidate moments without creating truth or adjudication. Blueprint 10 is complete with a read-only evaluation harness that summarizes generated candidate markers and Blueprint 9 review metadata. Blueprint 11 is complete with declared camera/court geometry evidence for future 3D readiness. Blueprint 12 is complete with provisional 3D ball trajectory candidate evidence that keeps height unknown by default and does not create 3D truth. Blueprints 13 through 16 add diagnostic-only 3D marker context, a display-only 3D Debug View, replay-time/selection coupling, and 3D debug review annotations without creating 3D truth, hit/bounce truth, in/out, score, or adjudication. Blueprints 17 through 19 add reviewed 3D debug dataset export, export-to-export regression reporting, and a local sample-point baseline gate without treating exported labels or baselines as truth. Blueprint 20 freezes the sample-point completion/readiness review and permits only controlled second-point expansion under the same candidate-only contract. Blueprint 21 adds that controlled second-point ingestion/replay smoke path without claiming generalization. Blueprint 22 turns that smoke into a second-point evidence parity manifest and protected baseline checkpoint. Blueprint 23 adds point-level provenance manifests. Blueprint 24 builds a manifest-backed multi-point replay navigator and index. Blueprint 25 adds a manifest-backed multi-point regression matrix. Blueprint 26 adds an observation-quality taxonomy and conservative profile. Blueprint 27 adds a structured human-review label schema and validator. Blueprint 28 adds a human-provided reviewer confidence and ambiguity metadata schema and validator. Blueprint 29 adds a multi-reviewer disagreement schema and structural report while still making no truth, in/out, score, winner, player identity, reviewer ranking, reviewer scoring, disagreement resolution, generalization, correctness, or adjudication claim. Blueprint 30 adds an INTENNSE label alignment contract that bridges TOM evidence/review/provenance structures to future external INTENNSE expert label references without importing labels, validating correctness, resolving disagreement, creating coaching/tactical conclusions, or adjudicating evidence.

## Blueprint 1 - Media, Observation Store, Viewer Foundation

Status: COMPLETE

Proved:

```text
real media
-> indexed media asset
-> observation store
-> queryable evidence
-> visual evidence viewer
-> frame-backed detection evidence
```

Did not add:

- candidate tracklet review/export completion
- optional real YOLO runtime
- pose evidence
- tennis-event interpretation
- scoring
- adjudication

## Blueprint 2 - Temporal Evidence Tracklet Candidate System

Status: COMPLETE

Proved:

```text
persisted detections
-> candidate tracklets
-> track point candidates
-> lineage to source detections
-> multi-run evidence bundle
-> query
-> review annotation
-> exportable review dataset
```

Did not add:

- pose
- homography
- bounce or hit detection
- rally/point/scoring
- identity proof
- adjudication

## Blueprint 3 - Optional YOLO Runtime / Detection Observation Adapter

Status: COMPLETE

Proved:

```text
optional YOLO runtime
-> runtime probe / device resolver
-> local weights validation
-> model_registry metadata
-> YOLO-like normalization
-> guarded frame inference provider
-> existing detection adapter persistence
-> atomic ball/player observations
-> existing viewer, frame artifact, tracklet, review, and export paths
```

Did not add:

- YOLO tracking mode
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- identity proof
- adjudication

## Blueprint 4 - Pose Observation / Movement Evidence Layer

Status: COMPLETE

Proved:

```text
pose schema
-> COCO17 skeleton registry
-> fake / serialized pose normalization
-> fixture pose processing run
-> persisted pose observation
-> source candidate lineage
-> pose overlay viewer
-> pose query
-> review annotation support
-> TOM-native pose review export
```

Did not add:

- real pose inference
- movement interpretation
- stroke classification
- serve/hit/split-step/biomechanics conclusions
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

## Blueprint 5 - Simple Completion / Product Hardening

Status: COMPLETE

Completed:

- 5A: canonical local fixture demo and runbook
- 5B: viewer/product polish
- 5C: final evidence/provenance audit
- 5D: docs/control-room consolidation
- 5E: final completion review

Final proof path:

```text
fixture demo
-> viewer inspection
-> review annotations
-> exports
-> provenance audit
-> canonical docs
-> final completion review
```

Blueprint 5 proved that TOM v3 Simple can be run, inspected, audited, explained, and demoed locally without adding tennis interpretation capability.

Blueprint 5 did not add real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, streaming, or adjudication.

## Blueprint 6 - Visual Replay / Live Observation Workstation

Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Milestone 6A proved:

```text
indexed media asset
-> browser-usable local video URL
-> replay info payload
-> frontend replay route
-> HTML video player
-> current TOM timestamp/frame display
-> timeline shell
-> available run context
```

Milestone 6A did not add:

- detection overlay playback
- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6B proved:

```text
indexed video playback
-> current TOM timestamp/frame
-> detection overlay chunk endpoint
-> persisted ball/player bbox overlays
-> detection layer toggle
-> detection run selection
-> click-to-select detection observation detail
```

Milestone 6B did not add:

- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6C proved:

```text
indexed video playback
-> current TOM timestamp/frame
-> detection overlay chunks
-> tracklet candidate overlay chunks
-> pose keypoint overlay chunks
-> synchronized bbox / point / skeleton rendering
-> click-to-select persisted evidence details
```

Milestone 6C did not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6D proved:

```text
indexed video playback
-> synchronized detection / tracklet / pose overlays
-> replay timeline endpoint
-> evidence lanes
-> detection ticks
-> tracklet candidate spans
-> pose ticks
-> review annotation markers
-> click-to-seek/select persisted evidence
```

Milestone 6D did not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6E proved:

```text
indexed video playback
-> Replay / Stream Proxy mode toggle
-> video-as-live live edge
-> hidden future overlays
-> hidden future timeline evidence
-> operator pause/review state
-> return-to-live-edge control
```

Milestone 6E did not add:

- real live stream ingestion
- HLS/RTSP/HDMI/camera capture
- websocket live updates
- model scheduling
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6F proved:

```text
Replay Mode
-> Stream Proxy Mode
-> synchronized detection / tracklet / pose evidence overlays
-> evidence timeline lanes
-> click-to-seek/select persisted evidence
-> hidden future evidence in Stream Proxy Mode
-> Blueprint 6 completion review
```

Milestone 6F did not add:

- real live stream ingestion
- HLS/RTSP/HDMI/camera capture
- stream backend/session tables
- websocket live updates
- live model scheduling
- real pose inference
- tennis-event interpretation
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Future real live ingestion and future tennis intelligence must begin as new blueprints.

## Blueprint 7 - Real Perception Runtime For Replay Workstation

Status: COMPLETE

Blueprint 7 mission:

```text
indexed video
-> real perception runtime
-> persisted model-output observations
-> replay workstation overlays
```

Milestone 7A proved:

```text
indexed media
-> optional YOLO runtime and local weights
-> media-owned frame sampling
-> explicit class mapping
-> real YOLO frame inference
-> persisted atomic ball/player detection observations
-> replay URL with real detectionRunId
```

Milestone 7B validates:

```text
real YOLO detection run
-> replay-info available run source metadata
-> real-vs-fixture run selector labels
-> overlay payload source/runtime/model/config metadata
-> selected detection detail source context
-> timeline detection source labels
```

Milestone 7C proves:

```text
real model-output detection observations
-> candidate tracklet builder
-> real-detection-derived tracklet run
-> track point candidates
-> lineage to source detections
-> replay URL with detectionRunId and trackletRunId
```

Milestone 7D proves:

```text
indexed media
-> optional pose runtime and local weights
-> crop-from-player-detection or full-frame pose inference
-> normalized COCO17 keypoint evidence
-> persisted player_pose_observation rows
-> lineage to source player detections when available
-> replay URL with poseRunId
```

Milestone 7E decides:

```text
court / camera / homography scope review
-> geometry evidence contract proposal
-> Blueprint 8 candidate
-> implementation deferred
```

Milestone 7F closes Blueprint 7:

```text
real perception ladder
-> final orchestration runbook
-> completion review
-> Blueprint 8 boundary preserved
```

Blueprint 7 Status: COMPLETE

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Milestones 7A/7B/7C/7D/7E/7F do not add:

- movement interpretation or biomechanics conclusions
- homography or court-space reasoning
- court/camera/homography runtime
- stream ingestion
- bounce or hit detection
- rally/point/scoring
- identity resolution or ball-path conclusions
- adjudication

Court/camera/homography runtime work is future Blueprint 8 milestone work.

Remaining Blueprint 7 milestones: none.

## Blueprint 8 - Court / Camera / Homography Evidence Layer

Status: COMPLETE / FROZEN

Blueprint 8 mission:

```text
indexed video
-> court / camera evidence
-> homography candidates
-> projection diagnostics
-> replayable geometry evidence
-> object-to-court projection candidates
-> ball trajectory candidates
-> hit/bounce event candidates
-> marker-level arbitration
-> replay review panels
-> point evidence snapshots
```

Milestone 8A proves:

```text
observation spine
-> court keypoint typed rows
-> court line typed rows
-> camera/view typed rows
-> homography candidate typed rows
-> projection diagnostic typed rows
-> lineage-ready geometry evidence
```

8A adds schema contracts, typed storage tables, migration, a normalized court template registry, observation writer support, lineage relationship constants, and fake persistence tests.

Milestone 8B proves:

```text
indexed media
-> fixture court evidence adapter
-> media-owned frame sampling
-> court keypoint observations
-> court line observations
-> camera/view observations
-> model/runtime/run/step provenance
```

8B adds worker `run-fixture-court`, Makefile `court-fixture`, deterministic fixture geometry, and adapter persistence tests.

Milestone 8C proves:

```text
fixture camera/view observations
-> camera/view query service
-> camera/view summary read model
-> camera/view evidence bundle
-> /court/camera-view API
```

8C adds read-only query, summary, and bundle access for camera/view geometry context evidence. It does not create new camera/view rows beyond the 8B fixture adapter path.

Milestone 8D proves:

```text
fixture court evidence
-> source court keypoint observations
-> source court line observations
-> source camera/view observations
-> homography candidate builder
-> homography_candidate_observation rows
-> source evidence lineage
```

8D adds worker `build-homography-candidates`, Makefile `homography-candidates`, candidate matrix computation, reprojection metrics, model/runtime/run/step provenance, and lineage from source keypoints, lines, and camera/view context.

8D does not add:

- real camera/view model
- projection diagnostics
- replay court overlay
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

Milestone 8E proves:

```text
persisted court evidence
-> replay overlay API
-> court keypoint overlays
-> court line overlays
-> camera/view evidence lane or badge
-> homography candidate display overlay
```

8E adds replay support for `courtRunId` and `homographyRunId`, court overlay payloads, frontend court layer toggles, selected court evidence details, and court timeline lanes.

8E does not add:

- projection diagnostics
- real camera/view model
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

Milestone 8F proves:

```text
homography candidate rows
-> projection diagnostic builder
-> projection_diagnostic_observation rows
-> projected court template keypoints/lines
-> diagnostic metrics
-> homography-to-diagnostic lineage
-> replay payload/detail support
-> court review dataset export
```

8F adds worker `build-projection-diagnostics`, Makefile `projection-diagnostics`, model/runtime/run/step provenance, `projection_diagnostic_observation` persistence, lineage from homography candidates, replay support for `projectionDiagnosticRunId`, worker `export-court-review-dataset`, Makefile `court-review-export`, TOM-native export artifacts, and tests for diagnostic and export boundaries.

8F does not add:

- ball/player court-space projection
- real camera/view model
- accepted/rejected court lifecycle
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

8B does not add:

- real court keypoint detector
- real court line detector
- homography computation
- projection diagnostics
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

8A does not add:

- real court keypoint detector
- real court line detector
- homography computation
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

## Blueprint 9 - Manual Candidate Review Annotation

Status: COMPLETE

Blueprint 9 proves:

```text
final hit/bounce candidate markers
-> operator review labels
-> missing-candidate notes
-> point evidence snapshot review summary
```

Review annotations are metadata only. They do not change generated candidate observations, final
marker counts, source evidence, in/out, score, accepted/rejected lifecycle, or adjudication.

## Blueprint 10 - Benchmark / Evaluation Harness

Status: COMPLETE

Blueprint 10 proves:

```text
event candidate run
+ Blueprint 9 review metadata
-> point candidate review evaluation report
```

The v0 harness summarizes generated hit/bounce candidate markers, rejection diagnostic counts,
review labels, missing-candidate notes, reviewed-marker coverage, and reviewed-only label fractions.
It does not compute precision/recall, create hit/bounce truth, decide in/out, score a point, promote
labels into truth, correct candidates, or adjudicate evidence.

## Blueprint 11 - 3D Readiness / Camera Geometry Evidence Layer

Status: COMPLETE

Blueprint 11 proves:

```text
media / court / homography / projection context
-> camera geometry evidence declaration
-> replay, snapshot, and evaluation geometry-readiness summaries
```

The v0 layer declares camera/court geometry metadata and unknown intrinsics/extrinsics placeholders
for future 3D evidence work. It does not create 3D ball trajectories, 3D truth, hit/bounce truth,
in/out, score, point state, accepted/rejected lifecycle, automatic correction, or adjudication.

## Blueprint 12 - 3D Ball Trajectory Candidate Evidence

Status: COMPLETE

Blueprint 12 proves:

```text
ball trajectory court candidates
+ camera geometry evidence
-> provisional 3D ball trajectory candidate evidence
-> replay, snapshot, and evaluation 3D-readiness summaries
```

The v0 layer persists metric court-plane x/y candidates from declared court dimensions and keeps
height unknown by default. It does not create true 3D reconstruction, verified ball height,
hit/bounce truth, in/out, score, point state, accepted/rejected lifecycle, automatic correction, or
adjudication.

## Blueprint 13 - 3D-Assisted Event Candidate Diagnostics

Status: COMPLETE

Blueprint 13 proves:

```text
final hit/bounce event markers
+ provisional 3D ball trajectory candidates
-> diagnostic-only per-marker 3D context
-> replay, snapshot, and evaluation summaries
```

The v0 layer records nearby 3D sample counts, nearest metric court-plane x/y, height status, and
conservative diagnostic labels. It does not change event classification, marker arbitration,
candidate counts, review annotations, in/out, score, point state, accepted/rejected lifecycle,
automatic correction, or adjudication.

## Blueprint 14 - 3D Trajectory Debug View

Status: COMPLETE

Blueprint 14 proves:

```text
provisional 3D ball trajectory candidates
+ selected hit/bounce marker diagnostics
-> replay 3D Debug View
```

The v0 view renders a top-down court-plane display of existing 3D candidate samples, unknown height
status, and selected-marker nearest 3D diagnostic context. It does not render a true 3D ball flight,
create height truth, change hit/bounce markers, decide in/out, score, or adjudicate evidence.

## Blueprint 15 - 3D Debug Selection / Timeline Coupling

Status: COMPLETE

Blueprint 15 proves:

```text
replay time / selected marker / clicked 3D sample
+ provisional 3D trajectory debug points
-> coupled display-only 3D inspection surface
```

The v0 panel highlights current-time nearest samples, local time-window samples, selected samples,
and selected-marker diagnostic samples. It can request replay seek through existing replay controls,
but it does not own playback time, mutate evidence, change hit/bounce markers, decide in/out,
score, or adjudicate.

## Blueprint 16 - 3D Debug Review Annotations

Status: COMPLETE

Blueprint 16 proves:

```text
selected 3D sample / selected diagnostic link / current replay time
-> 3D debug review annotation metadata
-> replay, snapshot, and evaluation summaries
```

Operators can mark 3D debug evidence as useful, wrong, unclear, needs review, missing a 3D sample,
bad 3D position, or bad diagnostic link. These labels are review metadata only. They do not change
3D candidates, 3D diagnostics, hit/bounce event candidates, in/out, score, or adjudication.

## Blueprint 17 - Reviewed 3D Debug Dataset Export

Status: COMPLETE

Blueprint 17 proves:

```text
reviewed 3D debug evidence
+ event marker review metadata
-> deterministic offline JSON/Markdown dataset export
```

The v0 export includes media/run identity, replay URL, camera geometry summary, 3D trajectory
summary, event marker context, 3D candidate rows, 3D diagnostic rows, 3D debug reviews, event
marker reviews, warnings, and limitations. It is for offline analysis, QA review, dataset curation,
and future training preparation only. Review labels are not truth or training truth, and the export
does not change live hit/bounce behavior, in/out, score, or adjudication.

## Blueprint 18 - Reviewed 3D Debug Dataset Regression Harness

Status: COMPLETE

Blueprint 18 proves:

```text
baseline reviewed 3D debug export
+ current reviewed 3D debug export
-> deterministic drift/regression report
```

The v0 regression harness compares summary counts, required section presence, warnings, event
markers, 3D candidates, 3D diagnostics, 3D debug reviews, and event marker reviews. Baseline exports
are not truth or training truth. Drift indicates export differences only; it does not change event
candidates, 3D candidates, review annotations, in/out, score, or adjudication.

## Blueprint 19 - Reviewed 3D Debug Baseline Freeze / Regression Gate

Status: COMPLETE

Blueprint 19 proves:

```text
sample_point reviewed 3D debug export
-> local baseline export + manifest
-> repeatable current export comparison gate
```

The v0 baseline workflow writes local baseline JSON/Markdown exports and a compact manifest, then
verifies a current export against that baseline through the Blueprint 18 regression report. The
baseline is not truth or training truth. The gate detects drift for review but does not change event
candidates, 3D candidates, review annotations, in/out, score, or adjudication.

## Blueprint 20 - sample_point Completion Review / Expansion Readiness Freeze

Status: COMPLETE

Blueprint 20 proves:

```text
sample_point evidence/review/export/regression profile
-> documented completion review
-> documented expansion readiness verdict
-> controlled second-point readiness gate
```

The review confirms the current `sample_point` profile: six event markers, three hit candidates,
three bounce candidates, 68 provisional 3D trajectory candidates with unknown height, six 3D
diagnostics, one event-marker review, zero 3D debug reviews, and a no-drift reviewed 3D debug
baseline gate. The readiness verdict allows one controlled second-point smoke only. It does not
create truth, training truth, in/out, score, point state, accepted/rejected lifecycle, or
adjudication.

## Blueprint 21 - Second Point Ingestion / Evidence Replay Smoke

Status: COMPLETE

Blueprint 21 proves:

```text
operator-provided local second point video
-> existing media indexing path
-> new media_id
-> Replay Workstation URL
```

The smoke command validates a local media path, indexes it through the existing media ingestion
path, and returns a replay URL. A second media asset with no event candidates and no 3D candidates
is valid for this milestone. This is a single additional evidence sample only; it is not a
generalization claim and does not create event logic, marker arbitration, 3D reconstruction, truth,
in/out, score, or adjudication.

## Blueprint 22 - Second Point Evidence Parity / Protected Baseline Gate

Status: COMPLETE

Blueprint 22 proves:

```text
operator-provided local second point video
-> existing media indexing path
-> Replay Workstation URL
-> second-point evidence profile
-> local baseline manifest
```

The parity command records which evidence layers currently exist for the second media asset and
writes a local manifest for that profile. It is valid for v0 to have only media/replay parity and no
event or 3D candidate layers. The second-point manifest is not truth, not a generalization claim,
and does not create or change event generation, marker arbitration, 3D generation, in/out, score, or
adjudication.

## Blueprint 23 - Point Manifest / Evidence Provenance Contract

Status: COMPLETE

Blueprint 23 proves:

```text
indexed media asset
-> optional event/3D/geometry evidence IDs
-> deterministic point_manifest_id
-> local point manifest JSON
```

The manifest records media source/storage provenance, a replay URL, associated run IDs when
provided, evidence availability booleans, profile counts, and explicit warning flags. It is a
provenance contract only. It does not create truth, training truth, 3D truth, player identity,
in/out, score, point winner, event generation, marker arbitration, 3D generation, generalization,
or adjudication.

## Blueprint 24 - Multi-Point Replay Navigation / Review Surface

Status: COMPLETE

Blueprint 24 proves:

```text
point manifest JSON files
-> read-only manifest discovery
-> local multi-point replay index
-> Replay Workstation point navigator
```

The index records manifest-backed points, replay URLs, associated run IDs, evidence availability,
profile counts, warning flags, and provenance-only labels for protected sample-point and
second-point stand-in contexts when safely inferable from manifest provenance. It is a navigation
and review surface only. It does not create observations, event candidates, 3D candidates, review
lifecycle decisions, truth, training truth, 3D truth, player identity, in/out, score, point winner,
generalization, or adjudication.

## Blueprint 25 - Multi-Point Regression Matrix / Baseline Expansion

Status: COMPLETE

Blueprint 25 proves:

```text
multi-point replay index
-> read-only evidence matrix
-> baseline/current matrix comparison
-> regression drift report
```

The matrix records manifest-backed points, replay URLs, associated run IDs, evidence availability,
profile counts, warning flags, and summary counts. It detects point presence, label, replay/run,
availability, count, and warning drift between baseline and current matrix artifacts. Added points
are additive/non-breaking by default; protected sample-point regressions and matrix contract
failures are breaking. The matrix is not truth, not a generalization claim, and does not create
observations, event candidates, 3D candidates, in/out, score, player identity, point winner, or
adjudication.

## Blueprint 26 - Observation Quality Taxonomy

Status: COMPLETE

Blueprint 26 proves:

```text
multi-point replay index
-> versioned observation-quality taxonomy
-> conservative observation-quality profile
-> review-support quality dimensions
```

The taxonomy records neutral quality dimensions, allowed values, and warning flags. The profile
reads existing replay-index rows only, preserves point manifest/media identity, replay URLs,
associated run IDs, evidence availability, profile counts, and provenance-only labels, and marks
visual quality as `unknown` unless reviewed by a human. Missing evidence is `unavailable`. The
taxonomy/profile contract is not truth, not a generalization claim, and does not inspect video,
create observations, event candidates, 3D candidates, in/out, score, player identity, point winner,
or adjudication.

## Blueprint 27 - Structured Review Label Schema

Status: COMPLETE

Blueprint 27 proves:

```text
future human review labels
-> versioned structured label schema
-> blank review-label bundle template
-> structural bundle validation
```

The schema records neutral label families, label definitions, value sets, provenance requirements,
validation rules, and warning flags. The template emits blank `not_assessed` human-review entries.
The validator checks structure, known label keys, allowed values, forbidden fields, and human-only
flags. It does not infer missing labels, create labels automatically, validate correctness, inspect
video, decide truth, create observations, event candidates, 3D candidates, in/out, score, player
identity, point winner, or adjudication.

## Blueprint 28 - Reviewer Confidence / Ambiguity Capture

Status: COMPLETE

Blueprint 28 proves:

```text
future human review uncertainty
-> versioned reviewer confidence and ambiguity schema
-> blank confidence bundle template
-> structural bundle validation
-> validation-only post-Codex helper
```

The schema records neutral reviewer confidence, ambiguity, ambiguity reason, evidence-sufficiency,
additional-review, time-spent, and review-context metadata. The template emits blank
`not_assessed` human-review entries. The validator checks structure, allowed values, optional
Blueprint 27 label keys, forbidden fields, and human-only flags. It does not infer missing
confidence, create labels automatically, validate correctness, judge confidence appropriateness,
inspect video, decide truth, create observations, event candidates, 3D candidates, in/out, score,
player identity, point winner, or adjudication.

## Blueprint 29 - Multi-Reviewer / Disagreement Foundation

Status: COMPLETE

Blueprint 29 proves:

```text
multiple human review inputs
-> versioned multi-reviewer review-set schema
-> blank multi-reviewer review-set template
-> referenced Blueprint 27/28 bundle validation
-> structural disagreement report
```

The schema records pseudonymous reviewer identity policy, reviewer entry definitions, disagreement
dimensions, value sets, provenance requirements, validation rules, and warning flags. The template
emits blank human-reviewer entries. The validator checks structure, reviewer IDs, forbidden fields,
disallowed identity fields, human-only flags, and referenced bundle structure when paths are
present. The report compares human-provided values structurally. It does not infer missing labels,
create labels automatically, validate correctness, say which reviewer is right, rank reviewers,
score reviewers, resolve disagreement, inspect video, decide truth, create observations, event
candidates, 3D candidates, in/out, score, player identity, point winner, or adjudication.

## Blueprint 30 - INTENNSE Label Alignment Contract

Status: COMPLETE

Blueprint 30 proves:

```text
TOM evidence/review/provenance structures
-> versioned INTENNSE alignment contract
-> blank alignment bundle template
-> TOM contract reference validation
-> structural alignment report
```

The contract records Blueprint 26 through 29 schema refs, alignment entities, alignment fields,
neutral value sets, provenance requirements, validation rules, and warning flags. The template
emits blank human-provided alignment entries. The validator checks structure, TOM contract
references, allowed entities/values, forbidden fields, and human-only flags. The report summarizes
reference presence and provenance issues structurally. It does not import INTENNSE labels, create
TOM labels, infer expert interpretation, validate correctness, resolve disagreement, inspect video,
decide truth, create observations, event candidates, 3D candidates, in/out, score, player identity,
point winner, coaching/tactical conclusions, match-outcome conclusions, or adjudication.
