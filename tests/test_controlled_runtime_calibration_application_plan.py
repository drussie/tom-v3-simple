from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_application_plan import (
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
    FORBIDDEN_APPLICATION_PLAN_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_application_plan,
    build_controlled_runtime_calibration_application_plan_inputs,
    build_controlled_runtime_calibration_post_application_verification_plan,
    build_controlled_runtime_calibration_pre_application_gate_report,
    build_controlled_runtime_calibration_rollback_plan_report,
    export_controlled_runtime_calibration_application_plan_contract,
    validate_controlled_runtime_calibration_application_plan,
    validate_controlled_runtime_calibration_application_plan_inputs,
)


def test_export_controlled_runtime_calibration_application_plan_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_application_plan_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["application_plan_scope"]["consumes_human_approval_gate"] is True
    assert contract["application_plan_scope"]["defines_config_delta_proposal"] is True
    assert contract["application_plan_scope"]["applies_threshold_changes"] is False
    assert contract["application_plan_scope"]["updates_runtime_configuration"] is False
    assert contract["application_plan_scope"]["updates_model_weights"] is False
    assert contract["application_plan_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["application_plan_schema"]["required_runtime_application_status"]
        == "not_applied"
    )
    assert contract["application_plan_schema"]["required_mutation_status"] == (
        "no_runtime_mutation"
    )
    assert contract["warnings"]["controlled_application_plan"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPLICATION_PLAN_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_controlled_runtime_calibration_application_plan_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_application_plan_inputs(
        contract_path=paths["contract"],
        source_human_approval_gate_path=paths["human_gate"],
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
        current_runtime_settings_ref="runtime_settings_fixture",
        output_path=paths["plan_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["plan_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["current_threshold"] == 0.55
    assert inputs["proposed_candidate_threshold"] == 0.58
    assert inputs["operator_signoff_ref"]["operator_signoff_status"] == (
        "operator_signoff_recorded_no_runtime_action"
    )
    assert inputs["source_artifact_presence"]["human_approval_gate"]["present"] is True
    assert inputs["missing_source_refs"] == []
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPLICATION_PLAN_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_application_plan_inputs(
        contract_path=paths["contract"],
        application_plan_inputs_path=paths["plan_inputs"],
        output_path=paths["plan_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_application_plan(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_plan_inputs(paths)

    result = build_controlled_runtime_calibration_application_plan(
        contract_path=paths["contract"],
        application_plan_inputs_path=paths["plan_inputs"],
        output_path=paths["plan"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["application_plan_type"] == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE
    assert result["application_plan_status"] == "application_plan_created"
    assert result["pre_application_gate_status"] == "pre_application_gates_defined"
    assert result["rollback_plan_status"] == "rollback_plan_defined"
    assert result["post_application_verification_status"] == (
        "post_application_verification_plan_defined"
    )
    assert result["future_baseline_policy_status"] == (
        "future_baseline_candidate_policy_defined"
    )
    assert result["runtime_application_status"] == "not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"
    assert result["future_blueprint_required_for_runtime_application"] is True

    plan = json.loads(paths["plan"].read_text(encoding="utf-8"))
    assert plan["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert plan["config_delta_proposal"]["delta_status"] == (
        "config_delta_proposed_for_future_blueprint"
    )
    assert plan["config_delta_proposal"]["runtime_application_status"] == "not_applied"
    assert plan["pre_application_gate"]["missing_requirements"] == []
    assert plan["rollback_plan"]["runtime_application_status"] == "not_applied"
    assert (
        plan["post_application_verification_plan"]["verification_status"]
        == "post_application_verification_plan_defined"
    )
    assert plan["future_baseline_candidate_policy"][
        "baseline_not_replaced_in_this_blueprint"
    ] is True
    assert plan["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPLICATION_PLAN_TOKENS & _walk_exact_strings_and_keys(plan))

    validation = validate_controlled_runtime_calibration_application_plan(
        contract_path=paths["contract"],
        application_plan_path=paths["plan"],
        output_path=paths["plan_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"
    assert validation["future_blueprint_required_for_runtime_application"] is True


def test_build_application_plan_reports(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_plan(paths)

    pre_gate_result = build_controlled_runtime_calibration_pre_application_gate_report(
        contract_path=paths["contract"],
        application_plan_path=paths["plan"],
        output_path=paths["pre_gate_report"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert pre_gate_result["ok"] is True
    pre_gate = json.loads(paths["pre_gate_report"].read_text(encoding="utf-8"))
    assert pre_gate["pre_application_gate_status"] == "pre_application_gates_defined"
    assert pre_gate["runtime_application_status"] == "not_applied"

    rollback_result = build_controlled_runtime_calibration_rollback_plan_report(
        contract_path=paths["contract"],
        application_plan_path=paths["plan"],
        output_path=paths["rollback_report"],
        generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
    )
    assert rollback_result["ok"] is True
    rollback = json.loads(paths["rollback_report"].read_text(encoding="utf-8"))
    assert rollback["rollback_status"] == "rollback_plan_defined"
    assert rollback["mutation_status"] == "no_runtime_mutation"

    verification_result = (
        build_controlled_runtime_calibration_post_application_verification_plan(
            contract_path=paths["contract"],
            application_plan_path=paths["plan"],
            output_path=paths["verification_plan"],
            generated_at=datetime(2026, 6, 20, 3, 10, tzinfo=UTC),
        )
    )
    assert verification_result["ok"] is True
    verification = json.loads(paths["verification_plan"].read_text(encoding="utf-8"))
    assert verification["verification_status"] == (
        "post_application_verification_plan_defined"
    )
    assert verification["required_operator_review_after_application"] is True
    assert verification["non_claims"] == NON_CLAIMS


def test_application_plan_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_plan(paths)
    plan = json.loads(paths["plan"].read_text(encoding="utf-8"))
    plan["runtime_application_performed"] = True
    paths["plan"].write_text(json.dumps(plan), encoding="utf-8")

    result = validate_controlled_runtime_calibration_application_plan(
        contract_path=paths["contract"],
        application_plan_path=paths["plan"],
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
        "human_gate": tmp_path / "human_gate.json",
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
        "plan_inputs": tmp_path / "plan_inputs.json",
        "plan_inputs_validation": tmp_path / "plan_inputs.validation.json",
        "plan": tmp_path / "plan.json",
        "plan_validation": tmp_path / "plan.validation.json",
        "pre_gate_report": tmp_path / "pre_gate_report.json",
        "rollback_report": tmp_path / "rollback_report.json",
        "verification_plan": tmp_path / "verification_plan.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_application_plan_contract(
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
        "candidate_setting_id": "candidate_setting_fixture",
        "source_proposal_item_id": "proposal_fixture",
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
        "all_required_gate_refs_present": True,
        "gate_summary_status": "gate_refs_present",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }
    blocker_summary = {
        "blocker_summary_status": "no_unresolved_blockers_reported",
        "unresolved_blocker_count": 0,
        "unresolved_blockers": [],
        "operator_review_required": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {"runtime_application_status_not_applied": True},
    }
    paths["human_gate"].write_text(
        json.dumps(
            {
                "approval_gate_id": "human_gate_fixture",
                "approval_gate_type": "controlled_runtime_calibration_human_approval_gate",
                "approval_gate_version": "v1",
                "generated_at": "2026-06-20T02:00:00+00:00",
                "source_approval_gate_input_path": str(paths["human_gate"]),
                "source_dry_run_review_packet_path": str(paths["review_packet"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "candidate_settings": candidate_settings,
                "dry_run_review_packet_status": "review_packet_created",
                "rollback_readiness_status": "rollback_ready_for_future_phase_review",
                "regression_gate_summary_status": "gate_refs_present",
                "blocker_summary_status": "no_unresolved_blockers_reported",
                "operator_signoff_status": "operator_signoff_recorded_no_runtime_action",
                "approval_gate_status": (
                    "approval_gate_human_signoff_recorded_no_runtime_action"
                ),
                "future_application_readiness_status": (
                    "future_application_requires_new_blueprint"
                ),
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "future_blueprint_required_for_runtime_application": True,
                "operator_signoff_record": {
                    "operator_signoff_id": "operator_signoff_fixture",
                    "signoff_status": "signoff_recorded_no_runtime_action",
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "blocker_resolution_summary": blocker_summary,
                "warnings": {"runtime_application_status_not_applied": True},
                "non_claims": {"approval_gate_is_not_runtime_application": True},
            }
        ),
        encoding="utf-8",
    )
    paths["review_packet"].write_text(
        json.dumps(
            {
                "review_packet_id": "review_packet_fixture",
                "review_packet_type": "controlled_runtime_calibration_dry_run_review_packet",
                "review_packet_version": "v1",
                "source_dry_run_execution_report_path": str(paths["dry_run_report"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "candidate_settings": candidate_settings,
                "rollback_readiness_summary": rollback_summary,
                "regression_gate_summary": gate_summary,
                "blocker_summary": {
                    "blocker_count": 0,
                    "blockers": [],
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                    "warnings": {"inspect_blockers": True},
                },
                "review_packet_status": "review_packet_created",
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "warnings": {"controlled_dry_run_review_packet": True},
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
                "mutation_status": "no_runtime_mutation",
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
                "mutation_status": "no_runtime_mutation",
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
                "mutation_status": "no_runtime_mutation",
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
                    "mutation_status": "no_runtime_mutation",
                    "warnings": {"classifier_correctness_not_assessed": True},
                }
            ),
            encoding="utf-8",
        )


def _build_plan_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_controlled_runtime_calibration_application_plan_inputs(
        contract_path=paths["contract"],
        source_human_approval_gate_path=paths["human_gate"],
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
        output_path=paths["plan_inputs"],
    )


def _build_plan(paths: dict[str, Path]) -> None:
    _build_plan_inputs(paths)
    build_controlled_runtime_calibration_application_plan(
        contract_path=paths["contract"],
        application_plan_inputs_path=paths["plan_inputs"],
        output_path=paths["plan"],
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
