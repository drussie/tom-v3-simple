from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.intennse_label_alignment import (
    ALIGNMENT_ENTITIES,
    ALIGNMENT_STATUS_VALUES,
    ALIGNMENT_WARNINGS,
    FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS,
    INTENNSE_ALIGNMENT_BUNDLE_TYPE,
    INTENNSE_ALIGNMENT_BUNDLE_VERSION,
    INTENNSE_ALIGNMENT_CONTRACT_TYPE,
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
    INTENNSE_ALIGNMENT_REPORT_TYPE,
    INTENNSE_ALIGNMENT_REPORT_VERSION,
    PROVENANCE_STATUS_VALUES,
    build_intennse_alignment_report,
    build_intennse_alignment_template,
    export_intennse_label_alignment_contract,
    validate_intennse_alignment_bundle,
)
from apps.worker.services.multi_reviewer_disagreement import (
    export_multi_reviewer_disagreement_schema,
)
from apps.worker.services.observation_quality_taxonomy import (
    export_observation_quality_taxonomy,
)
from apps.worker.services.review_label_schema import export_review_label_schema
from apps.worker.services.reviewer_confidence_schema import (
    export_reviewer_confidence_schema,
)

EXPECTED_ENTITIES = {entity["key"] for entity in ALIGNMENT_ENTITIES}


def test_export_intennse_label_alignment_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "intennse_label_alignment_contract_v1.json"

    result = export_intennse_label_alignment_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == INTENNSE_ALIGNMENT_CONTRACT_TYPE
    assert result["contract_version"] == INTENNSE_ALIGNMENT_CONTRACT_VERSION
    assert result["alignment_bundle_type"] == INTENNSE_ALIGNMENT_BUNDLE_TYPE
    assert result["alignment_bundle_version"] == INTENNSE_ALIGNMENT_BUNDLE_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["tom_schema_refs"] == {
        "observation_quality_taxonomy_version": "v1",
        "review_label_schema_version": "v1",
        "reviewer_confidence_schema_version": "v1",
        "multi_reviewer_disagreement_schema_version": "v1",
    }
    assert {item["key"] for item in contract["alignment_entities"]} == EXPECTED_ENTITIES
    assert set(
        _value_set(contract, "alignment_status_values")["allowed_values"]
    ) == set(ALIGNMENT_STATUS_VALUES)
    assert set(
        _value_set(contract, "provenance_status_values")["allowed_values"]
    ) == set(PROVENANCE_STATUS_VALUES)
    assert contract["validation_rules"]["structural_validation_only"] is True
    assert contract["validation_rules"]["does_not_resolve_disagreement"] is True
    assert contract["validation_rules"]["does_not_create_intennse_labels"] is True
    assert contract["warnings"] == ALIGNMENT_WARNINGS
    assert not FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS & _walk_keys(contract)


def test_build_intennse_alignment_template_preserves_references_and_is_blank(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "exports" / "intennse_alignment_template.current.json"

    result = build_intennse_alignment_template(
        point_manifest_id="point-manifest-1",
        media_id="media-1",
        replay_url="http://viewer.example/replay/media-1",
        associated_run_ids={
            "event_candidate_run_id": "event-run-1",
            "trajectory_3d_run_id": "trajectory-run-1",
            "camera_geometry_id": "camera-geometry-1",
        },
        tom_review_label_bundle_ref="tom://review-label-bundle/1",
        tom_reviewer_confidence_bundle_ref="tom://confidence-bundle/1",
        tom_multi_reviewer_review_set_ref="tom://multi-reviewer-review-set/1",
        tom_disagreement_report_ref="tom://disagreement-report/1",
        intennse_label_bundle_ref="intennse://label-bundle/1",
        intennse_schema_version="intennse-placeholder-v1",
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 13, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["alignment_entry_count"] == len(EXPECTED_ENTITIES)
    assert output_path.is_file()

    bundle = json.loads(output_path.read_text(encoding="utf-8"))
    assert bundle["generated_at"] == "2026-06-18T13:00:00+00:00"
    assert bundle["alignment_bundle_type"] == INTENNSE_ALIGNMENT_BUNDLE_TYPE
    assert bundle["intennse_label_bundle_ref"] == "intennse://label-bundle/1"
    assert bundle["associated_run_ids"]["camera_geometry_id"] == "camera-geometry-1"
    assert {entry["alignment_entity"] for entry in bundle["alignment_entries"]} == (
        EXPECTED_ENTITIES
    )
    for entry in bundle["alignment_entries"]:
        assert entry["alignment_status"] == "not_assessed"
        assert entry["provenance_status"] == "not_assessed"
        assert entry["requires_human_alignment_review"] == "not_assessed"
        assert entry["human_provided_only"] is True
        assert entry["machine_inferred"] is False
        assert entry["warnings"]["does_not_create_intennse_labels"] is True
    assert not FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS & _walk_keys(bundle)


def test_validate_intennse_alignment_bundle_allows_missing_refs_as_warnings(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    bundle_path = tmp_path / "alignment_bundle.json"
    build_intennse_alignment_template(
        point_manifest_id="point-manifest-1",
        media_id="media-1",
        replay_url="http://viewer.example/replay/media-1",
        output_path=bundle_path,
        generated_at=datetime(2026, 6, 18, 13, 0, tzinfo=UTC),
    )

    result = validate_intennse_alignment_bundle(
        contract_path=paths["intennse_contract"],
        bundle_path=bundle_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        output_path=tmp_path / "validation.json",
        validated_at=datetime(2026, 6, 18, 13, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["structural_warning_count"] == len(EXPECTED_ENTITIES)
    assert {item["warning_type"] for item in result["structural_warnings"]} == {
        "missing_intennse_reference"
    }
    assert len(result["tom_contract_validations"]) == 4
    assert all(item["ok"] is True for item in result["tom_contract_validations"])
    assert result["known_limitations"][3] == "Validation does not create INTENNSE labels."


def test_validate_intennse_alignment_bundle_rejects_forbidden_fields_and_values(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    bundle_path = tmp_path / "invalid_alignment_bundle.json"
    build_intennse_alignment_template(output_path=bundle_path)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle["score"] = "15-0"
    bundle["alignment_entries"][0]["alignment_status"] = "adjudicated"
    bundle["alignment_entries"][0]["human_provided_only"] = False
    bundle["alignment_entries"][0]["machine_inferred"] = True
    bundle["alignment_entries"][0]["tom_reference"]["winner"] = "player_a"
    _write_json(bundle_path, bundle)

    result = validate_intennse_alignment_bundle(
        contract_path=paths["intennse_contract"],
        bundle_path=bundle_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "invalid_alignment_status" in error_types
    assert "alignment_entry_must_be_human_provided_only" in error_types
    assert "alignment_entry_must_not_be_machine_inferred" in error_types
    assert result["warnings"]["does_not_resolve_disagreement"] is True


def test_build_intennse_alignment_report_summarizes_provenance_only(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    bundle_path = tmp_path / "alignment_bundle.json"
    build_intennse_alignment_template(
        point_manifest_id="point-manifest-1",
        media_id="media-1",
        replay_url="http://viewer.example/replay/media-1",
        intennse_label_bundle_ref="intennse://label-bundle/1",
        intennse_schema_version="intennse-placeholder-v1",
        output_path=bundle_path,
    )
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle["alignment_entries"][0]["alignment_status"] = "aligned_by_reference"
    bundle["alignment_entries"][0]["provenance_status"] = "provenance_present"
    bundle["alignment_entries"][0]["requires_human_alignment_review"] = "not_required"
    bundle["alignment_entries"][1]["tom_reference"] = {
        "reference_type": "replay_context_alignment"
    }
    bundle["alignment_entries"][1]["provenance_status"] = "provenance_partial"
    bundle["alignment_entries"][1]["requires_human_alignment_review"] = "required"
    _write_json(bundle_path, bundle)

    result = build_intennse_alignment_report(
        contract_path=paths["intennse_contract"],
        bundle_path=bundle_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        output_path=tmp_path / "alignment_report.json",
        generated_at=datetime(2026, 6, 18, 13, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["alignment_report_type"] == INTENNSE_ALIGNMENT_REPORT_TYPE
    assert result["alignment_report_version"] == INTENNSE_ALIGNMENT_REPORT_VERSION
    assert result["summary"]["alignment_entry_count"] == len(EXPECTED_ENTITIES)
    assert result["summary"]["alignment_reference_present_count"] == len(EXPECTED_ENTITIES) - 1
    assert result["summary"]["missing_tom_reference_count"] == 1
    assert result["summary"]["provenance_partial_count"] == 1
    assert result["summary"]["requires_human_alignment_review_count"] == 1
    assert result["report"]["warnings"]["intennse_references_are_external_placeholders"] is True
    assert {item["issue_type"] for item in result["report"]["provenance_issues"]} == {
        "missing_tom_reference",
        "provenance_partial",
    }


def _contract_paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "intennse_contract": tmp_path
        / "contracts"
        / "intennse_label_alignment_contract_v1.json",
        "observation_quality_taxonomy": tmp_path
        / "contracts"
        / "observation_quality_taxonomy_v1.json",
        "review_label_schema": tmp_path / "contracts" / "review_label_schema_v1.json",
        "reviewer_confidence_schema": tmp_path
        / "contracts"
        / "reviewer_confidence_ambiguity_schema_v1.json",
        "multi_reviewer_schema": tmp_path
        / "contracts"
        / "multi_reviewer_disagreement_schema_v1.json",
    }
    export_intennse_label_alignment_contract(
        output_path=paths["intennse_contract"],
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    export_observation_quality_taxonomy(
        output_path=paths["observation_quality_taxonomy"],
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    export_review_label_schema(
        output_path=paths["review_label_schema"],
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    export_reviewer_confidence_schema(
        output_path=paths["reviewer_confidence_schema"],
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    export_multi_reviewer_disagreement_schema(
        output_path=paths["multi_reviewer_schema"],
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    return paths


def _value_set(contract: dict[str, Any], key: str) -> dict[str, Any]:
    return next(
        item
        for item in contract["alignment_value_sets"]
        if item["key"] == key
    )


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(key)
            keys.update(_walk_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_walk_keys(item))
    return keys
