# Camera Geometry Confidence / Calibration Provenance v1 Review

Status: complete.

Blueprint 36 adds a calibration provenance contract, profile builder, validator, report builder,
Make targets, and tests. The current protected sample profile preserves the sample point replay URL
and run IDs, including the protected `camera_geometry_id`, and reports missing court keypoints,
homography candidates, and projection diagnostics as structural review gaps.

## Review Notes

- Contract path: `.data/contracts/camera_geometry_calibration_provenance_contract_v1.json`
- Generated profile path: `.data/exports/camera_geometry_calibration_profile.current.json`
- Generated validation path: `.data/exports/camera_geometry_calibration_profile.validation.json`
- Generated report path: `.data/exports/camera_geometry_calibration_report.current.json`
- Current protected sample profile: camera geometry present, replay context present, projection diagnostics missing, calibration review needed, human review ready.

## Non-Goals

The review found no new evidence generation path. Blueprint 36 does not validate calibration
correctness, create labels, decide in/out, score, identify players, determine a winner, rank
reviewers, score reviewer quality, resolve disagreement, train models, or adjudicate evidence.
