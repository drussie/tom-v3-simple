from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    NON_CLAIMS as EVALUATION_SANDBOX_NON_CLAIMS,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    SANDBOX_WARNINGS as EVALUATION_SANDBOX_WARNINGS,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    SOURCE_CONTRACT_REFS as EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_TYPE,
    build_review_guided_gameplay_calibration_sandbox_regression_baseline,
    build_review_guided_gameplay_calibration_sandbox_regression_report,
    export_review_guided_gameplay_calibration_sandbox_regression_contract,
    verify_review_guided_gameplay_calibration_sandbox_regression_baseline,
)


def test_export_calibration_sandbox_regression_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_review_guided_gameplay_calibration_sandbox_regression_contract(
        output_path=paths["regression_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
    )

    contract = json.loads(paths["regression_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["regression_scope"]["freezes_evaluation_input_structure"] is True
    assert contract["regression_scope"]["checks_candidate_settings_are_not_applied"] is True
    assert contract["regression_scope"]["applies_threshold_changes"] is False
    assert contract["regression_scope"]["applies_smoothing_changes"] is False
    assert contract["regression_scope"]["applies_hysteresis_changes"] is False
    assert contract["regression_scope"]["writes_runtime_config"] is False
    assert contract["regression_scope"]["updates_model_assets"] is False
    assert contract["regression_scope"]["replaces_existing_baselines"] is False
    assert (
        contract["source_contract_refs"][
            "review_guided_gameplay_calibration_evaluation_sandbox_contract_version"
        ]
        == "v1"
    )
    assert "not_applied_candidate_count" in contract["baseline_schema"]["required_fields"]
    assert contract["verification_schema"]["allowed_statuses"] == [
        "baseline_invalid",
        "baseline_missing",
        "breaking_drift_detected",
        "completed",
        "current_output_invalid",
        "drift_detected",
        "verification_failed",
    ]
    assert contract["warnings"]["sandbox_is_not_truth"] is True
    assert contract["warnings"]["sandbox_is_not_accuracy_scoring"] is True
    assert contract["warnings"]["runtime_config_not_updated"] is True
    assert not (
        FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_build_calibration_sandbox_regression_baseline_summarizes_sources(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        output_path=paths["baseline"],
        generated_at=datetime(2026, 6, 19, 15, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["baseline_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
    )

    baseline = json.loads(paths["baseline"].read_text(encoding="utf-8"))
    assert baseline["generated_at"] == "2026-06-19T15:00:00+00:00"
    assert baseline["candidate_setting_count"] == 6
    assert baseline["evaluated_candidate_count"] == 1
    assert baseline["blocked_candidate_count"] == 5
    assert baseline["ready_for_offline_evaluation_count"] == 1
    assert baseline["blocked_missing_review_data_count"] == 1
    assert baseline["blocked_insufficient_sample_size_count"] == 1
    assert baseline["blocked_fixture_only_data_count"] == 1
    assert baseline["blocked_no_human_review_count"] == 1
    assert baseline["invalid_candidate_count"] == 1
    assert baseline["not_applied_candidate_count"] == 6
    assert baseline["fixture_reuse_only"] is True
    assert baseline["not_distinct_real_broadcast_corpus"] is True
    assert baseline["does_not_claim_generalization"] is True
    assert baseline["warnings"]["sandbox_is_not_accuracy_scoring"] is True
    assert baseline["warnings"]["threshold_changes_not_applied"] is True
    assert baseline["non_claims"]["not_runtime_calibration"] is True
    assert not (
        FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS
        & _walk_exact_strings_and_keys(baseline)
    )


def test_verify_calibration_sandbox_regression_baseline_no_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)

    result = verify_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        baseline_path=paths["baseline"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        current_output_path=paths["current"],
        output_path=paths["verification"],
        verified_at=datetime(2026, 6, 19, 16, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["drift_detected"] is False
    assert result["breaking_drift_detected"] is False
    assert result["baseline_is_not_truth"] is True
    assert result["sandbox_is_not_truth"] is True
    assert result["sandbox_is_not_accuracy_scoring"] is True
    assert result["threshold_changes_not_applied"] is True
    assert result["smoothing_changes_not_applied"] is True
    assert result["hysteresis_changes_not_applied"] is True
    assert result["runtime_config_not_updated"] is True
    assert result["model_weights_not_modified"] is True
    assert result["baseline_not_replaced"] is True
    assert result["classifier_correctness_not_assessed"] is True
    assert result["generalization_not_claimed"] is True
    assert paths["current"].is_file()


def test_verify_calibration_sandbox_regression_detects_model_asset_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)
    report = json.loads(paths["evaluation_report"].read_text(encoding="utf-8"))
    report["model_asset_sha256"] = "changed-structural-sha"
    paths["evaluation_report"].write_text(json.dumps(report), encoding="utf-8")

    result = verify_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        baseline_path=paths["baseline"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        current_output_path=None,
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "breaking_drift_detected"
    assert result["drift_detected"] is True
    assert result["breaking_drift_detected"] is True
    assert any(
        item["field"] == "model_asset_sha256" and item["severity"] == "breaking"
        for item in result["drift_items"]
    )


def test_verify_calibration_sandbox_regression_rejects_forbidden_baseline_tokens(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)
    baseline = json.loads(paths["baseline"].read_text(encoding="utf-8"))
    baseline["baseline_replaced"] = True
    paths["baseline"].write_text(json.dumps(baseline), encoding="utf-8")

    result = verify_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        baseline_path=paths["baseline"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        current_output_path=None,
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "baseline_invalid"
    assert result["drift_detected"] is True
    assert any(
        item["error_type"] == "forbidden_field_or_value"
        for item in result["drift_items"]
    )


def test_build_calibration_sandbox_regression_report(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)
    verify_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        baseline_path=paths["baseline"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        current_output_path=paths["current"],
        output_path=paths["verification"],
    )

    result = build_review_guided_gameplay_calibration_sandbox_regression_report(
        contract_path=paths["regression_contract"],
        baseline_path=paths["baseline"],
        verification_path=paths["verification"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 19, 17, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["report_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_TYPE
    )
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["verification_status"] == "completed"
    assert report["summary"]["report_is_structural_only"] is True
    assert report["summary"]["model_weights_not_modified"] is True
    assert report["non_claims"]["not_generalization_claim"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "evaluation_contract": tmp_path / "evaluation_contract.json",
        "evaluation_inputs": tmp_path / "evaluation_inputs.json",
        "evaluation_report": tmp_path / "evaluation_report.json",
        "regression_contract": tmp_path / "regression_contract.json",
        "baseline": tmp_path / "baseline.json",
        "current": tmp_path / "current.json",
        "verification": tmp_path / "verification.json",
        "report": tmp_path / "report.json",
    }


def _build_baseline(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    build_review_guided_gameplay_calibration_sandbox_regression_baseline(
        contract_path=paths["regression_contract"],
        source_evaluation_input_path=paths["evaluation_inputs"],
        source_evaluation_report_path=paths["evaluation_report"],
        source_evaluation_contract_path=paths["evaluation_contract"],
        output_path=paths["baseline"],
    )


def _write_sources(paths: dict[str, Path]) -> None:
    export_review_guided_gameplay_calibration_sandbox_regression_contract(
        output_path=paths["regression_contract"]
    )
    paths["evaluation_contract"].write_text(
        json.dumps(
            {
                "contract_type": (
                    "review_guided_gameplay_calibration_evaluation_sandbox_contract"
                ),
                "contract_version": "v1",
                "sandbox_scope": {},
                "source_contract_refs": dict(EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS),
                "evaluation_input_schema": {},
                "candidate_setting_schema": {},
                "sandbox_evaluation_schema": {},
                "sandbox_report_schema": {},
                "validation_rules": {},
                "provenance_requirements": {},
                "warnings": dict(EVALUATION_SANDBOX_WARNINGS),
                "non_claims": dict(EVALUATION_SANDBOX_NON_CLAIMS),
            }
        ),
        encoding="utf-8",
    )
    inputs = _evaluation_inputs(paths)
    report = _evaluation_report(paths)
    paths["evaluation_inputs"].write_text(json.dumps(inputs), encoding="utf-8")
    paths["evaluation_report"].write_text(json.dumps(report), encoding="utf-8")


def _evaluation_inputs(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "evaluation_input_id": "evaluation_input_structural_fixture_v1",
        "evaluation_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
        "evaluation_input_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
        ),
        "generated_at": "2026-06-19T14:00:00+00:00",
        "source_calibration_proposal_path": "proposal.json",
        "source_metrics_report_path": "metrics.json",
        "source_review_loop_report_path": "review_loop.json",
        "source_review_bundle_path": "review_bundle.json",
        "source_corpus_run_path": "corpus_run.json",
        "source_regression_baseline_path": "gameplay_gate_regression.baseline.json",
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": "source-model-sha",
        "model_asset_exists": True,
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
        "candidate_settings": _candidate_settings(),
        "proposal_item_refs": [],
        "baseline_summary": {"baseline_available": True, "baseline_is_not_truth": True},
        "review_metrics_summary": {"reviewed_entry_count": 2, "unreviewed_entry_count": 0},
        "source_context": {"fixture_mode_used": True},
        "review_bundle_summary": {"entry_count": 2, "entries": []},
        "current_structural_summary": {"entry_count": 2},
        "source_contract_refs": dict(EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS),
        "warnings": {
            **dict(EVALUATION_SANDBOX_WARNINGS),
            "fixture_reuse_only": True,
        },
        "non_claims": dict(EVALUATION_SANDBOX_NON_CLAIMS),
        "tom_provenance": {"blueprint": "blueprint_50"},
    }


def _evaluation_report(paths: dict[str, Path]) -> dict[str, Any]:
    evaluations = _candidate_evaluations()
    blocked = [
        evaluation
        for evaluation in evaluations
        if str(evaluation["evaluation_status"]).startswith("blocked_")
    ]
    return {
        "evaluation_report_id": "evaluation_report_structural_fixture_v1",
        "evaluation_report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
        "evaluation_report_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
        ),
        "generated_at": "2026-06-19T14:30:00+00:00",
        "source_evaluation_input_path": str(paths["evaluation_inputs"]),
        "model_asset_ref": "model_assets/tom_v1/view_classifier_gameplay.pt",
        "model_asset_sha256": "source-model-sha",
        "model_asset_exists": True,
        "current_settings": {
            "threshold": 0.55,
            "smoothing_window": 3,
            "hysteresis_settings": {
                "enter_gameplay_probability": 0.6,
                "exit_gameplay_probability": 0.45,
            },
            "read_only_context": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
        },
        "candidate_evaluations": evaluations,
        "blocked_candidates": blocked,
        "baseline_comparison_summary": {
            "candidate_evaluation_count": 6,
            "evaluated_offline_count": 1,
            "completed_with_warnings_count": 0,
            "blocked_candidate_count": 5,
            "drift_detected_count": 0,
            "breaking_drift_detected_count": 0,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
            "runtime_config_not_updated": True,
            "baseline_not_replaced": True,
            "classifier_not_modified": True,
            "sandbox_is_not_truth": True,
            "sandbox_is_not_accuracy_scoring": True,
        },
        "review_coverage_summary": {"reviewed_entry_count": 2},
        "source_contract_refs": dict(EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS),
        "warnings": {
            **dict(EVALUATION_SANDBOX_WARNINGS),
            "fixture_reuse_only": True,
        },
        "non_claims": dict(EVALUATION_SANDBOX_NON_CLAIMS),
        "tom_provenance": {"blueprint": "blueprint_50"},
    }


def _candidate_settings() -> list[dict[str, Any]]:
    rows = [
        ("candidate-1", "proposal-1", "threshold_candidate", "ready_for_offline_evaluation"),
        ("candidate-2", "proposal-2", "no_candidate", "blocked_missing_review_data"),
        ("candidate-3", "proposal-3", "no_candidate", "blocked_insufficient_sample_size"),
        ("candidate-4", "proposal-4", "smoothing_window_candidate", "blocked_fixture_only_data"),
        ("candidate-5", "proposal-5", "no_candidate", "blocked_no_human_review"),
        ("candidate-6", "proposal-6", "not_applicable", "invalid_candidate"),
    ]
    return [
        {
            "candidate_setting_id": candidate_id,
            "source_proposal_item_id": proposal_id,
            "candidate_type": candidate_type,
            "threshold_candidate": 0.58
            if candidate_type == "threshold_candidate"
            else None,
            "smoothing_window_candidate": 5
            if candidate_type == "smoothing_window_candidate"
            else None,
            "hysteresis_candidate": None,
            "candidate_status": status,
            "not_applied": True,
            "evaluation_mode": (
                "structural_offline_evaluation"
                if status == "ready_for_offline_evaluation"
                else "fixture_only"
                if status == "blocked_fixture_only_data"
                else "baseline_comparison_only"
            ),
            "required_preconditions": ["manual_review_before_future_evaluation"],
            "source_metric_group": "structural_fixture",
            "source_review_entry_refs": [],
            "source_segment_refs": [],
            "human_review_required": True,
            "writes_runtime_config": False,
            "mutates_model_assets": False,
            "replaces_regression_baseline": False,
            "warnings": dict(EVALUATION_SANDBOX_WARNINGS),
        }
        for candidate_id, proposal_id, candidate_type, status in rows
    ]


def _candidate_evaluations() -> list[dict[str, Any]]:
    rows = [
        (
            "candidate-1",
            "threshold_candidate",
            "evaluated_offline",
            "safe_for_future_manual_review",
        ),
        (
            "candidate-2",
            "no_candidate",
            "blocked_missing_review_data",
            "needs_more_human_review",
        ),
        (
            "candidate-3",
            "no_candidate",
            "blocked_insufficient_sample_size",
            "needs_more_human_review",
        ),
        (
            "candidate-4",
            "smoothing_window_candidate",
            "blocked_fixture_only_data",
            "insufficient_data",
        ),
        (
            "candidate-5",
            "no_candidate",
            "blocked_no_human_review",
            "needs_more_human_review",
        ),
        (
            "candidate-6",
            "not_applicable",
            "blocked_invalid_candidate",
            "unsafe_for_runtime_application",
        ),
    ]
    return [
        {
            "candidate_evaluation_id": f"evaluation-{index}",
            "candidate_setting_id": candidate_id,
            "candidate_type": candidate_type,
            "evaluation_status": status,
            "evaluation_mode": "structural_offline_evaluation"
            if status == "evaluated_offline"
            else "fixture_only"
            if status == "blocked_fixture_only_data"
            else "baseline_comparison_only",
            "not_applied": True,
            "current_summary": {"entry_count": 2},
            "candidate_summary": {"entry_count": 2},
            "baseline_summary": {"baseline_available": True, "baseline_is_not_truth": True},
            "drift_detected": False,
            "breaking_drift_detected": False,
            "drift_items": [],
            "review_data_limitations": ["blocked_fixture_only_data"],
            "human_review_required": True,
            "decision_support_status": decision_status,
            "warnings": dict(EVALUATION_SANDBOX_WARNINGS),
        }
        for index, (candidate_id, candidate_type, status, decision_status) in enumerate(
            rows,
            start=1,
        )
    ]


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            seen.add(str(key))
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        seen.add(value)
    return seen
