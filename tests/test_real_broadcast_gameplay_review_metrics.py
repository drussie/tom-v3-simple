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
    ALLOWED_NEXT_ACTION_TYPES,
    DASHBOARD_CARD_IDS,
    DASHBOARD_TABLE_IDS,
    FORBIDDEN_REVIEW_METRICS_TOKENS,
    METRIC_GROUPS,
    REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE,
    REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION,
    REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
    REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
    build_real_broadcast_gameplay_review_metrics_report,
    build_real_broadcast_gameplay_review_next_actions_report,
    build_real_broadcast_gameplay_review_qa_dashboard,
    export_real_broadcast_gameplay_review_metrics_contract,
    validate_real_broadcast_gameplay_review_metrics_report,
)


def test_export_review_metrics_contract_is_stable(tmp_path: Path) -> None:
    paths = _paths(tmp_path)

    result = export_real_broadcast_gameplay_review_metrics_contract(
        output_path=paths["metrics_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE
    assert result["contract_version"] == (
        REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION
    )

    contract = json.loads(paths["metrics_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["metrics_scope"]["builds_metrics_report"] is True
    assert contract["metrics_scope"]["builds_dashboard_ready_json"] is True
    assert contract["metrics_scope"]["calculates_classifier_accuracy"] is False
    assert contract["metrics_scope"]["automatic_relabeling_allowed"] is False
    assert contract["metrics_scope"]["threshold_changes_allowed"] is False
    assert contract["metrics_scope"]["model_tuning_allowed"] is False
    assert contract["source_contract_refs"][
        "real_broadcast_gameplay_review_loop_contract_version"
    ] == "v1"
    assert contract["metric_groups"] == METRIC_GROUPS
    assert contract["qa_dashboard_schema"]["allowed_card_ids"] == DASHBOARD_CARD_IDS
    assert contract["qa_dashboard_schema"]["allowed_table_ids"] == DASHBOARD_TABLE_IDS
    assert (
        contract["next_actions_schema"]["allowed_next_action_types"]
        == ALLOWED_NEXT_ACTION_TYPES
    )
    assert not (FORBIDDEN_REVIEW_METRICS_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_review_metrics_report_summarizes_bp47_review_bundle(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_loop_report_with_one_completed_review(paths)

    result = build_real_broadcast_gameplay_review_metrics_report(
        contract_path=paths["metrics_contract"],
        source_review_loop_report_path=paths["review_loop_report"],
        source_review_bundle_path=paths["review_bundle"],
        source_corpus_run_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        output_path=paths["metrics_report"],
        generated_at=datetime(2026, 6, 19, 18, 30, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["metrics_report_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE

    report = json.loads(paths["metrics_report"].read_text(encoding="utf-8"))
    coverage = report["metric_groups"]["review_coverage"]
    segment = report["metric_groups"]["segment_status_distribution"]
    downstream = report["metric_groups"]["downstream_gate_review_distribution"]
    confidence = report["metric_groups"]["confidence_distribution"]
    ambiguity = report["metric_groups"]["ambiguity_flag_distribution"]
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))

    assert report["generated_at"] == "2026-06-19T18:30:00+00:00"
    assert coverage["review_bundle_entry_count"] == len(bundle["entries"])
    assert coverage["reviewed_entry_count"] == 1
    assert coverage["review_completion_rate"] == round(1 / len(bundle["entries"]), 6)
    assert coverage["rates_are_operational_completeness_only"] is True
    assert coverage["classifier_correctness_not_assessed"] is True
    assert segment["reviewed_as_gameplay_candidate_count"] == 1
    assert downstream["reviewer_would_allow_downstream_observation_count"] == 1
    assert confidence["review_confidence_high_count"] == 1
    assert ambiguity["camera_cut_unclear_count"] == 1
    assert report["model_asset_ref"] == str(paths["asset"])
    assert report["model_asset_sha256"]
    assert report["warnings"]["metrics_are_not_truth"] is True
    assert report["non_claims"]["not_automatic_relabeling"] is True


def test_validate_review_metrics_report_rejects_unsupported_and_forbidden_tokens(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_metrics_report(paths)
    report = json.loads(paths["metrics_report"].read_text(encoding="utf-8"))
    report["metric_groups"]["accuracy"] = {}
    report["truth"] = "not_allowed"
    paths["metrics_report"].write_text(json.dumps(report), encoding="utf-8")

    result = validate_real_broadcast_gameplay_review_metrics_report(
        contract_path=paths["metrics_contract"],
        metrics_report_path=paths["metrics_report"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "unsupported_metric_group",
        "forbidden_field_or_value",
    }


def test_build_review_metrics_qa_dashboard_is_structural_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_metrics_report(paths)

    result = build_real_broadcast_gameplay_review_qa_dashboard(
        contract_path=paths["metrics_contract"],
        metrics_report_path=paths["metrics_report"],
        output_path=paths["qa_dashboard"],
        generated_at=datetime(2026, 6, 19, 18, 45, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["dashboard_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE

    dashboard = json.loads(paths["qa_dashboard"].read_text(encoding="utf-8"))
    assert dashboard["generated_at"] == "2026-06-19T18:45:00+00:00"
    assert dashboard["validation_snapshot"]["ok"] is True
    assert [card["card_id"] for card in dashboard["cards"]] == DASHBOARD_CARD_IDS
    assert [table["table_id"] for table in dashboard["tables"]] == DASHBOARD_TABLE_IDS
    assert all(card["structural_only"] is True for card in dashboard["cards"])
    assert all(table["structural_only"] is True for table in dashboard["tables"])


def test_build_review_metrics_next_actions_keeps_review_operations_boundary(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_metrics_report(paths)

    result = build_real_broadcast_gameplay_review_next_actions_report(
        contract_path=paths["metrics_contract"],
        metrics_report_path=paths["metrics_report"],
        output_path=paths["next_actions"],
        generated_at=datetime(2026, 6, 19, 19, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"

    report = json.loads(paths["next_actions"].read_text(encoding="utf-8"))
    action_types = {action["action_type"] for action in report["prioritized_actions"]}
    assert "review_unreviewed_entries" in action_types
    assert "complete_missing_review_fields" in action_types
    assert "prepare_human_review_batch" in action_types
    assert all(
        action["changes_labels_or_thresholds"] is False
        for action in report["prioritized_actions"]
    )
    assert all(action["review_operations_only"] is True for action in report["prioritized_actions"])


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "broadcast_clip.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
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
        "qa_dashboard": tmp_path / "review_qa_dashboard.json",
        "next_actions": tmp_path / "review_next_actions.json",
    }


def _build_review_metrics_report(paths: dict[str, Path]) -> None:
    _build_review_bundle(paths)
    build_real_broadcast_gameplay_review_loop_report(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_loop_report"],
    )
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


def _build_review_loop_report_with_one_completed_review(paths: dict[str, Path]) -> None:
    _build_review_bundle(paths)
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    bundle["entries"][0]["human_review"] = {
        **bundle["entries"][0]["human_review"],
        "reviewer_id": "reviewer-1",
        "reviewed_at": "2026-06-19T18:20:00+00:00",
        "reviewed_segment_status": "reviewed_as_gameplay_candidate",
        "reviewed_downstream_gate_status": (
            "reviewer_would_allow_downstream_observation"
        ),
        "review_confidence": "high",
        "ambiguity_flags": ["camera_cut_unclear"],
        "reviewer_notes": "metadata only",
        "review_source": "manual_json_review",
    }
    paths["review_bundle"].write_text(json.dumps(bundle), encoding="utf-8")
    build_real_broadcast_gameplay_review_loop_report(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_loop_report"],
    )
    export_real_broadcast_gameplay_review_metrics_contract(
        output_path=paths["metrics_contract"]
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
        local_media_paths=[paths["media"]],
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
