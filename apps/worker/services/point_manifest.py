from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    CameraGeometryEvidence,
    EventCandidate3DDiagnostic,
    EventCandidateReviewAnnotation,
    HumanAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
    Trajectory3DDebugReviewAnnotation,
)

POINT_MANIFEST_TYPE = "point_evidence_provenance_manifest"
POINT_MANIFEST_VERSION = "v0"
POINT_MANIFEST_BLUEPRINT = "blueprint_23"
POINT_MANIFEST_BLUEPRINT_NAME = "point_manifest_evidence_provenance_contract_v0"
POINT_MANIFEST_OUTPUT_DIR = ".data/manifests"
TOM_PROJECT_NAME = "tom-v3-simple"
TOM_PROJECT_VERSION = "0.0.0"

EVENT_MARKER_TYPES = {"hit_candidate", "bounce_candidate"}
EVENT_CANDIDATE_OBSERVATION_TYPES = EVENT_MARKER_TYPES | {
    "event_candidate_rejection_diagnostic",
}

POINT_MANIFEST_WARNINGS = {
    "baseline_is_not_truth": True,
    "manifest_is_not_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "not_training_truth": True,
    "not_3d_truth": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_identify_players": True,
    "does_not_determine_winner": True,
    "not_generalization_claim": True,
}


def build_point_manifest(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None = None,
    trajectory_3d_run_id: str | None = None,
    camera_geometry_id: str | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_path: str | Path | None = None,
    output_dir: str | Path = POINT_MANIFEST_OUTPUT_DIR,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build and write a point-level evidence provenance manifest.

    The manifest is a read-only description of evidence already present in TOM. It does not
    generate candidates, reviews, 3D rows, scores, player identities, truth, or adjudication.
    """

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    run_validation = _validate_associated_evidence(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    if run_validation.get("ok") is False:
        return run_validation

    generated_at = generated_at or datetime.now(UTC)
    generated_at_iso = generated_at.isoformat()
    identity_inputs = _identity_inputs(
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    point_manifest_id = deterministic_point_manifest_id(identity_inputs)
    profile_counts = _profile_counts(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    availability = _evidence_availability(profile_counts)
    source = _media_source_payload(media)
    associated_run_ids = _associated_run_ids(
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )

    manifest: dict[str, Any] = {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": POINT_MANIFEST_VERSION,
        "point_manifest_id": point_manifest_id,
        "point_manifest_identity": identity_inputs,
        "media_id": media.id,
        "source_uri": source.get("source_uri"),
        "source_media_path": source.get("source_media_path"),
        "stored_uri": source.get("stored_uri"),
        "stored_path": source.get("stored_path"),
        "replay_url": _replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            event_candidate_run_id=event_candidate_run_id,
            trajectory_3d_run_id=trajectory_3d_run_id,
            camera_geometry_id=camera_geometry_id,
        ),
        "generated_at": generated_at_iso,
        "tom_provenance": {
            "project": TOM_PROJECT_NAME,
            "project_version": TOM_PROJECT_VERSION,
            "blueprint": POINT_MANIFEST_BLUEPRINT,
            "blueprint_name": POINT_MANIFEST_BLUEPRINT_NAME,
        },
        "associated_run_ids": associated_run_ids,
        "evidence_availability": availability,
        "profile_counts": profile_counts,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }

    manifest_path = _manifest_path(
        output_path=output_path,
        output_dir=output_dir,
        point_manifest_id=point_manifest_id,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "ok": True,
        "status": "completed",
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": POINT_MANIFEST_VERSION,
        "point_manifest_id": point_manifest_id,
        "media_id": media.id,
        "associated_run_ids": associated_run_ids,
        "evidence_availability": availability,
        "profile_counts": profile_counts,
        "manifest_output": str(manifest_path),
        "manifest": manifest,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }


def deterministic_point_manifest_id(identity_inputs: dict[str, Any]) -> str:
    identity_json = json.dumps(identity_inputs, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(identity_json.encode("utf-8")).hexdigest()[:24]
    return f"point_manifest_v0_{digest}"


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": POINT_MANIFEST_VERSION,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }


def _validate_associated_evidence(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> dict[str, Any]:
    event_run_error = _validate_run(
        session=session,
        media_id=media_id,
        run_id=event_candidate_run_id,
        missing_status="missing_event_candidate_run",
        mismatch_status="event_candidate_run_media_mismatch",
        label="event candidate run",
    )
    if event_run_error is not None:
        return event_run_error

    trajectory_run_error = _validate_run(
        session=session,
        media_id=media_id,
        run_id=trajectory_3d_run_id,
        missing_status="missing_trajectory_3d_run",
        mismatch_status="trajectory_3d_run_media_mismatch",
        label="trajectory 3D run",
    )
    if trajectory_run_error is not None:
        return trajectory_run_error

    if camera_geometry_id is not None:
        camera_geometry = session.get(CameraGeometryEvidence, camera_geometry_id)
        if camera_geometry is None:
            return _failed(
                "missing_camera_geometry",
                f"camera geometry evidence not found: {camera_geometry_id}",
            )
        if camera_geometry.media_id != media_id:
            return _failed(
                "camera_geometry_media_mismatch",
                (
                    f"camera geometry evidence {camera_geometry_id} does not belong "
                    f"to media {media_id}"
                ),
            )

    return {"ok": True}


def _validate_run(
    *,
    session: Session,
    media_id: str,
    run_id: str | None,
    missing_status: str,
    mismatch_status: str,
    label: str,
) -> dict[str, Any] | None:
    if run_id is None:
        return None
    run = session.get(ProcessingRun, run_id)
    if run is None:
        return _failed(missing_status, f"{label} not found: {run_id}")
    if run.media_id != media_id:
        return _failed(
            mismatch_status,
            f"{label} {run_id} does not belong to media {media_id}",
        )
    return None


def _identity_inputs(
    *,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> dict[str, Any]:
    return {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": POINT_MANIFEST_VERSION,
        "media_id": media_id,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "camera_geometry_id": camera_geometry_id,
    }


def _associated_run_ids(
    *,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> dict[str, str]:
    run_ids: dict[str, str] = {}
    if event_candidate_run_id is not None:
        run_ids["event_candidate_run_id"] = event_candidate_run_id
    if trajectory_3d_run_id is not None:
        run_ids["trajectory_3d_run_id"] = trajectory_3d_run_id
    if camera_geometry_id is not None:
        run_ids["camera_geometry_id"] = camera_geometry_id
    return run_ids


def _media_source_payload(media: MediaAsset) -> dict[str, str | None]:
    metadata = media.metadata_jsonb if isinstance(media.metadata_jsonb, dict) else {}
    return {
        "source_uri": _string_or_none(metadata.get("original_source_uri")) or media.source_uri,
        "source_media_path": _string_or_none(metadata.get("original_source_path")),
        "stored_uri": _string_or_none(metadata.get("stored_uri")) or media.source_uri,
        "stored_path": _string_or_none(metadata.get("stored_path")),
    }


def _profile_counts(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> dict[str, int]:
    event_counts = _event_candidate_observation_counts(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    trajectory_3d_candidate_count = _trajectory_3d_candidate_count(
        session=session,
        media_id=media_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    event_candidate_3d_diagnostic_count = _event_candidate_3d_diagnostic_count(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    event_marker_review_count = _event_marker_review_count(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    trajectory_3d_debug_review_count = _trajectory_3d_debug_review_count(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    human_annotation_count = _human_annotation_count(session=session, media_id=media_id)

    return {
        "event_marker_count": event_counts["hit_candidate_count"]
        + event_counts["bounce_candidate_count"],
        "hit_candidate_count": event_counts["hit_candidate_count"],
        "bounce_candidate_count": event_counts["bounce_candidate_count"],
        "event_candidate_observation_count": event_counts[
            "event_candidate_observation_count"
        ],
        "event_candidate_rejection_diagnostic_count": event_counts[
            "event_candidate_rejection_diagnostic_count"
        ],
        "trajectory_3d_candidate_count": trajectory_3d_candidate_count,
        "event_candidate_3d_diagnostic_count": event_candidate_3d_diagnostic_count,
        "event_marker_review_count": event_marker_review_count,
        "trajectory_3d_debug_review_count": trajectory_3d_debug_review_count,
        "human_annotation_count": human_annotation_count,
        "review_annotation_count": (
            human_annotation_count + event_marker_review_count + trajectory_3d_debug_review_count
        ),
    }


def _event_candidate_observation_counts(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
) -> dict[str, int]:
    query = (
        select(Observation.observation_type, func.count(Observation.id))
        .where(
            Observation.media_id == media_id,
            Observation.observation_type.in_(sorted(EVENT_CANDIDATE_OBSERVATION_TYPES)),
        )
        .group_by(Observation.observation_type)
    )
    if event_candidate_run_id is not None:
        query = query.where(Observation.run_id == event_candidate_run_id)
    rows = session.execute(query).all()
    counts = Counter({observation_type: int(count) for observation_type, count in rows})
    return {
        "hit_candidate_count": counts.get("hit_candidate", 0),
        "bounce_candidate_count": counts.get("bounce_candidate", 0),
        "event_candidate_rejection_diagnostic_count": counts.get(
            "event_candidate_rejection_diagnostic",
            0,
        ),
        "event_candidate_observation_count": sum(counts.values()),
    }


def _trajectory_3d_candidate_count(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> int:
    query = select(func.count(BallTrajectory3DCandidate.id)).where(
        BallTrajectory3DCandidate.media_id == media_id
    )
    if trajectory_3d_run_id is not None:
        query = query.where(BallTrajectory3DCandidate.trajectory_3d_run_id == trajectory_3d_run_id)
    if camera_geometry_id is not None:
        query = query.where(BallTrajectory3DCandidate.camera_geometry_id == camera_geometry_id)
    return int(session.scalar(query) or 0)


def _event_candidate_3d_diagnostic_count(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> int:
    query = select(func.count(EventCandidate3DDiagnostic.id)).where(
        EventCandidate3DDiagnostic.media_id == media_id
    )
    if event_candidate_run_id is not None:
        query = query.where(
            EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id
        )
    if trajectory_3d_run_id is not None:
        query = query.where(
            EventCandidate3DDiagnostic.trajectory_3d_run_id == trajectory_3d_run_id
        )
    if camera_geometry_id is not None:
        query = query.where(EventCandidate3DDiagnostic.camera_geometry_id == camera_geometry_id)
    return int(session.scalar(query) or 0)


def _event_marker_review_count(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
) -> int:
    query = select(func.count(EventCandidateReviewAnnotation.id)).where(
        EventCandidateReviewAnnotation.media_id == media_id
    )
    if event_candidate_run_id is not None:
        query = query.where(
            EventCandidateReviewAnnotation.event_candidate_run_id == event_candidate_run_id
        )
    return int(session.scalar(query) or 0)


def _trajectory_3d_debug_review_count(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> int:
    query = select(func.count(Trajectory3DDebugReviewAnnotation.id)).where(
        Trajectory3DDebugReviewAnnotation.media_id == media_id
    )
    if event_candidate_run_id is not None:
        query = query.where(
            Trajectory3DDebugReviewAnnotation.event_candidate_run_id == event_candidate_run_id
        )
    if trajectory_3d_run_id is not None:
        query = query.where(
            Trajectory3DDebugReviewAnnotation.trajectory_3d_run_id == trajectory_3d_run_id
        )
    if camera_geometry_id is not None:
        query = query.where(
            Trajectory3DDebugReviewAnnotation.camera_geometry_id == camera_geometry_id
        )
    return int(session.scalar(query) or 0)


def _human_annotation_count(*, session: Session, media_id: str) -> int:
    return int(
        session.scalar(
            select(func.count(HumanAnnotation.id)).where(HumanAnnotation.media_id == media_id)
        )
        or 0
    )


def _evidence_availability(profile_counts: dict[str, int]) -> dict[str, bool]:
    return {
        "media_indexed": True,
        "replay_available": True,
        "event_candidates_available": profile_counts["event_marker_count"] > 0,
        "trajectory_3d_candidates_available": profile_counts["trajectory_3d_candidate_count"] > 0,
        "event_candidate_3d_diagnostics_available": (
            profile_counts["event_candidate_3d_diagnostic_count"] > 0
        ),
        "review_annotations_available": profile_counts["review_annotation_count"] > 0,
        "trajectory_3d_debug_reviews_available": (
            profile_counts["trajectory_3d_debug_review_count"] > 0
        ),
    }


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    event_candidate_run_id: str | None,
    trajectory_3d_run_id: str | None,
    camera_geometry_id: str | None,
) -> str:
    params: dict[str, str] = {}
    if event_candidate_run_id is not None:
        params["eventCandidateRunId"] = event_candidate_run_id
    if trajectory_3d_run_id is not None:
        params["trajectory3dRunId"] = trajectory_3d_run_id
    if camera_geometry_id is not None:
        params["cameraGeometryId"] = camera_geometry_id
    query = urlencode(params)
    url = f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
    return f"{url}?{query}" if query else url


def _manifest_path(
    *,
    output_path: str | Path | None,
    output_dir: str | Path,
    point_manifest_id: str,
) -> Path:
    if output_path is not None and str(output_path).strip():
        return Path(output_path).expanduser()
    return Path(output_dir).expanduser() / f"{point_manifest_id}.json"


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
