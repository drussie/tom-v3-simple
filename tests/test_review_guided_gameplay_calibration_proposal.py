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
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    ALLOWED_EVALUATION_ACTIONS,
    ALLOWED_PROPOSAL_STATUSES,
    ALLOWED_PROPOSAL_TYPES,
    ALLOWED_RISK_FLAGS,
    FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
    build_review_guided_gameplay_calibration_inputs,
    build_review_guided_gameplay_calibration_proposal,
    build_review_guided_gameplay_calibration_proposal_report,
    export_review_guided_gameplay_calibration_proposal_contract,
    validate_review_guided_gameplay_calibration_inputs,
    validate_review_guided_gameplay_calibration_proposal,
)


def test_export_calibration_proposal_contract_is_stable(tmp_path: Path) -> None:
    paths = _paths(tmp_path)

    result = export_review_guided_gameplay_calibration_proposal_contract(
        output_path=paths["calibration_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE
    assert (
        result["contract_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION
    )

    contract = json.loads(paths["calibration_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["proposal_scope"]["builds_calibration_inputs"] is True
    assert contract["proposal_scope"]["builds_future_evaluation_proposals"] is True
    assert contract["proposal_scope"]["applies_threshold_changes"] is False
    assert contract["proposal_scope"]["applies_smoothing_changes"] is False
    assert contract["proposal_scope"]["applies_hysteresis_changes"] is False
    assert contract["proposal_scope"]["updates_model"] is False
    assert contract["proposal_scope"]["calculates_classifier_accuracy"] is False
    assert contract["proposal_item_schema"]["allowed_proposal_types"] == ALLOWED_PROPOSAL_TYPES
    assert contract["proposal_item_schema"]["allowed_proposal_statuses"] == (
        ALLOWED_PROPOSAL_STATUSES
    )
    assert contract["proposal_item_schema"]["allowed_proposed_evaluation_actions"] == (
        ALLOWED_EVALUATION_ACTIONS
    )
    assert contract["proposal_item_schema"]["allowed_risk_flags"] == ALLOWED_RISK_FLAGS
    assert contract["warnings"]["threshold_changes_not_applied"] is True
    assert contract["warnings"]["model_weights_not_modified"] is True
    assert not (FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_calibration_inputs_preserves_review_provenance_and_gate_settings(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_metrics_report(paths)

    result = build_review_guided_gameplay_calibration_inputs(
        contract_path=paths["calibration_contract"],
        source_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_review_dataset_path=None,
        source_corpus_run_path=paths["corpus_run"],
        source_regression_baseline_path=None,
        model_asset_path=paths["asset"],
        current_threshold=0.55,
        current_smoothing_window=3,
        hysteresis_enter=0.6,
        hysteresis_exit=0.45,
        output_path=paths["calibration_inputs"],
        generated_at=datetime(2026, 6, 19, 20, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["calibration_input_type"] == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE
    assert (
        result["calibration_input_version"]
        == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION
    )

    inputs = json.loads(paths["calibration_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-19T20:00:00+00:00"
    assert inputs["current_threshold"] == 0.55
    assert inputs["current_smoothing_window"] == 3
    assert inputs["current_hysteresis_settings"] == {
        "enter_gameplay_probability": 0.6,
        "exit_gameplay_probability": 0.45,
    }
    assert inputs["model_asset_ref"] == str(paths["asset"])
    assert inputs["model_asset_sha256"]
    assert inputs["review_metrics_summary"]["reviewed_entry_count"] == 2
    assert inputs["review_metrics_summary"]["unreviewed_entry_count"] >= 1
    assert inputs["ambiguity_summary"]["classifier_boundary_unclear_count"] == 1
    assert inputs["ambiguity_summary"]["broadcast_replay_possible_count"] == 1
    assert inputs["boundary_case_summary"]["classifier_boundary_case_count"] >= 1
    assert inputs["missing_review_summary"]["total_missing_review_field_count"] >= 1
    assert inputs["source_context"]["fixture_mode_used"] is True
    assert inputs["warnings"]["threshold_changes_not_applied"] is True
    assert inputs["non_claims"]["not_runtime_calibration"] is True


def test_validate_calibration_inputs_rejects_forbidden_tokens(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_calibration_inputs(paths)
    inputs = json.loads(paths["calibration_inputs"].read_text(encoding="utf-8"))
    inputs["accuracy"] = "truth"
    paths["calibration_inputs"].write_text(json.dumps(inputs), encoding="utf-8")

    result = validate_review_guided_gameplay_calibration_inputs(
        contract_path=paths["calibration_contract"],
        calibration_inputs_path=paths["calibration_inputs"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_field_or_value"
    }


def test_build_calibration_proposal_keeps_all_candidates_not_applied(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_calibration_inputs(paths)

    result = build_review_guided_gameplay_calibration_proposal(
        contract_path=paths["calibration_contract"],
        calibration_inputs_path=paths["calibration_inputs"],
        output_path=paths["calibration_proposal"],
        generated_at=datetime(2026, 6, 19, 20, 15, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["proposal_type"] == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE

    proposal = json.loads(paths["calibration_proposal"].read_text(encoding="utf-8"))
    proposal_types = {item["proposal_type"] for item in proposal["proposal_items"]}
    assert "missing_review_data_blocker" in proposal_types
    assert "human_review_batch_candidate" in proposal_types
    assert "threshold_review_candidate" in proposal_types
    assert "smoothing_window_review_candidate" in proposal_types
    assert "broadcast_replay_confusion_review" in proposal_types
    assert "commercial_or_graphic_confusion_review" in proposal_types
    assert "no_calibration_action" in proposal_types
    assert proposal["summary"]["no_runtime_changes_applied"] is True
    assert proposal["summary"]["candidate_settings_not_applied"] is True
    assert proposal["summary"]["threshold_changes_not_applied"] is True
    assert proposal["summary"]["smoothing_changes_not_applied"] is True
    assert proposal["summary"]["hysteresis_changes_not_applied"] is True
    assert proposal["summary"]["classifier_not_modified"] is True
    assert all(
        item["proposed_candidate_setting"]["not_applied"] is True
        for item in proposal["proposal_items"]
    )
    assert all(
        item["proposed_candidate_setting"]["writes_runtime_config"] is False
        for item in proposal["proposal_items"]
    )
    assert all(
        item["proposed_candidate_setting"]["affects_regression_baselines"] is False
        for item in proposal["proposal_items"]
    )
    assert all(
        item["proposed_candidate_setting"]["future_evaluation_only"] is True
        for item in proposal["proposal_items"]
    )


def test_validate_calibration_proposal_rejects_runtime_changing_candidates(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_calibration_proposal(paths)
    proposal = json.loads(paths["calibration_proposal"].read_text(encoding="utf-8"))
    proposal["proposal_items"][0]["proposal_type"] = "unsupported_candidate"
    proposal["proposal_items"][0]["proposal_status"] = "applied"
    proposal["proposal_items"][0]["proposed_evaluation_action"] = "change_gate_now"
    proposal["proposal_items"][0]["risk_flags"] = ["model_updated"]
    proposal["proposal_items"][0]["proposed_candidate_setting"]["not_applied"] = False
    proposal["proposal_items"][0]["proposed_candidate_setting"][
        "writes_runtime_config"
    ] = True
    proposal["proposal_items"][0]["proposed_candidate_setting"][
        "affects_regression_baselines"
    ] = True
    proposal["proposal_items"][0]["proposed_candidate_setting"][
        "future_evaluation_only"
    ] = False
    paths["calibration_proposal"].write_text(json.dumps(proposal), encoding="utf-8")

    result = validate_review_guided_gameplay_calibration_proposal(
        contract_path=paths["calibration_contract"],
        calibration_proposal_path=paths["calibration_proposal"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "unsupported_proposal_type",
        "unsupported_proposal_status",
        "unsupported_evaluation_action",
        "unsupported_risk_flag",
        "candidate_setting_must_be_not_applied",
        "candidate_setting_must_not_write_runtime_config",
        "candidate_setting_must_not_affect_baselines",
        "candidate_setting_must_be_future_evaluation_only",
        "forbidden_field_or_value",
    }


def test_build_calibration_proposal_report_is_structural_only(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_calibration_proposal(paths)

    result = build_review_guided_gameplay_calibration_proposal_report(
        contract_path=paths["calibration_contract"],
        calibration_proposal_path=paths["calibration_proposal"],
        output_path=paths["calibration_report"],
        generated_at=datetime(2026, 6, 19, 20, 30, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE

    report = json.loads(paths["calibration_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T20:30:00+00:00"
    assert report["validation_snapshot"]["ok"] is True
    assert report["proposal_summary"]["no_runtime_changes_applied"] is True
    assert report["proposal_type_counts"]["threshold_review_candidate"] == 1
    assert report["proposal_status_counts"]["blocked_fixture_only_data"] == 1
    assert report["warnings"]["threshold_changes_not_applied"] is True
    assert report["warnings"]["model_weights_not_modified"] is True
    assert report["non_claims"]["not_model_tuning"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "broadcast_clip.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    media_2 = tmp_path / "broadcast_clip_2.mp4"
    media_2.write_bytes(b"not a real video either; probe runner supplies metadata")
    media_3 = tmp_path / "broadcast_clip_3.mp4"
    media_3.write_bytes(b"still not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "media_2": media_2,
        "media_3": media_3,
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
        "calibration_report": tmp_path / "calibration_report.json",
    }


def _build_calibration_proposal(paths: dict[str, Path]) -> None:
    _build_calibration_inputs(paths)
    build_review_guided_gameplay_calibration_proposal(
        contract_path=paths["calibration_contract"],
        calibration_inputs_path=paths["calibration_inputs"],
        output_path=paths["calibration_proposal"],
    )


def _build_calibration_inputs(paths: dict[str, Path]) -> None:
    _build_review_metrics_report(paths)
    build_review_guided_gameplay_calibration_inputs(
        contract_path=paths["calibration_contract"],
        source_metrics_report_path=paths["metrics_report"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_review_dataset_path=None,
        source_corpus_run_path=paths["corpus_run"],
        source_regression_baseline_path=None,
        model_asset_path=paths["asset"],
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
    export_review_guided_gameplay_calibration_proposal_contract(
        output_path=paths["calibration_contract"]
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
        local_media_paths=[paths["media"], paths["media_2"], paths["media_3"]],
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
