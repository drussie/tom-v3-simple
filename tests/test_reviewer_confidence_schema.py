from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_label_schema import (
    REVIEW_LABEL_DEFINITIONS,
    export_review_label_schema,
)
from apps.worker.services.reviewer_confidence_schema import (
    CONFIDENCE_WARNINGS,
    FORBIDDEN_CONFIDENCE_VALUES,
    METADATA_DEFINITION_WARNINGS,
    REVIEWER_CONFIDENCE_BUNDLE_TYPE,
    REVIEWER_CONFIDENCE_BUNDLE_VERSION,
    REVIEWER_CONFIDENCE_SCHEMA_TYPE,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
    build_reviewer_confidence_template,
    export_reviewer_confidence_schema,
    validate_reviewer_confidence_bundle,
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
    "correct",
    "incorrect",
}

EXPECTED_METADATA_KEYS = {
    "reviewer_confidence",
    "ambiguity_level",
    "ambiguity_reasons",
    "evidence_sufficiency",
    "reviewer_uncertainty_note",
    "requires_additional_review",
    "reviewer_time_spent_bucket",
    "review_context_complete",
}

EXPECTED_REVIEW_LABEL_KEYS = {definition["key"] for definition in REVIEW_LABEL_DEFINITIONS}


def test_export_reviewer_confidence_schema_writes_contract(tmp_path: Path) -> None:
    output_path = tmp_path / "contracts" / "reviewer_confidence_ambiguity_schema_v1.json"

    result = export_reviewer_confidence_schema(
        output_path=output_path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["schema_type"] == REVIEWER_CONFIDENCE_SCHEMA_TYPE
    assert result["schema_version"] == REVIEWER_CONFIDENCE_SCHEMA_VERSION
    assert result["metadata_definition_count"] == len(EXPECTED_METADATA_KEYS)
    assert output_path.is_file()

    schema = json.loads(output_path.read_text(encoding="utf-8"))
    assert schema["exported_at"] == "2026-06-18T12:00:00+00:00"
    assert schema["schema_type"] == REVIEWER_CONFIDENCE_SCHEMA_TYPE
    assert schema["schema_version"] == REVIEWER_CONFIDENCE_SCHEMA_VERSION
    assert {item["key"] for item in schema["metadata_definitions"]} == EXPECTED_METADATA_KEYS
    assert schema["validation_rules"]["structural_validation_only"] is True
    assert schema["validation_rules"]["does_not_infer_missing_confidence"] is True
    assert schema["validation_rules"]["does_not_create_labels"] is True
    assert schema["warnings"] == CONFIDENCE_WARNINGS

    definitions = {item["key"]: item for item in schema["metadata_definitions"]}
    assert definitions["ambiguity_reasons"]["multi_select"] is True
    for key, definition in definitions.items():
        assert definition["required"] is False
        assert definition["human_provided_only"] is True
        assert definition["machine_inferred"] is False
        assert definition["warnings"] == METADATA_DEFINITION_WARNINGS
        if key != "ambiguity_reasons":
            assert definition["multi_select"] is False

    value_sets = (
        schema["confidence_value_sets"]
        + schema["ambiguity_value_sets"]
        + schema["evidence_sufficiency_value_sets"]
        + schema["metadata_value_sets"]
    )
    for value_set in value_sets:
        assert not set(value_set["allowed_values"]) & FORBIDDEN_CONFIDENCE_VALUES
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(schema)


def test_build_reviewer_confidence_template_creates_blank_human_only_bundle(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "exports" / "reviewer_confidence_template.current.json"

    result = build_reviewer_confidence_template(
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
    assert result["confidence_bundle_type"] == REVIEWER_CONFIDENCE_BUNDLE_TYPE
    assert result["confidence_bundle_version"] == REVIEWER_CONFIDENCE_BUNDLE_VERSION
    assert result["schema_version"] == REVIEWER_CONFIDENCE_SCHEMA_VERSION
    assert result["confidence_entry_count"] == len(EXPECTED_REVIEW_LABEL_KEYS)
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
    assert {entry["label_key"] for entry in bundle["confidence_entries"]} == (
        EXPECTED_REVIEW_LABEL_KEYS
    )
    for entry in bundle["confidence_entries"]:
        assert entry["reviewer_confidence"] == "not_assessed"
        assert entry["ambiguity_level"] == "not_assessed"
        assert entry["ambiguity_reasons"] == ["not_assessed"]
        assert entry["evidence_sufficiency"] == "not_assessed"
        assert entry["reviewer_uncertainty_note"] is None
        assert entry["requires_additional_review"] == "not_assessed"
        assert entry["reviewed_at"] is None
        assert entry["human_provided_only"] is True
        assert entry["machine_inferred"] is False
        assert entry["template_entry"] is True
    assert bundle["warnings"]["template_is_not_a_completed_review"] is True
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(bundle)


def test_validate_reviewer_confidence_bundle_accepts_structural_bundle(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    review_label_schema_path = _review_label_schema_path(tmp_path)
    bundle_path = tmp_path / "confidence_bundle.json"
    bundle = _blank_confidence_bundle()
    bundle["confidence_entries"] = [
        {
            "label_key": "media_visibility_review",
            "label_entry_id": "label-entry-1",
            "reviewer_confidence": "high",
            "ambiguity_level": "minor_ambiguity",
            "ambiguity_reasons": ["occlusion", "motion_blur"],
            "evidence_sufficiency": "sufficient_for_review",
            "reviewer_uncertainty_note": "Human reviewer noted brief partial obstruction.",
            "requires_additional_review": "not_required",
            "reviewer_time_spent_bucket": "30_to_120_seconds",
            "review_context_complete": "complete",
            "reviewed_at": "2026-06-18T12:10:00+00:00",
            "human_provided_only": True,
            "machine_inferred": False,
        }
    ]
    _write_json(bundle_path, bundle)

    result = validate_reviewer_confidence_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        review_label_schema_path=review_label_schema_path,
        output_path=tmp_path / "validation.json",
        validated_at=datetime(2026, 6, 18, 12, 15, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T12:15:00+00:00"
    assert result["warnings"]["does_not_validate_correctness"] is True


def test_validate_reviewer_confidence_bundle_rejects_forbidden_and_invalid_structure(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    review_label_schema_path = _review_label_schema_path(tmp_path)
    bundle_path = tmp_path / "invalid_confidence_bundle.json"
    bundle = _blank_confidence_bundle()
    bundle["score"] = "15-0"
    bundle["confidence_entries"] = [
        {
            "label_key": "unknown_label",
            "reviewer_confidence": "low",
            "ambiguity_level": "unknown",
            "ambiguity_reasons": ["unknown"],
            "evidence_sufficiency": "unknown",
            "requires_additional_review": "unknown",
            "reviewer_time_spent_bucket": "unknown",
            "review_context_complete": "unknown",
            "human_provided_only": True,
            "machine_inferred": False,
        },
        {
            "label_key": "media_visibility_review",
            "reviewer_confidence": "correct",
            "ambiguity_level": "not_assessed",
            "ambiguity_reasons": ["server"],
            "evidence_sufficiency": "not_assessed",
            "requires_additional_review": "not_assessed",
            "reviewer_time_spent_bucket": "not_assessed",
            "review_context_complete": "not_assessed",
            "human_provided_only": False,
            "machine_inferred": True,
        },
    ]
    _write_json(bundle_path, bundle)

    result = validate_reviewer_confidence_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        review_label_schema_path=review_label_schema_path,
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "unknown_label_key" in error_types
    assert "invalid_metadata_value" in error_types
    assert "forbidden_metadata_value" in error_types
    assert "confidence_entry_must_be_human_provided_only" in error_types
    assert "confidence_entry_must_not_be_machine_inferred" in error_types
    assert result["warnings"]["no_adjudication"] is True


def test_validate_reviewer_confidence_bundle_does_not_infer_missing_confidence(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    bundle_path = tmp_path / "empty_confidence_bundle.json"
    bundle = _blank_confidence_bundle()
    bundle["confidence_entries"] = []
    _write_json(bundle_path, bundle)

    result = validate_reviewer_confidence_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        output_path=None,
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert (
        result["known_limitations"][1]
        == "Validation does not infer missing confidence or ambiguity values."
    )


def test_validate_reviewer_confidence_bundle_label_key_check_is_optional(
    tmp_path: Path,
) -> None:
    schema_path = _schema_path(tmp_path)
    bundle_path = tmp_path / "optional_label_schema_bundle.json"
    bundle = _blank_confidence_bundle()
    bundle["confidence_entries"] = [
        {
            "label_key": "future_label_key",
            "reviewer_confidence": "not_assessed",
            "ambiguity_level": "not_assessed",
            "ambiguity_reasons": ["not_assessed"],
            "evidence_sufficiency": "not_assessed",
            "requires_additional_review": "not_assessed",
            "reviewer_time_spent_bucket": "not_assessed",
            "review_context_complete": "not_assessed",
            "human_provided_only": True,
            "machine_inferred": False,
        }
    ]
    _write_json(bundle_path, bundle)

    result = validate_reviewer_confidence_bundle(
        schema_path=schema_path,
        bundle_path=bundle_path,
        review_label_schema_path=None,
        output_path=None,
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0


def _schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "contracts" / "reviewer_confidence_ambiguity_schema_v1.json"
    result = export_reviewer_confidence_schema(
        output_path=path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    assert result["ok"] is True
    return path


def _review_label_schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "contracts" / "review_label_schema_v1.json"
    result = export_review_label_schema(
        output_path=path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    assert result["ok"] is True
    return path


def _blank_confidence_bundle() -> dict[str, Any]:
    return {
        "confidence_bundle_type": REVIEWER_CONFIDENCE_BUNDLE_TYPE,
        "confidence_bundle_version": REVIEWER_CONFIDENCE_BUNDLE_VERSION,
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "review_label_schema_version": "v1",
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "associated_run_ids": {},
        "confidence_entries": [],
        "warnings": {
            "confidence_is_not_truth": True,
            "ambiguity_is_not_truth": True,
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
