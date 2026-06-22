from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_execution_blocked_result import (  # noqa: E501
    FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_final_gate_rerun_blocked_reason_report,
    build_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result,
    build_controlled_runtime_calibration_final_gate_rerun_execution_inputs,
    build_controlled_runtime_calibration_final_gate_rerun_execution_precheck_report,
    build_controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report,
    build_controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report,
    build_controlled_runtime_calibration_runtime_mutation_prevention_report,
    export_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract,
    validate_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result,
    validate_controlled_runtime_calibration_final_gate_rerun_execution_inputs,
)


def test_export_final_gate_rerun_execution_blocked_result_contract_is_safe(
    tmp_path: Path,
) -> None:
    contract_path = tmp_path / "contract.json"

    result = (
        export_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract(
            output_path=contract_path,
            exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
        )
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract"
    )
    assert contract["exported_at"] == "2026-06-22T00:00:00+00:00"
    scope = contract["final_gate_rerun_execution_scope"]
    assert scope["default_state_remains_blocked_without_complete_human_resolution"] is True
    assert scope["single_candidate_option_does_not_create_selection"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_infer_human_resolution"] is True
    assert scope["does_not_execute_final_gate_in_blocked_state"] is True
    assert scope["does_not_execute_runtime_application"] is True
    assert scope["does_not_create_production_config"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS & _walk(contract))


def test_current_final_gate_rerun_execution_result_stays_blocked(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = build_controlled_runtime_calibration_final_gate_rerun_execution_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 22, 1, 0, tzinfo=UTC),
    )

    assert inputs_result["ok"] is True
    assert inputs_result["final_gate_rerun_execution_status"] == (
        "final_gate_rerun_execution_blocked_missing_human_resolution"
    )
    assert inputs_result["final_gate_rerun_result_status"] == (
        "final_gate_rerun_result_not_available"
    )
    assert inputs_result["final_gate_rerun_outcome_status"] == "final_gate_rerun_not_performed"
    assert inputs_result["final_gate_rerun_request_status"] == (
        "final_gate_rerun_request_blocked_missing_human_resolution"
    )
    assert inputs_result["human_resolution_completeness_gate_status"] == (
        "human_resolution_completeness_gate_not_ready"
    )
    assert inputs_result["missing_input_status"] == "required_human_inputs_missing"
    assert inputs_result["operator_input_completeness_status"] == "operator_inputs_incomplete"
    assert inputs_result["candidate_input_completeness_status"] == "candidate_inputs_incomplete"
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["candidate_option_count"] == 1

    assert (
        validate_controlled_runtime_calibration_final_gate_rerun_execution_inputs(
            contract_path=paths["contract"],
            final_gate_rerun_execution_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 22, 1, 5, tzinfo=UTC),
        )["ok"]
        is True
    )

    result = build_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result(
        contract_path=paths["contract"],
        final_gate_rerun_execution_inputs_path=paths["inputs"],
        output_path=paths["blocked_result"],
        generated_at=datetime(2026, 6, 22, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["final_gate_rerun_execution_status"] == (
        "final_gate_rerun_execution_blocked_missing_human_resolution"
    )
    assert result["final_gate_rerun_result_status"] == "final_gate_rerun_result_not_available"
    assert result["final_gate_rerun_outcome_status"] == "final_gate_rerun_not_performed"
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    blocked_result = _read(paths["blocked_result"])
    assert blocked_result["non_claims"] == NON_CLAIMS
    assert blocked_result["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert blocked_result["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert blocked_result["next_action_recommendation"] == [
        "provide_operator_inputs",
        "provide_selected_candidate_inputs",
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_human_resolution",
    ]
    assert "prepare_final_gate_rerun_execution_after_human_resolution" not in (
        blocked_result["next_action_recommendation"]
    )
    assert blocked_result["execution_precheck_report"][
        "final_gate_rerun_execution_blocked_before_command_execution"
    ] is True
    assert blocked_result["runtime_mutation_prevention_report"][
        "runtime_config_changed"
    ] is False
    assert blocked_result["non_execution_evidence_report"][
        "final_gate_rerun_command_not_executed"
    ] is True
    assert blocked_result["non_execution_evidence_report"][
        "runtime_application_command_not_executed"
    ] is True
    reason_codes = set(blocked_result["blocked_reason_report"]["blocked_reason_codes"])
    assert {
        "missing_operator_identity",
        "missing_operator_attestation",
        "missing_operator_timestamp",
        "missing_selected_candidate_ref",
        "missing_selected_candidate_source_path",
        "missing_selected_candidate_selection_reason",
        "missing_candidate_selection_timestamp",
        "missing_operator_reference_for_selection",
        "human_resolution_completeness_gate_not_ready",
        "final_gate_rerun_request_blocked_missing_human_resolution",
    } <= reason_codes
    assert not (
        FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS
        & _walk(blocked_result)
    )

    assert (
        validate_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result(
            contract_path=paths["contract"],
            final_gate_rerun_execution_blocked_result_path=paths["blocked_result"],
            output_path=paths["blocked_result_validation"],
            validated_at=datetime(2026, 6, 22, 2, 5, tzinfo=UTC),
        )["ok"]
        is True
    )
    assert _reports_pass(paths)


def test_ready_request_is_deferred_without_execution_or_runtime_mutation(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    ready_packet = _ready_bp73_packet(tmp_path)

    inputs = build_controlled_runtime_calibration_final_gate_rerun_execution_inputs(
        contract_path=paths["contract"],
        source_final_gate_rerun_request_packet_path=ready_packet,
        output_path=paths["inputs"],
    )
    assert inputs["ok"] is True
    assert inputs["final_gate_rerun_execution_status"] == (
        "final_gate_rerun_execution_deferred_to_future_blueprint"
    )
    assert inputs["runtime_application_status"] == "not_executed"
    assert inputs["runtime_config_changed"] is False
    assert inputs["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    result = build_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result(
        contract_path=paths["contract"],
        final_gate_rerun_execution_inputs_path=paths["inputs"],
        output_path=paths["blocked_result"],
    )
    assert result["ok"] is True
    assert result["final_gate_rerun_execution_status"] == (
        "final_gate_rerun_execution_deferred_to_future_blueprint"
    )
    assert result["final_gate_rerun_result_status"] == "final_gate_rerun_result_deferred"
    assert result["final_gate_rerun_outcome_status"] == "final_gate_rerun_deferred"
    assert result["reexecution_readiness_status"] == (
        "reexecution_blocked_final_gate_not_rerun"
    )
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    result_payload = _read(paths["blocked_result"])
    assert result_payload["next_action_recommendation"] == [
        "rerun_final_gate_after_human_resolution",
        "prepare_final_gate_rerun_execution_after_human_resolution",
        "prepare_reexecution_request_packet_after_final_gate_rerun",
    ]
    assert result_payload["non_execution_evidence_report"][
        "final_gate_rerun_command_not_executed"
    ] is True
    assert result_payload["runtime_mutation_prevention_report"][
        "application_status"
    ] == "not_executed"


def _reports_pass(paths: dict[str, Path]) -> bool:
    report_calls = [
        build_controlled_runtime_calibration_final_gate_rerun_execution_precheck_report,
        build_controlled_runtime_calibration_final_gate_rerun_blocked_reason_report,
        build_controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report,
        build_controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report,
        build_controlled_runtime_calibration_runtime_mutation_prevention_report,
    ]
    for index, report_call in enumerate(report_calls):
        result = report_call(
            contract_path=paths["contract"],
            final_gate_rerun_execution_blocked_result_path=paths["blocked_result"],
            output_path=paths["reports"] / f"report-{index}.json",
        )
        if result["ok"] is not True:
            return False
    return True


def _ready_bp73_packet(tmp_path: Path) -> Path:
    packet = _read(
        Path(".data/contracts/controlled_runtime_calibration_final_gate_rerun_request_packet_v1.json")
    )
    packet.update(
        {
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
            "final_gate_rerun_readiness_status": (
                "final_gate_rerun_ready_after_human_resolution"
            ),
            "reexecution_readiness_status": "reexecution_blocked_final_gate_not_rerun",
            "runtime_application_status": "not_executed",
            "runtime_config_changed": False,
            "mutation_status": "no_runtime_mutation_due_to_blocker",
            "production_config_status": "not_created",
            "baseline_update_status": "not_replaced",
            "model_update_status": "not_modified",
        }
    )
    packet["blocker_report"] = {**packet["blocker_report"], "blockers": []}
    packet["blocker_report"]["blocker_count"] = 0
    path = tmp_path / "ready-bp73-packet.json"
    path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _paths(tmp_path: Path) -> dict[str, Path]:
    reports = tmp_path / "reports"
    reports.mkdir()
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "blocked_result": tmp_path / "blocked-result.json",
        "blocked_result_validation": tmp_path / "blocked-result.validation.json",
        "reports": reports,
    }


def _export_contract(paths: dict[str, Path]) -> None:
    result = (
        export_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract(
            output_path=paths["contract"],
            exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
        )
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
