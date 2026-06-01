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
- TOM v1 court keypoint calibration now exposes raw `raw_0..raw_13` points and mapped TOM v3 points separately, but this does not make the court geometry trusted. It only makes preprocessing, coordinate interpretation, mapping, and homography errors easier to diagnose.
- Court geometry temporal persistence carries sparse candidate geometry forward in replay to reduce flicker, but it is display policy only. It does not confirm court geometry and currently uses max-gap/next-observation boundaries rather than real camera-cut boundaries.
- Real camera/view runtime is not implemented yet.
- Object-to-court projection candidates can project smoothed ball and main-player box candidates into
  normalized `court_template_2d` coordinates through candidate homographies. They remain derived
  candidate evidence and do not prove ball location, player location, court truth, bounce, hit,
  in/out, point, score, or identity.
- Hit/bounce candidate evidence can mark possible hit and bounce moments from trajectory physics
  proxies and main-player projection proximity, but it is deliberately low-authority candidate
  evidence. Hit candidates prefer player-proximate `court_y` net-axis reversal. Bounce candidates
  prefer image-y descending-to-ascending proxy plus speed reduction. These are not hit truth,
  bounce truth, in/out, rally, point, score, or adjudication.
- Hit/bounce rejection diagnostics explain why evaluated contexts were not emitted, deduped, or
  suppressed. They are diagnostic evidence only and do not create an accepted/rejected truth
  lifecycle.
- Replay Marker Inspector shows compact source method, timing, confidence, coordinate, and
  marker-level arbitration details for selected visible hit/bounce markers. It is an operator
  evidence display only and does not create hit truth, bounce truth, in/out, score, or adjudication.
- Replay current-only, short-trail, and full-trail controls are display policy only; they do not change persisted evidence or prove tracking correctness.
- Motion smoothing creates derived replay candidate evidence only. Smoothed ball, player-box, and pose candidates can reduce jitter, but they are not true ball positions, confirmed player boxes, actual pose, trajectory physics, bounce/hit/in-out, point, or score.
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
- Smoothed pose candidates inherit raw pose and track-assignment limits and do not invent missing keypoints across gaps.
- Smoothed ball candidates inherit source detection/tracklet limits and do not prove a trajectory or bounce.
- Smoothed main player box candidates inherit main-player track assignment limits and do not prove identity or subject truth.
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
- Replay Mode can display smoothed replay candidates through `motionSmoothingRunId`; these overlays are visual smoothing candidates, not object truth or tennis-event interpretation.
- Replay Mode can display object-to-court projection candidates through `courtProjectionRunId` in a
  normalized court mini-map; those points are candidate template projections, not confirmed court
  positions or tennis-event facts.
- Replay Mode can display `ball_trajectory_court_candidate` paths through `ballTrajectoryRunId`,
  but these are derived trajectory candidates only; they do not identify bounces, hits, in/out, or
  scoring events.
- Replay Mode can display `hit_candidate` and `bounce_candidate` markers through
  `eventCandidateRunId`; these mini-map and video markers must remain labeled as candidates and do
  not confirm hits, bounces, in/out, points, or scores.
- Event candidate markers are persistent review pins by default. Persistence helps operators see
  sparse candidates across the point, but it is display policy only and does not make a candidate
  true.
- Event candidate classification prioritizes player-proximate trajectory changes as
  `hit_candidate` before bounce consideration, but this remains a heuristic candidate label, not
  contact truth.
- Hit/Bounce Physics Heuristic Repair v0.2 makes that heuristic more tennis-specific, but image-y
  is still only a camera-space proxy and `court_y` is only the current template net-axis
  assumption.
- Hit/Bounce Recall Diagnostics + Header Layout Repair v0.2.1 adds a bounded far-side recall
  fallback and rejection diagnostics, but the recovered markers remain candidate evidence rather
  than confirmed hit/bounce events.
- Image-Space Net-Axis Hit Recall v0.2.6 uses broadcast image-y as a near/far-axis fallback for
  airborne hit-like candidate recall. This can recover visually obvious reversals that court-plane
  projection misses, but it is not true camera geometry, not hit truth, and not in/out or scoring
  evidence.
- Image-Space Direction-Change Hit Recall v0.2.7 uses full 2D broadcast image vector angle changes
  for additional airborne hit-like candidate recall. Player proximity is diagnostic only, and the
  signal can still be affected by camera perspective, occlusion, detection gaps, and projection
  artifacts. It does not prove racket contact.
- Local-Evidence Event-Type Classification v0.2.8 classifies image-space direction-change
  candidates as hit-like or bounce-like using local landing/contact evidence. It explicitly does
  not require a prior bounce before a hit candidate, and sequence remains weak diagnostic context
  only.
- Universal Hit Candidate Validity Guard v0.3.0 adds a final guard across all hit-candidate
  sources and tightens v0.2.9 by separating hard reversal evidence from image-direction-only
  transit evidence. It can reclassify unsupported landing-like hits or suppress fly-through/no-event
  hits into diagnostics, but it remains heuristic candidate evidence and does not prove contact,
  bounce, in/out, score, or point state.
- Marker-Level Event Arbitration v0.3.1 resolves visible marker conflicts after the universal guard.
  It can prefer a co-located bounce marker over a hit marker unless independent contact evidence is
  strong, and it can suppress transit/fly-through hit markers into diagnostics. It keeps
  `hit_requires_prior_bounce = false` and `sequence_is_hard_gate = false`; this is candidate-marker
  arbitration only, not truth or adjudication.
- Compact CLI + Marker Summary v0 shortens default operator output for hit/bounce candidate builds.
  It does not remove stored diagnostics or change candidate generation; verbose/debug flags are
  still required for the full diagnostic dump.
- Event Candidate Review Panel v0 is a replay navigation surface for final visible hit/bounce
  markers. It does not change candidate generation, arbitration, truth status, in/out, score, or
  adjudication.
- Point Evidence Snapshot v0 creates compact run reports for operator review and regression
  comparison. Snapshots preserve candidate-only warnings and do not make markers true, in/out,
  scoring, or adjudicated outcomes.
- Blueprint 8 Completion Review / Freeze v0 freezes the current replay evidence workstation as a
  reproducible candidate-evidence milestone only. It does not add or imply hit truth, bounce truth,
  in/out, score, point winner, player identity, manual accept/reject correction, accepted/rejected
  lifecycle, or adjudication.
- Marker correctness remains operator-reviewed. The current sample-point counts are reproducible,
  but there is not yet a benchmark set or dataset-level recall/precision report.
- Hit/Bounce Side-Zone + Sequence Classification Repair v0.2.2 can reclassify raw hit/bounce
  candidates using court-side zones and a simple event-sequence prior. This improves operator-review
  labels, but the sequence prior is heuristic candidate evidence only and is not rally, point,
  score, in/out, or adjudication logic.
- Player-Anchored Hit Recall v0.2.3 can recover additional `hit_candidate` markers by scanning
  wider ball trajectory windows around near/far main player projection anchors. The recall pass
  inherits projection and trajectory gaps and does not prove contact, rally order, in/out, point, or
  score.
- Player-Anchored Hit Contact-Zone Tightening v0.2.4 suppresses player-anchored hit candidates
  that overlap bounce/open-court landing clusters, but the contact-zone gate is still candidate
  geometry and does not prove racket contact.
- Net-Axis Reversal Hit Recall v0.2.5 can recover ball-first `hit_candidate` markers from
  `court_y` direction reversal without requiring player proximity. This improves recall but can
  still be fooled by sparse trajectories, projection noise, or camera geometry; player proximity is
  diagnostic support only and the marker is not hit truth.
- Event candidate video markers require a source ball court projection image point. If that point
  is unavailable, the candidate remains inspectable in replay but no broadcast-video marker is
  drawn.
- Replay view presets are display defaults only. Operator view hides raw/debug layers by default,
  and debug/audit view enables them, but neither preset changes persisted observations or proves
  evidence correctness.
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
- confirmed court-space reasoning
- line-call conclusions
- confirmed court-space projection of detections
- bounce detection
- hit detection
- stroke classification
- serve detection
- split-step detection
- rally segmentation
- point reconstruction
- scoring
- official tennis results
- manual correction workflow
- accepted/rejected candidate lifecycle
- multi-point or match-level event timeline
- dataset-level benchmark metrics

## Data / Export Limitations

- Exports are TOM-native review exports.
- Exports are not third-party training formats unless a future blueprint adds one.
- Large-scale analytics are not included.
- Artifact storage lifecycle is local/demo-oriented.
- Provenance audit checks structure, not model correctness.

## Boundary

TOM v3 Simple records evidence and review context. It does not decide official tennis meaning.
