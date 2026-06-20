from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_change_request import (
    CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
    FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_change_request,
    build_controlled_runtime_calibration_change_request_dry_run,
    build_controlled_runtime_calibration_change_request_inputs,
    build_controlled_runtime_calibration_change_request_report,
    export_controlled_runtime_calibration_change_request_contract,
    validate_controlled_runtime_calibration_change_request,
    validate_controlled_runtime_calibration_change_request_dry_run,
    validate_controlled_runtime_calibration_change_request_inputs,
)


def test_export_controlled_runtime_calibration_change_request_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_change_request_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["change_request_scope"]["requires_human_approval"] is True
    assert contract["change_request_scope"]["requires_rollback_plan"] is True
    assert contract["change_request_scope"]["applies_threshold_changes"] is False
    assert contract["change_request_scope"]["updates_runtime_configuration"] is False
    assert contract["change_request_schema"]["requires_runtime_application_status"] == (
        "not_applied"
    )
    assert contract["change_request_schema"]["requires_approval_status"] == (
        "human_approval_required"
    )
    assert contract["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_build_and_validate_controlled_runtime_calibration_change_request_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_change_request_inputs(
        contract_path=paths["contract"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["requested_change_scope"] == "gameplay_gate_threshold_candidate"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["approval_context"]["human_operator_approval_required"] is True
    assert inputs["rollback_context"]["rollback_plan_required"] is True
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS
        & _walk_exact_strings_and_keys(inputs)
    )

    validation = validate_controlled_runtime_calibration_change_request_inputs(
        contract_path=paths["contract"],
        change_request_inputs_path=paths["inputs"],
        output_path=paths["inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_change_request(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_inputs(paths)

    result = build_controlled_runtime_calibration_change_request(
        contract_path=paths["contract"],
        change_request_inputs_path=paths["inputs"],
        output_path=paths["change_request"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["change_request_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE
    )
    assert result["approval_status"] == "human_approval_required"
    assert result["runtime_application_status"] == "not_applied"
    assert result["dry_run_required"] is True
    assert result["rollback_plan_required"] is True

    change_request = json.loads(paths["change_request"].read_text(encoding="utf-8"))
    assert change_request["change_request_status"] == "ready_for_human_approval_review"
    assert change_request["requested_change_scope"] == "gameplay_gate_threshold_candidate"
    assert change_request["requested_candidate_settings"]["candidate_threshold"] == 0.58
    assert change_request["rollback_plan"]["rollback_status"] == "rollback_plan_created"
    assert change_request["warnings"]["runtime_application_status_not_applied"] is True
    assert change_request["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS
        & _walk_exact_strings_and_keys(change_request)
    )

    validation = validate_controlled_runtime_calibration_change_request(
        contract_path=paths["contract"],
        change_request_path=paths["change_request"],
        output_path=paths["change_request_validation"],
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["tracked_exports"] == []


def test_build_and_validate_controlled_runtime_calibration_dry_run(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_change_request(paths)

    result = build_controlled_runtime_calibration_change_request_dry_run(
        contract_path=paths["contract"],
        change_request_path=paths["change_request"],
        output_path=paths["dry_run"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["dry_run_type"] == CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE
    assert result["dry_run_status"] == "dry_run_plan_created"
    assert result["runtime_application_status"] == "not_applied"

    dry_run = json.loads(paths["dry_run"].read_text(encoding="utf-8"))
    assert dry_run["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert dry_run["dry_run_mode"] == "structural_dry_run"
    assert dry_run["expected_structural_changes"]["runtime_config_changes"] is False
    assert dry_run["expected_structural_changes"]["model_asset_changes"] is False
    assert dry_run["rollback_plan"]["rollback_status"] == "rollback_plan_created"
    assert dry_run["non_claims"]["runtime_application_not_performed"] is True

    validation = validate_controlled_runtime_calibration_change_request_dry_run(
        contract_path=paths["contract"],
        dry_run_path=paths["dry_run"],
        output_path=paths["dry_run_validation"],
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0


def test_build_controlled_runtime_calibration_change_request_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_dry_run(paths)

    result = build_controlled_runtime_calibration_change_request_report(
        contract_path=paths["contract"],
        change_request_path=paths["change_request"],
        dry_run_path=paths["dry_run"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 20, 4, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T04:00:00+00:00"
    assert report["summary"]["runtime_application_status"] == "not_applied"
    assert report["summary"]["dry_run_status"] == "dry_run_plan_created"
    assert report["summary"]["rollback_plan_status"] == "rollback_plan_created"
    assert report["non_claims"] == NON_CLAIMS


def test_change_request_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_change_request(paths)
    change_request = json.loads(paths["change_request"].read_text(encoding="utf-8"))
    change_request["threshold_applied"] = True
    paths["change_request"].write_text(json.dumps(change_request), encoding="utf-8")

    result = validate_controlled_runtime_calibration_change_request(
        contract_path=paths["contract"],
        change_request_path=paths["change_request"],
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
        "phase_freeze": tmp_path / "phase_freeze.json",
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "evaluation_report": tmp_path / "evaluation_report.json",
        "regression_verification": tmp_path / "regression_verification.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "change_request": tmp_path / "change_request.json",
        "change_request_validation": tmp_path / "change_request.validation.json",
        "dry_run": tmp_path / "dry_run.json",
        "dry_run_validation": tmp_path / "dry_run.validation.json",
        "report": tmp_path / "report.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_change_request_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )
    paths["model_asset"].write_bytes(b"model fixture")
    paths["phase_freeze"].write_text(
        json.dumps(
            {
                "freeze_type": "real_broadcast_gameplay_calibration_decision_phase_freeze",
                "freeze_version": "v1",
                "frozen_contract_refs": [
                    {"path": ".data/contracts/calibration_candidate_config_freeze_v1.json"}
                ],
                "protected_baseline_refs": [
                    {"path": ".data/baselines/gameplay_gate_regression.baseline.json"}
                ],
                "warnings": {"phase_freeze_is_not_truth": True},
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
                "approval_required": True,
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
                    "candidate_smoothing_window": None,
                    "candidate_hysteresis_settings": {},
                    "candidate_type": "threshold_candidate",
                    "candidate_source": {"candidate_packet_id": "candidate_ready"},
                    "not_applied": True,
                    "writes_runtime_configuration": False,
                    "affects_regression_baselines": False,
                },
                "selected_candidate_packet_ref": {
                    "candidate_packet_id": "candidate_ready"
                },
                "approval_blockers": ["missing_operator_review"],
                "supporting_evidence_refs": {
                    "source_decision_packet_path": str(paths["decision_packet"])
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
                "approval_required": True,
                "runtime_application_status": "not_applied",
                "warnings": {"human_operator_approval_required": True},
            }
        ),
        encoding="utf-8",
    )
    for key in (
        "decision_packet",
        "evaluation_report",
        "regression_verification",
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
    build_controlled_runtime_calibration_change_request_inputs(
        contract_path=paths["contract"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["inputs"],
    )


def _build_change_request(paths: dict[str, Path]) -> None:
    _build_inputs(paths)
    build_controlled_runtime_calibration_change_request(
        contract_path=paths["contract"],
        change_request_inputs_path=paths["inputs"],
        output_path=paths["change_request"],
    )


def _build_dry_run(paths: dict[str, Path]) -> None:
    _build_change_request(paths)
    build_controlled_runtime_calibration_change_request_dry_run(
        contract_path=paths["contract"],
        change_request_path=paths["change_request"],
        output_path=paths["dry_run"],
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
