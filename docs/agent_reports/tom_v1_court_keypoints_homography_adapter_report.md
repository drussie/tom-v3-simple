# TOM v1 Court Keypoints + Homography Adapter Report

## Summary

This repair/bridge milestone adds a TOM v1 court keypoint adapter path for `model_assets/tom_v1/keypoints_model.pth`.

The adapter probes the local weights, recognizes the model as a ResNet50 state dict with a 28-value keypoint head, persists real model-output `court_keypoint_observation` rows, optionally derives `court_line_observation` candidates from those keypoints, and preserves source metadata so homography candidates and projection diagnostics can distinguish real model-output court evidence from fixture court evidence.

All outputs remain geometry evidence only.

## Files Created

- `packages/model_adapters/tom_v3_model_adapters/court_keypoints.py`
- `apps/worker/services/real_court_keypoint_replay.py`
- `tests/test_tom_v1_court_keypoints_adapter.py`
- `docs/court/tom_v1_court_keypoints_adapter_v0.md`
- `docs/court/tom_v1_court_keypoints_mapping_v0.md`
- `docs/agent_reports/tom_v1_court_keypoints_homography_adapter_report.md`

## Files Modified

- `apps/worker/cli.py`
- `Makefile`
- `apps/api/services/replay.py`
- `apps/worker/services/homography_candidate_builder.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`
- `docs/court/court_homography_evidence_decision_v0.md`
- `docs/court/homography_candidate_persistence_v0.md`
- `docs/court/projection_diagnostics_v0.md`

## Model Format / Load Strategy

`keypoints_model.pth` is probed as a Torch state dict, not TorchScript. The local file is recognized as a torchvision ResNet50-compatible state dict with a final layer shape of `(28, 2048)`, representing 14 xy keypoint pairs.

The adapter uses `torchvision.models.resnet50(weights=None)` with a 28-value output head and fixed 224x224 preprocessing.

## Keypoint Mapping Status

The v0 mapping interprets 14 TOM v1 raw points and maps them into TOM v3's 12-point `tennis_court_v0` schema.

Eight points are direct mappings. Four TOM v3 points are inferred:

- `left_net_post`
- `right_net_post`
- `center_mark_near`
- `center_mark_far`

The raw model output and mapping metadata are preserved in `raw_model_payload_jsonb`.

## Persistence Decisions

Real court keypoints use the existing observation spine and typed court table.

Metadata marks:

- `real_model_output = true`
- `model_output_not_truth = true`
- `fixture_court_evidence = false`
- `geometry_evidence_only = true`
- `observation_only = true`
- `no_adjudication = true`

Derived line candidates are persisted only when the required source keypoints are present.

## Homography / Projection Decisions

The existing homography candidate builder is reused. It now preserves source court evidence metadata, including whether source keypoints were real model output and whether source lines were derived from real keypoints.

Projection diagnostics remain review evidence. They still do not project ball or player detections into court space.

## Replay Decisions

Replay payloads now distinguish fixture court evidence from real court keypoint model output and derived court line candidates. UI labels remain provenance labels, not truth labels.

## Tests Run

Focused tests were added for:

- missing-model probe behavior
- CLI plan-only behavior
- fake-provider keypoint normalization
- derived line candidate requirements
- real court keypoint persistence metadata
- replay payload source labeling
- homography source metadata preservation

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 263 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed with `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4` and `MAX_FRAMES=3`.
- Completion audit passed against `tmp_tom_v3_court_adapter_fixture.db`.

Local TOM v1 court model smoke:

- `tom-v1-court-keypoints-probe` loaded `model_assets/tom_v1/keypoints_model.pth` directly as `torch_load_state_dict`.
- Recognized architecture: `torchvision_resnet50_fc28_xy224`.
- Model SHA256: `16ebb7e46dc88247440c86b388e4f07f0d4abb76ce0a01a22925d3163f7fb7f3`.
- Model size: `94582426` bytes.
- Real court keypoint run produced `court_run_id=8def9301-702d-4733-b6a0-708feb55fa0b`.
- Court observations produced: 8 `court_keypoint_observation` rows and 8 derived `court_line_observation` rows.
- Homography candidate run produced `homography_run_id=8de07dc4-f43e-47ba-8109-6f315843bcc6` with 8 candidates.
- Projection diagnostic run produced `projection_diagnostic_run_id=0745c189-7dc9-41c4-be69-721c800ac6e4` with 8 diagnostics.

Browser/manual replay alignment smoke was not completed in this pass. The persisted image-space keypoints are materially different from the fixture geometry and should be reviewed visually before treating the mapping/preprocessing as visually reliable. They remain model-output evidence only.

## Known Limitations

- The v0 keypoint mapping should be visually reviewed against real replay.
- Four TOM v3 schema points are inferred by the adapter.
- The homography builder still uses a lightweight v0 fitting method.
- Good model output can still produce poor geometry if the mapping, preprocessing, camera view, or fit assumptions are wrong.

## Non-Goals Preserved

No court truth, accepted/rejected lifecycle, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, player identity, scoreboard OCR, or adjudication was added.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Step

Run a visual court geometry audit against replay output from the real TOM v1 keypoint adapter and decide whether the next repair should improve the keypoint mapping, preprocessing, or homography fit.
