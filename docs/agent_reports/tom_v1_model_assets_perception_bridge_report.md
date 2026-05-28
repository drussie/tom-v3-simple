# TOM v1 Model Assets + Perception Bridge Agent Report

## Summary

This repair/bridge milestone adds local model asset guardrails and a documented TOM v1 smoke path through TOM v3's existing observation-only real perception commands. It does not add new model architecture, court adapters, tennis-event interpretation, or committed model binaries.

The bridge acknowledges the current visual reality gap: TOM v3's replay/evidence infrastructure works, but fixture-derived overlays are not real tracking quality. Local TOM v1 detector and pose weights can now be tested as TOM v3 observation sources while preserving evidence-only semantics.

## Files Created

- `docs/perception/tom_v1_model_assets_bridge_v0.md`
- `docs/milestones/tom_v1_model_assets_perception_bridge.md`
- `docs/handoffs/tom_v1_model_assets_perception_bridge_handoff.md`
- `docs/agent_reports/tom_v1_model_assets_perception_bridge_report.md`

## Files Modified

- `.gitignore`
- `Makefile`
- `README.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OPTIONAL_YOLO.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`

## Gitignore / Model Asset Decisions

The repository now explicitly treats local model weights and runtime artifacts as ignored local assets:

```text
model_assets/
*.pt
*.pth
*.onnx
*.engine
*.torchscript
```

Local TOM v1 assets under `model_assets/tom_v1/` remain outside git. `git check-ignore -v` confirmed the expected ignore rule for the local TOM v1 model files present in this workspace.

## TOM v1 Model Inventory

The documented local inventory is:

```text
model_assets/tom_v1/best_ball_v2_1280.pt          # ball detector
model_assets/tom_v1/keypoints_model.pth           # court keypoints model, future adapter required
model_assets/tom_v1/view_classifier_gameplay.pt   # gameplay classifier, future adapter required
model_assets/tom_v1/yolo26n.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26s.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26x-pose.pt               # pose model
model_assets/tom_v1/yolo26x.pt                    # player/object detector
```

Likely usable now through the existing TOM v3 real YOLO detection path:

- `best_ball_v2_1280.pt`
- `yolo26x.pt`
- `yolo26n.pt`
- `yolo26s.pt`

Likely usable now through the existing TOM v3 real pose path:

- `yolo26x-pose.pt`

Future TOM v1-specific adapters are still required for:

- `keypoints_model.pth`
- `view_classifier_gameplay.pt`

## Runtime Probe Result

`yolo-runtime-probe --device auto` ran successfully as a command, but reported optional runtime unavailable in this environment.

Missing optional packages reported:

- `ultralytics`
- `torch`
- `opencv-python-headless`

Resolved device was `cpu`. This is acceptable for the bridge milestone because default CI must not require optional vision dependencies.

## Optional Local Model Smoke Result

The local TOM v1 model files are present and ignored by git. Real model smoke was not run because the optional YOLO runtime is unavailable locally.

Plan-only smoke commands were validated for:

- TOM v1 ball detection using `best_ball_v2_1280.pt`
- TOM v1 player/object detection using `yolo26x.pt`
- TOM v1 pose using `yolo26x-pose.pt`

## Commands Added / Documented

Makefile helpers:

```bash
make tom-v1-yolo-probe
make tom-v1-ball-detection MEDIA_ID=<media_id>
make tom-v1-player-detection MEDIA_ID=<media_id>
make tom-v1-tracklets DETECTION_RUN_ID=<real_detection_run_id>
make tom-v1-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id>
```

The runbook also documents direct CLI commands for:

- YOLO runtime probe
- TOM v1 ball detection smoke
- TOM v1 player detection smoke
- real-detection-derived tracklet smoke
- TOM v1 pose smoke
- replay URL construction using the resulting real run IDs

## Known Risks

- TOM v1 weights may not be directly compatible with the current optional YOLO/Ultralytics runtime.
- The TOM v1 ball detector may require lower confidence thresholds than the default player/object detector path.
- Sparse or incorrect model outputs can still produce visually poor overlays.
- TOM v1 court keypoints and gameplay classifier files are not yet wired into TOM v3 because they likely need TOM v1-specific adapters.
- No smoke result in this milestone proves model quality or tracking quality.

## Class Mapping Notes

The most likely first integration issue is class mapping. The TOM v1 ball detector may emit `class 0 = ball`, while TOM v3's detection adapter maps model outputs into explicit `ball_detection` and `player_detection` observation types.

If real detection returns zero useful detections, the documented order is:

1. Lower the confidence threshold.
2. Inspect debug payloads or artifacts if available.
3. Check class names emitted by Ultralytics.
4. Add an explicit class map only when model output proves the mapping.

Unknown classes should not be relabeled without evidence.

## Non-Goals Preserved

- No model binaries committed.
- No model assets moved into tracked paths.
- No mandatory Ultralytics, Torch, OpenCV, or GPU dependency added to default CI.
- No TOM v1 code architecture imported into TOM v3.
- No TOM v1-specific court keypoint adapter added.
- No TOM v1-specific gameplay classifier adapter added.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No claim that tracking quality is solved.
- No fixture evidence silently treated as real evidence.

## Validation Results

- `git check-ignore -v model_assets/tom_v1/best_ball_v2_1280.pt`: passed.
- `git check-ignore -v model_assets/tom_v1/yolo26x.pt`: passed.
- `git check-ignore -v model_assets/tom_v1/yolo26x-pose.pt`: passed.
- `git check-ignore -v model_assets/tom_v1/keypoints_model.pth`: passed.
- `git check-ignore -v model_assets/tom_v1/view_classifier_gameplay.pt`: passed.
- `.venv/bin/python -m apps.worker.cli yolo-runtime-probe --device auto`: command passed; runtime reported unavailable because optional packages are not installed.
- `make tom-v1-yolo-probe PYTHON=.venv/bin/python`: command passed; runtime reported unavailable.
- `make tom-v1-ball-detection MEDIA_ID=media-plan PYTHON=.venv/bin/python PLAN_ONLY=true MAX_FRAMES=214`: passed.
- `make tom-v1-player-detection MEDIA_ID=media-plan PYTHON=.venv/bin/python PLAN_ONLY=true MAX_FRAMES=214`: passed.
- `make tom-v1-pose MEDIA_ID=media-plan SOURCE_DETECTION_RUN_ID=detection-plan PYTHON=.venv/bin/python PLAN_ONLY=true MAX_FRAMES=214`: passed.
- `.venv/bin/python -m pytest -q`: passed, 242 tests.
- `ruff check .`: passed.
- `cd apps/web && npm run lint`: passed after clearing an ignored stale `.next` generated cache.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities.
- Fixture demo: passed with media id `5658e716-6904-4c79-8b5e-bd031d74a457`.
- Completion audit: passed.

## Push Status

Commit prepared on `codex/tom-v1-model-assets-perception-bridge`; final branch and tag push status is reported in the handoff response.

## Recommended Next Handoff

Milestone 8F.5 - Visual Reality Gap Audit + TOM v1 Perception Bridge

If a future local environment installs the optional YOLO runtime and successfully completes TOM v1 ball/player/pose real smoke, the next handoff can advance to:

Milestone 8F.6 - TOM v1 Court Keypoints / View Classifier Adapter
