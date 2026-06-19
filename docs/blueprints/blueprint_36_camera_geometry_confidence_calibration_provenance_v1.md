# Blueprint 36 - Camera Geometry Confidence / Calibration Provenance v1

Status: implemented.

Blueprint 36 adds a read-only camera geometry calibration provenance layer. It summarizes whether
camera geometry, replay context, homography/court/projection diagnostic evidence, review context,
and source provenance are structurally present for manifest-backed evidence points.

## Scope

Blueprint 36 proves:

```text
existing point manifests / replay index / regression matrix / corpus / feedback inputs
-> camera geometry calibration provenance contract
-> structural calibration profile
-> profile validation against TOM contracts
-> structural calibration report
```

The contract is tracked at:

```text
.data/contracts/camera_geometry_calibration_provenance_contract_v1.json
```

Generated current outputs are intentionally local exports:

```text
.data/exports/camera_geometry_calibration_profile.current.json
.data/exports/camera_geometry_calibration_profile.validation.json
.data/exports/camera_geometry_calibration_report.current.json
```

## Commands

```bash
make tom-v1-export-camera-geometry-calibration-provenance-contract PYTHON=.venv/bin/python
make tom-v1-build-camera-geometry-calibration-profile PYTHON=.venv/bin/python
make tom-v1-validate-camera-geometry-calibration-profile \
  PYTHON=.venv/bin/python \
  CAMERA_GEOMETRY_CALIBRATION_PROFILE=.data/exports/camera_geometry_calibration_profile.current.json
make tom-v1-build-camera-geometry-calibration-report \
  PYTHON=.venv/bin/python \
  CAMERA_GEOMETRY_CALIBRATION_PROFILE=.data/exports/camera_geometry_calibration_profile.current.json
```

## Boundary

This layer is provenance and review support only. It does not create camera geometry, homography
candidates, projection diagnostics, event candidates, 3D candidates, labels, calibration truth,
line-call conclusions, in/out, score, player identity, winner, tactical conclusions, betting
predictions, reviewer ranking, reviewer scoring, or adjudication.

The profile statuses are structural readiness values. `evidence_partial`,
`provenance_partial`, `review_ready`, `calibration_review_needed`, and
`regression_protected_context` are not correctness findings and are not model-readiness claims.
