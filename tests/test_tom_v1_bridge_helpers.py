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


def test_replay_display_policy_helpers_define_expected_modes() -> None:
    source = (ROOT / "apps/web/src/lib/replayOverlays.ts").read_text()

    assert 'displayMode === "current_only"' in source
    assert 'displayMode === "short_trail"' in source or '"short_trail"' in source
    assert 'displayMode === "full_trail"' in source
    assert "isActiveReplayPointForDisplay" in source
