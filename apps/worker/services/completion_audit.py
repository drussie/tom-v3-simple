from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    AtomicObservation,
    EvidenceArtifact,
    GameplayObservation,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProcessingRun,
    ProcessingStep,
    QueryResult,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

CORE_FRAME_OBSERVATION_TYPES = {
    "ball_detection",
    "player_detection",
    "ball_tracklet_candidate",
    "player_tracklet_candidate",
    "track_point_candidate",
    "player_pose_observation",
}
DEMO_RUN_NAMES = {
    "gameplay": "demo-fixture-gameplay-run",
    "detection": "demo-fixture-detection-run",
    "tracklet": "demo-candidate-tracklet-run",
    "pose": "demo-fixture-pose-run",
}
REVIEW_EXPORT_TYPES = {"pose_review_dataset_export", "tracklet_review_dataset_export"}
FRAME_ARTIFACT_TYPES = {"frame_image", "detection_frame_image"}
FILE_BACKED_ARTIFACT_TYPES = REVIEW_EXPORT_TYPES | FRAME_ARTIFACT_TYPES
DEMO_REQUIRED_EXPORT_TYPES = {
    "pose_review_dataset_export",
    "tracklet_review_dataset_export",
}


class AuditRecorder:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def record(
        self,
        *,
        name: str,
        severity: str,
        issues: list[str] | int,
        passed: str,
        failed: str,
    ) -> None:
        issue_count = issues if isinstance(issues, int) else len(issues)
        details = [] if isinstance(issues, int) else issues[:10]
        if issue_count == 0:
            status = "passed"
            message = passed
        elif severity == "fail":
            status = "failed"
            message = failed
        else:
            status = "warning"
            message = failed
        self.checks.append(
            {
                "name": name,
                "status": status,
                "severity": severity,
                "message": message,
                "count": issue_count,
                "details": details,
            }
        )

    def result(self, *, summary: dict[str, int], strict: bool) -> dict[str, Any]:
        failures = [
            check
            for check in self.checks
            if check["status"] == "failed" or (strict and check["status"] == "warning")
        ]
        warnings = [check for check in self.checks if check["status"] == "warning"]
        if failures:
            status = "failed"
        elif warnings:
            status = "warning"
        else:
            status = "passed"
        return {
            "ok": status != "failed",
            "status": status,
            "summary": summary,
            "checks": self.checks,
            "warnings": warnings,
            "failures": failures,
            "observation_only": True,
            "no_adjudication": True,
        }


def run_completion_audit(
    session: Session,
    media_id: str | None = None,
    demo_only: bool = True,
    strict: bool = False,
) -> dict[str, Any]:
    """Audit persisted TOM v3 evidence structure without judging model correctness."""

    scope = _load_scope(session, media_id=media_id, demo_only=demo_only)
    recorder = AuditRecorder()

    _check_media(recorder, scope=scope, media_id=media_id, demo_only=demo_only)
    _check_processing_runs(recorder, scope=scope, demo_only=demo_only)
    _check_processing_steps(recorder, scope=scope)
    _check_observations(recorder, scope=scope)
    _check_typed_rows(recorder, scope=scope)
    _check_tracklets(recorder, scope=scope, demo_only=demo_only)
    _check_pose(recorder, scope=scope, demo_only=demo_only)
    _check_lineage(recorder, scope=scope, demo_only=demo_only)
    _check_artifacts(recorder, scope=scope, demo_only=demo_only)
    _check_annotations(recorder, scope=scope, demo_only=demo_only)
    _check_exports(recorder, scope=scope, demo_only=demo_only)
    if demo_only:
        _check_demo_completeness(recorder, scope=scope)

    return recorder.result(summary=_summary(scope), strict=strict)


def _load_scope(
    session: Session,
    *,
    media_id: str | None,
    demo_only: bool,
) -> dict[str, Any]:
    all_media = list(session.scalars(select(MediaAsset)).all())
    if media_id is not None:
        media = [row for row in all_media if row.id == media_id]
    elif demo_only:
        media = [row for row in all_media if _is_demo_media(row)]
    else:
        media = all_media

    media_ids = {row.id for row in media}
    all_runs = list(session.scalars(select(ProcessingRun)).all())
    all_steps = list(session.scalars(select(ProcessingStep)).all())
    all_observations = list(session.scalars(select(Observation)).all())
    all_atomic = list(session.scalars(select(AtomicObservation)).all())
    all_gameplay = list(session.scalars(select(GameplayObservation)).all())
    all_pose = list(session.scalars(select(PoseObservation)).all())
    all_tracklets = list(session.scalars(select(Tracklet)).all())
    all_track_points = list(session.scalars(select(TrackPoint)).all())
    all_lineage = list(session.scalars(select(ObservationLineage)).all())
    all_artifacts = list(session.scalars(select(EvidenceArtifact)).all())
    all_annotations = list(session.scalars(select(HumanAnnotation)).all())
    all_query_results = list(session.scalars(select(QueryResult)).all())

    if media_id is None and not demo_only:
        runs = all_runs
        observations = all_observations
        artifacts = all_artifacts
        annotations = all_annotations
        tracklets = all_tracklets
        pose_rows = all_pose
    else:
        runs = [row for row in all_runs if row.media_id in media_ids]
        observations = [row for row in all_observations if row.media_id in media_ids]
        artifacts = [row for row in all_artifacts if row.media_id in media_ids]
        annotations = [row for row in all_annotations if row.media_id in media_ids]
        tracklets = [row for row in all_tracklets if row.media_id in media_ids]
        pose_rows = [
            row
            for row in all_pose
            if row.media_id in media_ids or row.observation_id in {obs.id for obs in observations}
        ]

    run_ids = {row.id for row in runs}
    observation_ids = {row.id for row in observations}
    tracklet_ids = {row.id for row in tracklets}
    track_points = (
        all_track_points
        if media_id is None and not demo_only
        else [row for row in all_track_points if row.tracklet_id in tracklet_ids]
    )
    track_point_ids = {row.id for row in track_points}
    steps = (
        all_steps
        if media_id is None and not demo_only
        else [row for row in all_steps if row.run_id in run_ids]
    )
    lineage = (
        all_lineage
        if media_id is None and not demo_only
        else [
            row
            for row in all_lineage
            if row.child_observation_id in observation_ids
            or row.parent_observation_id in observation_ids
        ]
    )
    atomic_rows = (
        all_atomic
        if media_id is None and not demo_only
        else [row for row in all_atomic if row.observation_id in observation_ids]
    )
    gameplay_rows = (
        all_gameplay
        if media_id is None and not demo_only
        else [row for row in all_gameplay if row.observation_id in observation_ids]
    )

    return {
        "all_media": all_media,
        "all_runs": all_runs,
        "all_steps": all_steps,
        "all_observations": all_observations,
        "all_artifacts": all_artifacts,
        "all_annotations": all_annotations,
        "media": media,
        "runs": runs,
        "steps": steps,
        "observations": observations,
        "atomic_rows": atomic_rows,
        "gameplay_rows": gameplay_rows,
        "pose_rows": pose_rows,
        "tracklets": tracklets,
        "track_points": track_points,
        "lineage": lineage,
        "artifacts": artifacts,
        "annotations": annotations,
        "query_results": all_query_results,
        "models": list(session.scalars(select(ModelRegistry)).all()),
        "runtime_configs": list(session.scalars(select(RuntimeConfig)).all()),
        "tracklet_ids": tracklet_ids,
        "track_point_ids": track_point_ids,
    }


def _check_media(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    media_id: str | None,
    demo_only: bool,
) -> None:
    media = scope["media"]
    missing_scope = []
    if media_id is not None and not media:
        missing_scope.append(f"media_id not found: {media_id}")
    elif demo_only and not media:
        missing_scope.append("No demo media found. Run make demo first.")
    elif not demo_only and not media:
        recorder.record(
            name="media_scope_has_rows",
            severity="warn",
            issues=1,
            passed="Media scope contains rows.",
            failed="No media rows found in all-data mode.",
        )
        return

    recorder.record(
        name="media_scope_has_rows",
        severity="fail",
        issues=missing_scope,
        passed="Media scope contains auditable media rows.",
        failed="Media scope is empty.",
    )
    if not media:
        return

    source_issues = [row.id for row in media if not row.source_uri]
    recorder.record(
        name="media_has_source_uri",
        severity="fail",
        issues=source_issues,
        passed="Media rows have source_uri.",
        failed="Media rows are missing source_uri.",
    )
    metadata_issues = [
        row.id
        for row in media
        if row.fps is None or row.frame_count is None or row.width is None or row.height is None
    ]
    recorder.record(
        name="media_has_probe_metadata",
        severity="warn",
        issues=metadata_issues,
        passed="Media rows include fps, frame_count, width, and height.",
        failed="Some media rows lack fps/frame_count/dimensions.",
    )
    if demo_only and media_id is None:
        non_demo = [row.id for row in media if not _is_demo_media(row)]
        recorder.record(
            name="demo_media_marked",
            severity="fail",
            issues=non_demo,
            passed="Demo media rows are marked with tom_v3_demo metadata.",
            failed="Demo media rows are missing tom_v3_demo metadata.",
        )


def _check_processing_runs(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    media_ids = {row.id for row in scope["media"]}
    runtime_config_ids = {row.id for row in scope["runtime_configs"]}
    runs: list[ProcessingRun] = scope["runs"]
    missing_media = [row.id for row in runs if row.media_id not in media_ids]
    recorder.record(
        name="processing_runs_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Processing runs reference media rows in scope.",
        failed="Processing runs reference missing media rows.",
    )
    bad_status = [
        f"{row.id}:{row.run_status}"
        for row in runs
        if row.run_status not in {"completed", "failed"}
    ]
    recorder.record(
        name="processing_runs_have_terminal_status",
        severity="warn",
        issues=bad_status,
        passed="Processing runs have completed/failed status.",
        failed="Processing runs are not in completed/failed status.",
    )
    missing_runtime = [
        row.id
        for row in runs
        if row.runtime_config_id is not None and row.runtime_config_id not in runtime_config_ids
    ]
    recorder.record(
        name="processing_runs_reference_runtime_config",
        severity="fail",
        issues=missing_runtime,
        passed="Processing runs reference existing runtime configs when present.",
        failed="Processing runs reference missing runtime configs.",
    )
    missing_completed_at = [
        row.id for row in runs if row.run_status == "completed" and row.completed_at is None
    ]
    recorder.record(
        name="completed_processing_runs_have_completed_at",
        severity="warn",
        issues=missing_completed_at,
        passed="Completed processing runs have completed_at.",
        failed="Completed processing runs are missing completed_at.",
    )
    if demo_only and scope["media"]:
        run_names = {row.run_name for row in runs}
        missing_demo_runs = [
            f"{label}:{name}"
            for label, name in DEMO_RUN_NAMES.items()
            if name not in run_names
        ]
        recorder.record(
            name="demo_expected_runs_exist",
            severity="fail",
            issues=missing_demo_runs,
            passed="Demo gameplay, detection, tracklet, and pose runs exist.",
            failed="Demo path is missing expected processing runs.",
        )


def _check_processing_steps(recorder: AuditRecorder, *, scope: dict[str, Any]) -> None:
    run_ids = {row.id for row in scope["runs"]}
    runtime_config_ids = {row.id for row in scope["runtime_configs"]}
    steps: list[ProcessingStep] = scope["steps"]
    missing_run = [row.id for row in steps if row.run_id not in run_ids]
    recorder.record(
        name="processing_steps_reference_runs",
        severity="fail",
        issues=missing_run,
        passed="Processing steps reference processing runs in scope.",
        failed="Processing steps reference missing processing runs.",
    )
    bad_status = [
        f"{row.id}:{row.step_status}"
        for row in steps
        if row.step_status not in {"completed", "failed"}
    ]
    recorder.record(
        name="processing_steps_have_terminal_status",
        severity="warn",
        issues=bad_status,
        passed="Processing steps have completed/failed status.",
        failed="Processing steps are not in completed/failed status.",
    )
    missing_runtime = [
        row.id
        for row in steps
        if row.runtime_config_id is not None and row.runtime_config_id not in runtime_config_ids
    ]
    recorder.record(
        name="processing_steps_reference_runtime_config",
        severity="fail",
        issues=missing_runtime,
        passed="Processing steps reference existing runtime configs when present.",
        failed="Processing steps reference missing runtime configs.",
    )
    run_ids_with_steps = {row.run_id for row in steps}
    missing_steps = [
        row.id
        for row in scope["runs"]
        if row.run_status == "completed" and row.id not in run_ids_with_steps
    ]
    recorder.record(
        name="completed_runs_have_processing_steps",
        severity="warn",
        issues=missing_steps,
        passed="Completed processing runs have processing steps.",
        failed="Completed processing runs are missing processing steps.",
    )


def _check_observations(recorder: AuditRecorder, *, scope: dict[str, Any]) -> None:
    media_ids = {row.id for row in scope["media"]}
    run_ids = {row.id for row in scope["runs"]}
    model_ids = {row.id for row in scope["models"]}
    runtime_config_ids = {row.id for row in scope["runtime_configs"]}
    runs_by_id = {row.id: row for row in scope["runs"]}
    observations: list[Observation] = scope["observations"]

    missing_media = [row.id for row in observations if row.media_id not in media_ids]
    recorder.record(
        name="observations_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Observations reference media rows in scope.",
        failed="Observations reference missing media rows.",
    )
    missing_run = [row.id for row in observations if row.run_id not in run_ids]
    recorder.record(
        name="observations_reference_runs",
        severity="fail",
        issues=missing_run,
        passed="Observations reference processing runs in scope.",
        failed="Observations reference missing processing runs.",
    )
    run_media_mismatch = [
        row.id
        for row in observations
        if row.run_id in runs_by_id and runs_by_id[row.run_id].media_id != row.media_id
    ]
    recorder.record(
        name="observations_run_media_matches",
        severity="fail",
        issues=run_media_mismatch,
        passed="Observation media_id matches its processing run media_id.",
        failed="Observations have media_id values that differ from their processing run.",
    )
    missing_type = [
        row.id for row in observations if not row.observation_family or not row.observation_type
    ]
    recorder.record(
        name="observations_have_family_and_type",
        severity="fail",
        issues=missing_type,
        passed="Observations have family and type.",
        failed="Observations are missing family/type values.",
    )
    missing_frame_time = [
        row.id
        for row in observations
        if row.observation_type in CORE_FRAME_OBSERVATION_TYPES
        and (
            row.frame_start is None
            or row.frame_end is None
            or row.timestamp_start_ms is None
            or row.timestamp_end_ms is None
        )
    ]
    recorder.record(
        name="core_observations_have_frame_time",
        severity="fail",
        issues=missing_frame_time,
        passed="Core demo observation types have frame/time fields.",
        failed="Core demo observation types are missing frame/time fields.",
    )
    missing_model = [
        row.id for row in observations if row.model_id is not None and row.model_id not in model_ids
    ]
    recorder.record(
        name="observations_reference_models",
        severity="fail",
        issues=missing_model,
        passed="Observations reference existing model registry rows when present.",
        failed="Observations reference missing model registry rows.",
    )
    missing_runtime = [
        row.id
        for row in observations
        if row.runtime_config_id is not None and row.runtime_config_id not in runtime_config_ids
    ]
    recorder.record(
        name="observations_reference_runtime_configs",
        severity="fail",
        issues=missing_runtime,
        passed="Observations reference existing runtime configs when present.",
        failed="Observations reference missing runtime configs.",
    )


def _check_typed_rows(recorder: AuditRecorder, *, scope: dict[str, Any]) -> None:
    observation_ids = {row.id for row in scope["observations"]}
    atomic_ids = {row.observation_id for row in scope["atomic_rows"]}
    gameplay_ids = {row.observation_id for row in scope["gameplay_rows"]}
    pose_ids = {row.observation_id for row in scope["pose_rows"]}
    tracklet_observation_ids = {
        row.observation_id for row in scope["tracklets"] if row.observation_id is not None
    }
    track_point_observation_ids = {
        row.observation_id for row in scope["track_points"] if row.observation_id is not None
    }

    missing_atomic_parent = [
        row.observation_id
        for row in scope["atomic_rows"]
        if row.observation_id not in observation_ids
    ]
    recorder.record(
        name="atomic_rows_reference_observations",
        severity="fail",
        issues=missing_atomic_parent,
        passed="Atomic typed rows reference observations in scope.",
        failed="Atomic typed rows reference missing observations.",
    )
    missing_gameplay_parent = [
        row.observation_id
        for row in scope["gameplay_rows"]
        if row.observation_id not in observation_ids
    ]
    recorder.record(
        name="gameplay_rows_reference_observations",
        severity="fail",
        issues=missing_gameplay_parent,
        passed="Gameplay typed rows reference observations in scope.",
        failed="Gameplay typed rows reference missing observations.",
    )
    missing_pose_parent = [
        row.observation_id
        for row in scope["pose_rows"]
        if row.observation_id not in observation_ids
    ]
    recorder.record(
        name="pose_rows_reference_observations",
        severity="fail",
        issues=missing_pose_parent,
        passed="Pose typed rows reference observations in scope.",
        failed="Pose typed rows reference missing observations.",
    )

    missing_atomic_detail = [
        row.id
        for row in scope["observations"]
        if row.observation_type in {"ball_detection", "player_detection"}
        and row.id not in atomic_ids
    ]
    recorder.record(
        name="detection_observations_have_atomic_detail",
        severity="fail",
        issues=missing_atomic_detail,
        passed="Ball/player detection observations have atomic typed rows.",
        failed="Ball/player detection observations are missing atomic typed rows.",
    )
    missing_gameplay_detail = [
        row.id
        for row in scope["observations"]
        if row.observation_family == "gameplay" and row.id not in gameplay_ids
    ]
    recorder.record(
        name="gameplay_observations_have_typed_detail",
        severity="fail",
        issues=missing_gameplay_detail,
        passed="Gameplay observations have gameplay typed rows.",
        failed="Gameplay observations are missing gameplay typed rows.",
    )
    missing_pose_detail = [
        row.id
        for row in scope["observations"]
        if row.observation_type == "player_pose_observation" and row.id not in pose_ids
    ]
    recorder.record(
        name="pose_observations_have_typed_detail",
        severity="fail",
        issues=missing_pose_detail,
        passed="Pose observations have pose typed rows.",
        failed="Pose observations are missing pose typed rows.",
    )
    missing_tracklet_row = [
        row.id
        for row in scope["observations"]
        if row.observation_type in {"ball_tracklet_candidate", "player_tracklet_candidate"}
        and row.id not in tracklet_observation_ids
    ]
    recorder.record(
        name="tracklet_observations_have_tracklet_rows",
        severity="fail",
        issues=missing_tracklet_row,
        passed="Tracklet candidate observations are linked by tracklet rows.",
        failed="Tracklet candidate observations are missing tracklet rows.",
    )
    missing_track_point_row = [
        row.id
        for row in scope["observations"]
        if row.observation_type == "track_point_candidate"
        and row.id not in track_point_observation_ids
    ]
    recorder.record(
        name="track_point_observations_have_track_point_rows",
        severity="fail",
        issues=missing_track_point_row,
        passed="Track point candidate observations are linked by track_point rows.",
        failed="Track point candidate observations are missing track_point rows.",
    )


def _check_tracklets(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    media_ids = {row.id for row in scope["media"]}
    run_ids = {row.id for row in scope["runs"]}
    observation_ids = {row.id for row in scope["observations"]}
    tracklet_ids = {row.id for row in scope["tracklets"]}

    missing_media = [row.id for row in scope["tracklets"] if row.media_id not in media_ids]
    recorder.record(
        name="tracklets_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Tracklet rows reference media rows in scope.",
        failed="Tracklet rows reference missing media rows.",
    )
    missing_run = [row.id for row in scope["tracklets"] if row.run_id not in run_ids]
    recorder.record(
        name="tracklets_reference_runs",
        severity="fail",
        issues=missing_run,
        passed="Tracklet rows reference processing runs in scope.",
        failed="Tracklet rows reference missing processing runs.",
    )
    missing_observation = [
        row.id
        for row in scope["tracklets"]
        if row.observation_id is None or row.observation_id not in observation_ids
    ]
    recorder.record(
        name="tracklets_reference_observations",
        severity="fail",
        issues=missing_observation,
        passed="Tracklet rows reference candidate observations.",
        failed="Tracklet rows reference missing candidate observations.",
    )
    bad_track_point_tracklet = [
        row.id for row in scope["track_points"] if row.tracklet_id not in tracklet_ids
    ]
    recorder.record(
        name="track_points_reference_tracklets",
        severity="fail",
        issues=bad_track_point_tracklet,
        passed="Track points reference tracklets in scope.",
        failed="Track points reference missing tracklets.",
    )
    bad_track_point_observation = [
        row.id
        for row in scope["track_points"]
        if row.observation_id is None or row.observation_id not in observation_ids
    ]
    recorder.record(
        name="track_points_reference_observations",
        severity="fail",
        issues=bad_track_point_observation,
        passed="Track points reference candidate observations.",
        failed="Track points reference missing candidate observations.",
    )
    missing_track_point_frame_time = [
        row.id
        for row in scope["track_points"]
        if row.frame_number is None or row.timestamp_ms is None
    ]
    recorder.record(
        name="track_points_have_frame_time",
        severity="fail",
        issues=missing_track_point_frame_time,
        passed="Track points have media-owned frame/time values.",
        failed="Track points are missing frame/time values.",
    )
    source_detection_issues = []
    for row in scope["track_points"]:
        source_id = (row.payload_jsonb or {}).get("source_detection_observation_id")
        if not source_id or source_id not in observation_ids:
            source_detection_issues.append(row.id)
    recorder.record(
        name="track_points_reference_source_detections",
        severity="fail",
        issues=source_detection_issues,
        passed="Track points preserve source detection observation ids.",
        failed="Track points are missing valid source detection observation ids.",
    )
    if demo_only and scope["media"]:
        recorder.record(
            name="demo_tracklets_exist",
            severity="warn",
            issues=0 if scope["tracklets"] else 1,
            passed="Demo contains candidate tracklets.",
            failed="No candidate tracklets found in demo scope.",
        )


def _check_pose(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    media_ids = {row.id for row in scope["media"]}
    run_ids = {row.id for row in scope["runs"]}
    observation_by_id = {row.id: row for row in scope["observations"]}
    observation_ids = set(observation_by_id)
    tracklet_ids = scope["tracklet_ids"]
    track_point_ids = scope["track_point_ids"]
    lineage_pairs = {
        (row.parent_observation_id, row.child_observation_id, row.relationship_type)
        for row in scope["lineage"]
    }
    pose_rows: list[PoseObservation] = scope["pose_rows"]

    missing_media = [row.observation_id for row in pose_rows if row.media_id not in media_ids]
    recorder.record(
        name="pose_rows_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Pose rows reference media rows in scope.",
        failed="Pose rows reference missing media rows.",
    )
    missing_run = [row.observation_id for row in pose_rows if row.run_id not in run_ids]
    recorder.record(
        name="pose_rows_reference_runs",
        severity="fail",
        issues=missing_run,
        passed="Pose rows reference processing runs in scope.",
        failed="Pose rows reference missing processing runs.",
    )
    bad_keypoints = []
    bad_keypoint_counts = []
    for row in pose_rows:
        if row.skeleton_format == "coco17" and len(row.keypoints_jsonb or []) != 17:
            bad_keypoints.append(row.observation_id)
        if row.keypoint_count != len(row.keypoints_jsonb or []):
            bad_keypoint_counts.append(row.observation_id)
    recorder.record(
        name="pose_coco17_keypoints_have_expected_count",
        severity="fail",
        issues=bad_keypoints,
        passed="COCO17 pose rows contain 17 keypoints.",
        failed="COCO17 pose rows have malformed keypoint arrays.",
    )
    recorder.record(
        name="pose_keypoint_count_matches_payload",
        severity="fail",
        issues=bad_keypoint_counts,
        passed="Pose keypoint_count matches keypoints_jsonb length.",
        failed="Pose keypoint_count does not match keypoints_jsonb length.",
    )
    bad_owner = [
        row.observation_id for row in pose_rows if row.frame_time_owner != "media_indexing"
    ]
    recorder.record(
        name="pose_frame_time_owner_is_media_indexing",
        severity="fail",
        issues=bad_owner,
        passed="Pose rows keep frame_time_owner=media_indexing.",
        failed="Pose rows have unexpected frame_time_owner values.",
    )
    frame_time_mismatch = []
    for row in pose_rows:
        observation = observation_by_id.get(row.observation_id)
        if observation is None:
            continue
        if (
            row.frame_number != observation.frame_start
            or row.frame_number != observation.frame_end
            or row.timestamp_ms != observation.timestamp_start_ms
            or row.timestamp_ms != observation.timestamp_end_ms
        ):
            frame_time_mismatch.append(row.observation_id)
    recorder.record(
        name="pose_frame_time_matches_observation",
        severity="fail",
        issues=frame_time_mismatch,
        passed="Pose rows match observation spine frame/time.",
        failed="Pose rows differ from observation spine frame/time.",
    )
    source_detection_issues = []
    missing_source_lineage = []
    for row in pose_rows:
        if row.subject_detection_observation_id:
            if row.subject_detection_observation_id not in observation_ids:
                source_detection_issues.append(row.observation_id)
            elif (
                row.subject_detection_observation_id,
                row.observation_id,
                "pose_from_subject_detection_candidate",
            ) not in lineage_pairs:
                missing_source_lineage.append(row.observation_id)
        if row.subject_tracklet_id and row.subject_tracklet_id not in tracklet_ids:
            source_detection_issues.append(row.observation_id)
        if row.subject_track_point_id and row.subject_track_point_id not in track_point_ids:
            source_detection_issues.append(row.observation_id)
    recorder.record(
        name="pose_subject_context_references_exist",
        severity="fail",
        issues=source_detection_issues,
        passed="Pose subject association candidate ids reference existing rows.",
        failed="Pose subject association candidate ids reference missing rows.",
    )
    recorder.record(
        name="pose_source_detection_lineage_exists",
        severity="fail",
        issues=missing_source_lineage,
        passed="Source-associated pose rows have source detection lineage.",
        failed="Source-associated pose rows are missing source detection lineage.",
    )
    if demo_only and scope["media"]:
        recorder.record(
            name="demo_pose_observations_exist",
            severity="warn",
            issues=0 if pose_rows else 1,
            passed="Demo contains pose observations.",
            failed="No pose observations found in demo scope.",
        )


def _check_lineage(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    observation_ids = {row.id for row in scope["observations"]}
    lineage: list[ObservationLineage] = scope["lineage"]
    missing_parent = [
        row.id for row in lineage if row.parent_observation_id not in observation_ids
    ]
    recorder.record(
        name="lineage_parents_reference_observations",
        severity="fail",
        issues=missing_parent,
        passed="Lineage parent ids reference observations in scope.",
        failed="Lineage rows reference missing parent observations.",
    )
    missing_child = [
        row.id for row in lineage if row.child_observation_id not in observation_ids
    ]
    recorder.record(
        name="lineage_children_reference_observations",
        severity="fail",
        issues=missing_child,
        passed="Lineage child ids reference observations in scope.",
        failed="Lineage rows reference missing child observations.",
    )
    missing_relationship = [row.id for row in lineage if not row.relationship_type]
    recorder.record(
        name="lineage_relationship_type_present",
        severity="fail",
        issues=missing_relationship,
        passed="Lineage rows have relationship_type.",
        failed="Lineage rows are missing relationship_type.",
    )
    if demo_only and scope["media"]:
        relationship_types = {row.relationship_type for row in lineage}
        expected = {"tracked_from", "grouped_from"}
        if any(row.subject_detection_observation_id for row in scope["pose_rows"]):
            expected.add("pose_from_subject_detection_candidate")
        missing_expected = sorted(expected - relationship_types)
        recorder.record(
            name="demo_expected_lineage_types_exist",
            severity="warn",
            issues=missing_expected,
            passed="Demo lineage includes expected relationship types.",
            failed="Demo lineage is missing expected relationship types.",
        )


def _check_artifacts(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    media_ids = {row.id for row in scope["media"]}
    run_ids = {row.id for row in scope["runs"]}
    observation_ids = {row.id for row in scope["observations"]}
    artifacts: list[EvidenceArtifact] = scope["artifacts"]

    missing_media = [row.id for row in artifacts if row.media_id not in media_ids]
    recorder.record(
        name="artifacts_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Artifacts reference media rows in scope.",
        failed="Artifacts reference missing media rows.",
    )
    missing_run = [
        row.id for row in artifacts if row.run_id is not None and row.run_id not in run_ids
    ]
    recorder.record(
        name="artifacts_reference_runs",
        severity="fail",
        issues=missing_run,
        passed="Artifacts reference processing runs when present.",
        failed="Artifacts reference missing processing runs.",
    )
    missing_target = [
        row.id
        for row in artifacts
        if row.target_observation_id is not None
        and row.target_observation_id not in observation_ids
    ]
    recorder.record(
        name="artifacts_reference_target_observations",
        severity="fail",
        issues=missing_target,
        passed="Artifacts reference target observations when present.",
        failed="Artifacts reference missing target observations.",
    )
    missing_uri = [row.id for row in artifacts if not row.uri]
    recorder.record(
        name="artifacts_have_uri",
        severity="fail",
        issues=missing_uri,
        passed="Artifacts have uri/path values.",
        failed="Artifacts are missing uri/path values.",
    )
    missing_checksum = [
        row.id
        for row in artifacts
        if row.artifact_type in FILE_BACKED_ARTIFACT_TYPES and not row.checksum
    ]
    recorder.record(
        name="file_backed_artifacts_have_checksum",
        severity="fail",
        issues=missing_checksum,
        passed="File-backed frame/export artifacts include checksums.",
        failed="File-backed frame/export artifacts are missing checksums.",
    )
    missing_files = []
    for row in artifacts:
        if row.artifact_type not in FILE_BACKED_ARTIFACT_TYPES:
            continue
        path = _path_from_local_uri(row.uri)
        if path is not None and not path.is_file():
            missing_files.append(row.id)
    recorder.record(
        name="file_backed_artifact_files_exist",
        severity="fail",
        issues=missing_files,
        passed="File-backed artifact files exist on disk.",
        failed="File-backed artifact files are missing from disk.",
    )
    if demo_only and scope["media"]:
        frame_count = len([row for row in artifacts if row.artifact_type in FRAME_ARTIFACT_TYPES])
        recorder.record(
            name="demo_frame_artifacts_exist",
            severity="warn",
            issues=0 if frame_count else 1,
            passed="Demo includes frame image artifacts.",
            failed="No frame image artifacts found in demo scope.",
        )


def _check_annotations(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    media_ids = {row.id for row in scope["media"]}
    observation_ids = {row.id for row in scope["observations"]}
    artifact_ids = {row.id for row in scope["artifacts"]}
    annotations: list[HumanAnnotation] = scope["annotations"]

    missing_media = [row.id for row in annotations if row.media_id not in media_ids]
    recorder.record(
        name="annotations_reference_media",
        severity="fail",
        issues=missing_media,
        passed="Annotations reference media rows in scope.",
        failed="Annotations reference missing media rows.",
    )
    missing_observation = [
        row.id
        for row in annotations
        if row.observation_id is not None and row.observation_id not in observation_ids
    ]
    recorder.record(
        name="annotations_reference_observations",
        severity="fail",
        issues=missing_observation,
        passed="Annotations reference observations when present.",
        failed="Annotations reference missing observations.",
    )
    missing_artifact = [
        row.id
        for row in annotations
        if row.evidence_artifact_id is not None and row.evidence_artifact_id not in artifact_ids
    ]
    recorder.record(
        name="annotations_reference_artifacts",
        severity="fail",
        issues=missing_artifact,
        passed="Annotations reference artifacts when present.",
        failed="Annotations reference missing artifacts.",
    )
    seeded_issues = []
    for row in annotations:
        payload = row.payload_jsonb or {}
        if payload.get("demo_seeded") is True:
            if row.created_by != "tom-v3-demo" or not payload.get("annotation_label"):
                seeded_issues.append(row.id)
    recorder.record(
        name="demo_seeded_annotations_are_labeled",
        severity="fail",
        issues=seeded_issues,
        passed="Demo-seeded annotations have label and created_by metadata.",
        failed="Demo-seeded annotations are missing label or created_by metadata.",
    )
    if demo_only and scope["media"]:
        recorder.record(
            name="demo_annotations_exist",
            severity="warn",
            issues=0 if annotations else 1,
            passed="Demo contains review annotations.",
            failed="No review annotations found in demo scope.",
        )


def _check_exports(
    recorder: AuditRecorder,
    *,
    scope: dict[str, Any],
    demo_only: bool,
) -> None:
    artifacts: list[EvidenceArtifact] = scope["artifacts"]
    export_artifacts = [row for row in artifacts if row.artifact_type in REVIEW_EXPORT_TYPES]
    query_results: list[QueryResult] = scope["query_results"]
    query_export_ids = {
        (row.result_payload_jsonb or {}).get("export_artifact_id")
        for row in query_results
        if isinstance(row.result_payload_jsonb, dict)
    }
    missing_query_result = [
        row.id for row in export_artifacts if row.id not in query_export_ids
    ]
    recorder.record(
        name="review_exports_have_query_result_memory",
        severity="warn",
        issues=missing_query_result,
        passed="Review export artifacts have query_result memory when created by export services.",
        failed="Review export artifacts are missing query_result memory.",
    )
    if demo_only and scope["media"]:
        present_types = {row.artifact_type for row in export_artifacts}
        missing_exports = sorted(DEMO_REQUIRED_EXPORT_TYPES - present_types)
        recorder.record(
            name="demo_review_exports_exist",
            severity="fail",
            issues=missing_exports,
            passed="Demo includes pose and tracklet review export artifacts.",
            failed="Demo is missing expected review export artifacts.",
        )


def _check_demo_completeness(recorder: AuditRecorder, *, scope: dict[str, Any]) -> None:
    if not scope["media"]:
        recorder.record(
            name="demo_completeness",
            severity="fail",
            issues=["No demo media found. Run make demo first."],
            passed="Demo evidence path is complete.",
            failed="Demo evidence path is incomplete.",
        )
        return

    observation_types = {row.observation_type for row in scope["observations"]}
    export_types = {
        row.artifact_type
        for row in scope["artifacts"]
        if row.artifact_type in REVIEW_EXPORT_TYPES
    }
    run_names = {row.run_name for row in scope["runs"]}
    issues = []
    if DEMO_RUN_NAMES["detection"] not in run_names:
        issues.append("missing demo detection run")
    if DEMO_RUN_NAMES["tracklet"] not in run_names:
        issues.append("missing demo tracklet run")
    if DEMO_RUN_NAMES["pose"] not in run_names:
        issues.append("missing demo pose run")
    if not ({"ball_detection", "player_detection"} & observation_types):
        issues.append("missing ball/player detection observations")
    if not scope["tracklets"]:
        issues.append("missing tracklet rows")
    if not scope["track_points"]:
        issues.append("missing track point rows")
    if "player_pose_observation" not in observation_types:
        issues.append("missing pose observations")
    if not scope["artifacts"]:
        issues.append("missing evidence artifacts")
    if not scope["annotations"]:
        issues.append("missing review annotations")
    for artifact_type in sorted(DEMO_REQUIRED_EXPORT_TYPES):
        if artifact_type not in export_types:
            issues.append(f"missing {artifact_type}")

    recorder.record(
        name="demo_completeness",
        severity="fail",
        issues=issues,
        passed=(
            "Demo evidence path contains media, runs, observations, lineage, "
            "artifacts, annotations, and exports."
        ),
        failed="Demo evidence path is incomplete.",
    )


def _summary(scope: dict[str, Any]) -> dict[str, int]:
    typed_row_count = (
        len(scope["atomic_rows"]) + len(scope["gameplay_rows"]) + len(scope["pose_rows"])
    )
    return {
        "media_count": len(scope["media"]),
        "run_count": len(scope["runs"]),
        "step_count": len(scope["steps"]),
        "observation_count": len(scope["observations"]),
        "typed_row_count": typed_row_count,
        "lineage_count": len(scope["lineage"]),
        "artifact_count": len(scope["artifacts"]),
        "annotation_count": len(scope["annotations"]),
        "export_artifact_count": len(
            [row for row in scope["artifacts"] if row.artifact_type in REVIEW_EXPORT_TYPES]
        ),
        "tracklet_count": len(scope["tracklets"]),
        "track_point_count": len(scope["track_points"]),
        "pose_observation_count": len(scope["pose_rows"]),
    }


def _is_demo_media(media: MediaAsset) -> bool:
    return (media.metadata_jsonb or {}).get("tom_v3_demo") is True


def _path_from_local_uri(uri: str) -> Path | None:
    parsed = urlparse(uri)
    if parsed.scheme == "file":
        return Path(unquote(parsed.path))
    if not parsed.scheme:
        return Path(uri)
    return None
