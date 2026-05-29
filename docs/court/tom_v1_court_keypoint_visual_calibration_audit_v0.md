# TOM v1 Court Keypoint Visual Calibration Audit v0

This repair/audit branch makes TOM v1 court keypoint output inspectable before treating mapped keypoints, derived lines, homography candidates, or projection diagnostics as visually reliable.

The current court adapter can run `model_assets/tom_v1/keypoints_model.pth` and persist `court_keypoint_observation` rows. The visual court overlay is still not trusted. This audit exposes the raw model outputs so the next repair can decide whether the problem is preprocessing, coordinate interpretation, keypoint order, inferred keypoints, or homography fitting.

## Debug Surfaces

Replay now supports two separate court keypoint views from the same persisted observation:

- raw TOM v1 keypoints labeled `raw_0` through `raw_13`
- mapped TOM v3 keypoints labeled with the `tennis_court_v0` names

The raw overlay uses `raw_keypoints_scaled_to_image` from `raw_model_payload_jsonb`. The mapped overlay uses the normalized TOM v3 `keypoints_jsonb`.

## Current Assumptions

The v0 adapter explicitly records:

```text
preprocessing_mode = full_frame_resize_224
coordinate_interpretation = output_as_pixels_224
model_input_size = 224
output_reference_size = 224.0
mapping_version = tom_v1_14_point_to_tom_v3_12_point_mapping_v0
```

Unsupported values such as `letterbox_224`, `crop_then_resize_224`, `output_as_normalized_0_1`, or `output_as_pixels_original_frame` fail clearly. They are planned variants, not implemented behavior in this audit.

## Debug Artifact

When `--emit-debug-artifacts` is supplied, each persisted court keypoint observation receives a `tom_v1_court_keypoint_calibration_debug_json` evidence artifact. The artifact metadata includes:

- frame number and timestamp
- image width and height
- preprocessing mode
- coordinate interpretation
- raw TOM v1 output
- raw keypoints scaled to image pixels
- mapped TOM v3 keypoints
- inferred TOM v3 keypoints
- mapping version
- evidence-only warnings

The artifact is a TOM-native debug artifact. It is local review metadata, not a court-truth artifact.

## CLI

```bash
.venv/bin/python -m apps.worker.cli run-real-court-keypoints \
  --media-id <media_id> \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --model-name tom-v1-court-keypoints \
  --model-version v1-local \
  --device auto \
  --img-size 224 \
  --every-n-frames 30 \
  --max-frames 214 \
  --allowed-root model_assets/tom_v1 \
  --preprocessing-mode full_frame_resize_224 \
  --coordinate-interpretation output_as_pixels_224 \
  --emit-debug-artifacts \
  --viewer-base-url http://127.0.0.1:3000
```

Makefile helper:

```bash
make tom-v1-court-keypoint-audit \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=30
```

## Replay Review

Open replay with the resulting `courtRunId` and enable:

- Show raw TOM v1 court keypoints
- Show mapped TOM v3 court keypoints
- Show derived court lines
- Show homography candidates
- Show projection diagnostics

Inspect raw points first. If `raw_0..raw_13` are not near the painted court structure, homography repair is premature. If raw points look plausible but mapped TOM v3 labels are wrong, the keypoint order/mapping is the likely repair target. If mapped keypoints are plausible but homography is wrong, the fit method is the likely target.

## Boundary

This audit does not add court truth, confirmed homography, accepted/rejected court lifecycle, ball/player court-space projection, bounce/hit/in-out, point reconstruction, scoring, player identity, scoreboard OCR, or adjudication.

The output remains court keypoint evidence, mapping debug evidence, homography candidate evidence, and projection diagnostic evidence only.
