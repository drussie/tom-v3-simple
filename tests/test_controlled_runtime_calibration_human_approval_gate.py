from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_human_approval_gate import (
    CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
    FORBIDDEN_APPROVAL_GATE_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_future_application_readiness_report,
    build_controlled_runtime_calibration_human_approval_gate,
    build_controlled_runtime_calibration_human_approval_gate_inputs,
    build_controlled_runtime_calibration_human_approval_summary,
    export_controlled_runtime_calibration_human_approval_gate_contract,
    validate_controlled_runtime_calibration_human_approval_gate,
    validate_controlled_runtime_calibration_human_approval_gate_inputs,
)


def test_export_controlled_runtime_calibration_human_approval_gate_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_human_approval_gate_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["approval_gate_scope"]["consumes_dry_run_review_packet"] is True
    assert contract["approval_gate_scope"]["requires_human_operator_signoff"] is True
    assert contract["approval_gate_scope"]["applies_threshold_changes"] is False
    assert contract["approval_gate_scope"]["updates_runtime_configuration"] is False
    assert contract["approval_gate_scope"]["updates_model_weights"] is False
    assert contract["approval_gate_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["approval_gate_schema"]["required_runtime_application_status"]
        == "not_applied"
    )
    assert contract["approval_gate_schema"]["required_mutation_status"] == (
        "no_runtime_mutation"
    )
    assert contract["warnings"]["controlled_human_approval_gate"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPROVAL_GATE_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_controlled_runtime_calibration_human_approval_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_human_approval_gate_inputs(
        contract_path=paths["contract"],
        source_dry_run_review_packet_path=paths["review_packet"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        operator_identity_ref="operator_fixture",
        operator_review_timestamp="2026-06-20T01:05:00+00:00",
        signoff_status="signoff_recorded_no_runtime_action",
        signoff_notes="reviewed for no-runtime-action gate fixture",
        output_path=paths["gate_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["gate_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["operator_signoff_context"]["human_operator_signoff_required"] is True
    assert inputs["operator_signoff_context"]["signoff_status"] == (
        "signoff_recorded_no_runtime_action"
    )
    assert inputs["future_application_context"]["runtime_application_status"] == (
        "not_applied"
    )
    assert inputs["source_artifact_presence"]["dry_run_review_packet"]["present"] is True
    assert inputs["missing_source_refs"] == []
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPROVAL_GATE_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_human_approval_gate_inputs(
        contract_path=paths["contract"],
        approval_gate_inputs_path=paths["gate_inputs"],
        output_path=paths["gate_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_human_approval_gate(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_gate_inputs(paths, signoff_status="signoff_recorded_no_runtime_action")

    result = build_controlled_runtime_calibration_human_approval_gate(
        contract_path=paths["contract"],
        approval_gate_inputs_path=paths["gate_inputs"],
        output_path=paths["gate"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["approval_gate_type"] == CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE
    assert result["approval_gate_status"] == "approval_gate_created_with_warnings"
    assert result["operator_signoff_status"] == (
        "operator_signoff_recorded_no_runtime_action"
    )
    assert result["future_application_readiness_status"] == (
        "future_application_requires_new_blueprint"
    )
    assert result["runtime_application_status"] == "not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"
    assert result["human_operator_signoff_required"] is True
    assert result["future_blueprint_required_for_runtime_application"] is True

    gate = json.loads(paths["gate"].read_text(encoding="utf-8"))
    assert gate["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert gate["dry_run_review_packet_status"] == "review_packet_created"
    assert gate["structural_summary_status"] == "no_structural_change_observed"
    assert gate["rollback_readiness_status"] == (
        "rollback_ready_for_future_phase_review"
    )
    assert gate["regression_gate_summary_status"] == "gate_refs_present"
    assert gate["blocker_resolution_summary"]["unresolved_blocker_count"] == 0
    assert (
        gate["human_approval_gate_record"][
            "runtime_application_allowed_in_this_blueprint"
        ]
        is False
    )
    assert gate["operator_signoff_record"]["runtime_application_status"] == "not_applied"
    assert gate["future_application_requirements"]["missing_requirements"] == [
        "explicit_runtime_config_change_proposal",
        "dry_run_to_runtime_comparison_plan",
        "post_application_review_plan",
        "post_application_regression_gate",
        "future_baseline_candidate_policy",
    ]
    assert gate["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPROVAL_GATE_TOKENS & _walk_exact_strings_and_keys(gate))

    validation = validate_controlled_runtime_calibration_human_approval_gate(
        contract_path=paths["contract"],
        approval_gate_path=paths["gate"],
        output_path=paths["gate_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"
    assert validation["human_operator_signoff_required"] is True


def test_build_human_approval_summary_and_future_readiness_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_gate(paths, signoff_status="signoff_required")

    summary_result = build_controlled_runtime_calibration_human_approval_summary(
        contract_path=paths["contract"],
        approval_gate_path=paths["gate"],
        output_path=paths["summary"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert summary_result["ok"] is True
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    assert summary["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert summary["approval_gate_status"] == "approval_gate_waiting_for_operator_signoff"
    assert summary["runtime_application_status"] == "not_applied"
    assert summary["mutation_status"] == "no_runtime_mutation"
    assert summary["human_operator_signoff_required"] is True
    assert summary["future_blueprint_required_for_runtime_application"] is True
    assert summary["non_claims"] == NON_CLAIMS

    readiness_result = (
        build_controlled_runtime_calibration_future_application_readiness_report(
            contract_path=paths["contract"],
            approval_gate_path=paths["gate"],
            output_path=paths["readiness_report"],
            generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
        )
    )
    assert readiness_result["ok"] is True
    readiness = json.loads(paths["readiness_report"].read_text(encoding="utf-8"))
    assert readiness["future_application_readiness_status"] == (
        "future_application_not_ready"
    )
    assert readiness["runtime_application_status"] == "not_applied"
    assert readiness["production_config_status"] == "not_created"
    assert readiness["baseline_update_status"] == "not_replaced"
    assert readiness["model_update_status"] == "not_modified"
    assert readiness["non_claims"] == NON_CLAIMS


def test_human_approval_gate_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_gate(paths)
    gate = json.loads(paths["gate"].read_text(encoding="utf-8"))
    gate["runtime_application_performed"] = True
    paths["gate"].write_text(json.dumps(gate), encoding="utf-8")

    result = validate_controlled_runtime_calibration_human_approval_gate(
        contract_path=paths["contract"],
        approval_gate_path=paths["gate"],
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
        "review_packet": tmp_path / "review_packet.json",
        "dry_run_report": tmp_path / "dry_run_report.json",
        "change_request": tmp_path / "change_request.json",
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "phase_freeze": tmp_path / "phase_freeze.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "gate_inputs": tmp_path / "gate_inputs.json",
        "gate_inputs_validation": tmp_path / "gate_inputs.validation.json",
        "gate": tmp_path / "gate.json",
        "gate_validation": tmp_path / "gate.validation.json",
        "summary": tmp_path / "summary.json",
        "readiness_report": tmp_path / "readiness_report.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_human_approval_gate_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )
    paths["model_asset"].write_bytes(b"model fixture")
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
    structural_summary = {
        "total_comparisons": 2,
        "structural_change_count": 0,
        "breaking_structural_change_count": 0,
        "warning_count": 0,
        "blocked_comparison_count": 0,
        "comparison_types_present": [
            "compare_gameplay_segment_counts",
            "compare_rollback_readiness",
        ],
        "drift_detected": False,
        "breaking_drift_detected": False,
        "summary_status": "no_structural_change_observed",
        "warnings": {"classifier_correctness_not_assessed": True},
    }
    rollback_summary = {
        "rollback_plan_present": True,
        "rollback_plan_status": "rollback_plan_created",
        "rollback_verification_gate_count": 4,
        "rollback_readiness_status": "rollback_ready_for_future_phase_review",
        "blockers": [],
        "warnings": {"rollback_readiness": True},
    }
    gate_summary = {
        "multi_point_regression_required": True,
        "protected_sample_point_gate_required": True,
        "gameplay_gate_regression_required": True,
        "calibration_sandbox_regression_required": True,
        "dry_run_regression_required": True,
        "all_required_gate_refs_present": True,
        "gate_summary_status": "gate_refs_present",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }
    paths["review_packet"].write_text(
        json.dumps(
            {
                "review_packet_id": "review_packet_fixture",
                "review_packet_type": "controlled_runtime_calibration_dry_run_review_packet",
                "review_packet_version": "v1",
                "generated_at": "2026-06-20T02:00:00+00:00",
                "source_review_packet_input_path": str(paths["review_packet"]),
                "source_dry_run_execution_report_path": str(paths["dry_run_report"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "candidate_settings": candidate_settings,
                "dry_run_status": "dry_run_completed_without_runtime_mutation",
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "operator_review_required": True,
                "future_blueprint_required_for_runtime_application": True,
                "structural_comparison_summary": structural_summary,
                "rollback_readiness_summary": rollback_summary,
                "regression_gate_summary": gate_summary,
                "blocker_summary": {
                    "blocker_count": 0,
                    "blockers": [],
                    "human_operator_review_required": True,
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                    "warnings": {"inspect_blockers": True},
                },
                "warning_summary": {"warning_count": 1, "warnings_present": True},
                "review_packet_status": "review_packet_created",
                "next_step_recommendation": "human_review_required",
                "warnings": {
                    "controlled_dry_run_review_packet": True,
                    "runtime_application_status_not_applied": True,
                },
                "non_claims": {"review_packet_is_not_runtime_calibration": True},
            }
        ),
        encoding="utf-8",
    )
    paths["dry_run_report"].write_text(
        json.dumps(
            {
                "dry_run_id": "dry_run_fixture",
                "dry_run_type": "controlled_runtime_calibration_dry_run_execution",
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "warnings": {"runtime_application_status_not_applied": True},
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
                "runtime_application_status": "not_applied",
                "selected_candidate_config_ref": selected_candidate_config_ref,
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


def _build_gate_inputs(
    paths: dict[str, Path],
    *,
    signoff_status: str = "signoff_required",
) -> None:
    _write_sources(paths)
    build_controlled_runtime_calibration_human_approval_gate_inputs(
        contract_path=paths["contract"],
        source_dry_run_review_packet_path=paths["review_packet"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        operator_identity_ref="operator_fixture",
        operator_review_timestamp="2026-06-20T01:05:00+00:00",
        signoff_status=signoff_status,
        output_path=paths["gate_inputs"],
    )


def _build_gate(
    paths: dict[str, Path],
    *,
    signoff_status: str = "signoff_required",
) -> None:
    _build_gate_inputs(paths, signoff_status=signoff_status)
    build_controlled_runtime_calibration_human_approval_gate(
        contract_path=paths["contract"],
        approval_gate_inputs_path=paths["gate_inputs"],
        output_path=paths["gate"],
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
