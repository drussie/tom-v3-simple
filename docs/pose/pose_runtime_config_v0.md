# Pose Runtime Config v0

## Purpose

Milestone 4A defines the pose runtime and model metadata contract without running real pose inference.

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

## Non-Goals

Milestone 4A does not add real pose runtime, pose weights validation, crop projection, overlay rendering, movement interpretation, or tennis-event candidates.
