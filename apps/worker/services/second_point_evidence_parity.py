from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    EventCandidateReviewAnnotation,
    HumanAnnotation,
    Observation,
    Trajectory3DDebugReviewAnnotation,
)

from apps.worker.services.second_point_smoke import run_second_point_ingestion_smoke

SECOND_POINT_PARITY_TYPE = "second_point_evidence_parity_baseline"
SECOND_POINT_PARITY_VERSION = "v0"
SECOND_POINT_PARITY_BASELINE_NAME = "second_point_evidence_parity_baseline_v0"
SECOND_POINT_PARITY_MANIFEST_TYPE = "second_point_evidence_parity_baseline_manifest"
DEFAULT_SECOND_POINT_PARITY_MANIFEST = (
    ".data/baselines/second_point_evidence_parity.baseline_manifest.json"
)


def build_second_point_evidence_parity(
    *,
    session: Session,
    media_path: str | None,
    run_name: str = "second-point-evidence-parity-v0",
    viewer_base_url: str = "http://127.0.0.1:3000",
    storage_root: str | Path = ".data/media",
    copy_to_storage: bool = True,
    baseline_manifest_output: str | Path = DEFAULT_SECOND_POINT_PARITY_MANIFEST,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    """Index one second-point media asset and write an evidence-parity manifest.

    This orchestrates existing media/replay evidence plumbing only. It does not run
    candidate generation, 3D generation, review creation, truth, scoring, or adjudication.
    """

    warnings = _warnings()
    smoke = run_second_point_ingestion_smoke(
        session=session,
        media_path=media_path,
        run_name=run_name,
        viewer_base_url=viewer_base_url,
        storage_root=storage_root,
        copy_to_storage=copy_to_storage,
        probe_runner=probe_runner,
    )
    if smoke.get("ok") is False:
        return {
            "ok": False,
            "status": smoke.get("status", "second_point_evidence_parity_failed"),
            "message": smoke.get("message", "second point evidence parity failed"),
            "parity_type": SECOND_POINT_PARITY_TYPE,
            "parity_version": SECOND_POINT_PARITY_VERSION,
            "source_media_path": smoke.get("source_media_path"),
            "warnings": warnings,
        }

    media_id = str(smoke["media_id"])
    profile = _second_point_profile(session, media_id)
    manifest_path = Path(baseline_manifest_output).expanduser()
    manifest = _build_manifest(
        media_id=media_id,
        source_media_path=str(smoke["source_media_path"]),
        replay_url=str(smoke["replay_url"]),
        profile=profile,
        warnings=warnings,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    profile["baseline_available"] = True
    return {
        "ok": True,
        "status": "completed",
        "parity_type": SECOND_POINT_PARITY_TYPE,
        "parity_version": SECOND_POINT_PARITY_VERSION,
        "run_name": run_name,
        "media_id": media_id,
        "source_media_path": smoke["source_media_path"],
        "source_uri": smoke.get("source_uri"),
        "stored_uri": smoke.get("stored_uri"),
        "stored_path": smoke.get("stored_path"),
        "storage_mode": smoke.get("storage_mode"),
        "checksum": smoke.get("checksum"),
        "media_metadata": smoke.get("media_metadata", {}),
        "replay_url": smoke["replay_url"],
        "second_point_profile": profile,
        "baseline_manifest_output": str(manifest_path),
        "manifest": manifest,
        "warnings": warnings,
    }


def _second_point_profile(session: Session, media_id: str) -> dict[str, Any]:
    event_candidate_count = _observation_count(
        session,
        media_id,
        {"hit_candidate", "bounce_candidate"},
    )
    trajectory_3d_count = int(
        session.scalar(
            select(func.count(BallTrajectory3DCandidate.id)).where(
                BallTrajectory3DCandidate.media_id == media_id
            )
        )
        or 0
    )
    human_review_count = int(
        session.scalar(
            select(func.count(HumanAnnotation.id)).where(HumanAnnotation.media_id == media_id)
        )
        or 0
    )
    event_review_count = int(
        session.scalar(
            select(func.count(EventCandidateReviewAnnotation.id)).where(
                EventCandidateReviewAnnotation.media_id == media_id
            )
        )
        or 0
    )
    trajectory_review_count = int(
        session.scalar(
            select(func.count(Trajectory3DDebugReviewAnnotation.id)).where(
                Trajectory3DDebugReviewAnnotation.media_id == media_id
            )
        )
        or 0
    )
    review_annotation_count = human_review_count + event_review_count + trajectory_review_count

    return {
        "media_indexed": True,
        "replay_available": True,
        "event_candidates_available": event_candidate_count > 0,
        "trajectory_3d_candidates_available": trajectory_3d_count > 0,
        "review_annotations_available": review_annotation_count > 0,
        "baseline_available": False,
        "counts": {
            "event_candidate_observation_count": event_candidate_count,
            "trajectory_3d_candidate_count": trajectory_3d_count,
            "review_annotation_count": review_annotation_count,
            "human_annotation_count": human_review_count,
            "event_candidate_review_annotation_count": event_review_count,
            "trajectory_3d_debug_review_annotation_count": trajectory_review_count,
        },
    }


def _observation_count(session: Session, media_id: str, observation_types: set[str]) -> int:
    return int(
        session.scalar(
            select(func.count(Observation.id)).where(
                Observation.media_id == media_id,
                Observation.observation_type.in_(sorted(observation_types)),
            )
        )
        or 0
    )


def _build_manifest(
    *,
    media_id: str,
    source_media_path: str,
    replay_url: str,
    profile: dict[str, Any],
    warnings: dict[str, bool],
) -> dict[str, Any]:
    manifest_profile = dict(profile)
    manifest_profile["baseline_available"] = True
    return {
        "manifest_type": SECOND_POINT_PARITY_MANIFEST_TYPE,
        "manifest_version": SECOND_POINT_PARITY_VERSION,
        "baseline_name": SECOND_POINT_PARITY_BASELINE_NAME,
        "media_id": media_id,
        "source_media_path": source_media_path,
        "replay_url": replay_url,
        "profile": manifest_profile,
        "warnings": {
            "baseline_is_not_truth": True,
            **warnings,
        },
    }


def _warnings() -> dict[str, bool]:
    return {
        "second_point_evidence_parity_only": True,
        "candidate_only": True,
        "observation_only": True,
        "not_truth": True,
        "not_generalization_claim": True,
        "does_not_change_sample_point": True,
        "does_not_create_in_out": True,
        "does_not_create_score": True,
        "no_adjudication": True,
    }
