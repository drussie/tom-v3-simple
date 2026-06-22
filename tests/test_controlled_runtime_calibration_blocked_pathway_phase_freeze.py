from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_blocked_pathway_phase_freeze import (  # noqa: E501
    FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_blocked_pathway_completion_summary,
    build_controlled_runtime_calibration_blocked_pathway_phase_freeze,
    build_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs,
    build_controlled_runtime_calibration_future_unblock_readiness_report,
    build_controlled_runtime_calibration_runtime_non_mutation_evidence_report,
    build_controlled_runtime_calibration_successful_pathway_remaining_work_report,
    build_controlled_runtime_calibration_unresolved_human_inputs_report,
    export_controlled_runtime_calibration_blocked_pathway_phase_freeze_contract,
    validate_controlled_runtime_calibration_blocked_pathway_phase_freeze,
    validate_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs,
)


def test_export_blocked_pathway_phase_freeze_contract_is_safe(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.json"

    result = export_controlled_runtime_calibration_blocked_pathway_phase_freeze_contract(
        output_path=contract_path,
        exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    contract = _read(contract_path)
    assert contract["contract_type"] == (
        "controlled_runtime_calibration_blocked_pathway_phase_freeze_contract"
    )
    assert contract["contract_version"] == "v1"
    assert contract["exported_at"] == "2026-06-22T00:00:00+00:00"
    scope = contract["blocked_pathway_phase_freeze_scope"]
    assert scope[
        "bp77_post_reexecution_verification_not_available_packet_is_authoritative_source"
    ] is True
    assert scope["freezes_blocked_pathway_only"] is True
    assert scope["blocked_pathway_complete_for_blocked_purpose"] is True
    assert scope["successful_runtime_calibration_not_completed"] is True
    assert scope["single_candidate_option_does_not_create_selection"] is True
    assert scope["does_not_infer_operator_signoff"] is True
    assert scope["does_not_infer_candidate_selection"] is True
    assert scope["does_not_infer_human_resolution"] is True
    assert scope["does_not_infer_final_gate_result"] is True
    assert scope["does_not_infer_reexecution_approval"] is True
    assert scope["does_not_infer_runtime_reexecution_output"] is True
    assert scope["does_not_execute_runtime_application"] is True
    assert scope["does_not_write_runtime_config"] is True
    assert scope["does_not_create_production_config"] is True
    assert scope["does_not_modify_model_weights"] is True
    assert scope["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS & _walk(contract))


def test_current_blocked_pathway_phase_freeze_completes_blocked_path_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = build_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 22, 1, 0, tzinfo=UTC),
    )

    assert inputs_result["ok"] is True
    assert inputs_result["blocked_pathway_phase_freeze_status"] == (
        "blocked_pathway_phase_freeze_completed"
    )
    assert inputs_result["blocked_pathway_completion_status"] == (
        "complete_for_blocked_pathway"
    )
    assert inputs_result["successful_pathway_completion_status"] == (
        "incomplete_pending_explicit_human_resolution"
    )
    assert inputs_result["successful_calibration_application_status"] == "not_completed"
    assert inputs_result["human_resolution_status"] == "human_resolution_missing"
    assert inputs_result["final_gate_rerun_status"] == "final_gate_rerun_not_performed"
    assert inputs_result["reexecution_status"] == "reexecution_not_performed"
    assert inputs_result["post_reexecution_verification_status"] == (
        "post_reexecution_verification_not_available"
    )
    assert inputs_result["runtime_application_status"] == "not_executed"
    assert inputs_result["runtime_config_changed"] is False
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["candidate_option_count"] == 1

    assert (
        validate_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 22, 1, 5, tzinfo=UTC),
        )["ok"]
        is True
    )

    result = build_controlled_runtime_calibration_blocked_pathway_phase_freeze(
        contract_path=paths["contract"],
        blocked_pathway_phase_freeze_inputs_path=paths["inputs"],
        output_path=paths["freeze"],
        generated_at=datetime(2026, 6, 22, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["blocked_pathway_phase_freeze_status"] == (
        "blocked_pathway_phase_freeze_completed"
    )
    assert result["blocked_pathway_completion_status"] == "complete_for_blocked_pathway"
    assert result["successful_calibration_application_status"] == "not_completed"
    assert result["runtime_application_status"] == "not_executed"
    assert result["runtime_config_changed"] is False
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"

    freeze = _read(paths["freeze"])
    assert freeze["non_claims"] == NON_CLAIMS
    assert freeze["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert freeze["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert "stop_blocked_calibration_pathway" in freeze["next_action_recommendation"]
    assert "successful_pathway_requires_new_human_resolution_cycle" in (
        freeze["next_action_recommendation"]
    )
    assert freeze["blocked_pathway_completion_summary"][
        "complete_for_blocked_pathway"
    ] is True
    assert freeze["blocked_pathway_completion_summary"][
        "successful_runtime_calibration_not_completed"
    ] is True
    assert freeze["unresolved_human_inputs_report"][
        "explicit_human_resolution_provided"
    ] is False
    assert freeze["unresolved_human_inputs_report"]["operator_signoff_provided"] is False
    assert freeze["unresolved_human_inputs_report"]["selected_candidate_supplied"] is False
    assert freeze["runtime_non_mutation_evidence_report"][
        "runtime_application_command_not_executed"
    ] is True
    assert freeze["runtime_non_mutation_evidence_report"]["runtime_config_changed"] is False
    assert freeze["successful_pathway_remaining_work_report"][
        "successful_runtime_calibration_not_completed"
    ] is True
    assert freeze["future_unblock_readiness_report"]["ready_for_runtime_application"] is False
    assert not (FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS & _walk(freeze))

    assert (
        validate_controlled_runtime_calibration_blocked_pathway_phase_freeze(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["freeze_validation"],
            validated_at=datetime(2026, 6, 22, 2, 5, tzinfo=UTC),
        )["ok"]
        is True
    )
    assert _reports_pass(paths)


def test_phase_freeze_rejects_fabricated_successful_completion(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    build_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs(
        contract_path=paths["contract"],
        output_path=paths["inputs"],
    )
    build_controlled_runtime_calibration_blocked_pathway_phase_freeze(
        contract_path=paths["contract"],
        blocked_pathway_phase_freeze_inputs_path=paths["inputs"],
        output_path=paths["freeze"],
    )
    freeze = _read(paths["freeze"])
    freeze["successful_pathway_completion_status"] = "complete_successful_runtime_calibration"
    freeze["successful_calibration_application_status"] = "completed_structural_only"
    paths["freeze"].write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")

    result = validate_controlled_runtime_calibration_blocked_pathway_phase_freeze(
        contract_path=paths["contract"],
        blocked_pathway_phase_freeze_path=paths["freeze"],
        output_path=paths["freeze_validation"],
    )

    assert result["ok"] is False
    error_codes = {error["code"] for error in result["errors"]}
    assert "successful_pathway_must_not_be_marked_complete_in_blocked_state" in (
        error_codes
    )
    assert "successful_calibration_application_must_not_be_completed" in error_codes


def _reports_pass(paths: dict[str, Path]) -> bool:
    reports = [
        build_controlled_runtime_calibration_blocked_pathway_completion_summary(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["completion_summary"],
        ),
        build_controlled_runtime_calibration_unresolved_human_inputs_report(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["unresolved_human_inputs"],
        ),
        build_controlled_runtime_calibration_runtime_non_mutation_evidence_report(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["runtime_non_mutation"],
        ),
        build_controlled_runtime_calibration_successful_pathway_remaining_work_report(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["successful_remaining_work"],
        ),
        build_controlled_runtime_calibration_future_unblock_readiness_report(
            contract_path=paths["contract"],
            blocked_pathway_phase_freeze_path=paths["freeze"],
            output_path=paths["future_unblock_readiness"],
        ),
    ]
    return all(report["ok"] for report in reports)


def _export_contract(paths: dict[str, Path]) -> None:
    result = export_controlled_runtime_calibration_blocked_pathway_phase_freeze_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 22, 0, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "freeze": tmp_path / "freeze.json",
        "freeze_validation": tmp_path / "freeze.validation.json",
        "completion_summary": tmp_path / "completion-summary.json",
        "unresolved_human_inputs": tmp_path / "unresolved-human-inputs.json",
        "runtime_non_mutation": tmp_path / "runtime-non-mutation.json",
        "successful_remaining_work": tmp_path / "successful-remaining-work.json",
        "future_unblock_readiness": tmp_path / "future-unblock-readiness.json",
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
