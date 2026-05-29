from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from apps.api.db import get_session
from apps.api.services.replay import (
    COURT_TEMPORAL_PERSISTENCE_MODES,
    DEFAULT_COURT_PERSISTENCE_MAX_GAP_MS,
    build_replay_overlay_chunk,
    build_replay_timeline,
    normalize_court_temporal_persistence,
    normalize_replay_layers,
)

router = APIRouter(tags=["replay"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/replay/overlays")
def get_replay_overlays(
    session: SessionDep,
    media_id: str,
    start_ms: int = Query(..., ge=0),
    end_ms: int = Query(..., ge=0),
    layers: str = "detections",
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    main_player_track_run_id: str | None = None,
    motion_smoothing_run_id: str | None = None,
    court_run_id: str | None = None,
    homography_run_id: str | None = None,
    projection_diagnostic_run_id: str | None = None,
    court_projection_run_id: str | None = None,
    ball_trajectory_run_id: str | None = None,
    court_temporal_persistence: str = Query(default="carry_forward"),
    court_persistence_max_gap_ms: int = Query(
        default=DEFAULT_COURT_PERSISTENCE_MAX_GAP_MS,
        ge=0,
        le=60000,
    ),
    min_confidence: float | None = Query(default=None, ge=0.0, le=1.0),
    min_pose_confidence: float | None = Query(default=None, ge=0.0, le=1.0),
) -> dict[str, object]:
    if start_ms > end_ms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_ms must be less than or equal to end_ms",
        )
    raw_court_temporal_persistence = court_temporal_persistence.strip().lower().replace("-", "_")
    if raw_court_temporal_persistence not in COURT_TEMPORAL_PERSISTENCE_MODES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="court_temporal_persistence must be off or carry_forward",
        )
    normalized_court_temporal_persistence = normalize_court_temporal_persistence(
        court_temporal_persistence
    )

    chunk = build_replay_overlay_chunk(
        session,
        media_id=media_id,
        start_ms=start_ms,
        end_ms=end_ms,
        layers=normalize_replay_layers(layers),
        detection_run_id=detection_run_id,
        tracklet_run_id=tracklet_run_id,
        pose_run_id=pose_run_id,
        main_player_track_run_id=main_player_track_run_id,
        motion_smoothing_run_id=motion_smoothing_run_id,
        court_run_id=court_run_id,
        homography_run_id=homography_run_id,
        projection_diagnostic_run_id=projection_diagnostic_run_id,
        court_projection_run_id=court_projection_run_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_temporal_persistence=normalized_court_temporal_persistence,
        court_persistence_max_gap_ms=court_persistence_max_gap_ms,
        min_confidence=min_confidence,
        min_pose_confidence=min_pose_confidence,
    )
    if chunk is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="media asset not found")
    return chunk


@router.get("/replay/timeline")
def get_replay_timeline(
    session: SessionDep,
    media_id: str,
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    main_player_track_run_id: str | None = None,
    motion_smoothing_run_id: str | None = None,
    court_run_id: str | None = None,
    homography_run_id: str | None = None,
    projection_diagnostic_run_id: str | None = None,
    court_projection_run_id: str | None = None,
    ball_trajectory_run_id: str | None = None,
    include_annotations: bool = True,
) -> dict[str, object]:
    timeline = build_replay_timeline(
        session,
        media_id=media_id,
        detection_run_id=detection_run_id,
        tracklet_run_id=tracklet_run_id,
        pose_run_id=pose_run_id,
        main_player_track_run_id=main_player_track_run_id,
        motion_smoothing_run_id=motion_smoothing_run_id,
        court_run_id=court_run_id,
        homography_run_id=homography_run_id,
        projection_diagnostic_run_id=projection_diagnostic_run_id,
        court_projection_run_id=court_projection_run_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        include_annotations=include_annotations,
    )
    if timeline is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="media asset not found")
    return timeline
