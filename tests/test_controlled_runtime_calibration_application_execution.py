from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_application_execution import (
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION,
    FORBIDDEN_APPLICATION_EXECUTION_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_application_audit_report,
    build_controlled_runtime_calibration_application_execution_inputs,
    build_controlled_runtime_calibration_applied_runtime_config,
    build_controlled_runtime_calibration_post_apply_verification_report,
    build_controlled_runtime_calibration_rollback_package,
    execute_controlled_runtime_calibration_application,
    export_controlled_runtime_calibration_application_execution_contract,
    validate_controlled_runtime_calibration_application_execution,
    validate_controlled_runtime_calibration_application_execution_inputs,
    verify_controlled_runtime_calibration_runtime_readback,
)


def test_export_controlled_runtime_calibration_application_execution_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_application_execution_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION
    )
    contract = _read(paths["contract"])
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["application_execution_scope"]["updates_runtime_configuration"] is True
    assert (
        contract["application_execution_scope"][
            "requires_passed_final_gate_before_staged_delta_application"
        ]
        is True
    )
    assert contract["application_execution_scope"]["creates_production_configuration"] is False
    assert contract["application_execution_scope"]["updates_model_weights"] is False
    assert contract["application_execution_scope"]["replaces_regression_baselines"] is False
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_APPLICATION_EXECUTION_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_validate_and_execute_controlled_application_with_passed_gate(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths, final_gate_status="final_gate_passed_not_applied")
    build_controlled_runtime_calibration_applied_runtime_config(
        output_path=paths["runtime_config"],
        generated_at=datetime(2026, 6, 20, 0, 5, tzinfo=UTC),
    )

    input_result = build_controlled_runtime_calibration_application_execution_inputs(
        contract_path=paths["contract"],
        source_pre_application_final_gate_path=paths["final_gate"],
        source_runtime_application_staging_path=paths["staging"],
        source_application_plan_path=paths["application_plan"],
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
        runtime_config_target_path=paths["runtime_config"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )
    assert input_result["ok"] is True
    inputs = _read(paths["inputs"])
    assert inputs["runtime_config_target_ref"]["exists"] is True
    assert inputs["source_pre_application_final_gate_status"] == (
        "final_gate_passed_not_applied"
    )
    assert inputs["blockers"] == []
    assert not (FORBIDDEN_APPLICATION_EXECUTION_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_application_execution_inputs(
        contract_path=paths["contract"],
        application_execution_inputs_path=paths["inputs"],
        output_path=paths["inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"

    execution_result = execute_controlled_runtime_calibration_application(
        contract_path=paths["contract"],
        application_execution_inputs_path=paths["inputs"],
        output_path=paths["execution"],
        rollback_package_output_path=paths["rollback_package"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert execution_result["ok"] is True
    assert execution_result["application_execution_status"] == (
        "application_executed_controlled_runtime_config_write"
    )
    assert execution_result["runtime_application_status"] == (
        "applied_by_controlled_blueprint"
    )
    assert execution_result["runtime_config_status"] == "updated_by_controlled_application"
    assert execution_result["mutation_status"] == (
        "controlled_runtime_config_mutation_performed"
    )
    assert execution_result["production_config_status"] == "not_created"
    assert execution_result["baseline_update_status"] == "not_replaced"
    assert execution_result["model_update_status"] == "not_modified"
    assert execution_result["atomic_write_status"] == "atomic_write_completed"
    assert execution_result["runtime_readback_status"] == "readback_verified"
    assert execution_result["rollback_package_status"] == "rollback_package_created"
    assert execution_result["runtime_config_target_sha256_before"] != (
        execution_result["runtime_config_target_sha256_after"]
    )

    runtime_config = _read(paths["runtime_config"])
    assert runtime_config["settings"]["threshold"] == 0.62
    assert runtime_config["settings"]["smoothing_window"] == 5
    assert runtime_config["settings"]["hysteresis_settings"] == {
        "enter_gameplay_probability": 0.67,
        "exit_gameplay_probability": 0.5,
    }
    assert runtime_config["config_scope"]["not_production_config"] is True
    assert runtime_config["config_scope"]["not_model_weights"] is True
    assert runtime_config["config_scope"]["not_baseline"] is True
    assert runtime_config["config_scope"]["not_truth"] is True

    execution = _read(paths["execution"])
    assert not (FORBIDDEN_APPLICATION_EXECUTION_TOKENS & _walk_exact_strings_and_keys(execution))
    execution_validation = validate_controlled_runtime_calibration_application_execution(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        output_path=paths["execution_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert execution_validation["ok"] is True
    assert execution_validation["status"] == "valid"


def test_application_execution_reports_from_successful_execution(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_successful_execution(paths)

    readback = verify_controlled_runtime_calibration_runtime_readback(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        runtime_config_target_path=paths["runtime_config"],
        output_path=paths["readback"],
        verified_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert readback["ok"] is True
    assert readback["runtime_readback_status"] == "readback_verified"

    audit = build_controlled_runtime_calibration_application_audit_report(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        output_path=paths["audit"],
        generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
    )
    assert audit["ok"] is True
    assert audit["runtime_config_status"] == "updated_by_controlled_application"

    rollback = build_controlled_runtime_calibration_rollback_package(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        output_path=paths["rollback_package"],
        generated_at=datetime(2026, 6, 20, 3, 10, tzinfo=UTC),
    )
    assert rollback["ok"] is True
    assert rollback["rollback_package_status"] == "rollback_package_created"

    post_apply = build_controlled_runtime_calibration_post_apply_verification_report(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        output_path=paths["post_apply"],
        generated_at=datetime(2026, 6, 20, 3, 15, tzinfo=UTC),
    )
    assert post_apply["ok"] is True
    assert post_apply["post_apply_verification_status"] == "post_apply_verification_passed"
    assert post_apply["runtime_readback_status"] == "readback_verified"


def test_application_execution_blocks_when_final_gate_is_not_passed(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths, final_gate_status="final_gate_blocked_missing_operator_signoff")
    build_controlled_runtime_calibration_applied_runtime_config(
        output_path=paths["runtime_config"],
        generated_at=datetime(2026, 6, 20, 0, 5, tzinfo=UTC),
    )
    before = paths["runtime_config"].read_text(encoding="utf-8")
    _build_inputs(paths)

    result = execute_controlled_runtime_calibration_application(
        contract_path=paths["contract"],
        application_execution_inputs_path=paths["inputs"],
        output_path=paths["execution"],
        rollback_package_output_path=paths["rollback_package"],
        generated_at=datetime(2026, 6, 20, 4, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["application_execution_status"] == (
        "application_blocked_final_gate_not_passed"
    )
    assert result["runtime_application_status"] == "blocked_from_runtime_application"
    assert result["runtime_config_status"] == "unchanged_due_to_blocker"
    assert result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert result["atomic_write_status"] == "atomic_write_blocked"
    assert result["runtime_readback_status"] == "readback_blocked"
    assert result["runtime_config_target_sha256_before"] == (
        result["runtime_config_target_sha256_after"]
    )
    assert paths["runtime_config"].read_text(encoding="utf-8") == before


def test_application_execution_rejects_forbidden_runtime_application_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_successful_execution(paths)
    execution = _read(paths["execution"])
    execution["uncontrolled" + "_runtime_config_update"] = True
    paths["execution"].write_text(json.dumps(execution), encoding="utf-8")

    validation = validate_controlled_runtime_calibration_application_execution(
        contract_path=paths["contract"],
        application_execution_path=paths["execution"],
        output_path=paths["execution_validation"],
        validated_at=datetime(2026, 6, 20, 5, 0, tzinfo=UTC),
    )

    assert validation["ok"] is False
    assert any(error["code"] == "forbidden_key" for error in validation["errors"])


def _build_successful_execution(paths: dict[str, Path]) -> None:
    _write_sources(paths, final_gate_status="final_gate_passed_not_applied")
    build_controlled_runtime_calibration_applied_runtime_config(
        output_path=paths["runtime_config"],
        generated_at=datetime(2026, 6, 20, 0, 5, tzinfo=UTC),
    )
    _build_inputs(paths)
    result = execute_controlled_runtime_calibration_application(
        contract_path=paths["contract"],
        application_execution_inputs_path=paths["inputs"],
        output_path=paths["execution"],
        rollback_package_output_path=paths["rollback_package"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _build_inputs(paths: dict[str, Path]) -> None:
    result = build_controlled_runtime_calibration_application_execution_inputs(
        contract_path=paths["contract"],
        source_pre_application_final_gate_path=paths["final_gate"],
        source_runtime_application_staging_path=paths["staging"],
        source_application_plan_path=paths["application_plan"],
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
        runtime_config_target_path=paths["runtime_config"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )
    assert result["ok"] is True


def _write_sources(paths: dict[str, Path], *, final_gate_status: str) -> None:
    export_controlled_runtime_calibration_application_execution_contract(
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
        "runtime_config_status": "not_updated",
    }
    staged_candidate_settings = {
        "candidate_source": {
            "candidate_packet_id": "candidate_packet_fixture",
            "candidate_setting_id": "candidate_setting_fixture",
            "source_proposal_item_id": "proposal_item_fixture",
        },
        "candidate_type": "fixture_candidate",
        "staged_candidate_threshold": 0.62,
        "staged_candidate_smoothing_window": 5,
        "staged_candidate_hysteresis_settings": {
            "enter_gameplay_probability": 0.67,
            "exit_gameplay_probability": 0.5,
        },
        "staged_not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }
    delta_fields = [
        {
            "field": "threshold",
            "current_value": 0.55,
            "staged_value": 0.62,
            "change_present": True,
            "runtime_config_status": "staged_delta_only",
            "mutation_status": "no_runtime_mutation",
        },
        {
            "field": "smoothing_window",
            "current_value": 3,
            "staged_value": 5,
            "change_present": True,
            "runtime_config_status": "staged_delta_only",
            "mutation_status": "no_runtime_mutation",
        },
        {
            "field": "hysteresis_settings",
            "current_value": current_settings["current_hysteresis_settings"],
            "staged_value": staged_candidate_settings[
                "staged_candidate_hysteresis_settings"
            ],
            "change_present": True,
            "runtime_config_status": "staged_delta_only",
            "mutation_status": "no_runtime_mutation",
        },
    ]
    blockers = (
        []
        if final_gate_status == "final_gate_passed_not_applied"
        else ["human_operator_approval_required"]
    )
    final_gate = {
        "final_gate_id": "final_gate_fixture",
        "final_gate_type": "controlled_runtime_calibration_pre_application_final_gate",
        "final_gate_version": "v1",
        "final_gate_status": final_gate_status,
        "readiness_status": "ready_for_future_runtime_application_blueprint",
        "runtime_application_status": "final_gate_passed_not_applied"
        if final_gate_status == "final_gate_passed_not_applied"
        else "blocked_from_runtime_application",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "source_runtime_application_staging_path": str(paths["staging"]),
        "source_application_plan_path": str(paths["application_plan"]),
        "source_human_approval_gate_path": str(paths["human_gate"]),
        "source_dry_run_review_packet_path": str(paths["review_packet"]),
        "source_dry_run_execution_report_path": str(paths["dry_run_report"]),
        "source_change_request_path": str(paths["change_request"]),
        "selected_candidate_config_ref": staged_candidate_settings["candidate_source"],
        "model_asset_ref": str(paths["model_asset"]),
        "model_asset_sha256": None,
        "current_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "staged_config_delta_ref": {
            "staged_config_delta_id": "staged_delta_fixture",
            "staged_config_delta_type": "controlled_runtime_calibration_staged_config_delta",
            "staged_config_delta_version": "v1",
            "delta_status": "staged_for_future_blueprint",
            "delta_fields": delta_fields,
            "runtime_application_status": "staged_not_applied",
            "runtime_config_status": "staged_delta_only",
            "mutation_status": "no_runtime_mutation",
        },
        "operator_signoff_ref": {
            "operator_signoff_required": True,
            "operator_signoff_artifact_present": (
                final_gate_status == "final_gate_passed_not_applied"
            ),
            "operator_signoff_status": "operator_signoff_recorded",
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "pre_apply_manifest_ref": {
            "pre_apply_manifest_id": "pre_apply_manifest_fixture",
            "manifest_status": "pre_apply_manifest_defined",
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "rollback_staging_ref": {
            "rollback_staging_id": "rollback_staging_fixture",
            "rollback_staging_status": "rollback_staging_record_defined",
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "post_application_verification_staging_ref": {
            "post_application_verification_staging_id": "post_apply_staging_fixture",
            "verification_staging_status": "post_application_verification_staged",
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "future_baseline_policy_ref": {
            "future_baseline_policy_status": (
                "future_baseline_candidate_staging_policy_defined"
            ),
            "baseline_update_status": "not_replaced",
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "required_regression_gates": _required_gates(),
        "required_operator_artifacts": [
            {"artifact": "human_approval_gate", "required": True},
            {"artifact": "operator_signoff_record", "required": True},
        ],
        "blockers": blockers,
        "warnings": {"final_gate_pass_is_not_runtime_application": True},
        "non_claims": {"final_gate_is_not_runtime_application": True},
    }
    _write(paths["final_gate"], final_gate)
    _write(
        paths["staging"],
        {
            "staging_id": "staging_fixture",
            "staging_type": "controlled_runtime_calibration_runtime_application_staging",
            "current_settings": current_settings,
            "staged_candidate_settings": staged_candidate_settings,
            "staged_config_delta": final_gate["staged_config_delta_ref"],
            "selected_candidate_config_ref": staged_candidate_settings["candidate_source"],
            "required_regression_gates": _required_gates(),
            "blockers": blockers,
        },
    )
    _write(paths["application_plan"], {"application_plan_id": "application_plan_fixture"})
    _write(paths["human_gate"], {"approval_gate_id": "human_gate_fixture"})
    _write(paths["review_packet"], {"review_packet_id": "review_packet_fixture"})
    _write(paths["dry_run_report"], {"dry_run_id": "dry_run_fixture"})
    _write(paths["change_request"], {"change_request_id": "change_request_fixture"})
    _write(
        paths["candidate_config_freeze"],
        {"candidate_config_freeze_id": "candidate_freeze_fixture"},
    )
    _write(paths["manual_packet"], {"manual_approval_packet_id": "manual_fixture"})
    _write(paths["decision_packet"], {"decision_packet_id": "decision_fixture"})
    _write(paths["phase_freeze"], {"freeze_id": "phase_freeze_fixture"})
    _write(paths["gameplay_baseline"], {"baseline_type": "gameplay_gate_regression"})
    _write(paths["sandbox_baseline"], {"baseline_type": "calibration_sandbox"})


def _required_gates() -> list[dict[str, Any]]:
    return [
        {"gate": "multi_point_regression_matrix", "required": True},
        {"gate": "protected_sample_point_reviewed_3d_debug", "required": True},
        {"gate": "gameplay_gate_regression_baseline", "required": True},
        {
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "required": True,
        },
    ]


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "runtime_config": tmp_path / "controlled_runtime_calibration_runtime_config.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "execution": tmp_path / "execution.json",
        "execution_validation": tmp_path / "execution.validation.json",
        "rollback_package": tmp_path / "rollback_package.json",
        "readback": tmp_path / "readback.json",
        "audit": tmp_path / "audit.json",
        "post_apply": tmp_path / "post_apply.json",
        "final_gate": tmp_path / "final_gate.json",
        "staging": tmp_path / "staging.json",
        "application_plan": tmp_path / "application_plan.json",
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
        "model_asset": tmp_path / "model.pt",
    }


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    exact: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            exact.add(str(key))
            exact.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, list):
        for child in value:
            exact.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, str):
        exact.add(value)
    return exact
