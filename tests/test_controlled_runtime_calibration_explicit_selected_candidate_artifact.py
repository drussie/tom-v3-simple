from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_explicit_selected_candidate_artifact import (  # noqa: E501
    FORBIDDEN_EXPLICIT_SELECTED_CANDIDATE_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_candidate_option_inventory_report,
    build_controlled_runtime_calibration_candidate_selection_requirements_report,
    build_controlled_runtime_calibration_explicit_selected_candidate_artifact,
    build_controlled_runtime_calibration_explicit_selected_candidate_artifact_inputs,
    build_controlled_runtime_calibration_selected_candidate_readiness_report,
    export_controlled_runtime_calibration_explicit_selected_candidate_artifact_contract,
    validate_controlled_runtime_calibration_explicit_selected_candidate_artifact,
    validate_controlled_runtime_calibration_explicit_selected_candidate_artifact_inputs,
)


def test_export_explicit_selected_candidate_artifact_contract_is_pending_safe(
    tmp_path: Path,
) -> None:
    contract_path = tmp_path / "contract.json"

    result = (
        export_controlled_runtime_calibration_explicit_selected_candidate_artifact_contract(
            output_path=contract_path,
            exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
        )
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_explicit_selected_candidate_artifact_contract"
    )
    assert contract["exported_at"] == "2026-06-21T00:00:00+00:00"
    assert contract["selected_candidate_artifact_scope"][
        "default_state_remains_pending_without_explicit_candidate_input"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_select_candidate_from_candidate_options"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_create_operator_signoff"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_rerun_final_gate"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_execute_application"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_modify_model_weights"
    ] is True
    assert contract["selected_candidate_artifact_scope"][
        "does_not_replace_baselines"
    ] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_EXPLICIT_SELECTED_CANDIDATE_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_current_explicit_selected_candidate_artifact_stays_pending(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = (
        build_controlled_runtime_calibration_explicit_selected_candidate_artifact_inputs(
            contract_path=paths["contract"],
            output_path=paths["inputs"],
            generated_at=datetime(2026, 6, 21, 1, 0, tzinfo=UTC),
        )
    )

    assert inputs_result["ok"] is True
    assert inputs_result["selected_candidate_status"] == "selected_candidate_required"
    assert (
        inputs_result["candidate_selection_validation_status"]
        == "candidate_selection_pending_explicit_input"
    )
    assert inputs_result["candidate_option_count"] == 1
    assert inputs_result["operator_signoff_status"] == "operator_signoff_required"
    assert inputs_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert (
        inputs_result["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["next_action_recommendation"] == [
        "provide_explicit_selected_candidate",
        "provide_explicit_operator_signoff",
        "rerun_final_gate_after_signoff_and_candidate_selection",
    ]

    inputs = _read(paths["inputs"])
    assert len(inputs["candidate_option_refs"]) == 1
    assert inputs["explicit_selected_candidate_ref"] is None
    assert inputs["explicit_selected_candidate_id"] is None
    assert inputs["operator_signoff_ref"] is None
    assert inputs["runtime_config_target_ref"]["path"] == (
        ".data/contracts/controlled_runtime_calibration_applied_runtime_config_v1.json"
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
        FORBIDDEN_EXPLICIT_SELECTED_CANDIDATE_TOKENS
        & _walk_exact_strings_and_keys(inputs)
    )

    inputs_validation = (
        validate_controlled_runtime_calibration_explicit_selected_candidate_artifact_inputs(
            contract_path=paths["contract"],
            selected_candidate_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 21, 1, 5, tzinfo=UTC),
        )
    )
    assert inputs_validation["ok"] is True
    assert inputs_validation["status"] == "valid"

    artifact_result = (
        build_controlled_runtime_calibration_explicit_selected_candidate_artifact(
            contract_path=paths["contract"],
            selected_candidate_inputs_path=paths["inputs"],
            output_path=paths["artifact"],
            generated_at=datetime(2026, 6, 21, 2, 0, tzinfo=UTC),
        )
    )
    assert artifact_result["ok"] is True
    assert artifact_result["selected_candidate_artifact_status"] == (
        "selected_candidate_artifact_created_pending_explicit_candidate_input"
    )
    assert artifact_result["selected_candidate_status"] == "selected_candidate_required"
    assert (
        artifact_result["candidate_selection_validation_status"]
        == "candidate_selection_pending_explicit_input"
    )
    assert artifact_result["candidate_option_count"] == 1
    assert artifact_result["operator_signoff_status"] == "operator_signoff_required"
    assert artifact_result["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert artifact_result["runtime_application_status"] == "not_executed"

    artifact = _read(paths["artifact"])
    assert artifact["selected_candidate_config_ref"] is None
    assert artifact["selected_candidate_id"] is None
    assert artifact["selected_candidate_settings_summary"] == {}
    assert artifact["selected_candidate_provenance"] == {}
    assert artifact["operator_signoff_ref"] is None
    assert artifact["candidate_option_inventory"][
        "discovered_candidate_option_count"
    ] == 1
    assert (
        artifact["candidate_option_inventory"]["inventory_status"]
        == "candidate_options_discovered"
    )
    assert artifact["selected_candidate_readiness"]["readiness_checks"][
        "selected_candidate_explicitly_recorded"
    ] is False
    assert artifact["selected_candidate_readiness"]["readiness_checks"][
        "operator_signoff_explicitly_recorded"
    ] is False
    assert artifact["runtime_config_changed"] is False
    assert artifact["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert artifact["runtime_application_status"] == "not_executed"
    assert artifact["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_EXPLICIT_SELECTED_CANDIDATE_TOKENS
        & _walk_exact_strings_and_keys(artifact)
    )

    artifact_validation = (
        validate_controlled_runtime_calibration_explicit_selected_candidate_artifact(
            contract_path=paths["contract"],
            selected_candidate_artifact_path=paths["artifact"],
            output_path=paths["artifact_validation"],
            validated_at=datetime(2026, 6, 21, 2, 5, tzinfo=UTC),
        )
    )
    assert artifact_validation["ok"] is True
    assert artifact_validation["status"] == "valid"

    inventory = build_controlled_runtime_calibration_candidate_option_inventory_report(
        contract_path=paths["contract"],
        selected_candidate_artifact_path=paths["artifact"],
        output_path=paths["inventory"],
        generated_at=datetime(2026, 6, 21, 3, 0, tzinfo=UTC),
    )
    assert inventory["ok"] is True
    assert inventory["discovered_candidate_option_count"] == 1
    assert inventory["inventory_status"] == "candidate_options_discovered"

    requirements = (
        build_controlled_runtime_calibration_candidate_selection_requirements_report(
            contract_path=paths["contract"],
            selected_candidate_artifact_path=paths["artifact"],
            output_path=paths["requirements"],
            generated_at=datetime(2026, 6, 21, 3, 5, tzinfo=UTC),
        )
    )
    assert requirements["ok"] is True
    assert requirements["selected_candidate_status"] == "selected_candidate_required"
    assert requirements["operator_signoff_status"] == "operator_signoff_required"

    readiness = build_controlled_runtime_calibration_selected_candidate_readiness_report(
        contract_path=paths["contract"],
        selected_candidate_artifact_path=paths["artifact"],
        output_path=paths["readiness"],
        generated_at=datetime(2026, 6, 21, 3, 10, tzinfo=UTC),
    )
    assert readiness["ok"] is True
    assert readiness["selected_candidate_status"] == "selected_candidate_required"
    assert (
        readiness["candidate_selection_validation_status"]
        == "candidate_selection_pending_explicit_input"
    )
    assert readiness["operator_signoff_status"] == "operator_signoff_required"
    assert readiness["final_gate_rerun_status"] == "final_gate_rerun_required"
    assert (
        readiness["reexecution_readiness_status"]
        == "reexecution_not_ready_blockers_unresolved"
    )


def test_invalid_explicit_selected_candidate_ref_is_rejected(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    result = (
        build_controlled_runtime_calibration_explicit_selected_candidate_artifact_inputs(
            contract_path=paths["contract"],
            explicit_selected_candidate_ref="missing_candidate_ref",
            output_path=paths["inputs"],
        )
    )

    assert result["ok"] is False
    assert result["selected_candidate_status"] == "selected_candidate_invalid"
    assert (
        result["candidate_selection_validation_status"]
        == "candidate_selection_invalid_unknown_candidate"
    )
    assert {
        error["code"] for error in result["errors"]
    } >= {"invalid_explicit_selected_candidate_ref"}


def _export_contract(paths: dict[str, Path]) -> None:
    result = (
        export_controlled_runtime_calibration_explicit_selected_candidate_artifact_contract(
            output_path=paths["contract"],
            exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
        )
    )
    assert result["ok"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "artifact": tmp_path / "artifact.json",
        "artifact_validation": tmp_path / "artifact.validation.json",
        "inventory": tmp_path / "inventory.json",
        "requirements": tmp_path / "requirements.json",
        "readiness": tmp_path / "readiness.json",
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
