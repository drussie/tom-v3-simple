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
    source = (ROOT / "apps/web/src/lib/replayOverlays.ts").read_text()

    assert 'displayMode === "current_only"' in source
    assert 'displayMode === "short_trail"' in source or '"short_trail"' in source
    assert 'displayMode === "full_trail"' in source
    assert "isActiveReplayPointForDisplay" in source
    assert "activeReplayMainPlayerTracks" in source
    assert "filterMainPlayerTracksAvailableAt" in source
    assert "activeReplaySmoothedBall" in source
    assert "activeReplaySmoothedPlayerBoxes" in source
    assert "activeReplaySmoothedPoses" in source
    assert "activeReplayCourtEvidence" in source
    assert 'item.temporal_display_mode === "carry_forward"' in source
    assert "current_replay_timestamp_ms" in source
