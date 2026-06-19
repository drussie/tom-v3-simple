from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_perception_execution import (
    build_gameplay_gated_perception_execution_plan,
    export_gameplay_gated_perception_execution_contract,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    build_gameplay_gated_routing_plan,
    export_gameplay_gated_routing_contract,
)
from apps.worker.services.gameplay_segment_gate import (
    export_gameplay_segment_gate_contract,
)
from apps.worker.services.gameplay_segment_replay_review import (
    ALLOWED_LANE_TYPES,
    ALLOWED_REVIEW_STATUSES,
    FORBIDDEN_REPLAY_REVIEW_TOKENS,
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE,
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
    GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE,
    GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION,
    GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE,
    GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION,
    GAMEPLAY_SEGMENT_REVIEW_REPORT_TYPE,
    GAMEPLAY_SEGMENT_REVIEW_REPORT_VERSION,
    build_gameplay_segment_replay_timeline,
    build_gameplay_segment_review_report,
    build_gameplay_segment_review_template,
    export_gameplay_segment_replay_review_contract,
    validate_gameplay_segment_replay_timeline,
    validate_gameplay_segment_review_bundle,
)


def test_export_gameplay_segment_replay_review_contract_is_stable(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "gameplay_segment_replay_review_contract_v1.json"

    result = export_gameplay_segment_replay_review_contract(
        output_path=output_path,
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["replay_review_scope"]["executes_gpu_or_model_inference"] is False
    assert contract["replay_review_scope"]["writes_observations"] is False
    assert (
        contract["source_contract_refs"][
            "gameplay_gated_perception_execution_contract_version"
        ]
        == "v1"
    )
    assert set(contract["timeline_lane_schema"]["allowed_lane_types"]) == ALLOWED_LANE_TYPES
    assert (
        set(contract["timeline_lane_schema"]["allowed_review_statuses"])
        == ALLOWED_REVIEW_STATUSES
    )
    assert not (FORBIDDEN_REPLAY_REVIEW_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_gameplay_segment_replay_timeline(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_execution_fixture(paths)

    result = build_gameplay_segment_replay_timeline(
        gameplay_segments_path=paths["gameplay_segments"],
        routing_plan_path=paths["routing_plan"],
        execution_plan_path=paths["execution_plan"],
        output_path=paths["timeline"],
        viewer_base_url="http://review.local",
        generated_at=datetime(2026, 6, 19, 21, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["timeline_type"] == GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE
    assert result["timeline_version"] == GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION
    assert result["timeline_entry_count"] == 9

    timeline = json.loads(paths["timeline"].read_text(encoding="utf-8"))
    assert timeline["generated_at"] == "2026-06-19T21:00:00+00:00"
    assert timeline["replay_url"] == "http://review.local/replay/media-replay-test"
    assert timeline["summary"]["lane_counts"] == {
        "downstream_allowed": 1,
        "downstream_blocked": 1,
        "downstream_review_required": 1,
        "gameplay_segment_candidate": 1,
        "non_gameplay_segment_candidate": 1,
        "perception_execution_window": 1,
        "perception_skipped_window": 2,
        "uncertain_segment": 1,
    }
    assert timeline["summary"]["review_needed_entry_count"] == 3
    assert all(
        entry["review_status"] in ALLOWED_REVIEW_STATUSES
        for entry in timeline["timeline_entries"]
    )

    validation = validate_gameplay_segment_replay_timeline(
        contract_path=paths["review_contract"],
        timeline_path=paths["timeline"],
        gameplay_segments_path=paths["gameplay_segments"],
        routing_plan_path=paths["routing_plan"],
        execution_plan_path=paths["execution_plan"],
        output_path=paths["timeline_validation"],
        validated_at=datetime(2026, 6, 19, 22, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["timeline_entry_count"] == 9


def test_build_and_validate_gameplay_segment_review_template(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_timeline_fixture(paths)

    result = build_gameplay_segment_review_template(
        timeline_path=paths["timeline"],
        output_path=paths["review_bundle"],
        reviewer_id="operator-1",
        generated_at=datetime(2026, 6, 19, 23, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["review_bundle_type"] == GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE
    assert result["review_bundle_version"] == GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION
    assert result["review_entry_count"] == 9

    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    assert bundle["generated_at"] == "2026-06-19T23:00:00+00:00"
    assert bundle["reviewer_id"] == "operator-1"
    assert bundle["summary"]["review_status_counts"] == {"not_reviewed": 9}
    assert bundle["summary"]["suggested_review_status_counts"]["review_needed"] == 3
    assert all(
        entry["operator_review"]["human_metadata_only"] is True
        for entry in bundle["review_entries"]
    )

    validation = validate_gameplay_segment_review_bundle(
        contract_path=paths["review_contract"],
        timeline_path=paths["timeline"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_validation"],
        validated_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["review_entry_count"] == 9


def test_validation_rejects_forbidden_review_values(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_timeline_fixture(paths)

    timeline = json.loads(paths["timeline"].read_text(encoding="utf-8"))
    timeline["timeline_entries"][0]["lane_type"] = "classifier_correctness"
    timeline["timeline_entries"][0]["review_status"] = "accepted"
    timeline["timeline_entries"][0]["score"] = "6-0"
    paths["timeline"].write_text(json.dumps(timeline), encoding="utf-8")

    timeline_validation = validate_gameplay_segment_replay_timeline(
        contract_path=paths["review_contract"],
        timeline_path=paths["timeline"],
        output_path=None,
    )

    assert timeline_validation["ok"] is False
    assert {error["error_type"] for error in timeline_validation["errors"]} >= {
        "forbidden_token_key",
        "forbidden_token_value",
        "invalid_lane_type",
        "invalid_review_status",
    }

    _build_timeline_fixture(paths)
    build_gameplay_segment_review_template(
        timeline_path=paths["timeline"],
        output_path=paths["review_bundle"],
    )
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    bundle["review_entries"][0]["review_status"] = "true_gameplay"
    bundle["review_entries"][0]["operator_review"]["review_status"] = "resolved"
    bundle["review_entries"][0]["reviewer_score"] = 10
    paths["review_bundle"].write_text(json.dumps(bundle), encoding="utf-8")

    bundle_validation = validate_gameplay_segment_review_bundle(
        contract_path=paths["review_contract"],
        timeline_path=paths["timeline"],
        bundle_path=paths["review_bundle"],
        output_path=None,
    )

    assert bundle_validation["ok"] is False
    assert {error["error_type"] for error in bundle_validation["errors"]} >= {
        "forbidden_token_key",
        "forbidden_token_value",
        "invalid_operator_review_status",
        "invalid_review_status",
    }


def test_build_gameplay_segment_review_report_uses_validation_snapshots(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_timeline_fixture(paths)
    build_gameplay_segment_review_template(
        timeline_path=paths["timeline"],
        output_path=paths["review_bundle"],
    )

    result = build_gameplay_segment_review_report(
        contract_path=paths["review_contract"],
        timeline_path=paths["timeline"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_report"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_SEGMENT_REVIEW_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_SEGMENT_REVIEW_REPORT_VERSION

    report = json.loads(paths["review_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert report["summary"]["timeline_validation_status"] == "valid"
    assert report["summary"]["review_bundle_validation_status"] == "valid"
    assert report["summary"]["review_needed_entry_count"] == 3
    assert report["next_review_contract"]["review_statuses_do_not_create_truth"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "gameplay_segments": tmp_path / "gameplay_segments.json",
        "routing_contract": tmp_path / "routing_contract.json",
        "routing_plan": tmp_path / "routing_plan.json",
        "execution_contract": tmp_path / "execution_contract.json",
        "execution_plan": tmp_path / "execution_plan.json",
        "review_contract": tmp_path / "review_contract.json",
        "timeline": tmp_path / "timeline.json",
        "timeline_validation": tmp_path / "timeline_validation.json",
        "review_bundle": tmp_path / "review_bundle.json",
        "review_validation": tmp_path / "review_validation.json",
        "review_report": tmp_path / "review_report.json",
    }


def _build_execution_fixture(paths: dict[str, Path]) -> None:
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_gated_perception_execution_contract(
        output_path=paths["execution_contract"]
    )
    export_gameplay_segment_replay_review_contract(output_path=paths["review_contract"])
    _write_gameplay_segments(paths["gameplay_segments"])
    build_gameplay_gated_routing_plan(
        gameplay_segments_path=paths["gameplay_segments"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        output_path=paths["routing_plan"],
        downstream_stages=["detection_generation"],
    )
    build_gameplay_gated_perception_execution_plan(
        routing_plan_path=paths["routing_plan"],
        routing_contract_path=paths["routing_contract"],
        output_path=paths["execution_plan"],
        perception_stages=["detection_generation"],
    )


def _build_timeline_fixture(paths: dict[str, Path]) -> None:
    _build_execution_fixture(paths)
    build_gameplay_segment_replay_timeline(
        gameplay_segments_path=paths["gameplay_segments"],
        routing_plan_path=paths["routing_plan"],
        execution_plan_path=paths["execution_plan"],
        output_path=paths["timeline"],
    )


def _write_gameplay_segments(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "output_type": "gameplay_segment_candidates",
                "output_version": "v1",
                "generated_at": "2026-06-19T15:00:00+00:00",
                "media_id": "media-replay-test",
                "source_media_path": "demo_assets/sample_point.mp4",
                "source_uri": "file:///tmp/sample_point.mp4",
                "segment_candidates": [
                    {
                        "segment_id": "segment-allowed",
                        "media_id": "media-replay-test",
                        "segment_start_ms": 0,
                        "segment_end_ms": 1000,
                        "start_frame_index": 0,
                        "end_frame_index": 30,
                        "segment_status": "gameplay_segment_candidate",
                        "downstream_gate_status": "allowed_for_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-blocked",
                        "media_id": "media-replay-test",
                        "segment_start_ms": 1000,
                        "segment_end_ms": 2000,
                        "start_frame_index": 31,
                        "end_frame_index": 60,
                        "segment_status": "non_gameplay_segment_candidate",
                        "downstream_gate_status": "blocked_from_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-review",
                        "media_id": "media-replay-test",
                        "segment_start_ms": 2000,
                        "segment_end_ms": 3000,
                        "start_frame_index": 61,
                        "end_frame_index": 90,
                        "segment_status": "uncertain_segment",
                        "downstream_gate_status": "requires_human_review",
                        "warnings": {"candidate_segment_only": True},
                    },
                ],
                "summary": {"segment_candidate_count": 3},
                "warnings": {"candidate_evidence_only": True},
            }
        ),
        encoding="utf-8",
    )


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            seen.add(str(key))
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        seen.add(value)
    return seen
