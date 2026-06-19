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
    ALLOWED_AMBIGUITY_FLAGS,
    ALLOWED_REVIEW_CONFIDENCE_VALUES,
    ALLOWED_REVIEW_SOURCE_VALUES,
    ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES,
    ALLOWED_REVIEWED_SEGMENT_STATUSES,
    FORBIDDEN_REVIEW_LOOP_TOKENS,
    REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE,
    REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION,
    REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE,
    REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION,
    REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE,
    build_real_broadcast_gameplay_human_review_readiness_report,
    build_real_broadcast_gameplay_review_bundle_template,
    build_real_broadcast_gameplay_review_loop_report,
    export_real_broadcast_gameplay_review_loop_contract,
    validate_real_broadcast_gameplay_review_bundle,
)


def test_export_real_broadcast_gameplay_review_loop_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_real_broadcast_gameplay_review_loop_contract(
        output_path=paths["review_loop_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE
    assert result["contract_version"] == REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION

    contract = json.loads(paths["review_loop_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["review_loop_scope"]["captures_human_review_metadata"] is True
    assert contract["review_loop_scope"]["creates_review_labels"] is False
    assert contract["review_loop_scope"]["automatic_relabeling_allowed"] is False
    assert contract["review_loop_scope"]["mutates_model_assets"] is False
    assert contract["review_loop_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["source_contract_refs"][
            "real_broadcast_gameplay_corpus_run_contract_version"
        ]
        == "v1"
    )
    assert (
        set(contract["review_entry_schema"]["allowed_reviewed_segment_statuses"])
        == ALLOWED_REVIEWED_SEGMENT_STATUSES
    )
    assert (
        set(contract["review_entry_schema"]["allowed_reviewed_downstream_gate_statuses"])
        == ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES
    )
    assert (
        set(contract["review_entry_schema"]["allowed_review_confidence_values"])
        == ALLOWED_REVIEW_CONFIDENCE_VALUES
    )
    assert (
        set(contract["review_entry_schema"]["allowed_ambiguity_flags"])
        == ALLOWED_AMBIGUITY_FLAGS
    )
    assert (
        set(contract["review_entry_schema"]["allowed_review_source_values"])
        == ALLOWED_REVIEW_SOURCE_VALUES
    )
    assert not (FORBIDDEN_REVIEW_LOOP_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_review_bundle_template_from_fixture_corpus_run(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_fixture_corpus_run(paths)
    export_real_broadcast_gameplay_review_loop_contract(
        output_path=paths["review_loop_contract"]
    )

    result = build_real_broadcast_gameplay_review_bundle_template(
        contract_path=paths["review_loop_contract"],
        source_corpus_run_path=paths["corpus_run"],
        model_asset_path=paths["asset"],
        output_path=paths["review_bundle"],
        generated_at=datetime(2026, 6, 19, 16, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["review_bundle_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE
    assert result["review_bundle_version"] == REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION

    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    assert bundle["generated_at"] == "2026-06-19T16:00:00+00:00"
    assert bundle["model_asset_exists"] is True
    assert bundle["model_asset_sha256"]
    assert bundle["summary"]["review_bundle_entry_count"] == len(bundle["entries"])
    assert bundle["summary"]["review_pending_count"] == len(bundle["entries"])
    assert bundle["warnings"]["review_loop_is_not_truth"] is True
    assert bundle["non_claims"]["not_automatic_relabeling"] is True

    first_entry = bundle["entries"][0]
    assert first_entry["expected_broadcast_content_tags"] == ["live_gameplay"]
    assert "segmentId=" in first_entry["replay_url"]
    assert first_entry["segment_start_ms"] is not None
    assert first_entry["human_review"] == {
        "reviewer_id": None,
        "reviewed_at": None,
        "reviewed_segment_status": "not_reviewed",
        "reviewed_downstream_gate_status": "no_review_decision",
        "review_confidence": "not_assessed",
        "ambiguity_flags": [],
        "reviewer_notes": None,
        "needs_additional_review": False,
        "review_duration_seconds": None,
        "review_source": "not_assessed",
    }

    validation = validate_real_broadcast_gameplay_review_bundle(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_bundle_validation"],
        validated_at=datetime(2026, 6, 19, 16, 5, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_validate_review_bundle_rejects_forbidden_and_bad_human_review(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_bundle(paths)
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    bundle["entries"][0]["truth"] = "not_allowed"
    bundle["entries"][0]["human_review"]["review_confidence"] = "certain"
    bundle["entries"][0]["human_review"]["review_source"] = "sideline_guess"
    bundle["entries"][0]["human_review"]["ambiguity_flags"] = ["settled"]
    paths["review_bundle"].write_text(json.dumps(bundle), encoding="utf-8")

    result = validate_real_broadcast_gameplay_review_bundle(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_field_or_value",
        "invalid_review_confidence",
        "invalid_review_source",
        "invalid_ambiguity_flag",
    }


def test_build_review_loop_report_summarizes_review_metadata(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_bundle(paths)
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    entry_count = len(bundle["entries"])
    bundle["entries"][0]["human_review"] = {
        **bundle["entries"][0]["human_review"],
        "reviewer_id": "reviewer-1",
        "reviewed_at": "2026-06-19T17:00:00+00:00",
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

    result = build_real_broadcast_gameplay_review_loop_report(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["review_loop_report"],
        generated_at=datetime(2026, 6, 19, 17, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE
    report = json.loads(paths["review_loop_report"].read_text(encoding="utf-8"))
    assert report["summary"]["review_bundle_entry_count"] == entry_count
    assert report["summary"]["reviewed_entry_count"] == 1
    assert report["summary"]["unreviewed_entry_count"] == entry_count - 1
    assert report["summary"]["reviewed_as_gameplay_candidate_count"] == 1
    assert report["summary"]["downstream_allow_review_count"] == 1
    assert report["summary"]["confidence_distribution"]["high"] == 1
    assert report["summary"]["ambiguity_flag_counts"]["camera_cut_unclear"] == 1
    assert report["warnings"]["classifier_correctness_not_assessed"] is True
    assert report["non_claims"]["not_classifier_accuracy_benchmark"] is True


def test_build_human_review_readiness_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_review_bundle(paths)

    result = build_real_broadcast_gameplay_human_review_readiness_report(
        contract_path=paths["review_loop_contract"],
        bundle_path=paths["review_bundle"],
        output_path=paths["human_review_readiness_report"],
        generated_at=datetime(2026, 6, 19, 18, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    readiness = result["readiness"]
    bundle = json.loads(paths["review_bundle"].read_text(encoding="utf-8"))
    assert readiness["ready_for_human_review"] is True
    assert readiness["review_bundle_entry_count"] == len(bundle["entries"])
    assert readiness["review_pending_count"] == len(bundle["entries"])
    assert readiness["readiness_is_not_correctness"] is True
    assert readiness["classifier_correctness_not_assessed"] is True


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
        "review_bundle_validation": tmp_path / "review_bundle.validation.json",
        "review_loop_report": tmp_path / "review_loop_report.json",
        "human_review_readiness_report": tmp_path / "human_review_readiness.json",
    }


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
