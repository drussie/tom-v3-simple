from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.many_point_ingestion_gate import (
    DISALLOWED_REQUESTED_ACTION_VALUES,
    EXECUTION_MODE_VALUES,
    FORBIDDEN_MANY_POINT_INGESTION_FIELDS,
    MANY_POINT_INGESTION_CONTRACT_TYPE,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
    MANY_POINT_INGESTION_GATE_TYPE,
    MANY_POINT_INGESTION_GATE_VERSION,
    MANY_POINT_INGESTION_MANIFEST_TYPE,
    MANY_POINT_INGESTION_MANIFEST_VERSION,
    MANY_POINT_INGESTION_PLAN_TYPE,
    MANY_POINT_INGESTION_PLAN_VERSION,
    MANY_POINT_INGESTION_WARNINGS,
    REQUESTED_ACTION_VALUES,
    build_many_point_ingestion_manifest_template,
    build_many_point_ingestion_plan,
    export_many_point_ingestion_gate_contract,
    run_many_point_ingestion_gate,
    validate_many_point_ingestion_manifest,
)


def test_export_many_point_ingestion_gate_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "many_point_ingestion_gate_contract_v1.json"

    result = export_many_point_ingestion_gate_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == MANY_POINT_INGESTION_CONTRACT_TYPE
    assert result["contract_version"] == MANY_POINT_INGESTION_CONTRACT_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["contract_type"] == MANY_POINT_INGESTION_CONTRACT_TYPE
    assert contract["contract_version"] == MANY_POINT_INGESTION_CONTRACT_VERSION
    assert contract["manifest_type"] == MANY_POINT_INGESTION_MANIFEST_TYPE
    assert contract["manifest_version"] == MANY_POINT_INGESTION_MANIFEST_VERSION
    assert contract["ingestion_scope"]["default_execution_mode"] == "dry_run"
    assert contract["ingestion_scope"]["silent_ingestion_allowed"] is False
    assert contract["ingestion_scope"]["event_generation_allowed"] is False
    assert set(contract["requested_action_values"]) == set(REQUESTED_ACTION_VALUES)
    assert set(contract["disallowed_requested_action_values"]) == set(
        DISALLOWED_REQUESTED_ACTION_VALUES
    )
    assert {item["mode"] for item in contract["execution_modes"]} == set(
        EXECUTION_MODE_VALUES
    )
    assert contract["source_contract_refs"] == {
        "observation_quality_taxonomy_version": "v1",
        "review_label_schema_version": "v1",
        "reviewer_confidence_schema_version": "v1",
        "multi_reviewer_disagreement_schema_version": "v1",
        "intennse_label_alignment_contract_version": "v1",
        "versioned_dataset_corpus_contract_version": "v1",
        "coverage_sampling_strategy_contract_version": "v1",
        "multi_point_regression_matrix_version": "v0",
        "point_manifest_version": "v0",
    }
    assert contract["warnings"] == MANY_POINT_INGESTION_WARNINGS
    assert not FORBIDDEN_MANY_POINT_INGESTION_FIELDS & _walk_keys(contract)


def test_many_point_ingestion_template_and_validation_use_explicit_paths(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    media_path = _media_file(tmp_path, "point-a.mp4", b"point-a")

    template_result = build_many_point_ingestion_manifest_template(
        local_media_paths=[media_path],
        source_label="demo_point",
        output_path=paths["manifest"],
        generated_at=datetime(2026, 6, 18, 16, 0, tzinfo=UTC),
    )
    validation_result = validate_many_point_ingestion_manifest(
        contract_path=paths["contract"],
        manifest_path=paths["manifest"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 18, 16, 5, tzinfo=UTC),
    )

    assert template_result["ok"] is True
    assert template_result["entry_count"] == 1
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["generated_at"] == "2026-06-18T16:00:00+00:00"
    assert manifest["entries"][0]["local_media_path"] == str(media_path)
    assert set(manifest["entries"][0]["requested_actions"]) == set(
        REQUESTED_ACTION_VALUES
    )

    assert validation_result["ok"] is True
    assert validation_result["status"] == "valid"
    assert validation_result["error_count"] == 0
    assert validation_result["entry_count"] == 1
    assert validation_result["validated_at"] == "2026-06-18T16:05:00+00:00"
    assert paths["validation"].is_file()


def test_many_point_ingestion_validation_rejects_unsafe_manifest_fields(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    media_path = _media_file(tmp_path, "point-a.mp4", b"point-a")
    manifest = _manifest(media_path)
    manifest["entries"][0]["requested_actions"].append("generate_event_candidates")
    manifest["entries"][0]["score"] = "15-0"
    _write_json(paths["manifest"], manifest)

    result = validate_many_point_ingestion_manifest(
        contract_path=paths["contract"],
        manifest_path=paths["manifest"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "unsupported_requested_action" in error_types
    assert "forbidden_field" in error_types
    assert result["warnings"]["does_not_create_event_candidates"] is True
    assert result["warnings"]["no_adjudication"] is True


def test_many_point_ingestion_validation_rejects_duplicate_media(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    media_path = _media_file(tmp_path, "point-a.mp4", b"point-a")
    manifest = _manifest(media_path)
    duplicate = dict(manifest["entries"][0])
    duplicate["ingestion_entry_id"] = "many_point_ingestion_entry_v1_duplicate"
    manifest["entries"].append(duplicate)
    manifest["entry_count"] = 2
    _write_json(paths["manifest"], manifest)

    result = validate_many_point_ingestion_manifest(
        contract_path=paths["contract"],
        manifest_path=paths["manifest"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} == {
        "duplicate_media_detected"
    }


def test_build_many_point_ingestion_plan_is_dry_run_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    media_path = _media_file(tmp_path, "point-a.mp4", b"point-a")
    _write_json(paths["manifest"], _manifest(media_path))

    result = build_many_point_ingestion_plan(
        contract_path=paths["contract"],
        manifest_path=paths["manifest"],
        output_path=paths["plan"],
        generated_at=datetime(2026, 6, 18, 16, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["plan_type"] == MANY_POINT_INGESTION_PLAN_TYPE
    assert result["plan_version"] == MANY_POINT_INGESTION_PLAN_VERSION
    assert result["mode"] == "dry_run"
    assert result["summary"]["entry_count"] == 1
    assert result["summary"]["indexed_entry_count"] == 0

    plan = json.loads(paths["plan"].read_text(encoding="utf-8"))
    entry = plan["entries"][0]
    assert entry["path_exists"] is True
    assert entry["checksum"] is not None
    assert entry["status"] == "would_index"
    assert entry["media_id"] is None
    assert plan["warnings"]["writes_enabled"] is False


def test_run_many_point_ingestion_gate_dry_run_does_not_index(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    media_path = _media_file(tmp_path, "point-a.mp4", b"point-a")
    _write_json(paths["manifest"], _manifest(media_path))

    result = run_many_point_ingestion_gate(
        contract_path=paths["contract"],
        manifest_path=paths["manifest"],
        mode="dry_run",
        output_path=paths["gate_report"],
        generated_at=datetime(2026, 6, 18, 16, 15, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["ingestion_gate_type"] == MANY_POINT_INGESTION_GATE_TYPE
    assert result["ingestion_gate_version"] == MANY_POINT_INGESTION_GATE_VERSION
    assert result["mode"] == "dry_run"
    assert result["validated_entry_count"] == 1
    assert result["indexed_entry_count"] == 0
    assert result["failed_entry_count"] == 0

    report = json.loads(paths["gate_report"].read_text(encoding="utf-8"))
    entry = report["entries"][0]
    assert entry["status"] == "dry_run_planned"
    assert entry["media_id"] is None
    assert entry["replay_url"] is None
    assert report["warnings"]["writes_media_or_manifest_state"] is False
    assert report["warnings"]["does_not_claim_generalization"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "contract": tmp_path / "contracts" / "many_point_ingestion_gate_contract_v1.json",
        "manifest": tmp_path / "exports" / "many_point_ingestion_manifest.template.json",
        "validation": tmp_path
        / "exports"
        / "many_point_ingestion_manifest.validation.json",
        "plan": tmp_path / "exports" / "many_point_ingestion_plan.current.json",
        "gate_report": tmp_path / "exports" / "many_point_ingestion_gate.current.json",
    }
    export_many_point_ingestion_gate_contract(output_path=paths["contract"])
    return paths


def _manifest(media_path: Path) -> dict[str, Any]:
    result = build_many_point_ingestion_manifest_template(
        local_media_paths=[media_path],
        output_path=None,
        generated_at=datetime(2026, 6, 18, 16, 0, tzinfo=UTC),
    )
    return result["manifest"]


def _media_file(tmp_path: Path, name: str, content: bytes) -> Path:
    path = tmp_path / "media" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_walk_keys(item))
    return keys
