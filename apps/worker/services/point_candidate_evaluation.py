import json
from collections import Counter
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    EventCandidateReviewAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.api.services.event_candidate_reviews import serialize_event_candidate_review
from apps.api.services.replay import build_event_candidate_marker_summary
from apps.worker.services.point_evidence_snapshot import build_point_evidence_snapshot

EVALUATION_TYPE = "point_candidate_review_evaluation"
EVALUATION_VERSION = "v0"

EVALUATION_WARNINGS = {
    "candidate_only": True,
    "review_metadata_only": True,
    "operator_reviewed_only": True,
    "not_truth": True,
    "no_adjudication": True,
    "not_in_out": True,
    "no_score_or_point_truth": True,
    "benchmark_metrics_unsupported": True,
}

CANDIDATE_REVIEW_LABELS = ("useful", "wrong", "unclear", "needs_review")
MISSING_REVIEW_LABELS = (
    "missing_hit_candidate",
    "missing_bounce_candidate",
    "missing_event_candidate",
)
CANDIDATE_TYPES = ("hit_candidate", "bounce_candidate")


def evaluate_point_candidates(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Summarize generated event candidates and operator review metadata."""

    if output_format not in {"json", "markdown"}:
        return _failed(
            "unsupported_format",
            f"unsupported point candidate evaluation format: {output_format}",
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

    point_snapshot = build_point_evidence_snapshot(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        viewer_base_url=viewer_base_url,
    )
    if point_snapshot.get("ok") is not True:
        return point_snapshot

    marker_summary = build_event_candidate_marker_summary(
        session=session,
        media=media,
        event_candidate_run_id=event_candidate_run_id,
    )
    review_rows = _event_candidate_review_rows(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
    )
    candidate_counts = _candidate_counts(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        final_marker_count=len(marker_summary),
    )
    latest_marker_reviews = _latest_candidate_marker_reviews_by_observation(review_rows)
    final_marker_ids = {
        marker["observation_id"]
        for marker in marker_summary
        if isinstance(marker.get("observation_id"), str)
    }
    reviewed_final_marker_ids = sorted(final_marker_ids & set(latest_marker_reviews))
    reviewed_final_markers = len(reviewed_final_marker_ids)
    unreviewed_final_markers = max(0, len(final_marker_ids) - reviewed_final_markers)
    review_coverage = {
        "reviewed_final_markers": reviewed_final_markers,
        "unreviewed_final_markers": unreviewed_final_markers,
        "reviewed_marker_fraction": _fraction(reviewed_final_markers, len(final_marker_ids)),
    }
    reviewed_only_rates = _reviewed_only_rates(
        [latest_marker_reviews[observation_id] for observation_id in reviewed_final_marker_ids]
    )
    evaluation = {
        "ok": True,
        "status": "completed",
        "evaluation_type": EVALUATION_TYPE,
        "evaluation_version": EVALUATION_VERSION,
        "media_id": media.id,
        "event_candidate_run_id": event_candidate_run_id,
        "replay_url": point_snapshot.get("replay_url"),
        "candidate_counts": candidate_counts,
        "review_summary": _review_summary(review_rows),
        "review_coverage": review_coverage,
        "reviewed_only_rates": reviewed_only_rates,
        "geometry_readiness": _geometry_readiness(point_snapshot),
        "candidate_type_breakdown": _candidate_type_breakdown(
            marker_summary,
            latest_marker_reviews,
        ),
        "marker_evaluation_summary": _marker_evaluation_summary(
            marker_summary,
            latest_marker_reviews,
        ),
        "missing_candidate_notes": _missing_candidate_notes(review_rows),
        "warnings": _warnings(reviewed_final_markers),
        "known_limitations": [
            "Operator review metadata is review-only and not adjudicated reference data.",
            "Reviewed-only rates are not dataset-level benchmark metrics.",
            "Missing-candidate notes are review metadata only.",
            "No in/out, score, point state, or adjudication is created.",
        ],
    }

    if output_format == "markdown":
        evaluation["markdown"] = render_point_candidate_evaluation_markdown(evaluation)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(evaluation["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(evaluation, indent=2, sort_keys=True), encoding="utf-8")
        evaluation["output_path"] = str(path)

    return evaluation


def render_point_candidate_evaluation_markdown(evaluation: dict[str, Any]) -> str:
    candidate_counts = _dict_or_empty(evaluation.get("candidate_counts"))
    review_summary = _dict_or_empty(evaluation.get("review_summary"))
    review_coverage = _dict_or_empty(evaluation.get("review_coverage"))
    candidate_type_breakdown = _dict_or_empty(evaluation.get("candidate_type_breakdown"))
    reviewed_markers = evaluation.get("marker_evaluation_summary")
    missing_notes = evaluation.get("missing_candidate_notes")

    rows = [
        "# Point Candidate Review Evaluation v0",
        "",
        f"Media ID: `{evaluation.get('media_id')}`  ",
        f"Event Candidate Run ID: `{evaluation.get('event_candidate_run_id')}`  ",
        f"Replay URL: `{evaluation.get('replay_url')}`",
        "",
        "## Candidate Counts",
        "",
        "| Type | Count |",
        "|---|---:|",
        f"| Hit candidates | {candidate_counts.get('hit_candidate', 0)} |",
        f"| Bounce candidates | {candidate_counts.get('bounce_candidate', 0)} |",
        f"| Final markers | {candidate_counts.get('final_marker_count', 0)} |",
        (
            "| Rejection diagnostics | "
            f"{candidate_counts.get('event_candidate_rejection_diagnostic', 0)} |"
        ),
        f"| Total observations | {candidate_counts.get('total_observations', 0)} |",
        "",
        "## Review Summary",
        "",
        "| Label | Count |",
        "|---|---:|",
        f"| Useful | {review_summary.get('useful', 0)} |",
        f"| Wrong | {review_summary.get('wrong', 0)} |",
        f"| Unclear | {review_summary.get('unclear', 0)} |",
        f"| Needs review | {review_summary.get('needs_review', 0)} |",
        f"| Missing notes | {review_summary.get('missing_candidate_notes', 0)} |",
        "",
        "## Review Coverage",
        "",
        (
            "Reviewed final markers: "
            f"{review_coverage.get('reviewed_final_markers', 0)} / "
            f"{candidate_counts.get('final_marker_count', 0)}  "
        ),
        f"Reviewed marker fraction: {review_coverage.get('reviewed_marker_fraction', 0)}",
        "",
        "## Candidate-Type Breakdown",
        "",
        "| Type | Final Markers | Reviewed | Useful | Wrong | Unclear | Needs Review |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for candidate_type, label in (("hit_candidate", "Hit"), ("bounce_candidate", "Bounce")):
        breakdown = _dict_or_empty(candidate_type_breakdown.get(candidate_type))
        rows.append(
            f"| {label} | {breakdown.get('final_markers', 0)} | "
            f"{breakdown.get('reviewed', 0)} | {breakdown.get('useful', 0)} | "
            f"{breakdown.get('wrong', 0)} | {breakdown.get('unclear', 0)} | "
            f"{breakdown.get('needs_review', 0)} |"
        )

    rows.extend(
        [
            "",
            "## Reviewed Markers",
            "",
            "| # | Type | Frame | Time ms | Label | Note |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    if isinstance(reviewed_markers, list) and reviewed_markers:
        for marker in reviewed_markers:
            if not isinstance(marker, dict):
                continue
            rows.append(
                f"| {marker.get('index', 'n/a')} | "
                f"{_candidate_type_label(marker.get('candidate_type'))} | "
                f"{marker.get('frame', 'n/a')} | {marker.get('timestamp_ms', 'n/a')} | "
                f"{marker.get('review_label', 'n/a')} | "
                f"{_markdown_cell(marker.get('review_note'))} |"
            )
    else:
        rows.append("| n/a | n/a | n/a | n/a | n/a | n/a |")

    rows.extend(["", "## Missing Candidate Notes"])
    if isinstance(missing_notes, list) and missing_notes:
        for note in missing_notes:
            if isinstance(note, dict):
                rows.append(
                    f"- {note.get('review_label', 'missing_event_candidate')} at "
                    f"frame {note.get('frame', 'n/a')} / "
                    f"{note.get('timestamp_ms', 'n/a')} ms: "
                    f"{_markdown_cell(note.get('review_note'))}"
                )
    else:
        rows.append("- none")

    rows.extend(["", "## Geometry Readiness"])
    geometry_readiness = _dict_or_empty(evaluation.get("geometry_readiness"))
    rows.append(
        f"- camera_geometry_available: "
        f"{geometry_readiness.get('camera_geometry_available', False)}"
    )
    rows.append(
        f"- court_plane_geometry_declared: "
        f"{geometry_readiness.get('court_plane_geometry_declared', False)}"
    )
    rows.append(
        "- true_3d_reconstruction_available: "
        f"{geometry_readiness.get('true_3d_reconstruction_available', False)}"
    )
    rows.append(
        "- 3d_ball_trajectory_available: "
        f"{geometry_readiness.get('3d_ball_trajectory_available', False)}"
    )

    rows.extend(
        [
            "",
            "## Boundary",
            "",
            "This is candidate evidence review metadata only.  ",
            "It is not truth, not score, not in/out, and not adjudication.",
        ]
    )
    return "\n".join(rows) + "\n"


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


def _candidate_counts(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    final_marker_count: int,
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
        "final_marker_count": final_marker_count,
        "event_candidate_rejection_diagnostic": counts.get(
            "event_candidate_rejection_diagnostic",
            0,
        ),
        "total_observations": sum(counts.values()),
    }


def _review_summary(rows: list[EventCandidateReviewAnnotation]) -> dict[str, int]:
    labels = Counter(row.review_label for row in rows)
    return {
        "total_reviews": len(rows),
        "candidate_marker_reviews": sum(
            1 for row in rows if row.annotation_kind == "candidate_marker_review"
        ),
        "missing_candidate_notes": sum(
            1 for row in rows if row.annotation_kind == "missing_candidate_note"
        ),
        "useful": labels.get("useful", 0),
        "wrong": labels.get("wrong", 0),
        "unclear": labels.get("unclear", 0),
        "needs_review": labels.get("needs_review", 0),
        "missing_hit_candidate": labels.get("missing_hit_candidate", 0),
        "missing_bounce_candidate": labels.get("missing_bounce_candidate", 0),
        "missing_event_candidate": labels.get("missing_event_candidate", 0),
    }


def _latest_candidate_marker_reviews_by_observation(
    rows: list[EventCandidateReviewAnnotation],
) -> dict[str, EventCandidateReviewAnnotation]:
    latest: dict[str, EventCandidateReviewAnnotation] = {}
    for row in rows:
        if row.annotation_kind != "candidate_marker_review" or row.observation_id is None:
            continue
        current = latest.get(row.observation_id)
        if current is None or (row.created_at, row.id) >= (current.created_at, current.id):
            latest[row.observation_id] = row
    return latest


def _reviewed_only_rates(rows: list[EventCandidateReviewAnnotation]) -> dict[str, float | None]:
    denominator = len(rows)
    if denominator == 0:
        return {
            "useful_fraction": None,
            "wrong_fraction": None,
            "unclear_fraction": None,
            "needs_review_fraction": None,
        }
    labels = Counter(row.review_label for row in rows)
    return {
        "useful_fraction": _fraction(labels.get("useful", 0), denominator),
        "wrong_fraction": _fraction(labels.get("wrong", 0), denominator),
        "unclear_fraction": _fraction(labels.get("unclear", 0), denominator),
        "needs_review_fraction": _fraction(labels.get("needs_review", 0), denominator),
    }


def _candidate_type_breakdown(
    marker_summary: list[dict[str, Any]],
    latest_marker_reviews: dict[str, EventCandidateReviewAnnotation],
) -> dict[str, dict[str, int]]:
    breakdown = {
        candidate_type: {
            "final_markers": 0,
            "reviewed": 0,
            "useful": 0,
            "wrong": 0,
            "unclear": 0,
            "needs_review": 0,
        }
        for candidate_type in CANDIDATE_TYPES
    }
    for marker in marker_summary:
        candidate_type = marker.get("candidate_type")
        if candidate_type not in breakdown:
            continue
        entry = breakdown[candidate_type]
        entry["final_markers"] += 1
        observation_id = marker.get("observation_id")
        review = (
            latest_marker_reviews.get(observation_id)
            if isinstance(observation_id, str)
            else None
        )
        if review is None:
            continue
        entry["reviewed"] += 1
        if review.review_label in CANDIDATE_REVIEW_LABELS:
            entry[review.review_label] += 1
    return breakdown


def _marker_evaluation_summary(
    marker_summary: list[dict[str, Any]],
    latest_marker_reviews: dict[str, EventCandidateReviewAnnotation],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for marker in marker_summary:
        observation_id = marker.get("observation_id")
        review = (
            latest_marker_reviews.get(observation_id)
            if isinstance(observation_id, str)
            else None
        )
        if review is None:
            continue
        rows.append(
            {
                "index": marker.get("index"),
                "observation_id": observation_id,
                "candidate_type": marker.get("candidate_type"),
                "frame": marker.get("frame"),
                "timestamp_ms": marker.get("timestamp_ms"),
                "source_method": marker.get("source_method"),
                "review_label": review.review_label,
                "review_note": review.note,
                "review_status": "reviewed",
            }
        )
    return rows


def _missing_candidate_notes(
    rows: list[EventCandidateReviewAnnotation],
) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    for row in rows:
        if row.annotation_kind != "missing_candidate_note":
            continue
        payload = serialize_event_candidate_review(row)
        created_at = payload.get("created_at")
        notes.append(
            {
                "id": row.id,
                "review_label": row.review_label,
                "frame": row.frame,
                "timestamp_ms": row.timestamp_ms,
                "image_x": row.image_x,
                "image_y": row.image_y,
                "court_x": row.court_x,
                "court_y": row.court_y,
                "review_note": row.note,
                "reviewer": row.reviewer,
                "created_at": (
                    created_at.isoformat() if hasattr(created_at, "isoformat") else None
                ),
                "review_status": "missing_candidate_note",
            }
        )
    return notes


def _geometry_readiness(point_snapshot: dict[str, Any]) -> dict[str, Any]:
    summary = point_snapshot.get("camera_geometry_summary")
    if not isinstance(summary, dict) or summary.get("available") is not True:
        return {
            "camera_geometry_available": False,
            "court_plane_geometry_declared": False,
            "true_3d_reconstruction_available": False,
            "3d_ball_trajectory_available": False,
            "geometry_evidence_only": True,
            "no_adjudication": True,
        }
    return {
        "camera_geometry_available": True,
        "camera_geometry_id": summary.get("camera_geometry_id"),
        "court_plane_geometry_declared": bool(
            summary.get("court_plane_geometry_declared") is True
        ),
        "camera_intrinsics_known": bool(summary.get("camera_intrinsics_known") is True),
        "camera_extrinsics_known": bool(summary.get("camera_extrinsics_known") is True),
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_available": False,
        "geometry_evidence_only": True,
        "no_adjudication": True,
    }


def _warnings(reviewed_final_markers: int) -> dict[str, bool]:
    warnings = dict(EVALUATION_WARNINGS)
    if reviewed_final_markers == 0:
        warnings["no_reviewed_markers"] = True
    return warnings


def _fraction(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "evaluation_type": EVALUATION_TYPE,
        "evaluation_version": EVALUATION_VERSION,
        "warnings": dict(EVALUATION_WARNINGS),
    }


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _candidate_type_label(value: Any) -> str:
    if value == "hit_candidate":
        return "Hit"
    if value == "bounce_candidate":
        return "Bounce"
    return "n/a"


def _markdown_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")
