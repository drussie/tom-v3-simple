# TOM v3 Simple Known Limitations

This registry makes TOM v3 Simple boundaries explicit.

## Model / Runtime Limitations

- Fixture gameplay is deterministic demo output, not real gameplay inference.
- Fixture detection is deterministic demo output.
- Optional YOLO requires a local optional runtime and local weights outside git.
- Real YOLO detection quality depends on the chosen model, class mapping, source video, device, and confidence settings.
- Real pose inference is not included.
- Fixture pose output is demo evidence only.
- Portable TOM v1 detector assets/source are not present in this repo state.

## Evidence Limitations

- Candidate tracklets are temporal groupings, not final object identity.
- Tracklets may contain wrong grouping, gaps, or missed detections.
- Track point candidates inherit limitations from source detection observations.
- Pose observations may be incomplete.
- Pose observations may be associated with the wrong subject candidate.
- Missing keypoints are recorded as missing evidence; they are not inferred.
- Review annotations do not mutate observations.

## Product Limitations

- TOM v3 Simple is local-first.
- Replay Mode currently supports local indexed file playback only.
- Replay Mode displays persisted detection observation, tracklet candidate, and pose keypoint evidence overlays.
- Replay Mode does not yet include full evidence timeline lanes, stream proxy mode, or live ingestion.
- There is no production deployment workflow.
- There is no auth or user management.
- There is no cloud storage lifecycle.
- There is no streaming support.
- There is no multi-camera support.
- The frontend has TypeScript/build validation and smoke coverage, but no dedicated frontend unit-test runner.

## Tennis-Understanding Limitations

TOM v3 Simple does not include:

- homography
- court-space reasoning
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
