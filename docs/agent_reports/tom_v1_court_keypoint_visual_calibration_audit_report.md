# TOM v1 Court Keypoint Visual Calibration Audit Report

## Summary

This repair branch makes the TOM v1 court keypoint adapter debuggable before court geometry is treated as visually reliable. It exposes raw TOM v1 keypoints in replay, separates them from mapped TOM v3 keypoints, records preprocessing and coordinate assumptions, emits optional per-frame calibration debug artifacts, and marks homography from this source as uncalibrated candidate geometry.

## Files Created

- `docs/court/tom_v1_court_keypoint_visual_calibration_audit_v0.md`
- `docs/agent_reports/tom_v1_court_keypoint_visual_calibration_audit_report.md`

## Files Modified

- `Makefile`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayCourtOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `apps/worker/services/homography_candidate_builder.py`
- `apps/worker/services/real_court_keypoint_replay.py`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`
- `docs/court/tom_v1_court_keypoints_adapter_v0.md`
- `docs/court/tom_v1_court_keypoints_mapping_v0.md`
- `tests/test_tom_v1_court_keypoints_adapter.py`

## Raw Keypoint Overlay Behavior

Court keypoint overlay payloads now include `raw_tom_v1_keypoints`. The replay workstation has a separate toggle for raw TOM v1 court keypoints and labels points as `raw_0` through `raw_13`.

## Mapped Keypoint Overlay Behavior

Mapped TOM v3 keypoints remain available as a separate toggle. The UI labels this as mapped TOM v3 court keypoints so the operator can compare model output against adapter mapping.

## Debug Artifact

When `--emit-debug-artifacts` is passed, each court keypoint observation gets a `tom_v1_court_keypoint_calibration_debug_json` artifact with raw/scaled/mapped keypoint payloads and evidence-only warnings.

## Preprocessing / Coordinate Assumptions

Implemented assumptions:

- `preprocessing_mode = full_frame_resize_224`
- `coordinate_interpretation = output_as_pixels_224`

Unsupported modes fail clearly. This prepares future repairs for `letterbox_224`, `crop_then_resize_224`, normalized coordinates, or original-frame pixel output without pretending those paths exist today.

## Homography Warning

Homography candidates built from TOM v1 court keypoint rows now carry uncalibrated source metadata. Replay payloads can surface this as a calibration warning. The homography remains candidate geometry only.

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 264 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed with `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4` and `MAX_FRAMES=3`.
- Completion audit passed against `tmp_tom_v3_court_calibration_fixture.db`.

Local TOM v1 calibration smoke:

- Court calibration run: `41398bd7-36fb-4839-bc3c-093002cffe96`
- Homography run from that court run: `fd8d7ae2-4a34-43e4-947c-3db5e897acb3`
- Projection diagnostic run: `9fde90dc-acbb-488c-9ab3-6127ea740d90`
- Produced 8 `court_keypoint_observation` rows, 8 derived `court_line_observation` rows, and 8 calibration debug artifacts.
- Overlay payload smoke returned 14 raw TOM v1 points and 12 mapped TOM v3 points for the first court keypoint observation.
- Browser replay smoke showed raw `raw_0..raw_13` labels and mapped TOM v3 labels over video.
- Browser smoke screenshot: `.data/artifacts/tom-v1-court-keypoint-calibration-audit-smoke.png`

Visual audit note: the raw/mapped court geometry is now visible and explainable, but the overlay still needs calibration review before being trusted. This repair did not claim geometry correctness.

## Known Limitations

- This audit does not make the court geometry correct.
- Browser visual calibration smoke is still required to decide whether raw points, mapping, preprocessing, or homography fit is the next repair target.
- Only `full_frame_resize_224` plus `output_as_pixels_224` is implemented.
- Derived keypoints may still hurt homography fit if the raw mapping is wrong.

## Non-Goals Preserved

No court truth, accepted/rejected lifecycle, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, player identity, scoreboard OCR, server/receiver logic, or adjudication was added.

## Push Status

Branch `codex/tom-v1-court-keypoint-visual-calibration-audit` and tag `tom-v3-tom-v1-court-keypoint-visual-calibration-audit` pushed to origin.

## Recommended Next Step

Run browser replay calibration smoke with raw TOM v1 points enabled first. If raw points are mislocated, investigate preprocessing/coordinate interpretation. If raw points are plausible but mapped labels are wrong, repair the TOM v1 index mapping. If both are plausible but homography remains poor, repair the homography fit.
