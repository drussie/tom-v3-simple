# Milestone 7F Agent Report - Perception Run Orchestration and Completion Review

## Summary

Milestone 7F closes Blueprint 7. It adds the final Blueprint 7 completion review, documents the final real perception orchestration ladder, marks Blueprint 7 complete in canonical docs, and preserves the Blueprint 8 boundary for court/camera/homography evidence.

## Files Created

- `docs/blueprints/tom_v3_blueprint_7_completion_review.md`
- `docs/milestones/milestone_7f_perception_run_orchestration_completion_review.md`
- `docs/handoffs/milestone_7f_perception_run_orchestration_completion_review_handoff.md`
- `docs/agent_reports/milestone_7f_perception_run_orchestration_completion_review_report.md`

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
- `docs/OPTIONAL_YOLO.md`
- `docs/perception/real_detection_replay_v0.md`
- `docs/perception/real_pose_replay_v0.md`
- `docs/court/court_homography_evidence_decision_v0.md`
- `docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md`
- `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md`

## Final Blueprint 7 Verdict

Blueprint 7 is complete.

TOM v3 can run optional real detection, build candidate tracklets from real detections, run optional real pose, preserve provenance and lineage, and show all three evidence layers in the replay workstation.

## Final Perception Ladder

```text
indexed media
-> optional real YOLO detection
-> real ball/player detection observations
-> candidate tracklets from real detections
-> source detection lineage
-> optional real pose keypoint observations
-> source player detection lineage when available
-> replay detection / tracklet / pose overlays
```

## Final Orchestration / Runbook Decisions

The final runbook keeps `make demo` and `make completion-audit` as the fixture-safe baseline. Real detection and real pose remain optional local-runtime paths. Real-detection-derived tracklets use the existing `build-tracklets` command.

## Optional Runtime Smoke Decision / Results

Optional real detection/pose smoke not run: no local weights found under `model_assets/` or `weights/`.

Plan-only real detection and plan-only real pose checks passed. This confirms the commands remain callable without requiring local model weights in the default validation path.

## Validation Results

- `.venv/bin/python -m pytest -q`: passed, 198 tests.
- `ruff check .`: passed.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`: passed.
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`: passed.
- Fixture demo with `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4`: passed.
- Fixture completion audit on `tmp_tom_v3_7f_fixture_demo.db`: passed.
- Plan-only `run-real-detection`: passed.
- Plan-only `run-real-pose`: passed.

## Known Limitations

- Real detection requires optional runtime dependencies and local YOLO weights.
- Real pose requires optional runtime dependencies and local pose weights.
- Candidate tracklets inherit source detection limitations.
- Pose observations are keypoint evidence only.
- Court/camera/homography remains future Blueprint 8 work.
- No event interpretation is added.

## Non-goals Preserved

7F adds no new runtime behavior, court/homography implementation, database schema, frontend features, bounce/hit/rally/point/scoring, movement/stroke interpretation, real stream ingestion, production deployment, or adjudication.

## Blueprint 8 Boundary

Court/camera/homography evidence is deferred to Blueprint 8. Future court work should begin from `docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md` and `docs/court/court_homography_evidence_decision_v0.md`.

## Push Status

Prepared for final commit, tag, and push on `codex/m7f-perception-run-orchestration-completion-review`. The final response records the exact commit SHA, tag, and remote push confirmation.

## Recommended Next Step

Stop Blueprint 7. Use/demo the real perception replay ladder when local weights are available.

Future work should begin as separate blueprints only if deliberately chosen:

- Blueprint 8 - Court / Camera / Homography Evidence Layer
- Blueprint 9 - Bounce / Hit Candidate Evidence
- Blueprint 10 - Movement / Stroke Evidence Candidates
- Blueprint 11 - Real Stream Ingestion
- Product Deployment Blueprint
