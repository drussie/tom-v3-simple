from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_CONTRACT_TYPE,
    COVERAGE_SAMPLING_CONTRACT_VERSION,
    DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
)
from apps.worker.services.intennse_label_alignment import (
    DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    INTENNSE_ALIGNMENT_CONTRACT_TYPE,
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.label_feedback_evaluation import (
    DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
    LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
    LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
    LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
    LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
)
from apps.worker.services.many_point_ingestion_gate import (
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    MANY_POINT_INGESTION_CONTRACT_TYPE,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)
from apps.worker.services.multi_point_regression_matrix import (
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)
from apps.worker.services.multi_reviewer_disagreement import (
    DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    MULTI_REVIEWER_SCHEMA_TYPE,
    MULTI_REVIEWER_SCHEMA_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
    OBSERVATION_QUALITY_TAXONOMY_TYPE,
    OBSERVATION_QUALITY_TAXONOMY_VERSION,
)
from apps.worker.services.point_manifest import POINT_MANIFEST_VERSION
from apps.worker.services.review_label_schema import (
    DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
)
from apps.worker.services.review_ops_metrics import (
    DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    REVIEW_OPS_METRICS_CONTRACT_TYPE,
    REVIEW_OPS_METRICS_CONTRACT_VERSION,
)
from apps.worker.services.reviewer_confidence_schema import (
    DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    REVIEWER_CONFIDENCE_SCHEMA_TYPE,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_CONTRACT_TYPE,
    DATASET_CORPUS_CONTRACT_VERSION,
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
)

CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE = (
    "camera_geometry_calibration_provenance_contract"
)
CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION = "v1"
CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE = "camera_geometry_calibration_profile"
CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION = "v1"
CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE = "camera_geometry_calibration_report"
CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION = "v1"
CAMERA_GEOMETRY_CALIBRATION_BLUEPRINT = "blueprint_36"
CAMERA_GEOMETRY_CALIBRATION_BLUEPRINT_NAME = (
    "camera_geometry_confidence_calibration_provenance_v1"
)

DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT = (
    ".data/contracts/camera_geometry_calibration_provenance_contract_v1.json"
)
DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT = (
    ".data/exports/camera_geometry_calibration_profile.current.json"
)
DEFAULT_CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT = (
    ".data/exports/camera_geometry_calibration_profile.validation.json"
)
DEFAULT_CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT = (
    ".data/exports/camera_geometry_calibration_report.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)

CAMERA_GEOMETRY_ENTITIES = [
    "camera_geometry_profile",
    "camera_geometry_evidence_ref",
    "camera_view_evidence_ref",
    "court_keypoint_evidence_ref",
    "court_line_evidence_ref",
    "homography_candidate_ref",
    "projection_diagnostic_ref",
    "object_to_court_projection_ref",
    "ball_trajectory_3d_ref",
    "replay_overlay_ref",
    "calibration_review_ref",
    "provenance_ref",
]

CALIBRATION_PROFILE_FIELDS = [
    "profile_type",
    "profile_version",
    "generated_at",
    "media_id",
    "camera_geometry_id",
    "camera_view_id",
    "homography_candidate_id",
    "projection_diagnostic_id",
    "trajectory_3d_run_id",
    "associated_run_ids",
    "replay_url",
    "source_paths",
    "evidence_availability",
    "court_keypoint_count",
    "court_line_count",
    "homography_candidate_count",
    "projection_diagnostic_count",
    "projection_residual_summary",
    "camera_geometry_source_status",
    "calibration_provenance_status",
    "calibration_evidence_status",
    "calibration_review_status",
    "calibration_confidence_status",
    "requires_human_calibration_review",
    "warnings",
]

CONFIDENCE_STATUS_VALUES = [
    "not_assessed",
    "unknown",
    "evidence_missing",
    "evidence_partial",
    "evidence_present",
    "provenance_partial",
    "provenance_present",
    "projection_diagnostics_present",
    "calibration_review_needed",
    "human_review_ready",
    "regression_protected_context",
    "not_applicable",
]

EVIDENCE_STATUS_VALUES = [
    "not_assessed",
    "missing_camera_geometry",
    "missing_camera_view",
    "missing_court_keypoints",
    "missing_homography_candidate",
    "missing_projection_diagnostics",
    "missing_replay_context",
    "evidence_partial",
    "evidence_present",
    "not_applicable",
]

PROVENANCE_STATUS_VALUES = [
    "not_assessed",
    "provenance_present",
    "provenance_partial",
    "provenance_missing",
    "conflicting_references",
    "not_applicable",
]

REVIEW_STATUS_VALUES = [
    "not_assessed",
    "review_missing",
    "review_optional",
    "review_needed",
    "review_ready",
    "not_applicable",
]

FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS = {
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
    "calibration_truth",
    "homography_truth",
    "geometry_truth",
    "line_call_truth",
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "reviewer_score",
    "reviewer_rank",
    "quality_score",
    "training_truth",
    "model_ready_truth",
    "pass_due_to_calibration",
    "fail_due_to_calibration",
}

CAMERA_GEOMETRY_CALIBRATION_WARNINGS = {
    "camera_geometry_calibration_provenance_is_not_truth": True,
    "camera_geometry_confidence_is_structural_only": True,
    "calibration_profile_does_not_create_evidence": True,
    "calibration_report_does_not_create_evidence": True,
    "observation_only": True,
    "provenance_only": True,
    "review_support_only": True,
    "no_adjudication": True,
    "does_not_create_calibration_truth": True,
    "does_not_create_homography_truth": True,
    "does_not_create_geometry_truth": True,
    "does_not_create_line_call_truth": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_generate_camera_geometry": True,
    "does_not_generate_homography": True,
    "does_not_generate_projection_diagnostics": True,
    "not_generalization_claim": True,
}

PROFILE_ENTRY_WARNINGS = {
    "calibration_profile_entry_is_structural_only": True,
    "calibration_status_is_not_truth": True,
    "confidence_status_is_not_a_score": True,
    "human_review_flag_is_routing_only": True,
    "no_adjudication": True,
}


def export_camera_geometry_calibration_provenance_contract(
    *,
    output_path: str | Path | None = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen camera-geometry calibration provenance contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE,
        "contract_version": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "report_type": CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
        "report_version": CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
        "contract": contract,
        "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_camera_geometry_calibration_profile(
    *,
    contract_path: str | Path = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
    replay_index_path: str | Path | None = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    regression_matrix_path: str | Path | None = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    corpus_manifest_path: str | Path | None = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    label_feedback_inputs_path: str | Path | None = (
        DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural camera-geometry calibration provenance profile."""

    generated_at = generated_at or datetime.now(UTC)
    contract_loaded = _load_json(
        contract_path,
        label="camera_geometry_calibration_provenance_contract",
    )
    if contract_loaded.get("ok") is False:
        return contract_loaded
    contract = _dict(contract_loaded["data"])
    contract_errors = _validate_contract_shape(contract)
    if contract_errors:
        return {
            "ok": False,
            "status": "invalid_camera_geometry_calibration_contract",
            "error_count": len(contract_errors),
            "errors": contract_errors,
            "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
        }

    replay_index_source = _load_optional_json(
        replay_index_path,
        label="multi_point_replay_index",
        type_field="index_type",
        expected_type=MULTI_POINT_REPLAY_INDEX_TYPE,
        version_field="index_version",
        expected_version=MULTI_POINT_REPLAY_INDEX_VERSION,
    )
    matrix_source = _load_optional_json(
        regression_matrix_path,
        label="multi_point_regression_matrix",
        type_field="matrix_type",
        expected_type=MULTI_POINT_REGRESSION_MATRIX_TYPE,
        version_field="matrix_version",
        expected_version=MULTI_POINT_REGRESSION_MATRIX_VERSION,
    )
    corpus_source = _load_optional_json(
        corpus_manifest_path,
        label="versioned_dataset_corpus_manifest",
        type_field="corpus_manifest_type",
        expected_type=DATASET_CORPUS_MANIFEST_TYPE,
        version_field="corpus_manifest_version",
        expected_version=DATASET_CORPUS_MANIFEST_VERSION,
    )
    feedback_source = _load_optional_json(
        label_feedback_inputs_path,
        label="label_feedback_evaluation_inputs",
        type_field="feedback_inputs_type",
        expected_type=LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        version_field="feedback_inputs_version",
        expected_version=LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
    )
    sources = {
        "multi_point_replay_index": replay_index_source,
        "multi_point_regression_matrix": matrix_source,
        "versioned_dataset_corpus_manifest": corpus_source,
        "label_feedback_evaluation_inputs": feedback_source,
    }
    source_paths = {
        "contract_path": str(Path(contract_path)),
        "replay_index_path": _path_or_none(replay_index_path),
        "regression_matrix_path": _path_or_none(regression_matrix_path),
        "corpus_manifest_path": _path_or_none(corpus_manifest_path),
        "label_feedback_inputs_path": _path_or_none(label_feedback_inputs_path),
    }
    profile_entries = _profile_entries(
        replay_index=_dict(replay_index_source.get("data")),
        matrix=_dict(matrix_source.get("data")),
        corpus_manifest=_dict(corpus_source.get("data")),
        feedback_inputs=_dict(feedback_source.get("data")),
        source_paths=source_paths,
        generated_at=generated_at,
    )
    source_warnings = _source_warnings(sources)
    profile = {
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "profile_id": _profile_id(profile_entries),
        "generated_at": generated_at.isoformat(),
        "source_paths": source_paths,
        "source_statuses": _source_statuses(sources),
        "source_contract_versions": _source_contract_refs(),
        "calibration_profile_count": len(profile_entries),
        "camera_geometry_profiles": profile_entries,
        "summary": _summary_counts(profile_entries),
        "source_warnings": source_warnings,
        "known_limitations": _known_limitations(
            profile_count=len(profile_entries),
            source_warnings=source_warnings,
        ),
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "structural_warning_count": len(source_warnings),
            "validation_does_not_create_calibration_truth": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
            "profile_uses_existing_artifacts_only": True,
            "missing_projection_diagnostics_are_structural_gaps": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "calibration_profile_count": len(profile_entries),
        "summary": profile["summary"],
        "profile": profile,
        "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile, indent=2, sort_keys=True), encoding="utf-8")
        result["profile_output"] = str(path)
    return result


def validate_camera_geometry_calibration_profile(
    *,
    contract_path: str | Path = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
    profile_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    intennse_alignment_contract_path: str | Path | None = (
        DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT
    ),
    dataset_corpus_contract_path: str | Path | None = (
        DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT
    ),
    coverage_sampling_contract_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT
    ),
    many_point_ingestion_contract_path: str | Path | None = (
        DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT
    ),
    review_ops_metrics_contract_path: str | Path | None = (
        DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT
    ),
    label_feedback_contract_path: str | Path | None = (
        DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate the calibration provenance profile structurally."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(
        contract_path,
        label="camera_geometry_calibration_provenance_contract",
    )
    if contract_loaded.get("ok") is False:
        return contract_loaded
    profile_loaded = _load_json(profile_path, label="camera_geometry_calibration_profile")
    if profile_loaded.get("ok") is False:
        return profile_loaded

    contract = _dict(contract_loaded["data"])
    profile = _dict(profile_loaded["data"])
    errors = _validate_contract_shape(contract)
    structural_warnings: list[dict[str, Any]] = []
    contract_validations: list[dict[str, Any]] = []
    if not errors:
        contract_result = _validate_referenced_contracts(
            observation_quality_taxonomy_path=observation_quality_taxonomy_path,
            review_label_schema_path=review_label_schema_path,
            reviewer_confidence_schema_path=reviewer_confidence_schema_path,
            multi_reviewer_schema_path=multi_reviewer_schema_path,
            intennse_alignment_contract_path=intennse_alignment_contract_path,
            dataset_corpus_contract_path=dataset_corpus_contract_path,
            coverage_sampling_contract_path=coverage_sampling_contract_path,
            many_point_ingestion_contract_path=many_point_ingestion_contract_path,
            review_ops_metrics_contract_path=review_ops_metrics_contract_path,
            label_feedback_contract_path=label_feedback_contract_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        contract_validations.extend(_list(contract_result.get("validations")))
        profile_result = _validate_profile_shape(profile)
        errors.extend(_list(profile_result.get("errors")))
        structural_warnings.extend(_list(profile_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "camera_geometry_calibration_profile_validation",
        "validation_version": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "profile_path": str(Path(profile_path)),
        "contract_type": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE,
        "contract_version": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "referenced_contract_validations": contract_validations,
        "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
        "known_limitations": [
            "Validation checks contract, profile, status, and provenance shape.",
            "Validation reports missing geometry diagnostics as structural gaps.",
            "Validation does not create camera geometry or homography candidates.",
            "Validation does not create projection diagnostics.",
            "Validation does not decide calibration validity.",
            "Validation does not create training truth.",
            "Validation does not modify regression baselines.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_camera_geometry_calibration_report(
    *,
    contract_path: str | Path = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
    profile_path: str | Path = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT,
    output_path: str | Path | None = DEFAULT_CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural report over camera-geometry calibration profiles."""

    generated_at = generated_at or datetime.now(UTC)
    contract_loaded = _load_json(
        contract_path,
        label="camera_geometry_calibration_provenance_contract",
    )
    if contract_loaded.get("ok") is False:
        return contract_loaded
    profile_loaded = _load_json(profile_path, label="camera_geometry_calibration_profile")
    if profile_loaded.get("ok") is False:
        return profile_loaded
    contract = _dict(contract_loaded["data"])
    profile = _dict(profile_loaded["data"])
    errors = _validate_contract_shape(contract)
    errors.extend(_list(_validate_profile_shape(profile).get("errors")))
    if errors:
        return {
            "ok": False,
            "status": "invalid_camera_geometry_calibration_profile",
            "error_count": len(errors),
            "errors": errors,
            "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
        }

    profiles = [
        item
        for item in _list(profile.get("camera_geometry_profiles"))
        if isinstance(item, dict)
    ]
    summary = _report_summary(profiles)
    report = {
        "report_type": CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
        "report_version": CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_profile_path": str(Path(profile_path)),
        "source_paths": _dict(profile.get("source_paths")),
        "source_contract_versions": _source_contract_refs(),
        "calibration_profile_count": len(profiles),
        "summary": summary,
        "camera_geometry_source_status_counts": _status_counts(
            profiles,
            "camera_geometry_source_status",
        ),
        "calibration_evidence_status_counts": _status_counts(
            profiles,
            "calibration_evidence_status",
        ),
        "calibration_provenance_status_counts": _status_counts(
            profiles,
            "calibration_provenance_status",
        ),
        "calibration_review_status_counts": _status_counts(
            profiles,
            "calibration_review_status",
        ),
        "calibration_confidence_status_counts": _status_counts(
            profiles,
            "calibration_confidence_status",
        ),
        "report_sections": _report_sections(summary),
        "source_warnings": _list(profile.get("source_warnings")),
        "known_limitations": _list(profile.get("known_limitations")),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
            "report_is_structural_only": True,
            "report_does_not_create_calibration_truth": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
        "report_version": CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
        "calibration_profile_count": len(profiles),
        "summary": summary,
        "report": report,
        "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE,
        "contract_version": CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "report_type": CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
        "report_version": CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
        "calibration_scope": {
            "purpose": (
                "Summarize camera-geometry, court-geometry, homography, projection, "
                "replay, and review provenance as structural evidence readiness."
            ),
            "read_only": True,
            "uses_existing_artifacts_only": True,
            "media_ingestion_allowed": False,
            "event_generation_allowed": False,
            "three_d_generation_allowed": False,
            "camera_geometry_generation_allowed": False,
            "homography_generation_allowed": False,
            "projection_diagnostic_generation_allowed": False,
            "line_call_decision_allowed": False,
            "score_decision_allowed": False,
            "player_identity_decision_allowed": False,
            "reviewer_ranking_allowed": False,
            "reviewer_scoring_allowed": False,
            "model_retraining_allowed": False,
        },
        "source_contract_refs": _source_contract_refs(),
        "camera_geometry_entities": list(CAMERA_GEOMETRY_ENTITIES),
        "calibration_profile_schema": {
            "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
            "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
            "profile_fields": [
                {"key": field, "required": True}
                for field in CALIBRATION_PROFILE_FIELDS
            ],
            "profiles_array_field": "camera_geometry_profiles",
            "read_only": True,
        },
        "calibration_report_schema": {
            "report_type": CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
            "report_version": CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
            "summary_is_structural_only": True,
            "report_sections_are_review_routing_only": True,
        },
        "evidence_confidence_semantics": {
            "confidence_status_values": list(CONFIDENCE_STATUS_VALUES),
            "evidence_status_values": list(EVIDENCE_STATUS_VALUES),
            "provenance_status_values": list(PROVENANCE_STATUS_VALUES),
            "review_status_values": list(REVIEW_STATUS_VALUES),
            "confidence_is_not_probability": True,
            "confidence_is_not_score": True,
            "confidence_is_not_calibration_decision": True,
            "missing_diagnostics_are_review_gaps": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "contract_shape_validated": True,
            "profile_shape_validated": True,
            "allowed_confidence_status_values_only": True,
            "allowed_evidence_status_values_only": True,
            "allowed_provenance_status_values_only": True,
            "allowed_review_status_values_only": True,
            "referenced_contract_versions_validated_when_paths_available": True,
            "missing_optional_refs_are_structural_warnings": True,
            "does_not_create_calibration_truth": True,
            "does_not_create_geometry_truth": True,
            "does_not_create_homography_truth": True,
            "does_not_create_line_call_truth": True,
            "does_not_create_event_truth": True,
            "does_not_create_3d_truth": True,
            "does_not_create_labels": True,
            "does_not_rank_reviewers": True,
            "does_not_score_reviewers": True,
            "does_not_modify_evaluation_baselines": True,
            "does_not_ingest_media": True,
            "does_not_execute_sampling": True,
            "forbidden_fields": sorted(FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS),
            "forbidden_values": sorted(FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS),
        },
        "provenance_requirements": {
            "source_paths_preserved": True,
            "source_contract_versions_preserved": True,
            "point_manifest_refs_preserved": True,
            "replay_urls_preserved": True,
            "associated_run_ids_preserved": True,
            "camera_geometry_ids_preserved": True,
            "trajectory_3d_run_ids_preserved": True,
            "evidence_availability_preserved": True,
            "profile_counts_preserved": True,
            "source_warnings_preserved_when_available": True,
            "protected_sample_point_preserved_as_regression_context": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(CAMERA_GEOMETRY_CALIBRATION_WARNINGS),
    }


def _source_contract_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "versioned_dataset_corpus_contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "coverage_sampling_strategy_contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "review_ops_metrics_contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "label_feedback_evaluation_contract_version": (
            LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION
        ),
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _profile_entries(
    *,
    replay_index: dict[str, Any],
    matrix: dict[str, Any],
    corpus_manifest: dict[str, Any],
    feedback_inputs: dict[str, Any],
    source_paths: dict[str, Any],
    generated_at: datetime,
) -> list[dict[str, Any]]:
    feedback_by_manifest = _items_by_manifest(
        _list(feedback_inputs.get("feedback_entries"))
    )
    points = _merged_point_contexts(
        replay_points=_list(replay_index.get("points")),
        matrix_points=_list(matrix.get("points")),
        corpus_entries=_list(corpus_manifest.get("corpus_entries")),
    )
    return [
        _profile_entry(
            point=point,
            feedback_entry=feedback_by_manifest.get(
                _string_or_none(point.get("point_manifest_id"))
            ),
            source_paths=source_paths,
            generated_at=generated_at,
        )
        for point in points
    ]


def _profile_entry(
    *,
    point: dict[str, Any],
    feedback_entry: dict[str, Any] | None,
    source_paths: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    associated_run_ids = _string_dict(point.get("associated_run_ids"))
    profile_counts = _int_dict(point.get("profile_counts"))
    base_availability = _bool_dict(point.get("evidence_availability"))
    camera_geometry_id = _first_string(
        associated_run_ids.get("camera_geometry_id"),
        point.get("camera_geometry_id"),
    )
    camera_view_id = _first_string(
        associated_run_ids.get("camera_view_id"),
        point.get("camera_view_id"),
    )
    homography_candidate_id = _first_string(
        associated_run_ids.get("homography_candidate_id"),
        associated_run_ids.get("homography_run_id"),
        point.get("homography_candidate_id"),
    )
    projection_diagnostic_id = _first_string(
        associated_run_ids.get("projection_diagnostic_id"),
        associated_run_ids.get("projection_diagnostic_run_id"),
        point.get("projection_diagnostic_id"),
    )
    trajectory_3d_run_id = _first_string(
        associated_run_ids.get("trajectory_3d_run_id"),
        point.get("trajectory_3d_run_id"),
    )
    court_keypoint_count = _count_value(profile_counts, "court_keypoint_count")
    court_line_count = _count_value(profile_counts, "court_line_count")
    homography_candidate_count = _count_value(profile_counts, "homography_candidate_count")
    projection_diagnostic_count = _count_value(
        profile_counts,
        "projection_diagnostic_count",
    )
    evidence_availability = {
        **base_availability,
        "camera_geometry_available": camera_geometry_id is not None,
        "camera_view_available": camera_view_id is not None,
        "court_keypoints_available": court_keypoint_count > 0,
        "court_lines_available": court_line_count > 0,
        "homography_candidate_available": (
            homography_candidate_id is not None or homography_candidate_count > 0
        ),
        "projection_diagnostics_available": (
            projection_diagnostic_id is not None or projection_diagnostic_count > 0
        ),
        "replay_context_available": bool(_string_or_none(point.get("replay_url"))),
        "trajectory_3d_run_available": trajectory_3d_run_id is not None,
    }
    labels = _string_list(point.get("labels"))
    statuses = _calibration_statuses(
        labels=labels,
        evidence_availability=evidence_availability,
        camera_geometry_id=camera_geometry_id,
    )
    source_warning_flags = {
        "missing_camera_geometry": camera_geometry_id is None,
        "missing_camera_view": camera_view_id is None,
        "missing_court_keypoints": court_keypoint_count == 0,
        "missing_homography_candidate": not evidence_availability[
            "homography_candidate_available"
        ],
        "missing_projection_diagnostics": not evidence_availability[
            "projection_diagnostics_available"
        ],
        "missing_replay_context": not evidence_availability["replay_context_available"],
        "regression_protected_context": "protected_sample_point" in labels,
    }
    return {
        "profile_type": CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
        "profile_version": CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
        "profile_entry_id": _profile_entry_id(point),
        "generated_at": generated_at.isoformat(),
        "source_corpus_entry_id": _string_or_none(point.get("corpus_entry_id")),
        "point_manifest_id": _string_or_none(point.get("point_manifest_id")),
        "point_manifest_path": _string_or_none(point.get("point_manifest_path"))
        or _string_or_none(point.get("manifest_path")),
        "media_id": _string_or_none(point.get("media_id")),
        "camera_geometry_id": camera_geometry_id,
        "camera_view_id": camera_view_id,
        "homography_candidate_id": homography_candidate_id,
        "projection_diagnostic_id": projection_diagnostic_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "associated_run_ids": associated_run_ids,
        "replay_url": _string_or_none(point.get("replay_url")),
        "source_paths": _entry_source_paths(point=point, source_paths=source_paths),
        "source_media_path": _string_or_none(point.get("source_media_path")),
        "source_uri": _string_or_none(point.get("source_uri")),
        "stored_path": _string_or_none(point.get("stored_path")),
        "stored_uri": _string_or_none(point.get("stored_uri")),
        "evidence_availability": evidence_availability,
        "profile_counts": profile_counts,
        "court_keypoint_count": court_keypoint_count,
        "court_line_count": court_line_count,
        "homography_candidate_count": homography_candidate_count,
        "projection_diagnostic_count": projection_diagnostic_count,
        "projection_residual_summary": _dict(point.get("projection_residual_summary")),
        "camera_geometry_source_status": statuses["camera_geometry_source_status"],
        "calibration_provenance_status": statuses["calibration_provenance_status"],
        "calibration_evidence_status": statuses["calibration_evidence_status"],
        "calibration_review_status": statuses["calibration_review_status"],
        "calibration_confidence_status": statuses["calibration_confidence_status"],
        "requires_human_calibration_review": statuses[
            "requires_human_calibration_review"
        ],
        "labels": labels,
        "calibration_review_refs": _review_refs(feedback_entry),
        "feedback_evaluation_ref": _feedback_ref(feedback_entry),
        "provenance_ref": {
            "corpus_provenance_status": _string_or_none(point.get("provenance_status")),
            "corpus_provenance_gaps": _string_list(point.get("provenance_gaps")),
            "source_paths": _entry_source_paths(point=point, source_paths=source_paths),
        },
        "source_warnings": _dict(point.get("warnings")),
        "warnings": {
            **dict(PROFILE_ENTRY_WARNINGS),
            **source_warning_flags,
        },
    }


def _calibration_statuses(
    *,
    labels: list[str],
    evidence_availability: dict[str, bool],
    camera_geometry_id: str | None,
) -> dict[str, Any]:
    camera_available = camera_geometry_id is not None
    replay_available = evidence_availability.get("replay_context_available") is True
    court_available = evidence_availability.get("court_keypoints_available") is True
    homography_available = evidence_availability.get("homography_candidate_available") is True
    diagnostics_available = (
        evidence_availability.get("projection_diagnostics_available") is True
    )
    source_status = "evidence_present" if camera_available else "missing_camera_geometry"

    if not camera_available:
        evidence_status = "missing_camera_geometry"
    elif not replay_available:
        evidence_status = "missing_replay_context"
    elif court_available and homography_available and diagnostics_available:
        evidence_status = "evidence_present"
    else:
        evidence_status = "evidence_partial"

    if camera_available and replay_available and (
        court_available or homography_available or diagnostics_available
    ):
        provenance_status = "provenance_present"
    elif camera_available or replay_available:
        provenance_status = "provenance_partial"
    else:
        provenance_status = "provenance_missing"

    if camera_available and replay_available:
        review_status = "review_ready"
    elif camera_available or replay_available:
        review_status = "review_needed"
    else:
        review_status = "review_missing"

    requires_human_review = not (
        camera_available
        and replay_available
        and court_available
        and homography_available
        and diagnostics_available
    )

    if "protected_sample_point" in labels:
        confidence_status = "regression_protected_context"
    elif not camera_available:
        confidence_status = "evidence_missing"
    elif diagnostics_available:
        confidence_status = "projection_diagnostics_present"
    elif evidence_status == "evidence_partial":
        confidence_status = "evidence_partial"
    elif provenance_status == "provenance_partial":
        confidence_status = "provenance_partial"
    elif evidence_status == "evidence_present":
        confidence_status = "evidence_present"
    else:
        confidence_status = "evidence_missing"

    return {
        "camera_geometry_source_status": source_status,
        "calibration_evidence_status": evidence_status,
        "calibration_provenance_status": provenance_status,
        "calibration_review_status": review_status,
        "calibration_confidence_status": confidence_status,
        "requires_human_calibration_review": requires_human_review,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "calibration_scope",
        "source_contract_refs",
        "camera_geometry_entities",
        "calibration_profile_schema",
        "calibration_report_schema",
        "evidence_confidence_semantics",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors

    errors.extend(_source_contract_ref_errors(_dict(contract.get("source_contract_refs"))))
    semantics = _dict(contract.get("evidence_confidence_semantics"))
    if set(_string_list(semantics.get("confidence_status_values"))) != set(
        CONFIDENCE_STATUS_VALUES
    ):
        errors.append(
            _error(
                "invalid_confidence_status_values",
                "evidence_confidence_semantics.confidence_status_values",
                semantics.get("confidence_status_values"),
            )
        )
    if set(_string_list(semantics.get("evidence_status_values"))) != set(
        EVIDENCE_STATUS_VALUES
    ):
        errors.append(
            _error(
                "invalid_evidence_status_values",
                "evidence_confidence_semantics.evidence_status_values",
                semantics.get("evidence_status_values"),
            )
        )
    if set(_string_list(semantics.get("provenance_status_values"))) != set(
        PROVENANCE_STATUS_VALUES
    ):
        errors.append(
            _error(
                "invalid_provenance_status_values",
                "evidence_confidence_semantics.provenance_status_values",
                semantics.get("provenance_status_values"),
            )
        )
    if set(_string_list(semantics.get("review_status_values"))) != set(
        REVIEW_STATUS_VALUES
    ):
        errors.append(
            _error(
                "invalid_review_status_values",
                "evidence_confidence_semantics.review_status_values",
                semantics.get("review_status_values"),
            )
        )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "contract_shape_validated",
        "profile_shape_validated",
        "allowed_confidence_status_values_only",
        "allowed_evidence_status_values_only",
        "allowed_provenance_status_values_only",
        "allowed_review_status_values_only",
        "does_not_create_calibration_truth",
        "does_not_create_geometry_truth",
        "does_not_create_homography_truth",
        "does_not_create_line_call_truth",
        "does_not_create_event_truth",
        "does_not_create_3d_truth",
        "does_not_create_labels",
        "does_not_rank_reviewers",
        "does_not_score_reviewers",
        "does_not_modify_evaluation_baselines",
        "does_not_ingest_media",
        "does_not_execute_sampling",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_profile_shape(profile: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(profile, path="profile")
    errors.extend(_forbidden_value_errors(profile, path="profile"))
    structural_warnings: list[dict[str, Any]] = []
    if profile.get("profile_type") != CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE:
        errors.append(
            _error("invalid_profile_type", "profile_type", profile.get("profile_type"))
        )
    if profile.get("profile_version") != CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION:
        errors.append(
            _error(
                "invalid_profile_version",
                "profile_version",
                profile.get("profile_version"),
            )
        )
    entries = [
        item
        for item in _list(profile.get("camera_geometry_profiles"))
        if isinstance(item, dict)
    ]
    if len(entries) != int(profile.get("calibration_profile_count") or 0):
        errors.append(
            _error(
                "profile_count_mismatch",
                "calibration_profile_count",
                profile.get("calibration_profile_count"),
            )
        )
    for index, entry in enumerate(entries):
        path = f"camera_geometry_profiles[{index}]"
        errors.extend(_validate_profile_entry(entry, path=path))
        if entry.get("requires_human_calibration_review") is True:
            structural_warnings.append(
                _warning(
                    "requires_human_calibration_review",
                    path,
                    entry.get("profile_entry_id"),
                )
            )
        if entry.get("calibration_provenance_status") == "provenance_partial":
            structural_warnings.append(
                _warning("provenance_partial", path, entry.get("profile_entry_id"))
            )
        if (
            _dict(entry.get("evidence_availability")).get("projection_diagnostics_available")
            is not True
        ):
            structural_warnings.append(
                _warning(
                    "missing_projection_diagnostics",
                    path,
                    entry.get("profile_entry_id"),
                )
            )
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_profile_entry(entry: dict[str, Any], *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in (
        "profile_type",
        "profile_version",
        "profile_entry_id",
        "media_id",
        "associated_run_ids",
        "replay_url",
        "source_paths",
        "evidence_availability",
        "camera_geometry_source_status",
        "calibration_provenance_status",
        "calibration_evidence_status",
        "calibration_review_status",
        "calibration_confidence_status",
        "requires_human_calibration_review",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_profile_field", f"{path}.{field}", None))
    if entry.get("profile_type") != CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE:
        errors.append(
            _error("invalid_profile_entry_type", f"{path}.profile_type", entry.get("profile_type"))
        )
    if entry.get("profile_version") != CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION:
        errors.append(
            _error(
                "invalid_profile_entry_version",
                f"{path}.profile_version",
                entry.get("profile_version"),
            )
        )
    if entry.get("camera_geometry_source_status") not in EVIDENCE_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_camera_geometry_source_status",
                f"{path}.camera_geometry_source_status",
                entry.get("camera_geometry_source_status"),
            )
        )
    if entry.get("calibration_evidence_status") not in EVIDENCE_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_calibration_evidence_status",
                f"{path}.calibration_evidence_status",
                entry.get("calibration_evidence_status"),
            )
        )
    if entry.get("calibration_provenance_status") not in PROVENANCE_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_calibration_provenance_status",
                f"{path}.calibration_provenance_status",
                entry.get("calibration_provenance_status"),
            )
        )
    if entry.get("calibration_review_status") not in REVIEW_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_calibration_review_status",
                f"{path}.calibration_review_status",
                entry.get("calibration_review_status"),
            )
        )
    if entry.get("calibration_confidence_status") not in CONFIDENCE_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_calibration_confidence_status",
                f"{path}.calibration_confidence_status",
                entry.get("calibration_confidence_status"),
            )
        )
    return errors


def _validate_referenced_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
    intennse_alignment_contract_path: str | Path | None,
    dataset_corpus_contract_path: str | Path | None,
    coverage_sampling_contract_path: str | Path | None,
    many_point_ingestion_contract_path: str | Path | None,
    review_ops_metrics_contract_path: str | Path | None,
    label_feedback_contract_path: str | Path | None,
) -> dict[str, Any]:
    specs = [
        (
            "observation_quality_taxonomy",
            observation_quality_taxonomy_path,
            "taxonomy_type",
            OBSERVATION_QUALITY_TAXONOMY_TYPE,
            "taxonomy_version",
            OBSERVATION_QUALITY_TAXONOMY_VERSION,
        ),
        (
            "review_label_schema",
            review_label_schema_path,
            "schema_type",
            REVIEW_LABEL_SCHEMA_TYPE,
            "schema_version",
            REVIEW_LABEL_SCHEMA_VERSION,
        ),
        (
            "reviewer_confidence_schema",
            reviewer_confidence_schema_path,
            "schema_type",
            REVIEWER_CONFIDENCE_SCHEMA_TYPE,
            "schema_version",
            REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        ),
        (
            "multi_reviewer_disagreement_schema",
            multi_reviewer_schema_path,
            "schema_type",
            MULTI_REVIEWER_SCHEMA_TYPE,
            "schema_version",
            MULTI_REVIEWER_SCHEMA_VERSION,
        ),
        (
            "intennse_label_alignment_contract",
            intennse_alignment_contract_path,
            "contract_type",
            INTENNSE_ALIGNMENT_CONTRACT_TYPE,
            "contract_version",
            INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        ),
        (
            "versioned_dataset_corpus_contract",
            dataset_corpus_contract_path,
            "contract_type",
            DATASET_CORPUS_CONTRACT_TYPE,
            "contract_version",
            DATASET_CORPUS_CONTRACT_VERSION,
        ),
        (
            "coverage_sampling_strategy_contract",
            coverage_sampling_contract_path,
            "contract_type",
            COVERAGE_SAMPLING_CONTRACT_TYPE,
            "contract_version",
            COVERAGE_SAMPLING_CONTRACT_VERSION,
        ),
        (
            "many_point_ingestion_gate_contract",
            many_point_ingestion_contract_path,
            "contract_type",
            MANY_POINT_INGESTION_CONTRACT_TYPE,
            "contract_version",
            MANY_POINT_INGESTION_CONTRACT_VERSION,
        ),
        (
            "review_ops_metrics_contract",
            review_ops_metrics_contract_path,
            "contract_type",
            REVIEW_OPS_METRICS_CONTRACT_TYPE,
            "contract_version",
            REVIEW_OPS_METRICS_CONTRACT_VERSION,
        ),
        (
            "label_feedback_evaluation_contract",
            label_feedback_contract_path,
            "contract_type",
            LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
            "contract_version",
            LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
        ),
    ]
    validations: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    for label, path, type_field, expected_type, version_field, expected_version in specs:
        validation = _validate_json_type_version(
            label=label,
            path=path,
            type_field=type_field,
            expected_type=expected_type,
            version_field=version_field,
            expected_version=expected_version,
        )
        validations.append(validation)
        if validation["status"] == "missing":
            structural_warnings.append(_warning("source_contract_missing", label, path))
        elif validation["status"] == "not_supplied":
            structural_warnings.append(_warning("source_contract_not_supplied", label, path))
        elif validation["ok"] is not True:
            errors.append(
                _error(
                    "invalid_referenced_contract",
                    label,
                    validation.get("error") or validation,
                )
            )
    return {
        "validations": validations,
        "errors": errors,
        "structural_warnings": structural_warnings,
    }


def _merged_point_contexts(
    *,
    replay_points: list[Any],
    matrix_points: list[Any],
    corpus_entries: list[Any],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for items in (replay_points, matrix_points, corpus_entries):
        for item in items:
            if not isinstance(item, dict):
                continue
            key = _point_key(item)
            if key not in merged:
                merged[key] = {}
                order.append(key)
            merged[key].update({k: v for k, v in item.items() if v is not None})
    return sorted((merged[key] for key in order), key=_point_sort_key)


def _items_by_manifest(items: list[Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        point_manifest_id = _string_or_none(item.get("point_manifest_id"))
        if point_manifest_id:
            result[point_manifest_id] = item
    return result


def _summary_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary = Counter()
    summary["calibration_profile_count"] = len(entries)
    for entry in entries:
        availability = _dict(entry.get("evidence_availability"))
        summary["camera_geometry_evidence_present_count"] += (
            availability.get("camera_geometry_available") is True
        )
        summary["camera_geometry_evidence_missing_count"] += (
            availability.get("camera_geometry_available") is not True
        )
        summary["projection_diagnostics_present_count"] += (
            availability.get("projection_diagnostics_available") is True
        )
        summary["missing_projection_diagnostics_count"] += (
            availability.get("projection_diagnostics_available") is not True
        )
        summary["provenance_partial_count"] += (
            entry.get("calibration_provenance_status") == "provenance_partial"
        )
        summary["calibration_review_needed_count"] += (
            entry.get("requires_human_calibration_review") is True
        )
        summary["human_review_ready_count"] += (
            entry.get("calibration_review_status") == "review_ready"
        )
        summary["regression_protected_context_count"] += (
            entry.get("calibration_confidence_status")
            == "regression_protected_context"
        )
        summary["missing_homography_candidate_count"] += (
            availability.get("homography_candidate_available") is not True
        )
        summary["missing_court_keypoints_count"] += (
            availability.get("court_keypoints_available") is not True
        )
        summary["missing_replay_context_count"] += (
            availability.get("replay_context_available") is not True
        )
    return {key: int(value) for key, value in sorted(summary.items())}


def _report_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary = _summary_counts(entries)
    summary["structural_confidence_only_count"] = len(entries)
    summary["camera_geometry_profiles_reported_count"] = len(entries)
    return summary


def _report_sections(summary: dict[str, int]) -> list[dict[str, Any]]:
    section_specs = [
        ("camera_geometry_evidence_present", "camera_geometry_evidence_present_count"),
        ("camera_geometry_evidence_missing", "camera_geometry_evidence_missing_count"),
        ("projection_diagnostics_present", "projection_diagnostics_present_count"),
        ("provenance_partial", "provenance_partial_count"),
        ("calibration_review_needed", "calibration_review_needed_count"),
        ("human_review_ready", "human_review_ready_count"),
        ("regression_protected_context", "regression_protected_context_count"),
        ("structural_confidence_only", "structural_confidence_only_count"),
    ]
    return [
        {
            "section_id": section_id,
            "profile_count": int(summary.get(count_key, 0)),
            "status": "present" if int(summary.get(count_key, 0)) else "not_applicable",
            "structural_only": True,
            "warnings": dict(PROFILE_ENTRY_WARNINGS),
        }
        for section_id, count_key in section_specs
    ]


def _status_counts(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter()
    for entry in entries:
        status = _string_or_none(entry.get(field))
        if status:
            counts[status] += 1
    return dict(sorted(counts.items()))


def _source_contract_ref_errors(refs: dict[str, Any]) -> list[dict[str, Any]]:
    expected = _source_contract_refs()
    errors: list[dict[str, Any]] = []
    for key, expected_value in expected.items():
        if refs.get(key) != expected_value:
            errors.append(
                _error("invalid_source_contract_ref", key, refs.get(key))
            )
    return errors


def _validate_json_type_version(
    *,
    label: str,
    path: str | Path | None,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {
            "label": label,
            "path": None,
            "ok": True,
            "status": "not_supplied",
            "optional": True,
        }
    loaded = _load_json(path, label=label)
    if loaded.get("ok") is False:
        if loaded.get("status") == "missing":
            return {
                "label": label,
                "path": str(Path(path)),
                "ok": True,
                "status": "missing",
                "optional": True,
            }
        return {
            "label": label,
            "path": str(Path(path)),
            "ok": False,
            "status": "invalid_json",
            "error": loaded.get("error"),
        }
    payload = _dict(loaded.get("data"))
    type_value = payload.get(type_field)
    version_value = payload.get(version_field)
    ok = type_value == expected_type and version_value == expected_version
    return {
        "label": label,
        "path": str(Path(path)),
        "ok": ok,
        "status": "valid" if ok else "invalid_type_or_version",
        "type_field": type_field,
        "type_value": type_value,
        "expected_type": expected_type,
        "version_field": version_field,
        "version_value": version_value,
        "expected_version": expected_version,
    }


def _load_optional_json(
    path: str | Path | None,
    *,
    label: str,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": True, "status": "not_supplied", "label": label, "data": {}}
    loaded = _load_json(path, label=label)
    if loaded.get("ok") is False:
        if loaded.get("status") == "missing":
            return {**loaded, "ok": True, "data": {}}
        return loaded
    payload = _dict(loaded.get("data"))
    warnings: list[dict[str, Any]] = []
    if payload.get(type_field) != expected_type:
        warnings.append(
            _warning("unexpected_source_type", f"{label}.{type_field}", payload.get(type_field))
        )
    if payload.get(version_field) != expected_version:
        warnings.append(
            _warning(
                "unexpected_source_version",
                f"{label}.{version_field}",
                payload.get(version_field),
            )
        )
    return {
        "ok": True,
        "status": "loaded",
        "label": label,
        "path": str(Path(path)),
        "data": payload,
        "warnings": warnings,
    }


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {
            "ok": False,
            "status": "missing",
            "label": label,
            "path": str(file_path),
            "error": f"{label} not found: {file_path}",
        }
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(file_path),
            "error": str(exc),
        }
    return {
        "ok": True,
        "status": "loaded",
        "label": label,
        "path": str(file_path),
        "data": data,
    }


def _source_statuses(sources: dict[str, dict[str, Any]]) -> dict[str, str]:
    return {
        key: (
            "loaded"
            if source.get("status") == "loaded"
            else "missing"
            if source.get("status") == "missing"
            else "not_supplied"
            if source.get("status") == "not_supplied"
            else "invalid"
            if source.get("ok") is False
            else str(source.get("status") or "unknown")
        )
        for key, source in sources.items()
    }


def _source_warnings(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for label, source in sources.items():
        status = source.get("status")
        if status == "missing":
            warnings.append(_warning("source_path_missing", label, source.get("path")))
        elif status == "not_supplied":
            warnings.append(_warning("source_not_supplied", label, None))
        elif source.get("ok") is False:
            warnings.append(_warning("source_invalid", label, source.get("error")))
        for warning in _list(source.get("warnings")):
            if isinstance(warning, dict):
                warnings.append(warning)
    return warnings


def _known_limitations(
    *,
    profile_count: int,
    source_warnings: list[dict[str, Any]],
) -> list[str]:
    limitations = [
        "The profile summarizes existing camera-geometry provenance only.",
        "The profile does not create calibration evidence or projection diagnostics.",
        "Structural readiness is not calibration validity.",
        "Human review flags are routing signals for future review surfaces.",
        "The report does not modify replay, manifests, matrices, or baselines.",
    ]
    if profile_count == 0:
        limitations.append("No manifest-backed points were available to profile.")
    if source_warnings:
        limitations.append("One or more optional source artifacts were missing or partial.")
    return limitations


def _profile_id(entries: list[dict[str, Any]]) -> str:
    identity = [
        {
            "point_manifest_id": entry.get("point_manifest_id"),
            "media_id": entry.get("media_id"),
            "camera_geometry_id": entry.get("camera_geometry_id"),
            "trajectory_3d_run_id": entry.get("trajectory_3d_run_id"),
        }
        for entry in entries
    ]
    digest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return f"camera_geometry_calibration_profile_v1_{digest}"


def _profile_entry_id(point: dict[str, Any]) -> str:
    identity = {
        "point_manifest_id": _string_or_none(point.get("point_manifest_id")),
        "media_id": _string_or_none(point.get("media_id")),
        "camera_geometry_id": _string_dict(point.get("associated_run_ids")).get(
            "camera_geometry_id"
        ),
    }
    digest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return f"camera_geometry_profile_v1_{digest}"


def _point_key(item: dict[str, Any]) -> str:
    for key in ("point_manifest_id", "corpus_entry_id", "media_id"):
        value = _string_or_none(item.get(key))
        if value:
            return value
    return hashlib.sha256(
        json.dumps(item, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _point_sort_key(item: dict[str, Any]) -> tuple[str, str, str]:
    labels = ",".join(_string_list(item.get("labels")))
    protected_sort = "0" if "protected_sample_point" in labels else "1"
    return (
        protected_sort,
        _string_or_none(item.get("media_id")) or "",
        _string_or_none(item.get("point_manifest_id")) or "",
    )


def _entry_source_paths(
    *,
    point: dict[str, Any],
    source_paths: dict[str, Any],
) -> dict[str, Any]:
    return {
        "point_manifest_path": _string_or_none(point.get("point_manifest_path"))
        or _string_or_none(point.get("manifest_path")),
        "multi_point_replay_index_path": source_paths.get("replay_index_path"),
        "multi_point_regression_matrix_path": source_paths.get("regression_matrix_path"),
        "versioned_dataset_corpus_manifest_path": source_paths.get("corpus_manifest_path"),
        "label_feedback_evaluation_inputs_path": source_paths.get(
            "label_feedback_inputs_path"
        ),
    }


def _review_refs(feedback_entry: dict[str, Any] | None) -> dict[str, Any]:
    feedback = _dict(feedback_entry)
    return {
        "review_label_bundle_refs": _list(feedback.get("review_label_bundle_refs")),
        "reviewer_confidence_bundle_refs": _list(
            feedback.get("reviewer_confidence_bundle_refs")
        ),
        "multi_reviewer_review_set_refs": _list(
            feedback.get("multi_reviewer_review_set_refs")
        ),
        "disagreement_report_refs": _list(feedback.get("disagreement_report_refs")),
        "structural_review_artifact_available": bool(
            _list(feedback.get("review_label_bundle_refs"))
            or _list(feedback.get("reviewer_confidence_bundle_refs"))
            or _list(feedback.get("multi_reviewer_review_set_refs"))
        ),
    }


def _feedback_ref(feedback_entry: dict[str, Any] | None) -> dict[str, Any]:
    feedback = _dict(feedback_entry)
    return {
        "feedback_entry_id": _string_or_none(feedback.get("feedback_entry_id")),
        "evaluation_signal_type": _string_or_none(feedback.get("evaluation_signal_type")),
        "evaluation_signal_status": _string_or_none(
            feedback.get("evaluation_signal_status")
        ),
        "evaluation_harness_actions": _string_list(
            feedback.get("evaluation_harness_actions")
        ),
        "requires_human_review": feedback.get("requires_human_review") is True,
    }


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS:
                errors.append(_error("forbidden_field", child_path, key))
            errors.extend(_forbidden_field_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_field_errors(nested, path=f"{path}[{index}]"))
    return errors


def _forbidden_value_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            errors.extend(_forbidden_value_errors(nested, path=f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_value_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS:
        errors.append(_error("forbidden_value", path, value))
    return errors


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _warning(warning_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"warning_type": warning_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CAMERA_GEOMETRY_CALIBRATION_BLUEPRINT,
        "blueprint_name": CAMERA_GEOMETRY_CALIBRATION_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _first_string(*values: Any) -> str | None:
    for value in values:
        text = _string_or_none(value)
        if text is not None:
            return text
    return None


def _string_list(value: Any) -> list[str]:
    return [str(item) for item in _list(value) if _string_or_none(item) is not None]


def _string_dict(value: Any) -> dict[str, str]:
    return {
        str(key): str(item)
        for key, item in _dict(value).items()
        if _string_or_none(item) is not None
    }


def _bool_dict(value: Any) -> dict[str, bool]:
    return {str(key): bool(item) for key, item in _dict(value).items()}


def _int_dict(value: Any) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, item in _dict(value).items():
        try:
            result[str(key)] = int(item)
        except (TypeError, ValueError):
            continue
    return result


def _count_value(counts: dict[str, int], key: str) -> int:
    return max(int(counts.get(key, 0)), 0)


def _path_or_none(path: str | Path | None) -> str | None:
    if path is None or not str(path).strip():
        return None
    return str(Path(path))
