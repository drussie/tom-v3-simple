from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_dry_run_review_packet import (
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE,
    FORBIDDEN_REVIEW_PACKET_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_dry_run_operator_checklist,
    build_controlled_runtime_calibration_dry_run_review_packet,
    build_controlled_runtime_calibration_dry_run_review_packet_inputs,
    build_controlled_runtime_calibration_dry_run_review_summary,
    export_controlled_runtime_calibration_dry_run_review_packet_contract,
    validate_controlled_runtime_calibration_dry_run_review_packet,
    validate_controlled_runtime_calibration_dry_run_review_packet_inputs,
)


def test_export_controlled_runtime_calibration_dry_run_review_packet_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_dry_run_review_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["review_packet_scope"]["packages_existing_dry_run_report"] is True
    assert contract["review_packet_scope"]["requires_human_operator_review"] is True
    assert contract["review_packet_scope"]["applies_threshold_changes"] is False
    assert contract["review_packet_scope"]["updates_runtime_configuration"] is False
    assert contract["review_packet_scope"]["updates_model_weights"] is False
    assert contract["review_packet_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["review_packet_schema"]["required_runtime_application_status"]
        == "not_applied"
    )
    assert contract["review_packet_schema"]["required_mutation_status"] == (
        "no_runtime_mutation"
    )
    assert contract["warnings"]["controlled_dry_run_review_packet"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_controlled_runtime_calibration_dry_run_review_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_dry_run_review_packet_inputs(
        contract_path=paths["contract"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_dry_run_inputs_path=paths["dry_run_inputs"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["review_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["review_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["operator_review_context"]["operator_review_required"] is True
    assert inputs["operator_review_context"]["mutation_status"] == "no_runtime_mutation"
    assert inputs["rollback_plan_ref"]["rollback_plan_id"] == "rollback_fixture"
    assert inputs["source_artifact_presence"]["dry_run_execution_report"]["present"] is True
    assert inputs["missing_source_refs"] == []
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_dry_run_review_packet_inputs(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["review_inputs"],
        output_path=paths["review_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_dry_run_review_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_inputs(paths)

    result = build_controlled_runtime_calibration_dry_run_review_packet(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["review_inputs"],
        output_path=paths["review_packet"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["review_packet_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE
    )
    assert result["review_packet_status"] == "review_packet_created_with_warnings"
    assert result["next_step_recommendation"] == "human_review_required"
    assert result["runtime_application_status"] == "not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"
    assert result["operator_review_required"] is True
    assert result["future_blueprint_required_for_runtime_application"] is True

    packet = json.loads(paths["review_packet"].read_text(encoding="utf-8"))
    assert packet["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert packet["structural_comparison_summary"]["total_comparisons"] == 2
    assert (
        packet["rollback_readiness_summary"]["rollback_readiness_status"]
        == "rollback_ready_for_future_phase_review"
    )
    assert packet["regression_gate_summary"]["all_required_gate_refs_present"] is True
    assert packet["blocker_summary"]["blockers"] == [
        "human_operator_approval_required"
    ]
    assert {item["checklist_item"] for item in packet["operator_review_checklist"]} >= {
        "confirm_no_runtime_application",
        "confirm_no_runtime_mutation",
        "confirm_no_production_config",
        "confirm_no_model_change",
        "confirm_no_baseline_replacement",
        "decide_next_phase_readiness",
    }
    assert packet["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(packet))

    validation = validate_controlled_runtime_calibration_dry_run_review_packet(
        contract_path=paths["contract"],
        review_packet_path=paths["review_packet"],
        output_path=paths["review_packet_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"
    assert validation["operator_review_required"] is True


def test_build_review_summary_and_operator_checklist(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_review_packet(paths)

    summary_result = build_controlled_runtime_calibration_dry_run_review_summary(
        contract_path=paths["contract"],
        review_packet_path=paths["review_packet"],
        output_path=paths["review_summary"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert summary_result["ok"] is True
    summary = json.loads(paths["review_summary"].read_text(encoding="utf-8"))
    assert summary["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert summary["runtime_application_status"] == "not_applied"
    assert summary["mutation_status"] == "no_runtime_mutation"
    assert summary["operator_review_required"] is True
    assert summary["future_blueprint_required_for_runtime_application"] is True
    assert summary["non_claims"] == NON_CLAIMS

    checklist_result = (
        build_controlled_runtime_calibration_dry_run_operator_checklist(
            contract_path=paths["contract"],
            review_packet_path=paths["review_packet"],
            output_path=paths["operator_checklist"],
            generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
        )
    )
    assert checklist_result["ok"] is True
    checklist = json.loads(paths["operator_checklist"].read_text(encoding="utf-8"))
    assert checklist["operator_review_required"] is True
    assert checklist["runtime_application_status"] == "not_applied"
    assert checklist["production_config_status"] == "not_created"
    assert checklist["baseline_update_status"] == "not_replaced"
    assert checklist["model_update_status"] == "not_modified"
    assert {item["checklist_item"] for item in checklist["items"]} >= {
        "inspect_rollback_readiness",
        "inspect_regression_gate_requirements",
        "confirm_no_runtime_application",
    }
    assert checklist["non_claims"] == NON_CLAIMS


def test_review_packet_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_packet(paths)
    packet = json.loads(paths["review_packet"].read_text(encoding="utf-8"))
    packet["runtime_application_performed"] = True
    paths["review_packet"].write_text(json.dumps(packet), encoding="utf-8")

    result = validate_controlled_runtime_calibration_dry_run_review_packet(
        contract_path=paths["contract"],
        review_packet_path=paths["review_packet"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(
        error["error_type"] == "forbidden_field_or_value"
        for error in result["errors"]
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "dry_run_inputs": tmp_path / "dry_run_inputs.json",
        "dry_run_report": tmp_path / "dry_run_report.json",
        "change_request": tmp_path / "change_request.json",
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "phase_freeze": tmp_path / "phase_freeze.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "review_inputs": tmp_path / "review_inputs.json",
        "review_inputs_validation": tmp_path / "review_inputs.validation.json",
        "review_packet": tmp_path / "review_packet.json",
        "review_packet_validation": tmp_path / "review_packet.validation.json",
        "review_summary": tmp_path / "review_summary.json",
        "operator_checklist": tmp_path / "operator_checklist.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_dry_run_review_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )
    paths["model_asset"].write_bytes(b"model fixture")
    gate_refs = [
        {
            "gate_id": "multi_point_regression_matrix_gate",
            "make_target": "tom-v1-verify-multi-point-regression-matrix",
        },
        {
            "gate_id": "protected_sample_point_reviewed_3d_debug_gate",
            "make_target": "tom-v1-verify-reviewed-3d-debug-baseline",
        },
        {
            "gate_id": "gameplay_gate_regression_baseline_gate",
            "make_target": "tom-v1-verify-gameplay-gate-regression-baseline",
        },
        {
            "gate_id": "calibration_sandbox_regression_baseline_gate",
            "make_target": (
                "tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline"
            ),
        },
    ]
    current_settings = {
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
        "runtime_application_status": "not_applied",
    }
    candidate_settings = {
        "candidate_threshold": 0.58,
        "candidate_smoothing_window": 5,
        "candidate_hysteresis_settings": {
            "enter_gameplay_probability": 0.62,
            "exit_gameplay_probability": 0.43,
        },
        "candidate_type": "threshold_candidate",
        "candidate_source": {"candidate_packet_id": "candidate_fixture"},
        "not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }
    selected_candidate_config_ref = {
        "candidate_packet_id": "candidate_fixture",
        "candidate_config_freeze_id": "candidate_config_freeze_fixture",
    }
    rollback_plan_ref = {
        "rollback_plan_id": "rollback_fixture",
        "rollback_plan_version": "v1",
        "rollback_status": "rollback_plan_created",
        "rollback_scope": "restore_prior_runtime_settings",
    }
    paths["dry_run_inputs"].write_text(
        json.dumps(
            {
                "dry_run_input_id": "dry_run_input_fixture",
                "dry_run_input_type": "controlled_runtime_calibration_dry_run_inputs",
                "dry_run_input_version": "v1",
                "generated_at": "2026-06-20T01:00:00+00:00",
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "candidate_settings": candidate_settings,
                "rollback_plan_ref": rollback_plan_ref,
                "regression_gate_requirements": gate_refs,
                "warnings": {"runtime_application_status_not_applied": True},
                "non_claims": {
                    "dry_run_is_not_runtime_calibration": True,
                    "runtime_application_not_performed": True,
                },
            }
        ),
        encoding="utf-8",
    )
    paths["dry_run_report"].write_text(
        json.dumps(
            {
                "dry_run_id": "dry_run_report_fixture",
                "dry_run_type": "controlled_runtime_calibration_dry_run_execution",
                "dry_run_version": "v1",
                "generated_at": "2026-06-20T02:00:00+00:00",
                "source_dry_run_input_path": str(paths["dry_run_inputs"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "candidate_settings": candidate_settings,
                "dry_run_mode": "validate_only",
                "dry_run_status": "dry_run_completed_without_runtime_mutation",
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "rollback_readiness_status": "rollback_plan_present",
                "regression_gate_requirements": gate_refs,
                "structural_comparison_results": [
                    {
                        "comparison_id": "comparison_fixture_1",
                        "comparison_type": "compare_gameplay_segment_counts",
                        "comparison_status": "no_structural_change",
                        "drift_detected": False,
                        "breaking_drift_detected": False,
                        "warnings": {"classifier_correctness_not_assessed": True},
                    },
                    {
                        "comparison_id": "comparison_fixture_2",
                        "comparison_type": "compare_rollback_readiness",
                        "comparison_status": "no_structural_change",
                        "drift_detected": False,
                        "breaking_drift_detected": False,
                        "warnings": {"structural_change_summary": True},
                    },
                ],
                "blockers": ["human_operator_approval_required"],
                "rollback_plan_ref": rollback_plan_ref,
                "warnings": {
                    "controlled_dry_run": True,
                    "runtime_application_status_not_applied": True,
                },
                "non_claims": {
                    "dry_run_is_not_runtime_calibration": True,
                    "runtime_application_not_performed": True,
                },
            }
        ),
        encoding="utf-8",
    )
    paths["change_request"].write_text(
        json.dumps(
            {
                "change_request_id": "change_request_fixture",
                "change_request_type": "controlled_runtime_calibration_change_request",
                "runtime_application_status": "not_applied",
                "current_settings": current_settings,
                "requested_candidate_settings": candidate_settings,
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "rollback_plan": rollback_plan_ref,
                "required_regression_gates": gate_refs,
                "warnings": {"human_operator_review_required": True},
            }
        ),
        encoding="utf-8",
    )
    paths["candidate_config_freeze"].write_text(
        json.dumps(
            {
                "candidate_config_freeze_id": "candidate_config_freeze_fixture",
                "candidate_config_freeze_type": "calibration_candidate_config_freeze",
                "manual_approval_status": "operator_review_required",
                "runtime_application_status": "not_applied",
                "candidate_settings": candidate_settings,
                "warnings": {"candidate_config_freeze_is_review_only": True},
            }
        ),
        encoding="utf-8",
    )
    paths["manual_packet"].write_text(
        json.dumps(
            {
                "manual_approval_packet_id": "manual_packet_fixture",
                "manual_approval_packet_type": "calibration_candidate_manual_approval_packet",
                "operator_review_status": "operator_review_required",
                "runtime_application_status": "not_applied",
                "warnings": {"human_operator_review_required": True},
            }
        ),
        encoding="utf-8",
    )
    for key in (
        "decision_packet",
        "phase_freeze",
        "gameplay_baseline",
        "sandbox_baseline",
    ):
        paths[key].write_text(
            json.dumps(
                {
                    "artifact": key,
                    "runtime_application_status": "not_applied",
                    "warnings": {"classifier_correctness_not_assessed": True},
                }
            ),
            encoding="utf-8",
        )


def _build_review_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_controlled_runtime_calibration_dry_run_review_packet_inputs(
        contract_path=paths["contract"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_dry_run_inputs_path=paths["dry_run_inputs"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["review_inputs"],
    )


def _build_review_packet(paths: dict[str, Path]) -> None:
    _build_review_inputs(paths)
    build_controlled_runtime_calibration_dry_run_review_packet(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["review_inputs"],
        output_path=paths["review_packet"],
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            found.add(str(key))
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        found.add(value)
    return found
