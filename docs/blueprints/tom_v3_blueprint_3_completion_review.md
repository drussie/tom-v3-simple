# TOM v3 Blueprint 3 Completion Review

## Verdict

Blueprint 3 Status: COMPLETE

Blueprint 3 is complete enough to close. It proved that TOM v3 can safely introduce optional real YOLO / Ultralytics runtime without contaminating the base environment, validate and register local model weights, normalize YOLO-like outputs into TOM v3 detection payloads, persist YOLO-origin ball/player observations through the existing detection pipeline, document a real local YOLO smoke path, and keep downstream viewer, tracklet, review, and export contracts unchanged.

Blueprint 3 did not add pose, court homography, bounce detection, hit detection, rally or point reconstruction, scoring, identity proof, YOLO tracking mode, or adjudication.

## What Blueprint 3 Proves

Blueprint 3 proves this path:

```text
optional YOLO runtime
-> runtime probe and device resolver
-> local weights validation
-> model_registry metadata
-> YOLO-like result normalization
-> guarded frame inference provider
-> existing detection adapter persistence
-> atomic ball/player observations
-> existing viewer, frame artifact, tracklet, review, and export paths
```

It also proves that the default TOM v3 environment can continue to run tests, worker commands, API imports, and viewer validation without Ultralytics, Torch, OpenCV, real model weights, CUDA, or MPS.

## What Blueprint 3 Does Not Prove

Blueprint 3 does not prove that a detection is correct.

It does not prove object identity, ball path correctness, player identity, bounce or hit events, rally state, point state, score state, or any official result. It does not implement pose, court homography, YOLO tracking mode, automatic model download, production GPU deployment, or remote model storage.

## Completion Questions

1. Is Blueprint 3 complete enough to close?
   Yes. The runtime boundary, registry, normalization, persistence bridge, local smoke path, docs, and tests are in place.

2. What exactly does Blueprint 3 prove?
   It proves optional YOLO model output can be normalized and persisted as TOM v3 observation rows without changing downstream contracts.

3. What does Blueprint 3 intentionally not prove?
   It does not prove detection correctness, identity, tracking, pose, homography, bounce, hit, rally, point, score, or any adjudicated result.

4. Does the base `tom_v3` environment remain lightweight?
   Yes. Ultralytics, Torch, and OpenCV are optional and not required for the base test suite.

5. Is `tom_v3_yolo` optional and documented?
   Yes. `requirements-yolo.txt`, runtime docs, and the local runbook describe the optional environment.

6. Are missing YOLO dependencies handled safely?
   Yes. `yolo-runtime-probe` reports unavailable packages without crashing, and real YOLO smoke skips cleanly when runtime is missing.

7. Are missing or invalid weights handled safely?
   Yes. Validation rejects missing, unsafe, empty, unsupported, or checksum-mismatched weights before model registration or detection persistence.

8. Are model weights excluded from git?
   Yes. `.gitignore` excludes `model_assets/`, `weights/`, `*.pt`, `*.pth`, `*.onnx`, and `*.engine`.

9. Can model weights be validated and registered?
   Yes. `register-yolo-model` validates local weights and creates or reuses a `model_registry` row.

10. Does `model_registry` preserve weights fingerprint and class mapping?
   Yes. Registry metadata stores weights path, sha256, size, runtime family, task, class map, runtime probe, and milestone provenance.

11. Can YOLO-like outputs be normalized into TOM v3 detection payloads?
   Yes. The normalization layer maps class names/ids, converts `xyxy` to bbox/center, skips invalid boxes, and reports unmapped classes.

12. Can mocked YOLO outputs persist as atomic observations through the existing detection pipeline?
   Yes. The fake provider path persists `ball_detection` and `player_detection` atomic observations through `run_detection_adapter`.

13. Does the YOLO adapter preserve media-owned frame/time?
   Yes. Frame numbers are sampled from indexed media and timestamps are derived from TOM v3 frame/time utilities.

14. Does the YOLO adapter avoid fixture fallback during YOLO runs?
   Yes. YOLO failures raise/record clear errors and do not persist fixture detections.

15. Does the YOLO adapter avoid YOLO tracking mode?
   Yes. The adapter runs frame inference only. Tracklets are built later by the existing Blueprint 2 tracklet builder.

16. Does the viewer consume YOLO detections through the existing detection overlay path?
   Yes. YOLO-origin observations share the normal `ball_detection` / `player_detection` payload contract and viewer payload.

17. Can YOLO-origin detections feed the existing Blueprint 2 tracklet builder?
   Yes. YOLO-origin detection runs use the same persisted observation contract consumed by `build-tracklets`.

18. Is pose still out of scope?
   Yes. Pose belongs to a later blueprint.

19. Is homography still out of scope?
   Yes. Court homography is not part of Blueprint 3.

20. Is bounce/hit/rally/point/scoring still out of scope?
   Yes. Blueprint 3 adds none of these.

21. Is the next blueprint boundary clear?
   Yes. Recommended next blueprint: Blueprint 4 - Pose Observation / Movement Evidence Layer.

## Invariant Audit

| Invariant | Status | Coverage |
| --- | --- | --- |
| Base imports do not require Ultralytics | Covered | `tests/test_yolo_runtime.py::test_base_worker_cli_imports_without_yolo_runtime` |
| Runtime probe does not crash when YOLO packages are missing | Covered | `tests/test_yolo_runtime.py::test_runtime_probe_reports_unavailable_when_imports_missing` |
| Device resolver handles CPU, MPS, CUDA, unavailable devices | Covered | `tests/test_yolo_runtime.py` device resolver tests |
| Weights validation rejects missing files | Covered | `tests/test_yolo_model_registry.py::test_missing_weights_fail_clearly` |
| Weights validation rejects unsafe paths | Covered | `tests/test_yolo_model_registry.py::test_unsafe_weights_path_outside_allowed_root_fails` |
| Weights validation rejects checksum mismatch | Covered | `tests/test_yolo_model_registry.py::test_checksum_mismatch_fails_clearly` |
| Valid weights can create a model registry row | Covered | `tests/test_yolo_model_registry.py::test_model_registry_row_created_from_valid_weights` |
| Registry stores weights sha256 and size | Covered | `tests/test_yolo_model_registry.py::test_model_registry_row_created_from_valid_weights` |
| Registry stores class map | Covered | `tests/test_yolo_model_registry.py::test_model_registry_row_created_from_valid_weights` |
| Normalization maps ball classes to `ball_detection` | Covered | `tests/test_yolo_normalization.py::test_sports_ball_maps_to_ball_detection` |
| Normalization maps person/player classes to `player_detection` | Covered | `tests/test_yolo_normalization.py::test_person_maps_to_player_detection_unknown_player` |
| Normalization skips unmapped classes | Covered | `tests/test_yolo_normalization.py::test_unmapped_class_is_counted_but_not_emitted` |
| Normalization skips invalid bboxes | Covered | `tests/test_yolo_normalization.py::test_invalid_bbox_is_skipped_with_warning` |
| YOLO adapter can persist mocked YOLO detections | Covered | `tests/test_yolo_frame_inference.py::test_mocked_yolo_adapter_run_persists_atomic_observations` |
| Persisted YOLO detections are atomic observations | Covered | `tests/test_yolo_frame_inference.py::test_mocked_yolo_adapter_run_persists_atomic_observations` |
| Persisted YOLO detections include `source_runtime = ultralytics_yolo` | Covered | `tests/test_yolo_frame_inference.py::test_mocked_yolo_adapter_run_persists_atomic_observations` |
| Persisted YOLO detections include `frame_time_owner = media_indexing` | Covered | `tests/test_yolo_frame_inference.py::test_mocked_yolo_adapter_run_persists_atomic_observations` |
| YOLO failure does not fall back to fixture detections | Covered | `tests/test_yolo_frame_inference.py::test_failed_yolo_run_does_not_persist_observations` and `tests/test_real_yolo_smoke.py::test_missing_runtime_returns_structured_skip_without_fixture_fallback` |
| YOLO failure does not persist fake real detections | Covered | `tests/test_yolo_frame_inference.py::test_failed_yolo_run_does_not_persist_observations` |
| Smoke helper can plan commands without runtime/assets | Covered | `tests/test_real_yolo_smoke.py::test_smoke_plan_only_does_not_require_runtime_or_assets` |
| Smoke helper skips cleanly when runtime/assets are missing | Covered | `tests/test_real_yolo_smoke.py` missing runtime and missing weights tests |
| Viewer consumes persisted YOLO detections through normal payloads | Covered | `tests/test_yolo_frame_inference.py::test_mocked_yolo_adapter_run_persists_atomic_observations` via `build_viewer_run_payload` |
| Tracklet builder can consume YOLO-origin detection runs | Covered by contract and docs | YOLO-origin runs write the same `ball_detection` / `player_detection` observations consumed by Blueprint 2; local smoke docs include `build-tracklets` after YOLO detection |
| Docs avoid overclaiming correctness | Covered by review | Blueprint 3 docs consistently describe model outputs as observations and retain the no-adjudication boundary |

No additional code-path tests were added in 3F because the existing 3A-3E tests cover the requested runtime, registry, normalization, persistence, failure, smoke, and viewer contracts. The tracklet compatibility invariant is intentionally contract-level: Blueprint 2 consumes persisted detection observations independent of producer, and the YOLO path persists the same observation types and payloads.

## Runtime / Weights Behavior

The base environment can run:

```bash
python -m apps.worker.cli yolo-runtime-probe
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

without optional YOLO packages.

Real local YOLO smoke requires:

- optional `tom_v3_yolo` environment,
- `requirements-yolo.txt`,
- local weights under an ignored model asset path,
- `register-yolo-model`,
- indexed media,
- `run-detection-adapter --adapter yolo --model-registry-id ...`.

The smoke helper never falls back to fixture detections for a YOLO run.

## Viewer And Blueprint 2 Compatibility

YOLO-origin detections persist as ordinary atomic detection observations, so the existing viewer overlay and frame artifact layers need no separate YOLO viewer.

Candidate tracklets remain a Blueprint 2 operation:

```text
YOLO detection run
-> persisted ball/player observations
-> build-tracklets
-> tracklet evidence bundle
-> query/review/export
```

The YOLO adapter does not create tracklets or run YOLO tracking mode.

## Remaining Limitations

- Real local YOLO validation depends on developer-supplied runtime packages, model weights, and sample media.
- CI intentionally does not install Ultralytics, Torch, or OpenCV.
- The frame inference provider is simple and frame-level, not optimized video streaming.
- Real output quality depends on the supplied weights and class map.
- Production GPU workers, remote model storage, and automatic model downloads remain out of scope.

## Next Blueprint Recommendation

Recommended next blueprint:

```text
Blueprint 4 - Pose Observation / Movement Evidence Layer
```

Pose should remain outside Blueprint 3. Blueprint 4 should preserve the same TOM v3 invariant: model outputs are observations, not adjudicated results.

## Blueprint 4 Follow-Up

Blueprint 4 is complete. It adds typed pose observation schema, COCO17 skeleton metadata, keypoint validation, normalization, fixture pose persistence, lineage, viewer overlay, query/review/export integration, and completion review. It does not add real pose inference, movement interpretation, homography, bounce, hit, rally, point, scoring, or adjudication.
