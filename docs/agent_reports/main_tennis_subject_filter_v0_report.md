# Main Tennis Player Subject Filter v0 Report

## Summary

Added a candidate subject selection layer that reduces broad `player_detection` pose sources to at most two tennis-player subject candidates per frame: `near_player_candidate` and `far_player_candidate`.

The filter persists `main_player_subject_candidate` observations and preserves lineage from source `player_detection` observations. Real pose crop mode can now consume a `source_subject_run_id` so pose inference runs only on selected candidate subjects.

## Files Created

- `apps/worker/services/main_subject_filter.py`
- `docs/perception/main_tennis_subject_filter_v0.md`
- `docs/agent_reports/main_tennis_subject_filter_v0_report.md`
- `tests/test_main_subject_filter.py`

## Files Modified

- `Makefile`
- `apps/worker/cli.py`
- `apps/worker/services/real_pose_replay.py`
- `packages/model_adapters/tom_v3_model_adapters/pose_normalization.py`
- `packages/schema/tom_v3_schema/enums.py`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`
- `README.md`
- `tests/test_tom_v1_bridge_helpers.py`

## Design Decisions

- Used existing observation spine rows with `observation_family = tracking` and `observation_type = main_player_subject_candidate`.
- Avoided a database migration and avoided a parallel subject store.
- Preserved raw `player_detection` observations unchanged.
- Stored selection score/features in payload JSON and runtime config.
- Added lineage from raw detections to subject candidates.
- Added pose lineage from selected candidates to pose observations when `source_subject_run_id` is used.

## Pose Integration

`run-real-pose` now accepts `--source-subject-run-id`. When supplied in crop-from-player-detection mode, pose crops use only selected source detections referenced by `main_player_subject_candidate` observations.

Without `--source-subject-run-id`, the existing broad player-detection crop behavior remains available.

## Non-goals Preserved

- No confirmed player identity.
- No tennis-event interpretation.
- No bounce/hit/in-out/rally/point/scoring.
- No ball/player court-space projection.
- No accepted/rejected lifecycle.
- No mutation or deletion of raw detections.

## Validation Results

- Focused tests: `14 passed`
- Full Python tests: `251 passed`
- Ruff: passed
- Web lint/build/audit: passed; `npm audit --omit=dev` found `0 vulnerabilities`

## Optional Local Smoke

Using `sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db`:

- Source player detection run: `62dc6f02-8173-47b2-b7fa-9d6726ccfc3e`
- Main subject run: `1e7e863a-25e5-4b5e-a9be-7cc0cd833339`
- Raw player detections considered: `1514`
- Main subject candidates: `428`
- Filtered pose run: `a0a49cae-6a3e-4ed1-8359-e75214be0788`
- Filtered pose observations: `424`
- Pose lineage: `424` `pose_from_subject_detection_candidate` rows and `424` `pose_from_main_subject_candidate` rows
- Replay overlay proxy returned filtered pose payloads with `subject_candidate_observation_id`, `subject_role_candidate`, `candidate_subject_only`, and `not_identity_truth`

## Recommended Next Step

Use the TOM v1 player detection run, run `make tom-v1-main-subjects`, then run `make tom-v1-pose-main-subjects` and inspect the filtered pose replay.
