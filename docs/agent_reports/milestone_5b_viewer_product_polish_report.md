# Milestone 5B Agent Report - Viewer / Product Polish

## Summary

Milestone 5B polishes the TOM v3 Simple Evidence Viewer so the local fixture demo is easier to inspect and explain.

The work adds clearer empty states, a run evidence summary, consistent observation/evidence/candidate wording, readable lineage descriptions, stronger artifact and annotation display, keypoint annotation metadata display, and viewer payload regression coverage. It does not add new model/runtime capability or tennis interpretation.

## Files Created

- `apps/web/src/components/RunEvidenceSummary.tsx`
- `apps/web/src/lib/evidenceCopy.ts`
- `docs/milestones/milestone_5b_viewer_product_polish.md`
- `docs/handoffs/milestone_5b_viewer_product_polish_handoff.md`
- `docs/web/viewer_product_polish_v0.md`
- `docs/agent_reports/milestone_5b_viewer_product_polish_report.md`

## Files Modified

- `apps/web/src/app/globals.css`
- `apps/web/src/components/AnnotationPanel.tsx`
- `apps/web/src/components/ArtifactPanel.tsx`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/components/LineagePanel.tsx`
- `apps/web/src/components/ObservationDetailPanel.tsx`
- `apps/web/src/components/ObservationList.tsx`
- `apps/web/src/components/PoseOverlayPanel.tsx`
- `apps/web/src/components/TrackletEvidencePanel.tsx`
- `tests/test_local_demo.py`
- `README.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/blueprints/tom_v3_blueprint_5_simple_completion_product_hardening.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `docs/web/pose_overlay_viewer_v0.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`
- `docs/pose/pose_query_review_export_v0.md`

## Viewer Polish Decisions

The viewer remains the single evidence surface. 5B adds a run evidence summary and improves the existing panels rather than creating separate detection, tracklet, pose, or export apps.

The shared `evidenceCopy` helper keeps wording consistent across panels.

## Empty State Decisions

Empty states now explain what is missing and, where practical, which local command creates the missing evidence. Text guidance was preferred over new action buttons to keep the milestone narrow and avoid a product redesign.

## Terminology Decisions

User-visible copy now favors:

- observation
- evidence
- candidate
- source context
- model output
- fixture demo evidence
- keypoint evidence
- review annotation

Tracklet labels use candidate language, pose labels use keypoint evidence language, and annotations are described as non-mutating review evidence.

## Detection / Tracklet / Pose Panel Decisions

Detection panels clarify that bbox observations are evidence outputs and point users to frame artifact extraction when imagery is missing.

Tracklet panels describe candidate temporal grouping and readable source lineage while preserving raw relationship types.

Pose panels emphasize persisted keypoint evidence and keep missing keypoints visible as missing evidence.

## Lineage / Artifact / Annotation Decisions

Lineage rows now include human-readable relationship descriptions.

Artifact rows include target observation context, URI, checksum, created timestamp, and export record count metadata when available.

Annotation rows include label/type, creator, frame range, notes, keypoint metadata, and demo/review flags.

## Tests Run

- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `.venv/bin/python -m pytest tests/test_local_demo.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5b_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- Browser smoke against local API/web servers for detection, tracklet, and pose demo run URLs

## Validation Results

- Focused local demo tests: passed, `3 passed`.
- Full Python suite: passed, `150 passed`.
- Ruff: passed.
- Web lint/typecheck: passed.
- Web production build: passed.
- Web audit: passed, `0 vulnerabilities`.
- Alembic smoke: passed through the repo venv.
- Synthetic viewer smoke: passed with `ok = true`.
- Fixture demo smoke: passed with generated synthetic demo media, fixture gameplay/detection/tracklet/pose runs, seeded review annotations, pose review export, tracklet review export, and viewer URLs.
- Browser smoke: passed for detection, tracklet candidate, and pose run URLs. Verified the run evidence summary, detection evidence note, tracklet candidate evidence language, source detection observation wording, pose keypoint evidence note, annotation review copy, and review export summary on local demo data.

## Known Limitations

- The viewer shows review export artifacts only when they are present in the current viewer payload.
- There is still no frontend unit-test runner; frontend validation relies on TypeScript build, browser smoke, and Python viewer-payload contract tests.
- The polish is intentionally conservative and does not redesign navigation or add new UI workflows.

## Non-goals Preserved

Milestone 5B did not add:

- new model/runtime capability
- real pose inference
- movement interpretation
- stroke classification
- serve detection
- hit detection
- bounce detection
- rally or point reconstruction
- scoring
- homography
- adjudication

## Recommended Next Handoff

Milestone 5C - Final Evidence / Provenance Audit
