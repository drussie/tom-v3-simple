# Blueprint 36 Agent Report - Camera Geometry Confidence / Calibration Provenance v1

## Summary

Implemented Blueprint 36 as a read-only provenance layer for camera geometry and calibration
review readiness. The new service exports a frozen contract, builds structural profiles from
existing manifest/index/matrix/corpus/feedback artifacts, validates profiles against TOM contracts,
and emits a structural report.

## Added

- `apps.worker.services.camera_geometry_calibration_provenance`
- Worker CLI commands:
  - `export-camera-geometry-calibration-provenance-contract`
  - `build-camera-geometry-calibration-profile`
  - `validate-camera-geometry-calibration-profile`
  - `build-camera-geometry-calibration-report`
- Make targets:
  - `tom-v1-export-camera-geometry-calibration-provenance-contract`
  - `tom-v1-build-camera-geometry-calibration-profile`
  - `tom-v1-validate-camera-geometry-calibration-profile`
  - `tom-v1-build-camera-geometry-calibration-report`
- Tracked contract:
  - `.data/contracts/camera_geometry_calibration_provenance_contract_v1.json`
- Focused tests:
  - `tests/test_camera_geometry_calibration_provenance.py`
- Post-Codex validation smokes for BP36.

## Boundary

The implementation reads existing JSON artifacts only. It does not create camera geometry,
homography, projection diagnostics, event candidates, 3D candidates, review labels, training truth,
line-call conclusions, score, player identity, winners, reviewer rankings, or adjudication.
