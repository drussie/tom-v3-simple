from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    TrackletReviewDatasetExportRequest,
    TrackletReviewDatasetExportResponse,
)
from tom_v3_schema.ids import new_uuid
from tom_v3_storage.db_models import EvidenceArtifact, QueryResult
from tom_v3_storage.local_media import calculate_sha256

from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.api.services.tracklet_query import query_tracklets

EXPORT_VERSION = "tracklet_review_dataset_v0"
EXPORT_ARTIFACT_TYPE = "tracklet_review_dataset_export"
EXPORT_WARNINGS = {
    "candidate_evidence_only": True,
    "annotations_are_reviews_not_truth": True,
    "no_adjudication": True,
}


class TrackletReviewExportError(ValueError):
    pass


def export_tracklet_review_dataset(
    session: Session,
    request: TrackletReviewDatasetExportRequest,
) -> TrackletReviewDatasetExportResponse:
    tracklet_ids = _selected_tracklet_ids(session, request)
    if not tracklet_ids:
        raise TrackletReviewExportError("no tracklets matched export request")

    bundles = [_bundle_or_raise(session, tracklet_id) for tracklet_id in tracklet_ids]
    export_id = new_uuid()
    export_payload = _export_payload(
        export_id=export_id,
        request=request,
        tracklet_ids=tracklet_ids,
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
        tracklet_ids=tracklet_ids,
        bundles=bundles,
    )
    query_result = _persist_query_result(
        session=session,
        request=request,
        tracklet_ids=tracklet_ids,
        bundles=bundles,
        artifact=artifact,
    )
    session.commit()
    session.refresh(artifact)
    if query_result is not None:
        session.refresh(query_result)

    return TrackletReviewDatasetExportResponse(
        export_id=export_id,
        artifact_id=artifact.id,
        uri=artifact.uri,
        path=str(export_path),
        checksum=checksum,
        tracklet_count=len(tracklet_ids),
        tracklet_ids=tracklet_ids,
        query_result_id=query_result.id if query_result is not None else None,
        warnings=EXPORT_WARNINGS,
        metadata=artifact.metadata_jsonb,
    )


def _selected_tracklet_ids(
    session: Session,
    request: TrackletReviewDatasetExportRequest,
) -> list[str]:
    ids = list(dict.fromkeys(request.tracklet_ids))
    if request.query is not None:
        query_result = query_tracklets(session, request.query)
        ids.extend(row.tracklet["id"] for row in query_result.tracklets)
    return sorted(set(ids))


def _bundle_or_raise(session: Session, tracklet_id: str) -> dict[str, Any]:
    bundle = build_tracklet_evidence_bundle(session, tracklet_id)
    if bundle is None:
        raise TrackletReviewExportError(f"tracklet not found: {tracklet_id}")
    return bundle


def _export_payload(
    export_id: str,
    request: TrackletReviewDatasetExportRequest,
    tracklet_ids: list[str],
    bundles: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_bundles = [
        _bundle_for_export(
            bundle=bundle,
            include_frame_artifacts=request.include_frame_artifacts,
            include_annotations=request.include_annotations,
        )
        for bundle in bundles
    ]
    return {
        "tracklet_review_dataset_export": {
            "export_version": EXPORT_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "export_id": export_id,
            "query_spec": _query_spec(request),
            "selection": {
                "tracklet_ids": tracklet_ids,
                "tracklet_count": len(tracklet_ids),
            },
            "warnings": EXPORT_WARNINGS,
            "media": _unique_by_id(
                bundle.get("media") for bundle in selected_bundles if bundle.get("media")
            ),
            "runs": _runs(selected_bundles),
            "runtime_configs": _runtime_configs(selected_bundles),
            "models": _models(selected_bundles),
            "tracklets": selected_bundles,
            "annotations": _annotations(selected_bundles),
            "artifacts": _artifacts(selected_bundles),
            "lineage": _lineage(selected_bundles),
            "provenance": {
                "generated_by": request.created_by or "tom-v3-worker",
                "repo_milestone": "2D",
                "blueprint": "Blueprint 2 - Temporal Evidence Tracklet Candidate System",
                "no_adjudication": True,
            },
        }
    }


def _bundle_for_export(
    bundle: dict[str, Any],
    include_frame_artifacts: bool,
    include_annotations: bool,
) -> dict[str, Any]:
    exported = json.loads(json.dumps(bundle))
    if not include_frame_artifacts:
        exported["frame_artifacts"] = []
        for point in exported.get("track_points", []):
            point["frame_artifacts"] = []
        for source_detection in exported.get("source_detections", []):
            source_detection["frame_artifacts"] = []
    if not include_annotations:
        exported["annotations"] = []
        exported["annotation_summary"] = {}
        exported["tracklet"]["annotations"] = []
        exported["tracklet"]["annotation_summary"] = {}
        for point in exported.get("track_points", []):
            point["annotations"] = []
            point["annotation_summary"] = {}
        for source_detection in exported.get("source_detections", []):
            source_detection["annotations"] = []
            source_detection["annotation_summary"] = {}
    return exported


def _query_spec(request: TrackletReviewDatasetExportRequest) -> dict[str, Any]:
    return {
        "tracklet_ids": request.tracklet_ids,
        "query": request.query.model_dump(exclude_none=True) if request.query else None,
        "include_frame_artifacts": request.include_frame_artifacts,
        "include_annotations": request.include_annotations,
        "format": request.format,
        "query_name": request.query_name,
    }


def _export_path(output_root: str | Path, export_id: str, export_format: str) -> Path:
    return (
        Path(output_root).expanduser().resolve()
        / "tracklets"
        / export_id
        / f"tracklet_review_dataset.{export_format}"
    )


def _persist_export_artifact(
    session: Session,
    request: TrackletReviewDatasetExportRequest,
    export_id: str,
    export_path: Path,
    checksum: str,
    tracklet_ids: list[str],
    bundles: list[dict[str, Any]],
) -> EvidenceArtifact:
    media_id = _artifact_media_id(bundles)
    run_id = _artifact_run_id(bundles)
    artifact = EvidenceArtifact(
        media_id=media_id,
        run_id=run_id,
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
            "tracklet_count": len(tracklet_ids),
            "tracklet_ids": tracklet_ids,
            "query_spec": _query_spec(request),
            "include_frame_artifacts": request.include_frame_artifacts,
            "include_annotations": request.include_annotations,
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
    session: Session,
    request: TrackletReviewDatasetExportRequest,
    tracklet_ids: list[str],
    bundles: list[dict[str, Any]],
    artifact: EvidenceArtifact,
) -> QueryResult | None:
    if request.query is None:
        return None
    result_observation_ids = [
        bundle["tracklet"]["observation"]["id"]
        for bundle in bundles
        if bundle.get("tracklet", {}).get("observation")
    ]
    row = QueryResult(
        query_name=request.query_name or "tracklet_review_dataset_export",
        query_payload_jsonb=_query_spec(request),
        result_payload_jsonb={
            "tracklet_ids": tracklet_ids,
            "result_count": len(tracklet_ids),
            "result_observation_ids": result_observation_ids,
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
        raise TrackletReviewExportError("export requires at least one media-backed tracklet")
    return sorted(media_ids)[0]


def _artifact_run_id(bundles: list[dict[str, Any]]) -> str | None:
    run_ids = {
        bundle["runs"]["tracklet_run"]["id"]
        for bundle in bundles
        if bundle.get("runs", {}).get("tracklet_run")
    }
    return next(iter(run_ids)) if len(run_ids) == 1 else None


def _media_scope(bundles: list[dict[str, Any]]) -> str:
    media_ids = {
        bundle["media"]["id"]
        for bundle in bundles
        if bundle.get("media") and bundle["media"].get("id")
    }
    return "single_media" if len(media_ids) == 1 else "multiple_media"


def _runs(bundles: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        "tracklet_runs": _unique_by_id(
            bundle["runs"]["tracklet_run"]
            for bundle in bundles
            if bundle.get("runs", {}).get("tracklet_run")
        ),
        "source_detection_runs": _unique_by_id(
            bundle["runs"]["source_detection_run"]
            for bundle in bundles
            if bundle.get("runs", {}).get("source_detection_run")
        ),
    }


def _runtime_configs(bundles: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        "tracklet_runtime_configs": _unique_by_id(
            bundle["runtime_configs"]["tracklet_runtime_config"]
            for bundle in bundles
            if bundle.get("runtime_configs", {}).get("tracklet_runtime_config")
        ),
        "source_detection_runtime_configs": _unique_by_id(
            bundle["runtime_configs"]["source_detection_runtime_config"]
            for bundle in bundles
            if bundle.get("runtime_configs", {}).get("source_detection_runtime_config")
        ),
    }


def _models(bundles: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        "tracklet_builder_models": _unique_by_id(
            bundle["model_registry"]["tracklet_builder_model"]
            for bundle in bundles
            if bundle.get("model_registry", {}).get("tracklet_builder_model")
        ),
        "source_detection_models": _unique_by_id(
            bundle["model_registry"]["source_detection_model"]
            for bundle in bundles
            if bundle.get("model_registry", {}).get("source_detection_model")
        ),
    }


def _annotations(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(
        annotation for bundle in bundles for annotation in bundle.get("annotations", [])
    )


def _artifacts(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(
        artifact for bundle in bundles for artifact in bundle.get("frame_artifacts", [])
    )


def _lineage(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _unique_by_id(row for bundle in bundles for row in bundle.get("lineage", []))


def _unique_by_id(items: Any) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for item in items:
        if isinstance(item, dict) and item.get("id"):
            rows[str(item["id"])] = item
    return [rows[key] for key in sorted(rows)]
