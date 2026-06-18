from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    OBSERVATION_QUALITY_PROFILE_TYPE,
    OBSERVATION_QUALITY_TAXONOMY_TYPE,
    OBSERVATION_QUALITY_WARNINGS,
    QUALITY_ALLOWED_VALUES,
    build_observation_quality_profile,
    export_observation_quality_taxonomy,
)

FORBIDDEN_DECISION_KEYS = {
    "in_out",
    "score",
    "point_winner",
    "player_identity",
    "rally_state",
    "server_state",
    "receiver_state",
}

EXPECTED_DIMENSIONS = {
    "media_quality",
    "camera_stability",
    "court_visibility",
    "ball_visibility",
    "player_visibility",
    "occlusion",
    "motion_blur",
    "lighting",
    "frame_continuity",
    "replay_context_completeness",
    "evidence_completeness",
    "calibration_readiness",
    "trajectory_3d_readiness",
    "review_readiness",
    "annotation_readiness",
    "provenance_completeness",
}


def test_export_observation_quality_taxonomy_writes_contract(tmp_path: Path) -> None:
    output_path = tmp_path / "contracts" / "observation_quality_taxonomy_v1.json"

    result = export_observation_quality_taxonomy(
        output_path=output_path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["taxonomy_type"] == OBSERVATION_QUALITY_TAXONOMY_TYPE
    assert result["dimension_count"] == len(EXPECTED_DIMENSIONS)
    assert output_path.is_file()

    taxonomy = json.loads(output_path.read_text(encoding="utf-8"))
    assert taxonomy["exported_at"] == "2026-06-18T12:00:00+00:00"
    assert {item["key"] for item in taxonomy["dimensions"]} == EXPECTED_DIMENSIONS
    assert taxonomy["warnings"] == OBSERVATION_QUALITY_WARNINGS
    for dimension in taxonomy["dimensions"]:
        assert dimension["default_value"] == "unknown"
        assert set(QUALITY_ALLOWED_VALUES).issubset(set(dimension["allowed_values"]))
        assert dimension["warnings"]["dimension_is_not_truth"] is True
        assert dimension["warnings"]["no_adjudication"] is True
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(taxonomy)


def test_build_observation_quality_profile_preserves_context_and_unknown_quality(
    tmp_path: Path,
) -> None:
    index_path = tmp_path / "manifests" / "multi_point_replay_index.json"
    output_path = tmp_path / "exports" / "observation_quality_profile.current.json"
    _write_json(
        index_path,
        _replay_index(
            [
                _index_point(
                    point_manifest_id="point_manifest_v0_sample",
                    media_id="media-1",
                    manifest_path="/tmp/sample.point_manifest.json",
                    replay_url="http://viewer.example/replay/media-1?eventCandidateRunId=run-1",
                    source_media_path="/data/sample.mp4",
                    associated_run_ids={"event_candidate_run_id": "run-1"},
                    evidence_availability={
                        "media_indexed": True,
                        "replay_available": True,
                        "event_candidates_available": True,
                        "trajectory_3d_candidates_available": False,
                        "review_annotations_available": False,
                    },
                    profile_counts={"event_marker_count": 2},
                    labels=["protected_sample_point"],
                )
            ]
        ),
    )

    result = build_observation_quality_profile(
        source_index_path=index_path,
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 12, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["profile_type"] == OBSERVATION_QUALITY_PROFILE_TYPE
    assert result["point_count"] == 1
    assert result["summary"] == {
        "point_count": 1,
        "replay_available_count": 1,
        "review_ready_count": 1,
        "unknown_quality_count": 1,
        "requires_human_review_count": 1,
    }
    assert output_path.is_file()

    profile = json.loads(output_path.read_text(encoding="utf-8"))
    point = profile["points"][0]
    dimensions = _dimension_map(point)
    assert point["labels"] == ["protected_sample_point"]
    assert point["associated_run_ids"] == {"event_candidate_run_id": "run-1"}
    assert dimensions["media_quality"]["value"] == "unknown"
    assert dimensions["media_quality"]["requires_human_review"] is True
    assert dimensions["replay_context_completeness"]["value"] == "sufficient_for_review"
    assert dimensions["replay_context_completeness"]["requires_human_review"] is False
    assert dimensions["trajectory_3d_readiness"]["value"] == "unavailable"
    assert dimensions["review_readiness"]["value"] == "needs_human_review"
    assert dimensions["provenance_completeness"]["value"] == "sufficient_for_review"
    assert point["warnings"]["quality_profile_is_not_truth"] is True
    assert profile["warnings"]["does_not_create_event_candidates"] is True
    assert profile["warnings"]["does_not_create_3d_candidates"] is True
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(profile)


def test_build_observation_quality_profile_marks_missing_evidence_unavailable(
    tmp_path: Path,
) -> None:
    index_path = tmp_path / "multi_point_replay_index.json"
    _write_json(
        index_path,
        _replay_index(
            [
                _index_point(
                    point_manifest_id="point_manifest_v0_empty",
                    media_id="media-empty",
                    manifest_path="/tmp/empty.point_manifest.json",
                    replay_url=None,
                    source_media_path=None,
                    associated_run_ids={},
                    evidence_availability={
                        "media_indexed": False,
                        "replay_available": False,
                        "event_candidates_available": False,
                        "trajectory_3d_candidates_available": False,
                        "review_annotations_available": False,
                    },
                    profile_counts={},
                    labels=["second_point_parity_stand_in"],
                )
            ]
        ),
    )

    result = build_observation_quality_profile(
        source_index_path=index_path,
        output_path=None,
        generated_at=datetime(2026, 6, 18, 12, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["summary"]["replay_available_count"] == 0
    assert result["summary"]["review_ready_count"] == 0
    point = result["profile"]["points"][0]
    dimensions = _dimension_map(point)
    assert dimensions["media_quality"]["value"] == "unavailable"
    assert dimensions["replay_context_completeness"]["value"] == "unavailable"
    assert dimensions["evidence_completeness"]["value"] == "unavailable"
    assert dimensions["review_readiness"]["value"] == "unavailable"
    assert dimensions["provenance_completeness"]["value"] == "sufficient_for_review"
    assert point["warnings"]["review_support_only"] is True


def test_build_observation_quality_profile_rejects_invalid_source_index(
    tmp_path: Path,
) -> None:
    index_path = tmp_path / "invalid.json"
    _write_json(index_path, {"index_type": "not_a_replay_index", "index_version": "v0"})

    result = build_observation_quality_profile(source_index_path=index_path, output_path=None)

    assert result["ok"] is False
    assert result["status"] == "invalid_source_index_type"
    assert result["warnings"]["taxonomy_is_not_truth"] is True
    assert result["warnings"]["no_adjudication"] is True


def _replay_index(points: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "index_type": MULTI_POINT_REPLAY_INDEX_TYPE,
        "index_version": MULTI_POINT_REPLAY_INDEX_VERSION,
        "generated_at": "2026-06-18T12:00:00+00:00",
        "point_count": len(points),
        "points": points,
        "warnings": {
            "manifest_index_is_not_truth": True,
            "navigation_only": True,
            "no_adjudication": True,
        },
    }


def _index_point(
    *,
    point_manifest_id: str,
    media_id: str,
    manifest_path: str,
    replay_url: str | None,
    source_media_path: str | None,
    associated_run_ids: dict[str, str],
    evidence_availability: dict[str, bool],
    profile_counts: dict[str, int],
    labels: list[str],
) -> dict[str, Any]:
    return {
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "manifest_path": manifest_path,
        "replay_url": replay_url,
        "source_media_path": source_media_path,
        "source_uri": f"file://{source_media_path}" if source_media_path else None,
        "stored_path": source_media_path,
        "stored_uri": f"file://{source_media_path}" if source_media_path else None,
        "associated_run_ids": associated_run_ids,
        "evidence_availability": evidence_availability,
        "profile_counts": profile_counts,
        "labels": labels,
        "warnings": {
            "manifest_is_not_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    }


def _dimension_map(point: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        dimension["dimension_key"]: dimension
        for dimension in point["quality_dimensions"]
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_walk_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_walk_keys(item))
        return keys
    return set()
