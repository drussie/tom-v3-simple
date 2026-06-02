from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from tom_v3_schema.event_candidate_reviews import (
    EventCandidateReviewCreate,
    EventCandidateReviewList,
    EventCandidateReviewRead,
    EventCandidateReviewUpdate,
)

from apps.api.db import get_session
from apps.api.services.event_candidate_reviews import (
    EventCandidateReviewError,
    create_event_candidate_review,
    delete_event_candidate_review,
    list_event_candidate_reviews,
    serialize_event_candidate_review,
    update_event_candidate_review,
)
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
    event_candidate_run_id: str | None = None,
    trajectory_3d_run_id: str | None = None,
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
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
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
    event_candidate_run_id: str | None = None,
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
        event_candidate_run_id=event_candidate_run_id,
        include_annotations=include_annotations,
    )
    if timeline is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="media asset not found")
    return timeline


@router.get(
    "/replay/{media_id}/event-candidate-reviews",
    response_model=EventCandidateReviewList,
)
def get_event_candidate_reviews(
    media_id: str,
    session: SessionDep,
    event_candidate_run_id: str = Query(...),
) -> dict[str, object]:
    try:
        return list_event_candidate_reviews(
            session,
            media_id=media_id,
            event_candidate_run_id=event_candidate_run_id,
        )
    except EventCandidateReviewError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error


@router.post(
    "/replay/{media_id}/event-candidate-reviews",
    response_model=EventCandidateReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def post_event_candidate_review(
    media_id: str,
    request: EventCandidateReviewCreate,
    session: SessionDep,
) -> dict[str, object]:
    try:
        row = create_event_candidate_review(session, media_id=media_id, request=request)
        return serialize_event_candidate_review(row)
    except EventCandidateReviewError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error


@router.patch(
    "/replay/{media_id}/event-candidate-reviews/{review_id}",
    response_model=EventCandidateReviewRead,
)
def patch_event_candidate_review(
    media_id: str,
    review_id: str,
    request: EventCandidateReviewUpdate,
    session: SessionDep,
) -> dict[str, object]:
    try:
        row = update_event_candidate_review(
            session,
            media_id=media_id,
            review_id=review_id,
            request=request,
        )
        return serialize_event_candidate_review(row)
    except EventCandidateReviewError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error


@router.delete("/replay/{media_id}/event-candidate-reviews/{review_id}")
def delete_event_candidate_review_endpoint(
    media_id: str,
    review_id: str,
    session: SessionDep,
) -> dict[str, object]:
    try:
        return delete_event_candidate_review(session, media_id=media_id, review_id=review_id)
    except EventCandidateReviewError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
