# Milestone 5A - Local Demo / Runbook Completion Path

## Status

Status: complete.

## Goal

Start Blueprint 5 by creating a deterministic local fixture demo path and canonical runbook for TOM v3 Simple.

The demo proves the completed evidence loop without requiring YOLO weights, real pose weights, GPU runtime, or network access.

## What Changed

- Added a local fixture demo orchestration service.
- Added worker `run-demo`.
- Added Makefile demo, demo-plan, demo-reset, demo-export, demo-open, completion-check, yolo-probe, and yolo-smoke targets.
- Added deterministic media resolution with custom media, fixture media, or generated synthetic fallback.
- Added seeded review annotations for detection, tracklet, and pose evidence.
- Added pose and tracklet review dataset exports to the demo path.
- Added canonical `docs/RUNBOOK_LOCAL.md`.
- Documented Blueprint 5 as a completion/product-hardening pass.

## Demo Path

```text
resolve media
-> index media
-> run fixture gameplay adapter
-> run fixture detection adapter
-> extract frame artifacts
-> build candidate tracklets
-> run fixture pose adapter
-> seed review annotations
-> export pose review dataset
-> export tracklet review dataset
-> print summary with viewer URLs
```

## Evidence Boundary

Fixture outputs are demo evidence only.

They do not prove object correctness, player identity, movement meaning, tennis events, score, or official results.

No real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication was added.

## Validation

Milestone 5A adds focused tests for:

- demo media resolution priority
- demo stage planning
- fixture demo execution in a temporary SQLite database
- seeded review annotations
- review export artifact creation
- summary IDs, counts, exports, and viewer URLs

Full project validation is recorded in the 5A agent report.
