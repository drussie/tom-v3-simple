# Blueprint 11 3D Readiness / Camera Geometry Evidence Layer v0 Report

## Summary

Blueprint 11 adds declared camera/court geometry evidence for future 3D readiness. It records
camera model, geometry status, declared court dimensions, unknown camera intrinsics/extrinsics, a
world-coordinate convention, source run linkage, capabilities, and no-truth warnings.

## Added

- `camera_geometry_evidence` persistence table and migration
- `tom_v3_schema.camera_geometry` contract
- `declare-camera-geometry` worker CLI command
- `tom-v1-declare-camera-geometry` Make helper
- replay info `camera_geometry_summary`
- replay side-panel camera geometry readiness display
- point evidence snapshot `camera_geometry_summary`
- point candidate evaluation `geometry_readiness`
- tests for persistence, status validation, snapshot/evaluation/replay integration, and boundaries

## Boundary

No 3D reconstruction was added. No 3D ball trajectory was added. Hit/bounce candidate generation,
marker arbitration, review annotations, source observations, in/out, score, point state, and
adjudication were not changed.

## Validation Notes

Local bridge smoke declared camera geometry for media
`9518fb01-0da1-4344-9a84-ff88ec8e9b1e` from court projection run
`82498799-490f-44df-9222-0157356c5ff7`.

- `camera_geometry_id`: `eb2b67a9-5df6-4577-861c-daf036fdc1e2`
- `geometry_run_id`: `2bd926b9-e1c0-4dcb-93c0-6bfbd33c3ffd`
- `geometry_status`: `declared`
- `camera_model`: `homography_backed_court_plane`
- `court_model`: `itf_standard_tennis_court`

Snapshot and evaluation smoke runs found the declared camera geometry and preserved the existing
candidate/review counts. The evaluation summary reported camera geometry available, court-plane
geometry declared, no true 3D reconstruction, and no 3D ball trajectory.

Validation passed:

- `.venv/bin/python -m pytest -q` (`343 passed`)
- `ruff check .`
- `git diff --check`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- fixture `make demo`
- fixture `make completion-audit`
- Alembic upgrade through `0005_camera_geometry_evidence`
