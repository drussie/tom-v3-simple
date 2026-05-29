# TOM v1 Court Keypoints Mapping v0

The TOM v1 `keypoints_model.pth` bridge maps a 14-point raw model output into TOM v3's 12-point `tennis_court_v0` schema.

The raw model output is interpreted as 14 xy pairs in model-input pixel space. The v0 adapter scales those coordinates from a 224x224 reference space into source image pixels.

This is now treated as a calibration assumption:

```text
preprocessing_mode = full_frame_resize_224
coordinate_interpretation = output_as_pixels_224
```

The visual calibration audit exposes raw `raw_0..raw_13` points separately from mapped TOM v3 points so this assumption can be reviewed before repairing homography.

## Direct Mapping

```text
TOM v1 raw index 0  -> far_left_baseline_corner
TOM v1 raw index 1  -> far_right_baseline_corner
TOM v1 raw index 2  -> near_left_baseline_corner
TOM v1 raw index 3  -> near_right_baseline_corner
TOM v1 raw index 8  -> service_line_t_far_left
TOM v1 raw index 9  -> service_line_t_far_right
TOM v1 raw index 10 -> service_line_t_near_left
TOM v1 raw index 11 -> service_line_t_near_right
```

## Raw Points Retained In Payload

The adapter also preserves raw names for all 14 TOM v1 outputs in `raw_model_payload_jsonb`:

```text
0  far_left_baseline_corner
1  far_right_baseline_corner
2  near_left_baseline_corner
3  near_right_baseline_corner
4  far_left_singles_sideline_corner
5  near_left_singles_sideline_corner
6  far_right_singles_sideline_corner
7  near_right_singles_sideline_corner
8  service_line_t_far_left
9  service_line_t_far_right
10 service_line_t_near_left
11 service_line_t_near_right
12 center_service_t_far
13 center_service_t_near
```

Replay payloads expose these as `raw_tom_v1_keypoints`, with source-index labels `raw_0` through `raw_13` and image-space coordinates under the current coordinate interpretation.

## Inferred TOM v3 Points

TOM v3's `tennis_court_v0` schema requires 12 keypoints. Four are inferred by the adapter:

```text
left_net_post   = midpoint(far_left_baseline_corner, near_left_baseline_corner)
right_net_post  = midpoint(far_right_baseline_corner, near_right_baseline_corner)
center_mark_near = midpoint(near_left_baseline_corner, near_right_baseline_corner)
center_mark_far  = midpoint(far_left_baseline_corner, far_right_baseline_corner)
```

Inferred keypoints use `visibility = inferred_by_adapter` and reduced confidence. This is adapter normalization evidence, not a claim that the point is physically correct in the video.

## Mapping Limits

This mapping is v0 and should be reviewed against real replay overlays. If the projected court geometry is poor, the likely causes are:

- wrong TOM v1 output order
- model trained for a different frame crop or preprocessing convention
- insufficient camera/view context
- a homography fit that is too simple for the view

Poor fit is still useful evidence. It should be reported as model/mapping/geometry uncertainty, not hidden or relabeled as court truth.

If raw points are visibly wrong, the next repair should investigate preprocessing or coordinate interpretation before changing the mapping. If raw points are plausible but TOM v3 labels are wrong, repair the mapping. If raw and mapped points are plausible but the candidate geometry is still wrong, repair the homography fit.
