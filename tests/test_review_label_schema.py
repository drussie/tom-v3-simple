from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_label_schema import (
    FORBIDDEN_REVIEW_LABEL_VALUES,
    LABEL_DEFINITION_WARNINGS,
    REVIEW_LABEL_BUNDLE_TYPE,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
    REVIEW_LABEL_WARNINGS,
    build_review_label_template,
    export_review_label_schema,
    validate_review_label_bundle,
)

FORBIDDEN_DECISION_KEYS = {
    "in_out",
    "score",
    "winner",
    "point_winner",
    "player_identity",
    "server",
    "receiver",
    "adjudication",
    "accepted",
    "rejected",
}

EXPECTED_FAMILIES = {
    "evidence_visibility_review",
    "replay_review_readiness",
    "observation_quality_review",
    "event_candidate_review_context",
    "trajectory_3d_review_context",
    "provenance_review",
    "reviewer_note_context",
}

EXPECTED_LABEL_KEYS = {
    "media_visibility_review",
    "court_visibility_review",
    "ball_visibility_review",
    "replay_readiness_review",
    "observation_quality_profile_review",
    "event_candidate_context_review",
    "trajectory_3d_context_review",
    "provenance_context_review",
    "reviewer_note_context_review",
}


def test_export_review_label_schema_writes_contract(tmp_path: Path) -> None:
    output_path = tmp_path / "contracts" / "review_label_schema_v1.json"

    result = export_review_label_schema(
        output_path=output_path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["schema_type"] == REVIEW_LABEL_SCHEMA_TYPE
    assert result["schema_version"] == REVIEW_LABEL_SCHEMA_VERSION
    assert result["label_family_count"] == len(EXPECTED_FAMILIES)
    assert result["label_definition_count"] == len(EXPECTED_LABEL_KEYS)
    assert output_path.is_file()

    schema = json.loads(output_path.read_text(encoding="utf-8"))
    assert schema["exported_at"] == "2026-06-18T12:00:00+00:00"
    assert {item["key"] for item in schema["label_families"]} == EXPECTED_FAMILIES
    assert {item["key"] for item in schema["label_definitions"]} == EXPECTED_LABEL_KEYS
    assert schema["warnings"] == REVIEW_LABEL_WARNINGS
    assert schema["validation_rules"]["structural_validation_only"] is True
    assert schema["validation_rules"]["does_not_infer_missing_labels"] is True
    assert schema["validation_rules"]["does_not_create_labels"] is True

    for definition in schema["label_definitions"]:
        assert definition["required"] is False
        assert definition["multi_select"] is False
        assert definition["human_provided_only"] is True
        assert definition["machine_inferred"] is False
        assert definition["warnings"] == LABEL_DEFINITION_WARNINGS
    for value_set in schema["value_sets"]:
        assert not set(value_set["allowed_values"]) & FORBIDDEN_REVIEW_LABEL_VALUES
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(schema)


def test_build_review_label_template_creates_blank_human_only_bundle(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "exports" / "review_label_template.current.json"

    result = build_review_label_template(
        point_manifest_id="point-manifest-1",
        media_id="media-1",
        replay_url="http://viewer.example/replay/media-1",
        associated_run_ids={
            "event_candidate_run_id": "event-run-1",
            "trajectory_3d_run_id": "trajectory-run-1",
            "camera_geometry_id": "camera-geometry-1",
        },
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 12, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["label_bundle_type"] == REVIEW_LABEL_BUNDLE_TYPE
    assert result["schema_version"] == REVIEW_LABEL_SCHEMA_VERSION
    assert result["label_entry_count"] == len(EXPECTED_LABEL_KEYS)
    assert output_path.is_file()

    bundle = json.loads(output_path.read_text(encoding="utf-8"))
    assert bundle["generated_at"] == "2026-06-18T12:05:00+00:00"
    assert bundle["point_manifest_id"] == "point-manifest-1"
    assert bundle["media_id"] == "media-1"
    assert bundle["associated_run_ids"] == {
        "camera_geometry_id": "camera-geometry-1",
        "event_candidate_run_id": "event-run-1",
        "trajectory_3d_run_id": "trajectory-run-1",
    }
    assert {entry["label_key"] for entry in bundle["label_entries"]} == EXPECTED_LABEL_KEYS
    for entry in bundle["label_entries"]:
        assert entry["value"] == "not_assessed"
        assert entry["reviewer_note"] is None
        assert entry["evidence_reference"] is None
        assert entry["reviewed_at"] is None
        assert entry["human_provided_only"] is True
        assert entry["machine_inferred"] is False
        assert entry["template_entry"] is True
    assert bundle["warnings"]["template_is_not_a_completed_review"] is True
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(bundle)


def test_validate_review_label_bundle_accepts_structural_bundle(tmp_path: Path) -> None:
    schema_path = _schema_path(tmp_path)
    bundle_path = tmp_path / "bundle.json"
    bundle = _blank_bundle()
    bundle["label_entries"] = [
        {
            "label_key": "media_visibility_review",
            "value": "visible",
            "reviewer_note": "Human reviewer saw usable media.",
            "evidence_reference": {"source": "replay"},
            "reviewed_at": "2026-06-18T12:10:00+00:00",
            "human_provided_only": True,
            "machine_inferred": False,
        }
    ]
    _write_json(bundle_path, bundle)

    result = validate_review_label_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        output_path=tmp_path / "validation.json",
        validated_at=datetime(2026, 6, 18, 12, 15, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T12:15:00+00:00"
    assert result["warnings"]["does_not_validate_correctness"] is True


def test_validate_review_label_bundle_rejects_forbidden_and_invalid_structure(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    bundle_path = tmp_path / "invalid_bundle.json"
    bundle = _blank_bundle()
    bundle["score"] = "15-0"
    bundle["label_entries"] = [
        {
            "label_key": "unknown_label",
            "value": "not_assessed",
            "human_provided_only": True,
            "machine_inferred": False,
        },
        {
            "label_key": "media_visibility_review",
            "value": "correct",
            "human_provided_only": False,
            "machine_inferred": True,
        },
    ]
    _write_json(bundle_path, bundle)

    result = validate_review_label_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "unknown_label_key" in error_types
    assert "invalid_label_value" in error_types
    assert "forbidden_label_value" in error_types
    assert "label_entry_must_be_human_provided_only" in error_types
    assert "label_entry_must_not_be_machine_inferred" in error_types
    assert result["warnings"]["no_adjudication"] is True


def test_validate_review_label_bundle_does_not_infer_missing_labels(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    bundle_path = tmp_path / "empty_bundle.json"
    bundle = _blank_bundle()
    bundle["label_entries"] = []
    _write_json(bundle_path, bundle)

    result = validate_review_label_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        output_path=None,
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert (
        result["known_limitations"][1]
        == "Validation does not infer missing labels or create labels."
    )


def _schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "contracts" / "review_label_schema_v1.json"
    result = export_review_label_schema(
        output_path=path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    assert result["ok"] is True
    return path


def _blank_bundle() -> dict[str, Any]:
    return {
        "label_bundle_type": "structured_review_label_bundle",
        "label_bundle_version": "v1",
        "schema_type": "structured_review_label_schema",
        "schema_version": "v1",
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "associated_run_ids": {},
        "label_entries": [],
        "warnings": {
            "label_is_not_truth": True,
            "human_review_only": True,
            "no_adjudication": True,
        },
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_walk_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_walk_keys(item))
        return keys
    return set()
