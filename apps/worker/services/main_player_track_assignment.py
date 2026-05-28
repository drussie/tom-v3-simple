from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import mean
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.worker.services.main_subject_filter import MAIN_SUBJECT_OBSERVATION_TYPE

MAIN_PLAYER_TRACK_OBSERVATION_TYPE = "main_player_track_candidate"
MAIN_PLAYER_TRACK_ASSIGNMENT_OBSERVATION_TYPE = "main_player_track_assignment_candidate"
MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD = "main_player_track_assignment_v0"
MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS = {
    "candidate_track_only": True,
    "candidate_subject_only": True,
    "not_identity_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "raw_detections_not_mutated": True,
}

SUBJECT_ROLE_TO_TRACK_ROLE = {
    "near_player_candidate": "near_player_track_candidate",
    "far_player_candidate": "far_player_track_candidate",
}


class MainPlayerTrackAssignmentError(ValueError):
    pass


@dataclass(frozen=True)
class MainPlayerTrackAssignmentConfig:
    min_assignment_score: float = 0.25
    max_center_jump_norm: float = 0.35
    max_area_ratio_change: float = 3.0

    def as_dict(self) -> dict[str, float]:
        return {
            "min_assignment_score": self.min_assignment_score,
            "max_center_jump_norm": self.max_center_jump_norm,
            "max_area_ratio_change": self.max_area_ratio_change,
        }


@dataclass(frozen=True)
class SubjectCandidateInput:
    observation: Observation
    detection: Observation
    role: str
    track_role: str
    bbox: dict[str, float]
    selection_score: float
    timestamp_ms: int


@dataclass(frozen=True)
class TrackAssignmentCandidate:
    subject: SubjectCandidateInput
    track_candidate_id: str
    assignment_score: float
    continuity_score: float
    center_distance_norm: float | None
    area_change_ratio: float | None


def build_main_player_track_assignment_plan(
    *,
    media_id: str = "<media_id>",
    source_detection_run_id: str = "<source_detection_run_id>",
    source_subject_run_id: str = "<source_subject_run_id>",
    run_name: str = "main-player-track-assignment-v0",
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    viewer_base_url: str = "http://127.0.0.1:3000",
    config: MainPlayerTrackAssignmentConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MainPlayerTrackAssignmentConfig()
    command_parts = [
        "python -m apps.worker.cli assign-main-player-tracks",
        f"--media-id {media_id}",
        f"--source-detection-run-id {source_detection_run_id}",
        f"--source-subject-run-id {source_subject_run_id}",
        f"--run-name {run_name}",
        f"--every-n-frames {every_n_frames}",
    ]
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")
    if max_frames is not None:
        command_parts.append(f"--max-frames {max_frames}")

    return {
        "steps": [
            "validate_media",
            "validate_source_detection_run",
            "validate_source_subject_run",
            "query_main_subject_candidates",
            "assign_near_and_far_track_candidates",
            "persist_main_player_track_candidate_observations",
            "persist_main_player_track_assignment_candidate_observations",
            "write_subject_detection_and_track_lineage",
        ],
        "command": " ".join(command_parts),
        "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
        "source_detection_run_id": source_detection_run_id,
        "source_subject_run_id": source_subject_run_id,
        "run_name": run_name,
        "sampling": {
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "frame_time_owner": "media_indexing",
        },
        "assignment_config": resolved_config.as_dict(),
        "replay_url_template": (
            f"{viewer_base_url}/replay/{media_id}?"
            "detectionRunId=<source_detection_run_id>"
            "&subjectRunId=<source_subject_run_id>"
            "&mainPlayerTrackRunId=<main_player_track_run_id>"
        ),
        "warnings": dict(MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS),
    }


def assign_main_player_tracks(
    *,
    session: Session,
    media_id: str,
    source_detection_run_id: str,
    source_subject_run_id: str,
    run_name: str = "main-player-track-assignment-v0",
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
    config: MainPlayerTrackAssignmentConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MainPlayerTrackAssignmentConfig()
    plan = build_main_player_track_assignment_plan(
        media_id=media_id,
        source_detection_run_id=source_detection_run_id,
        source_subject_run_id=source_subject_run_id,
        run_name=run_name,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        viewer_base_url=viewer_base_url,
        config=resolved_config,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "main player track assignment planned",
            "plan": plan,
            "warnings": dict(MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    source_detection_run = session.get(ProcessingRun, source_detection_run_id)
    if source_detection_run is None:
        return _failed(
            "missing_source_detection_run",
            f"source detection run not found: {source_detection_run_id}",
        )
    if source_detection_run.media_id != media.id:
        return _failed(
            "source_detection_run_media_mismatch",
            "source detection run media_id does not match media_id.",
        )

    source_subject_run = session.get(ProcessingRun, source_subject_run_id)
    if source_subject_run is None:
        return _failed(
            "missing_source_subject_run",
            f"source subject run not found: {source_subject_run_id}",
        )
    if source_subject_run.media_id != media.id:
        return _failed(
            "source_subject_run_media_mismatch",
            "source subject run media_id does not match media_id.",
        )

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            source_detection_run_id=source_detection_run_id,
            source_subject_run_id=source_subject_run_id,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
            config=resolved_config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            source_detection_run_id=source_detection_run_id,
            source_subject_run_id=source_subject_run_id,
            config=resolved_config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        subject_inputs = _source_subject_candidates(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
            source_subject_run_id=source_subject_run_id,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
        )
        assignments_by_role = _assign_tracks_by_role(
            media=media,
            subject_inputs=subject_inputs,
            config=resolved_config,
        )
        track_observations = _persist_track_candidates(
            session=session,
            media=media,
            run=run,
            model=model,
            runtime_config=runtime_config,
            source_detection_run_id=source_detection_run_id,
            source_subject_run_id=source_subject_run_id,
            assignments_by_role=assignments_by_role,
        )
        assignment_observations = _persist_track_assignments(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            track_observations=track_observations,
            assignments_by_role=assignments_by_role,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session, run, step, str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    role_counts = Counter(
        str(observation.payload_jsonb.get("track_role_candidate"))
        for observation in track_observations.values()
    )
    assignment_role_counts = Counter(
        str(observation.payload_jsonb.get("track_role_candidate"))
        for observation in assignment_observations
    )
    sampled_frames = sorted(
        {
            int(observation.frame_start)
            for observation in assignment_observations
            if observation.frame_start is not None
        }
    )
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_subject_candidate_count=len(subject_inputs),
        track_count=len(track_observations),
        assignment_count=len(assignment_observations),
        sampled_frames=sampled_frames,
        role_counts=role_counts,
        assignment_role_counts=assignment_role_counts,
    )
    replay_url = (
        f"{viewer_base_url}/replay/{media.id}?"
        f"detectionRunId={source_detection_run_id}"
        f"&subjectRunId={source_subject_run_id}"
        f"&mainPlayerTrackRunId={run.id}"
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "main player track assignment complete",
        "main_player_track_run_id": run.id,
        "media_id": media.id,
        "source_detection_run_id": source_detection_run_id,
        "source_subject_run_id": source_subject_run_id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "tracks": {
            "near_player_track_candidate": role_counts.get("near_player_track_candidate", 0),
            "far_player_track_candidate": role_counts.get("far_player_track_candidate", 0),
            "total": len(track_observations),
        },
        "assignments": {
            "near_player_track_assignment_candidate": assignment_role_counts.get(
                "near_player_track_candidate", 0
            ),
            "far_player_track_assignment_candidate": assignment_role_counts.get(
                "far_player_track_candidate", 0
            ),
            "total": len(assignment_observations),
        },
        "source_subject_candidates_considered": len(subject_inputs),
        "selected_frames": len(sampled_frames),
        "sampled_frames": sampled_frames,
        "replay_url": replay_url,
        "warnings": dict(MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS),
    }


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "main-player-track-assignment",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "tracking",
            ModelRegistry.source == "apps.worker.services.main_player_track_assignment",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="main-player-track-assignment",
        version="v0",
        model_family="tracking",
        source="apps.worker.services.main_player_track_assignment",
        metadata_jsonb={
            "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
            "candidate_track_only": True,
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
            "raw_detections_not_mutated": True,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    source_detection_run_id: str,
    source_subject_run_id: str,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    config: MainPlayerTrackAssignmentConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="main-player-track-assignment-config",
        config_version="v0",
        payload_jsonb={
            "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
            "source_detection_run_id": source_detection_run_id,
            "source_subject_run_id": source_subject_run_id,
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "assignment_config": config.as_dict(),
            **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_run(
    *,
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    source_detection_run_id: str,
    source_subject_run_id: str,
    config: MainPlayerTrackAssignmentConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
            "source_detection_run_id": source_detection_run_id,
            "source_subject_run_id": source_subject_run_id,
            "assignment_config": config.as_dict(),
            "evidence_source": "main_player_track_assignment",
            "source_label": "main player track candidate assignment",
            **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    *,
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="main_player_track_assignment_v0",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
            **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _source_subject_candidates(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str,
    source_subject_run_id: str,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
) -> list[SubjectCandidateInput]:
    if every_n_frames <= 0:
        raise MainPlayerTrackAssignmentError("every_n_frames must be greater than 0")
    resolved_start = 0 if frame_start is None else int(frame_start)
    resolved_end = None if frame_end is None else int(frame_end)
    if resolved_start < 0:
        raise MainPlayerTrackAssignmentError("frame_start must be greater than or equal to 0")
    if resolved_end is not None and resolved_end < 0:
        raise MainPlayerTrackAssignmentError("frame_end must be greater than or equal to 0")
    if resolved_end is not None and resolved_start > resolved_end:
        raise MainPlayerTrackAssignmentError("frame_start must be less than or equal to frame_end")

    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == source_subject_run_id,
            Observation.observation_type == MAIN_SUBJECT_OBSERVATION_TYPE,
            Observation.frame_start.is_not(None),
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.frame_start, Observation.id)
    )
    query = query.where(Observation.frame_start >= resolved_start)
    if resolved_end is not None:
        query = query.where(Observation.frame_start <= resolved_end)
    rows = list(session.scalars(query).all())
    if every_n_frames > 1:
        rows = [
            row
            for row in rows
            if row.frame_start is not None
            and (int(row.frame_start) - resolved_start) % every_n_frames == 0
        ]
    if max_frames is not None:
        allowed_frames = set(
            sorted({int(row.frame_start) for row in rows})[: max(0, int(max_frames))]
        )
        rows = [
            row
            for row in rows
            if row.frame_start is not None and int(row.frame_start) in allowed_frames
        ]

    inputs: list[SubjectCandidateInput] = []
    for row in rows:
        payload = row.payload_jsonb or {}
        role = str(payload.get("subject_role_candidate") or "")
        track_role = SUBJECT_ROLE_TO_TRACK_ROLE.get(role)
        if track_role is None:
            continue
        detection_id = str(payload.get("source_detection_observation_id") or "")
        if not detection_id:
            continue
        detection = session.get(Observation, detection_id)
        if detection is None:
            continue
        if detection.run_id != source_detection_run_id:
            continue
        if detection.observation_type != "player_detection":
            continue
        bbox = _bbox(payload) or _bbox(_merged_payload(detection))
        if bbox is None:
            continue
        timestamp_ms = int(
            row.timestamp_start_ms
            if row.timestamp_start_ms is not None
            else frame_to_timestamp_ms(media.fps or 30.0, int(row.frame_start))
        )
        inputs.append(
            SubjectCandidateInput(
                observation=row,
                detection=detection,
                role=role,
                track_role=track_role,
                bbox=bbox,
                selection_score=float(payload.get("selection_score") or row.confidence or 0.0),
                timestamp_ms=timestamp_ms,
            )
        )
    return inputs


def _assign_tracks_by_role(
    *,
    media: MediaAsset,
    subject_inputs: list[SubjectCandidateInput],
    config: MainPlayerTrackAssignmentConfig,
) -> dict[str, list[TrackAssignmentCandidate]]:
    by_role: dict[str, list[SubjectCandidateInput]] = defaultdict(list)
    for subject in subject_inputs:
        by_role[subject.track_role].append(subject)

    assignments: dict[str, list[TrackAssignmentCandidate]] = {}
    for track_role, subjects in by_role.items():
        track_candidate_id = f"{track_role}_001"
        ordered = sorted(
            subjects,
            key=lambda subject: (
                subject.observation.frame_start or 0,
                subject.observation.id,
            ),
        )
        previous: SubjectCandidateInput | None = None
        role_assignments: list[TrackAssignmentCandidate] = []
        for subject in ordered:
            continuity_score = 1.0
            center_distance = None
            area_change = None
            if previous is not None:
                center_distance = _normalized_center_distance(
                    previous.bbox,
                    subject.bbox,
                    width=float(media.width or 1),
                    height=float(media.height or 1),
                )
                continuity_score = max(
                    0.0,
                    1.0 - (center_distance / max(0.001, config.max_center_jump_norm)),
                )
                area_change = _area_change_ratio(previous.bbox, subject.bbox)
                if area_change > config.max_area_ratio_change:
                    continuity_score *= 0.5
            assignment_score = _bounded(
                0.60 * subject.selection_score
                + 0.30 * continuity_score
                + 0.10 * _area_score(subject.bbox, media)
            )
            if assignment_score >= config.min_assignment_score:
                role_assignments.append(
                    TrackAssignmentCandidate(
                        subject=subject,
                        track_candidate_id=track_candidate_id,
                        assignment_score=assignment_score,
                        continuity_score=_bounded(continuity_score),
                        center_distance_norm=(
                            None if center_distance is None else round(center_distance, 6)
                        ),
                        area_change_ratio=None if area_change is None else round(area_change, 6),
                    )
                )
                previous = subject
        if role_assignments:
            assignments[track_role] = role_assignments
    return assignments


def _persist_track_candidates(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    source_detection_run_id: str,
    source_subject_run_id: str,
    assignments_by_role: dict[str, list[TrackAssignmentCandidate]],
) -> dict[str, Any]:
    writer = ObservationWriter(session)
    observations: dict[str, Any] = {}
    for track_role, assignments in sorted(assignments_by_role.items()):
        first = assignments[0].subject
        last = assignments[-1].subject
        scores = [assignment.assignment_score for assignment in assignments]
        source_candidate_count = len(
            {
                assignment.subject.observation.id
                for assignment in assignments
            }
        )
        track_candidate_id = assignments[0].track_candidate_id
        payload = {
            "track_role_candidate": track_role,
            "track_candidate_id": track_candidate_id,
            "source_subject_run_id": source_subject_run_id,
            "source_detection_run_id": source_detection_run_id,
            "frame_start": int(first.observation.frame_start),
            "frame_end": int(last.observation.frame_start),
            "timestamp_start_ms": first.timestamp_ms,
            "timestamp_end_ms": last.timestamp_ms,
            "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
            "track_summary": {
                "source_candidate_count": source_candidate_count,
                "assigned_detection_count": len(assignments),
                "mean_assignment_score": round(mean(scores), 6) if scores else None,
                "min_assignment_score": min(scores) if scores else None,
                "max_assignment_score": max(scores) if scores else None,
            },
            "assignment_source_candidate_ids": [
                assignment.subject.observation.id for assignment in assignments
            ],
            **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
        }
        observations[track_role] = writer.write(
            ObservationCreate(
                media_id=media.id,
                run_id=run.id,
                observation_family="tracking",
                observation_type=MAIN_PLAYER_TRACK_OBSERVATION_TYPE,
                granularity="frame_range",
                frame_start=int(first.observation.frame_start),
                frame_end=int(last.observation.frame_start),
                timestamp_start_ms=first.timestamp_ms,
                timestamp_end_ms=last.timestamp_ms,
                confidence=round(mean(scores), 6) if scores else None,
                model_id=model.id,
                runtime_config_id=runtime_config.id,
                coordinate_space="image_pixels",
                payload_jsonb=payload,
                idempotency_key=f"{run.id}:main-player-track:{track_role}",
            )
        )
    return observations


def _persist_track_assignments(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    track_observations: dict[str, Any],
    assignments_by_role: dict[str, list[TrackAssignmentCandidate]],
) -> list[Any]:
    writer = ObservationWriter(session)
    observations = []
    for track_role, assignments in sorted(assignments_by_role.items()):
        track_observation = track_observations[track_role]
        for index, assignment in enumerate(assignments):
            subject = assignment.subject
            frame_number = int(subject.observation.frame_start)
            payload = {
                "track_candidate_id": assignment.track_candidate_id,
                "track_role_candidate": track_role,
                "source_track_candidate_observation_id": track_observation.id,
                "source_subject_candidate_observation_id": subject.observation.id,
                "source_detection_observation_id": subject.detection.id,
                "source_subject_run_id": subject.observation.run_id,
                "source_detection_run_id": subject.detection.run_id,
                "frame_number": frame_number,
                "timestamp_ms": subject.timestamp_ms,
                "assignment_method": "nearest_temporal_continuity_v0",
                "assignment_score": assignment.assignment_score,
                "selection_score": subject.selection_score,
                "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
                "assignment_features": {
                    "continuity_score": assignment.continuity_score,
                    "center_distance_norm": assignment.center_distance_norm,
                    "area_change_ratio": assignment.area_change_ratio,
                    "bbox_center_x": _bbox_center(subject.bbox)[0],
                    "bbox_center_y": _bbox_center(subject.bbox)[1],
                    "bbox_area": subject.bbox["width"] * subject.bbox["height"],
                },
                "bbox": subject.bbox,
                **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
            }
            observations.append(
                writer.write(
                    ObservationCreate(
                        media_id=media.id,
                        run_id=run.id,
                        observation_family="tracking",
                        observation_type=MAIN_PLAYER_TRACK_ASSIGNMENT_OBSERVATION_TYPE,
                        granularity="frame",
                        frame_start=frame_number,
                        frame_end=frame_number,
                        timestamp_start_ms=subject.timestamp_ms,
                        timestamp_end_ms=subject.timestamp_ms,
                        confidence=assignment.assignment_score,
                        model_id=model.id,
                        runtime_config_id=runtime_config.id,
                        coordinate_space="image_pixels",
                        payload_jsonb=payload,
                        idempotency_key=(
                            f"{run.id}:main-player-track-assignment:{track_role}:"
                            f"{frame_number}:{subject.observation.id}:{index}"
                        ),
                        lineage=[
                            ObservationLineageCreate(
                                parent_observation_id=subject.observation.id,
                                relationship_type=(
                                    "main_player_track_assignment_from_subject_candidate"
                                ),
                                processing_step_id=step.id,
                                payload_jsonb={
                                    "selection_method": MAIN_PLAYER_TRACK_ASSIGNMENT_METHOD,
                                    "track_role_candidate": track_role,
                                    "track_candidate_id": assignment.track_candidate_id,
                                    "assignment_score": assignment.assignment_score,
                                    **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
                                },
                            ),
                            ObservationLineageCreate(
                                parent_observation_id=subject.detection.id,
                                relationship_type=(
                                    "main_player_track_assignment_from_player_detection"
                                ),
                                processing_step_id=step.id,
                                payload_jsonb={
                                    "source_observation_type": subject.detection.observation_type,
                                    "track_role_candidate": track_role,
                                    "track_candidate_id": assignment.track_candidate_id,
                                    "assignment_score": assignment.assignment_score,
                                    **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
                                },
                            ),
                            ObservationLineageCreate(
                                parent_observation_id=track_observation.id,
                                relationship_type=(
                                    "main_player_track_assignment_for_track_candidate"
                                ),
                                processing_step_id=step.id,
                                payload_jsonb={
                                    "source_observation_type": MAIN_PLAYER_TRACK_OBSERVATION_TYPE,
                                    "track_role_candidate": track_role,
                                    "track_candidate_id": assignment.track_candidate_id,
                                    "assignment_score": assignment.assignment_score,
                                    **MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS,
                                },
                            ),
                        ],
                    )
                )
            )
    return observations


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_subject_candidate_count: int,
    track_count: int,
    assignment_count: int,
    sampled_frames: list[int],
    role_counts: Counter[str],
    assignment_role_counts: Counter[str],
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "source_subject_candidate_count": source_subject_candidate_count,
        "main_player_track_candidate_count": track_count,
        "main_player_track_assignment_candidate_count": assignment_count,
        "sampled_frames": sampled_frames,
        "counts_by_track_role": dict(role_counts),
        "assignment_counts_by_track_role": dict(assignment_role_counts),
        "counts_by_observation_type": {
            MAIN_PLAYER_TRACK_OBSERVATION_TYPE: track_count,
            MAIN_PLAYER_TRACK_ASSIGNMENT_OBSERVATION_TYPE: assignment_count,
        },
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "source_subject_candidate_count": source_subject_candidate_count,
        "main_player_track_candidate_count": track_count,
        "main_player_track_assignment_candidate_count": assignment_count,
        "sampled_frames": sampled_frames,
        "counts_by_track_role": dict(role_counts),
        "assignment_counts_by_track_role": dict(assignment_role_counts),
    }
    session.commit()


def _mark_failed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    error_message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {**run.metadata_jsonb, "error": error_message}
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {**step.metadata_jsonb, "error": error_message}
    session.commit()


def _merged_payload(observation: Observation) -> dict[str, Any]:
    atomic_payload = (
        observation.atomic_detail.payload_jsonb
        if observation.atomic_detail is not None
        else {}
    )
    return {**observation.payload_jsonb, **atomic_payload}


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    width = _number(value.get("width", value.get("w")))
    height = _number(value.get("height", value.get("h")))
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "width": width, "height": height}


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _bbox_center(bbox: dict[str, float]) -> tuple[float, float]:
    return (
        round(bbox["x"] + bbox["width"] / 2.0, 6),
        round(bbox["y"] + bbox["height"] / 2.0, 6),
    )


def _normalized_center_distance(
    previous: dict[str, float],
    current: dict[str, float],
    *,
    width: float,
    height: float,
) -> float:
    previous_x, previous_y = _bbox_center(previous)
    current_x, current_y = _bbox_center(current)
    dx = (current_x - previous_x) / max(1.0, width)
    dy = (current_y - previous_y) / max(1.0, height)
    return (dx * dx + dy * dy) ** 0.5


def _area_change_ratio(previous: dict[str, float], current: dict[str, float]) -> float:
    previous_area = max(1.0, previous["width"] * previous["height"])
    current_area = max(1.0, current["width"] * current["height"])
    return max(previous_area / current_area, current_area / previous_area)


def _area_score(bbox: dict[str, float], media: MediaAsset) -> float:
    image_area = max(1.0, float(media.width or 1) * float(media.height or 1))
    return min(1.0, (bbox["width"] * bbox["height"]) / image_area / 0.06)


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


def _failed(
    status: str,
    message: str,
    error_type: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(MAIN_PLAYER_TRACK_ASSIGNMENT_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
