from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def makefile_text() -> str:
    return (ROOT / "Makefile").read_text()


def test_tom_v1_make_helpers_include_allowed_root_and_imgsz_defaults() -> None:
    makefile = makefile_text()

    assert '--allowed-root "$(TOM_V1_MODEL_ROOT)"' in makefile
    assert 'tom-v1-ball-detection:' in makefile
    assert '--imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),1280)"' in makefile
    assert 'tom-v1-player-detection:' in makefile
    assert '--imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)"' in makefile
    assert 'tom-v1-pose:' in makefile
    assert '--weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt"' in makefile
    assert "tom-v1-main-subjects:" in makefile
    assert "select-main-player-subjects" in makefile
    assert "tom-v1-main-player-tracks:" in makefile
    assert "assign-main-player-tracks" in makefile
    assert "tom-v1-pose-main-subjects:" in makefile
    assert '--source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)"' in makefile
    assert "tom-v1-pose-main-tracks:" in makefile
    assert '--source-track-run-id "$(SOURCE_TRACK_RUN_ID)"' in makefile
    assert "tom-v1-motion-smoothing:" in makefile
    assert "smooth-motion-candidates" in makefile
    assert '--main-player-track-run-id "$(MAIN_PLAYER_TRACK_RUN_ID)"' in makefile
    assert "--run-name motion-smoothing-stable-replay-candidates-v0" in makefile


def test_replay_display_policy_helpers_define_expected_modes() -> None:
    makefile = makefile_text()
    source = (ROOT / "apps/web/src/lib/replayOverlays.ts").read_text()
    workstation = (ROOT / "apps/web/src/components/ReplayWorkstation.tsx").read_text()
    overlay = (ROOT / "apps/web/src/components/ReplaySmoothedMotionOverlay.tsx").read_text()
    pose_overlay = (ROOT / "apps/web/src/components/ReplayPoseOverlay.tsx").read_text()
    css = (ROOT / "apps/web/src/app/globals.css").read_text()

    assert 'displayMode === "current_only"' in source
    assert 'displayMode === "short_trail"' in source or '"short_trail"' in source
    assert 'displayMode === "full_trail"' in source
    assert "isActiveReplayPointForDisplay" in source
    assert "activeReplayMainPlayerTracks" in source
    assert "filterMainPlayerTracksAvailableAt" in source
    assert "activeReplaySmoothedBall" in source
    assert "activeReplaySmoothedPlayerBoxes" in source
    assert "activeReplaySmoothedPoses" in source
    assert 'displayMode: ReplayOverlayDisplayMode = "current_only"' in source
    assert "selectNearestCurrentSmoothedCandidate" in source
    assert "selectCurrentSmoothedCandidatesByKey" in source
    assert "track_role_candidate ?? item.track_candidate_id" in source
    assert "track_candidate_id ?? item.track_role_candidate" in source
    assert "bExactFrame - aExactFrame" in source
    assert "localeCompare" in source
    assert "initialLayerPresetState.detectionDisplayMode" in workstation
    assert "initialLayerPresetState.smoothedMotionDisplayMode" in workstation
    assert "Smoothed motion display" in workstation
    assert "displayMode={smoothedMotionDisplayMode}" in workstation
    assert 'displayMode = "current_only"' in overlay
    assert "labelBallIds" in overlay
    assert "labelBoxIds" in overlay
    assert 'ReplayPoseVisualStyle = "limbs_only" | "limbs_and_joints" | "joints_only"' in (
        ROOT / "apps/web/src/lib/types.ts"
    ).read_text()
    assert "poseEdgeSideClass" in source
    assert 'start.startsWith("left_") && end.startsWith("left_")' in source
    assert 'start.startsWith("right_") && end.startsWith("right_")' in source
    assert "initialLayerPresetState.poseVisualStyle" in workstation
    assert "Pose visual style" in workstation
    assert "poseVisualStyle={poseVisualStyle}" in workstation
    assert 'poseVisualStyle = "limbs_only"' in pose_overlay
    assert 'poseVisualStyle = "limbs_only"' in overlay
    assert 'const showLimbs = poseVisualStyle !== "joints_only"' in pose_overlay
    assert 'const showJoints = poseVisualStyle !== "limbs_only"' in pose_overlay
    assert 'const showLimbs = poseVisualStyle !== "joints_only"' in overlay
    assert 'const showJoints = poseVisualStyle !== "limbs_only"' in overlay
    assert "pose-limb-${poseEdgeSideClass(start, end)}" in pose_overlay
    assert "replay-smoothed-pose-edge" in overlay
    assert ".replay-pose-group .pose-limb-left" in css
    assert ".replay-pose-group .pose-limb-right" in css
    assert ".replay-pose-group .pose-limb-neutral" in css
    assert "activeReplayCourtEvidence" in source
    assert 'item.temporal_display_mode === "carry_forward"' in source
    assert "current_replay_timestamp_ms" in source
    assert 'ReplayLayerPreset = "operator" | "debug"' in (
        ROOT / "apps/web/src/lib/types.ts"
    ).read_text()
    assert "normalizeReplayLayerPreset" in workstation
    assert "applyLayerPreset" in workstation
    assert "Replay view preset" in workstation
    assert "Operator view" in workstation
    assert "Debug / audit view" in workstation
    assert "showRawCourtKeypoints: false" in workstation
    assert "showHomography: false" in workstation
    assert "showProjectionDiagnostics: false" in workstation
    assert "showBallCourtProjection: context.hasCourtProjectionRun" in workstation
    assert "showMainPlayerCourtProjection: context.hasCourtProjectionRun" in workstation
    assert "showBallCourtTrajectory: context.hasBallTrajectoryRun" in workstation
    assert "showEventCandidates: context.hasEventCandidateRun" in workstation
    assert "showSmoothedBall: context.hasMotionSmoothingRun" in workstation
    assert "showSmoothedPlayerBoxes: context.hasMotionSmoothingRun" in workstation
    assert "showSmoothedPoses: context.hasMotionSmoothingRun" in workstation
    assert "courtTemporalPersistence: \"carry_forward\"" in workstation
    assert "viewPreset?: string" in (
        ROOT / "apps/web/src/app/replay/[mediaId]/page.tsx"
    ).read_text()
    assert "ballTrajectoryRunId?: string" in (
        ROOT / "apps/web/src/app/replay/[mediaId]/page.tsx"
    ).read_text()
    assert "ReplayBallCourtTrajectoryOverlay" in (ROOT / "apps/web/src/lib/types.ts").read_text()
    assert "ballTrajectoryRunId" in (ROOT / "apps/web/src/lib/api.ts").read_text()
    assert "eventCandidateRunId" in (ROOT / "apps/web/src/lib/api.ts").read_text()
    assert "eventCandidateRunId?: string" in (
        ROOT / "apps/web/src/app/replay/[mediaId]/page.tsx"
    ).read_text()
    assert "BALL TRAJECTORY CANDIDATE" in (
        ROOT / "apps/web/src/components/ReplayCourtProjectionMiniMap.tsx"
    ).read_text()
    assert "HIT CANDIDATE" in (
        ROOT / "apps/web/src/components/ReplayCourtProjectionMiniMap.tsx"
    ).read_text()
    assert "BOUNCE CANDIDATE" in (
        ROOT / "apps/web/src/components/ReplayCourtProjectionMiniMap.tsx"
    ).read_text()
    assert "tom-v1-hit-bounce-candidates:" in makefile
    assert "build-hit-bounce-candidates" in makefile
    assert '--ball-trajectory-run-id "$(BALL_TRAJECTORY_RUN_ID)"' in makefile
    assert '--court-projection-run-id "$(COURT_PROJECTION_RUN_ID)"' in makefile
