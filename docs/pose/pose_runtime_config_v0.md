# Pose Runtime Config v0

## Purpose

Milestone 4A defines the pose runtime and model metadata contract without running real pose inference. Milestone 4B adds normalization-only adapter diagnostics for fake or serialized pose output. Milestone 4C creates fixture pose runtime config rows for worker persistence runs.

## Model Registry Metadata

Pose model registry rows should use:

```text
model_family = pose
model_runtime = ultralytics | fixture | future_runtime
model_task = pose
```

Metadata should include:

- model name/version
- weights path when applicable
- weights sha256 and size when applicable
- skeleton format/version
- keypoint schema JSON
- runtime package versions when available
- `blueprint = 4`
- milestone provenance

Milestone 4A fixture insertion creates a fixture pose model registry row with COCO17 metadata and no real weights.

Milestone 4C worker persistence creates or reuses a fixture pose adapter model row with:

```text
model_family = pose
model_runtime = fixture
model_task = pose
skeleton_format = coco17
normalization_only = true
no_real_pose_inference = true
```

## Runtime Config Shape

The pose runtime config payload is shaped as:

```json
{
  "adapter": "fixture_pose",
  "adapter_version": "v0",
  "frame_sample_policy": "explicit_frames",
  "subject_source_mode": "full_frame",
  "model_registry_id": "<model_registry_id>",
  "weights_path": null,
  "device": "cpu",
  "imgsz": null,
  "conf": null,
  "iou": null,
  "max_det": null,
  "skeleton_format": "coco17",
  "skeleton_version": "v1",
  "keypoint_schema_json": {},
  "artifact_settings": {
    "emit_debug_artifact": false
  },
  "frame_time_owner": "media_indexing",
  "blueprint": 4,
  "milestone": "4A"
}
```

Future real pose adapters can reuse the Blueprint 3 discipline: optional runtime dependency path, explicit local weights, fingerprinting, model registry metadata, and guarded inference.

Milestone 4C worker runtime configs add:

- `frame_sample_rate`
- `max_frames`
- `source_detection_run_id`
- `link_source_detections`
- `normalization_only = true`
- `no_real_pose_inference = true`
- `milestone = 4C`

## Normalization Adapter Diagnostics

The 4B normalization adapter result includes:

- adapter name/version
- input pose count
- normalized pose count
- skipped pose count
- warnings
- `note = normalization only, no real pose inference`

## Non-Goals

Milestones 4A, 4B, and 4C do not add real pose runtime, pose weights validation, overlay rendering, movement interpretation, or tennis-event candidates.
