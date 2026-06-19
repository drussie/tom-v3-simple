from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_pipeline_routing import (
    ALLOWED_OVERRIDE_STATUSES,
    ALLOWED_ROUTING_DECISIONS,
    ALLOWED_ROUTING_MODES,
    ALLOWED_SKIP_REASONS,
    DEFAULT_DOWNSTREAM_STAGES,
    FORBIDDEN_ROUTING_TOKENS,
    GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
    GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
    GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
    GAMEPLAY_GATED_ROUTING_REPORT_TYPE,
    GAMEPLAY_GATED_ROUTING_REPORT_VERSION,
    build_gameplay_gated_routing_plan,
    build_gameplay_gated_routing_report,
    export_gameplay_gated_routing_contract,
    validate_gameplay_gated_routing_plan,
)
from apps.worker.services.gameplay_segment_gate import (
    export_gameplay_segment_gate_contract,
)


def test_export_gameplay_gated_routing_contract_is_stable(tmp_path: Path) -> None:
    output_path = tmp_path / "gameplay_gated_pipeline_routing_contract_v1.json"

    result = export_gameplay_gated_routing_contract(
        output_path=output_path,
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["routing_scope"]["default_routing_mode"] == "dry_run"
    assert contract["routing_scope"]["executes_downstream_jobs_by_default"] is False
    assert contract["source_contract_refs"]["gameplay_segment_gate_contract_version"] == "v1"
    assert set(contract["routing_plan_schema"]["allowed_routing_modes"]) == ALLOWED_ROUTING_MODES
    assert (
        set(contract["routing_plan_schema"]["allowed_routing_decisions"])
        == ALLOWED_ROUTING_DECISIONS
    )
    assert (
        set(contract["skip_reason_schema"]["allowed_skip_reasons"])
        == ALLOWED_SKIP_REASONS
    )
    assert (
        set(contract["override_policy_schema"]["allowed_override_statuses"])
        == ALLOWED_OVERRIDE_STATUSES
    )
    assert not (FORBIDDEN_ROUTING_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_gameplay_gated_routing_plan(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    _write_gameplay_segments(paths["gameplay_segments"])

    result = build_gameplay_gated_routing_plan(
        gameplay_segments_path=paths["gameplay_segments"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        output_path=paths["routing_plan"],
        routing_mode="dry_run",
        downstream_stages=["detection_generation", "pose_generation"],
        generated_at=datetime(2026, 6, 19, 15, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["plan_type"] == GAMEPLAY_GATED_ROUTING_PLAN_TYPE
    assert result["plan_version"] == GAMEPLAY_GATED_ROUTING_PLAN_VERSION
    assert result["downstream_stage_count"] == 2
    assert result["segment_count"] == 3
    assert result["routing_entry_count"] == 6

    plan = json.loads(paths["routing_plan"].read_text(encoding="utf-8"))
    assert plan["generated_at"] == "2026-06-19T15:00:00+00:00"
    assert plan["routing_mode"] == "dry_run"
    assert len(plan["allowed_windows"]) == 1
    assert len(plan["blocked_windows"]) == 1
    assert len(plan["uncertain_windows"]) == 1
    assert plan["summary"]["downstream_jobs_executed"] is False
    assert plan["summary"]["routing_decision_counts"] == {
        "allow_downstream_observation": 2,
        "require_human_review": 2,
        "skip_non_gameplay": 2,
    }
    assert plan["replay_timeline"]["lane"]["display_only"] is True
    assert all(stage in DEFAULT_DOWNSTREAM_STAGES for stage in plan["downstream_stages"])

    validation = validate_gameplay_gated_routing_plan(
        contract_path=paths["routing_contract"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        plan_path=paths["routing_plan"],
        output_path=paths["routing_validation"],
        validated_at=datetime(2026, 6, 19, 16, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["routing_entry_count"] == 6


def test_validate_gameplay_gated_routing_plan_rejects_forbidden_and_bad_values(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    _write_gameplay_segments(paths["gameplay_segments"])
    build_gameplay_gated_routing_plan(
        gameplay_segments_path=paths["gameplay_segments"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        output_path=paths["routing_plan"],
        downstream_stages=["detection_generation"],
    )
    plan = json.loads(paths["routing_plan"].read_text(encoding="utf-8"))
    plan["routing_mode"] = "auto_execute_everything"
    plan["routing_entries"][0]["routing_decision"] = "confirmed_gameplay"
    plan["routing_entries"][0]["score"] = "6-0"
    paths["routing_plan"].write_text(json.dumps(plan), encoding="utf-8")

    result = validate_gameplay_gated_routing_plan(
        contract_path=paths["routing_contract"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        plan_path=paths["routing_plan"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_token_key",
        "forbidden_token_value",
        "invalid_routing_decision",
        "invalid_routing_mode",
    }


def test_build_gameplay_gated_routing_report_uses_validation_snapshot(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    _write_gameplay_segments(paths["gameplay_segments"])
    build_gameplay_gated_routing_plan(
        gameplay_segments_path=paths["gameplay_segments"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        output_path=paths["routing_plan"],
        downstream_stages=["detection_generation", "review_queue_inclusion"],
    )

    result = build_gameplay_gated_routing_report(
        contract_path=paths["routing_contract"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        plan_path=paths["routing_plan"],
        output_path=paths["routing_report"],
        generated_at=datetime(2026, 6, 19, 17, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATED_ROUTING_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_GATED_ROUTING_REPORT_VERSION

    report = json.loads(paths["routing_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T17:00:00+00:00"
    assert report["summary"]["validation_status"] == "valid"
    assert report["summary"]["downstream_jobs_executed"] is False
    assert report["next_pipeline_contract"]["this_report_executes_downstream_jobs"] is False
    assert len(report["stage_summaries"]) == 2


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "routing_contract": tmp_path / "routing_contract.json",
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "gameplay_segments": tmp_path / "gameplay_segments.json",
        "routing_plan": tmp_path / "routing_plan.json",
        "routing_validation": tmp_path / "routing_validation.json",
        "routing_report": tmp_path / "routing_report.json",
    }


def _write_gameplay_segments(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "output_type": "gameplay_segment_candidates",
                "output_version": "v1",
                "generated_at": "2026-06-19T15:00:00+00:00",
                "media_id": "media-routing-test",
                "source_media_path": "demo_assets/sample_point.mp4",
                "source_uri": "file:///tmp/sample_point.mp4",
                "segment_candidates": [
                    {
                        "segment_id": "segment-allowed",
                        "media_id": "media-routing-test",
                        "segment_start_ms": 0,
                        "segment_end_ms": 1000,
                        "segment_status": "gameplay_segment_candidate",
                        "downstream_gate_status": "allowed_for_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-blocked",
                        "media_id": "media-routing-test",
                        "segment_start_ms": 1000,
                        "segment_end_ms": 2000,
                        "segment_status": "non_gameplay_segment_candidate",
                        "downstream_gate_status": "blocked_from_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-review",
                        "media_id": "media-routing-test",
                        "segment_start_ms": 2000,
                        "segment_end_ms": 3000,
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
