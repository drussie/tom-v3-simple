from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_post_reexecution_verification_not_available_packet import (  # noqa: E501
    FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_post_reexecution_final_gate_dependency_report,
    build_controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report,
    build_controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report,
    build_controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report,
    build_controlled_runtime_calibration_post_reexecution_verification_availability_report,
    build_controlled_runtime_calibration_post_reexecution_verification_inputs,
    build_controlled_runtime_calibration_post_reexecution_verification_not_available_packet,
    export_controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract,
    validate_controlled_runtime_calibration_post_reexecution_verification_inputs,
    validate_controlled_runtime_calibration_post_reexecution_verification_not_available_packet,
)


def test_export_post_reexecution_verification_not_available_contract_is_safe(
    tmp_path: Path,
) -> None:
    contract_path = tmp_path / "contract.json"

    result = (
        export_controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract(
            output_path=contract_path,
            exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
        )
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract"
    )
    assert contract["contract_version"] == "v1"
    assert contract["exported_at"] == "2026-06-22T00:00:00+00:00"
    scope = contract["post_reexecution_verification_scope"]
    assert scope["bp76_reexecution_execution_blocked_result_is_authoritative_source"] is True
    assert scope["default_state_not_available_without_runtime_reexecution"] is True
    assert scope["runtime_reexecution_required_before_post_verification"] is True
    assert scope["single_candidate_option_does_not_create_selection"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_infer_human_resolution"] is True
    assert scope["does_not_infer_final_gate_result"] is True
    assert scope["does_not_infer_reexecution_approval"] is True
    assert scope["does_not_infer_runtime_reexecution_output"] is True
    assert scope["does_not_infer_post_reexecution_verification"] is True
    assert scope["does_not_execute_runtime_reexecution"] is True
    assert scope["does_not_execute_runtime_application"] is True
    assert scope["does_not_write_runtime_config"] is True
    assert scope["does_not_create_production_config"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS & _walk(contract))


def test_current_post_reexecution_verification_packet_is_not_available(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = build_controlled_runtime_calibration_post_reexecution_verification_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 22, 1, 0, tzinfo=UTC),
    )

    assert inputs_result["ok"] is True
    assert inputs_result["post_reexecution_verification_status"] == (
        "post_reexecution_verification_not_available"
    )
    assert inputs_result["post_reexecution_verification_reason"] == (
        "runtime_reexecution_not_performed"
    )
    assert inputs_result["post_reexecution_result_status"] == (
        "post_reexecution_result_not_available"
    )
    assert inputs_result["post_reexecution_outcome_status"] == (
        "post_reexecution_not_verified"
    )
    assert inputs_result["reexecution_execution_status"] == (
        "reexecution_execution_blocked_final_gate_not_rerun"
    )
    assert inputs_result["reexecution_result_status"] == "reexecution_result_not_available"
    assert inputs_result["reexecution_outcome_status"] == "reexecution_not_performed"
    assert inputs_result["final_gate_rerun_result_status"] == (
        "final_gate_rerun_result_not_available"
    )
    assert inputs_result["final_gate_rerun_outcome_status"] == (
        "final_gate_rerun_not_performed"
    )
    assert inputs_result["human_resolution_completeness_gate_status"] == (
        "human_resolution_completeness_gate_not_ready"
    )
    assert inputs_result["missing_input_status"] == "required_human_inputs_missing"
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["candidate_option_count"] == 1

    assert (
        validate_controlled_runtime_calibration_post_reexecution_verification_inputs(
            contract_path=paths["contract"],
            post_reexecution_verification_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 22, 1, 5, tzinfo=UTC),
        )["ok"]
        is True
    )

    result = (
        build_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(
            contract_path=paths["contract"],
            post_reexecution_verification_inputs_path=paths["inputs"],
            output_path=paths["packet"],
            generated_at=datetime(2026, 6, 22, 2, 0, tzinfo=UTC),
        )
    )

    assert result["ok"] is True
    assert result["post_reexecution_verification_status"] == (
        "post_reexecution_verification_not_available"
    )
    assert result["post_reexecution_verification_reason"] == (
        "runtime_reexecution_not_performed"
    )
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    packet = _read(paths["packet"])
    assert packet["non_claims"] == NON_CLAIMS
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
        "prepare_controlled_calibration_phase_freeze_blocked",
    ]
    assert "prepare_post_reexecution_verification_after_runtime_execution" not in (
        packet["next_action_recommendation"]
    )
    assert packet["verification_availability_report"][
        "runtime_reexecution_not_performed"
    ] is True
    assert packet["missing_execution_evidence_report"][
        "missing_runtime_reexecution_output"
    ] is True
    assert packet["runtime_non_mutation_evidence_report"][
        "runtime_application_command_not_executed"
    ] is True
    assert packet["runtime_non_mutation_evidence_report"]["runtime_config_changed"] is False
    assert packet["final_gate_dependency_report"][
        "final_gate_dependency_status"
    ] == "final_gate_dependency_unresolved"
    assert packet["phase_freeze_readiness_report"][
        "phase_freeze_recommended_status"
    ] == "blocked_pathway_freeze_ready"
    assert not (FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS & _walk(packet))

    assert (
        validate_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
            validated_at=datetime(2026, 6, 22, 2, 5, tzinfo=UTC),
        )["ok"]
        is True
    )
    assert _reports_pass(paths)


def test_packet_validation_rejects_fabricated_available_verification(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    build_controlled_runtime_calibration_post_reexecution_verification_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
    )
    build_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(
        contract_path=paths["contract"],
        post_reexecution_verification_inputs_path=paths["inputs"],
        output_path=paths["packet"],
    )
    packet = _read(paths["packet"])
    packet["post_reexecution_verification_status"] = (
        "post_reexecution_verification_ready_after_runtime_reexecution"
    )
    paths["packet"].write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")

    result = (
        validate_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
        )
    )

    assert result["ok"] is False
    error_codes = {error["code"] for error in result["errors"]}
    assert "post_reexecution_verification_status_must_match_bp76_state" in error_codes
    assert (
        "post_reexecution_verification_must_be_unavailable_without_runtime_reexecution"
        in error_codes
    )


def _reports_pass(paths: dict[str, Path]) -> bool:
    reports = [
        build_controlled_runtime_calibration_post_reexecution_verification_availability_report(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["availability_report"],
        ),
        build_controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["missing_evidence_report"],
        ),
        build_controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["runtime_non_mutation_report"],
        ),
        build_controlled_runtime_calibration_post_reexecution_final_gate_dependency_report(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["final_gate_dependency_report"],
        ),
        build_controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report(
            contract_path=paths["contract"],
            post_reexecution_verification_not_available_packet_path=paths["packet"],
            output_path=paths["phase_freeze_readiness_report"],
        ),
    ]
    return all(report["ok"] for report in reports)


def _export_contract(paths: dict[str, Path]) -> None:
    result = (
        export_controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract(
            output_path=paths["contract"],
            exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
        )
    )
    assert result["ok"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet.validation.json",
        "availability_report": tmp_path / "availability.json",
        "missing_evidence_report": tmp_path / "missing-evidence.json",
        "runtime_non_mutation_report": tmp_path / "runtime-non-mutation.json",
        "final_gate_dependency_report": tmp_path / "final-gate-dependency.json",
        "phase_freeze_readiness_report": tmp_path / "phase-freeze-readiness.json",
    }


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _walk(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            seen.add(str(key))
            seen.update(_walk(item))
    elif isinstance(value, list):
        for item in value:
            seen.update(_walk(item))
    elif isinstance(value, str):
        seen.add(value)
    return seen
