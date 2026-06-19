from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_perception_execution import (
    ALLOWED_EXECUTION_DECISIONS,
    ALLOWED_EXECUTION_MODES,
    ALLOWED_SKIP_REASONS,
    DEFAULT_PERCEPTION_STAGES,
    FORBIDDEN_EXECUTION_TOKENS,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_TYPE,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_VERSION,
    build_gameplay_gated_perception_execution_plan,
    build_gameplay_gated_perception_execution_report,
    export_gameplay_gated_perception_execution_contract,
    validate_gameplay_gated_perception_execution_plan,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    build_gameplay_gated_routing_plan,
    export_gameplay_gated_routing_contract,
)
from apps.worker.services.gameplay_segment_gate import (
    export_gameplay_segment_gate_contract,
)


def test_export_gameplay_gated_perception_execution_contract_is_stable(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "gameplay_gated_perception_execution_contract_v1.json"

    result = export_gameplay_gated_perception_execution_contract(
        output_path=output_path,
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["execution_scope"]["default_execution_mode"] == "dry_run"
    assert contract["execution_scope"]["executes_gpu_or_model_inference_by_default"] is False
    assert contract["execution_scope"]["writes_observations_by_default"] is False
    assert (
        contract["source_contract_refs"]["gameplay_gated_pipeline_routing_contract_version"]
        == "v1"
    )
    assert (
        set(contract["execution_plan_schema"]["allowed_execution_modes"])
        == ALLOWED_EXECUTION_MODES
    )
    assert (
        set(contract["execution_plan_schema"]["allowed_execution_decisions"])
        == ALLOWED_EXECUTION_DECISIONS
    )
    assert (
        set(contract["skipped_window_schema"]["allowed_skip_reasons"])
        == ALLOWED_SKIP_REASONS
    )
    assert set(contract["perception_stage_schema"]["allowed_stages"]) == set(
        DEFAULT_PERCEPTION_STAGES
    )
    assert not (FORBIDDEN_EXECUTION_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_gameplay_gated_perception_execution_plan(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_routing_fixture(paths)

    result = build_gameplay_gated_perception_execution_plan(
        routing_plan_path=paths["routing_plan"],
        routing_contract_path=paths["routing_contract"],
        output_path=paths["execution_plan"],
        execution_mode="dry_run",
        perception_stages=["detection_generation", "pose_generation"],
        generated_at=datetime(2026, 6, 19, 18, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["plan_type"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE
    assert result["plan_version"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION
    assert result["perception_stage_count"] == 2
    assert result["routing_entry_count"] == 6
    assert result["execution_entry_count"] == 6

    plan = json.loads(paths["execution_plan"].read_text(encoding="utf-8"))
    assert plan["generated_at"] == "2026-06-19T18:00:00+00:00"
    assert plan["execution_mode"] == "dry_run"
    assert len(plan["allowed_execution_windows"]) == 1
    assert len(plan["skipped_windows"]) == 1
    assert len(plan["review_required_windows"]) == 1
    assert plan["summary"]["perception_jobs_executed"] is False
    assert plan["summary"]["gpu_or_model_inference_executed"] is False
    assert plan["summary"]["observations_written"] is False
    assert plan["summary"]["execution_decision_counts"] == {
        "execute_on_gameplay_window": 2,
        "require_human_review": 2,
        "skip_non_gameplay_window": 2,
    }
    assert all(stage in DEFAULT_PERCEPTION_STAGES for stage in plan["perception_stages"])

    validation = validate_gameplay_gated_perception_execution_plan(
        contract_path=paths["execution_contract"],
        routing_contract_path=paths["routing_contract"],
        routing_plan_path=paths["routing_plan"],
        plan_path=paths["execution_plan"],
        output_path=paths["execution_validation"],
        validated_at=datetime(2026, 6, 19, 19, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["execution_entry_count"] == 6


def test_validate_gameplay_gated_perception_execution_plan_rejects_bad_values(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_routing_fixture(paths)
    build_gameplay_gated_perception_execution_plan(
        routing_plan_path=paths["routing_plan"],
        routing_contract_path=paths["routing_contract"],
        output_path=paths["execution_plan"],
        perception_stages=["detection_generation"],
    )
    plan = json.loads(paths["execution_plan"].read_text(encoding="utf-8"))
    plan["execution_mode"] = "auto_execute_models"
    plan["execution_entries"][0]["execution_decision"] = "confirmed_gameplay"
    plan["execution_entries"][0]["score"] = "6-0"
    plan["execution_entries"][0]["provenance_status"] = "missing_context"
    paths["execution_plan"].write_text(json.dumps(plan), encoding="utf-8")

    result = validate_gameplay_gated_perception_execution_plan(
        contract_path=paths["execution_contract"],
        routing_contract_path=paths["routing_contract"],
        routing_plan_path=paths["routing_plan"],
        plan_path=paths["execution_plan"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_token_key",
        "forbidden_token_value",
        "invalid_execution_decision",
        "invalid_execution_mode",
        "invalid_provenance_status",
    }


def test_build_gameplay_gated_perception_execution_report_uses_validation_snapshot(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_routing_fixture(paths)
    build_gameplay_gated_perception_execution_plan(
        routing_plan_path=paths["routing_plan"],
        routing_contract_path=paths["routing_contract"],
        output_path=paths["execution_plan"],
        perception_stages=["detection_generation", "trajectory_3d_generation"],
    )

    result = build_gameplay_gated_perception_execution_report(
        contract_path=paths["execution_contract"],
        routing_contract_path=paths["routing_contract"],
        routing_plan_path=paths["routing_plan"],
        plan_path=paths["execution_plan"],
        output_path=paths["execution_report"],
        generated_at=datetime(2026, 6, 19, 20, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_VERSION

    report = json.loads(paths["execution_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T20:00:00+00:00"
    assert report["summary"]["validation_status"] == "valid"
    assert report["summary"]["perception_jobs_executed"] is False
    assert (
        report["next_execution_contract"]["this_report_executes_perception_jobs"]
        is False
    )
    assert len(report["stage_summaries"]) == 2


def test_fixture_execution_only_adds_non_mutating_output_refs(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_routing_fixture(paths)

    result = build_gameplay_gated_perception_execution_plan(
        routing_plan_path=paths["routing_plan"],
        routing_contract_path=paths["routing_contract"],
        output_path=paths["execution_plan"],
        execution_mode="fixture_execution_only",
        perception_stages=["detection_generation"],
    )

    assert result["ok"] is True
    plan = json.loads(paths["execution_plan"].read_text(encoding="utf-8"))
    output_refs = [
        entry["output_ref"]
        for entry in plan["execution_entries"]
        if entry["execution_decision"] == "execute_on_gameplay_window"
    ]
    assert len(output_refs) == 1
    assert output_refs[0]["output_ref_type"] == "fixture_execution_placeholder"
    assert output_refs[0]["writes_observations"] is False
    assert output_refs[0]["runs_heavy_inference"] is False


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "gameplay_segments": tmp_path / "gameplay_segments.json",
        "routing_contract": tmp_path / "routing_contract.json",
        "routing_plan": tmp_path / "routing_plan.json",
        "execution_contract": tmp_path / "execution_contract.json",
        "execution_plan": tmp_path / "execution_plan.json",
        "execution_validation": tmp_path / "execution_validation.json",
        "execution_report": tmp_path / "execution_report.json",
    }


def _build_routing_fixture(paths: dict[str, Path]) -> None:
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_gated_perception_execution_contract(
        output_path=paths["execution_contract"]
    )
    _write_gameplay_segments(paths["gameplay_segments"])
    build_gameplay_gated_routing_plan(
        gameplay_segments_path=paths["gameplay_segments"],
        gameplay_gate_contract_path=paths["gameplay_contract"],
        output_path=paths["routing_plan"],
        downstream_stages=[
            "detection_generation",
            "pose_generation",
            "trajectory_3d_generation",
        ],
    )


def _write_gameplay_segments(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "output_type": "gameplay_segment_candidates",
                "output_version": "v1",
                "generated_at": "2026-06-19T15:00:00+00:00",
                "media_id": "media-execution-test",
                "source_media_path": "demo_assets/sample_point.mp4",
                "source_uri": "file:///tmp/sample_point.mp4",
                "segment_candidates": [
                    {
                        "segment_id": "segment-allowed",
                        "media_id": "media-execution-test",
                        "segment_start_ms": 0,
                        "segment_end_ms": 1000,
                        "segment_status": "gameplay_segment_candidate",
                        "downstream_gate_status": "allowed_for_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-blocked",
                        "media_id": "media-execution-test",
                        "segment_start_ms": 1000,
                        "segment_end_ms": 2000,
                        "segment_status": "non_gameplay_segment_candidate",
                        "downstream_gate_status": "blocked_from_downstream_observation",
                        "warnings": {"candidate_segment_only": True},
                    },
                    {
                        "segment_id": "segment-review",
                        "media_id": "media-execution-test",
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
