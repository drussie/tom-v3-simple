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
    ALLOWED_EXPECTED_BROADCAST_CONTENT_TAGS,
    ALLOWED_REQUESTED_STEPS,
    ALLOWED_RUN_MODES,
    FORBIDDEN_CORPUS_TOKENS,
    REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE,
    REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
    REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
    REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
    REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE,
    REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION,
    REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE,
    REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION,
    build_real_broadcast_gameplay_corpus_manifest_template,
    build_real_broadcast_gameplay_corpus_report,
    export_real_broadcast_gameplay_corpus_run_contract,
    run_real_broadcast_gameplay_corpus,
    validate_real_broadcast_gameplay_corpus_manifest,
)


def test_export_real_broadcast_gameplay_corpus_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_real_broadcast_gameplay_corpus_run_contract(
        output_path=paths["corpus_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE
    assert result["contract_version"] == REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION

    contract = json.loads(paths["corpus_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["corpus_run_scope"]["default_run_mode"] == "dry_run"
    assert contract["corpus_run_scope"]["automatic_media_discovery_allowed"] is False
    assert contract["corpus_run_scope"]["silent_folder_scan_allowed"] is False
    assert contract["corpus_run_scope"]["trains_or_modifies_classifier"] is False
    assert contract["corpus_run_scope"]["commits_model_weights"] is False
    assert set(contract["corpus_run_scope"]["allowed_run_modes"]) == ALLOWED_RUN_MODES
    assert (
        set(contract["input_manifest_schema"]["allowed_expected_broadcast_content_tags"])
        == ALLOWED_EXPECTED_BROADCAST_CONTENT_TAGS
    )
    assert (
        set(contract["input_manifest_schema"]["allowed_requested_steps"])
        == ALLOWED_REQUESTED_STEPS
    )
    assert (
        contract["source_contract_refs"][
            "gameplay_gate_pathway_completion_freeze_version"
        ]
        == "v1"
    )
    assert not (FORBIDDEN_CORPUS_TOKENS & _walk_exact_strings_and_keys(contract))


def test_manifest_template_and_validation_preserve_broadcast_context_tags(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)

    result = build_real_broadcast_gameplay_corpus_manifest_template(
        local_media_paths=[paths["media"]],
        source_label="broadcast_clip",
        expected_broadcast_content_tags=["live_gameplay", "replay_package"],
        output_path=paths["manifest"],
        generated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["entry_count"] == 1
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["manifest_type"] == REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE
    assert manifest["manifest_version"] == REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION
    assert manifest["default_run_mode"] == "dry_run"
    assert manifest["entries"][0]["expected_broadcast_content_tags"] == [
        "live_gameplay",
        "replay_package",
    ]
    assert manifest["entries"][0]["allow_fixture_mode"] is False
    assert manifest["warnings"]["content_tags_are_operator_context_not_truth"] is True

    validation = validate_real_broadcast_gameplay_corpus_manifest(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["manifest"],
        output_path=paths["manifest_validation"],
        run_mode="dry_run",
        validated_at=datetime(2026, 6, 19, 12, 5, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["structural_warning_count"] == 0


def test_manifest_validation_rejects_disallowed_steps_and_real_missing_paths(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_real_broadcast_gameplay_corpus_manifest_template(
        local_media_paths=[tmp_path / "missing.mp4"],
        output_path=paths["manifest"],
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    manifest["entries"][0]["requested_steps"].append("calculate_classifier_accuracy")
    manifest["entries"][0]["score"] = "15-0"
    paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_real_broadcast_gameplay_corpus_manifest(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["manifest"],
        output_path=None,
        run_mode="explicit_local_media_run",
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "disallowed_requested_step",
        "forbidden_token_key",
        "local_media_path_not_found",
    }


def test_run_real_broadcast_gameplay_corpus_dry_run_does_not_process_missing_path(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_real_broadcast_gameplay_corpus_manifest_template(
        output_path=paths["manifest"],
        generated_at=datetime(2026, 6, 19, 13, 0, tzinfo=UTC),
    )

    result = run_real_broadcast_gameplay_corpus(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["manifest"],
        run_mode="dry_run",
        output_dir=paths["output_dir"],
        output_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        generated_at=datetime(2026, 6, 19, 13, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE
    assert result["report_version"] == REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION
    report = json.loads(paths["corpus_run"].read_text(encoding="utf-8"))
    assert report["run_mode"] == "dry_run"
    assert report["entry_count"] == 1
    assert report["processed_entry_count"] == 0
    assert report["skipped_entry_count"] == 1
    assert report["entries"][0]["status"] == "dry_run_planned"
    assert report["entries"][0]["artifact_outputs"] == {}
    assert report["warnings"]["default_mode_is_dry_run"] is True


def test_run_real_broadcast_gameplay_corpus_fixture_mode_builds_review_chain(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_real_broadcast_gameplay_corpus_manifest_template(
        local_media_paths=[paths["media"]],
        source_label="broadcast_fixture",
        expected_broadcast_content_tags=["live_gameplay"],
        output_path=paths["manifest"],
        allow_fixture_mode=True,
    )

    result = run_real_broadcast_gameplay_corpus(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["manifest"],
        run_mode="fixture_only",
        output_dir=paths["output_dir"],
        output_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        gameplay_segment_contract_path=paths["gameplay_contract"],
        routing_contract_path=paths["routing_contract"],
        execution_contract_path=paths["execution_contract"],
        replay_review_contract_path=paths["review_contract"],
        review_dataset_contract_path=paths["review_dataset_contract"],
        generated_at=datetime(2026, 6, 19, 14, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    report = json.loads(paths["corpus_run"].read_text(encoding="utf-8"))
    entry = report["entries"][0]
    assert entry["status"] == "fixture_completed"
    assert entry["gameplay_segment_candidate_count"] >= 1
    assert (
        entry["downstream_allowed_window_count"]
        + entry["downstream_blocked_window_count"]
        + entry["downstream_review_required_window_count"]
    ) >= 1
    assert entry["replay_timeline_entry_count"] >= 1
    assert entry["review_dataset_entry_count"] >= 1
    assert entry["model_asset"]["sha256"]
    assert report["summary"]["processed_entry_count"] == 1
    assert report["warnings"]["classifier_accuracy_not_claimed"] is True


def test_build_real_broadcast_gameplay_corpus_report_validates_run_output(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_real_broadcast_gameplay_corpus_manifest_template(
        local_media_paths=[paths["media"]],
        output_path=paths["manifest"],
        allow_fixture_mode=True,
    )
    run_real_broadcast_gameplay_corpus(
        contract_path=paths["corpus_contract"],
        manifest_path=paths["manifest"],
        run_mode="fixture_only",
        output_dir=paths["output_dir"],
        output_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        gameplay_segment_contract_path=paths["gameplay_contract"],
        routing_contract_path=paths["routing_contract"],
        execution_contract_path=paths["execution_contract"],
        replay_review_contract_path=paths["review_contract"],
        review_dataset_contract_path=paths["review_dataset_contract"],
        probe_runner=_fake_probe_runner(),
    )

    result = build_real_broadcast_gameplay_corpus_report(
        contract_path=paths["corpus_contract"],
        corpus_run_path=paths["corpus_run"],
        output_path=paths["final_report"],
        generated_at=datetime(2026, 6, 19, 15, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE
    assert result["report_version"] == REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION
    final_report = json.loads(paths["final_report"].read_text(encoding="utf-8"))
    assert final_report["report_built_at"] == "2026-06-19T15:00:00+00:00"
    assert final_report["human_review_readiness"]["ready_for_human_review"] is True
    assert final_report["validation_summary"]["status"] == "valid"
    assert final_report["human_review_readiness"]["readiness_is_not_correctness"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "broadcast_clip.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "asset": asset,
        "corpus_contract": tmp_path / "real_broadcast_gameplay_corpus_contract.json",
        "manifest": tmp_path / "real_broadcast_manifest.json",
        "manifest_validation": tmp_path / "real_broadcast_manifest.validation.json",
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "routing_contract": tmp_path / "routing_contract.json",
        "execution_contract": tmp_path / "execution_contract.json",
        "review_contract": tmp_path / "review_contract.json",
        "review_dataset_contract": tmp_path / "review_dataset_contract.json",
        "output_dir": tmp_path / "corpus_outputs",
        "corpus_run": tmp_path / "corpus_run.current.json",
        "final_report": tmp_path / "corpus_run.report.json",
    }


def _export_contracts(paths: dict[str, Path]) -> None:
    export_real_broadcast_gameplay_corpus_run_contract(
        output_path=paths["corpus_contract"]
    )
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_gated_perception_execution_contract(
        output_path=paths["execution_contract"]
    )
    export_gameplay_segment_replay_review_contract(output_path=paths["review_contract"])
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
