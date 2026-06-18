from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_reviewer_disagreement import (
    DISAGREEMENT_REPORT_TYPE,
    DISAGREEMENT_REPORT_VERSION,
    MULTI_REVIEWER_REVIEW_SET_TYPE,
    MULTI_REVIEWER_REVIEW_SET_VERSION,
    MULTI_REVIEWER_SCHEMA_TYPE,
    MULTI_REVIEWER_SCHEMA_VERSION,
    MULTI_REVIEWER_WARNINGS,
    build_multi_reviewer_review_set_template,
    build_reviewer_disagreement_report,
    export_multi_reviewer_disagreement_schema,
    validate_multi_reviewer_review_set,
)
from apps.worker.services.review_label_schema import (
    REVIEW_LABEL_BUNDLE_TYPE,
    REVIEW_LABEL_BUNDLE_VERSION,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
    export_review_label_schema,
)
from apps.worker.services.reviewer_confidence_schema import (
    REVIEWER_CONFIDENCE_BUNDLE_TYPE,
    REVIEWER_CONFIDENCE_BUNDLE_VERSION,
    REVIEWER_CONFIDENCE_SCHEMA_TYPE,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
    export_reviewer_confidence_schema,
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
    "truth",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_reliability",
}

EXPECTED_DIMENSIONS = {
    "label_value_disagreement",
    "confidence_disagreement",
    "ambiguity_disagreement",
    "evidence_sufficiency_disagreement",
    "missing_review_bundle",
    "missing_confidence_bundle",
    "reviewer_note_difference",
    "provenance_mismatch",
    "not_assessed_difference",
}


def test_export_multi_reviewer_disagreement_schema_writes_contract(tmp_path: Path) -> None:
    output_path = tmp_path / "contracts" / "multi_reviewer_disagreement_schema_v1.json"

    result = export_multi_reviewer_disagreement_schema(
        output_path=output_path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["schema_type"] == MULTI_REVIEWER_SCHEMA_TYPE
    assert result["schema_version"] == MULTI_REVIEWER_SCHEMA_VERSION
    assert result["review_set_type"] == MULTI_REVIEWER_REVIEW_SET_TYPE
    assert result["review_set_version"] == MULTI_REVIEWER_REVIEW_SET_VERSION
    assert result["disagreement_dimension_count"] == len(EXPECTED_DIMENSIONS)
    assert output_path.is_file()

    schema = json.loads(output_path.read_text(encoding="utf-8"))
    assert schema["exported_at"] == "2026-06-18T12:00:00+00:00"
    assert {item["key"] for item in schema["disagreement_dimensions"]} == EXPECTED_DIMENSIONS
    assert schema["reviewer_identity_policy"]["pseudonymous_identifiers_only"] is True
    assert schema["reviewer_identity_policy"]["real_name_required"] is False
    assert schema["reviewer_identity_policy"]["email_required"] is False
    assert schema["reviewer_identity_policy"]["reviewer_ranking_allowed"] is False
    assert schema["validation_rules"]["structural_validation_only"] is True
    assert schema["validation_rules"]["does_not_resolve_disagreements"] is True
    assert schema["validation_rules"]["does_not_score_reviewers"] is True
    assert schema["warnings"] == MULTI_REVIEWER_WARNINGS
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(schema)


def test_build_multi_reviewer_review_set_template_is_blank_and_human_only(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "exports" / "multi_reviewer_review_set_template.current.json"

    result = build_multi_reviewer_review_set_template(
        point_manifest_id="point-manifest-1",
        media_id="media-1",
        replay_url="http://viewer.example/replay/media-1",
        associated_run_ids={
            "event_candidate_run_id": "event-run-1",
            "trajectory_3d_run_id": "trajectory-run-1",
            "camera_geometry_id": "camera-geometry-1",
        },
        reviewer_count=2,
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 12, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["review_set_type"] == MULTI_REVIEWER_REVIEW_SET_TYPE
    assert result["reviewer_count"] == 2
    assert output_path.is_file()

    review_set = json.loads(output_path.read_text(encoding="utf-8"))
    assert review_set["generated_at"] == "2026-06-18T12:05:00+00:00"
    assert {entry["reviewer_id"] for entry in review_set["reviewer_entries"]} == {
        "reviewer_1",
        "reviewer_2",
    }
    for entry in review_set["reviewer_entries"]:
        assert entry["review_label_bundle_path"] is None
        assert entry["reviewer_confidence_bundle_path"] is None
        assert entry["human_provided_only"] is True
        assert entry["machine_inferred"] is False
        assert entry["warnings"]["does_not_rank_reviewers"] is True
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(review_set)


def test_validate_multi_reviewer_review_set_allows_missing_bundle_refs_as_warnings(
    tmp_path: Path,
) -> None:
    schema_path = _multi_reviewer_schema_path(tmp_path)
    review_set_path = tmp_path / "review_set.json"
    build_multi_reviewer_review_set_template(
        output_path=review_set_path,
        generated_at=datetime(2026, 6, 18, 12, 5, tzinfo=UTC),
    )

    result = validate_multi_reviewer_review_set(
        schema_path=schema_path,
        review_set_path=review_set_path,
        review_label_schema_path=_review_label_schema_path(tmp_path),
        reviewer_confidence_schema_path=_confidence_schema_path(tmp_path),
        output_path=tmp_path / "validation.json",
        validated_at=datetime(2026, 6, 18, 12, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["structural_warning_count"] == 4
    assert {item["warning_type"] for item in result["structural_warnings"]} == {
        "missing_review_bundle",
        "missing_confidence_bundle",
    }
    assert result["known_limitations"][3] == "Validation does not say which reviewer is correct."


def test_validate_multi_reviewer_review_set_validates_referenced_bundles(
    tmp_path: Path,
) -> None:
    paths = _schema_paths(tmp_path)
    review_set_path = _review_set_with_bundles(tmp_path, paths)

    result = validate_multi_reviewer_review_set(
        schema_path=paths["multi_reviewer_schema"],
        review_set_path=review_set_path,
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["confidence_schema"],
        output_path=None,
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["structural_warning_count"] == 0
    assert len(result["nested_validations"]) == 4
    assert all(item["ok"] is True for item in result["nested_validations"])


def test_validate_multi_reviewer_review_set_rejects_forbidden_and_invalid_structure(
    tmp_path: Path,
) -> None:
    schema_path = _multi_reviewer_schema_path(tmp_path)
    review_set_path = tmp_path / "invalid_review_set.json"
    review_set = _blank_review_set()
    review_set["score"] = "15-0"
    review_set["reviewer_entries"] = [
        {
            "reviewer_id": "reviewer_1",
            "reviewer_email": "reviewer@example.invalid",
            "human_provided_only": True,
            "machine_inferred": False,
        },
        {
            "reviewer_id": "reviewer_1",
            "human_provided_only": False,
            "machine_inferred": True,
            "reviewer_score": 100,
        },
    ]
    _write_json(review_set_path, review_set)

    result = validate_multi_reviewer_review_set(
        schema_path=schema_path,
        review_set_path=review_set_path,
        review_label_schema_path=_review_label_schema_path(tmp_path),
        reviewer_confidence_schema_path=_confidence_schema_path(tmp_path),
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "disallowed_reviewer_identity_field" in error_types
    assert "duplicate_reviewer_id" in error_types
    assert "reviewer_entry_must_be_human_provided_only" in error_types
    assert "reviewer_entry_must_not_be_machine_inferred" in error_types
    assert result["warnings"]["does_not_resolve_disagreement"] is True


def test_build_reviewer_disagreement_report_detects_structural_disagreement(
    tmp_path: Path,
) -> None:
    paths = _schema_paths(tmp_path)
    review_set_path = _review_set_with_bundles(tmp_path, paths)

    result = build_reviewer_disagreement_report(
        schema_path=paths["multi_reviewer_schema"],
        review_set_path=review_set_path,
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["confidence_schema"],
        output_path=tmp_path / "disagreement_report.json",
        generated_at=datetime(2026, 6, 18, 12, 20, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["disagreement_report_type"] == DISAGREEMENT_REPORT_TYPE
    assert result["disagreement_report_version"] == DISAGREEMENT_REPORT_VERSION
    assert result["summary"]["reviewer_count"] == 2
    assert result["summary"]["disagreement_observed_count"] >= 1

    report = result["report"]
    group = next(
        item
        for item in report["comparison_groups"]
        if item["label_key"] == "media_visibility_review"
    )
    dimensions = {item["dimension"] for item in group["disagreement_dimensions"]}
    assert {
        "label_value_disagreement",
        "confidence_disagreement",
        "ambiguity_disagreement",
        "evidence_sufficiency_disagreement",
    } <= dimensions
    assert group["disagreement_observed"] is True
    assert group["requires_additional_review"] is True
    assert "conflicting_human_inputs" in group["report_notes"]
    assert "needs_additional_review" in group["report_notes"]
    assert {item["value"] for item in group["reviewer_values"]} == {
        "visible",
        "obscured",
    }
    assert report["warnings"]["conflicting_human_inputs_are_not_resolved"] is True


def _schema_paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "multi_reviewer_schema": _multi_reviewer_schema_path(tmp_path),
        "review_label_schema": _review_label_schema_path(tmp_path),
        "confidence_schema": _confidence_schema_path(tmp_path),
    }


def _multi_reviewer_schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "contracts" / "multi_reviewer_disagreement_schema_v1.json"
    result = export_multi_reviewer_disagreement_schema(
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


def _confidence_schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "contracts" / "reviewer_confidence_ambiguity_schema_v1.json"
    result = export_reviewer_confidence_schema(
        output_path=path,
        exported_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )
    assert result["ok"] is True
    return path


def _review_set_with_bundles(tmp_path: Path, paths: dict[str, Path]) -> Path:
    del paths
    reviewer_1_label = tmp_path / "reviewer_1_label_bundle.json"
    reviewer_2_label = tmp_path / "reviewer_2_label_bundle.json"
    reviewer_1_confidence = tmp_path / "reviewer_1_confidence_bundle.json"
    reviewer_2_confidence = tmp_path / "reviewer_2_confidence_bundle.json"
    _write_json(
        reviewer_1_label,
        _review_label_bundle(value="visible", note="Reviewer one saw visible media."),
    )
    _write_json(
        reviewer_2_label,
        _review_label_bundle(value="obscured", note="Reviewer two saw obstruction."),
    )
    _write_json(
        reviewer_1_confidence,
        _confidence_bundle(
            confidence="high",
            ambiguity="none_observed",
            sufficiency="sufficient_for_review",
        ),
    )
    _write_json(
        reviewer_2_confidence,
        _confidence_bundle(
            confidence="low",
            ambiguity="high_ambiguity",
            sufficiency="insufficient_for_review",
        ),
    )
    review_set = _blank_review_set()
    review_set["reviewer_entries"] = [
        _reviewer_entry(
            reviewer_id="reviewer_1",
            label_path=reviewer_1_label,
            confidence_path=reviewer_1_confidence,
        ),
        _reviewer_entry(
            reviewer_id="reviewer_2",
            label_path=reviewer_2_label,
            confidence_path=reviewer_2_confidence,
        ),
    ]
    review_set_path = tmp_path / "review_set_with_bundles.json"
    _write_json(review_set_path, review_set)
    return review_set_path


def _blank_review_set() -> dict[str, Any]:
    return {
        "review_set_type": MULTI_REVIEWER_REVIEW_SET_TYPE,
        "review_set_version": MULTI_REVIEWER_REVIEW_SET_VERSION,
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "associated_run_ids": {},
        "reviewer_entries": [],
        "warnings": {
            "review_set_is_not_truth": True,
            "disagreement_is_not_truth": True,
            "human_review_only": True,
            "no_adjudication": True,
        },
    }


def _reviewer_entry(
    *,
    reviewer_id: str,
    label_path: Path,
    confidence_path: Path,
) -> dict[str, Any]:
    return {
        "reviewer_id": reviewer_id,
        "reviewer_role": None,
        "reviewer_session_id": None,
        "reviewer_notes": None,
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "review_label_bundle_path": str(label_path),
        "review_label_bundle_ref": None,
        "reviewer_confidence_bundle_path": str(confidence_path),
        "reviewer_confidence_bundle_ref": None,
        "associated_run_ids": {},
        "submitted_at": "2026-06-18T12:12:00+00:00",
        "human_provided_only": True,
        "machine_inferred": False,
        "warnings": {
            "human_review_only": True,
            "does_not_score_reviewers": True,
            "does_not_resolve_disagreement": True,
        },
    }


def _review_label_bundle(*, value: str, note: str) -> dict[str, Any]:
    return {
        "label_bundle_type": REVIEW_LABEL_BUNDLE_TYPE,
        "label_bundle_version": REVIEW_LABEL_BUNDLE_VERSION,
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "associated_run_ids": {},
        "label_entries": [
            {
                "label_key": "media_visibility_review",
                "value": value,
                "reviewer_note": note,
                "evidence_reference": {"source": "replay"},
                "reviewed_at": "2026-06-18T12:10:00+00:00",
                "human_provided_only": True,
                "machine_inferred": False,
            }
        ],
        "warnings": {
            "label_is_not_truth": True,
            "human_review_only": True,
            "no_adjudication": True,
        },
    }


def _confidence_bundle(
    *,
    confidence: str,
    ambiguity: str,
    sufficiency: str,
) -> dict[str, Any]:
    return {
        "confidence_bundle_type": REVIEWER_CONFIDENCE_BUNDLE_TYPE,
        "confidence_bundle_version": REVIEWER_CONFIDENCE_BUNDLE_VERSION,
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "point_manifest_id": "point-manifest-1",
        "media_id": "media-1",
        "replay_url": "http://viewer.example/replay/media-1",
        "associated_run_ids": {},
        "confidence_entries": [
            {
                "label_key": "media_visibility_review",
                "label_entry_id": None,
                "reviewer_confidence": confidence,
                "ambiguity_level": ambiguity,
                "ambiguity_reasons": ["reviewer_uncertain"],
                "evidence_sufficiency": sufficiency,
                "reviewer_uncertainty_note": None,
                "requires_additional_review": "not_assessed",
                "reviewer_time_spent_bucket": "unknown",
                "review_context_complete": "complete",
                "reviewed_at": "2026-06-18T12:11:00+00:00",
                "human_provided_only": True,
                "machine_inferred": False,
            }
        ],
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
