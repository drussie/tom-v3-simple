# TOM v1 Court Keypoints Adapter v0

This repair/bridge milestone connects the local TOM v1 court keypoint model to the TOM v3 court evidence spine.

The flow is:

```text
indexed media
-> model_assets/tom_v1/keypoints_model.pth
-> TOM v1 court keypoint adapter
-> court_keypoint_observation rows
-> optional court_line_observation rows derived from keypoints
-> homography candidates
-> projection diagnostics
-> replay overlays
```

The output is model-output geometry evidence only. It is not court truth, a confirmed court model, a true homography, a line-call decision, or tennis-event interpretation.

## Model Format

Local probing shows `keypoints_model.pth` can be loaded as a Torch state dict. It is recognized as a ResNet50-style model with an `fc.weight` shape of `(28, 2048)`, which corresponds to 14 xy keypoint pairs.

The adapter uses `torchvision.models.resnet50(weights=None)` with a 28-value output head, loads the state dict, and runs local frame inference when Torch, torchvision, and OpenCV are available.

The model appears to emit coordinates in a 224x224 model-input pixel space. The CLI accepts `--img-size` for run documentation and compatibility, but the recognized v0 adapter uses a fixed 224x224 preprocessing path and scales the output back to source image pixels.

## CLI

Probe the local model without writing observations:

```bash
.venv/bin/python -m apps.worker.cli tom-v1-court-keypoints-probe \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --allowed-root model_assets/tom_v1
```

Run court keypoints:

```bash
.venv/bin/python -m apps.worker.cli run-real-court-keypoints \
  --media-id <media_id> \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --model-name tom-v1-court-keypoints \
  --model-version v1-local \
  --device auto \
  --img-size 640 \
  --every-n-frames 30 \
  --max-frames 214 \
  --allowed-root model_assets/tom_v1 \
  --viewer-base-url http://127.0.0.1:3000
```

Makefile helpers:

```bash
make tom-v1-court-keypoints-probe PYTHON=.venv/bin/python
make tom-v1-court-keypoints MEDIA_ID=<media_id> PYTHON=.venv/bin/python
```

## Persisted Evidence

The adapter writes `court_keypoint_observation` rows through the existing observation writer.

Metadata preserves:

- `fixture_court_evidence = false`
- `real_model_output = true`
- `model_output_not_truth = true`
- `geometry_evidence_only = true`
- `observation_only = true`
- `no_adjudication = true`
- `frame_time_owner = media_indexing`

When all required endpoints are present, the service derives `court_line_observation` rows from keypoint pairs. Those line rows are labeled:

```text
line_source = derived_from_real_keypoint_observations
candidate_line_only = true
```

Derived line candidates are review geometry evidence only.

## Homography And Diagnostics

Existing `build-homography-candidates` and `build-projection-diagnostics` commands can consume the real court run. Homography candidate metadata carries source evidence provenance such as:

- `source_court_evidence_source = real_model_output`
- `source_court_keypoint_real_model_output = true`
- `source_court_line_derived_from_real_keypoints = true`

This provenance helps replay and review distinguish real model-output court evidence from fixture court evidence.

## Replay Labels

Replay payloads now distinguish:

- fixture court evidence
- real court keypoint model output
- derived court line candidate
- homography candidate
- projection diagnostic

The labels are provenance labels. They do not imply a confirmed court, accepted homography, in/out decision, bounce, point, or score.

## Non-Goals

This adapter does not add:

- accepted/rejected court lifecycle
- court truth
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- player identity or scoreboard OCR
- TOM v2-style adjudication
