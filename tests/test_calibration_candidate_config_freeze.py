from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.calibration_candidate_config_freeze import (
    CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE,
    CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION,
    CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
    CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE,
    FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS,
    SOURCE_CONTRACT_REFS,
    build_calibration_candidate_config_freeze,
    build_calibration_candidate_config_freeze_inputs,
    build_calibration_candidate_config_freeze_report,
    build_calibration_candidate_manual_approval_packet,
    export_calibration_candidate_config_freeze_contract,
    validate_calibration_candidate_config_freeze,
    validate_calibration_candidate_config_freeze_inputs,
    validate_calibration_candidate_manual_approval_packet,
)


def test_export_calibration_candidate_config_freeze_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_calibration_candidate_config_freeze_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE
    assert (
        result["contract_version"]
        == CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["freeze_scope"]["applies_threshold_changes"] is False
    assert contract["freeze_scope"]["applies_smoothing_changes"] is False
    assert contract["freeze_scope"]["applies_hysteresis_changes"] is False
    assert contract["freeze_scope"]["updates_runtime_configuration"] is False
    assert contract["freeze_scope"]["updates_model_weights"] is False
    assert contract["freeze_scope"]["mutates_regression_baselines"] is False
    assert contract["candidate_config_schema"]["requires_not_applied"] is True
    assert (
        contract["source_contract_refs"][
            "calibration_candidate_decision_packet_contract_version"
        ]
        == "v1"
    )
    assert contract["warnings"]["candidate_config_freeze_is_not_truth"] is True
    assert contract["warnings"]["automatic_approval_not_performed"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_build_and_validate_calibration_candidate_config_freeze_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_calibration_candidate_config_freeze_inputs(
        contract_path=paths["contract"],
        source_decision_packet_path=paths["decision_packet"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_calibration_proposal_path=paths["proposal"],
        source_review_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_corpus_run_path=paths["corpus_run"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["freeze_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    freeze_inputs = json.loads(paths["freeze_inputs"].read_text(encoding="utf-8"))
    assert freeze_inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert freeze_inputs["current_threshold"] == 0.55
    assert freeze_inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert len(freeze_inputs["candidate_packet_refs"]) == 2
    assert (
        freeze_inputs["selected_candidate_packet_ref"]["candidate_packet_id"]
        == "candidate_ready"
    )
    assert freeze_inputs["source_contract_refs"] == SOURCE_CONTRACT_REFS
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
        & _walk_exact_strings_and_keys(freeze_inputs)
    )

    validation = validate_calibration_candidate_config_freeze_inputs(
        contract_path=paths["contract"],
        freeze_inputs_path=paths["freeze_inputs"],
        output_path=paths["freeze_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_calibration_candidate_config_freeze(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_freeze_inputs(paths)

    result = build_calibration_candidate_config_freeze(
        contract_path=paths["contract"],
        freeze_inputs_path=paths["freeze_inputs"],
        output_path=paths["config_freeze"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["candidate_config_freeze_type"] == CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE
    assert result["runtime_application_status"] == "not_applied"
    assert result["approval_required"] is True
    assert result["not_applied"] is True

    freeze = json.loads(paths["config_freeze"].read_text(encoding="utf-8"))
    assert freeze["candidate_config_status"] == "frozen_for_manual_review"
    assert freeze["manual_approval_status"] == "operator_review_required"
    assert freeze["runtime_application_status"] == "not_applied"
    assert freeze["not_applied"] is True
    assert freeze["approval_required"] is True
    assert freeze["candidate_settings"]["candidate_threshold"] == 0.58
    assert freeze["candidate_settings"]["not_applied"] is True
    assert "missing_operator_review" in freeze["approval_blockers"]
    assert freeze["warnings"]["baseline_not_replaced"] is True
    assert freeze["non_claims"]["automatic_rejection_not_performed"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
        & _walk_exact_strings_and_keys(freeze)
    )

    validation = validate_calibration_candidate_config_freeze(
        contract_path=paths["contract"],
        candidate_config_freeze_path=paths["config_freeze"],
        output_path=paths["config_freeze_validation"],
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0


def test_build_and_validate_manual_approval_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_freeze(paths)

    result = build_calibration_candidate_manual_approval_packet(
        contract_path=paths["contract"],
        candidate_config_freeze_path=paths["config_freeze"],
        output_path=paths["manual_packet"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["manual_approval_packet_type"]
        == CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE
    )
    assert result["runtime_application_status"] == "not_applied"

    packet = json.loads(paths["manual_packet"].read_text(encoding="utf-8"))
    assert packet["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert packet["operator_review_status"] == "operator_review_required"
    assert packet["approval_required"] is True
    assert packet["runtime_application_status"] == "not_applied"
    assert {
        item["checklist_item"] for item in packet["operator_checklist"]
    } >= {
        "reviewed_candidate_packet",
        "confirmed_no_runtime_application",
        "confirmed_model_weights_unchanged",
        "confirmed_baselines_unchanged",
        "confirmed_human_approval_required",
    }
    assert {
        action["action_type"] for action in packet["operator_next_actions"]
    } >= {
        "review_candidate_config_freeze",
        "do_not_apply_runtime_change",
        "prepare_future_runtime_change_request",
    }
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
        & _walk_exact_strings_and_keys(packet)
    )

    validation = validate_calibration_candidate_manual_approval_packet(
        contract_path=paths["contract"],
        manual_approval_packet_path=paths["manual_packet"],
        output_path=paths["manual_packet_validation"],
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0


def test_config_freeze_validation_rejects_runtime_application_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_freeze(paths)
    freeze = json.loads(paths["config_freeze"].read_text(encoding="utf-8"))
    freeze["runtime_application_status"] = "future_manual_application_required"
    freeze["threshold_applied"] = True
    paths["config_freeze"].write_text(json.dumps(freeze), encoding="utf-8")

    result = validate_calibration_candidate_config_freeze(
        contract_path=paths["contract"],
        candidate_config_freeze_path=paths["config_freeze"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field_or_value" in error_types
    assert "runtime_application_status_must_remain_not_applied" in error_types


def test_build_calibration_candidate_config_freeze_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_manual_packet(paths)

    result = build_calibration_candidate_config_freeze_report(
        contract_path=paths["contract"],
        candidate_config_freeze_path=paths["config_freeze"],
        manual_approval_packet_path=paths["manual_packet"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 20, 4, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T04:00:00+00:00"
    assert report["candidate_config_summary"]["runtime_application_status"] == (
        "not_applied"
    )
    assert report["candidate_config_summary"]["approval_required"] is True
    assert report["manual_approval_summary"]["approval_required"] is True
    assert report["structural_drift_summary"]["sandbox_regression_status"] == (
        "regression_gate_passed"
    )
    assert report["warnings"]["candidate_config_freeze_is_not_truth"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
        & _walk_exact_strings_and_keys(report)
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "proposal": tmp_path / "proposal.json",
        "evaluation_report": tmp_path / "evaluation_report.json",
        "regression_verification": tmp_path / "regression_verification.json",
        "metrics_report": tmp_path / "metrics_report.json",
        "review_loop_report": tmp_path / "review_loop_report.json",
        "corpus_run": tmp_path / "corpus_run.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "freeze_inputs": tmp_path / "freeze_inputs.json",
        "freeze_inputs_validation": tmp_path / "freeze_inputs.validation.json",
        "config_freeze": tmp_path / "config_freeze.json",
        "config_freeze_validation": tmp_path / "config_freeze.validation.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "manual_packet_validation": tmp_path / "manual_packet.validation.json",
        "report": tmp_path / "report.json",
    }


def _build_freeze_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_calibration_candidate_config_freeze_inputs(
        contract_path=paths["contract"],
        source_decision_packet_path=paths["decision_packet"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_calibration_proposal_path=paths["proposal"],
        source_review_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_corpus_run_path=paths["corpus_run"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["freeze_inputs"],
    )


def _build_freeze(paths: dict[str, Path]) -> None:
    _build_freeze_inputs(paths)
    build_calibration_candidate_config_freeze(
        contract_path=paths["contract"],
        freeze_inputs_path=paths["freeze_inputs"],
        output_path=paths["config_freeze"],
    )


def _build_manual_packet(paths: dict[str, Path]) -> None:
    _build_freeze(paths)
    build_calibration_candidate_manual_approval_packet(
        contract_path=paths["contract"],
        candidate_config_freeze_path=paths["config_freeze"],
        output_path=paths["manual_packet"],
    )


def _write_sources(paths: dict[str, Path]) -> None:
    export_calibration_candidate_config_freeze_contract(output_path=paths["contract"])
    paths["model_asset"].write_bytes(b"model fixture")
    paths["decision_packet"].write_text(json.dumps(_decision_packet()), encoding="utf-8")
    paths["proposal"].write_text(json.dumps(_proposal()), encoding="utf-8")
    paths["evaluation_report"].write_text(
        json.dumps(_evaluation_report()),
        encoding="utf-8",
    )
    paths["regression_verification"].write_text(
        json.dumps(_regression_verification()),
        encoding="utf-8",
    )
    paths["metrics_report"].write_text(json.dumps(_metrics_report()), encoding="utf-8")
    paths["review_loop_report"].write_text(json.dumps({"summary": {}}), encoding="utf-8")
    paths["corpus_run"].write_text(json.dumps({"summary": {}}), encoding="utf-8")
    paths["gameplay_baseline"].write_text(json.dumps({"summary": {}}), encoding="utf-8")
    paths["sandbox_baseline"].write_text(json.dumps({"summary": {}}), encoding="utf-8")


def _decision_packet() -> dict[str, Any]:
    return {
        "decision_packet_id": "decision_packet_fixture_v1",
        "decision_packet_type": "calibration_candidate_decision_packet",
        "decision_packet_version": "v1",
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": _sha256(b"model fixture"),
        "current_settings": _current_settings(),
        "candidate_packets": [
            _candidate_packet(
                "candidate_ready",
                "setting_threshold",
                "proposal_threshold",
                "threshold_candidate",
                "ready_for_operator_review",
                "ready_for_human_decision",
                [],
                [],
                threshold_candidate=0.58,
            ),
            _candidate_packet(
                "candidate_fixture",
                "setting_smoothing",
                "proposal_smoothing",
                "smoothing_window_candidate",
                "blocked_fixture_only_data",
                "blocked_from_runtime_consideration",
                ["fixture_only_review_data"],
                ["fixture_only_review_data"],
                smoothing_window_candidate=5,
            ),
        ],
        "regression_gate_summary": {
            "sandbox_regression_status": "regression_gate_passed",
            "baseline_comparison_status": "no_structural_drift",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_not_replaced": True,
            "classifier_correctness_not_assessed": True,
        },
        "review_coverage_summary": {
            "reviewed_entry_count": 12,
            "unreviewed_entry_count": 0,
            "human_operator_decision_required": True,
        },
        "warnings": _warnings(),
        "non_claims": {},
    }


def _candidate_packet(
    packet_id: str,
    setting_id: str,
    proposal_id: str,
    candidate_type: str,
    candidate_status: str,
    decision_support_status: str,
    blockers: list[str],
    risk_flags: list[str],
    *,
    threshold_candidate: float | None = None,
    smoothing_window_candidate: int | None = None,
) -> dict[str, Any]:
    return {
        "candidate_packet_id": packet_id,
        "candidate_setting_id": setting_id,
        "source_proposal_item_id": proposal_id,
        "candidate_type": candidate_type,
        "candidate_setting_summary": {
            "setting_type": candidate_type,
            "candidate_value": threshold_candidate or smoothing_window_candidate,
            "threshold_candidate": threshold_candidate,
            "smoothing_window_candidate": smoothing_window_candidate,
            "hysteresis_candidate": None,
            "future_manual_review_candidate": True,
            "not_applied": True,
            "writes_runtime_config": False,
            "affects_regression_baselines": False,
        },
        "candidate_status": candidate_status,
        "sandbox_evaluation_status": "evaluated_offline",
        "sandbox_regression_status": "regression_gate_passed",
        "baseline_comparison_status": "no_structural_drift",
        "review_coverage_status": "sufficient_for_operator_review",
        "decision_support_status": decision_support_status,
        "operator_review_status": "operator_review_needed",
        "not_applied": True,
        "runtime_change_status": "not_applied",
        "required_preconditions": ["human_operator_review"],
        "blockers": blockers,
        "risk_flags": risk_flags,
        "evidence_refs": {
            "candidate_evaluation_id": f"evaluation_{setting_id}",
            "source_metric_group": "boundary_segments",
            "source_review_entry_refs": [{"review_entry_id": f"review_{setting_id}"}],
            "source_segment_refs": [{"segment_id": f"segment_{setting_id}"}],
        },
        "provenance_status": "source_artifacts_available",
        "warnings": _warnings(),
    }


def _proposal() -> dict[str, Any]:
    return {
        "proposal_id": "proposal_fixture_v1",
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": _sha256(b"model fixture"),
        "warnings": _warnings(),
    }


def _evaluation_report() -> dict[str, Any]:
    return {
        "evaluation_report_id": "evaluation_report_fixture_v1",
        "evaluation_report_type": "review_guided_gameplay_calibration_evaluation_report",
        "evaluation_report_version": "v1",
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": _sha256(b"model fixture"),
        "current_settings": _current_settings(),
        "candidate_evaluations": [
            {
                "candidate_evaluation_id": "evaluation_setting_threshold",
                "candidate_setting_id": "setting_threshold",
                "candidate_type": "threshold_candidate",
                "evaluation_status": "evaluated_offline",
                "decision_support_status": "safe_for_future_manual_review",
                "warnings": _warnings(),
            }
        ],
        "warnings": _warnings(),
    }


def _regression_verification() -> dict[str, Any]:
    return {
        "baseline_id": "calibration_sandbox_baseline_fixture_v1",
        "status": "completed",
        "drift_detected": False,
        "breaking_drift_detected": False,
        "drift_items": [],
        "baseline_is_not_truth": True,
        "baseline_not_replaced": True,
        "classifier_correctness_not_assessed": True,
        "warnings": _warnings(),
    }


def _metrics_report() -> dict[str, Any]:
    return {
        "metrics_report_id": "metrics_report_fixture_v1",
        "summary": {
            "entry_count": 12,
            "reviewed_entry_count": 12,
            "unreviewed_entry_count": 0,
            "missing_required_review_field_count": 0,
        },
        "warnings": _warnings(),
    }


def _current_settings() -> dict[str, Any]:
    return {
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
    }


def _warnings() -> dict[str, bool]:
    return {
        "candidate_config_freeze_is_not_truth": True,
        "candidate_config_freeze_is_not_accuracy_scoring": True,
        "candidate_config_freeze_is_not_runtime_calibration": True,
        "manual_approval_packet_is_not_runtime_config": True,
        "threshold_changes_not_applied": True,
        "smoothing_changes_not_applied": True,
        "hysteresis_changes_not_applied": True,
        "classifier_not_modified": True,
        "model_weights_not_modified": True,
        "runtime_config_not_updated": True,
        "baseline_not_replaced": True,
        "automatic_relabeling_not_performed": True,
        "automatic_approval_not_performed": True,
        "automatic_rejection_not_performed": True,
        "generalization_not_claimed": True,
        "production_readiness_not_claimed": True,
        "human_operator_approval_required": True,
    }


def _sha256(value: bytes) -> str:
    import hashlib

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
