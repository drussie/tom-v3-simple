# TOM v3 Simple Known Limitations

This registry makes TOM v3 Simple boundaries explicit.

## Model / Runtime Limitations

- Fixture gameplay is deterministic demo output, not real gameplay inference.
- Fixture detection is deterministic demo output.
- Optional YOLO requires a local optional runtime and local weights outside git.
- Real YOLO detection quality depends on the chosen model, class mapping, source video, device, and confidence settings.
- Real YOLO detection replay is optional and local-runtime dependent.
- Real YOLO detections are model-output observations; they do not establish ball/player state.
- Replay source labels distinguish real model output from fixture evidence, but they do not evaluate model correctness.
- Candidate tracklets can be built from real YOLO detection runs, but they inherit the source model and class-mapping limitations.
- Real-detection-derived tracklet labels describe provenance only; they do not evaluate track correctness or identity.
- Optional real pose replay requires local pose runtime and local pose weights outside git.
- Real pose quality depends on the chosen pose model, source media, source player detections or frame sampling, device, and confidence settings.
- Real pose observations are keypoint evidence; they do not establish movement, stroke, serve, split-step, biomechanics, or body-state conclusions.
- Fixture pose output is demo evidence only.
- Blueprint 8A adds court/camera/homography schema and typed persistence contracts.
- Blueprint 8B adds deterministic fixture court keypoint, line, and camera/view evidence only.
- Blueprint 8C adds camera/view query, summary, and evidence-bundle read models only.
- Blueprint 8D adds homography candidate persistence from fixture court evidence only.
- Blueprint 8E adds replay overlays for persisted court keypoint, court line, camera/view, and homography candidate evidence only.
- Fixture court evidence is schema/provenance plumbing, not a real court model.
- Camera/view summaries are geometry context read models; they do not confirm camera state or homography validity.
- Homography candidates and overlays are candidate geometry evidence; they do not confirm a court model or camera geometry.
- Real court/camera/homography runtime is not implemented yet.
- Projection diagnostics are schema-level only and do not project ball/player detections into court space.
- Portable TOM v1 detector assets/source are not present in this repo state.

## Evidence Limitations

- Candidate tracklets are temporal groupings, not final object identity.
- Tracklets may contain wrong grouping, gaps, or missed detections.
- Track point candidates inherit limitations from source detection observations.
- Tracklet lineage preserves source detection observations, including real model-output provenance when available, but lineage is not correctness proof.
- Pose observations may be incomplete.
- Pose observations may be associated with the wrong subject candidate.
- Real crop-mode pose observations inherit the source player detection limitations.
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
- Homography candidate overlays are display-only candidate geometry; they are not projection diagnostics or court truth.
- Camera/view evidence can be queried through API read models and viewed in the replay court evidence context.
- The court keypoint/line adapter is fixture-only; no real court keypoint or line model is implemented yet.
- There is no production deployment workflow.
- There is no auth or user management.
- There is no cloud storage lifecycle.
- There is no real streaming protocol support.
- There is no multi-camera support.
- The frontend has TypeScript/build validation and smoke coverage, but no dedicated frontend unit-test runner.

## Tennis-Understanding Limitations

TOM v3 Simple does not include:

- confirmed homography
- court truth
- court-space reasoning
- in/out conclusions
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
