from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_segment_gate import (
    ALLOWED_DOWNSTREAM_GATE_STATUSES,
    ALLOWED_RAW_CLASSIFICATION_STATUSES,
    ALLOWED_SEGMENT_STATUSES,
    FORBIDDEN_GAMEPLAY_GATE_TOKENS,
    GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
    GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    GAMEPLAY_SEGMENT_REPORT_TYPE,
    GAMEPLAY_SEGMENT_REPORT_VERSION,
    build_gameplay_segment_candidates,
    build_gameplay_segment_report,
    export_gameplay_segment_gate_contract,
    inspect_gameplay_classifier_asset,
    validate_gameplay_segment_candidates,
)


def test_export_gameplay_segment_gate_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "gameplay_segment_gate_contract_v1.json"

    result = export_gameplay_segment_gate_contract(
        output_path=output_path,
        exported_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE
    assert result["contract_version"] == GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-19T00:00:00+00:00"
    assert contract["gate_scope"]["purpose"] == "gameplay_observation_suitability_gate"
    assert (
        contract["model_asset_contract"]["default_model_asset_path"]
        == "model_assets/tom_v1/view_classifier_gameplay.pt"
    )
    assert set(
        contract["gameplay_classification_schema"]["allowed_raw_statuses"]
    ) == ALLOWED_RAW_CLASSIFICATION_STATUSES
    assert set(
        contract["segment_candidate_schema"]["allowed_segment_statuses"]
    ) == ALLOWED_SEGMENT_STATUSES
    assert set(
        contract["segment_candidate_schema"]["allowed_downstream_gate_statuses"]
    ) == ALLOWED_DOWNSTREAM_GATE_STATUSES
    assert contract["warnings"]["does_not_run_downstream_perception"] is True
    assert not (FORBIDDEN_GAMEPLAY_GATE_TOKENS & _walk_exact_strings_and_keys(contract))


def test_inspect_gameplay_classifier_asset_hashes_existing_asset(tmp_path: Path) -> None:
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"tom-v1 gameplay classifier placeholder")
    output_path = tmp_path / "inspection.json"

    result = inspect_gameplay_classifier_asset(
        model_asset_path=asset,
        output_path=output_path,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["model_asset_exists"] is True
    assert result["model_asset_size_bytes"] == len(b"tom-v1 gameplay classifier placeholder")
    assert result["model_asset_sha256"]
    assert result["model_asset_ref"].startswith("tom_v1_gameplay_classifier_")
    assert output_path.is_file()


def test_build_and_validate_gameplay_segment_candidates(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    export_gameplay_segment_gate_contract(output_path=paths["contract"])

    result = build_gameplay_segment_candidates(
        local_media_path=paths["media"],
        model_asset_path=paths["asset"],
        output_path=paths["candidates"],
        media_id="media-gameplay-gate-test",
        frame_sample_rate=15,
        max_frames=8,
        generated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
        probe_runner=_fake_probe_runner(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["output_type"] == GAMEPLAY_SEGMENT_CANDIDATES_TYPE
    assert result["output_version"] == GAMEPLAY_SEGMENT_CANDIDATES_VERSION
    assert result["model_asset_exists"] is True
    assert result["model_asset_sha256"]

    candidates = json.loads(paths["candidates"].read_text(encoding="utf-8"))
    assert candidates["generated_at"] == "2026-06-19T12:00:00+00:00"
    assert candidates["media_id"] == "media-gameplay-gate-test"
    assert candidates["classifier"]["inference_mode"] == "provenance_fixture"
    assert candidates["summary"]["classification_count"] == len(candidates["classifications"])
    assert len(candidates["classifications"]) >= 3
    assert len(candidates["segment_candidates"]) >= 2
    assert any(
        item["downstream_gate_status"] == "allowed_for_downstream_observation"
        for item in candidates["segment_candidates"]
    )
    assert candidates["replay_timeline"]["lane"]["display_only"] is True

    validation = validate_gameplay_segment_candidates(
        contract_path=paths["contract"],
        candidates_path=paths["candidates"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 19, 13, 0, tzinfo=UTC),
    )

    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0
    assert validation["classification_count"] == len(candidates["classifications"])
    assert validation["segment_candidate_count"] == len(candidates["segment_candidates"])


def test_validate_gameplay_segment_candidates_rejects_forbidden_and_bad_status(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    export_gameplay_segment_gate_contract(output_path=paths["contract"])
    build_gameplay_segment_candidates(
        local_media_path=paths["media"],
        model_asset_path=paths["asset"],
        output_path=paths["candidates"],
        media_id="media-gameplay-gate-test",
        probe_runner=_fake_probe_runner(),
    )
    candidates = json.loads(paths["candidates"].read_text(encoding="utf-8"))
    candidates["classifications"][0]["raw_status"] = "true_gameplay"
    candidates["segment_candidates"][0]["winner"] = "team_a"
    paths["candidates"].write_text(json.dumps(candidates), encoding="utf-8")

    result = validate_gameplay_segment_candidates(
        contract_path=paths["contract"],
        candidates_path=paths["candidates"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_token_key",
        "forbidden_token_value",
        "invalid_raw_status",
    }


def test_build_gameplay_segment_report_uses_validation_snapshot(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    export_gameplay_segment_gate_contract(output_path=paths["contract"])
    build_gameplay_segment_candidates(
        local_media_path=paths["media"],
        model_asset_path=paths["asset"],
        output_path=paths["candidates"],
        media_id="media-gameplay-gate-test",
        probe_runner=_fake_probe_runner(),
    )

    result = build_gameplay_segment_report(
        contract_path=paths["contract"],
        candidates_path=paths["candidates"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 19, 14, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_SEGMENT_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_SEGMENT_REPORT_VERSION

    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T14:00:00+00:00"
    assert report["summary"]["validation_status"] == "valid"
    assert report["downstream_gate_summary"]["runs_downstream_jobs"] is False
    assert report["next_pipeline_contract"]["this_report_runs_downstream_jobs"] is False


def _paths(tmp_path: Path) -> dict[str, Path]:
    media = tmp_path / "sample.mp4"
    media.write_bytes(b"not a real video; probe runner supplies metadata")
    asset = tmp_path / "view_classifier_gameplay.pt"
    asset.write_bytes(b"asset bytes")
    return {
        "media": media,
        "asset": asset,
        "contract": tmp_path / "contract.json",
        "candidates": tmp_path / "candidates.json",
        "validation": tmp_path / "validation.json",
        "report": tmp_path / "report.json",
    }


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
