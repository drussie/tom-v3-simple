from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_schema.court import get_court_template
from tom_v3_schema.skeletons import get_skeleton_definition
from tom_v3_storage.db_models import (
    AtomicObservation,
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    HomographyCandidateObservation,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    PoseObservation,
    ProcessingRun,
    Tracklet,
    TrackPoint,
)
from tom_v3_video.paths import local_path_from_uri_or_path

DETECTION_TYPES = {"ball_detection", "player_detection"}
TRACKLET_TYPES = {
    "ball_tracklet_candidate",
    "player_tracklet_candidate",
    "track_point_candidate",
}
POSE_TYPES = {"player_pose_observation"}
GAMEPLAY_TYPES = {"view_state"}
COURT_KEYPOINT_TYPES = {"court_keypoint_observation"}
COURT_LINE_TYPES = {"court_line_observation"}
CAMERA_VIEW_TYPES = {"camera_view_observation"}
COURT_EVIDENCE_TYPES = COURT_KEYPOINT_TYPES | COURT_LINE_TYPES | CAMERA_VIEW_TYPES
HOMOGRAPHY_TYPES = {"homography_candidate_observation"}


def timestamp_ms_to_replay_frame(media: MediaAsset, timestamp_ms: int | float | None) -> int:
    fps = _positive_float(media.fps)
    frame_count = _positive_int(media.frame_count)
    if fps is None or frame_count is None or timestamp_ms is None:
        return 0
    frame = round((float(timestamp_ms) / 1000.0) * fps)
    return _clamp_frame(frame, frame_count)


def frame_to_replay_timestamp_ms(media: MediaAsset, frame_number: int | float | None) -> int:
    fps = _positive_float(media.fps)
    frame_count = _positive_int(media.frame_count)
    if fps is None or frame_number is None:
        return 0
    frame = int(round(float(frame_number)))
    if frame_count is not None:
        frame = _clamp_frame(frame, frame_count)
    else:
        frame = max(0, frame)
    return int(round((frame / fps) * 1000.0))


def current_time_seconds_to_frame(
    media: MediaAsset,
    current_time_seconds: int | float | None,
) -> int:
    if current_time_seconds is None:
        return 0
    return timestamp_ms_to_replay_frame(media, float(current_time_seconds) * 1000.0)


def build_replay_info(session: Session, media_id: str) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    frame_time_index = (media.metadata_jsonb or {}).get("frame_time_index")
    return {
        "media_id": media.id,
        "video_url": f"/media/{media.id}/video",
        "source_uri": media.source_uri,
        "width": media.width,
        "height": media.height,
        "duration_ms": media.duration_ms,
        "fps": media.fps,
        "frame_count": media.frame_count,
        "frame_time_mode": "indexed" if media.fps and media.frame_count else "unavailable",
        "frame_time_index": frame_time_index,
        "available_runs": available_runs_for_media(session, media.id),
        "observation_only": True,
        "no_adjudication": True,
    }


def build_replay_overlay_chunk(
    session: Session,
    *,
    media_id: str,
    start_ms: int,
    end_ms: int,
    layers: set[str],
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    court_run_id: str | None = None,
    homography_run_id: str | None = None,
    min_confidence: float | None = None,
    min_pose_confidence: float | None = None,
) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    detections = (
        build_detection_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            detection_run_id=detection_run_id,
            min_confidence=min_confidence,
        )
        if "detections" in layers
        else []
    )
    tracklets = (
        build_tracklet_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            tracklet_run_id=tracklet_run_id,
        )
        if "tracklets" in layers
        else []
    )
    poses = (
        build_pose_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            pose_run_id=pose_run_id,
            min_pose_confidence=min_pose_confidence,
        )
        if "pose" in layers
        else []
    )
    court_keypoints = (
        build_court_keypoint_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            court_run_id=court_run_id,
        )
        if "court_keypoints" in layers
        else []
    )
    court_lines = (
        build_court_line_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            court_run_id=court_run_id,
        )
        if "court_lines" in layers
        else []
    )
    camera_view = (
        build_camera_view_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            court_run_id=court_run_id,
        )
        if "camera_view" in layers
        else []
    )
    homography_candidates = (
        build_homography_candidate_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            homography_run_id=homography_run_id,
        )
        if "homography_candidates" in layers
        else []
    )
    return {
        "media_id": media.id,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "coordinate_space": "image_pixels",
        "video_width": media.width,
        "video_height": media.height,
        "detections": detections,
        "tracklets": tracklets,
        "poses": poses,
        "court_keypoints": court_keypoints,
        "court_lines": court_lines,
        "camera_view": camera_view,
        "homography_candidates": homography_candidates,
        "observation_only": True,
        "no_adjudication": True,
    }


def build_replay_timeline(
    session: Session,
    *,
    media_id: str,
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    court_run_id: str | None = None,
    homography_run_id: str | None = None,
    include_annotations: bool = True,
) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    annotation_items: list[dict[str, Any]] = []
    annotations_without_time_count = 0
    if include_annotations:
        annotation_items, annotations_without_time_count = build_annotation_timeline_items(
            session=session,
            media=media,
            selected_run_ids={
                run_id
                for run_id in (
                    detection_run_id,
                    tracklet_run_id,
                    pose_run_id,
                    court_run_id,
                    homography_run_id,
                )
                if run_id is not None
            },
        )

    return {
        "media_id": media.id,
        "duration_ms": media.duration_ms,
        "frame_count": media.frame_count,
        "fps": media.fps,
        "observation_only": True,
        "no_adjudication": True,
        "annotations_without_time_count": annotations_without_time_count,
        "lanes": [
            {
                "lane_type": "detections",
                "label": "Detection observations",
                "items": build_detection_timeline_items(
                    session=session,
                    media=media,
                    detection_run_id=detection_run_id,
                ),
            },
            {
                "lane_type": "tracklets",
                "label": "Tracklet candidates",
                "items": build_tracklet_timeline_items(
                    session=session,
                    media=media,
                    tracklet_run_id=tracklet_run_id,
                ),
            },
            {
                "lane_type": "pose",
                "label": "Pose observations",
                "items": build_pose_timeline_items(
                    session=session,
                    media=media,
                    pose_run_id=pose_run_id,
                ),
            },
            {
                "lane_type": "court_keypoints",
                "label": "Court keypoint evidence",
                "items": build_court_keypoint_timeline_items(
                    session=session,
                    media=media,
                    court_run_id=court_run_id,
                ),
            },
            {
                "lane_type": "court_lines",
                "label": "Court line evidence",
                "items": build_court_line_timeline_items(
                    session=session,
                    media=media,
                    court_run_id=court_run_id,
                ),
            },
            {
                "lane_type": "camera_view",
                "label": "Camera/view evidence",
                "items": build_camera_view_timeline_items(
                    session=session,
                    media=media,
                    court_run_id=court_run_id,
                ),
            },
            {
                "lane_type": "homography_candidates",
                "label": "Homography candidates",
                "items": build_homography_candidate_timeline_items(
                    session=session,
                    media=media,
                    homography_run_id=homography_run_id,
                ),
            },
            {
                "lane_type": "annotations",
                "label": "Review annotations",
                "items": annotation_items,
            },
        ],
    }


def build_detection_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    detection_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.observation_family == "atomic",
            Observation.observation_type.in_(sorted(DETECTION_TYPES)),
        )
        .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
    )
    if detection_run_id is not None:
        query = query.where(Observation.run_id == detection_run_id)

    items: list[dict[str, Any]] = []
    for observation in session.scalars(query).all():
        item = detection_timeline_item_from_observation(observation)
        if item is not None:
            items.append(item)
    return items


def detection_timeline_item_from_observation(
    observation: Observation,
) -> dict[str, Any] | None:
    if observation.observation_type not in DETECTION_TYPES:
        return None

    frame_number, timestamp_ms = _observation_frame_time(observation)
    if frame_number is None or timestamp_ms is None:
        return None

    payload = _merged_detection_payload(observation)
    label = _detection_label(observation, payload)
    source_metadata = _detection_source_metadata(observation, payload)
    return {
        "item_type": "detection",
        "observation_id": observation.id,
        "run_id": observation.run_id,
        "timestamp_ms": timestamp_ms,
        "frame_number": frame_number,
        "label": label,
        "observation_type": observation.observation_type,
        "confidence": observation.confidence,
        "display_label": f"{label} detection observation · {source_metadata['source_label']}",
        **source_metadata,
    }


def build_tracklet_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    tracklet_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Tracklet)
        .where(Tracklet.media_id == media.id)
        .order_by(Tracklet.frame_start, Tracklet.id)
    )
    if tracklet_run_id is not None:
        query = query.where(Tracklet.run_id == tracklet_run_id)

    items: list[dict[str, Any]] = []
    for tracklet in session.scalars(query).all():
        item = tracklet_timeline_item_from_row(media, tracklet)
        if item is not None:
            items.append(item)
    return items


def tracklet_timeline_item_from_row(
    media: MediaAsset,
    tracklet: Tracklet,
) -> dict[str, Any] | None:
    overlay_item = tracklet_overlay_item_from_row(media, tracklet)
    if overlay_item is None:
        return None

    label_hint = overlay_item["label_hint"] or overlay_item["track_type"]
    return {
        "item_type": "tracklet",
        "observation_id": overlay_item["observation_id"],
        "tracklet_id": overlay_item["tracklet_id"],
        "run_id": overlay_item["run_id"],
        "timestamp_start_ms": overlay_item["timestamp_start_ms"],
        "timestamp_end_ms": overlay_item["timestamp_end_ms"],
        "frame_start": overlay_item["frame_start"],
        "frame_end": overlay_item["frame_end"],
        "label_hint": overlay_item["label_hint"],
        "track_type": overlay_item["track_type"],
        "track_status": overlay_item["track_status"],
        "identity_status": overlay_item["identity_status"],
        "track_point_count": len(overlay_item["points"]),
        "display_label": f"{label_hint} tracklet candidate",
        "source_detection_run_id": overlay_item["source_detection_run_id"],
        "source_detection_evidence_source": overlay_item["source_detection_evidence_source"],
        "source_detection_source_label": overlay_item["source_detection_source_label"],
        "source_detection_runtime": overlay_item["source_detection_runtime"],
        "source_detection_real_model_output": overlay_item[
            "source_detection_real_model_output"
        ],
        "is_real_detection_derived": overlay_item["is_real_detection_derived"],
        "candidate_evidence_only": overlay_item["candidate_evidence_only"],
    }


def build_pose_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    pose_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(PoseObservation)
        .where(PoseObservation.media_id == media.id)
        .order_by(PoseObservation.timestamp_ms, PoseObservation.observation_id)
    )
    if pose_run_id is not None:
        query = query.where(PoseObservation.run_id == pose_run_id)

    items: list[dict[str, Any]] = []
    for pose in session.scalars(query).all():
        item = pose_timeline_item_from_row(pose)
        if item is not None:
            items.append(item)
    return items


def pose_timeline_item_from_row(pose: PoseObservation) -> dict[str, Any] | None:
    if pose.frame_number is None or pose.timestamp_ms is None:
        return None

    source_metadata = _pose_source_metadata(pose)
    return {
        "item_type": "pose",
        "observation_id": pose.observation_id,
        "run_id": pose.run_id,
        "timestamp_ms": pose.timestamp_ms,
        "frame_number": pose.frame_number,
        "pose_confidence": pose.pose_confidence,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "display_label": _pose_display_label(source_metadata),
        **source_metadata,
    }


def build_court_keypoint_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(CourtKeypointObservation)
        .where(CourtKeypointObservation.media_id == media.id)
        .order_by(CourtKeypointObservation.timestamp_ms, CourtKeypointObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CourtKeypointObservation.run_id == court_run_id)
    return [court_keypoint_timeline_item_from_row(row) for row in session.scalars(query).all()]


def court_keypoint_timeline_item_from_row(
    row: CourtKeypointObservation,
) -> dict[str, Any]:
    return {
        "item_type": "court_keypoint",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "timestamp_ms": row.timestamp_ms,
        "frame_number": row.frame_number,
        "court_keypoint_schema": row.court_keypoint_schema,
        "schema_version": row.schema_version,
        "keypoint_count": row.keypoint_count,
        "keypoints_present_count": row.keypoints_present_count,
        "keypoints_missing_count": row.keypoints_missing_count,
        "mean_keypoint_confidence": row.mean_keypoint_confidence,
        "display_label": "court keypoint evidence",
        **_court_source_metadata(row, "court keypoint evidence"),
    }


def build_court_line_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(CourtLineObservation)
        .where(CourtLineObservation.media_id == media.id)
        .order_by(CourtLineObservation.timestamp_ms, CourtLineObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CourtLineObservation.run_id == court_run_id)
    return [court_line_timeline_item_from_row(row) for row in session.scalars(query).all()]


def court_line_timeline_item_from_row(row: CourtLineObservation) -> dict[str, Any]:
    return {
        "item_type": "court_line",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "timestamp_ms": row.timestamp_ms,
        "frame_number": row.frame_number,
        "line_count": row.line_count,
        "line_classes": row.line_classes_jsonb,
        "mean_line_confidence": row.mean_line_confidence,
        "display_label": "court line evidence",
        **_court_source_metadata(row, "court line evidence"),
    }


def build_camera_view_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(CameraViewObservation)
        .where(CameraViewObservation.media_id == media.id)
        .order_by(CameraViewObservation.timestamp_ms, CameraViewObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CameraViewObservation.run_id == court_run_id)
    return [camera_view_timeline_item_from_row(row) for row in session.scalars(query).all()]


def camera_view_timeline_item_from_row(row: CameraViewObservation) -> dict[str, Any]:
    return {
        "item_type": "camera_view",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "timestamp_ms": row.timestamp_ms,
        "frame_number": row.frame_number,
        "frame_start": row.frame_start,
        "frame_end": row.frame_end,
        "timestamp_start_ms": row.timestamp_start_ms,
        "timestamp_end_ms": row.timestamp_end_ms,
        "view_label": row.view_label,
        "view_confidence": row.view_confidence,
        "camera_motion_hint": row.camera_motion_hint,
        "stability_score": row.stability_score,
        "cut_likelihood": row.cut_likelihood,
        "display_label": "camera/view evidence",
        **_court_source_metadata(row, "camera/view evidence"),
    }


def build_homography_candidate_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    homography_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(HomographyCandidateObservation)
        .where(HomographyCandidateObservation.media_id == media.id)
        .order_by(
            HomographyCandidateObservation.timestamp_ms,
            HomographyCandidateObservation.observation_id,
        )
    )
    if homography_run_id is not None:
        query = query.where(HomographyCandidateObservation.run_id == homography_run_id)
    return [
        homography_candidate_timeline_item_from_row(row) for row in session.scalars(query).all()
    ]


def homography_candidate_timeline_item_from_row(
    row: HomographyCandidateObservation,
) -> dict[str, Any]:
    return {
        "item_type": "homography_candidate",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "timestamp_ms": row.timestamp_ms,
        "frame_number": row.frame_number,
        "status": row.status,
        "template_name": row.template_name,
        "template_version": row.template_version,
        "matrix_direction": row.matrix_direction,
        "source_point_count": row.source_point_count,
        "source_line_count": row.source_line_count,
        "reprojection_error_mean": row.reprojection_error_mean,
        "confidence": row.confidence,
        "display_label": "homography candidate",
        **_court_source_metadata(
            row,
            "homography candidate",
            evidence_source="homography_candidate",
        ),
    }


def build_annotation_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    selected_run_ids: set[str],
) -> tuple[list[dict[str, Any]], int]:
    annotations = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.media_id == media.id)
        .order_by(
            HumanAnnotation.timestamp_start_ms,
            HumanAnnotation.frame_start,
            HumanAnnotation.id,
        )
    ).all()

    items: list[dict[str, Any]] = []
    annotations_without_time_count = 0
    for annotation in annotations:
        target = (
            session.get(Observation, annotation.observation_id)
            if annotation.observation_id is not None
            else None
        )
        if selected_run_ids and (target is None or target.run_id not in selected_run_ids):
            continue

        frame_number = (
            annotation.frame_start
            if annotation.frame_start is not None
            else target.frame_start
            if target is not None
            else None
        )
        timestamp_ms = (
            annotation.timestamp_start_ms
            if annotation.timestamp_start_ms is not None
            else target.timestamp_start_ms
            if target is not None
            else None
        )
        if frame_number is None or timestamp_ms is None:
            annotations_without_time_count += 1
            continue

        items.append(
            {
                "item_type": "annotation",
                "annotation_id": annotation.id,
                "target_observation_id": annotation.observation_id,
                "target_observation_type": target.observation_type if target is not None else None,
                "target_run_id": target.run_id if target is not None else None,
                "timestamp_ms": timestamp_ms,
                "frame_number": frame_number,
                "annotation_label": _annotation_label(annotation),
                "created_by": annotation.created_by,
                "display_label": "review annotation",
            }
        )

    items.sort(key=lambda item: (item["timestamp_ms"], item["frame_number"], item["annotation_id"]))
    return items, annotations_without_time_count


def build_detection_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    detection_run_id: str | None = None,
    min_confidence: float | None = None,
) -> list[dict[str, Any]]:
    timestamp_end = func.coalesce(Observation.timestamp_end_ms, Observation.timestamp_start_ms)
    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.observation_family == "atomic",
            Observation.observation_type.in_(sorted(DETECTION_TYPES)),
            Observation.timestamp_start_ms.is_not(None),
            Observation.timestamp_start_ms <= end_ms,
            timestamp_end >= start_ms,
        )
        .order_by(Observation.timestamp_start_ms, Observation.observation_type, Observation.id)
    )
    if detection_run_id is not None:
        query = query.where(Observation.run_id == detection_run_id)
    if min_confidence is not None:
        query = query.where(
            Observation.confidence.is_not(None),
            Observation.confidence >= min_confidence,
        )

    items: list[dict[str, Any]] = []
    for observation in session.scalars(query).all():
        item = detection_overlay_item_from_observation(observation)
        if item is not None:
            items.append(item)
    return items


def detection_overlay_item_from_observation(
    observation: Observation,
) -> dict[str, Any] | None:
    if observation.observation_type not in DETECTION_TYPES:
        return None

    payload = _merged_detection_payload(observation)
    bbox = _bbox_from_payload(payload)
    frame_number = (
        observation.frame_start if observation.frame_start is not None else observation.frame_end
    )
    timestamp_ms = (
        observation.timestamp_start_ms
        if observation.timestamp_start_ms is not None
        else observation.timestamp_end_ms
    )
    if bbox is None or frame_number is None or timestamp_ms is None:
        return None

    source_metadata = _detection_source_metadata(observation, payload)
    return {
        "overlay_type": "detection_bbox",
        "observation_id": observation.id,
        "run_id": observation.run_id,
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "observation_type": observation.observation_type,
        "label": _detection_label(observation, payload),
        "confidence": observation.confidence,
        "bbox": bbox,
        "source_language": "detection observation",
        "source_runtime": _string_or_none(payload.get("source_runtime")),
        "coordinate_space": observation.coordinate_space or "image_pixels",
        "class_id": _optional_int(payload.get("class_id")),
        "class_label": _string_or_none(payload.get("class_label")),
        "frame_time_owner": _string_or_none(payload.get("frame_time_owner")),
        **source_metadata,
    }


def build_tracklet_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    tracklet_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Tracklet)
        .where(Tracklet.media_id == media.id)
        .order_by(Tracklet.frame_start, Tracklet.id)
    )
    if tracklet_run_id is not None:
        query = query.where(Tracklet.run_id == tracklet_run_id)

    items: list[dict[str, Any]] = []
    for tracklet in session.scalars(query).all():
        item = tracklet_overlay_item_from_row(media, tracklet)
        if item is None:
            continue
        if _time_ranges_overlap(
            item["timestamp_start_ms"],
            item["timestamp_end_ms"],
            start_ms,
            end_ms,
        ):
            items.append(item)
    return items


def tracklet_overlay_item_from_row(
    media: MediaAsset,
    tracklet: Tracklet,
) -> dict[str, Any] | None:
    points = []
    for point in tracklet.points:
        item = point_overlay_item_from_row(media, point)
        if item is not None:
            points.append(item)
    points.sort(
        key=lambda item: (item["timestamp_ms"], item["frame_number"], item["track_point_id"])
    )
    if not points:
        return None

    timestamps = [point["timestamp_ms"] for point in points]
    metadata = tracklet.metadata_jsonb or {}
    observation_id = _string_or_none(tracklet.observation_id)
    source_metadata = _tracklet_source_metadata(metadata)
    return {
        "overlay_type": "tracklet_candidate",
        "observation_id": observation_id,
        "tracklet_id": tracklet.id,
        "run_id": tracklet.run_id,
        "track_type": tracklet.track_family,
        "label_hint": _tracklet_label_hint(tracklet),
        "track_status": _string_or_none(metadata.get("track_status")) or "candidate",
        "identity_status": _string_or_none(metadata.get("identity_status")) or "unverified",
        "frame_start": tracklet.frame_start,
        "frame_end": tracklet.frame_end,
        "timestamp_start_ms": min(timestamps),
        "timestamp_end_ms": max(timestamps),
        "points": points,
        "source_language": "tracklet candidate",
        **source_metadata,
    }


def point_overlay_item_from_row(
    media: MediaAsset,
    point: TrackPoint,
) -> dict[str, Any] | None:
    frame_number = point.frame_number
    timestamp_ms = (
        point.timestamp_ms
        if point.timestamp_ms is not None
        else frame_to_replay_timestamp_ms(media, frame_number)
    )
    x = _numeric(point.x)
    y = _numeric(point.y)
    if frame_number is None or timestamp_ms is None or x is None or y is None:
        return None

    payload = point.payload_jsonb or {}
    bbox = _track_point_bbox(point, payload)
    return {
        "track_point_id": point.id,
        "observation_id": point.observation_id,
        "source_detection_observation_id": _string_or_none(
            payload.get("source_detection_observation_id")
        ),
        "source_detection_run_id": _string_or_none(payload.get("source_detection_run_id")),
        "source_detection_evidence_source": _string_or_none(
            payload.get("source_detection_evidence_source")
        ),
        "source_detection_source_label": _string_or_none(
            payload.get("source_detection_source_label")
        ),
        "source_detection_runtime": _string_or_none(payload.get("source_detection_runtime")),
        "source_detection_real_model_output": _truthy(
            payload.get("source_detection_real_model_output")
        )
        or _truthy(payload.get("source_detection_is_real_model_output")),
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "x": x,
        "y": y,
        "bbox": bbox,
        "confidence": point.confidence,
    }


def build_pose_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    pose_run_id: str | None = None,
    min_pose_confidence: float | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(PoseObservation)
        .where(
            PoseObservation.media_id == media.id,
            PoseObservation.timestamp_ms.is_not(None),
            PoseObservation.timestamp_ms >= start_ms,
            PoseObservation.timestamp_ms <= end_ms,
        )
        .order_by(PoseObservation.timestamp_ms, PoseObservation.observation_id)
    )
    if pose_run_id is not None:
        query = query.where(PoseObservation.run_id == pose_run_id)
    if min_pose_confidence is not None:
        query = query.where(
            PoseObservation.pose_confidence.is_not(None),
            PoseObservation.pose_confidence >= min_pose_confidence,
        )

    return [pose_overlay_item_from_row(pose) for pose in session.scalars(query).all()]


def pose_overlay_item_from_row(pose: PoseObservation) -> dict[str, Any]:
    keypoints = _pose_overlay_keypoints(pose.keypoints_jsonb or [])
    source_metadata = _pose_source_metadata(pose)
    return {
        "overlay_type": "pose_skeleton",
        "observation_id": pose.observation_id,
        "run_id": pose.run_id,
        "frame_number": pose.frame_number,
        "timestamp_ms": pose.timestamp_ms,
        "skeleton_format": pose.skeleton_format,
        "skeleton_version": pose.skeleton_version,
        "pose_confidence": pose.pose_confidence,
        "bbox": _pose_bbox(pose),
        "keypoint_count": pose.keypoint_count,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "mean_keypoint_confidence": pose.mean_keypoint_confidence,
        "min_keypoint_confidence": pose.min_keypoint_confidence,
        "max_keypoint_confidence": pose.max_keypoint_confidence,
        "keypoints": keypoints,
        "edges": [list(edge) for edge in _pose_edges(pose)],
        "subject_context": {
            "subject_ref_type": pose.subject_ref_type,
            "subject_detection_observation_id": pose.subject_detection_observation_id,
            "subject_tracklet_id": pose.subject_tracklet_id,
            "subject_track_point_id": pose.subject_track_point_id,
            "association_status": pose.association_status,
            "association_method": pose.association_method,
            "association_confidence": pose.association_confidence,
        },
        "source_language": "pose keypoint evidence",
        **source_metadata,
    }


def build_court_keypoint_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(CourtKeypointObservation)
        .where(
            CourtKeypointObservation.media_id == media.id,
            CourtKeypointObservation.timestamp_ms >= start_ms,
            CourtKeypointObservation.timestamp_ms <= end_ms,
        )
        .order_by(CourtKeypointObservation.timestamp_ms, CourtKeypointObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CourtKeypointObservation.run_id == court_run_id)
    return [court_keypoint_overlay_item_from_row(row) for row in session.scalars(query).all()]


def court_keypoint_overlay_item_from_row(row: CourtKeypointObservation) -> dict[str, Any]:
    return {
        "overlay_type": "court_keypoint_evidence",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "coordinate_space": row.coordinate_space,
        "court_keypoint_schema": row.court_keypoint_schema,
        "schema_version": row.schema_version,
        "keypoints": _court_keypoints(row.keypoints_jsonb or []),
        "keypoint_count": row.keypoint_count,
        "keypoints_present_count": row.keypoints_present_count,
        "keypoints_missing_count": row.keypoints_missing_count,
        "mean_keypoint_confidence": row.mean_keypoint_confidence,
        "min_keypoint_confidence": row.min_keypoint_confidence,
        "max_keypoint_confidence": row.max_keypoint_confidence,
        "frame_time_owner": row.frame_time_owner,
        **_court_source_metadata(row, "court keypoint evidence"),
    }


def build_court_line_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(CourtLineObservation)
        .where(
            CourtLineObservation.media_id == media.id,
            CourtLineObservation.timestamp_ms >= start_ms,
            CourtLineObservation.timestamp_ms <= end_ms,
        )
        .order_by(CourtLineObservation.timestamp_ms, CourtLineObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CourtLineObservation.run_id == court_run_id)
    return [court_line_overlay_item_from_row(row) for row in session.scalars(query).all()]


def court_line_overlay_item_from_row(row: CourtLineObservation) -> dict[str, Any]:
    return {
        "overlay_type": "court_line_evidence",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "coordinate_space": row.coordinate_space,
        "line_segments": _court_line_segments(row.line_segments_jsonb or []),
        "line_classes": row.line_classes_jsonb,
        "line_count": row.line_count,
        "mean_line_confidence": row.mean_line_confidence,
        "frame_time_owner": row.frame_time_owner,
        **_court_source_metadata(row, "court line evidence"),
    }


def build_camera_view_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    court_run_id: str | None = None,
) -> list[dict[str, Any]]:
    timestamp_start = func.coalesce(
        CameraViewObservation.timestamp_start_ms,
        CameraViewObservation.timestamp_ms,
    )
    timestamp_end = func.coalesce(
        CameraViewObservation.timestamp_end_ms,
        CameraViewObservation.timestamp_ms,
    )
    query = (
        select(CameraViewObservation)
        .where(
            CameraViewObservation.media_id == media.id,
            timestamp_start <= end_ms,
            timestamp_end >= start_ms,
        )
        .order_by(CameraViewObservation.timestamp_ms, CameraViewObservation.observation_id)
    )
    if court_run_id is not None:
        query = query.where(CameraViewObservation.run_id == court_run_id)
    return [camera_view_overlay_item_from_row(row) for row in session.scalars(query).all()]


def camera_view_overlay_item_from_row(row: CameraViewObservation) -> dict[str, Any]:
    return {
        "overlay_type": "camera_view_evidence",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "frame_start": row.frame_start,
        "frame_end": row.frame_end,
        "timestamp_start_ms": row.timestamp_start_ms,
        "timestamp_end_ms": row.timestamp_end_ms,
        "view_label": row.view_label,
        "view_confidence": row.view_confidence,
        "camera_motion_hint": row.camera_motion_hint,
        "stability_score": row.stability_score,
        "cut_likelihood": row.cut_likelihood,
        "frame_time_owner": row.frame_time_owner,
        **_court_source_metadata(row, "camera/view evidence"),
    }


def build_homography_candidate_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    homography_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(HomographyCandidateObservation)
        .where(
            HomographyCandidateObservation.media_id == media.id,
            HomographyCandidateObservation.timestamp_ms >= start_ms,
            HomographyCandidateObservation.timestamp_ms <= end_ms,
        )
        .order_by(
            HomographyCandidateObservation.timestamp_ms,
            HomographyCandidateObservation.observation_id,
        )
    )
    if homography_run_id is not None:
        query = query.where(HomographyCandidateObservation.run_id == homography_run_id)
    return [
        homography_candidate_overlay_item_from_row(row) for row in session.scalars(query).all()
    ]


def homography_candidate_overlay_item_from_row(
    row: HomographyCandidateObservation,
) -> dict[str, Any]:
    return {
        "overlay_type": "homography_candidate",
        "observation_id": row.observation_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "source_court_keypoint_observation_id": row.source_court_keypoint_observation_id,
        "source_court_line_observation_id": row.source_court_line_observation_id,
        "source_camera_view_observation_id": row.source_camera_view_observation_id,
        "homography_matrix": row.homography_matrix_jsonb,
        "inverse_homography_matrix": row.inverse_homography_matrix_jsonb,
        "matrix_direction": row.matrix_direction,
        "template_name": row.template_name,
        "template_version": row.template_version,
        "template": _court_template_payload(row.template_name, row.template_version),
        "reprojection_error_mean": row.reprojection_error_mean,
        "reprojection_error_median": row.reprojection_error_median,
        "reprojection_error_max": row.reprojection_error_max,
        "inlier_count": row.inlier_count,
        "outlier_count": row.outlier_count,
        "source_point_count": row.source_point_count,
        "source_line_count": row.source_line_count,
        "confidence": row.confidence,
        "status": row.status,
        "frame_time_owner": row.frame_time_owner,
        **_court_source_metadata(
            row,
            "homography candidate",
            evidence_source="homography_candidate",
        ),
    }


def available_runs_for_media(session: Session, media_id: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "detection": _run_summaries_for_observation_types(session, media_id, DETECTION_TYPES),
        "tracklet": _run_summaries_for_observation_types(session, media_id, TRACKLET_TYPES),
        "pose": _run_summaries_for_observation_types(session, media_id, POSE_TYPES),
        "gameplay": _run_summaries_for_observation_types(session, media_id, GAMEPLAY_TYPES),
        "court": _court_run_summaries(session, media_id),
        "homography": _homography_run_summaries(session, media_id),
    }


def normalize_replay_layers(layers: str | list[str] | tuple[str, ...] | None) -> set[str]:
    if layers is None:
        return {"detections"}
    if isinstance(layers, str):
        raw_layers = layers.split(",")
    else:
        raw_layers = [part for layer in layers for part in str(layer).split(",")]
    normalized: set[str] = set()
    for raw_layer in raw_layers:
        layer = raw_layer.strip().lower()
        if not layer:
            continue
        if layer == "poses":
            layer = "pose"
        if layer == "tracklet":
            layer = "tracklets"
        if layer in {"court", "court_evidence"}:
            normalized.update(
                {
                    "court_keypoints",
                    "court_lines",
                    "camera_view",
                    "homography_candidates",
                }
            )
            continue
        if layer in {"court_keypoint", "court-keypoints"}:
            layer = "court_keypoints"
        if layer in {"court_line", "court-lines"}:
            layer = "court_lines"
        if layer in {"camera", "camera-view", "camera_views"}:
            layer = "camera_view"
        if layer in {"homography", "homographies", "homography-candidates"}:
            layer = "homography_candidates"
        normalized.add(layer)
    return normalized


def resolve_media_video_path(media: MediaAsset) -> Path | None:
    metadata = media.metadata_jsonb or {}
    candidates = [
        metadata.get("stored_uri"),
        metadata.get("stored_path"),
        media.source_uri,
        metadata.get("original_source_uri"),
        metadata.get("original_source_path"),
    ]
    for candidate in candidates:
        if not isinstance(candidate, str) or not candidate.strip():
            continue
        try:
            path = local_path_from_uri_or_path(candidate)
        except ValueError:
            continue
        if path.is_file():
            return path
    return None


def _court_run_summaries(session: Session, media_id: str) -> list[dict[str, Any]]:
    summaries = _run_summaries_for_observation_types(session, media_id, COURT_EVIDENCE_TYPES)
    if not summaries:
        return []

    counts_by_run_type = _counts_by_run_and_type(session, media_id, COURT_EVIDENCE_TYPES)
    for summary in summaries:
        run_id = summary["run_id"]
        summary.update(
            {
                "evidence_source": "fixture_court_evidence"
                if summary.get("is_fixture")
                else "court_evidence",
                "source_label": "fixture court evidence"
                if summary.get("is_fixture")
                else "court evidence",
                "court_keypoint_count": counts_by_run_type.get(
                    (run_id, "court_keypoint_observation"), 0
                ),
                "court_line_count": counts_by_run_type.get(
                    (run_id, "court_line_observation"), 0
                ),
                "camera_view_count": counts_by_run_type.get(
                    (run_id, "camera_view_observation"), 0
                ),
                "geometry_evidence_only": True,
                "is_real_model_output": False,
                "model_output_not_truth": False,
            }
        )
    return summaries


def _homography_run_summaries(session: Session, media_id: str) -> list[dict[str, Any]]:
    summaries = _run_summaries_for_observation_types(session, media_id, HOMOGRAPHY_TYPES)
    if not summaries:
        return []

    candidate_counts = _counts_by_run_and_type(session, media_id, HOMOGRAPHY_TYPES)
    for summary in summaries:
        run = session.get(ProcessingRun, summary["run_id"])
        runtime_payload = run.runtime_config.payload_jsonb if run and run.runtime_config else {}
        run_metadata = run.metadata_jsonb if run is not None else {}
        source_court_run_id = (
            _string_or_none(run_metadata.get("source_court_run_id"))
            or _string_or_none(runtime_payload.get("source_court_run_id"))
        )
        summary.update(
            {
                "evidence_source": "homography_candidate",
                "source_label": "homography candidate",
                "candidate_count": candidate_counts.get(
                    (summary["run_id"], "homography_candidate_observation"), 0
                ),
                "source_court_run_id": source_court_run_id,
                "candidate_geometry": True,
                "geometry_evidence_only": True,
                "is_fixture": False,
                "is_real_model_output": False,
                "model_output_not_truth": False,
            }
        )
    return summaries


def _counts_by_run_and_type(
    session: Session,
    media_id: str,
    observation_types: set[str],
) -> dict[tuple[str, str], int]:
    return {
        (run_id, observation_type): int(count)
        for run_id, observation_type, count in session.execute(
            select(Observation.run_id, Observation.observation_type, func.count())
            .where(
                Observation.media_id == media_id,
                Observation.observation_type.in_(sorted(observation_types)),
            )
            .group_by(Observation.run_id, Observation.observation_type)
        ).all()
    }


def _run_summaries_for_observation_types(
    session: Session,
    media_id: str,
    observation_types: set[str],
) -> list[dict[str, Any]]:
    counts = dict(
        session.execute(
            select(Observation.run_id, func.count())
            .where(
                Observation.media_id == media_id,
                Observation.observation_type.in_(sorted(observation_types)),
            )
            .group_by(Observation.run_id)
        ).all()
    )
    if not counts:
        return []

    runs = session.scalars(
        select(ProcessingRun)
        .where(ProcessingRun.id.in_(list(counts.keys())))
        .order_by(ProcessingRun.started_at, ProcessingRun.id)
    ).all()
    summaries: list[dict[str, Any]] = []
    for run in runs:
        source_metadata = _run_source_metadata(
            session=session,
            run=run,
            media_id=media_id,
            observation_types=observation_types,
        )
        summaries.append(
            {
                "run_id": run.id,
                "run_name": run.run_name,
                "run_status": run.run_status,
                "created_at": run.started_at.isoformat() if run.started_at else None,
                "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                "observation_count": int(counts.get(run.id, 0)),
                "runtime_config_id": run.runtime_config_id,
                **source_metadata,
            }
        )
    return summaries


def _merged_detection_payload(observation: Observation) -> dict[str, Any]:
    atomic = observation.atomic_detail
    return {
        **(observation.payload_jsonb or {}),
        **(atomic.payload_jsonb if isinstance(atomic, AtomicObservation) else {}),
    }


def _run_source_metadata(
    session: Session,
    run: ProcessingRun,
    media_id: str,
    observation_types: set[str],
) -> dict[str, Any]:
    observation = session.scalar(
        select(Observation)
        .where(
            Observation.media_id == media_id,
            Observation.run_id == run.id,
            Observation.observation_type.in_(sorted(observation_types)),
        )
        .order_by(Observation.created_at, Observation.id)
        .limit(1)
    )
    payload = _merged_detection_payload(observation) if observation is not None else {}
    runtime_payload = run.runtime_config.payload_jsonb if run.runtime_config is not None else {}
    run_metadata = run.metadata_jsonb or {}
    diagnostics = (run.metadata_jsonb or {}).get("diagnostics")
    if not isinstance(diagnostics, dict):
        diagnostics = {}

    tracklet_source_metadata = (
        _tracklet_run_source_metadata(
            run_metadata=run_metadata,
            runtime_payload=runtime_payload,
            payload=payload,
        )
        if observation_types == TRACKLET_TYPES
        else None
    )
    if tracklet_source_metadata is not None:
        model = (
            session.get(ModelRegistry, observation.model_id)
            if observation and observation.model_id
            else None
        )
        return {
            **tracklet_source_metadata,
            "adapter_name": None,
            "source_runtime": tracklet_source_metadata["source_detection_runtime"],
            "model_name": model.name if model is not None else None,
            "model_version": model.version if model is not None else None,
            "model_registry_id": model.id if model is not None else None,
            "is_real_model_output": False,
            "model_output_not_truth": False,
        }

    model = (
        session.get(ModelRegistry, observation.model_id)
        if observation and observation.model_id
        else None
    )
    source_runtime = (
        _string_or_none(payload.get("source_runtime"))
        or _string_or_none(diagnostics.get("source_runtime"))
        or _string_or_none(runtime_payload.get("source_runtime"))
    )
    adapter_name = (
        _string_or_none(runtime_payload.get("adapter"))
        or _string_or_none((run.metadata_jsonb or {}).get("adapter_name"))
    )
    is_real_model_output = _truthy(payload.get("real_model_output")) or (
        source_runtime == "ultralytics_yolo" and adapter_name in {"yolo", "ultralytics"}
    ) or (
        source_runtime == "ultralytics_pose"
    )
    is_fixture = (
        _string_or_none(runtime_payload.get("adapter")) == "fixture"
        or source_runtime == "fixture"
        or source_runtime == "fixture_pose"
        or "fixture" in run.run_name.lower()
        or "fixture" in (adapter_name or "").lower()
    )
    explicit_evidence_source = _string_or_none(payload.get("evidence_source"))
    evidence_source = (
        "real_pose_model_output"
        if explicit_evidence_source == "real_pose_model_output"
        or source_runtime == "ultralytics_pose"
        else explicit_evidence_source
        if explicit_evidence_source
        else
        "real_model_output"
        if is_real_model_output
        else "fixture_demo"
        if is_fixture
        else "persisted_evidence"
    )
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "adapter_name": adapter_name,
        "source_runtime": source_runtime,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "model_registry_id": model.id if model is not None else None,
        "is_fixture": is_fixture,
        "is_real_model_output": is_real_model_output,
        "model_output_not_truth": is_real_model_output,
    }


def _detection_source_metadata(
    observation: Observation,
    payload: dict[str, Any],
) -> dict[str, Any]:
    source_runtime = _string_or_none(payload.get("source_runtime"))
    is_real_model_output = _truthy(payload.get("real_model_output")) or (
        source_runtime == "ultralytics_yolo"
    )
    adapter_name = _string_or_none(payload.get("adapter_name")) or ""
    is_fixture = (
        source_runtime == "fixture"
        or _string_or_none(payload.get("adapter_type")) == "fixture"
        or "fixture" in adapter_name.lower()
    )
    evidence_source = (
        "real_model_output"
        if is_real_model_output
        else "fixture_demo"
        if is_fixture
        else "persisted_evidence"
    )
    model = observation.model
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "real_model_output": is_real_model_output,
        "model_output_not_truth": is_real_model_output,
        "model_registry_id": observation.model_id,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "runtime_config_id": observation.runtime_config_id,
        "is_fixture": is_fixture,
        "is_real_model_output": is_real_model_output,
    }


def _pose_source_metadata(pose: PoseObservation) -> dict[str, Any]:
    observation = pose.observation
    payload = observation.payload_jsonb if observation is not None else {}
    metadata = pose.metadata_jsonb or {}
    source_runtime = (
        _string_or_none(payload.get("source_runtime"))
        or _string_or_none(metadata.get("source_runtime"))
    )
    evidence_source = (
        _string_or_none(payload.get("evidence_source"))
        or _string_or_none(metadata.get("evidence_source"))
    )
    is_real_model_output = (
        evidence_source == "real_pose_model_output"
        or source_runtime == "ultralytics_pose"
        or _truthy(payload.get("real_model_output"))
        or _truthy(metadata.get("real_model_output"))
    )
    is_fixture = (
        source_runtime == "fixture_pose"
        or _truthy(metadata.get("no_real_pose_inference"))
        or evidence_source == "fixture_demo"
    )
    if evidence_source is None:
        evidence_source = (
            "real_pose_model_output"
            if is_real_model_output
            else "fixture_demo"
            if is_fixture
            else "persisted_evidence"
        )
    model = observation.model if observation is not None else None
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "source_runtime": source_runtime,
        "real_model_output": is_real_model_output,
        "model_output_not_truth": is_real_model_output,
        "model_registry_id": observation.model_id if observation is not None else None,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "runtime_config_id": observation.runtime_config_id if observation is not None else None,
        "is_fixture": is_fixture,
        "is_real_model_output": is_real_model_output,
    }


def _court_source_metadata(
    row: (
        CourtKeypointObservation
        | CourtLineObservation
        | CameraViewObservation
        | HomographyCandidateObservation
    ),
    source_label: str,
    *,
    evidence_source: str | None = None,
) -> dict[str, Any]:
    observation = row.observation
    payload = observation.payload_jsonb if observation is not None else {}
    metadata = row.metadata_jsonb or {}
    model = row.model if hasattr(row, "model") else None
    if model is None and observation is not None:
        model = observation.model

    fixture_court_evidence = _truthy(metadata.get("fixture_court_evidence")) or _truthy(
        payload.get("fixture_court_evidence")
    )
    fixture_camera_view_evidence = _truthy(
        metadata.get("fixture_camera_view_evidence")
    ) or _truthy(payload.get("fixture_camera_view_evidence"))
    candidate_geometry = _truthy(metadata.get("candidate_geometry")) or _truthy(
        payload.get("candidate_geometry")
    )
    geometry_evidence_only = (
        _truthy(metadata.get("geometry_evidence_only"))
        or _truthy(payload.get("geometry_evidence_only"))
        or True
    )
    resolved_evidence_source = evidence_source
    if resolved_evidence_source is None:
        if candidate_geometry:
            resolved_evidence_source = "homography_candidate"
        elif fixture_court_evidence:
            resolved_evidence_source = "fixture_court_evidence"
        elif fixture_camera_view_evidence:
            resolved_evidence_source = "fixture_camera_view_evidence"
        else:
            resolved_evidence_source = "court_evidence"

    return {
        "evidence_source": resolved_evidence_source,
        "source_label": source_label,
        "source_runtime": _string_or_none(payload.get("source_runtime"))
        or _string_or_none(metadata.get("source_runtime")),
        "model_registry_id": row.model_id,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "runtime_config_id": row.runtime_config_id,
        "fixture_court_evidence": fixture_court_evidence,
        "fixture_camera_view_evidence": fixture_camera_view_evidence,
        "candidate_geometry": candidate_geometry,
        "geometry_evidence_only": geometry_evidence_only,
        "observation_only": True,
        "no_adjudication": True,
        "is_fixture": fixture_court_evidence or fixture_camera_view_evidence,
        "is_real_model_output": False,
        "model_output_not_truth": False,
    }


def _tracklet_run_source_metadata(
    *,
    run_metadata: dict[str, Any],
    runtime_payload: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    source_detection_run_id = (
        _string_or_none(payload.get("source_detection_run_id"))
        or _string_or_none(run_metadata.get("source_detection_run_id"))
        or _string_or_none(runtime_payload.get("source_detection_run_id"))
    )
    if source_detection_run_id is None:
        return None

    source_detection_evidence_source = (
        _string_or_none(payload.get("source_detection_evidence_source"))
        or _string_or_none(run_metadata.get("source_detection_evidence_source"))
        or _string_or_none(runtime_payload.get("source_detection_evidence_source"))
        or "persisted_evidence"
    )
    is_real_detection_derived = (
        source_detection_evidence_source == "real_model_output"
        or _truthy(payload.get("source_detection_real_model_output"))
        or _truthy(run_metadata.get("source_detection_real_model_output"))
        or _truthy(runtime_payload.get("source_detection_real_model_output"))
        or _truthy(payload.get("source_detection_is_real_model_output"))
        or _truthy(run_metadata.get("source_detection_is_real_model_output"))
        or _truthy(runtime_payload.get("source_detection_is_real_model_output"))
    )
    is_fixture = source_detection_evidence_source == "fixture_demo" or _truthy(
        payload.get("source_detection_is_fixture")
    )
    evidence_source = (
        "real_detection_derived_tracklet"
        if is_real_detection_derived
        else "fixture_derived_tracklet"
        if is_fixture
        else "persisted_tracklet"
    )
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "source_detection_run_id": source_detection_run_id,
        "source_detection_evidence_source": source_detection_evidence_source,
        "source_detection_source_label": _source_label(source_detection_evidence_source),
        "source_detection_runtime": (
            _string_or_none(payload.get("source_detection_runtime"))
            or _string_or_none(run_metadata.get("source_detection_runtime"))
            or _string_or_none(runtime_payload.get("source_detection_runtime"))
        ),
        "is_fixture": is_fixture,
        "is_real_detection_derived": is_real_detection_derived,
    }


def _tracklet_source_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    source_detection_evidence_source = (
        _string_or_none(metadata.get("source_detection_evidence_source"))
        or "persisted_evidence"
    )
    is_real_detection_derived = (
        source_detection_evidence_source == "real_model_output"
        or _truthy(metadata.get("source_detection_real_model_output"))
        or _truthy(metadata.get("source_detection_is_real_model_output"))
        or _truthy(metadata.get("is_real_detection_derived"))
    )
    return {
        "source_detection_run_id": _string_or_none(metadata.get("source_detection_run_id")),
        "source_detection_evidence_source": source_detection_evidence_source,
        "source_detection_source_label": _source_label(source_detection_evidence_source),
        "source_detection_runtime": _string_or_none(metadata.get("source_detection_runtime")),
        "source_detection_real_model_output": is_real_detection_derived,
        "is_real_detection_derived": is_real_detection_derived,
        "candidate_evidence_only": bool(metadata.get("candidate_evidence_only", True)),
    }


def _source_label(evidence_source: str) -> str:
    if evidence_source == "real_pose_model_output":
        return "real pose model output"
    if evidence_source == "real_model_output":
        return "real model output"
    if evidence_source == "fixture_demo":
        return "fixture evidence"
    if evidence_source == "real_detection_derived_tracklet":
        return "real-detection-derived tracklet candidates"
    if evidence_source == "fixture_derived_tracklet":
        return "fixture-derived tracklet candidates"
    if evidence_source == "persisted_tracklet":
        return "persisted tracklet candidates"
    if evidence_source == "fixture_court_evidence":
        return "fixture court evidence"
    if evidence_source == "fixture_camera_view_evidence":
        return "fixture camera/view evidence"
    if evidence_source == "court_evidence":
        return "court evidence"
    if evidence_source == "homography_candidate":
        return "homography candidate"
    return "persisted evidence"


def _display_label(base_label: str, source_metadata: dict[str, Any]) -> str:
    source_label = source_metadata.get("source_label")
    return f"{base_label} · {source_label}" if source_label else base_label


def _pose_display_label(source_metadata: dict[str, Any]) -> str:
    if source_metadata.get("evidence_source") == "real_pose_model_output":
        return _display_label("pose observation", source_metadata)
    return "pose observation"


def _bbox_from_payload(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if isinstance(value, dict):
        x = _numeric(value.get("x"))
        y = _numeric(value.get("y"))
        width = _numeric(value.get("width", value.get("w")))
        height = _numeric(value.get("height", value.get("h")))
    elif isinstance(value, list | tuple) and len(value) == 4:
        x = _numeric(value[0])
        y = _numeric(value[1])
        width = _numeric(value[2])
        height = _numeric(value[3])
    else:
        return None

    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "w": width, "h": height}


def _track_point_bbox(point: TrackPoint, payload: dict[str, Any]) -> dict[str, float] | None:
    payload_bbox = _bbox_from_payload(payload)
    if payload_bbox is not None:
        return payload_bbox

    width = _numeric(point.width)
    height = _numeric(point.height)
    x = _numeric(point.x)
    y = _numeric(point.y)
    if width is None or height is None or x is None or y is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {
        "x": x - width / 2.0,
        "y": y - height / 2.0,
        "w": width,
        "h": height,
    }


def _tracklet_label_hint(tracklet: Tracklet) -> str | None:
    if tracklet.subject_ref:
        return tracklet.subject_ref
    if tracklet.track_family == "ball":
        return "ball"
    if tracklet.track_family == "player":
        return "player_unknown"
    return None


def _pose_bbox(pose: PoseObservation) -> dict[str, float | None] | None:
    x = _numeric(pose.bbox_x)
    y = _numeric(pose.bbox_y)
    width = _numeric(pose.bbox_w)
    height = _numeric(pose.bbox_h)
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {
        "x": x,
        "y": y,
        "w": width,
        "h": height,
        "confidence": pose.bbox_confidence,
    }


def _pose_overlay_keypoints(keypoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for keypoint in keypoints:
        if not isinstance(keypoint, dict):
            continue
        normalized.append(
            {
                "index": keypoint.get("index"),
                "name": keypoint.get("name"),
                "x": keypoint.get("x"),
                "y": keypoint.get("y"),
                "confidence": keypoint.get("confidence"),
                "present": bool(keypoint.get("present")),
            }
        )
    return normalized


def _court_keypoints(keypoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for keypoint in keypoints:
        if not isinstance(keypoint, dict):
            continue
        normalized.append(
            {
                "name": keypoint.get("name"),
                "x": keypoint.get("x"),
                "y": keypoint.get("y"),
                "confidence": keypoint.get("confidence"),
                "present": bool(keypoint.get("present")),
                "visibility": keypoint.get("visibility"),
                "source_index": keypoint.get("source_index"),
            }
        )
    return normalized


def _court_line_segments(line_segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for segment in line_segments:
        if not isinstance(segment, dict):
            continue
        normalized.append(
            {
                "line_class": segment.get("line_class"),
                "x1": segment.get("x1"),
                "y1": segment.get("y1"),
                "x2": segment.get("x2"),
                "y2": segment.get("y2"),
                "confidence": segment.get("confidence"),
                "visibility": segment.get("visibility"),
            }
        )
    return normalized


def _court_template_payload(template_name: str, template_version: str) -> dict[str, Any] | None:
    try:
        template = get_court_template(template_name, template_version)
    except ValueError:
        return None
    return {
        "template_name": template.template_name,
        "template_version": template.template_version,
        "target_coordinate_space": template.target_coordinate_space,
        "keypoints": [keypoint.model_dump(mode="json") for keypoint in template.keypoints],
        "lines": [line.model_dump(mode="json") for line in template.lines],
    }


def _pose_edges(pose: PoseObservation) -> list[tuple[str, str]]:
    try:
        return list(get_skeleton_definition(pose.skeleton_format, pose.skeleton_version).edges)
    except ValueError:
        return []


def _time_ranges_overlap(
    start_a: int | float | None,
    end_a: int | float | None,
    start_b: int,
    end_b: int,
) -> bool:
    if start_a is None or end_a is None:
        return False
    return float(start_a) <= end_b and float(end_a) >= start_b


def _observation_frame_time(observation: Observation) -> tuple[int | None, int | None]:
    frame_number = (
        observation.frame_start if observation.frame_start is not None else observation.frame_end
    )
    timestamp_ms = (
        observation.timestamp_start_ms
        if observation.timestamp_start_ms is not None
        else observation.timestamp_end_ms
    )
    return frame_number, timestamp_ms


def _detection_label(observation: Observation, payload: dict[str, Any]) -> str:
    for key in ("label", "class_label"):
        value = _string_or_none(payload.get(key))
        if value is not None:
            return value

    detector = payload.get("detector")
    if isinstance(detector, dict):
        detector_label = _string_or_none(detector.get("label"))
        if detector_label is not None:
            return detector_label

    return observation.observation_type.replace("_detection", "")


def _annotation_label(annotation: HumanAnnotation) -> str:
    payload = annotation.payload_jsonb or {}
    label = _string_or_none(payload.get("annotation_label"))
    return label if label is not None else annotation.annotation_type


def _numeric(value: Any) -> float | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _truthy(value: Any) -> bool:
    return value is True or value == "true" or value == 1


def _positive_float(value: float | None) -> float | None:
    if value is None or value <= 0:
        return None
    return float(value)


def _positive_int(value: int | None) -> int | None:
    if value is None or value <= 0:
        return None
    return int(value)


def _clamp_frame(frame: int, frame_count: int) -> int:
    return max(0, min(frame, frame_count - 1))
