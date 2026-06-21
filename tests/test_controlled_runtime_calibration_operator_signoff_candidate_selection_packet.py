from __future__ import annotations

from pathlib import Path

from apps.worker.services.controlled_runtime_calibration_operator_signoff_candidate_selection_packet import (  # noqa: E501
    build_controlled_runtime_calibration_candidate_selection_options,
    build_controlled_runtime_calibration_candidate_selection_validation_report,
    build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet,
    build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs,
    build_controlled_runtime_calibration_operator_signoff_requirements,
    build_controlled_runtime_calibration_resolution_readiness_report,
    export_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract,
    validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet,
    validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs,
)


def test_export_operator_signoff_candidate_selection_contract_is_pending_safe(
    tmp_path: Path,
) -> None:
    contract_path = tmp_path / "contract.json"

    result = export_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract(  # noqa: E501
        output_path=contract_path,
    )

    assert result["ok"] is True
    contract = result["contract"]
    assert (
        contract["contract_type"]
        == "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract"  # noqa: E501
    )
    assert contract["packet_scope"]["does_not_create_operator_signoff"] is True
    assert contract["packet_scope"]["does_not_choose_candidate"] is True
    assert contract["packet_scope"]["does_not_rerun_final_gate"] is True
    assert contract["packet_scope"]["does_not_execute_application"] is True
    assert contract["non_claims"]["packet_does_not_infer_operator_signoff"] is True
    assert contract["non_claims"]["packet_does_not_infer_candidate_selection"] is True


def test_current_packet_stays_pending_without_explicit_refs(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.json"
    inputs_path = tmp_path / "inputs.json"
    inputs_validation_path = tmp_path / "inputs.validation.json"
    packet_path = tmp_path / "packet.json"
    packet_validation_path = tmp_path / "packet.validation.json"
    signoff_requirements_path = tmp_path / "operator_signoff_requirements.json"
    candidate_options_path = tmp_path / "candidate_options.json"
    candidate_validation_path = tmp_path / "candidate_validation.json"
    readiness_path = tmp_path / "resolution_readiness.json"

    export_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract(  # noqa: E501
        output_path=contract_path,
    )
    inputs_result = (
        build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs(  # noqa: E501
            contract_path=contract_path,
            output_path=inputs_path,
        )
    )
    assert inputs_result["ok"] is True
    assert inputs_result["candidate_option_count"] == 1
    assert inputs_result["operator_signoff_status"] == "operator_signoff_required"
    assert inputs_result["candidate_selection_status"] == "selected_candidate_required"
    assert inputs_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    inputs_validation = (
        validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs(  # noqa: E501
            contract_path=contract_path,
            packet_inputs_path=inputs_path,
            output_path=inputs_validation_path,
        )
    )
    assert inputs_validation["ok"] is True
    assert inputs_validation["status"] == "valid"

    packet_result = (
        build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet(
            contract_path=contract_path,
            packet_inputs_path=inputs_path,
            output_path=packet_path,
        )
    )
    assert packet_result["ok"] is True
    assert (
        packet_result["packet_status"]
        == "packet_created_pending_operator_signoff_and_candidate_selection"
    )
    assert packet_result["operator_signoff_status"] == "operator_signoff_required"
    assert packet_result["candidate_selection_status"] == "selected_candidate_required"
    assert packet_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert (
        packet_result["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )
    assert packet_result["next_action_recommendation"] == [
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_signoff_and_candidate_selection",
    ]

    packet_validation = (
        validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet(  # noqa: E501
            contract_path=contract_path,
            packet_path=packet_path,
            output_path=packet_validation_path,
        )
    )
    assert packet_validation["ok"] is True
    assert packet_validation["status"] == "valid"

    signoff_requirements = build_controlled_runtime_calibration_operator_signoff_requirements(  # noqa: E501
        contract_path=contract_path,
        packet_path=packet_path,
        output_path=signoff_requirements_path,
    )
    assert signoff_requirements["ok"] is True
    assert signoff_requirements["operator_signoff_status"] == "operator_signoff_required"

    candidate_options = build_controlled_runtime_calibration_candidate_selection_options(
        contract_path=contract_path,
        packet_path=packet_path,
        output_path=candidate_options_path,
    )
    assert candidate_options["ok"] is True
    assert candidate_options["candidate_option_count"] == 1
    assert candidate_options["candidate_selection_status"] == "selected_candidate_required"

    candidate_validation = (
        build_controlled_runtime_calibration_candidate_selection_validation_report(
            contract_path=contract_path,
            packet_path=packet_path,
            output_path=candidate_validation_path,
        )
    )
    assert candidate_validation["ok"] is True
    assert (
        candidate_validation["candidate_selection_status"]
        == "selected_candidate_required"
    )

    readiness = build_controlled_runtime_calibration_resolution_readiness_report(
        contract_path=contract_path,
        packet_path=packet_path,
        output_path=readiness_path,
    )
    assert readiness["ok"] is True
    assert readiness["operator_signoff_status"] == "operator_signoff_required"
    assert readiness["candidate_selection_status"] == "selected_candidate_required"
    assert readiness["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert (
        readiness["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )


def test_invalid_explicit_selected_candidate_is_rejected(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.json"
    inputs_path = tmp_path / "inputs.json"

    export_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract(  # noqa: E501
        output_path=contract_path,
    )

    result = build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs(  # noqa: E501
        contract_path=contract_path,
        explicit_selected_candidate_ref="missing_candidate_ref",
        output_path=inputs_path,
    )

    assert result["ok"] is False
    assert result["candidate_selection_status"] == "selected_candidate_invalid"
    assert {
        error["code"] for error in result["errors"]
    } >= {"invalid_explicit_selected_candidate_ref"}
