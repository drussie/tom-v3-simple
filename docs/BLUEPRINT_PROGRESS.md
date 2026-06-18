# TOM v3 Simple - Blueprint Progress

## Current Progress Gauge

Current: Blueprints 1, 2, 3, 4, 5, 6, 7, and 8 complete/frozen; Blueprint 9 manual candidate review annotations are complete; Blueprint 10 benchmark/evaluation harness is complete; Blueprint 11 3D readiness / camera geometry evidence is complete; Blueprint 12 3D ball trajectory candidate evidence is complete; Blueprints 13 through 16 add diagnostic-only 3D marker context, the 3D Debug View, selection/timeline coupling, and 3D debug review annotations; Blueprint 17 exports reviewed 3D debug datasets; Blueprint 18 compares those exports for deterministic drift; Blueprint 19 freezes and verifies a local sample-point reviewed 3D debug baseline; Blueprint 20 completes the sample-point review and controlled expansion readiness freeze; Blueprint 21 adds a controlled second-point ingestion/replay smoke; Blueprint 22 adds second-point evidence parity and a local baseline manifest checkpoint; Blueprint 23 adds a point manifest / evidence provenance contract; Blueprint 24 adds manifest-backed multi-point replay navigation/review indexing; Blueprint 25 adds a manifest-backed multi-point regression matrix; TOM v3 Simple remains an observation-only evidence platform.

## Current

- Repo exists.
- Mission is defined.
- Observation-only boundary is agreed.
- Persistence-first design is selected.
- Gameplay/non-gameplay layer is first-class.
- Visual evidence viewer is first-class.
- GitHub-as-memory workflow is selected.
- Backend app exists.
- Initial database migrations exist.
- Core schema models exist.
- Observation writer exists.
- Media, run, model, runtime config, observation, artifact, and annotation APIs exist.
- Synthetic/dev insertion path exists.
- Worker CLI exists.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Candidate observations have lineage and artifacts.
- Visual evidence viewer foundation exists.
- Viewer data is loaded from backend/API contracts.
- Milestone 0 local setup and demo runbooks exist.
- Makefile commands exist for common local workflows.
- Integration smoke validation exists for synthetic viewer data.
- Real local media file registration exists.
- ffprobe-based metadata extraction exists.
- Media checksum and local storage copy/register modes exist.
- Central frame/time mapping utilities exist.
- Worker `index-media` exists.
- Gameplay adapter interface exists.
- Fixture gameplay adapter produces persisted view-state observations.
- TOM v1 portability assessment exists.
- Worker `run-gameplay-adapter` exists.
- Existing viewer can show gameplay bands from adapter runs.
- Detection adapter interface exists.
- Fixture detection adapter produces persisted ball/player atomic observations.
- YOLO26/Ultralytics portability assessment exists.
- Worker `run-detection-adapter` exists.
- Query/viewer paths can inspect detection observations.
- Detection overlay viewer transform exists.
- Persisted ball/player bboxes are visually inspectable in the viewer.
- Detection observations can be selected and highlighted in the overlay.
- Frame extraction service exists.
- Worker `extract-frame-artifacts` exists.
- Frame image artifacts are persisted as evidence artifacts.
- Viewer can display frame artifacts behind persisted detection bboxes.
- Tracklet builder service exists.
- Persisted detections can be grouped into candidate tracklets.
- Tracklet and track point rows are persisted.
- Tracklet candidates have first-class observation spine rows.
- Track point candidates have first-class observation spine rows.
- Observation lineage links source detections to track points and track points to tracklets.
- Tracklet evidence bundle service exists.
- Viewer can inspect source detection evidence from a tracklet builder run.
- Tracklet query service exists.
- Candidate tracklets are searchable by run, source run, family, subject, frame range, confidence, gaps, point count, and review annotations.
- Tracklet evidence bundles include annotation summaries.
- Viewer review controls can add annotations to tracklet, track point, and source detection observations.
- Tracklet review dataset export service exists.
- Candidate tracklet evidence can be exported by tracklet ids or by structured query filters.
- Export artifacts are persisted as local JSON files with `evidence_artifact` metadata and checksums.
- Query-based exports can persist `query_result` memory.
- Blueprint 2 completion review exists.
- Temporal evidence invariants are documented and validated.
- Blueprint 2 is complete.
- Blueprint 3 is complete.
- Base `tom_v3` does not require Ultralytics, Torch, or OpenCV imports.
- Optional YOLO dependency path exists in `requirements-yolo.txt`.
- YOLO runtime probe and device resolver exist.
- Worker `yolo-runtime-probe` reports optional dependency and device availability.
- Model weights and runtime assets are ignored by git.
- YOLO weights validation exists.
- Local weights are fingerprinted with sha256 and file size.
- Default ball/player YOLO class mapping exists and is validated.
- YOLO model registry helper exists.
- Worker `register-yolo-model` validates/registers weights without creating runs or observations.
- YOLO-like frame result normalization exists.
- Class mapping can normalize YOLO output to `ball_detection` and `player_detection`.
- `xyxy` boxes convert to TOM v3 bbox/center payloads.
- Unmapped classes and invalid boxes are counted without emitting observations.
- YOLO adapter skeleton can normalize fake frame results without real inference.
- YOLO frame inference provider boundary exists.
- Fake YOLO provider can drive deterministic persistence tests.
- Guarded Ultralytics provider can run frame-level prediction when optional runtime and weights are available.
- Worker detection adapter can persist mocked YOLO detections as atomic `ball_detection` and `player_detection` observations.
- YOLO runs can use registered model metadata and weights checksum validation.
- Failed YOLO runs do not persist fixture fallback detections.
- Local real-YOLO smoke helper exists.
- Smoke plan covers runtime probe, weights registration, media indexing, YOLO detection, frame artifacts, viewer inspection, and optional tracklet building.
- Missing runtime, weights, or media produce structured skipped smoke output.
- Blueprint 2 tracklet compatibility is documented for YOLO detection runs.
- Blueprint 3 completion review exists.
- Real model runtime invariants are documented and mapped to test coverage.
- Blueprint 3 is complete.
- Blueprint 4 is complete.
- Pose observation schema foundation exists.
- COCO17 skeleton registry exists.
- Keypoint schema validation helpers exist.
- `pose_observation` typed persistence exists.
- Synthetic/fake pose observations can be inserted with first-class observation spine rows.
- Pose observations use media-owned frame/time.
- Pose runtime config and model registry metadata contracts are documented.
- Pose adapter normalization exists for fake/serialized pose frame results.
- COCO17 keypoint names/indices are assigned from the skeleton registry during normalization.
- Missing keypoints are preserved as missing evidence.
- Bbox, confidence, crop projection, and subject association candidate normalization are tested.
- Normalized pose output can instantiate `PoseObservationCreate`.
- Pose processing service exists.
- Worker `run-pose-adapter` can persist fixture pose observations.
- Pose processing runs and steps are created for fixture pose runs.
- Normalized pose payloads are persisted through `ObservationWriter`.
- Source `player_detection` observations can link to pose observations through `pose_from_subject_detection_candidate` lineage.
- Unassociated full-frame fixture poses persist with no lineage.
- Viewer run payloads include typed pose detail.
- Existing Evidence Viewer can render pose observations.
- COCO17 skeleton edges and present keypoint markers render from persisted image-pixel coordinates.
- Missing keypoints remain missing evidence and are not drawn as present markers.
- Selected pose metadata, keypoint confidence rows, and source association candidate context are visible in the viewer.
- Pose query service and API exist.
- Pose observations are searchable by run/media/frame/time, confidence, missing keypoint count, skeleton format, and source association fields.
- Pose evidence bundle service and API exist.
- Pose annotations use the existing generic `human_annotation` path with pose labels and keypoint-level metadata.
- Pose review dataset export exists as TOM-native JSON with `evidence_artifact` metadata, checksum, and query result memory.
- Blueprint 4 completion review exists.
- Pose evidence invariants are documented and mapped to focused tests and viewer contracts.
- Blueprint 4 is complete.
- Blueprint 5 has started.
- Canonical local fixture demo path exists.
- Worker `run-demo` can exercise media indexing, fixture gameplay, fixture detections, frame artifacts, candidate tracklets, fixture pose observations, review annotations, and review exports.
- Makefile `demo`, `demo-plan`, `demo-reset`, `demo-export`, `demo-open`, `completion-check`, `yolo-probe`, and `yolo-smoke` targets exist.
- `docs/RUNBOOK_LOCAL.md` is the canonical copy/pasteable local runbook.
- Optional YOLO smoke remains separate from the fixture demo.
- Viewer product polish exists.
- Evidence Viewer includes a run evidence summary, clearer empty states, and consistent observation/evidence/candidate wording.
- Detection, tracklet, pose, lineage, artifact, and annotation panels expose source context and review metadata more clearly.
- Review export artifacts are summarized when present in the viewer payload.
- Completion/provenance audit service exists.
- Worker `completion-audit` returns PASS/WARN/FAIL-style JSON.
- Makefile `completion-audit` runs the demo-scoped audit.
- The audit checks media, processing runs/steps, observations, typed rows, candidate tracklets, pose rows, lineage, artifacts, annotations, and review exports.
- Demo completeness audit passes after `make demo` and fails clearly when no demo media exists.
- Canonical docs now describe the final-ish TOM v3 Simple state without requiring milestone archaeology.
- `docs/CONTROL_ROOM.md`, `docs/ARCHITECTURE.md`, `docs/OBSERVATION_CONTRACT.md`, `docs/BLUEPRINT_STATUS.md`, `docs/KNOWN_LIMITATIONS.md`, `docs/OPTIONAL_YOLO.md`, `docs/EXPORTS.md`, and `docs/COMPLETION_CHECKLIST.md` exist.
- README, local runbook, current-state, progress, implementation log, and control-room index point to the consolidated docs.
- Final completion review exists.
- TOM v3 Simple is marked complete in canonical docs.
- Blueprint 6 is complete as the visual replay/operator layer.
- Replay info and local video serving endpoints exist.
- Replay frame/time mapping helpers exist.
- Frontend `/replay/<media_id>` route exists.
- Replay page displays indexed video, current timestamp/frame, timeline shell, detection overlay playback, and available run context.
- Replay detection overlay endpoint exists for persisted ball/player detection observations.
- Replay page can fetch detection overlay chunks by media/time window and detection run.
- Replay page renders persisted detection bboxes over video playback.
- Detection overlay selection shows persisted detection observation details.
- Replay overlay endpoint can return tracklet candidate overlays and pose keypoint overlays.
- Replay page can fetch detection, tracklet, and pose overlay chunks together.
- Replay page renders candidate track points, selected candidate paths, pose bboxes, present keypoints, and COCO17 skeleton edges over video playback.
- Replay overlay selection shows persisted detection, tracklet candidate, track point candidate, and pose observation details.
- Replay timeline endpoint and frontend evidence lanes exist for detection ticks, tracklet candidate spans, pose ticks, and review annotation markers.
- Replay timeline items can seek playback and select persisted evidence detail.
- Replay workstation Stream Proxy Mode exists for video-as-live review over indexed local media.
- Stream Proxy Mode hides future overlays and future timeline evidence until the live-like edge reaches it.
- Stream Proxy Mode displays available evidence counts, pause/review state, lag, and return-to-live-edge control.
- Blueprint 6 completion review exists.
- Blueprint 6 is marked complete in canonical docs.
- Blueprint 7 has started as the real perception runtime for the replay workstation.
- Worker `run-real-detection` exists for optional real YOLO detection replay runs.
- Makefile `real-detection` exists.
- Real YOLO detection replay runs reuse runtime probing, weights validation, model registry, class mapping, frame inference, and atomic observation persistence.
- Real detection replay observations remain media-owned, observation-only model output.
- Replay-info detection run metadata distinguishes real model-output runs from fixture demo runs.
- Replay detection overlays and detection timeline items include optional source/runtime/model/config metadata for real detection validation.
- Replay selected detection detail displays source/runtime/model/config/class context when available.
- Candidate tracklets can be built from real model-output detection observations using the existing tracklet builder.
- Real-detection-derived tracklet runs preserve source detection run metadata and source detection observation lineage.
- Worker `run-real-pose` exists for optional real pose replay runs.
- Makefile `real-pose` exists.
- Real pose replay runs reuse optional runtime probing, local weights validation, model registry metadata, COCO17 pose normalization, and typed pose observation persistence.
- Real pose replay observations remain media-owned, observation-only model output.
- Crop-from-player-detection mode preserves source player detection lineage through `pose_from_subject_detection_candidate`.
- Replay-info pose run metadata distinguishes real pose model-output runs from fixture pose runs.
- Replay pose overlays and pose timeline items include optional source/runtime/model/config metadata for real pose validation.
- Replay selected pose detail displays source/runtime/model/config and subject association context when available.
- Court/homography decision gate exists.
- Court/camera/homography evidence has started as Blueprint 8 schema, fixture adapter, camera/view read-model work, homography candidate persistence, replay court overlays, projection diagnostics, and court review export.
- No court-space ball/player projection, movement interpretation, bounce, hit, rally, point, scoring, or adjudication has been added.
- Blueprint 7 completion review exists.
- Blueprint 7 is marked complete in canonical docs.
- Final real perception orchestration is documented for fixture-safe demo, optional real detection, optional real-detection-derived tracklets, and optional real pose replay.
- Blueprint 8 is complete/frozen as the current visual evidence platform milestone.
- Court keypoint, court line, camera/view, homography candidate, and projection diagnostic schema contracts exist.
- Court evidence typed storage tables and migration exist.
- Court template registry v0 exists.
- Fake court evidence can be persisted through the observation writer with lineage.
- Worker `run-fixture-court` exists.
- Makefile `court-fixture` exists.
- Fixture court evidence can persist court keypoint, court line, and camera/view observations with model/runtime/run/step provenance.
- Camera/view evidence query service exists.
- Camera/view evidence summary read model exists.
- Camera/view evidence bundle service exists.
- API endpoints under `/court/camera-view` expose camera/view query, summary, and bundle payloads.
- Worker `build-homography-candidates` exists.
- Makefile `homography-candidates` exists.
- Homography candidate observations can be persisted from court keypoint, court line, and camera/view source evidence.
- Homography candidate lineage links source keypoints, lines, and camera/view context.

## Blueprint 7 Status

Status: complete.

Milestone 7A starts Blueprint 7 with real YOLO detection replay:

```text
indexed media
-> optional YOLO runtime and local weights
-> media-owned frame sampling
-> explicit class mapping
-> real model-output atomic detection observations
-> replay workstation detection overlays
```

Milestone 7B validates real detection overlay use in the replay workstation:

```text
real detection run
-> source-aware replay-info
-> source-aware run selector labels
-> overlay/timeline source metadata
-> selected detection model/runtime/config detail
```

Milestone 7C builds candidate tracklets from real detection observations:

```text
real model-output detections
-> candidate tracklet builder
-> source-aware tracklet run metadata
-> track point candidates with source detection ids
-> replay tracklet overlays
```

Milestone 7D adds real pose replay runtime:

```text
indexed media
-> optional pose runtime and local weights
-> source player detections or sampled frames
-> COCO17 pose keypoint observations
-> source detection lineage when available
-> replay pose overlays
```

Milestone 7E is a court/homography evidence decision gate:

```text
Blueprint 7 real perception runtime
-> court/camera/homography scope review
-> future evidence contract
-> Blueprint 8 candidate
-> no implementation
```

Milestone 7F closes Blueprint 7:

```text
fixture-safe baseline
-> optional real YOLO detection
-> optional real-detection-derived tracklets
-> optional real pose replay
-> replay workstation URLs
-> Blueprint 8 court/homography boundary
```

Blueprint 7 progress after 7F: complete.

Remaining Blueprint 7 work: none. Future evaluation workflows, movement/stroke evidence, bounce/hit candidates, real stream ingestion, and product deployment should start as separate blueprints.

## Blueprint 8 Status

Status: complete / frozen.

Milestone 8A starts Blueprint 8 with court evidence schema and persistence:

```text
observation spine
-> court keypoint observation
-> court line observation
-> camera/view observation
-> homography candidate observation
-> projection diagnostic observation
```

Blueprint 8 progress after 8A: about 10-15%.

Milestone 8B adds fixture court keypoint, line, and camera/view evidence:

```text
indexed media
-> fixture court evidence adapter
-> court_keypoint_observation
-> court_line_observation
-> camera_view_observation
-> processing provenance
```

Blueprint 8 progress after 8B: about 25-30%.

Milestone 8C hardens camera/view evidence as geometry context:

```text
camera_view_observation
-> query filters
-> summary metrics
-> evidence bundle
-> /court/camera-view API
```

Blueprint 8 progress after 8C: about 35-40%.

Milestone 8D adds homography candidate persistence:

```text
court_keypoint_observation
+ court_line_observation
+ camera_view_observation
-> homography_candidate_observation
-> source evidence lineage
```

Blueprint 8 progress after 8D: about 50-55%.

Milestone 8E renders persisted court geometry evidence in replay:

```text
courtRunId + homographyRunId
-> replay overlay API
-> court keypoint evidence
-> court line evidence
-> camera/view evidence
-> homography candidate overlay
```

Blueprint 8 progress after 8E: about 65-70%.

Milestone 8F adds projection diagnostics and review export:

```text
homography_candidate_observation
-> projection_diagnostic_observation
-> projected template geometry
-> diagnostic metrics
-> court review dataset export
```

Blueprint 8 progress after 8F: about 80-85%.

Blueprint 8 Completion Review / Freeze v0 closes the blueprint as the current Visual Evidence
Platform milestone:

```text
real detections
-> smoothed motion candidates
-> court projection candidates
-> ball trajectory candidates
-> hit/bounce event candidates
-> marker-level arbitration
-> replay marker inspector
-> event candidate review panel
-> point evidence snapshot
```

Blueprint 8 is now frozen as candidate evidence only. It does not add truth promotion, in/out,
score, point winners, player identity, accepted/rejected lifecycle, manual correction, or
adjudication.

## Blueprint 9 Status

Status: complete.

Blueprint 9 Manual Candidate Review Annotation v0 adds operator review metadata for event candidate
markers and missing-candidate notes:

```text
hit/bounce candidate markers
-> operator review labels
-> missing-candidate notes
-> point evidence snapshot review summary
```

Review annotations are metadata only. They do not mutate generated candidate observations, change
marker counts, create accepted/rejected truth, or add in/out, score, point state, or adjudication.

## Blueprint 10 Status

Status: complete.

Blueprint 10 Benchmark / Evaluation Harness v0 adds read-only summaries over generated point
candidate markers and Blueprint 9 operator review metadata:

```text
event candidate run
+ operator review annotations
-> point candidate review evaluation
```

The v0 evaluator reports candidate counts, rejection diagnostic counts, reviewed/unreviewed marker
coverage, reviewed-only label fractions, candidate-type breakdowns, reviewed marker details, and
missing-candidate notes. It does not compute precision/recall in v0 and does not create truth,
automatic correction, in/out, score, point state, accepted/rejected lifecycle, or adjudication.

## Blueprint 11 Status

Status: complete.

Blueprint 11 3D Readiness / Camera Geometry Evidence Layer v0 adds declared camera/court geometry
evidence:

```text
court and projection context
-> declared camera geometry evidence
-> 3D-readiness summary
```

The v0 layer records court dimensions, geometry status, camera model, unknown
intrinsics/extrinsics placeholders, source run linkage, world-coordinate conventions, and
capability warnings. It prepares future 3D evidence layers without creating 3D trajectories, event
truth, in/out, score, point state, accepted/rejected lifecycle, or adjudication.

## Blueprint 12 Status

Status: complete.

Blueprint 12 3D Ball Trajectory Candidate Evidence v0 adds provisional 3D candidate evidence:

```text
ball trajectory court candidates
+ declared camera geometry
-> metric court-plane x/y candidates
-> unknown/default height diagnostics
-> 3D trajectory readiness summary
```

The v0 layer keeps `height_model = none_unknown` by default. It can record explicit court-plane
placeholder z only when requested, and the output remains candidate evidence only. It does not
change hit/bounce generation, marker arbitration, review labels, in/out, score, point state,
accepted/rejected lifecycle, automatic correction, or adjudication.

## Blueprint 5 Status

Status: complete.

Milestones 5A, 5B, 5C, 5D, and 5E are complete. TOM v3 Simple has a repeatable local fixture demo that proves the completed evidence loop without optional YOLO weights or real pose weights:

```text
media
-> fixture gameplay
-> fixture detections
-> frame artifacts
-> candidate tracklets
-> fixture pose observations
-> review annotations
-> TOM-native exports
-> viewer URLs
-> provenance audit
```

The viewer has also been polished with clearer empty states, run-level evidence summary, candidate/evidence wording, readable lineage descriptions, and review/export metadata display.

The completion audit checks local demo evidence structure across media, runs, steps, observations, typed rows, lineage, artifacts, annotations, and exports. The docs/control-room consolidation makes the current state readable without milestone archaeology. The final completion review confirms that TOM v3 Simple is complete enough to stop building and start using/demoing.

The docs/control-room consolidation now gives new developers a short canonical reading path:

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

Remaining Blueprint 5 work: none.

## Blueprint 6 Status

Status: complete.

Milestone 6A is complete. Blueprint 6 starts with Replay Mode:

```text
indexed media
-> replay info payload
-> browser video endpoint
-> /replay/<media_id>
-> HTML video playback
-> current timestamp/frame display
-> timeline shell
-> selected run context
```

Current Blueprint 6 progress: about 15-20%.

Milestone 6B is complete. It adds detection observation overlay playback only:

```text
current replay timestamp/frame
-> overlay chunk fetch
-> persisted ball/player detection boxes
-> click-to-select evidence detail
```

Current Blueprint 6 progress after 6B: about 30-35%.

Milestone 6C is complete. It adds tracklet candidate and pose keypoint evidence overlay playback:

```text
current replay timestamp/frame
-> overlay chunk fetch
-> persisted candidate track points/paths
-> persisted pose keypoints/skeletons
-> click-to-select evidence detail
```

Current Blueprint 6 progress after 6C: about 50-55%.

Milestone 6D is complete. It adds timeline lanes and evidence scrubbing:

```text
replay timeline endpoint
-> detection ticks
-> tracklet candidate spans
-> pose ticks
-> review annotation markers
-> click-to-seek/select evidence detail
```

Current Blueprint 6 progress after 6D: about 65-70%.

Milestone 6E is complete. It adds Stream Proxy Mode:

```text
indexed local video
-> video-as-live mode
-> live-like edge
-> hidden future overlays
-> hidden future timeline evidence
-> pause/review state
-> return to live edge
```

Current Blueprint 6 progress after 6E: about 80-85%.

Milestone 6F is complete. It closes Blueprint 6:

```text
Replay Mode
-> Stream Proxy Mode
-> synchronized detection / tracklet / pose evidence overlays
-> evidence timeline lanes
-> click-to-seek/select persisted evidence
-> hidden future evidence in Stream Proxy Mode
-> completion review
```

Current Blueprint 6 progress after 6F: 100%.

Remaining Blueprint 6 work: none.

## Milestone 5D Status

Status: complete.

Milestone 5D consolidates TOM v3 Simple repo memory into a concise canonical documentation set. README is now practical and short, `docs/CONTROL_ROOM.md` is the current status document, and the new architecture, observation contract, blueprint status, known limitations, optional YOLO, exports, and completion checklist docs describe the current platform without adding new implementation behavior.

## Milestone 5E Status

Status: complete.

Milestone 5E closes TOM v3 Simple with a final completion review, final agent report, final status updates, and final validation pass. The platform is complete as a lightweight local observation/evidence system. Future work should start as a separate blueprint.

## After Milestone 0A

Expected: ~30%

- Repo memory structure exists.
- Architecture docs exist.
- Observation-store schema direction exists.
- Future Codex agents have stable contracts.

## Milestone 0A Status

Status: complete.

The repo now has durable project memory, architecture docs, schema contracts, milestone docs, a handoff file, an agent report, and lightweight tracked skeleton directories for future implementation work.

## After Milestone 0B

Expected: ~40-45%

- Backend app exists.
- Initial database migrations exist.
- Core schema models exist.
- Observation writer exists.
- Media and run APIs exist.
- Observation query/detail APIs exist.
- Synthetic/dev insertion path exists.
- Worker CLI exists.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Candidate observations have lineage and artifacts.
- Docs and implementation log are updated.

## Milestone 0B Status

Status: complete.

The repo now has a tested backend/API foundation for media, runs, models, runtime configs, observations, lineage, artifacts, annotations, and dev synthetic persistence.

## After Milestone 0C

Expected: ~50-55%

- Worker package has executable entrypoints.
- Rich synthetic run generation exists outside the API route.
- Synthetic evidence is visual-viewer-ready.
- Track coverage and missingness are represented.
- Gameplay/non-gameplay/uncertain bands are persisted.
- Candidate observations have lineage and artifacts.
- API dev route reuses shared seeding code.
- Tests validate the worker/seeder path.

## Milestone 0C Status

Status: complete.

The repo now has a worker CLI and shared synthetic seeder that creates viewer-ready baseline observations for Milestone 0D.

## After Milestone 0D

Expected: ~65%

- `apps/web` has a working visual evidence viewer foundation.
- The viewer can load a run by run id.
- The viewer shows gameplay/non-gameplay/uncertain bands.
- The viewer shows ball, near-player, and far-player track coverage rows.
- The viewer shows homography valid/missing intervals.
- The viewer shows candidate markers.
- The viewer shows observation detail, lineage, and artifact metadata.
- Missingness is visible.

## Milestone 0D Status

Status: complete.

The repo now has a backend-composed viewer run endpoint and a Next.js web app that renders persisted synthetic evidence without adding real ML or a frontend-only evidence model.

## After Milestone 0E

Expected: ~75-80%

- Milestone 0 is consolidated.
- Repo docs are current and easy to follow.
- Local environment setup is documented.
- Local demo commands are documented and tested.
- Backend, worker, and web validation passes.
- Branch/default-branch cleanup is explicitly documented.
- The next real media/model milestone is ready.

## Milestone 0E Status

Status: complete.

The repo now has one documented local setup path, one synthetic seed path, one backend API, one viewer path, one validation story, and exact branch/default-branch cleanup guidance.

## After Milestone 1A

Expected: ~85%

- Real local media file registration exists.
- ffprobe-based duration, FPS, frame count, dimensions, codec, and format extraction exists.
- Media checksum and storage path are persisted.
- Frame/time mapping ownership is centralized in media indexing utilities.
- Viewer/API can load real media metadata before observations exist.
- Future gameplay/model adapters have a stable media substrate.

## Milestone 1A Status

Status: complete.

The repo now has real media indexing for local files, durable media registration, storage metadata, checksum persistence, frame/time summaries, API/worker entrypoints, tests, and docs.

## After Milestone 1B

Expected: ~90%

- First gameplay/view-state adapter seam exists.
- TOM v1 portability status is documented.
- Fixture gameplay adapter provides deterministic dev/test output.
- Gameplay adapter runs create model, config, run, and step records.
- Gameplay adapter output persists typed gameplay observations.
- Existing viewer can display gameplay/non_gameplay/uncertain bands from adapter runs.

## Milestone 1B Status

Status: complete.

The repo now has a stable TOM v3 gameplay adapter interface, fixture adapter, TOM v1 unavailable stub, worker CLI commands, persistence flow, viewer compatibility tests, and model adapter docs.

## After Milestone 1C

Expected: ~95%

- First ball/player detection adapter seam exists.
- YOLO26/Ultralytics portability status is documented.
- Fixture detection adapter provides deterministic dev/test output.
- Detection adapter runs create model, config, run, and step records.
- Detection adapter output persists typed atomic observations.
- Query API can retrieve ball_detection and player_detection observations.
- Existing viewer payload includes detection observations.

## Milestone 1C Status

Status: complete.

The repo now has a TOM v3 detection adapter interface, fixture detector, YOLO unavailable stub, worker CLI commands, atomic observation persistence flow, query/viewer compatibility tests, and model adapter docs.

## After Milestone 1D

Expected: ~100% for the TOM v3 Simple observation-platform MVP loop

- Persisted ball/player detections are visually inspectable.
- Existing viewer can render detection bboxes on a coordinate-space media panel.
- Detection observations can be selected from the timeline/list and highlighted in the overlay.
- Missing video playback does not block inspection.
- TOM v3 remains observation-only.

## Milestone 1D Status

Status: complete.

The repo now has a data-driven detection overlay layer that renders persisted bbox observations from the viewer payload without adding tracking, event inference, or a frontend-only detection model.

## After Milestone 1E

Expected: ~105% / MVP+ foundation

- Selected detection frames can have real frame image artifacts.
- Frame extraction service exists.
- Frame artifact metadata is persisted as evidence artifact rows.
- Viewer displays real frame imagery when available.
- Coordinate canvas fallback still works.
- TOM v3 remains observation-only.

## Milestone 1E Status

Status: complete.

The repo now has ffmpeg-backed frame artifact extraction, local artifact metadata persistence, artifact file serving for local development, and viewer support for drawing persisted detection bboxes over extracted frame imagery.

## After Milestone 1F

Expected: ~15% through the MVP+ temporal-evidence extension

- Tracklet foundation exists.
- Persisted detections can be grouped into tracklet candidates.
- `tracklet` and `track_point` rows are created from source observations.
- Existing viewer can show basic tracklet coverage/evidence.
- TOM v3 still does not claim identity, bounce, hit, rally, or point state.

## Milestone 1F Status

Status: complete.

The repo now has a deterministic tracklet-builder run path that creates candidate temporal groupings from persisted detection observations without mutating the source detection run or adding higher-level tennis event interpretation.

## After Milestone 2A

Expected: ~25% through the MVP+ temporal-evidence extension

- Tracklet candidates have observation spine rows.
- Track point candidates have observation spine rows.
- `tracklet.observation_id` points to a tracklet candidate observation.
- `track_point.observation_id` points to a track point candidate observation.
- Source detections are linked through `tracked_from` lineage.
- Track points are linked to tracklets through `grouped_from` lineage.
- Viewer/query paths can inspect candidate track observations.

## Milestone 2A Status

Status: complete.

The existing 1F branch now satisfies the Blueprint 2 persistence contract: candidate tracklets and track points are first-class observations with lineage to source detections and grouping observations.

## After Milestone 2B

Expected: ~55-60% through Blueprint 2

- A tracklet evidence bundle combines tracklet run evidence with source detection run evidence.
- Viewer can inspect a tracklet candidate and see its source detections.
- Viewer can drill from tracklet to track point to source detection.
- Frame artifacts are shown when available.
- Multi-run evidence remains descriptive and observation-only.

## Milestone 2B Status

Status: complete.

The repo now has a dynamic tracklet evidence bundle endpoint and a lightweight viewer panel for tracklet candidate, track point candidate, source detection, frame artifact, and lineage inspection across runs.

## After Milestone 2C

Expected: ~75% through Blueprint 2

- Tracklet candidates can be queried with structured review filters.
- Query responses include tracklet summaries, counts, annotation summaries, and evidence bundle URLs.
- Evidence bundles include tracklet, track point, and source detection annotation summaries.
- Viewer review controls can create annotations on selected candidate evidence.
- Query/review remains descriptive and observation-only.

## Milestone 2C Status

Status: complete.

The repo now has structured tracklet candidate query, evidence-bundle annotation summaries, and a viewer review flow that writes human annotations without mutating source observations, candidate track points, candidate tracklets, lineage, or artifacts.

## After Milestone 2D

Expected: ~90% through Blueprint 2

- Tracklet evidence bundles can be exported into durable review dataset artifacts.
- Reviewed candidate evidence can be packaged for future evaluation or training workflows.
- Export rows preserve media, run, model, config, lineage, artifact, and annotation provenance.
- Export artifacts carry explicit candidate-only and no-adjudication warnings.
- Export does not mutate source observations.

## Milestone 2D Status

Status: complete.

The repo now has a JSON review dataset export path for candidate tracklet evidence, available through both worker CLI and API, with persisted export artifact metadata and optional query result memory for query-based exports.

## After Milestone 2E

Expected: 100% through Blueprint 2

- Blueprint 2 completion review exists.
- Blueprint 2 status is complete.
- The 1F to 2A naming transition is documented.
- Temporal evidence invariants are documented and validated.
- Local runbook includes the complete Blueprint 2 flow.
- Next blueprint boundary is clear.

## Milestone 2E Status

Status: complete.

Blueprint 2 is complete. TOM v3 can build candidate tracklets from persisted detections, preserve source lineage, inspect evidence across runs, query and review candidates, and export review datasets without adding pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## After Milestone 3A

Expected: ~15-20% through Blueprint 3

- Base `tom_v3` remains lightweight.
- Optional YOLO dependency install path exists.
- Runtime probe can report Ultralytics, Torch, OpenCV, CUDA, and MPS availability.
- Device resolver can choose `cpu`, `mps`, or `cuda:0` safely.
- Missing runtime dependencies produce clear actionable diagnostics.
- Documentation explains how to create and validate `tom_v3_yolo`.
- No real YOLO detections are persisted yet.

## Milestone 3A Status

Status: complete.

The repo now has a clean optional YOLO runtime boundary with `requirements-yolo.txt`, import guards, runtime diagnostics, device resolution, worker probe command, weights ignore policy, tests, and docs. Blueprint 3 is prepared for model registry and weights validation without adding real inference, pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## After Milestone 3B

Expected: ~35-40% through Blueprint 3

- YOLO model registry contract exists.
- YOLO weights can be validated from local filesystem paths.
- Weights are fingerprinted with sha256 and file size.
- Required checksum mismatches fail clearly.
- Safe local root policy exists for `model_assets/yolo` and `weights/yolo`.
- Default ball/player class mapping exists.
- Optional model metadata probe can capture class names when runtime is available.
- Model registry rows can be created or reused for validated weights.
- No real YOLO detections are persisted yet.

## Milestone 3B Status

Status: complete.

The repo now has a YOLO weights validation and model registry foundation. Local weights can be validated, fingerprinted, mapped to TOM v3 ball/player observation targets, and registered in `model_registry` without creating processing runs or observations.

## After Milestone 3C

Expected: ~55-60% through Blueprint 3

- YOLO-like result normalization exists.
- Fake/serialized YOLO boxes can become TOM v3 detection payloads.
- Class-name and class-id mapping is tested.
- Bbox, center, confidence, class id, class name, and runtime metadata normalization is tested.
- Unmapped classes and invalid inputs are accounted for without persistence.
- YOLO adapter skeleton can prepare an adapter result from normalized output.
- No real full-media YOLO inference is required yet.
- No real YOLO detections are persisted yet.

## Milestone 3C Status

Status: complete.

The repo now has YOLO detection normalization foundations. YOLO-like frame result dictionaries can be transformed into TOM v3-compatible detection payloads and adapter results, ready for future observation persistence once real frame inference is introduced.

## After Milestone 3D

Expected: ~75-80% through Blueprint 3

- YOLO frame inference path exists behind the existing detection adapter interface.
- Real or mocked Ultralytics-style frame results can become `DetectionAdapterResult` output.
- The existing worker detection persistence path can write YOLO-origin `ball_detection` and `player_detection` observations.
- Persisted YOLO-origin observations use media-owned frame/time.
- Missing runtime, weights, checksum, or device failures do not create fake detections.
- Fixture adapter behavior remains unchanged.
- Existing viewer/query paths can inspect persisted YOLO-origin detections.
- No tracklets are created inside the YOLO adapter.

## Milestone 3D Status

Status: complete.

The repo now has a guarded YOLO frame inference and persistence bridge. Mocked provider tests prove YOLO-style frame outputs can be normalized and persisted as TOM v3 atomic detection observations through the existing worker path, while optional real Ultralytics runtime remains isolated behind import guards and registered local weights.

## After Milestone 3E

Expected: ~90-95% through Blueprint 3

- Real local `tom_v3_yolo` setup path is documented.
- Real YOLO runtime probe path is documented.
- Local weights registration path is documented.
- YOLO detection adapter run against indexed media is locally smoke-testable.
- Frame artifact and viewer overlay validation path is documented.
- Tracklet builder compatibility with YOLO detection runs is documented and smoke-testable.
- Missing runtime/assets skip safely.
- No real YOLO dependencies are required by default tests.

## Milestone 3E Status

Status: complete.

The repo now has an optional local real-YOLO smoke workflow through worker `smoke-real-yolo-local` and `scripts/smoke_real_yolo_local.py`. The helper can plan the workflow without assets, skips cleanly when optional runtime or weights are missing, and documents how YOLO-origin detections flow into the existing viewer and Blueprint 2 candidate tracklet path.

## After Milestone 3F

Expected: 100% through Blueprint 3

- Blueprint 3 completion review exists.
- Blueprint 3 status is complete.
- Real model runtime invariants are documented and mapped to existing tests.
- The local runbook describes the complete base-env and optional `tom_v3_yolo` paths.
- The YOLO observation persistence boundary is clear.
- Viewer and Blueprint 2 tracklet compatibility are documented.
- Next blueprint boundary is clear.

## Milestone 3F Status

Status: complete.

Blueprint 3 is complete. TOM v3 can keep YOLO runtime optional, validate and register local weights, normalize YOLO-like model outputs, persist YOLO-origin atomic detection observations through the existing detection pipeline, inspect them through the existing viewer/frame artifact path, and feed Blueprint 2 candidate tracklet/review/export workflows without adding pose, homography, bounce, hit, rally, point, scoring, YOLO tracking mode, or adjudication.

## After Milestone 4A

Expected: ~15-20% through Blueprint 4

- Pose has a first-class schema foundation.
- `pose_observation` typed rows connect to the central observation spine.
- COCO17 skeleton format and keypoint schema validation are centralized.
- Synthetic/fake pose observations can be inserted for persistence validation.
- Pose records are queryable through existing observation media/run/frame paths.
- Pose model registry and runtime config metadata contracts are documented.
- No real pose inference, pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4A Status

Status: complete.

The repo now has a Blueprint 4 pose evidence foundation: COCO17 skeleton metadata, keypoint validation helpers, pose schema models, a `pose_observation` table, writer support for pose typed extensions, and synthetic pose insertion tests that preserve media-owned frame/time. Pose remains observation evidence only.

## After Milestone 4B

Expected: ~35-40% through Blueprint 4

- Fake or serialized pose model output can normalize into TOM v3 pose payloads.
- COCO17 keypoint order and schema validation are reused.
- Full-frame pose output normalization exists.
- Crop-local to full-frame coordinate projection exists.
- Pose confidence and keypoint summary computation are tested.
- Normalized pose payloads are persistence-ready.
- No real pose runtime, pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4B Status

Status: complete.

The repo now has a pose adapter normalization foundation. Fake/serialized pose frame results can become `PoseObservationCreate`-compatible normalized pose observations with COCO17 keypoints, missing-keypoint preservation, bbox/confidence handling, crop projection, subject association candidate passthrough, and normalization-only adapter diagnostics.

## After Milestone 4C

Expected: ~55-60% through Blueprint 4

- Normalized pose payloads can be persisted through an explicit pose processing service.
- A pose `processing_run` and `processing_step` are created.
- Pose observations are written through `ObservationWriter`.
- Pose observations preserve media-owned frame/time.
- Pose observations can link to source `player_detection` observations.
- Candidate tracklet and track point relationship names are reserved for future pose context.
- Lineage rows explain the source evidence chain.
- No real pose runtime, pose overlay viewer, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4C Status

Status: complete.

The repo now has a pose persistence and lineage foundation. Worker `run-pose-adapter` creates fixture pose runs, persists typed `pose_observation` rows through the central observation writer, preserves media-owned frame/time, and links source `player_detection` observations to pose observations with `pose_from_subject_detection_candidate` lineage when candidate subject context is supplied.

## After Milestone 4D

Expected: ~70-75% through Blueprint 4

- Existing Evidence Viewer can render pose observations.
- Viewer payloads include typed `pose_observation` detail.
- COCO17 skeleton edges render from persisted keypoint evidence.
- Present keypoints render as markers.
- Missing keypoints remain missing evidence and are not drawn as present markers.
- Pose bbox renders when available.
- Selected pose metadata and keypoint confidence rows are visible.
- Source association candidate context is visible when supplied.
- No real pose runtime, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4D Status

Status: complete.

The repo now has a pose overlay viewer foundation. The existing Evidence Viewer can inspect persisted `player_pose_observation` rows, draw COCO17 keypoint evidence and skeleton edges in image-pixel coordinates, show selected pose metadata, list all keypoint present/missing states, and display source association candidate context without interpreting movement.

## After Milestone 4E

Expected: ~88-92% through Blueprint 4

- Pose observations can be queried with pose-specific filters.
- Pose evidence bundles include pose detail, source context, lineage, artifacts, and annotations.
- Pose observations can receive review annotations through the generic annotation API.
- Keypoint-level annotation metadata is supported in annotation payload JSON.
- Pose evidence can be exported as TOM-native review dataset JSON.
- Export artifacts are persisted with checksum and evidence artifact metadata.
- Run/media/query-based exports can persist query result memory.
- No real pose runtime, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4E Status

Status: complete.

The repo now has pose query, review, and export integration. Persisted `player_pose_observation` rows can be filtered by typed pose fields, inspected through a pose evidence bundle, annotated with review labels and keypoint metadata, and exported as review dataset artifacts without changing the underlying pose evidence.

## After Milestone 4F

Expected: 100% through Blueprint 4

- Blueprint 4 completion review exists.
- Blueprint 4 status is complete.
- Full pose evidence path is documented end to end.
- Pose schema, skeleton registry, normalization, persistence, lineage, viewer, query, review, and export invariants are documented.
- The local runbook describes the complete fixture pose validation path.
- Next blueprint boundary is clear.
- No real pose runtime, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication is added.

## Milestone 4F Status

Status: complete.

Blueprint 4 is complete. TOM v3 can persist pose model output as observation evidence with a first-class pose schema, COCO17 skeleton registry, keypoint validation, normalization, processing-run persistence, source candidate lineage, viewer overlay, pose-specific query filters, review annotation support, evidence bundles, and TOM-native review dataset export without adding real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.

## Blueprint 13 Status

Status: complete.

TOM v3 now has a diagnostic-only bridge from final hit/bounce event candidate markers to nearby
3D ball trajectory candidate samples. The bridge persists `event_candidate_3d_diagnostic` rows,
adds a CLI/Make workflow, and surfaces compact diagnostics in replay marker inspection, point
snapshots, and point candidate evaluations. It does not change event candidate counts or create
truth, in/out, score, or adjudication.

## Blueprint 14 Status

Status: complete.

TOM v3 now has a display-only 3D Debug View in Replay Workstation. The view loads existing
`ball_trajectory_3d_candidate` rows through the replay read model, renders court-plane metric x/y
candidate samples in a compact SVG court view, and highlights the nearest 3D diagnostic sample for
the selected hit/bounce marker when Blueprint 13 diagnostics are available. Height remains unknown
in v0, and the view does not create true 3D reconstruction, change event candidates, decide in/out,
score, or adjudicate evidence.

## Blueprint 15 Status

Status: complete.

The 3D Debug View is now coupled to replay time and selection. It highlights the 3D candidate
sample nearest to current replay time, emphasizes samples in the local ±250ms window, lets an
operator click or keyboard-select a sample to request video seek, displays selected sample
metadata, and continues to highlight the selected-marker nearest diagnostic sample when available.
The panel remains display-only and does not own playback time, mutate evidence, change
hit/bounce markers, decide in/out, score, or adjudicate.

## Blueprint 16 Status

Status: complete.

TOM v3 now supports operator review annotations for 3D Debug View evidence. Selected 3D candidate
samples, marker-linked 3D diagnostics, and missing 3D sample moments can receive review metadata
without changing source candidates or event markers. Point evidence snapshots and point candidate
evaluations include compact 3D debug review summaries. These reviews do not create 3D truth,
hit/bounce truth, in/out, score, or adjudication.

## Blueprint 17 Status

Status: complete.

TOM v3 can now export reviewed 3D debug evidence as deterministic offline JSON/Markdown dataset
artifacts. The export includes event markers, 3D candidate rows, 3D diagnostics, 3D debug reviews,
event marker reviews, camera geometry summary, replay URL, warnings, and limitations. The export is
read-only and does not change event candidates, marker arbitration, 3D candidates, 3D diagnostics,
review annotations, in/out, score, or adjudication. Review labels remain operator metadata, not
training truth.

## Blueprint 18 Status

Status: complete.

TOM v3 can now compare a current reviewed 3D debug dataset export against a saved baseline export
and produce deterministic JSON/Markdown drift reports. The regression harness compares summary
counts, section presence, warnings, event markers, 3D candidates, 3D diagnostics, 3D debug reviews,
and event marker reviews. Baseline exports are not truth or training truth, and drift does not change
event candidates, 3D candidates, review annotations, in/out, score, or adjudication.

## Blueprint 19 Status

Status: complete.

TOM v3 can now freeze the current sample-point reviewed 3D debug export as a local baseline with a
compact manifest, then verify future current exports against that baseline. The gate returns a
Blueprint 18 regression report and passes when no drift is detected. The baseline is not truth or
training truth, and the gate does not change event candidates, marker arbitration, 3D candidates,
3D diagnostics, review annotations, in/out, score, or adjudication.

## Blueprint 20 Status

Status: complete.

TOM v3 now has a documented `sample_point` completion review and expansion readiness checkpoint.
The frozen profile is six event markers, 68 provisional 3D trajectory candidates, six event
candidate 3D diagnostics, one event-marker review, zero 3D debug reviews, and a no-drift baseline
gate. The next recommended milestone is a controlled second-point ingestion/replay smoke, not
multi-point generalization or truth/adjudication.

## Blueprint 21 Status

Status: complete.

TOM v3 can now index a single operator-provided second-point video through the existing media path
and return a Replay Workstation URL. The smoke explicitly allows an empty candidate state for the
second media asset, preserves `sample_point` as the protected baseline, and does not claim
multi-point generalization.

## Blueprint 22 Status

Status: complete.

TOM v3 can now build a second-point evidence parity profile for one operator-provided local media
asset. The command indexes the media, returns a replay URL, records whether event candidates, 3D
candidates, and review annotations exist, and writes a local baseline manifest for the profile.
The manifest is not truth, not a generalization claim, and does not change event generation,
marker arbitration, 3D generation, in/out, score, or adjudication.

## Blueprint 23 Status

Status: complete.

TOM v3 can now build a point-level provenance manifest for an indexed media asset and optional
associated event candidate, 3D trajectory, and camera geometry evidence IDs. The manifest records a
deterministic `point_manifest_id`, media source/storage provenance, replay URL, TOM/Blueprint
provenance, evidence availability booleans, profile counts, and explicit warning flags. It is
observation-only and does not create truth, adjudication, scoring, player identity, event
generation, marker arbitration, 3D generation, or generalization claims.

## Blueprint 24 Status

Status: complete.

TOM v3 can now discover existing point manifest JSON files, build a local multi-point replay index,
serve that index through the replay API, and show manifest-backed point navigation in the Replay
Workstation. The index preserves replay run-ID context and reports evidence availability/profile
counts from manifests only. It does not create new observations, event candidates, 3D candidates,
review lifecycle decisions, truth, score, player identity, point winner, in/out, generalization, or
adjudication.

## Blueprint 25 Status

Status: complete.

TOM v3 can now build and compare a multi-point evidence regression matrix from the Blueprint 24
replay index. The matrix preserves per-point replay URLs, associated run IDs, evidence
availability, profile counts, warnings, and provenance-only labels. Comparison reports additive
points separately from breaking protected/contract drift. It does not create observations, event
candidates, 3D candidates, labels, truth, score, player identity, point winner, in/out,
generalization, or adjudication.
