# TOM v1 Model Assets + Perception Bridge

Status: complete when this branch is accepted.

## Summary

This repair/bridge milestone adds guardrails and runbook support for testing local TOM v1 model assets through TOM v3's existing optional real perception commands.

It is not Blueprint 8G. It does not close Blueprint 8 or add a new perception architecture.

## Why

TOM v3's replay/evidence infrastructure works, but fixture visual quality is not real tracking quality. Ball and player overlays can be sparse or visually poor, court lines are fixture/static, and TOM v1 local perception assets may produce better observation sources.

This bridge makes those assets safe to test locally without committing model files or weakening TOM v3's observation-only semantics.

## Flow

```text
indexed media
-> optional YOLO runtime probe
-> TOM v1 ball detector smoke
-> TOM v1 player detector smoke
-> real-detection-derived candidate tracklets
-> TOM v1 pose model smoke
-> replay workstation with real run ids
```

## Added

- Explicit local model asset ignore guardrails.
- TOM v1 model inventory documentation.
- TOM v1 optional runtime probe and smoke runbook.
- Makefile helpers for probe, ball detection, player detection, tracklets, and pose.
- Class mapping risk notes for TOM v1 detector outputs.

## Non-Goals

- No model files committed.
- No new court keypoint or gameplay classifier adapter.
- No bounce/hit/in-out/rally/point/scoring.
- No ball/player court-space projection.
- No tracking quality claim.
- No TOM v1 architecture replacement.
- No mandatory YOLO dependency in default CI.
