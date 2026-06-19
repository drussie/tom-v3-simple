from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_review_dataset_export import (
    ALLOWED_AMBIGUITY_FLAGS,
    ALLOWED_REVIEW_CONFIDENCE_VALUES,
    ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES,
    ALLOWED_REVIEWED_SEGMENT_STATUSES,
    FORBIDDEN_REVIEW_DATASET_TOKENS,
    GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE,
    GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
    GAMEPLAY_GATE_REVIEW_DATASET_REPORT_TYPE,
    GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
    GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
    build_gameplay_gate_review_dataset,
    build_gameplay_gate_review_dataset_report,
    export_gameplay_gate_review_dataset_contract,
    validate_gameplay_gate_review_dataset,
)


def test_export_gameplay_gate_review_dataset_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_gameplay_gate_review_dataset_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["dataset_scope"]["creates_review_dataset_export"] is True
    assert contract["dataset_scope"]["creates_review_labels"] is False
    assert contract["dataset_scope"]["mutates_model_assets"] is False
    assert contract["dataset_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["source_contract_refs"]["gameplay_gate_regression_baseline_contract_version"]
        == "v1"
    )
    assert set(
        contract["review_entry_schema"]["allowed_reviewed_segment_statuses"]
    ) == ALLOWED_REVIEWED_SEGMENT_STATUSES
    assert set(
        contract["review_entry_schema"]["allowed_reviewed_downstream_gate_statuses"]
    ) == ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES
    assert set(
        contract["review_entry_schema"]["allowed_review_confidence_values"]
    ) == ALLOWED_REVIEW_CONFIDENCE_VALUES
    assert set(
        contract["review_entry_schema"]["allowed_ambiguity_flags"]
    ) == ALLOWED_AMBIGUITY_FLAGS
    assert not (FORBIDDEN_REVIEW_DATASET_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_gameplay_gate_review_dataset(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _write_contract_and_regression_context(paths)

    result = build_gameplay_gate_review_dataset(
        contract_path=paths["contract"],
        work_dir=paths["work_dir"],
        fixture_media_path=paths["media"],
        model_asset_path=paths["asset"],
        regression_baseline_path=paths["baseline"],
        regression_verification_path=paths["verification"],
        output_path=paths["dataset"],
        generated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["dataset_type"] == GAMEPLAY_GATE_REVIEW_DATASET_TYPE
    assert result["dataset_version"] == GAMEPLAY_GATE_REVIEW_DATASET_VERSION

    dataset = json.loads(paths["dataset"].read_text(encoding="utf-8"))
    assert dataset["generated_at"] == "2026-06-19T12:00:00+00:00"
    assert dataset["model_asset_exists"] is True
    assert dataset["model_asset_sha256"]
    assert dataset["baseline_context"]["verification_status"] == "completed"
    assert dataset["summary"]["entry_count"] == len(dataset["entries"])
    assert dataset["summary"]["human_review_pending_count"] == len(dataset["entries"])
    assert dataset["summary"]["classifier_correctness_not_assessed"] is True
    assert dataset["summary"]["dataset_is_not_truth"] is True

    first_entry = dataset["entries"][0]
    assert "segmentId=" in first_entry["replay_url"]
    assert "startMs=" in first_entry["replay_url"]
    assert "endMs=" in first_entry["replay_url"]
    assert first_entry["review_status"] == "not_reviewed"
    assert first_entry["human_review_fields"] == {
        "reviewer_id": None,
        "reviewed_at": None,
        "reviewed_segment_status": "not_reviewed",
        "reviewed_downstream_gate_status": "no_review_decision",
        "review_confidence": "not_assessed",
        "ambiguity_flags": [],
        "reviewer_notes": None,
        "needs_additional_review": False,
    }
    assert first_entry["provenance_status"] == "source_artifacts_available"

    validation = validate_gameplay_gate_review_dataset(
        contract_path=paths["contract"],
        dataset_path=paths["dataset"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 19, 13, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_validate_gameplay_gate_review_dataset_rejects_forbidden_and_bad_metadata(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_dataset(paths)
    dataset = json.loads(paths["dataset"].read_text(encoding="utf-8"))
    dataset["entries"][0]["truth"] = "not_allowed"
    dataset["entries"][0]["human_review_fields"]["review_confidence"] = "certain"
    paths["dataset"].write_text(json.dumps(dataset), encoding="utf-8")

    result = validate_gameplay_gate_review_dataset(
        contract_path=paths["contract"],
        dataset_path=paths["dataset"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_field_or_value",
        "invalid_review_confidence",
    }


def test_build_gameplay_gate_review_dataset_report(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_dataset(paths)

    result = build_gameplay_gate_review_dataset_report(
        contract_path=paths["contract"],
        dataset_path=paths["dataset"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 19, 14, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATE_REVIEW_DATASET_REPORT_TYPE
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["summary"]["human_review_pending_count"] == report["entry_count"]
    assert report["summary"]["classifier_correctness_not_assessed"] is True
    assert report["summary"]["dataset_is_not_truth"] is True
    assert report["non_claims"]["not_classifier_correctness_benchmark"] is True
    assert report["validation_snapshot"]["status"] == "valid"


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "sample_point.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "asset": asset,
        "contract": tmp_path / "contract.json",
        "baseline": tmp_path / "baseline.json",
        "verification": tmp_path / "verification.json",
        "dataset": tmp_path / "dataset.json",
        "validation": tmp_path / "validation.json",
        "report": tmp_path / "report.json",
        "work_dir": tmp_path / "work",
    }


def _write_contract_and_regression_context(paths: dict[str, Path]) -> None:
    export_gameplay_gate_review_dataset_contract(output_path=paths["contract"])
    paths["baseline"].write_text(
        json.dumps(
            {
                "baseline_id": "gameplay_gate_regression_baseline_fixture",
                "baseline_type": "gameplay_gate_regression_baseline",
                "baseline_version": "v1",
                "model_asset_sha256": "fixture-model-sha",
                "threshold": 0.55,
                "smoothing_window": 3,
                "hysteresis_settings": {
                    "enter_gameplay_min_consecutive": 2,
                    "exit_gameplay_min_consecutive": 2,
                },
                "summary": {},
            }
        ),
        encoding="utf-8",
    )
    paths["verification"].write_text(
        json.dumps(
            {
                "status": "completed",
                "drift_detected": False,
                "breaking_drift_detected": False,
            }
        ),
        encoding="utf-8",
    )


def _build_dataset(paths: dict[str, Path]) -> None:
    _write_contract_and_regression_context(paths)
    build_gameplay_gate_review_dataset(
        contract_path=paths["contract"],
        work_dir=paths["work_dir"],
        fixture_media_path=paths["media"],
        model_asset_path=paths["asset"],
        regression_baseline_path=paths["baseline"],
        regression_verification_path=paths["verification"],
        output_path=paths["dataset"],
        probe_runner=_fake_probe_runner(),
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
        for item in value:
            seen.update(_walk_exact_strings_and_keys(item))
    elif isinstance(value, str):
        seen.add(value)
    return seen
