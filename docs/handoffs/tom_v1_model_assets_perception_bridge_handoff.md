# TOM v1 Model Assets + Perception Bridge Handoff

## Current State

TOM v3 Simple, Blueprint 6, Blueprint 7, and Blueprint 8A-8F are complete. The replay workstation can display fixture/demo and persisted geometry evidence layers, and the replay overlay UI fetch/render repair is merged to `main`.

This bridge prepares local TOM v1 model assets for safe TOM v3 smoke testing.

## Local Assets

Expected local-only inventory:

```text
model_assets/tom_v1/best_ball_v2_1280.pt          # ball detector
model_assets/tom_v1/keypoints_model.pth           # court keypoints model, future adapter required
model_assets/tom_v1/view_classifier_gameplay.pt   # gameplay classifier, future adapter required
model_assets/tom_v1/yolo26n.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26s.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26x-pose.pt               # pose model
model_assets/tom_v1/yolo26x.pt                    # player/object detector
```

## What To Do Next

1. Install optional YOLO runtime locally if needed.
2. Run:

```bash
make tom-v1-yolo-probe PYTHON=.venv/bin/python
```

3. Index sample media through `make demo`.
4. Run `make tom-v1-ball-detection`.
5. Run `make tom-v1-player-detection`.
6. Run `make tom-v1-tracklets` from a real detection run.
7. Run `make tom-v1-pose` from the player detection run.
8. Open replay with the real `detectionRunId`, `trackletRunId`, and `poseRunId`.

## Cautions

- `keypoints_model.pth` and `view_classifier_gameplay.pt` need future TOM v1-specific adapters.
- The TOM v1 ball detector may require explicit class-map validation.
- Do not treat fixture evidence as real evidence.
- Do not claim tracking quality is solved until real smoke output is inspected.
- Do not add tennis-event interpretation.

## Recommended Next Handoff

Milestone 8F.5 - Visual Reality Gap Audit + TOM v1 Perception Bridge

If TOM v1 local smoke succeeds and the immediate need shifts to court/view assets:

Milestone 8F.6 - TOM v1 Court Keypoints / View Classifier Adapter
