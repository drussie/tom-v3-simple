from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_explicit_human_resolution_record import (
    build_controlled_runtime_calibration_explicit_human_resolution_record,
    build_controlled_runtime_calibration_explicit_human_resolution_record_inputs,
    export_controlled_runtime_calibration_explicit_human_resolution_record_contract,
)
from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_request_packet import (
    FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_final_gate_rerun_execution_plan,
    build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report,
    build_controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report,
    build_controlled_runtime_calibration_final_gate_rerun_request_blocker_report,
    build_controlled_runtime_calibration_final_gate_rerun_request_packet,
    build_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs,
    export_controlled_runtime_calibration_final_gate_rerun_request_packet_contract,
    validate_controlled_runtime_calibration_final_gate_rerun_request_packet,
    validate_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs,
)
from apps.worker.services.controlled_runtime_calibration_human_resolution_completeness_gate import (
    build_controlled_runtime_calibration_human_resolution_completeness_gate,
    build_controlled_runtime_calibration_human_resolution_completeness_gate_inputs,
    export_controlled_runtime_calibration_human_resolution_completeness_gate_contract,
)


def test_export_final_gate_rerun_request_packet_contract_is_blocked_safe(
    tmp_path: Path,
) -> None:
    contract_path = tmp_path / "contract.json"

    result = export_controlled_runtime_calibration_final_gate_rerun_request_packet_contract(
        output_path=contract_path,
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_final_gate_rerun_request_packet_contract"
    )
    assert contract["exported_at"] == "2026-06-21T00:00:00+00:00"
    scope = contract["final_gate_rerun_request_scope"]
    assert scope["default_state_remains_blocked_without_complete_human_resolution"] is True
    assert scope["single_candidate_option_does_not_create_selection"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_infer_human_resolution"] is True
    assert scope["does_not_execute_final_gate_rerun"] is True
    assert scope["does_not_execute_runtime_application"] is True
    assert scope["does_not_create_production_config"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS & _walk(contract))


def test_current_final_gate_rerun_request_packet_stays_blocked(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_request_contract(paths)

    inputs_result = (
        build_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs(
            contract_path=paths["contract"],
            output_path=paths["inputs"],
            generated_at=datetime(2026, 6, 21, 1, 0, tzinfo=UTC),
        )
    )

    assert inputs_result["ok"] is True
    assert inputs_result["final_gate_rerun_request_status"] == (
        "final_gate_rerun_request_blocked_missing_human_resolution"
    )
    assert inputs_result["human_resolution_completeness_gate_status"] == (
        "human_resolution_completeness_gate_not_ready"
    )
    assert inputs_result["human_resolution_record_status"] == (
        "human_resolution_record_pending_explicit_inputs"
    )
    assert inputs_result["human_resolution_provided_status"] == "human_resolution_not_provided"
    assert inputs_result["human_resolution_completeness_status"] == "human_resolution_incomplete"
    assert inputs_result["missing_input_status"] == "required_human_inputs_missing"
    assert inputs_result["operator_input_completeness_status"] == "operator_inputs_incomplete"
    assert inputs_result["candidate_input_completeness_status"] == "candidate_inputs_incomplete"
    assert inputs_result["final_gate_rerun_execution_status"] == "final_gate_rerun_not_executed"
    assert inputs_result["final_gate_rerun_readiness_status"] == (
        "final_gate_rerun_not_ready_missing_human_resolution"
    )
    assert inputs_result["reexecution_readiness_status"] == (
        "reexecution_not_ready_blockers_unresolved"
    )
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["candidate_option_count"] == 1

    inputs = _read(paths["inputs"])
    assert inputs["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert inputs["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert inputs["production_config_status"] == "not_created"
    assert inputs["baseline_update_status"] == "not_replaced"
    assert inputs["model_update_status"] == "not_modified"
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS & _walk(inputs))

    assert (
        validate_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 21, 1, 5, tzinfo=UTC),
        )["ok"]
        is True
    )

    packet_result = build_controlled_runtime_calibration_final_gate_rerun_request_packet(
        contract_path=paths["contract"],
        final_gate_rerun_request_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 2, 0, tzinfo=UTC),
    )

    assert packet_result["ok"] is True
    assert packet_result["final_gate_rerun_request_status"] == (
        "final_gate_rerun_request_blocked_missing_human_resolution"
    )
    assert packet_result["final_gate_rerun_execution_status"] == "final_gate_rerun_not_executed"

    packet = _read(paths["packet"])
    assert packet["runtime_application_status"] == "not_executed"
    assert packet["runtime_config_changed"] is False
    assert packet["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert packet["production_config_status"] == "not_created"
    assert packet["baseline_update_status"] == "not_replaced"
    assert packet["model_update_status"] == "not_modified"
    assert packet["next_action_recommendation"] == [
        "provide_operator_inputs",
        "provide_selected_candidate_inputs",
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_human_resolution",
    ]
    assert "prepare_final_gate_rerun_execution_blueprint" not in (
        packet["next_action_recommendation"]
    )
    blocker_codes = {
        blocker["blocker_code"] for blocker in packet["blocker_report"]["blockers"]
    }
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
        "final_gate_rerun_not_ready_missing_human_resolution",
    } <= blocker_codes
    assert packet["final_gate_rerun_execution_plan"]["execution_status"] == (
        "final_gate_rerun_not_executed"
    )
    assert packet["reexecution_dependency_report"]["reexecution_readiness_status"] == (
        "reexecution_not_ready_blockers_unresolved"
    )
    assert packet["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS & _walk(packet))

    assert (
        validate_controlled_runtime_calibration_final_gate_rerun_request_packet(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
            validated_at=datetime(2026, 6, 21, 2, 5, tzinfo=UTC),
        )["ok"]
        is True
    )
    assert (
        build_controlled_runtime_calibration_final_gate_rerun_request_blocker_report(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_path=paths["packet"],
            output_path=paths["blocker"],
        )["ok"]
        is True
    )
    assert (
        build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_path=paths["packet"],
            output_path=paths["prerequisite"],
        )["ok"]
        is True
    )
    assert (
        build_controlled_runtime_calibration_final_gate_rerun_execution_plan(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_path=paths["packet"],
            output_path=paths["plan"],
        )["ok"]
        is True
    )
    assert (
        build_controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report(
            contract_path=paths["contract"],
            final_gate_rerun_request_packet_path=paths["packet"],
            output_path=paths["dependency"],
        )["ok"]
        is True
    )


def test_complete_future_human_resolution_allows_request_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_request_contract(paths)
    complete_gate = _build_complete_bp72_gate(tmp_path)

    inputs_result = (
        build_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs(
            contract_path=paths["contract"],
            source_human_resolution_completeness_gate_path=complete_gate,
            output_path=paths["inputs"],
        )
    )
    assert inputs_result["ok"] is True
    assert inputs_result["final_gate_rerun_request_status"] == (
        "final_gate_rerun_request_ready_after_human_resolution"
    )
    assert inputs_result["human_resolution_completeness_gate_status"] == (
        "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    )
    assert inputs_result["human_resolution_completeness_status"] == "human_resolution_complete"
    assert inputs_result["operator_input_completeness_status"] == "operator_inputs_complete"
    assert inputs_result["candidate_input_completeness_status"] == "candidate_inputs_complete"
    assert inputs_result["final_gate_rerun_execution_status"] == "final_gate_rerun_not_executed"
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    packet_result = build_controlled_runtime_calibration_final_gate_rerun_request_packet(
        contract_path=paths["contract"],
        final_gate_rerun_request_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
    )
    assert packet_result["ok"] is True
    assert packet_result["final_gate_rerun_request_status"] == (
        "final_gate_rerun_request_ready_after_human_resolution"
    )
    assert packet_result["final_gate_rerun_execution_status"] == "final_gate_rerun_not_executed"
    assert packet_result["next_action_recommendation"] == [
        "rerun_final_gate_after_human_resolution",
        "prepare_final_gate_rerun_execution_blueprint",
    ]

    packet = _read(paths["packet"])
    assert packet["final_gate_rerun_execution_plan"]["execution_status"] == (
        "final_gate_rerun_execution_deferred_to_future_blueprint"
    )
    assert packet["runtime_application_status"] == "not_executed"
    assert packet["runtime_config_changed"] is False
    assert packet["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert packet["production_config_status"] == "not_created"
    assert packet["baseline_update_status"] == "not_replaced"
    assert packet["model_update_status"] == "not_modified"
    assert packet["reexecution_readiness_status"] == "reexecution_blocked_final_gate_not_rerun"


def _build_complete_bp72_gate(tmp_path: Path) -> Path:
    bp72_contract = tmp_path / "bp72-contract.json"
    bp72_inputs = tmp_path / "bp72-inputs.json"
    bp72_gate = tmp_path / "bp72-gate.json"
    export_result = (
        export_controlled_runtime_calibration_human_resolution_completeness_gate_contract(
            output_path=bp72_contract,
            exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
        )
    )
    assert export_result["ok"] is True
    record_path = _build_complete_bp71_record(tmp_path)
    inputs_result = build_controlled_runtime_calibration_human_resolution_completeness_gate_inputs(
        contract_path=bp72_contract,
        source_explicit_human_resolution_record_path=record_path,
        output_path=bp72_inputs,
    )
    assert inputs_result["ok"] is True
    gate_result = build_controlled_runtime_calibration_human_resolution_completeness_gate(
        contract_path=bp72_contract,
        completeness_gate_inputs_path=bp72_inputs,
        output_path=bp72_gate,
    )
    assert gate_result["ok"] is True
    return bp72_gate


def _build_complete_bp71_record(tmp_path: Path) -> Path:
    bp71_contract = tmp_path / "bp71-contract.json"
    bp71_inputs = tmp_path / "bp71-inputs.json"
    bp71_record = tmp_path / "bp71-record.json"
    export_result = export_controlled_runtime_calibration_explicit_human_resolution_record_contract(
        output_path=bp71_contract,
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )
    assert export_result["ok"] is True
    default_record = _read(
        Path(".data/contracts/controlled_runtime_calibration_explicit_human_resolution_record_v1.json")
    )
    option = default_record["candidate_option_refs"][0]
    selected_ref = json.dumps(
        {
            "path": option["source_path"],
            "candidate_id": option["candidate_id"],
            "candidate_version": option["candidate_version"],
        }
    )
    inputs_result = build_controlled_runtime_calibration_explicit_human_resolution_record_inputs(
        contract_path=bp71_contract,
        explicit_operator_identity_ref="operator:reviewer-1",
        explicit_operator_signoff_timestamp="2026-06-21T04:00:00+00:00",
        explicit_operator_attestation_text="I reviewed the controlled calibration packet.",
        explicit_operator_scope_acknowledgement="acknowledged",
        explicit_selected_candidate_ref=selected_ref,
        explicit_selected_candidate_id=option["candidate_id"],
        explicit_selected_candidate_version=option["candidate_version"],
        explicit_selected_candidate_source_path=option["source_path"],
        explicit_selected_candidate_selection_reason=(
            "operator selected the frozen candidate for final-gate review"
        ),
        explicit_candidate_selection_timestamp="2026-06-21T04:05:00+00:00",
        explicit_operator_reference_for_selection="operator:reviewer-1",
        output_path=bp71_inputs,
        generated_at=datetime(2026, 6, 21, 4, 10, tzinfo=UTC),
    )
    assert inputs_result["ok"] is True
    record_result = build_controlled_runtime_calibration_explicit_human_resolution_record(
        contract_path=bp71_contract,
        human_resolution_record_inputs_path=bp71_inputs,
        output_path=bp71_record,
        generated_at=datetime(2026, 6, 21, 4, 15, tzinfo=UTC),
    )
    assert record_result["ok"] is True
    return bp71_record


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet.validation.json",
        "blocker": tmp_path / "blocker.json",
        "prerequisite": tmp_path / "prerequisite.json",
        "plan": tmp_path / "plan.json",
        "dependency": tmp_path / "dependency.json",
    }


def _export_request_contract(paths: dict[str, Path]) -> None:
    result = export_controlled_runtime_calibration_final_gate_rerun_request_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
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
