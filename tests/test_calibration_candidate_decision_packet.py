from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.calibration_candidate_decision_packet import (
    CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE,
    CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION,
    CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
    FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS,
    build_calibration_candidate_decision_packet,
    build_calibration_candidate_decision_packet_inputs,
    build_calibration_candidate_decision_packet_report,
    export_calibration_candidate_decision_packet_contract,
    validate_calibration_candidate_decision_packet,
    validate_calibration_candidate_decision_packet_inputs,
)
from apps.worker.services.calibration_candidate_decision_packet import (
    SOURCE_CONTRACT_REFS as DECISION_PACKET_SOURCE_CONTRACT_REFS,
)


def test_export_calibration_candidate_decision_packet_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_calibration_candidate_decision_packet_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE
    assert (
        result["contract_version"]
        == CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["packet_scope"]["packages_prior_calibration_evidence"] is True
    assert contract["packet_scope"]["updates_runtime_config"] is False
    assert contract["packet_scope"]["updates_model_weights"] is False
    assert contract["packet_scope"]["mutates_regression_baselines"] is False
    assert contract["packet_scope"]["applies_threshold_changes"] is False
    assert contract["packet_scope"]["applies_smoothing_changes"] is False
    assert contract["packet_scope"]["applies_hysteresis_changes"] is False
    assert (
        contract["source_contract_refs"][
            "review_guided_gameplay_calibration_sandbox_regression_contract_version"
        ]
        == "v1"
    )
    assert (
        "candidate_packet_id"
        in contract["candidate_packet_schema"]["required_fields"]
    )
    assert contract["candidate_packet_schema"]["requires_not_applied"] is True
    assert contract["warnings"]["decision_packet_is_not_truth"] is True
    assert contract["warnings"]["runtime_config_not_updated"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_build_and_validate_calibration_candidate_decision_packet_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_calibration_candidate_decision_packet_inputs(
        contract_path=paths["contract"],
        source_calibration_proposal_path=paths["proposal"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_review_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_corpus_run_path=paths["corpus_run"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["packet_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    packet_inputs = json.loads(paths["packet_inputs"].read_text(encoding="utf-8"))
    assert packet_inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert packet_inputs["proposal_summary"]["proposal_item_count"] == 3
    assert packet_inputs["blocked_candidate_summary"]["proposal_blocked_item_count"] == 2
    assert packet_inputs["sandbox_regression_summary"]["status"] == "completed"
    assert packet_inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert len(packet_inputs["candidate_inputs"]) == 3
    assert packet_inputs["source_contract_refs"] == DECISION_PACKET_SOURCE_CONTRACT_REFS
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS
        & _walk_exact_strings_and_keys(packet_inputs)
    )

    validation = validate_calibration_candidate_decision_packet_inputs(
        contract_path=paths["contract"],
        packet_inputs_path=paths["packet_inputs"],
        output_path=paths["packet_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_calibration_candidate_decision_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_packet_inputs(paths)

    result = build_calibration_candidate_decision_packet(
        contract_path=paths["contract"],
        packet_inputs_path=paths["packet_inputs"],
        output_path=paths["decision_packet"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["decision_packet_type"] == CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE

    packet = json.loads(paths["decision_packet"].read_text(encoding="utf-8"))
    assert packet["summary"]["candidate_packet_count"] == 3
    assert packet["summary"]["blocked_candidate_count"] == 2
    assert packet["summary"]["ready_for_operator_review_count"] == 1
    assert packet["summary"]["not_applied_candidate_count"] == 3
    assert packet["summary"]["runtime_change_status"] == "not_applied"
    assert packet["regression_gate_summary"]["sandbox_regression_status"] == (
        "regression_gate_passed"
    )
    assert {candidate["candidate_status"] for candidate in packet["candidate_packets"]} == {
        "blocked_fixture_only_data",
        "blocked_missing_review_data",
        "ready_for_operator_review",
    }
    assert all(candidate["not_applied"] is True for candidate in packet["candidate_packets"])
    assert all(
        candidate["runtime_change_status"] == "not_applied"
        for candidate in packet["candidate_packets"]
    )
    assert {
        action["action_type"] for action in packet["operator_next_actions"]
    } >= {
        "do_not_apply_runtime_change",
        "inspect_missing_review_fields",
        "prepare_offline_followup_experiment",
        "review_candidate_packet",
    }
    assert packet["warnings"]["decision_packet_is_not_truth"] is True
    assert packet["non_claims"]["human_operator_decision_required"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS
        & _walk_exact_strings_and_keys(packet)
    )

    validation = validate_calibration_candidate_decision_packet(
        contract_path=paths["contract"],
        decision_packet_path=paths["decision_packet"],
        output_path=paths["decision_packet_validation"],
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0


def test_decision_packet_validation_rejects_forbidden_runtime_selection(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_packet(paths)
    packet = json.loads(paths["decision_packet"].read_text(encoding="utf-8"))
    packet["candidate_packets"][0]["runtime_change_status"] = "future_manual_change_required"
    packet["candidate_packets"][0]["auto_approved"] = True
    paths["decision_packet"].write_text(json.dumps(packet), encoding="utf-8")

    result = validate_calibration_candidate_decision_packet(
        contract_path=paths["contract"],
        decision_packet_path=paths["decision_packet"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field_or_value" in error_types
    assert "invalid_runtime_change_status" in error_types


def test_build_calibration_candidate_decision_packet_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_packet(paths)

    result = build_calibration_candidate_decision_packet_report(
        contract_path=paths["contract"],
        decision_packet_path=paths["decision_packet"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T03:00:00+00:00"
    assert report["operator_review_needed"] is True
    assert report["decision_packet_summary"]["candidate_packet_count"] == 3
    assert report["decision_packet_summary"]["runtime_change_status"] == "not_applied"
    assert report["structural_drift_summary"]["sandbox_regression_status"] == (
        "regression_gate_passed"
    )
    assert report["warnings"]["decision_packet_is_not_truth"] is True
    assert not (
        FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS
        & _walk_exact_strings_and_keys(report)
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "proposal": tmp_path / "proposal.json",
        "evaluation_inputs": tmp_path / "evaluation_inputs.json",
        "evaluation_report": tmp_path / "evaluation_report.json",
        "regression_verification": tmp_path / "regression_verification.json",
        "metrics_report": tmp_path / "metrics_report.json",
        "review_loop_report": tmp_path / "review_loop_report.json",
        "corpus_run": tmp_path / "corpus_run.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "packet_inputs": tmp_path / "packet_inputs.json",
        "packet_inputs_validation": tmp_path / "packet_inputs.validation.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "decision_packet_validation": tmp_path / "decision_packet.validation.json",
        "report": tmp_path / "report.json",
    }


def _build_packet_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_calibration_candidate_decision_packet_inputs(
        contract_path=paths["contract"],
        source_calibration_proposal_path=paths["proposal"],
        source_sandbox_evaluation_report_path=paths["evaluation_report"],
        source_sandbox_regression_verification_path=paths["regression_verification"],
        source_review_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_corpus_run_path=paths["corpus_run"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["packet_inputs"],
    )


def _build_packet(paths: dict[str, Path]) -> None:
    _build_packet_inputs(paths)
    build_calibration_candidate_decision_packet(
        contract_path=paths["contract"],
        packet_inputs_path=paths["packet_inputs"],
        output_path=paths["decision_packet"],
    )


def _write_sources(paths: dict[str, Path]) -> None:
    export_calibration_candidate_decision_packet_contract(output_path=paths["contract"])
    paths["model_asset"].write_bytes(b"model fixture")
    paths["proposal"].write_text(json.dumps(_proposal()), encoding="utf-8")
    paths["evaluation_inputs"].write_text(
        json.dumps(_evaluation_inputs(paths)),
        encoding="utf-8",
    )
    paths["evaluation_report"].write_text(
        json.dumps(_evaluation_report(paths)),
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


def _proposal() -> dict[str, Any]:
    items = [
        _proposal_item(
            "proposal_ready_threshold",
            "threshold_review_candidate",
            "needs_additional_review",
            "boundary_segments",
            "threshold_candidate",
            0.58,
            ["review_boundary_segments"],
            ["boundary_case_possible"],
        ),
        _proposal_item(
            "proposal_missing_review",
            "missing_review_data_blocker",
            "blocked_missing_review_data",
            "missing_review_fields",
            "not_applicable",
            None,
            ["complete_required_human_review_fields"],
            ["human_review_required", "missing_review_fields"],
        ),
        _proposal_item(
            "proposal_fixture_smoothing",
            "smoothing_window_review_candidate",
            "blocked_fixture_only_data",
            "source_context",
            "smoothing_window_candidate",
            5,
            ["collect_distinct_real_broadcast_review_data"],
            ["fixture_only_source"],
        ),
    ]
    return {
        "proposal_id": "proposal_fixture_v1",
        "proposal_items": items,
        "blocked_items": items[1:],
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": _sha256(b"model fixture"),
        "source_contract_refs": dict(DECISION_PACKET_SOURCE_CONTRACT_REFS),
        "warnings": {
            "classifier_not_modified": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
        },
        "non_claims": {},
    }


def _proposal_item(
    item_id: str,
    proposal_type: str,
    status: str,
    source_metric_group: str,
    setting_type: str,
    candidate_value: int | float | None,
    required_preconditions: list[str],
    risk_flags: list[str],
) -> dict[str, Any]:
    return {
        "proposal_item_id": item_id,
        "proposal_type": proposal_type,
        "proposal_status": status,
        "source_metric_group": source_metric_group,
        "proposed_candidate_setting": {
            "setting_type": setting_type,
            "candidate_value": candidate_value,
            "future_evaluation_only": True,
            "not_applied": True,
            "writes_runtime_config": False,
            "affects_regression_baselines": False,
        },
        "required_preconditions": required_preconditions,
        "risk_flags": risk_flags,
        "source_review_entry_refs": [],
        "source_segment_refs": [],
        "warnings": {
            "classifier_not_modified": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
        },
    }


def _evaluation_inputs(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "evaluation_input_id": "evaluation_input_fixture_v1",
        "source_calibration_proposal_path": str(paths["proposal"]),
        "candidate_settings": [
            _candidate_setting(
                "setting_threshold",
                "proposal_ready_threshold",
                "threshold_candidate",
                "ready_for_offline_evaluation",
                "boundary_segments",
                threshold_candidate=0.58,
            ),
            _candidate_setting(
                "setting_missing",
                "proposal_missing_review",
                "no_candidate",
                "blocked_missing_review_data",
                "missing_review_fields",
            ),
            _candidate_setting(
                "setting_fixture",
                "proposal_fixture_smoothing",
                "smoothing_window_candidate",
                "blocked_fixture_only_data",
                "source_context",
                smoothing_window_candidate=5,
            ),
        ],
    }


def _candidate_setting(
    setting_id: str,
    proposal_item_id: str,
    candidate_type: str,
    status: str,
    source_metric_group: str,
    *,
    threshold_candidate: float | None = None,
    smoothing_window_candidate: int | None = None,
) -> dict[str, Any]:
    return {
        "candidate_setting_id": setting_id,
        "source_proposal_item_id": proposal_item_id,
        "candidate_type": candidate_type,
        "candidate_status": status,
        "source_metric_group": source_metric_group,
        "threshold_candidate": threshold_candidate,
        "smoothing_window_candidate": smoothing_window_candidate,
        "hysteresis_candidate": None,
        "not_applied": True,
        "writes_runtime_config": False,
        "required_preconditions": ["human_operator_review"],
        "risk_flags": [],
        "source_review_entry_refs": [{"review_entry_id": f"review_{setting_id}"}],
        "source_segment_refs": [{"segment_id": f"segment_{setting_id}"}],
        "warnings": {"classifier_not_modified": True},
    }


def _evaluation_report(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "evaluation_report_id": "evaluation_report_fixture_v1",
        "evaluation_report_type": "review_guided_gameplay_calibration_evaluation_report",
        "evaluation_report_version": "v1",
        "source_evaluation_input_path": str(paths["evaluation_inputs"]),
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": _sha256(b"model fixture"),
        "current_settings": {
            "current_threshold": 0.55,
            "current_smoothing_window": 3,
            "current_hysteresis_settings": {
                "enter_gameplay_probability": 0.6,
                "exit_gameplay_probability": 0.45,
            },
        },
        "candidate_evaluations": [
            {
                "candidate_evaluation_id": "evaluation_threshold",
                "candidate_setting_id": "setting_threshold",
                "candidate_type": "threshold_candidate",
                "evaluation_status": "evaluated_offline",
                "decision_support_status": "safe_for_future_manual_review",
                "warnings": {"classifier_not_modified": True},
            },
            {
                "candidate_evaluation_id": "evaluation_missing",
                "candidate_setting_id": "setting_missing",
                "candidate_type": "no_candidate",
                "evaluation_status": "blocked_missing_review_data",
                "decision_support_status": "needs_more_human_review",
                "warnings": {"classifier_not_modified": True},
            },
            {
                "candidate_evaluation_id": "evaluation_fixture",
                "candidate_setting_id": "setting_fixture",
                "candidate_type": "smoothing_window_candidate",
                "evaluation_status": "blocked_fixture_only_data",
                "decision_support_status": "blocked_from_runtime_consideration",
                "warnings": {"classifier_not_modified": True},
            },
        ],
        "blocked_candidates": [
            {
                "candidate_setting_id": "setting_missing",
                "evaluation_status": "blocked_missing_review_data",
            },
            {
                "candidate_setting_id": "setting_fixture",
                "evaluation_status": "blocked_fixture_only_data",
            },
        ],
        "baseline_comparison_summary": {
            "drift_detected_count": 0,
            "breaking_drift_detected_count": 0,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
            "runtime_config_not_updated": True,
            "baseline_not_replaced": True,
            "classifier_not_modified": True,
        },
        "review_coverage_summary": {
            "reviewed_entry_count": 12,
            "unreviewed_entry_count": 0,
            "total_missing_review_field_count": 0,
        },
        "source_contract_refs": dict(DECISION_PACKET_SOURCE_CONTRACT_REFS),
        "warnings": {
            "sandbox_is_not_truth": True,
            "sandbox_is_not_accuracy_scoring": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
            "runtime_config_not_updated": True,
            "baseline_not_replaced": True,
            "classifier_not_modified": True,
        },
        "non_claims": {},
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
        "source_contract_refs": dict(DECISION_PACKET_SOURCE_CONTRACT_REFS),
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
        "source_context": {"fixture_mode_used": False},
        "warnings": {
            "metrics_are_not_truth": True,
            "classifier_not_modified": True,
        },
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
