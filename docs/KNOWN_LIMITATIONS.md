# TOM v3 Simple Known Limitations

This registry makes TOM v3 Simple boundaries explicit.

## Model / Runtime Limitations

- Fixture gameplay is deterministic demo output, not real gameplay inference.
- Fixture detection is deterministic demo output.
- Optional YOLO requires a local optional runtime and local weights outside git.
- TOM v1 model assets under `model_assets/tom_v1/` are local-only ignored files and are not part of the repository.
- TOM v1 bridge helpers can run local smoke when optional runtime and model files are present; they do not prove ball/player tracking quality.
- TOM v1 ball/player detection smoke depends on optional YOLO runtime compatibility, class mapping, confidence thresholds, source media, and device.
- TOM v1 `keypoints_model.pth` is supported through the TOM v1 court keypoint adapter path, not through YOLO. TOM v1 `view_classifier_gameplay.pt` still requires a future TOM v1-specific adapter.
- Real YOLO detection quality depends on the chosen model, class mapping, source video, device, and confidence settings.
- Real YOLO detection replay is optional and local-runtime dependent.
- Real YOLO detections are model-output observations; they do not establish ball/player state.
- Replay source labels distinguish real model output from fixture evidence, but they do not evaluate model correctness.
- Candidate tracklets can be built from real YOLO detection runs, but they inherit the source model and class-mapping limitations.
- Real-detection-derived tracklet labels describe provenance only; they do not evaluate track correctness or identity.
- Optional real pose replay requires local pose runtime and local pose weights outside git.
- Real pose quality depends on the chosen pose model, source media, source player detections or frame sampling, device, and confidence settings.
- Real pose observations are keypoint evidence; they do not establish movement, stroke, serve, split-step, biomechanics, or body-state conclusions.
- Main tennis-player subject filtering selects `near_player_candidate` and `far_player_candidate` pose source candidates only; it does not confirm player identity or delete raw detections.
- Main player track assignment v0.1 groups those frame-local candidates into `near_player_track_candidate` and `far_player_track_candidate` visual track candidates, applies simple continuity and edge/wall jump rejection, and may leave gaps. It does not confirm identity, player names, server/receiver role, side changes, or track truth.
- Fixture pose output is demo evidence only.
- Blueprint 8A adds court/camera/homography schema and typed persistence contracts.
- Blueprint 8B adds deterministic fixture court keypoint, line, and camera/view evidence only.
- Blueprint 8C adds camera/view query, summary, and evidence-bundle read models only.
- Blueprint 8D adds homography candidate persistence from fixture court evidence only.
- Blueprint 8E adds replay overlays for persisted court keypoint, court line, camera/view, and homography candidate evidence only.
- Blueprint 8F adds projection diagnostic observations and court review export only.
- Fixture court evidence is schema/provenance plumbing, not a real court model.
- Camera/view summaries are geometry context read models; they do not confirm camera state or homography validity.
- Homography candidates and overlays are candidate geometry evidence; they do not confirm a court model or camera geometry.
- Real TOM v1 court keypoint model output can be persisted as court evidence, but mapping/preprocessing and homography fit quality still require visual audit. It is model-output geometry evidence, not court truth.
- Real camera/view runtime is not implemented yet.
- Projection diagnostics project court template geometry for review only; they do not project ball/player detections into court space.
- Replay current-only, short-trail, and full-trail controls are display policy only; they do not change persisted evidence or prove tracking correctness.
- TOM v1 model binaries may exist locally, but they are intentionally not tracked or uploaded.

## Evidence Limitations

- Candidate tracklets are temporal groupings, not final object identity.
- Tracklets may contain wrong grouping, gaps, or missed detections.
- Track point candidates inherit limitations from source detection observations.
- Tracklet lineage preserves source detection observations, including real model-output provenance when available, but lineage is not correctness proof.
- Pose observations may be incomplete.
- Pose observations may be associated with the wrong subject candidate.
- Real crop-mode pose observations inherit the source player detection limitations.
- Filtered crop-mode pose observations also inherit the main subject filter heuristic limitations.
- Track-filtered crop-mode pose observations also inherit main player track assignment limitations, including possible gaps, missed accepted assignments, or wrong temporary visual assignments when the heuristic is fooled.
- Full-frame real pose observations may be unassociated with a source player detection.
- Missing keypoints are recorded as missing evidence; they are not inferred.
- Review annotations do not mutate observations.

## Product Limitations

- TOM v3 Simple is local-first.
- Replay Mode currently supports local indexed file playback only.
- Replay Mode displays persisted detection observation, tracklet candidate, and pose keypoint evidence overlays.
- Replay Mode includes evidence timeline lanes for navigation.
- Replay Mode can display real YOLO detection replay runs through `detectionRunId` when local runtime/weights are available.
- Replay Mode can display real-detection-derived candidate tracklets through `trackletRunId` when a tracklet run has been built from a real detection run.
- Replay Mode can display real pose replay runs through `poseRunId` when local runtime/weights are available.
- Blueprint 6 is complete for local replay/operator workstation behavior, not for production live ingestion.
- Blueprint 7 is complete for optional real perception replay through detection observations, candidate tracklets, and pose keypoint evidence. It is not a court/homography, movement, stroke, event, stream, or deployment blueprint.
- Stream Proxy Mode is a live-like UI mode over indexed local media; it is not real live ingestion.
- Stream Proxy Mode hides future evidence in the UI, but the underlying observations are already persisted.
- Replay Mode can display persisted fixture court keypoint, court line, camera/view, and homography candidate evidence through `courtRunId` and `homographyRunId`.
- Replay Mode can display projection diagnostic evidence through `projectionDiagnosticRunId`.
- Replay Mode can display selectable `NEAR TRACK` / `FAR TRACK` main player track candidate labels through `mainPlayerTrackRunId`; these labels are visual track candidate labels, not identities.
- Homography candidate overlays and projection diagnostic overlays are display-only candidate geometry; they are not final court models.
- Camera/view evidence can be queried through API read models and viewed in the replay court evidence context.
- The fixture court keypoint/line adapter remains available for demos. The TOM v1 court keypoint adapter can write real model-output keypoint rows and derived line candidates, but those rows still require review and do not establish a confirmed court model.
- There is no production deployment workflow.
- There is no auth or user management.
- There is no cloud storage lifecycle.
- There is no real streaming protocol support.
- There is no multi-camera support.
- The frontend has TypeScript/build validation and smoke coverage, but no dedicated frontend unit-test runner.

## Tennis-Understanding Limitations

TOM v3 Simple does not include:

- confirmed homography
- confirmed court model
- court-space reasoning
- line-call conclusions
- court-space projection of detections
- bounce detection
- hit detection
- stroke classification
- serve detection
- split-step detection
- rally segmentation
- point reconstruction
- scoring
- official tennis results

## Data / Export Limitations

- Exports are TOM-native review exports.
- Exports are not third-party training formats unless a future blueprint adds one.
- Large-scale analytics are not included.
- Artifact storage lifecycle is local/demo-oriented.
- Provenance audit checks structure, not model correctness.

## Boundary

TOM v3 Simple records evidence and review context. It does not decide official tennis meaning.
