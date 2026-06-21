from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_blocked_execution_resolution_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION,
    FORBIDDEN_RESOLUTION_PACKET_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_blocked_execution_resolution_packet,
    build_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs,
    build_controlled_runtime_calibration_blocker_resolution_checklist,
    build_controlled_runtime_calibration_candidate_selection_requirements,
    build_controlled_runtime_calibration_final_gate_rerun_plan,
    build_controlled_runtime_calibration_operator_action_plan,
    build_controlled_runtime_calibration_reexecution_readiness_plan,
    export_controlled_runtime_calibration_blocked_execution_resolution_packet_contract,
    validate_controlled_runtime_calibration_blocked_execution_resolution_packet,
    validate_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs,
)


def test_export_blocked_execution_resolution_packet_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_blocked_execution_resolution_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION
    )
    contract = _read(paths["contract"])
    assert contract["exported_at"] == "2026-06-21T00:00:00+00:00"
    assert contract["resolution_packet_scope"]["does_not_write_runtime_config"] is True
    assert contract["resolution_packet_scope"]["does_not_create_operator_signoff"] is True
    assert contract["resolution_packet_scope"]["does_not_select_candidate"] is True
    assert contract["resolution_packet_scope"]["does_not_rerun_final_gate"] is True
    assert contract["resolution_packet_scope"]["does_not_execute_application"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_RESOLUTION_PACKET_TOKENS & _walk_exact_strings_and_keys(contract))


def test_current_bp64_blocked_execution_builds_resolution_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = (
        build_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs(
            contract_path=paths["contract"],
            source_application_execution_review_packet_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_application_execution_review_packet_v1.json"
            ),
            source_application_execution_review_packet_contract_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_application_execution_review_packet_contract_v1.json"
            ),
            model_asset_path="model_assets/tom_v1/view_classifier_gameplay.pt",
            output_path=paths["inputs"],
            generated_at=datetime(2026, 6, 21, 1, 0, tzinfo=UTC),
        )
    )

    assert inputs_result["ok"] is True
    assert inputs_result["status"] == "completed"
    assert inputs_result["application_outcome_status"] == (
        "application_blocked_safely_before_runtime_mutation"
    )
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert "resolve_operator_signoff_before_reapplying" in inputs_result[
        "next_action_recommendation"
    ]
    assert "select_candidate_before_reapplying" in inputs_result[
        "next_action_recommendation"
    ]
    assert "rerun_final_gate_after_resolution" in inputs_result[
        "next_action_recommendation"
    ]

    inputs_validation = (
        validate_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs(
            contract_path=paths["contract"],
            resolution_packet_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 21, 1, 5, tzinfo=UTC),
        )
    )
    assert inputs_validation["ok"] is True
    assert inputs_validation["status"] == "valid"

    packet_result = build_controlled_runtime_calibration_blocked_execution_resolution_packet(
        contract_path=paths["contract"],
        resolution_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 2, 0, tzinfo=UTC),
    )

    assert packet_result["ok"] is True
    assert packet_result["resolution_packet_status"] == (
        "resolution_packet_created_for_blocked_execution"
    )
    assert packet_result["blocker_resolution_status"] == (
        "blockers_identified_resolution_required"
    )
    assert packet_result["operator_action_status"] == "operator_signoff_required"
    assert packet_result["candidate_selection_status"] == "selected_candidate_required"
    assert packet_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert packet_result["reexecution_readiness_status"] == (
        "reexecution_not_ready_blockers_unresolved"
    )

    packet = _read(paths["packet"])
    assert packet["runtime_config_changed"] is False
    assert packet["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["runtime_application_status"] == "blocked_from_runtime_application"
    assert packet["runtime_config_status"] == "unchanged_due_to_blocker"
    assert packet["production_config_status"] == "not_created"
    assert packet["baseline_update_status"] == "not_replaced"
    assert packet["model_update_status"] == "not_modified"
    assert packet["operator_action_plan"]["required_operator_artifacts"][
        "operator_signoff_ref"
    ]["created_by_blueprint_65"] is False
    assert packet["candidate_selection_requirements"]["required_candidate_refs"][
        "selected_candidate_config_ref"
    ]["status"] == "selected_candidate_required"
    assert packet["final_gate_rerun_plan"]["final_gate_rerun_status"] == (
        "final_gate_rerun_required"
    )
    assert packet["reexecution_readiness_plan"]["reexecution_readiness_status"] == (
        "reexecution_not_ready_blockers_unresolved"
    )
    assert packet["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_RESOLUTION_PACKET_TOKENS & _walk_exact_strings_and_keys(packet))

    packet_validation = validate_controlled_runtime_calibration_blocked_execution_resolution_packet(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["packet_validation"],
        validated_at=datetime(2026, 6, 21, 2, 5, tzinfo=UTC),
    )
    assert packet_validation["ok"] is True
    assert packet_validation["status"] == "valid"
    assert packet_validation["resolution_packet_status"] == (
        "resolution_packet_created_for_blocked_execution"
    )

    _assert_generated_reports(paths)


def test_resolution_packet_validation_rejects_forbidden_tokens(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    build_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs(
        contract_path=paths["contract"],
        source_application_execution_review_packet_path=(
            ".data/contracts/"
            "controlled_runtime_calibration_application_execution_review_packet_v1.json"
        ),
        source_application_execution_review_packet_contract_path=(
            ".data/contracts/"
            "controlled_runtime_calibration_application_execution_review_packet_contract_v1.json"
        ),
        output_path=paths["inputs"],
    )
    build_controlled_runtime_calibration_blocked_execution_resolution_packet(
        contract_path=paths["contract"],
        resolution_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
    )

    packet = _read(paths["packet"])
    packet["forbidden_probe"] = "_".join(["model", "updated"])
    _write(paths["packet"], packet)

    result = validate_controlled_runtime_calibration_blocked_execution_resolution_packet(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["packet_validation"],
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(error["code"] == "forbidden_value" for error in result["errors"])


def _assert_generated_reports(paths: dict[str, Path]) -> None:
    checklist = build_controlled_runtime_calibration_blocker_resolution_checklist(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["checklist"],
        generated_at=datetime(2026, 6, 21, 3, 0, tzinfo=UTC),
    )
    assert checklist["ok"] is True
    assert checklist["check_count"] == 14

    operator_plan = build_controlled_runtime_calibration_operator_action_plan(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["operator_plan"],
        generated_at=datetime(2026, 6, 21, 3, 5, tzinfo=UTC),
    )
    assert operator_plan["ok"] is True
    assert operator_plan["operator_action_status"] == "operator_signoff_required"

    candidate_requirements = (
        build_controlled_runtime_calibration_candidate_selection_requirements(
            contract_path=paths["contract"],
            resolution_packet_path=paths["packet"],
            output_path=paths["candidate_requirements"],
            generated_at=datetime(2026, 6, 21, 3, 10, tzinfo=UTC),
        )
    )
    assert candidate_requirements["ok"] is True
    assert candidate_requirements["candidate_selection_status"] == (
        "selected_candidate_required"
    )

    final_gate_plan = build_controlled_runtime_calibration_final_gate_rerun_plan(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["final_gate_plan"],
        generated_at=datetime(2026, 6, 21, 3, 15, tzinfo=UTC),
    )
    assert final_gate_plan["ok"] is True
    assert final_gate_plan["final_gate_rerun_status"] == "final_gate_rerun_required"

    reexecution_plan = build_controlled_runtime_calibration_reexecution_readiness_plan(
        contract_path=paths["contract"],
        resolution_packet_path=paths["packet"],
        output_path=paths["reexecution_plan"],
        generated_at=datetime(2026, 6, 21, 3, 20, tzinfo=UTC),
    )
    assert reexecution_plan["ok"] is True
    assert reexecution_plan["reexecution_readiness_status"] == (
        "reexecution_not_ready_blockers_unresolved"
    )


def _export_contract(paths: dict[str, Path]) -> None:
    result = export_controlled_runtime_calibration_blocked_execution_resolution_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs_validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet_validation.json",
        "checklist": tmp_path / "checklist.json",
        "operator_plan": tmp_path / "operator_plan.json",
        "candidate_requirements": tmp_path / "candidate_requirements.json",
        "final_gate_plan": tmp_path / "final_gate_plan.json",
        "reexecution_plan": tmp_path / "reexecution_plan.json",
    }


def _read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    assert isinstance(payload, dict)
    return payload


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            found.add(str(key))
            found.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, str):
        found.add(value)
    return found
