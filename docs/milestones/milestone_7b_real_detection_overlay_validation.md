# Milestone 7B - Real Detection Overlay Validation

## Status

Complete.

## Goal

Make real YOLO detection replay runs clear and inspectable in the replay workstation.

Milestone 7A created the optional `run-real-detection` path. Milestone 7B validates that those persisted real model-output detections are understandable in replay surfaces without changing the observation contract.

## What Changed

- Replay-info available detection runs now include optional source metadata.
- Detection run selectors distinguish real model output from fixture demo evidence.
- Detection overlay payloads include optional source/runtime/model/config/class fields.
- Detection timeline items include source metadata and source-aware display labels.
- Selected detection detail shows model/runtime/config/class metadata when present.
- `run-real-detection` output includes a stream-proxy replay URL and local API/web command hints.
- Tests cover fixture source metadata and fake real YOLO source metadata without requiring weights.

## Evidence Source Labels

Replay run metadata can now report:

- `evidence_source = real_model_output`
- `evidence_source = fixture_demo`
- `evidence_source = persisted_evidence`

These labels are display metadata only. They do not change persisted observations or promote model output into tennis meaning.

## Non-goals

7B does not add real-detection-derived tracklets, real pose inference, court/homography evidence, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

Real model output remains evidence only.
