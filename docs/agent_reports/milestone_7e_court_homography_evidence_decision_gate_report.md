# Milestone 7E Agent Report - Court / Homography Evidence Decision Gate

## Summary

Milestone 7E is a docs and architecture decision gate. It defers court/camera/homography implementation to Blueprint 8, proposes the future evidence contract, and keeps Blueprint 7 focused on real detection, real-detection-derived candidate tracklets, real pose keypoint evidence, orchestration, and closeout.

## Files Created

- `docs/court/court_homography_evidence_decision_v0.md`
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`
- `docs/milestones/milestone_7e_court_homography_evidence_decision_gate.md`
- `docs/handoffs/milestone_7e_court_homography_evidence_decision_gate_handoff.md`
- `docs/agent_reports/milestone_7e_court_homography_evidence_decision_gate_report.md`

## Files Modified

- `README.md`
- `docs/CONTROL_ROOM.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CURRENT_STATE.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md`

## Decision

Court / camera / homography evidence should be Blueprint 8.

Blueprint 7 should not absorb court/homography runtime, schema migration, court overlay rendering, production coordinate transforms, or tennis-event interpretation.

## Court Evidence Contract Decisions

7E proposes a future `court` observation family with candidate observation types:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

The proposed contract keeps media-owned frame/time, explicit coordinate spaces, model/runtime/config provenance, confidence fields, raw payloads, metadata, and review annotations.

## Homography Candidate Decisions

Homography should be persisted as candidate geometry evidence derived from source court keypoints and/or court lines. The future contract should include source observation ids, a homography matrix, target court template metadata, reprojection error, inlier count, confidence, status, and lineage.

## Replay Integration Decisions

Future Blueprint 8 replay layers should be toggleable and source-aware:

- court keypoint evidence
- court line evidence
- homography candidate
- projection diagnostic

Selected detail should show frame/time, model/runtime/config, source evidence, matrix, diagnostics, lineage, artifacts, annotations, and candidate-only wording.

## Review / Export Decisions

Future review labels should cover court keypoints, court lines, homography candidates, projection diagnostics, occlusion, unstable camera views, insufficient source evidence, and uncertain geometry. Future TOM-native exports should preserve source evidence, matrix/diagnostics, lineage, artifacts, and annotations.

## Risks / Tradeoffs

- Court geometry can be mistaken for a final geometry model too early.
- Homography quality depends on camera view.
- Broadcast overlays and cuts can disrupt court evidence.
- Projection into court space can invite event interpretation.
- Schema scope can expand quickly.
- Replay overlays can become visually cluttered.

Mitigations are candidate/evidence wording, camera/view state, confidence and diagnostics, explicit future-blueprint boundaries, toggleable replay layers, and no event interpretation inside Blueprint 8 unless deliberately scoped later.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7e_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7e_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`

## Validation Results

- Full Python suite: passed, 198 tests.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed with `demo_assets/sample_point.mp4`.
- Completion audit: passed with `status = passed`.

## Known Limitations

- 7E is docs/status only.
- No court/homography runtime exists yet.
- No schema migration exists yet.
- No replay court overlay exists yet.
- Court/homography remains future Blueprint 8 work.

## Non-goals Preserved

7E does not add court runtime, homography computation, court overlays, court-space coordinate transforms, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Handoff

Milestone 7F - Perception Run Orchestration and Completion Review.
