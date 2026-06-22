from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_reexecution_request_packet import (
    FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_final_gate_dependency_report,
    build_controlled_runtime_calibration_reexecution_execution_plan,
    build_controlled_runtime_calibration_reexecution_prerequisite_report,
    build_controlled_runtime_calibration_reexecution_request_blocker_report,
    build_controlled_runtime_calibration_reexecution_request_packet,
    build_controlled_runtime_calibration_reexecution_request_packet_inputs,
    build_controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report,
    export_controlled_runtime_calibration_reexecution_request_packet_contract,
    validate_controlled_runtime_calibration_reexecution_request_packet,
    validate_controlled_runtime_calibration_reexecution_request_packet_inputs,
)


def test_export_reexecution_request_packet_contract_is_safe(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.json"

    result = export_controlled_runtime_calibration_reexecution_request_packet_contract(
        output_path=contract_path,
        exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_reexecution_request_packet_contract"
    )
    assert contract["contract_version"] == "v1"
    assert contract["exported_at"] == "2026-06-22T00:00:00+00:00"
    scope = contract["reexecution_request_scope"]
    assert scope["bp74_blocked_result_is_authoritative_source"] is True
    assert scope["default_state_remains_blocked_without_final_gate_rerun_result"] is True
    assert scope["single_candidate_option_does_not_create_selection"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_infer_human_resolution"] is True
    assert scope["does_not_infer_final_gate_result"] is True
    assert scope["does_not_execute_final_gate_rerun"] is True
    assert scope["does_not_execute_runtime_application"] is True
    assert scope["does_not_write_runtime_config"] is True
    assert scope["does_not_create_production_config"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS & _walk(contract))


def test_current_reexecution_request_packet_stays_blocked(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = build_controlled_runtime_calibration_reexecution_request_packet_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 22, 1, 0, tzinfo=UTC),
    )

    assert inputs_result["ok"] is True
    assert inputs_result["reexecution_request_status"] == (
        "reexecution_request_blocked_final_gate_not_rerun"
    )
    assert inputs_result["reexecution_readiness_status"] == (
        "reexecution_blocked_final_gate_not_rerun"
    )
    assert inputs_result["final_gate_rerun_execution_status"] == (
        "final_gate_rerun_execution_blocked_missing_human_resolution"
    )
    assert inputs_result["final_gate_rerun_result_status"] == (
        "final_gate_rerun_result_not_available"
    )
    assert inputs_result["final_gate_rerun_outcome_status"] == "final_gate_rerun_not_performed"
    assert inputs_result["human_resolution_completeness_gate_status"] == (
        "human_resolution_completeness_gate_not_ready"
    )
    assert inputs_result["operator_signoff_status"] == "operator_signoff_required"
    assert inputs_result["selected_candidate_status"] == "selected_candidate_required"
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["candidate_option_count"] == 1

    assert (
        validate_controlled_runtime_calibration_reexecution_request_packet_inputs(
            contract_path=paths["contract"],
            reexecution_request_packet_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 22, 1, 5, tzinfo=UTC),
        )["ok"]
        is True
    )

    result = build_controlled_runtime_calibration_reexecution_request_packet(
        contract_path=paths["contract"],
        reexecution_request_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 22, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["reexecution_request_status"] == (
        "reexecution_request_blocked_final_gate_not_rerun"
    )
    assert result["reexecution_readiness_status"] == (
        "reexecution_blocked_final_gate_not_rerun"
    )
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    packet = _read(paths["packet"])
    assert packet["non_claims"] == NON_CLAIMS
    assert packet["candidate_option_count"] == 1
    assert packet["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["next_action_recommendation"] == [
        "provide_human_resolution_inputs",
        "provide_operator_inputs",
        "provide_selected_candidate_inputs",
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_human_resolution",
    ]
    assert "prepare_reexecution_after_final_gate_rerun" not in (
        packet["next_action_recommendation"]
    )
    blocker_codes = set(packet["blocker_report"]["blocker_codes"])
    assert {
        "final_gate_rerun_not_performed",
        "final_gate_rerun_result_not_available",
        "final_gate_rerun_execution_blocked_missing_human_resolution",
        "human_resolution_completeness_gate_not_ready",
        "missing_operator_identity",
        "missing_selected_candidate_ref",
        "runtime_application_blocked_before_mutation",
    } <= blocker_codes
    assert packet["final_gate_dependency_report"]["final_gate_rerun_performed"] is False
    assert packet["final_gate_dependency_report"][
        "final_gate_rerun_result_available"
    ] is False
    assert packet["final_gate_dependency_report"]["final_gate_dependency_status"] == (
        "final_gate_dependency_unresolved"
    )
    assert packet["reexecution_execution_plan"]["execution_status"] == "not_executed"
    assert packet["runtime_mutation_prevention_report"]["runtime_config_changed"] is False
    assert packet["runtime_mutation_prevention_report"]["application_status"] == "not_executed"
    assert not (FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS & _walk(packet))

    assert (
        validate_controlled_runtime_calibration_reexecution_request_packet(
            contract_path=paths["contract"],
            reexecution_request_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
            validated_at=datetime(2026, 6, 22, 2, 5, tzinfo=UTC),
        )["ok"]
        is True
    )
    assert _reports_pass(paths)


def test_structural_final_gate_result_creates_ready_request_without_mutation(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    performed_bp74_result = _performed_bp74_result(tmp_path)

    inputs = build_controlled_runtime_calibration_reexecution_request_packet_inputs(
        contract_path=paths["contract"],
        source_final_gate_rerun_execution_blocked_result_path=performed_bp74_result,
        output_path=paths["inputs"],
    )
    assert inputs["ok"] is True
    assert inputs["reexecution_request_status"] == (
        "reexecution_request_ready_after_final_gate_rerun"
    )
    assert inputs["reexecution_readiness_status"] == (
        "reexecution_ready_after_final_gate_rerun"
    )
    assert inputs["runtime_application_status"] == "not_executed"
    assert inputs["runtime_config_changed"] is False
    assert inputs["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    result = build_controlled_runtime_calibration_reexecution_request_packet(
        contract_path=paths["contract"],
        reexecution_request_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
    )
    assert result["ok"] is True
    assert result["reexecution_request_status"] == (
        "reexecution_request_ready_after_final_gate_rerun"
    )
    assert result["reexecution_readiness_status"] == (
        "reexecution_ready_after_final_gate_rerun"
    )
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    packet = _read(paths["packet"])
    assert packet["final_gate_dependency_report"]["final_gate_rerun_performed"] is True
    assert packet["final_gate_dependency_report"]["final_gate_rerun_result_available"] is True
    assert packet["final_gate_dependency_report"]["final_gate_dependency_status"] == (
        "final_gate_dependency_satisfied"
    )
    assert packet["reexecution_execution_plan"]["execution_status"] == (
        "runtime_application_deferred_to_future_blueprint"
    )
    assert packet["runtime_mutation_prevention_report"]["runtime_config_changed"] is False
    assert packet["runtime_mutation_prevention_report"]["application_status"] == "not_executed"
    assert packet["next_action_recommendation"] == [
        "rerun_final_gate_after_human_resolution",
        "prepare_reexecution_after_final_gate_rerun",
    ]


def _reports_pass(paths: dict[str, Path]) -> bool:
    report_calls = [
        build_controlled_runtime_calibration_reexecution_request_blocker_report,
        build_controlled_runtime_calibration_reexecution_prerequisite_report,
        build_controlled_runtime_calibration_final_gate_dependency_report,
        build_controlled_runtime_calibration_reexecution_execution_plan,
        build_controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report,
    ]
    for index, report_call in enumerate(report_calls):
        result = report_call(
            contract_path=paths["contract"],
            reexecution_request_packet_path=paths["packet"],
            output_path=paths["reports"] / f"report-{index}.json",
        )
        if result["ok"] is not True:
            return False
    return True


def _performed_bp74_result(tmp_path: Path) -> Path:
    payload = _read(
        Path(
            ".data/contracts/"
            "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_v1.json"
        )
    )
    payload.update(
        {
            "final_gate_rerun_execution_status": (
                "final_gate_rerun_execution_completed_structural_only"
            ),
            "final_gate_rerun_result_status": "final_gate_rerun_result_structural_only",
            "final_gate_rerun_outcome_status": "final_gate_rerun_structural_only",
            "final_gate_rerun_request_status": (
                "final_gate_rerun_request_ready_after_human_resolution"
            ),
            "human_resolution_completeness_gate_status": (
                "human_resolution_completeness_gate_ready_for_final_gate_rerun"
            ),
            "human_resolution_record_status": (
                "human_resolution_record_created_with_complete_explicit_inputs"
            ),
            "human_resolution_provided_status": "human_resolution_explicitly_provided",
            "human_resolution_completeness_status": "human_resolution_complete",
            "missing_input_status": "no_required_inputs_missing",
            "operator_input_completeness_status": "operator_inputs_complete",
            "candidate_input_completeness_status": "candidate_inputs_complete",
            "operator_signoff_status": "operator_signoff_explicitly_recorded",
            "selected_candidate_status": "selected_candidate_explicitly_recorded",
            "runtime_application_status": "not_executed",
            "runtime_config_changed": False,
            "mutation_status": "no_runtime_mutation_due_to_blocker",
            "production_config_status": "not_created",
            "baseline_update_status": "not_replaced",
            "model_update_status": "not_modified",
        }
    )
    path = tmp_path / "performed-bp74-result.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _paths(tmp_path: Path) -> dict[str, Path]:
    reports = tmp_path / "reports"
    reports.mkdir()
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet.validation.json",
        "reports": reports,
    }


def _export_contract(paths: dict[str, Path]) -> None:
    result = export_controlled_runtime_calibration_reexecution_request_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    assert isinstance(payload, dict)
    return payload


def _walk(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            found.add(str(key))
            found.update(_walk(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(_walk(nested))
    elif isinstance(value, str):
        found.add(value)
    return found
