from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_regression_baseline import (
    FORBIDDEN_REGRESSION_TOKENS,
    GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE,
    GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION,
    GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE,
    GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
    GAMEPLAY_GATE_REGRESSION_REPORT_TYPE,
    build_gameplay_gate_regression_baseline,
    build_gameplay_gate_regression_report,
    export_gameplay_gate_regression_baseline_contract,
    verify_gameplay_gate_regression_baseline,
)
from apps.worker.services.gameplay_gated_many_point_smoke import (
    build_gameplay_gated_many_point_smoke_manifest_template,
)


def test_export_gameplay_gate_regression_contract_is_stable(tmp_path: Path) -> None:
    paths = _paths(tmp_path)

    result = export_gameplay_gate_regression_baseline_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["baseline_scope"]["freezes_structural_counts"] is True
    assert contract["baseline_scope"]["does_not_assess_classifier_correctness"] is True
    assert (
        contract["source_contract_refs"]["gameplay_gated_many_point_smoke_contract_version"]
        == "v1"
    )
    assert not (FORBIDDEN_REGRESSION_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_gameplay_gate_regression_baseline(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _write_contract_and_manifest(paths)

    result = build_gameplay_gate_regression_baseline(
        contract_path=paths["contract"],
        smoke_manifest_path=paths["manifest"],
        work_dir=paths["work_dir"],
        model_asset_path=paths["asset"],
        output_path=paths["baseline"],
        generated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["baseline_type"] == GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE
    assert result["baseline_version"] == GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION

    baseline = json.loads(paths["baseline"].read_text(encoding="utf-8"))
    assert baseline["generated_at"] == "2026-06-19T12:00:00+00:00"
    assert baseline["classifier_asset_exists"] is True
    assert baseline["model_asset_sha256"]
    assert baseline["entry_count"] == 2
    assert baseline["gameplay_segment_candidate_count"] >= 2
    assert baseline["warnings"]["fixture_reuse_only"] is True
    assert baseline["non_claims"]["not_classifier_accuracy_benchmark"] is True


def test_verify_gameplay_gate_regression_baseline_no_drift(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)

    result = verify_gameplay_gate_regression_baseline(
        contract_path=paths["contract"],
        baseline_path=paths["baseline"],
        smoke_manifest_path=paths["manifest"],
        work_dir=paths["work_dir"],
        model_asset_path=paths["asset"],
        output_path=paths["verification"],
        verified_at=datetime(2026, 6, 19, 13, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["drift_detected"] is False
    assert result["breaking_drift_detected"] is False
    assert result["baseline_is_not_truth"] is True
    assert result["gameplay_gate_is_not_truth"] is True
    assert result["classifier_correctness_not_assessed"] is True
    assert result["generalization_not_claimed"] is True


def test_verify_gameplay_gate_regression_baseline_detects_drift(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)
    baseline = json.loads(paths["baseline"].read_text(encoding="utf-8"))
    baseline["summary"]["gameplay_segment_candidate_count"] += 10
    paths["baseline"].write_text(json.dumps(baseline), encoding="utf-8")

    result = verify_gameplay_gate_regression_baseline(
        contract_path=paths["contract"],
        baseline_path=paths["baseline"],
        smoke_manifest_path=paths["manifest"],
        work_dir=paths["work_dir"],
        model_asset_path=paths["asset"],
        output_path=None,
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is False
    assert result["status"] == "breaking_drift_detected"
    assert result["drift_detected"] is True
    assert result["breaking_drift_detected"] is True
    assert any(
        item["field"] == "gameplay_segment_candidate_count"
        and item["severity"] == "breaking"
        for item in result["drift_items"]
    )


def test_build_gameplay_gate_regression_report(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_baseline(paths)
    verify_gameplay_gate_regression_baseline(
        contract_path=paths["contract"],
        baseline_path=paths["baseline"],
        smoke_manifest_path=paths["manifest"],
        work_dir=paths["work_dir"],
        model_asset_path=paths["asset"],
        output_path=paths["verification"],
        probe_runner=_fake_probe_runner(),
    )

    result = build_gameplay_gate_regression_report(
        contract_path=paths["contract"],
        baseline_path=paths["baseline"],
        verification_path=paths["verification"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 19, 14, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATE_REGRESSION_REPORT_TYPE
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["verification_status"] == "completed"
    assert report["summary"]["report_is_structural_only"] is True
    assert report["non_claims"]["not_generalization_claim"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "sample_point.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "asset": asset,
        "contract": tmp_path / "contract.json",
        "manifest": tmp_path / "manifest.json",
        "baseline": tmp_path / "baseline.json",
        "verification": tmp_path / "verification.json",
        "report": tmp_path / "report.json",
        "work_dir": tmp_path / "work",
    }


def _write_contract_and_manifest(paths: dict[str, Path]) -> None:
    export_gameplay_gate_regression_baseline_contract(output_path=paths["contract"])
    build_gameplay_gated_many_point_smoke_manifest_template(
        local_media_paths=[paths["media"], paths["media"]],
        source_label="regression_fixture",
        output_path=paths["manifest"],
        generated_at=datetime(2026, 6, 19, 11, 0, tzinfo=UTC),
        allow_fixture_mode=True,
    )


def _build_baseline(paths: dict[str, Path]) -> None:
    _write_contract_and_manifest(paths)
    build_gameplay_gate_regression_baseline(
        contract_path=paths["contract"],
        smoke_manifest_path=paths["manifest"],
        work_dir=paths["work_dir"],
        model_asset_path=paths["asset"],
        output_path=paths["baseline"],
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
        for nested in value:
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        seen.add(value)
    return seen
