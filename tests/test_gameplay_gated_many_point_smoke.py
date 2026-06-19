from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_many_point_smoke import (
    ALLOWED_SMOKE_MODES,
    ALLOWED_SMOKE_STEPS,
    FORBIDDEN_SMOKE_TOKENS,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
    build_gameplay_gated_many_point_smoke_manifest_template,
    build_gameplay_gated_many_point_smoke_report,
    export_gameplay_gated_many_point_smoke_contract,
    run_gameplay_gated_many_point_smoke,
    validate_gameplay_gated_many_point_smoke_manifest,
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
from apps.worker.services.many_point_ingestion_gate import (
    export_many_point_ingestion_gate_contract,
)


def test_export_gameplay_gated_many_point_smoke_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_gameplay_gated_many_point_smoke_contract(
        output_path=paths["smoke_contract"],
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION

    contract = json.loads(paths["smoke_contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["smoke_scope"]["default_smoke_mode"] == "fixture_only"
    assert contract["smoke_scope"]["runs_gpu_or_model_inference_by_default"] is False
    assert contract["smoke_scope"]["mutates_model_assets"] is False
    assert contract["smoke_scope"]["mutates_regression_baselines"] is False
    assert set(contract["smoke_scope"]["allowed_smoke_modes"]) == ALLOWED_SMOKE_MODES
    assert (
        set(contract["smoke_manifest_schema"]["allowed_requested_smoke_steps"])
        == ALLOWED_SMOKE_STEPS
    )
    assert (
        contract["source_contract_refs"]["gameplay_segment_replay_review_contract_version"]
        == "v1"
    )
    assert not (FORBIDDEN_SMOKE_TOKENS & _walk_exact_strings_and_keys(contract))


def test_smoke_manifest_template_and_validation_allow_fixture_reuse(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)

    result = build_gameplay_gated_many_point_smoke_manifest_template(
        local_media_paths=[paths["media"], paths["media"]],
        source_label="fixture_point",
        output_path=paths["manifest"],
        generated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["entry_count"] == 2
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["manifest_type"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE
    assert manifest["manifest_version"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION
    assert manifest["warnings"]["fixture_reuse_only"] is True
    assert manifest["warnings"]["not_distinct_real_points"] is True
    assert manifest["warnings"]["does_not_claim_generalization"] is True

    validation = validate_gameplay_gated_many_point_smoke_manifest(
        contract_path=paths["smoke_contract"],
        manifest_path=paths["manifest"],
        output_path=paths["manifest_validation"],
        validated_at=datetime(2026, 6, 19, 12, 5, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["structural_warning_count"] == 2
    assert validation["warnings"]["fixture_reuse_only"] is True


def test_smoke_manifest_validation_rejects_forbidden_fields_and_steps(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_gameplay_gated_many_point_smoke_manifest_template(
        local_media_paths=[paths["media"]],
        output_path=paths["manifest"],
    )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    manifest["entries"][0]["requested_smoke_steps"].append("create_truth")
    manifest["entries"][0]["score"] = "15-0"
    paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_gameplay_gated_many_point_smoke_manifest(
        contract_path=paths["smoke_contract"],
        manifest_path=paths["manifest"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "disallowed_requested_smoke_step",
        "forbidden_token_key",
    }


def test_run_gameplay_gated_many_point_smoke_builds_structural_chain(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_gameplay_gated_many_point_smoke_manifest_template(
        local_media_paths=[paths["media"], paths["media"]],
        source_label="fixture_point",
        output_path=paths["manifest"],
    )

    result = run_gameplay_gated_many_point_smoke(
        contract_path=paths["smoke_contract"],
        manifest_path=paths["manifest"],
        smoke_mode="fixture_only",
        output_dir=paths["output_dir"],
        output_path=paths["smoke_output"],
        model_asset_path=paths["asset"],
        many_point_contract_path=paths["many_point_contract"],
        gameplay_segment_contract_path=paths["gameplay_contract"],
        routing_contract_path=paths["routing_contract"],
        execution_contract_path=paths["execution_contract"],
        replay_review_contract_path=paths["review_contract"],
        generated_at=datetime(2026, 6, 19, 13, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION

    report = json.loads(paths["smoke_output"].read_text(encoding="utf-8"))
    assert report["entry_count"] == 2
    assert report["validated_entry_count"] == 2
    assert report["failed_entry_count"] == 0
    assert report["warnings"]["fixture_reuse_only"] is True
    assert report["warnings"]["not_distinct_real_points"] is True
    assert report["many_point_ingestion_gate"]["ok"] is True
    assert all(entry["status"] == "fixture_smoke_completed" for entry in report["entries"])
    assert all(entry["gameplay_segment_candidate_count"] >= 1 for entry in report["entries"])
    assert all(entry["downstream_allowed_window_count"] >= 1 for entry in report["entries"])
    assert all(entry["replay_timeline_entry_count"] >= 1 for entry in report["entries"])
    assert all(entry["model_asset"]["sha256"] for entry in report["entries"])


def test_build_gameplay_gated_many_point_smoke_report_validates_run_output(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contracts(paths)
    build_gameplay_gated_many_point_smoke_manifest_template(
        local_media_paths=[paths["media"]],
        output_path=paths["manifest"],
    )
    run_gameplay_gated_many_point_smoke(
        contract_path=paths["smoke_contract"],
        manifest_path=paths["manifest"],
        output_dir=paths["output_dir"],
        output_path=paths["smoke_output"],
        model_asset_path=paths["asset"],
        many_point_contract_path=paths["many_point_contract"],
        gameplay_segment_contract_path=paths["gameplay_contract"],
        routing_contract_path=paths["routing_contract"],
        execution_contract_path=paths["execution_contract"],
        replay_review_contract_path=paths["review_contract"],
        probe_runner=_fake_probe_runner(),
    )

    result = build_gameplay_gated_many_point_smoke_report(
        contract_path=paths["smoke_contract"],
        smoke_report_path=paths["smoke_output"],
        output_path=paths["final_report"],
        generated_at=datetime(2026, 6, 19, 14, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    final_report = json.loads(paths["final_report"].read_text(encoding="utf-8"))
    assert final_report["report_built_at"] == "2026-06-19T14:00:00+00:00"
    assert final_report["validation_summary"]["status"] == "valid"
    assert final_report["summary"]["does_not_mutate_model_assets"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "sample_point.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "asset": asset,
        "smoke_contract": tmp_path / "gameplay_gated_many_point_smoke_contract.json",
        "manifest": tmp_path / "smoke_manifest.json",
        "manifest_validation": tmp_path / "smoke_manifest.validation.json",
        "many_point_contract": tmp_path / "many_point_contract.json",
        "gameplay_contract": tmp_path / "gameplay_contract.json",
        "routing_contract": tmp_path / "routing_contract.json",
        "execution_contract": tmp_path / "execution_contract.json",
        "review_contract": tmp_path / "review_contract.json",
        "output_dir": tmp_path / "smoke_outputs",
        "smoke_output": tmp_path / "smoke.current.json",
        "final_report": tmp_path / "smoke.report.json",
    }


def _export_contracts(paths: dict[str, Path]) -> None:
    export_gameplay_gated_many_point_smoke_contract(output_path=paths["smoke_contract"])
    export_many_point_ingestion_gate_contract(output_path=paths["many_point_contract"])
    export_gameplay_segment_gate_contract(output_path=paths["gameplay_contract"])
    export_gameplay_gated_routing_contract(output_path=paths["routing_contract"])
    export_gameplay_gated_perception_execution_contract(
        output_path=paths["execution_contract"]
    )
    export_gameplay_segment_replay_review_contract(output_path=paths["review_contract"])


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
