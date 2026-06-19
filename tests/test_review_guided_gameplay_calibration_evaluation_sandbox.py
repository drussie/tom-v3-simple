from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_review_dataset_export import (
    export_gameplay_gate_review_dataset_contract,
)
from apps.worker.services.gameplay_gated_perception_execution import (
    export_gameplay_gated_perception_execution_contract,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    export_gameplay_gated_routing_contract,
)
from apps.worker.services.gameplay_segment_gate import (
    export_gameplay_segment_gate_contract,
)
from apps.worker.services.gameplay_segment_replay_review import (
    export_gameplay_segment_replay_review_contract,
)
from apps.worker.services.real_broadcast_gameplay_gate_corpus_run import (
    build_real_broadcast_gameplay_corpus_manifest_template,
    export_real_broadcast_gameplay_corpus_run_contract,
    run_real_broadcast_gameplay_corpus,
)
from apps.worker.services.real_broadcast_gameplay_review_loop import (
    build_real_broadcast_gameplay_review_bundle_template,
    build_real_broadcast_gameplay_review_loop_report,
    export_real_broadcast_gameplay_review_loop_contract,
)
from apps.worker.services.real_broadcast_gameplay_review_metrics import (
    build_real_broadcast_gameplay_review_metrics_report,
    export_real_broadcast_gameplay_review_metrics_contract,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    ALLOWED_CANDIDATE_STATUSES,
    ALLOWED_CANDIDATE_TYPES,
    ALLOWED_DECISION_SUPPORT_STATUSES,
    ALLOWED_DRIFT_SEVERITIES,
    ALLOWED_EVALUATION_MODES,
    ALLOWED_EVALUATION_STATUSES,
    FORBIDDEN_EVALUATION_SANDBOX_TOKENS,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE,
    build_review_guided_gameplay_calibration_evaluation_inputs,
    build_review_guided_gameplay_calibration_evaluation_summary,
    export_review_guided_gameplay_calibration_evaluation_sandbox_contract,
    run_review_guided_gameplay_calibration_evaluation_sandbox,
    validate_review_guided_gameplay_calibration_evaluation_inputs,
    validate_review_guided_gameplay_calibration_evaluation_report,
)
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    build_review_guided_gameplay_calibration_inputs,
    build_review_guided_gameplay_calibration_proposal,
    export_review_guided_gameplay_calibration_proposal_contract,
)


def test_export_calibration_evaluation_sandbox_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_review_guided_gameplay_calibration_evaluation_sandbox_contract(
        output_path=paths["evaluation_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
    )

    contract = json.loads(paths["evaluation_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["sandbox_scope"]["builds_evaluation_inputs"] is True
    assert contract["sandbox_scope"]["runs_offline_evaluation"] is True
    assert contract["sandbox_scope"]["applies_threshold_changes"] is False
    assert contract["sandbox_scope"]["applies_smoothing_changes"] is False
    assert contract["sandbox_scope"]["applies_hysteresis_changes"] is False
    assert contract["sandbox_scope"]["updates_runtime_config"] is False
    assert contract["sandbox_scope"]["updates_model"] is False
    assert contract["sandbox_scope"]["mutates_regression_baselines"] is False
    assert contract["candidate_setting_schema"]["allowed_candidate_types"] == (
        ALLOWED_CANDIDATE_TYPES
    )
    assert contract["candidate_setting_schema"]["allowed_candidate_statuses"] == (
        ALLOWED_CANDIDATE_STATUSES
    )
    assert contract["sandbox_evaluation_schema"]["allowed_evaluation_modes"] == (
        ALLOWED_EVALUATION_MODES
    )
    assert contract["sandbox_evaluation_schema"]["allowed_evaluation_statuses"] == (
        ALLOWED_EVALUATION_STATUSES
    )
    assert contract["sandbox_evaluation_schema"][
        "allowed_decision_support_statuses"
    ] == ALLOWED_DECISION_SUPPORT_STATUSES
    assert contract["sandbox_evaluation_schema"]["allowed_drift_severities"] == (
        ALLOWED_DRIFT_SEVERITIES
    )
    assert contract["warnings"]["sandbox_is_not_truth"] is True
    assert contract["warnings"]["threshold_changes_not_applied"] is True
    assert contract["warnings"]["runtime_config_not_updated"] is True
    assert contract["warnings"]["baseline_not_replaced"] is True
    assert not (FORBIDDEN_EVALUATION_SANDBOX_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_calibration_evaluation_inputs_preserves_candidate_provenance(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_inputs(paths, include_fixture_context=False)

    result = validate_review_guided_gameplay_calibration_evaluation_inputs(
        contract_path=paths["evaluation_contract"],
        evaluation_inputs_path=paths["evaluation_inputs"],
        output_path=None,
    )

    assert result["ok"] is True
    assert result["status"] == "valid"

    inputs = json.loads(paths["evaluation_inputs"].read_text(encoding="utf-8"))
    assert (
        inputs["evaluation_input_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE
    )
    assert (
        inputs["evaluation_input_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
    )
    assert inputs["current_threshold"] == 0.55
    assert inputs["current_smoothing_window"] == 3
    assert inputs["current_hysteresis_settings"] == {
        "enter_gameplay_probability": 0.6,
        "exit_gameplay_probability": 0.45,
    }
    assert inputs["model_asset_ref"] == str(paths["asset"])
    assert inputs["model_asset_sha256"]
    assert inputs["source_calibration_proposal_path"] == str(paths["calibration_proposal"])
    assert inputs["source_corpus_run_path"] is None
    assert inputs["source_context"]["fixture_mode_used"] is False
    assert inputs["review_metrics_summary"]["reviewed_entry_count"] == 2
    assert inputs["review_metrics_summary"]["unreviewed_entry_count"] == 0
    assert inputs["review_metrics_summary"]["total_missing_review_field_count"] == 0
    assert inputs["warnings"]["sandbox_is_not_truth"] is True
    assert inputs["warnings"]["threshold_changes_not_applied"] is True
    assert inputs["non_claims"]["not_runtime_calibration"] is True

    by_type = {item["candidate_type"]: item for item in inputs["candidate_settings"]}
    assert by_type["threshold_candidate"]["candidate_status"] == (
        "ready_for_offline_evaluation"
    )
    assert by_type["threshold_candidate"]["not_applied"] is True
    assert by_type["threshold_candidate"]["writes_runtime_config"] is False
    assert by_type["threshold_candidate"]["mutates_model_assets"] is False
    assert by_type["threshold_candidate"]["replaces_regression_baseline"] is False
    assert by_type["smoothing_window_candidate"]["candidate_status"] == (
        "blocked_insufficient_sample_size"
    )
    assert by_type["hysteresis_candidate"]["candidate_status"] == (
        "ready_for_offline_evaluation"
    )


def test_evaluation_inputs_preserve_fixture_only_blocking_when_supplied(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_inputs(paths, include_fixture_context=True)

    inputs = json.loads(paths["evaluation_inputs"].read_text(encoding="utf-8"))
    assert inputs["source_corpus_run_path"] == str(paths["corpus_run"])
    assert inputs["source_context"]["fixture_mode_used"] is True
    assert "blocked_fixture_only_data" in {
        item["candidate_status"] for item in inputs["candidate_settings"]
    }


def test_validate_calibration_evaluation_inputs_rejects_runtime_application(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_inputs(paths, include_fixture_context=False)
    inputs = json.loads(paths["evaluation_inputs"].read_text(encoding="utf-8"))
    candidate = inputs["candidate_settings"][0]
    candidate["not_applied"] = False
    candidate["writes_runtime_config"] = True
    candidate["mutates_model_assets"] = True
    candidate["replaces_regression_baseline"] = True
    candidate["risk_flags"] = ["runtime_config_updated"]
    paths["evaluation_inputs"].write_text(json.dumps(inputs), encoding="utf-8")

    result = validate_review_guided_gameplay_calibration_evaluation_inputs(
        contract_path=paths["evaluation_contract"],
        evaluation_inputs_path=paths["evaluation_inputs"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "candidate_setting_must_be_not_applied",
        "candidate_setting_must_not_write_runtime_config",
        "candidate_setting_must_not_mutate_model_assets",
        "candidate_setting_must_not_replace_baseline",
        "forbidden_field_or_value",
    }


def test_run_calibration_evaluation_sandbox_is_offline_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_inputs(paths, include_fixture_context=False)

    result = run_review_guided_gameplay_calibration_evaluation_sandbox(
        contract_path=paths["evaluation_contract"],
        evaluation_inputs_path=paths["evaluation_inputs"],
        evaluation_mode="structural_offline_evaluation",
        output_path=paths["evaluation_report"],
        generated_at=datetime(2026, 6, 19, 21, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["evaluation_report_type"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE
    )
    assert (
        result["evaluation_report_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
    )

    report = json.loads(paths["evaluation_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T21:00:00+00:00"
    assert report["current_settings"]["read_only_context"] is True
    assert report["baseline_comparison_summary"]["runtime_config_not_updated"] is True
    assert report["baseline_comparison_summary"]["baseline_not_replaced"] is True
    assert report["baseline_comparison_summary"]["classifier_not_modified"] is True
    assert report["warnings"]["sandbox_is_not_accuracy_scoring"] is True
    assert report["non_claims"]["not_model_tuning"] is True
    assert all(
        evaluation["not_applied"] is True
        for evaluation in report["candidate_evaluations"]
    )
    assert "evaluated_offline" in {
        evaluation["evaluation_status"] for evaluation in report["candidate_evaluations"]
    }
    assert "completed_with_warnings" in {
        evaluation["evaluation_status"] for evaluation in report["candidate_evaluations"]
    }

    validation = validate_review_guided_gameplay_calibration_evaluation_report(
        contract_path=paths["evaluation_contract"],
        evaluation_report_path=paths["evaluation_report"],
        output_path=None,
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"


def test_validate_calibration_evaluation_report_rejects_application_claims(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_report(paths)
    report = json.loads(paths["evaluation_report"].read_text(encoding="utf-8"))
    evaluation = report["candidate_evaluations"][0]
    evaluation["evaluation_status"] = "applied_to_runtime"
    evaluation["not_applied"] = False
    evaluation["drift_items"] = [{"field": "entry_count", "severity": "critical"}]
    report["baseline_replaced"] = True
    paths["evaluation_report"].write_text(json.dumps(report), encoding="utf-8")

    result = validate_review_guided_gameplay_calibration_evaluation_report(
        contract_path=paths["evaluation_contract"],
        evaluation_report_path=paths["evaluation_report"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "unsupported_evaluation_status",
        "candidate_evaluation_must_be_not_applied",
        "unsupported_drift_severity",
        "forbidden_field_or_value",
    }


def test_build_calibration_evaluation_summary_reports_validation_snapshot(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_evaluation_report(paths)

    result = build_review_guided_gameplay_calibration_evaluation_summary(
        contract_path=paths["evaluation_contract"],
        evaluation_report_path=paths["evaluation_report"],
        output_path=paths["evaluation_summary"],
        generated_at=datetime(2026, 6, 19, 21, 30, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["summary_type"] == (
        REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE
    )

    summary = json.loads(paths["evaluation_summary"].read_text(encoding="utf-8"))
    assert summary["generated_at"] == "2026-06-19T21:30:00+00:00"
    assert summary["validation_snapshot"]["ok"] is True
    assert summary["candidate_evaluation_count"] >= 1
    assert summary["evaluation_status_counts"]["evaluated_offline"] >= 1
    assert summary["baseline_comparison_summary"]["runtime_config_not_updated"] is True
    assert summary["warnings"]["production_readiness_not_claimed"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "broadcast_clip.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    media_2 = tmp_path / "broadcast_clip_2.mp4"
    media_2.write_bytes(b"not a real video either; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "media_2": media_2,
        "asset": asset,
        "corpus_contract": tmp_path / "real_broadcast_gameplay_corpus_contract.json",
        "corpus_manifest": tmp_path / "real_broadcast_manifest.json",
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "routing_contract": tmp_path / "routing_contract.json",
        "execution_contract": tmp_path / "execution_contract.json",
        "replay_review_contract": tmp_path / "replay_review_contract.json",
        "review_dataset_contract": tmp_path / "review_dataset_contract.json",
        "corpus_output_dir": tmp_path / "corpus_outputs",
        "corpus_run": tmp_path / "corpus_run.current.json",
        "review_loop_contract": tmp_path / "review_loop_contract.json",
        "review_bundle": tmp_path / "review_bundle.template.json",
        "review_loop_report": tmp_path / "review_loop_report.json",
        "metrics_contract": tmp_path / "review_metrics_contract.json",
        "metrics_report": tmp_path / "review_metrics_report.json",
        "calibration_contract": tmp_path / "calibration_contract.json",
        "calibration_inputs": tmp_path / "calibration_inputs.json",
        "calibration_proposal": tmp_path / "calibration_proposal.json",
        "evaluation_contract": tmp_path / "evaluation_contract.json",
        "evaluation_inputs": tmp_path / "evaluation_inputs.json",
        "evaluation_report": tmp_path / "evaluation_report.json",
        "evaluation_summary": tmp_path / "evaluation_summary.json",
    }


def _build_evaluation_report(paths: dict[str, Path]) -> None:
    _build_evaluation_inputs(paths, include_fixture_context=False)
    run_review_guided_gameplay_calibration_evaluation_sandbox(
        contract_path=paths["evaluation_contract"],
        evaluation_inputs_path=paths["evaluation_inputs"],
        evaluation_mode="structural_offline_evaluation",
        output_path=paths["evaluation_report"],
    )


def _build_evaluation_inputs(
    paths: dict[str, Path],
    *,
    include_fixture_context: bool,
) -> None:
    _build_calibration_proposal(paths)
    export_review_guided_gameplay_calibration_evaluation_sandbox_contract(
        output_path=paths["evaluation_contract"]
    )
    build_review_guided_gameplay_calibration_evaluation_inputs(
        contract_path=paths["evaluation_contract"],
        source_calibration_proposal_path=paths["calibration_proposal"],
        source_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_corpus_run_path=paths["corpus_run"] if include_fixture_context else None,
        source_regression_baseline_path=None,
        model_asset_path=paths["asset"],
        current_threshold=0.55,
        current_smoothing_window=3,
        hysteresis_enter=0.6,
        hysteresis_exit=0.45,
        output_path=paths["evaluation_inputs"],
        generated_at=datetime(2026, 6, 19, 20, 45, tzinfo=UTC),
    )


def _build_calibration_proposal(paths: dict[str, Path]) -> None:
    _build_calibration_inputs(paths)
    build_review_guided_gameplay_calibration_proposal(
        contract_path=paths["calibration_contract"],
        calibration_inputs_path=paths["calibration_inputs"],
        output_path=paths["calibration_proposal"],
    )


def _build_calibration_inputs(paths: dict[str, Path]) -> None:
    _build_review_metrics_report(paths)
    export_review_guided_gameplay_calibration_proposal_contract(
        output_path=paths["calibration_contract"]
    )
    build_review_guided_gameplay_calibration_inputs(
        contract_path=paths["calibration_contract"],
        source_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_review_dataset_path=None,
        source_corpus_run_path=None,
        source_regression_baseline_path=None,
        model_asset_path=paths["asset"],
        current_threshold=0.55,
        current_smoothing_window=3,
        hysteresis_enter=0.6,
        hysteresis_exit=0.45,
        output_path=paths["calibration_inputs"],
    )


def _build_review_metrics_report(paths: dict[str, Path]) -> None:
    _build_review_loop_report(paths)
    export_real_broadcast_gameplay_review_metrics_contract(
        output_path=paths["metrics_contract"]
    )
    build_real_broadcast_gameplay_review_metrics_report(
        contract_path=paths["metrics_contract"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_corpus_run_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        output_path=paths["metrics_report"],
    )


def _build_review_loop_report(paths: dict[str, Path]) -> None:
    _build_review_bundle(paths)
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    bundle["entries"][0]["human_review"] = {
        **bundle["entries"][0]["human_review"],
        "reviewer_id": "reviewer-1",
        "reviewed_at": "2026-06-19T19:00:00+00:00",
        "reviewed_segment_status": "reviewed_as_uncertain",
        "reviewed_downstream_gate_status": "reviewer_would_request_additional_review",
        "review_confidence": "low",
        "ambiguity_flags": [
            "classifier_boundary_unclear",
            "broadcast_replay_possible",
        ],
        "reviewer_notes": "boundary metadata only",
        "review_source": "manual_json_review",
    }
    bundle["entries"][1]["human_review"] = {
        **bundle["entries"][1]["human_review"],
        "reviewer_id": "reviewer-2",
        "reviewed_at": "2026-06-19T19:05:00+00:00",
        "reviewed_segment_status": "reviewed_as_non_gameplay_candidate",
        "reviewed_downstream_gate_status": "reviewer_would_block_downstream_observation",
        "review_confidence": "medium",
        "ambiguity_flags": ["commercial_or_graphic_possible"],
        "reviewer_notes": "review operations metadata only",
        "review_source": "manual_json_review",
    }
    paths["review_bundle"].write_text(json.dumps(bundle), encoding="utf-8")
    build_real_broadcast_gameplay_review_loop_report(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_loop_report"],
    )


def _build_review_bundle(paths: dict[str, Path]) -> None:
    _build_fixture_corpus_run(paths)
    export_real_broadcast_gameplay_review_loop_contract(
        output_path=paths["review_loop_contract"]
    )
    build_real_broadcast_gameplay_review_bundle_template(
        contract_path=paths["review_loop_contract"],
        source_corpus_run_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        output_path=paths["review_bundle"],
    )


def _build_fixture_corpus_run(paths: dict[str, Path]) -> None:
    _export_corpus_contracts(paths)
    build_real_broadcast_gameplay_corpus_manifest_template(
        local_media_paths=[paths["media"], paths["media_2"]],
        source_label="broadcast_fixture",
        expected_broadcast_content_tags=["live_gameplay"],
        output_path=paths["corpus_manifest"],
        allow_fixture_mode=True,
    )
    run_real_broadcast_gameplay_corpus(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["corpus_manifest"],
        run_mode="fixture_only",
        output_dir=paths["corpus_output_dir"],
        output_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        gameplay_segment_contract_path=paths["gameplay_contract"],
        routing_contract_path=paths["routing_contract"],
        execution_contract_path=paths["execution_contract"],
        replay_review_contract_path=paths["replay_review_contract"],
        review_dataset_contract_path=paths["review_dataset_contract"],
        probe_runner=_fake_probe_runner(),
    )


def _export_corpus_contracts(paths: dict[str, Path]) -> None:
    export_real_broadcast_gameplay_corpus_run_contract(
        output_path=paths["corpus_contract"]
    )
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_gated_perception_execution_contract(
        output_path=paths["execution_contract"]
    )
    export_gameplay_segment_replay_review_contract(
        output_path=paths["replay_review_contract"]
    )
    export_gameplay_gate_review_dataset_contract(
        output_path=paths["review_dataset_contract"]
    )


def _fake_probe_runner() -> Any:
    raw_probe = {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "h264",
                "avg_frame_rate": "30/1",
                "duration": "4.0",
                "nb_frames": "120",
                "width": 1280,
                "height": 720,
            }
        ],
        "format": {"duration": "4.0", "format_name": "mov,mp4,m4a,3gp,3g2,mj2"},
    }

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=json.dumps(raw_probe),
            stderr="",
        )

    return runner


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
