from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient

from apps.api.main import create_app
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_TYPE,
    build_multi_point_replay_index,
)
from apps.worker.services.point_manifest import (
    POINT_MANIFEST_TYPE,
    POINT_MANIFEST_WARNINGS,
)

PROTECTED_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_EVENT_RUN_ID = "1b946366-7ec1-426f-8b40-494535a9b3fb"
PROTECTED_TRAJECTORY_RUN_ID = "ea76ccab-c51d-4a63-9682-9fd0bbb83f14"
PROTECTED_CAMERA_GEOMETRY_ID = "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"
FORBIDDEN_DECISION_KEYS = {
    "in_out",
    "score",
    "point_winner",
    "player_identity",
    "rally_state",
    "server_state",
    "receiver_state",
}


def test_multi_point_replay_index_discovers_manifests_and_preserves_replay_context(
    tmp_path: Path,
) -> None:
    manifest_root = tmp_path / "manifests"
    protected_path = manifest_root / "sample_point.blueprint_23.point_manifest.json"
    second_path = manifest_root / "second_point" / "sample_point.stand_in.point_manifest.json"
    output_path = manifest_root / "multi_point_replay_index.json"

    _write_json(
        protected_path,
        _point_manifest(
            point_manifest_id="point_manifest_v0_protected",
            media_id=PROTECTED_MEDIA_ID,
            source_media_path="/data/sample_point.mp4",
            replay_url=(
                f"http://viewer.example/replay/{PROTECTED_MEDIA_ID}"
                f"?eventCandidateRunId={PROTECTED_EVENT_RUN_ID}"
            ),
            associated_run_ids={
                "event_candidate_run_id": PROTECTED_EVENT_RUN_ID,
                "trajectory_3d_run_id": PROTECTED_TRAJECTORY_RUN_ID,
                "camera_geometry_id": PROTECTED_CAMERA_GEOMETRY_ID,
            },
            profile_counts={
                "event_marker_count": 2,
                "trajectory_3d_candidate_count": 12,
                "review_annotation_count": 3,
            },
        ),
    )
    _write_json(
        manifest_root / "zzz_duplicate_protected.point_manifest.json",
        _point_manifest(
            point_manifest_id="point_manifest_v0_protected",
            media_id=PROTECTED_MEDIA_ID,
            source_media_path="/data/sample_point.mp4",
            replay_url=f"http://viewer.example/replay/{PROTECTED_MEDIA_ID}",
            associated_run_ids={
                "event_candidate_run_id": PROTECTED_EVENT_RUN_ID,
                "trajectory_3d_run_id": PROTECTED_TRAJECTORY_RUN_ID,
                "camera_geometry_id": PROTECTED_CAMERA_GEOMETRY_ID,
            },
            profile_counts={
                "event_marker_count": 2,
                "trajectory_3d_candidate_count": 12,
                "review_annotation_count": 3,
            },
        ),
    )
    _write_json(
        second_path,
        _point_manifest(
            point_manifest_id="point_manifest_v0_second",
            media_id="second-point-media-id",
            source_media_path="/demo_assets/sample_point.mp4",
            replay_url="http://viewer.example/replay/second-point-media-id",
            associated_run_ids={},
            profile_counts={
                "event_marker_count": 0,
                "trajectory_3d_candidate_count": 0,
                "review_annotation_count": 0,
            },
        ),
    )
    _write_json(manifest_root / "not-a-point.json", {"manifest_type": "other"})
    _write_text(manifest_root / "invalid.json", "{")

    result = build_multi_point_replay_index(
        manifest_root=manifest_root,
        output_path=output_path,
        viewer_base_url="http://127.0.0.1:3000",
        generated_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["index_type"] == MULTI_POINT_REPLAY_INDEX_TYPE
    assert result["point_count"] == 2
    assert result["skipped_manifest_count"] == 3
    assert output_path.is_file()

    index = json.loads(output_path.read_text(encoding="utf-8"))
    assert index["generated_at"] == "2026-06-17T12:00:00+00:00"
    assert index["point_count"] == 2
    assert index["warnings"]["navigation_only"] is True
    assert index["warnings"]["manifest_index_is_not_truth"] is True
    assert index["warnings"]["observation_only"] is True
    assert index["warnings"]["no_adjudication"] is True

    protected_point = index["points"][0]
    assert protected_point["labels"] == ["protected_sample_point"]
    assert protected_point["manifest_path"] == str(protected_path)
    replay_params = parse_qs(urlparse(protected_point["replay_url"]).query)
    assert replay_params["eventCandidateRunId"] == [PROTECTED_EVENT_RUN_ID]
    assert replay_params["trajectory3dRunId"] == [PROTECTED_TRAJECTORY_RUN_ID]
    assert replay_params["cameraGeometryId"] == [PROTECTED_CAMERA_GEOMETRY_ID]
    assert protected_point["profile_counts"]["event_marker_count"] == 2
    assert protected_point["warnings"]["manifest_is_not_truth"] is True

    second_point = index["points"][1]
    assert second_point["labels"] == ["second_point_parity_stand_in"]
    assert second_point["evidence_availability"]["media_indexed"] is True
    assert second_point["evidence_availability"]["replay_available"] is True
    assert second_point["evidence_availability"]["event_candidates_available"] is False

    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(index)


def test_multi_point_replay_index_handles_missing_manifest_root(tmp_path: Path) -> None:
    output_path = tmp_path / "exports" / "empty_index.json"

    result = build_multi_point_replay_index(
        manifest_root=tmp_path / "missing",
        output_path=output_path,
        generated_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["point_count"] == 0
    assert result["skipped_manifest_count"] == 0
    assert output_path.is_file()
    index = json.loads(output_path.read_text(encoding="utf-8"))
    assert index["points"] == []
    assert index["warnings"]["does_not_create_in_out"] is True


def test_replay_point_manifests_api_returns_file_backed_index(tmp_path: Path) -> None:
    manifest_root = tmp_path / "manifests"
    _write_json(
        manifest_root / "point_manifest.json",
        _point_manifest(
            point_manifest_id="point_manifest_v0_api",
            media_id="api-media-id",
            source_media_path="/tmp/api-media.mp4",
            replay_url="http://viewer.example/replay/api-media-id",
            associated_run_ids={"event_candidate_run_id": "event-run-api"},
            profile_counts={"event_marker_count": 1},
        ),
    )

    app = create_app()
    with TestClient(app) as client:
        response = client.get(
            "/replay/point-manifests",
            params={
                "manifest_root": str(manifest_root),
                "viewer_base_url": "http://127.0.0.1:3000",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["index_type"] == MULTI_POINT_REPLAY_INDEX_TYPE
    assert body["point_count"] == 1
    point = body["points"][0]
    assert point["point_manifest_id"] == "point_manifest_v0_api"
    replay_params = parse_qs(urlparse(point["replay_url"]).query)
    assert replay_params["eventCandidateRunId"] == ["event-run-api"]
    assert body["warnings"]["no_adjudication"] is True


def _point_manifest(
    *,
    point_manifest_id: str,
    media_id: str,
    source_media_path: str,
    replay_url: str,
    associated_run_ids: dict[str, str],
    profile_counts: dict[str, int],
) -> dict[str, Any]:
    counts = {
        "event_marker_count": 0,
        "hit_candidate_count": 0,
        "bounce_candidate_count": 0,
        "event_candidate_observation_count": 0,
        "event_candidate_rejection_diagnostic_count": 0,
        "trajectory_3d_candidate_count": 0,
        "event_candidate_3d_diagnostic_count": 0,
        "event_marker_review_count": 0,
        "trajectory_3d_debug_review_count": 0,
        "human_annotation_count": 0,
        "review_annotation_count": 0,
        **profile_counts,
    }
    return {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": "v0",
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "source_media_path": source_media_path,
        "source_uri": f"file://{source_media_path}",
        "stored_path": source_media_path,
        "stored_uri": f"file://{source_media_path}",
        "replay_url": replay_url,
        "generated_at": "2026-06-17T12:00:00+00:00",
        "tom_provenance": {
            "project": "tom-v3-simple",
            "project_version": "0.0.0",
            "blueprint": "blueprint_23",
        },
        "associated_run_ids": associated_run_ids,
        "evidence_availability": {
            "media_indexed": True,
            "replay_available": True,
            "event_candidates_available": counts["event_marker_count"] > 0,
            "trajectory_3d_candidates_available": counts["trajectory_3d_candidate_count"] > 0,
            "event_candidate_3d_diagnostics_available": False,
            "review_annotations_available": counts["review_annotation_count"] > 0,
            "trajectory_3d_debug_reviews_available": False,
        },
        "profile_counts": counts,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


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
