import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    EventCandidateReviewAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
    RuntimeConfig,
)

from apps.api.services.event_candidate_reviews import (
    build_event_candidate_review_summary,
    serialize_event_candidate_review,
)
from apps.api.services.replay import build_event_candidate_marker_summary

SNAPSHOT_TYPE = "point_evidence_snapshot"
SNAPSHOT_VERSION = "v0"

SNAPSHOT_WARNINGS = {
    "candidate_only": True,
    "event_candidate_only": True,
    "observation_only": True,
    "not_hit_truth": True,
    "not_bounce_truth": True,
    "not_in_out_truth": True,
    "no_score_or_point_truth": True,
    "no_adjudication": True,
}

KNOWN_LIMITATIONS = [
    "Candidate evidence only.",
    "No in/out decision.",
    "No score or point winner.",
    "No accepted/rejected lifecycle.",
    "Marker correctness remains operator-reviewed.",
]

ACTIVE_VERSION_KEYS = {
    "physics_heuristic": "physics_heuristic_version",
    "marker_level_arbitration": "marker_level_arbitration_version",
    "universal_hit_validity_guard": "universal_hit_validity_guard_version",
    "local_evidence_classification": "local_evidence_event_type_classification_version",
    "image_space_direction_change_hit_recall": (
        "image_space_direction_change_hit_recall_version"
    ),
    "image_space_net_axis_hit_recall": "image_space_net_axis_hit_recall_version",
    "net_axis_reversal_hit_recall": "net_axis_reversal_hit_recall_version",
}


def build_point_evidence_snapshot(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Build a durable point evidence snapshot without changing source evidence."""

    if output_format not in {"json", "markdown"}:
        return _failed(
            "unsupported_format",
            f"unsupported point evidence snapshot format: {output_format}",
        )

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    event_run = session.get(ProcessingRun, event_candidate_run_id)
    if event_run is None:
        return _failed(
            "missing_event_candidate_run",
            f"event candidate run not found: {event_candidate_run_id}",
        )
    if event_run.media_id != media.id:
        return _failed(
            "event_candidate_run_media_mismatch",
            f"event candidate run {event_candidate_run_id} does not belong to media {media.id}",
        )

    marker_summary = _compact_marker_summary(
        build_event_candidate_marker_summary(
            session=session,
            media=media,
            event_candidate_run_id=event_candidate_run_id,
        )
    )
    observations = _event_candidate_observation_counts(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
    )
    source_run_ids = _source_run_ids(session=session, event_run=event_run)
    candidate_summary = _candidate_summary(event_run)
    review_rows = _event_candidate_review_rows(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
    )

    snapshot: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "snapshot_type": SNAPSHOT_TYPE,
        "snapshot_version": SNAPSHOT_VERSION,
        "media_id": media.id,
        "event_candidate_run_id": event_candidate_run_id,
        "source_run_ids": source_run_ids,
        "replay_url": _replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            source_run_ids=source_run_ids,
            event_candidate_run_id=event_candidate_run_id,
        ),
        "observations": observations,
        "active_versions": _active_versions(candidate_summary),
        "marker_summary": marker_summary,
        "review_summary": build_event_candidate_review_summary(review_rows),
        "review_annotations": _compact_review_annotations(review_rows),
        "warnings": dict(SNAPSHOT_WARNINGS),
        "known_limitations": list(KNOWN_LIMITATIONS),
    }

    if output_format == "markdown":
        snapshot["markdown"] = render_point_evidence_snapshot_markdown(snapshot)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(snapshot["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")
        snapshot["output_path"] = str(path)

    return snapshot


def render_point_evidence_snapshot_markdown(snapshot: dict[str, Any]) -> str:
    rows = [
        "# Point Evidence Snapshot v0",
        "",
        f"Media ID: `{snapshot.get('media_id')}`  ",
        f"Event Candidate Run ID: `{snapshot.get('event_candidate_run_id')}`  ",
        f"Replay URL: `{snapshot.get('replay_url')}`",
        "",
        "## Final Markers",
        "",
        "| # | Type | Frame | Time ms | Confidence | Source | Decision |",
        "|---|------|-------|---------|------------|--------|----------|",
    ]
    marker_summary = snapshot.get("marker_summary")
    if isinstance(marker_summary, list) and marker_summary:
        for marker in marker_summary:
            if not isinstance(marker, dict):
                continue
            marker_type = "HIT" if marker.get("candidate_type") == "hit_candidate" else "BOUNCE"
            rows.append(
                (
                    "| {index} | {marker_type} | {frame} | {timestamp_ms} | "
                    "{confidence} | {source} | {decision} |"
                ).format(
                    index=marker.get("index", "n/a"),
                    marker_type=marker_type,
                    frame=marker.get("frame", "n/a"),
                    timestamp_ms=marker.get("timestamp_ms", "n/a"),
                    confidence=_format_markdown_confidence(marker.get("confidence")),
                    source=str(marker.get("source_method") or "n/a"),
                    decision=str(marker.get("arbitration_decision") or "n/a"),
                )
            )
    else:
        rows.append("| n/a | n/a | n/a | n/a | n/a | n/a | n/a |")

    rows.extend(["", "## Operator Reviews"])
    review_summary = snapshot.get("review_summary")
    if isinstance(review_summary, dict):
        rows.append(f"- total_reviews: {review_summary.get('total_reviews', 0)}")
        rows.append(f"- useful: {review_summary.get('useful', 0)}")
        rows.append(f"- wrong: {review_summary.get('wrong', 0)}")
        rows.append(f"- unclear: {review_summary.get('unclear', 0)}")
        rows.append(f"- needs_review: {review_summary.get('needs_review', 0)}")
        rows.append(
            f"- missing_candidate_note: {review_summary.get('missing_candidate_note', 0)}"
        )
    else:
        rows.append("- total_reviews: 0")

    rows.extend(["", "## Active Versions"])
    active_versions = snapshot.get("active_versions")
    if isinstance(active_versions, dict) and active_versions:
        for key, value in active_versions.items():
            rows.append(f"- {key}: {value}")
    else:
        rows.append("- n/a")

    rows.extend(["", "## Warnings"])
    for warning in KNOWN_LIMITATIONS:
        rows.append(f"- {warning}")
    rows.extend(
        [
            "- Not hit truth.",
            "- Not bounce truth.",
            "- Not in/out.",
            "- No score or point truth.",
            "- No adjudication.",
        ]
    )
    return "\n".join(rows) + "\n"


def _event_candidate_observation_counts(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> dict[str, int]:
    rows = session.execute(
        select(Observation.observation_type, func.count(Observation.id))
        .where(
            Observation.media_id == media_id,
            Observation.run_id == event_candidate_run_id,
        )
        .group_by(Observation.observation_type)
    ).all()
    counts = Counter({observation_type: int(count) for observation_type, count in rows})
    return {
        "hit_candidate": counts.get("hit_candidate", 0),
        "bounce_candidate": counts.get("bounce_candidate", 0),
        "event_candidate_rejection_diagnostic": counts.get(
            "event_candidate_rejection_diagnostic",
            0,
        ),
        "total": sum(counts.values()),
    }


def _event_candidate_review_rows(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> list[EventCandidateReviewAnnotation]:
    return list(
        session.scalars(
            select(EventCandidateReviewAnnotation)
            .where(
                EventCandidateReviewAnnotation.media_id == media_id,
                EventCandidateReviewAnnotation.event_candidate_run_id
                == event_candidate_run_id,
            )
            .order_by(
                EventCandidateReviewAnnotation.created_at,
                EventCandidateReviewAnnotation.id,
            )
        ).all()
    )


def _compact_review_annotations(
    rows: list[EventCandidateReviewAnnotation],
) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for row in rows:
        payload = serialize_event_candidate_review(row)
        created_at = payload.get("created_at")
        compact.append(
            {
                key: (
                    created_at.isoformat()
                    if key == "created_at" and hasattr(created_at, "isoformat")
                    else payload.get(key)
                )
                for key in (
                    "id",
                    "observation_id",
                    "annotation_kind",
                    "review_label",
                    "candidate_type",
                    "frame",
                    "timestamp_ms",
                    "image_x",
                    "image_y",
                    "court_x",
                    "court_y",
                    "note",
                    "reviewer",
                    "created_at",
                )
                if payload.get(key) is not None
            }
        )
    return compact


def _compact_marker_summary(marker_summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        marker
        for marker in marker_summary
        if marker.get("candidate_type") in {"hit_candidate", "bounce_candidate"}
    ]
    rows.sort(
        key=lambda marker: (
            marker.get("timestamp_ms") if marker.get("timestamp_ms") is not None else -1,
            marker.get("frame") if marker.get("frame") is not None else -1,
            str(marker.get("candidate_type") or ""),
            str(marker.get("observation_id") or ""),
        )
    )
    compact_rows: list[dict[str, Any]] = []
    for index, marker in enumerate(rows, start=1):
        compact_marker: dict[str, Any] = {
            "index": index,
            "candidate_type": marker.get("candidate_type"),
            "frame": marker.get("frame"),
            "timestamp_ms": marker.get("timestamp_ms"),
        }
        for key in (
            "source_method",
            "arbitration_decision",
            "arbitration_reason",
            "confidence",
            "court_x",
            "court_y",
            "image_x",
            "image_y",
        ):
            value = marker.get(key)
            if value is not None:
                compact_marker[key] = value
        compact_rows.append(compact_marker)
    return compact_rows


def _source_run_ids(*, session: Session, event_run: ProcessingRun) -> dict[str, str]:
    source_run_ids: dict[str, str] = {}
    event_payload = _run_payload(session=session, run=event_run)
    _set_if_present(
        source_run_ids,
        "ball_trajectory_run_id",
        _string_or_none(event_payload.get("source_ball_trajectory_run_id")),
    )
    _set_if_present(
        source_run_ids,
        "court_projection_run_id",
        _string_or_none(event_payload.get("source_court_projection_run_id")),
    )

    court_projection_run_id = source_run_ids.get("court_projection_run_id")
    if court_projection_run_id is not None:
        court_projection_run = session.get(ProcessingRun, court_projection_run_id)
        if court_projection_run is not None:
            court_projection_payload = _run_payload(session=session, run=court_projection_run)
            _set_if_present(
                source_run_ids,
                "motion_smoothing_run_id",
                _string_or_none(
                    court_projection_payload.get("source_motion_smoothing_run_id")
                ),
            )
            _set_if_present(
                source_run_ids,
                "homography_run_id",
                _string_or_none(court_projection_payload.get("source_homography_run_id")),
            )

    homography_run_id = source_run_ids.get("homography_run_id")
    if homography_run_id is not None:
        homography_run = session.get(ProcessingRun, homography_run_id)
        if homography_run is not None:
            homography_payload = _run_payload(session=session, run=homography_run)
            _set_if_present(
                source_run_ids,
                "court_run_id",
                _string_or_none(homography_payload.get("source_court_run_id")),
            )

    return source_run_ids


def _run_payload(*, session: Session, run: ProcessingRun) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if isinstance(run.metadata_jsonb, dict):
        payload.update(run.metadata_jsonb)
    if run.runtime_config_id is not None:
        runtime_config = session.get(RuntimeConfig, run.runtime_config_id)
        if runtime_config is not None and isinstance(runtime_config.payload_jsonb, dict):
            payload.update(runtime_config.payload_jsonb)
    return payload


def _candidate_summary(event_run: ProcessingRun) -> dict[str, Any]:
    metadata = event_run.metadata_jsonb if isinstance(event_run.metadata_jsonb, dict) else {}
    candidate_summary = metadata.get("candidate_summary")
    if isinstance(candidate_summary, dict):
        return candidate_summary
    return metadata


def _active_versions(candidate_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        label: candidate_summary[source_key]
        for label, source_key in ACTIVE_VERSION_KEYS.items()
        if candidate_summary.get(source_key) is not None
    }


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    source_run_ids: dict[str, str],
    event_candidate_run_id: str,
) -> str:
    params: dict[str, str] = {}
    if source_run_ids.get("motion_smoothing_run_id") is not None:
        params["motionSmoothingRunId"] = source_run_ids["motion_smoothing_run_id"]
    if source_run_ids.get("court_run_id") is not None:
        params["courtRunId"] = source_run_ids["court_run_id"]
    if source_run_ids.get("court_projection_run_id") is not None:
        params["courtProjectionRunId"] = source_run_ids["court_projection_run_id"]
    if source_run_ids.get("ball_trajectory_run_id") is not None:
        params["ballTrajectoryRunId"] = source_run_ids["ball_trajectory_run_id"]
    params["eventCandidateRunId"] = event_candidate_run_id
    if source_run_ids.get("court_run_id") is not None:
        params["courtTemporalPersistence"] = "carry_forward"
        params["courtPersistenceMaxGapMs"] = "1500"
    return f"{viewer_base_url.rstrip('/')}/replay/{media_id}?{urlencode(params)}"


def _set_if_present(target: dict[str, str], key: str, value: str | None) -> None:
    if value is not None:
        target[key] = value


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _format_markdown_confidence(value: object) -> str:
    if isinstance(value, int | float):
        return f"{float(value):.3f}"
    return "n/a"


def _failed(status: str, message: str) -> dict[str, Any]:
    return {"ok": False, "status": status, "message": message}
