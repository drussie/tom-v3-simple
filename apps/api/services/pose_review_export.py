from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    PoseReviewDatasetExportRequest,
    PoseReviewDatasetExportResponse,
)
from tom_v3_schema.ids import new_uuid
from tom_v3_schema.pose import PoseQueryFilters
from tom_v3_storage.db_models import EvidenceArtifact, QueryResult
from tom_v3_storage.local_media import calculate_sha256

from apps.api.services.pose_evidence_bundle import get_pose_evidence_bundle
from apps.api.services.pose_query import query_poses

EXPORT_VERSION = "pose_review_dataset_v0"
EXPORT_ARTIFACT_TYPE = "pose_review_dataset_export"
EXPORT_WARNINGS = {
    "pose_evidence_only": True,
    "annotations_are_reviews_only": True,
    "no_movement_interpretation": True,
    "no_adjudication": True,
}


class PoseReviewExportError(ValueError):
    pass


def export_pose_review_dataset(
    session: Session,
    request: PoseReviewDatasetExportRequest,
) -> PoseReviewDatasetExportResponse:
    pose_observation_ids = _selected_pose_observation_ids(session, request)
    if not pose_observation_ids:
        raise PoseReviewExportError("no pose observations matched export request")

    bundles = [_bundle_or_raise(session, pose_id) for pose_id in pose_observation_ids]
    export_id = new_uuid()
    export_payload = _export_payload(
        export_id=export_id,
        request=request,
        pose_observation_ids=pose_observation_ids,
        bundles=bundles,
    )
    export_path = _export_path(request.output_root, export_id, request.format)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(json.dumps(export_payload, indent=2, sort_keys=True), encoding="utf-8")
    checksum = calculate_sha256(export_path)

    artifact = _persist_export_artifact(
        session=session,
        request=request,
        export_id=export_id,
        export_path=export_path,
        checksum=checksum,
        pose_observation_ids=pose_observation_ids,
        bundles=bundles,
    )
    query_result = _persist_query_result(
        session=session,
        request=request,
        pose_observation_ids=pose_observation_ids,
        bundles=bundles,
        artifact=artifact,
    )
    session.commit()
    session.refresh(artifact)
    if query_result is not None:
        session.refresh(query_result)

    return PoseReviewDatasetExportResponse(
        export_id=export_id,
        artifact_id=artifact.id,
        uri=artifact.uri,
        path=str(export_path),
        checksum=checksum,
        pose_count=len(pose_observation_ids),
        pose_observation_ids=pose_observation_ids,
        query_result_id=query_result.id if query_result is not None else None,
        warnings=EXPORT_WARNINGS,
        metadata=artifact.metadata_jsonb,
    )


def _selected_pose_observation_ids(
    session: Session,
    request: PoseReviewDatasetExportRequest,
) -> list[str]:
    ids = list(dict.fromkeys(request.pose_observation_ids))
    query = _query_from_request(request)
    if query is not None:
        result = query_poses(session, query)
        ids.extend(row.observation["id"] for row in result.poses)
    return sorted(set(ids))


def _query_from_request(request: PoseReviewDatasetExportRequest) -> PoseQueryFilters | None:
    if request.query is None and request.run_id is None and request.media_id is None:
        return None
    query = request.query or PoseQueryFilters(limit=500)
    updates: dict[str, Any] = {"limit": 500}
    if request.run_id is not None:
        updates["run_id"] = request.run_id
    if request.media_id is not None:
        updates["media_id"] = request.media_id
    return query.model_copy(update=updates)


def _bundle_or_raise(session: Session, pose_observation_id: str) -> dict[str, Any]:
    bundle = get_pose_evidence_bundle(session, pose_observation_id)
    if bundle is None:
        raise PoseReviewExportError(f"pose observation not found: {pose_observation_id}")
    return bundle


def _export_payload(
    *,
    export_id: str,
    request: PoseReviewDatasetExportRequest,
    pose_observation_ids: list[str],
    bundles: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_bundles = [
        _bundle_for_export(
            bundle=bundle,
            include_annotations=request.include_annotations,
            include_artifacts=request.include_artifacts,
        )
        for bundle in bundles
    ]
    return {
        "pose_review_dataset_export": {
            "export_version": EXPORT_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "export_id": export_id,
            "query_spec": _query_spec(request),
            "selection": {
                "pose_observation_ids": pose_observation_ids,
                "pose_count": len(pose_observation_ids),
            },
            "warnings": EXPORT_WARNINGS,
            "media": _unique_by_id(
                bundle.get("media") for bundle in selected_bundles if bundle.get("media")
            ),
            "runs": _unique_by_id(
                bundle.get("run") for bundle in selected_bundles if bundle.get("run")
            ),
            "runtime_configs": _unique_by_id(
                bundle.get("runtime_config")
                for bundle in selected_bundles
                if bundle.get("runtime_config")
            ),
            "models": _unique_by_id(
                bundle.get("model_registry")
                for bundle in selected_bundles
                if bundle.get("model_registry")
            ),
            "records": [_record_for_export(bundle) for bundle in selected_bundles],
            "annotations": _annotations(selected_bundles),
            "artifacts": _artifacts(selected_bundles),
            "lineage": _lineage(selected_bundles),
            "provenance": {
                "generated_by": request.created_by or "tom-v3-worker",
                "repo_milestone": "4E",
                "blueprint": "Blueprint 4 - Pose Observation Movement Evidence Layer",
                "observation_only": True,
                "no_movement_interpretation": True,
                "no_adjudication": True,
            },
        }
    }


def _bundle_for_export(
    *,
    bundle: dict[str, Any],
    include_annotations: bool,
    include_artifacts: bool,
) -> dict[str, Any]:
    exported = json.loads(json.dumps(bundle))
    if not include_annotations:
        exported["annotations"] = []
        exported["annotation_summary"] = {}
        exported["pose_observation"]["annotations"] = []
        exported["pose_observation"]["annotation_summary"] = {}
    if not include_artifacts:
        exported["artifacts"] = []
    return exported


def _record_for_export(bundle: dict[str, Any]) -> dict[str, Any]:
    pose_bundle = bundle["pose_observation"]
    observation = pose_bundle["observation"]
    pose = pose_bundle["pose"]
    source_context = bundle.get("source_context", {})
    bbox = {
        "x": pose.get("bbox_x"),
        "y": pose.get("bbox_y"),
        "w": pose.get("bbox_w"),
        "h": pose.get("bbox_h"),
        "confidence": pose.get("bbox_confidence"),
    }
    return {
        "record_type": "pose_observation_review",
        "media": {
            "media_id": observation["media_id"],
            "frame_number": pose["frame_number"],
            "timestamp_ms": pose["timestamp_ms"],
            "frame_image_artifact_uri": _first_artifact_uri(bundle.get("artifacts", [])),
        },
        "pose_observation": {
            "observation_id": observation["id"],
            "run_id": observation["run_id"],
            "model_id": observation.get("model_id"),
            "runtime_config_id": observation.get("runtime_config_id"),
            "skeleton_format": pose["skeleton_format"],
            "skeleton_version": pose["skeleton_version"],
            "pose_confidence": pose.get("pose_confidence"),
            "bbox": bbox,
            "keypoint_count": pose["keypoint_count"],
            "keypoints_present_count": pose["keypoints_present_count"],
            "keypoints_missing_count": pose["keypoints_missing_count"],
            "mean_keypoint_confidence": pose.get("mean_keypoint_confidence"),
            "min_keypoint_confidence": pose.get("min_keypoint_confidence"),
            "max_keypoint_confidence": pose.get("max_keypoint_confidence"),
            "keypoints": pose["keypoints_jsonb"],
        },
        "subject_context": {
            "subject_ref_type": source_context.get("subject_ref_type"),
            "source_detection_observation_id": pose.get("subject_detection_observation_id"),
            "subject_tracklet_id": pose.get("subject_tracklet_id"),
            "subject_track_point_id": pose.get("subject_track_point_id"),
            "association_status": source_context.get("association_status"),
            "association_method": source_context.get("association_method"),
            "association_confidence": source_context.get("association_confidence"),
            "source_detection": source_context.get("source_detection"),
            "tracklet": source_context.get("tracklet"),
            "track_point": source_context.get("track_point"),
        },
        "lineage": bundle.get("lineage", []),
        "artifacts": {
            "pose_overlay_image_uri": None,
            "source_frame_uri": _first_artifact_uri(bundle.get("artifacts", [])),
            "items": bundle.get("artifacts", []),
        },
        "annotations": bundle.get("annotations", []),
        "warnings": EXPORT_WARNINGS,
    }


def _query_spec(request: PoseReviewDatasetExportRequest) -> dict[str, Any]:
    return {
        "pose_observation_ids": request.pose_observation_ids,
        "query": request.query.model_dump(exclude_none=True) if request.query else None,
        "run_id": request.run_id,
        "media_id": request.media_id,
        "include_annotations": request.include_annotations,
        "include_artifacts": request.include_artifacts,
        "format": request.format,
        "query_name": request.query_name,
    }


def _export_path(output_root: str | Path, export_id: str, export_format: str) -> Path:
    return (
        Path(output_root).expanduser().resolve()
        / "pose"
        / export_id
        / f"pose_review_dataset.{export_format}"
    )


def _persist_export_artifact(
    *,
    session: Session,
    request: PoseReviewDatasetExportRequest,
    export_id: str,
    export_path: Path,
    checksum: str,
    pose_observation_ids: list[str],
    bundles: list[dict[str, Any]],
) -> EvidenceArtifact:
    artifact = EvidenceArtifact(
        media_id=_artifact_media_id(bundles),
        run_id=_artifact_run_id(bundles),
        target_observation_id=None,
        artifact_type=EXPORT_ARTIFACT_TYPE,
        uri=export_path.as_uri(),
        frame_start=None,
        frame_end=None,
        timestamp_start_ms=None,
        timestamp_end_ms=None,
        checksum=checksum,
        metadata_jsonb={
            "export_version": EXPORT_VERSION,
            "export_id": export_id,
            "pose_count": len(pose_observation_ids),
            "pose_observation_ids": pose_observation_ids,
            "query_spec": _query_spec(request),
            "include_annotations": request.include_annotations,
            "include_artifacts": request.include_artifacts,
            "format": request.format,
            **EXPORT_WARNINGS,
            "media_scope": _media_scope(bundles),
            "path": str(export_path),
        },
    )
    session.add(artifact)
    session.flush()
    return artifact


def _persist_query_result(
    *,
    session: Session,
    request: PoseReviewDatasetExportRequest,
    pose_observation_ids: list[str],
    bundles: list[dict[str, Any]],
    artifact: EvidenceArtifact,
) -> QueryResult | None:
    if request.query is None and request.run_id is None and request.media_id is None:
        return None
    row = QueryResult(
        query_name=request.query_name or "pose_review_dataset_export",
        query_payload_jsonb=_query_spec(request),
        result_payload_jsonb={
            "pose_observation_ids": pose_observation_ids,
            "result_count": len(pose_observation_ids),
            "result_observation_ids": [
                bundle["pose_observation"]["observation"]["id"] for bundle in bundles
            ],
            "export_artifact_id": artifact.id,
            "export_artifact_uri": artifact.uri,
            **EXPORT_WARNINGS,
        },
        created_by=request.created_by,
    )
    session.add(row)
    session.flush()
    return row


def _artifact_media_id(bundles: list[dict[str, Any]]) -> str:
    media_ids = {
        bundle["media"]["id"]
        for bundle in bundles
        if bundle.get("media") and bundle["media"].get("id")
    }
    if not media_ids:
        raise PoseReviewExportError("export requires at least one media-backed pose")
    return sorted(media_ids)[0]


def _artifact_run_id(bundles: list[dict[str, Any]]) -> str | None:
    run_ids = {
        bundle["run"]["id"] for bundle in bundles if bundle.get("run") and bundle["run"].get("id")
    }
    return next(iter(run_ids)) if len(run_ids) == 1 else None


def _media_scope(bundles: list[dict[str, Any]]) -> str:
    media_ids = {
        bundle["media"]["id"]
        for bundle in bundles
        if bundle.get("media") and bundle["media"].get("id")
    }
    return "single_media" if len(media_ids) == 1 else "multiple_media"


def _annotations(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(
        annotation for bundle in bundles for annotation in bundle.get("annotations", [])
    )


def _artifacts(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(
        artifact for bundle in bundles for artifact in bundle.get("artifacts", [])
    )


def _lineage(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(row for bundle in bundles for row in bundle.get("lineage", []))


def _first_artifact_uri(artifacts: list[dict[str, Any]]) -> str | None:
    for artifact in artifacts:
        uri = artifact.get("uri")
        if isinstance(uri, str) and uri:
            return uri
    return None


def _unique_by_id(items: Any) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for item in items:
        if isinstance(item, dict) and item.get("id"):
            rows[str(item["id"])] = item
    return [rows[key] for key in sorted(rows)]
