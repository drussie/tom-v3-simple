from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_dry_run_execution import (
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
    FORBIDDEN_DRY_RUN_EXECUTION_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_dry_run_inputs,
    build_controlled_runtime_calibration_dry_run_rollback_readiness_report,
    build_controlled_runtime_calibration_dry_run_summary,
    export_controlled_runtime_calibration_dry_run_execution_contract,
    run_controlled_runtime_calibration_dry_run,
    validate_controlled_runtime_calibration_dry_run_inputs,
    validate_controlled_runtime_calibration_dry_run_report,
)


def test_export_controlled_runtime_calibration_dry_run_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_dry_run_execution_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["dry_run_scope"]["executes_change_request_in_dry_run_mode"] is True
    assert contract["dry_run_scope"]["applies_threshold_changes"] is False
    assert contract["dry_run_scope"]["updates_runtime_configuration"] is False
    assert contract["dry_run_scope"]["updates_model_weights"] is False
    assert contract["dry_run_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["dry_run_execution_schema"]["required_runtime_application_status"]
        == "not_applied"
    )
    assert (
        contract["dry_run_execution_schema"]["required_mutation_status"]
        == "no_runtime_mutation"
    )
    assert contract["warnings"]["no_runtime_mutation"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_DRY_RUN_EXECUTION_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_controlled_runtime_calibration_dry_run_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_dry_run_inputs(
        contract_path=paths["contract"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["dry_run_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["dry_run_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["dry_run_mode"] == "validate_only"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["current_threshold"] == 0.55
    assert inputs["candidate_threshold"] == 0.58
    assert inputs["rollback_plan_ref"]["rollback_plan_id"] == "rollback_fixture"
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_DRY_RUN_EXECUTION_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_dry_run_inputs(
        contract_path=paths["contract"],
        dry_run_inputs_path=paths["dry_run_inputs"],
        output_path=paths["dry_run_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_run_and_validate_controlled_runtime_calibration_dry_run(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_inputs(paths)

    result = run_controlled_runtime_calibration_dry_run(
        contract_path=paths["contract"],
        dry_run_inputs_path=paths["dry_run_inputs"],
        output_path=paths["dry_run_report"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["dry_run_type"] == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE
    assert result["dry_run_status"] == "dry_run_completed_without_runtime_mutation"
    assert result["runtime_application_status"] == "not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"

    report = json.loads(paths["dry_run_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert report["rollback_readiness_status"] == "rollback_plan_present"
    assert report["blockers"] == ["human_operator_approval_required"]
    assert {
        result["comparison_type"] for result in report["structural_comparison_results"]
    } >= {
        "compare_gameplay_segment_counts",
        "compare_regression_gate_requirements",
        "compare_rollback_readiness",
    }
    assert all(
        result["drift_detected"] is False
        and result["breaking_drift_detected"] is False
        for result in report["structural_comparison_results"]
    )
    assert report["non_claims"]["runtime_application_not_performed"] is True
    assert not (FORBIDDEN_DRY_RUN_EXECUTION_TOKENS & _walk_exact_strings_and_keys(report))

    validation = validate_controlled_runtime_calibration_dry_run_report(
        contract_path=paths["contract"],
        dry_run_report_path=paths["dry_run_report"],
        output_path=paths["dry_run_report_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"


def test_build_summary_and_rollback_readiness_report(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _run_dry_run(paths)

    summary_result = build_controlled_runtime_calibration_dry_run_summary(
        contract_path=paths["contract"],
        dry_run_report_path=paths["dry_run_report"],
        output_path=paths["summary"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert summary_result["ok"] is True
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    assert summary["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert summary["runtime_application_status"] == "not_applied"
    assert summary["mutation_status"] == "no_runtime_mutation"
    assert summary["structural_comparison_count"] == 8
    assert summary["non_claims"] == NON_CLAIMS

    readiness_result = (
        build_controlled_runtime_calibration_dry_run_rollback_readiness_report(
            contract_path=paths["contract"],
            dry_run_report_path=paths["dry_run_report"],
            output_path=paths["rollback_readiness"],
            generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
        )
    )
    assert readiness_result["ok"] is True
    readiness = json.loads(paths["rollback_readiness"].read_text(encoding="utf-8"))
    assert readiness["rollback_readiness_status"] == "rollback_plan_present"
    assert readiness["runtime_application_status"] == "not_applied"
    assert readiness["baseline_update_status"] == "not_replaced"
    assert readiness["model_update_status"] == "not_modified"
    assert readiness["required_verification_gates"] == ["gameplay_gate_regression"]
    assert readiness["non_claims"] == NON_CLAIMS


def test_dry_run_report_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _run_dry_run(paths)
    report = json.loads(paths["dry_run_report"].read_text(encoding="utf-8"))
    report["runtime_application_performed"] = True
    paths["dry_run_report"].write_text(json.dumps(report), encoding="utf-8")

    result = validate_controlled_runtime_calibration_dry_run_report(
        contract_path=paths["contract"],
        dry_run_report_path=paths["dry_run_report"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(
        error["error_type"] == "forbidden_field_or_value"
        for error in result["errors"]
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "change_request": tmp_path / "change_request.json",
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "phase_freeze": tmp_path / "phase_freeze.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "dry_run_inputs": tmp_path / "dry_run_inputs.json",
        "dry_run_inputs_validation": tmp_path / "dry_run_inputs.validation.json",
        "dry_run_report": tmp_path / "dry_run_report.json",
        "dry_run_report_validation": tmp_path / "dry_run_report.validation.json",
        "summary": tmp_path / "summary.json",
        "rollback_readiness": tmp_path / "rollback_readiness.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_dry_run_execution_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )
    paths["model_asset"].write_bytes(b"model fixture")
    paths["change_request"].write_text(
        json.dumps(
            {
                "change_request_id": "change_request_fixture",
                "change_request_type": "controlled_runtime_calibration_change_request",
                "change_request_version": "v1",
                "change_request_status": "ready_for_human_approval_review",
                "approval_status": "human_approval_required",
                "runtime_application_status": "not_applied",
                "current_settings": {
                    "current_threshold": 0.55,
                    "current_smoothing_window": 3,
                    "current_hysteresis_settings": {
                        "enter_gameplay_probability": 0.6,
                        "exit_gameplay_probability": 0.45,
                    },
                },
                "requested_candidate_settings": {
                    "candidate_threshold": 0.58,
                    "candidate_smoothing_window": 5,
                    "candidate_hysteresis_settings": {
                        "enter_gameplay_probability": 0.62,
                        "exit_gameplay_probability": 0.43,
                    },
                    "candidate_type": "threshold_candidate",
                    "candidate_source": {"candidate_packet_id": "candidate_fixture"},
                },
                "selected_candidate_config_ref": {
                    "candidate_packet_id": "candidate_fixture",
                    "candidate_config_freeze_id": "candidate_config_freeze_fixture",
                },
                "required_regression_gates": ["gameplay_gate_regression"],
                "rollback_plan": {
                    "rollback_plan_id": "rollback_fixture",
                    "rollback_plan_version": "v1",
                    "rollback_status": "rollback_plan_created",
                    "rollback_scope": "restore_prior_runtime_settings",
                },
                "warnings": {"runtime_application_status_not_applied": True},
            }
        ),
        encoding="utf-8",
    )
    paths["candidate_config_freeze"].write_text(
        json.dumps(
            {
                "candidate_config_freeze_id": "candidate_config_freeze_fixture",
                "candidate_config_freeze_type": "calibration_candidate_config_freeze",
                "candidate_config_freeze_version": "v1",
                "candidate_config_status": "frozen_for_manual_review",
                "manual_approval_status": "operator_review_required",
                "runtime_application_status": "not_applied",
                "current_settings": {
                    "current_threshold": 0.55,
                    "current_smoothing_window": 3,
                    "current_hysteresis_settings": {
                        "enter_gameplay_probability": 0.6,
                        "exit_gameplay_probability": 0.45,
                    },
                },
                "candidate_settings": {
                    "candidate_threshold": 0.58,
                    "candidate_smoothing_window": 5,
                    "candidate_hysteresis_settings": {
                        "enter_gameplay_probability": 0.62,
                        "exit_gameplay_probability": 0.43,
                    },
                    "candidate_type": "threshold_candidate",
                    "candidate_source": {"candidate_packet_id": "candidate_fixture"},
                    "not_applied": True,
                    "writes_runtime_configuration": False,
                    "affects_regression_baselines": False,
                },
                "warnings": {"candidate_config_freeze_is_not_truth": True},
            }
        ),
        encoding="utf-8",
    )
    paths["manual_packet"].write_text(
        json.dumps(
            {
                "manual_approval_packet_id": "manual_packet_fixture",
                "manual_approval_packet_type": "calibration_candidate_manual_approval_packet",
                "operator_review_status": "operator_review_required",
                "runtime_application_status": "not_applied",
                "warnings": {"human_operator_approval_required": True},
            }
        ),
        encoding="utf-8",
    )
    for key in (
        "decision_packet",
        "phase_freeze",
        "gameplay_baseline",
        "sandbox_baseline",
    ):
        paths[key].write_text(
            json.dumps(
                {
                    "artifact": key,
                    "runtime_application_status": "not_applied",
                    "warnings": {"classifier_correctness_not_assessed": True},
                }
            ),
            encoding="utf-8",
        )


def _build_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_controlled_runtime_calibration_dry_run_inputs(
        contract_path=paths["contract"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["dry_run_inputs"],
    )


def _run_dry_run(paths: dict[str, Path]) -> None:
    _build_inputs(paths)
    run_controlled_runtime_calibration_dry_run(
        contract_path=paths["contract"],
        dry_run_inputs_path=paths["dry_run_inputs"],
        output_path=paths["dry_run_report"],
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            found.add(str(key))
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        found.add(value)
    return found
