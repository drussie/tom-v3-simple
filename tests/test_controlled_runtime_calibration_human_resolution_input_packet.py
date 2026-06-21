from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_human_resolution_input_packet import (  # noqa: E501
    FORBIDDEN_HUMAN_RESOLUTION_TOKENS,
    HUMAN_RESOLUTION_ATTESTATION_TEXT_TEMPLATE,
    NON_CLAIMS,
    build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report,
    build_controlled_runtime_calibration_human_resolution_input_packet,
    build_controlled_runtime_calibration_human_resolution_input_packet_inputs,
    build_controlled_runtime_calibration_human_resolution_input_template,
    build_controlled_runtime_calibration_human_resolution_readiness_report,
    build_controlled_runtime_calibration_human_resolution_requirements_report,
    export_controlled_runtime_calibration_human_resolution_input_packet_contract,
    validate_controlled_runtime_calibration_human_resolution_input_packet,
    validate_controlled_runtime_calibration_human_resolution_input_packet_inputs,
)


def test_export_human_resolution_contract_is_pending_safe(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.json"

    result = export_controlled_runtime_calibration_human_resolution_input_packet_contract(
        output_path=contract_path,
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_human_resolution_input_packet_contract"
    )
    assert contract["exported_at"] == "2026-06-21T00:00:00+00:00"
    scope = contract["human_resolution_input_scope"]
    assert scope["default_state_remains_pending_without_explicit_human_input"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_select_candidate_from_candidate_options"] is True
    assert scope["does_not_rerun_final_gate"] is True
    assert scope["does_not_execute_application"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_HUMAN_RESOLUTION_TOKENS & _walk_exact_strings_and_keys(contract)
    )


def test_current_human_resolution_packet_stays_pending(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = (
        build_controlled_runtime_calibration_human_resolution_input_packet_inputs(
            contract_path=paths["contract"],
            output_path=paths["inputs"],
            generated_at=datetime(2026, 6, 21, 1, 0, tzinfo=UTC),
        )
    )

    assert inputs_result["ok"] is True
    assert inputs_result["human_resolution_status"] == "human_resolution_input_required"
    assert inputs_result["operator_signoff_status"] == "operator_signoff_required"
    assert (
        inputs_result["operator_attestation_status"] == "operator_attestation_required"
    )
    assert inputs_result["operator_identity_status"] == "operator_identity_required"
    assert inputs_result["operator_timestamp_status"] == "operator_timestamp_required"
    assert inputs_result["selected_candidate_status"] == "selected_candidate_required"
    assert (
        inputs_result["candidate_selection_validation_status"]
        == "candidate_selection_pending_explicit_input"
    )
    assert inputs_result["candidate_option_count"] == 1
    assert inputs_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert (
        inputs_result["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["next_action_recommendation"] == [
        "provide_human_resolution_inputs",
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_human_resolution",
    ]

    inputs = _read(paths["inputs"])
    assert len(inputs["candidate_option_refs"]) == 1
    assert inputs["explicit_operator_identity_ref"] is None
    assert inputs["explicit_operator_attestation_text"] is None
    assert inputs["explicit_selected_candidate_ref"] is None
    assert inputs["explicit_selected_candidate_selection_reason"] is None
    assert inputs["source_bp66_candidate_option_count"] == 1
    assert inputs["source_bp67_signoff_artifact_status"] == (
        "signoff_artifact_created_pending_explicit_operator_input"
    )
    assert inputs["source_bp68_selected_candidate_artifact_status"] == (
        "selected_candidate_artifact_created_pending_explicit_candidate_input"
    )
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
    assert not (
        FORBIDDEN_HUMAN_RESOLUTION_TOKENS & _walk_exact_strings_and_keys(inputs)
    )

    inputs_validation = (
        validate_controlled_runtime_calibration_human_resolution_input_packet_inputs(
            contract_path=paths["contract"],
            human_resolution_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 21, 1, 5, tzinfo=UTC),
        )
    )
    assert inputs_validation["ok"] is True
    assert inputs_validation["status"] == "valid"

    packet_result = build_controlled_runtime_calibration_human_resolution_input_packet(
        contract_path=paths["contract"],
        human_resolution_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 2, 0, tzinfo=UTC),
    )
    assert packet_result["ok"] is True
    assert packet_result["human_resolution_status"] == "human_resolution_input_required"
    assert packet_result["operator_signoff_status"] == "operator_signoff_required"
    assert packet_result["selected_candidate_status"] == "selected_candidate_required"
    assert (
        packet_result["candidate_selection_validation_status"]
        == "candidate_selection_pending_explicit_input"
    )
    assert packet_result["candidate_option_count"] == 1
    assert packet_result["runtime_application_status"] == "not_executed"

    packet = _read(paths["packet"])
    assert packet["operator_identity_ref"] is None
    assert packet["selected_candidate_config_ref"] is None
    assert packet["selected_candidate_settings_summary"] == {}
    assert packet["selected_candidate_provenance"] == {}
    assert packet["runtime_config_changed"] is False
    assert packet["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert packet["runtime_application_status"] == "not_executed"
    requirements = packet["human_resolution_requirements"]["requirements"]
    assert requirements["candidate_option_count_does_not_create_selection"][
        "status"
    ] == "preserved"
    assert requirements["human_resolution_must_be_explicit"]["status"] == "preserved"
    assert requirements["explicit_operator_identity_required"]["provided"] is False
    assert requirements["explicit_selected_candidate_ref_required"]["provided"] is False
    template = packet["human_resolution_input_template"]
    assert template["attestation_text_template"] == HUMAN_RESOLUTION_ATTESTATION_TEXT_TEMPLATE
    assert set(template["template_placeholders"]) >= {
        "operator_identity_ref",
        "operator_signoff_timestamp",
        "operator_attestation_text",
        "operator_scope_acknowledgement",
        "selected_candidate_config_ref",
        "selected_candidate_id",
        "selected_candidate_version",
        "selected_candidate_source_path",
        "selected_candidate_selection_reason",
        "candidate_selection_timestamp",
        "operator_reference_for_selection",
    }
    assert packet["human_resolution_readiness"]["readiness_checks"][
        "human_resolution_explicitly_recorded"
    ] is False
    assert packet["final_gate_rerun_prerequisites"]["prerequisite_checks"][
        "runtime_application_not_executed_by_this_packet"
    ]["status"] == "not_executed"
    assert packet["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_HUMAN_RESOLUTION_TOKENS & _walk_exact_strings_and_keys(packet)
    )

    packet_validation = (
        validate_controlled_runtime_calibration_human_resolution_input_packet(
            contract_path=paths["contract"],
            human_resolution_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
            validated_at=datetime(2026, 6, 21, 2, 5, tzinfo=UTC),
        )
    )
    assert packet_validation["ok"] is True
    assert packet_validation["status"] == "valid"

    requirements_report = (
        build_controlled_runtime_calibration_human_resolution_requirements_report(
            contract_path=paths["contract"],
            human_resolution_packet_path=paths["packet"],
            output_path=paths["requirements"],
            generated_at=datetime(2026, 6, 21, 3, 0, tzinfo=UTC),
        )
    )
    assert requirements_report["ok"] is True
    assert (
        requirements_report["human_resolution_status"]
        == "human_resolution_input_required"
    )

    template_report = (
        build_controlled_runtime_calibration_human_resolution_input_template(
            contract_path=paths["contract"],
            human_resolution_packet_path=paths["packet"],
            output_path=paths["template"],
            generated_at=datetime(2026, 6, 21, 3, 5, tzinfo=UTC),
        )
    )
    assert template_report["ok"] is True

    readiness_report = (
        build_controlled_runtime_calibration_human_resolution_readiness_report(
            contract_path=paths["contract"],
            human_resolution_packet_path=paths["packet"],
            output_path=paths["readiness"],
            generated_at=datetime(2026, 6, 21, 3, 10, tzinfo=UTC),
        )
    )
    assert readiness_report["ok"] is True
    assert (
        readiness_report["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )

    final_gate_report = (
        build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report(
            contract_path=paths["contract"],
            human_resolution_packet_path=paths["packet"],
            output_path=paths["final_gate"],
            generated_at=datetime(2026, 6, 21, 3, 15, tzinfo=UTC),
        )
    )
    assert final_gate_report["ok"] is True
    assert final_gate_report["final_gate_rerun_status"] == "final_gate_rerun_required"


def test_invalid_human_resolution_inputs_are_rejected(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    result = build_controlled_runtime_calibration_human_resolution_input_packet_inputs(
        contract_path=paths["contract"],
        explicit_operator_identity_ref="operator:reviewer-1",
        explicit_selected_candidate_ref="missing_candidate_ref",
        output_path=paths["inputs"],
    )

    assert result["ok"] is False
    assert result["human_resolution_status"] == "human_resolution_invalid"
    assert result["operator_signoff_status"] == "operator_signoff_invalid"
    assert result["selected_candidate_status"] == "selected_candidate_invalid"
    assert {
        error["code"] for error in result["errors"]
    } >= {
        "invalid_explicit_operator_resolution_input",
        "invalid_explicit_selected_candidate_ref",
    }


def _export_contract(paths: dict[str, Path]) -> None:
    result = export_controlled_runtime_calibration_human_resolution_input_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet.validation.json",
        "requirements": tmp_path / "requirements.json",
        "template": tmp_path / "template.json",
        "readiness": tmp_path / "readiness.json",
        "final_gate": tmp_path / "final_gate.json",
    }


def _read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    assert isinstance(payload, dict)
    return payload


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            result.add(str(key))
            result.update(_walk_exact_strings_and_keys(item))
    elif isinstance(value, list):
        for item in value:
            result.update(_walk_exact_strings_and_keys(item))
    elif isinstance(value, str):
        result.add(value)
    return result
