from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.camera_geometry_calibration_provenance import (
    CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
)
from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gate_pathway_completion_freeze import (
    GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
    GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gate_review_dataset_export import (
    GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_many_point_smoke import (
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_perception_execution import (
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_segment_replay_review import (
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
)
from apps.worker.services.intennse_label_alignment import (
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.label_feedback_evaluation import (
    LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
)
from apps.worker.services.many_point_ingestion_gate import (
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)
from apps.worker.services.multi_point_regression_matrix import (
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_reviewer_disagreement import (
    MULTI_REVIEWER_SCHEMA_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    OBSERVATION_QUALITY_TAXONOMY_VERSION,
)
from apps.worker.services.point_manifest import POINT_MANIFEST_VERSION
from apps.worker.services.real_broadcast_gameplay_gate_corpus_run import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
)
from apps.worker.services.review_label_schema import REVIEW_LABEL_SCHEMA_VERSION
from apps.worker.services.review_ops_metrics import REVIEW_OPS_METRICS_CONTRACT_VERSION
from apps.worker.services.reviewer_confidence_schema import (
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
)
from apps.worker.services.tom_v3_expansion_completion_freeze import (
    TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_CONTRACT_VERSION,
)

REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE = (
    "real_broadcast_gameplay_review_loop_contract"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE = (
    "real_broadcast_gameplay_review_bundle"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_TYPE = (
    "real_broadcast_gameplay_review_bundle_validation"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE = (
    "real_broadcast_gameplay_review_loop_report"
)
REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_TYPE = (
    "real_broadcast_gameplay_human_review_readiness_report"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_BLUEPRINT = "blueprint_47"
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_BLUEPRINT_NAME = (
    "real_broadcast_gameplay_review_loop_v1"
)

DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT = (
    ".data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_bundle.template.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_bundle.validation.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_loop_report.current.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_human_review_readiness_report.current.json"
)

REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

ALLOWED_REVIEWED_SEGMENT_STATUSES = {
    "not_reviewed",
    "reviewed_as_gameplay_candidate",
    "reviewed_as_non_gameplay_candidate",
    "reviewed_as_uncertain",
    "needs_additional_review",
    "not_applicable",
}
ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES = {
    "no_review_decision",
    "reviewer_would_allow_downstream_observation",
    "reviewer_would_block_downstream_observation",
    "reviewer_requests_additional_review",
    "not_applicable",
}
ALLOWED_REVIEW_CONFIDENCE_VALUES = {
    "not_assessed",
    "low",
    "medium",
    "high",
    "not_applicable",
}
ALLOWED_AMBIGUITY_FLAGS = {
    "broadcast_replay_possible",
    "commercial_or_graphic_possible",
    "crowd_or_bench_cutaway_possible",
    "player_closeup_possible",
    "bench_or_coach_shot_possible",
    "changeover_possible",
    "interview_possible",
    "warmup_or_practice_possible",
    "camera_cut_unclear",
    "short_segment_unclear",
    "classifier_boundary_unclear",
    "expected_tag_unclear",
    "not_applicable",
}
ALLOWED_REVIEW_SOURCE_VALUES = {
    "replay_workstation",
    "exported_bundle",
    "manual_json_review",
    "external_review_tool",
    "not_assessed",
    "not_applicable",
}
ALLOWED_PROVENANCE_STATUSES = {
    "source_artifacts_available",
    "partial_source_context",
    "missing_source_context",
}

FORBIDDEN_REVIEW_LOOP_TOKENS = {
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
    "true",
    "false",
    "true_gameplay",
    "false_gameplay",
    "confirmed_gameplay",
    "point_truth",
    "event_truth",
    "rally_truth",
    "line_call_truth",
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "training_truth",
    "model_ready_truth",
    "generalization_proven",
    "production_ready_truth",
    "classifier_accuracy_claim",
    "reviewer_score",
    "reviewer_rank",
}

REVIEW_LOOP_WARNINGS = {
    "review_loop_is_not_truth": True,
    "gameplay_gate_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_assessed": True,
    "expected_tags_are_not_truth": True,
    "review_metadata_is_not_training_truth": True,
    "human_review_required": True,
    "automatic_relabeling_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "model_assets_are_not_mutated": True,
    "regression_baselines_are_not_mutated": True,
    "review_values_do_not_modify_source_artifacts": True,
}

ENTRY_WARNINGS = {
    "human_review_metadata_only": True,
    "review_entry_is_not_truth": True,
    "expected_tags_are_not_truth": True,
    "classifier_statuses_are_evidence_only": True,
    "automatic_relabeling_not_performed": True,
}

NON_CLAIMS = {
    "not_point_detection": True,
    "not_scoring": True,
    "not_line_calling": True,
    "not_gameplay_ground_truth": True,
    "not_classifier_correctness_benchmark": True,
    "not_classifier_accuracy_benchmark": True,
    "not_generalization_claim": True,
    "not_production_readiness_claim": True,
    "not_training_label_source": True,
    "not_automatic_relabeling": True,
}

SOURCE_CONTRACT_REFS = {
    "real_broadcast_gameplay_corpus_run_contract_version": (
        REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION
    ),
    "gameplay_gate_review_dataset_export_contract_version": (
        GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION
    ),
    "gameplay_gate_pathway_completion_freeze_version": (
        GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION
    ),
    "gameplay_gate_regression_baseline_contract_version": (
        GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION
    ),
    "gameplay_segment_replay_review_contract_version": (
        GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION
    ),
    "gameplay_gated_many_point_smoke_contract_version": (
        GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION
    ),
    "gameplay_gated_perception_execution_contract_version": (
        GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
    ),
    "gameplay_gated_pipeline_routing_contract_version": (
        GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
    ),
    "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
    "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
    "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
    "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
    "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
    "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
    "versioned_dataset_corpus_contract_version": DATASET_CORPUS_CONTRACT_VERSION,
    "coverage_sampling_strategy_contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
    "review_ops_metrics_contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
    "label_feedback_evaluation_contract_version": LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
    "camera_geometry_calibration_provenance_contract_version": (
        CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION
    ),
    "tom_v3_expansion_completion_freeze_version": (
        TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION
    ),
    "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
    "point_manifest_version": POINT_MANIFEST_VERSION,
}


def export_real_broadcast_gameplay_review_loop_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION,
        "review_bundle_type": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE,
        "review_bundle_version": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION,
        "contract": contract,
        "warnings": dict(REVIEW_LOOP_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_real_broadcast_gameplay_review_bundle_template(
    *,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT,
    source_corpus_run_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    source_review_dataset_path: str | Path | None = None,
    source_replay_timeline_path: str | Path | None = None,
    source_routing_plan_path: str | Path | None = None,
    source_execution_plan_path: str | Path | None = None,
    source_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if errors:
        bundle = _empty_bundle(
            generated_at=generated_at,
            source_corpus_run_path=source_corpus_run_path,
            source_review_dataset_path=source_review_dataset_path,
            source_replay_timeline_path=source_replay_timeline_path,
            source_routing_plan_path=source_routing_plan_path,
            source_execution_plan_path=source_execution_plan_path,
            source_regression_baseline_path=source_regression_baseline_path,
            model_asset_path=model_asset_path,
            entries=[],
        )
        return _write_bundle_result(
            bundle=bundle,
            output_path=output_path,
            ok=False,
            status="invalid_contract",
            errors=errors,
        )

    source_contexts = _collect_source_contexts(
        source_corpus_run_path=source_corpus_run_path,
        source_review_dataset_path=source_review_dataset_path,
    )
    entries = [
        _review_entry_from_dataset_entry(
            dataset_entry=dataset_entry,
            dataset=dataset,
            corpus_entry=corpus_entry,
            source_dataset_path=dataset_path,
            source_corpus_run_path=source_corpus_run_path,
        )
        for dataset, corpus_entry, dataset_path in source_contexts
        for dataset_entry in _list(dataset.get("entries"))
        if isinstance(dataset_entry, dict)
    ]
    bundle = _empty_bundle(
        generated_at=generated_at,
        source_corpus_run_path=source_corpus_run_path,
        source_review_dataset_path=source_review_dataset_path,
        source_replay_timeline_path=source_replay_timeline_path,
        source_routing_plan_path=source_routing_plan_path,
        source_execution_plan_path=source_execution_plan_path,
        source_regression_baseline_path=source_regression_baseline_path,
        model_asset_path=model_asset_path,
        entries=entries,
    )
    bundle["source_contract_refs"] = dict(SOURCE_CONTRACT_REFS)
    bundle["summary"] = _bundle_summary(entries)
    return _write_bundle_result(
        bundle=bundle,
        output_path=output_path,
        ok=True,
        status="completed",
        errors=[],
    )


def validate_real_broadcast_gameplay_review_bundle(
    *,
    bundle_path: str | Path,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    bundle = _load_required_json(bundle_path, "real_broadcast_gameplay_review_bundle", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if bundle:
        errors.extend(_validate_bundle_shape(bundle))
        errors.extend(_validate_source_contract_refs(bundle))
        errors.extend(_forbidden_token_errors(bundle, path="review_bundle"))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_TYPE,
        "validation_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "bundle_path": str(Path(bundle_path)),
        "contract_type": contract.get("contract_type") if contract else None,
        "contract_version": contract.get("contract_version") if contract else None,
        "review_bundle_type": bundle.get("review_bundle_type") if bundle else None,
        "review_bundle_version": bundle.get("review_bundle_version") if bundle else None,
        "review_bundle_entry_count": len(_list(bundle.get("entries"))) if bundle else 0,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(REVIEW_LOOP_WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed review metadata values, provenance refs, "
            "and exact forbidden tokens.",
            "Validation does not infer review metadata.",
            "Validation does not assess classifier correctness.",
            "Validation does not create event labels or point labels.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_real_broadcast_gameplay_review_loop_report(
    *,
    bundle_path: str | Path,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    bundle_load_errors: list[dict[str, Any]] = []
    bundle = _load_required_json(
        bundle_path,
        "real_broadcast_gameplay_review_bundle",
        bundle_load_errors,
    )
    validation = validate_real_broadcast_gameplay_review_bundle(
        bundle_path=bundle_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if bundle_load_errors or validation.get("ok") is False:
        result = {
            "ok": False,
            "status": "invalid_review_bundle",
            "report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE,
            "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
            "error_count": len(bundle_load_errors) + int(validation.get("error_count") or 0),
            "errors": bundle_load_errors + _list(validation.get("errors")),
            "warnings": dict(REVIEW_LOOP_WARNINGS),
        }
        _write_json_if_requested(output_path, result, result, "report_output")
        return result

    entries = [entry for entry in _list(bundle.get("entries")) if isinstance(entry, dict)]
    report = {
        "report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_bundle_path": str(Path(bundle_path)),
        "review_bundle_id": bundle.get("review_bundle_id"),
        "review_bundle_version": bundle.get("review_bundle_version"),
        "review_bundle_entry_count": len(entries),
        "summary": _review_loop_report_summary(entries),
        "model_asset_provenance": _model_asset_provenance_from_bundle(bundle),
        "status_distributions": {
            "reviewed_segment_status": _human_counter(
                entries,
                "reviewed_segment_status",
            ),
            "reviewed_downstream_gate_status": _human_counter(
                entries,
                "reviewed_downstream_gate_status",
            ),
            "review_confidence": _human_counter(entries, "review_confidence"),
            "review_source": _human_counter(entries, "review_source"),
            "segment_status": _counter(entries, "segment_status"),
            "downstream_gate_status": _counter(entries, "downstream_gate_status"),
        },
        "ambiguity_flag_counts": _ambiguity_flag_counts(entries),
        "missing_review_field_counts": _missing_review_field_counts(entries),
        "validation_snapshot": validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **dict(REVIEW_LOOP_WARNINGS),
            **_dict(bundle.get("warnings")),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
        "review_bundle_id": bundle.get("review_bundle_id"),
        "review_bundle_entry_count": len(entries),
        "summary": report["summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def build_real_broadcast_gameplay_human_review_readiness_report(
    *,
    bundle_path: str | Path,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    bundle_load_errors: list[dict[str, Any]] = []
    bundle = _load_required_json(
        bundle_path,
        "real_broadcast_gameplay_review_bundle",
        bundle_load_errors,
    )
    validation = validate_real_broadcast_gameplay_review_bundle(
        bundle_path=bundle_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if bundle_load_errors or validation.get("ok") is False:
        result = {
            "ok": False,
            "status": "invalid_review_bundle",
            "report_type": REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_TYPE,
            "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
            "error_count": len(bundle_load_errors) + int(validation.get("error_count") or 0),
            "errors": bundle_load_errors + _list(validation.get("errors")),
            "warnings": dict(REVIEW_LOOP_WARNINGS),
        }
        _write_json_if_requested(output_path, result, result, "report_output")
        return result

    entries = [entry for entry in _list(bundle.get("entries")) if isinstance(entry, dict)]
    readiness = {
        "ready_for_human_review": bool(entries)
        and all(_string_or_none(entry.get("replay_url")) for entry in entries),
        "review_bundle_entry_count": len(entries),
        "review_pending_count": sum(
            1
            for entry in entries
            if _dict(entry.get("human_review")).get("reviewed_segment_status")
            == "not_reviewed"
        ),
        "needs_additional_review_count": _needs_additional_review_count(entries),
        "entries_with_replay_url_count": sum(
            1 for entry in entries if _string_or_none(entry.get("replay_url")) is not None
        ),
        "entries_with_timestamp_context_count": sum(
            1
            for entry in entries
            if entry.get("segment_start_ms") is not None
            and entry.get("segment_end_ms") is not None
        ),
        "human_review_required": True,
        "readiness_is_not_correctness": True,
        "review_loop_is_not_truth": True,
        "classifier_correctness_not_assessed": True,
    }
    report = {
        "report_type": REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_bundle_path": str(Path(bundle_path)),
        "review_bundle_id": bundle.get("review_bundle_id"),
        "readiness": readiness,
        "model_asset_provenance": _model_asset_provenance_from_bundle(bundle),
        "validation_snapshot": validation,
        "warnings": {
            **dict(REVIEW_LOOP_WARNINGS),
            **_dict(bundle.get("warnings")),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "report_type": REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
        "review_bundle_id": bundle.get("review_bundle_id"),
        "readiness": readiness,
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "review_loop_scope": {
            "purpose": "real_broadcast_gameplay_human_review_loop",
            "reads_real_broadcast_corpus_run_report": True,
            "reads_gameplay_gate_review_dataset_export": True,
            "reads_replay_timeline_when_supplied": True,
            "reads_routing_and_execution_context_when_supplied": True,
            "reads_regression_baseline_context_when_supplied": True,
            "captures_human_review_metadata": True,
            "creates_review_labels": False,
            "automatic_relabeling_allowed": False,
            "runs_gpu_or_model_inference": False,
            "mutates_model_assets": False,
            "mutates_regression_baselines": False,
            "scores_classifier": False,
            "creates_tennis_conclusions": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "review_bundle_template_schema": {
            "review_bundle_type": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE,
            "review_bundle_version": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION,
            "entries_derived_from_existing_reviewable_segments": True,
            "human_review_fields_start_blank_or_not_assessed": True,
            "preserves_replay_urls_and_timestamps": True,
            "preserves_classifier_probabilities_as_evidence": True,
            "preserves_expected_tags_as_operator_context": True,
        },
        "review_bundle_schema": {
            "required_fields": [
                "review_bundle_id",
                "review_bundle_version",
                "generated_at",
                "source_corpus_run_path",
                "source_review_dataset_path",
                "source_replay_timeline_path",
                "source_routing_plan_path",
                "source_execution_plan_path",
                "source_regression_baseline_path",
                "model_asset_ref",
                "model_asset_sha256",
                "entries",
                "summary",
                "warnings",
                "non_claims",
            ],
        },
        "review_entry_schema": {
            "required_fields": [
                "review_entry_id",
                "corpus_entry_id",
                "review_dataset_entry_id",
                "media_id",
                "source_media_path",
                "source_label",
                "replay_url",
                "segment_id",
                "segment_start_ms",
                "segment_end_ms",
                "start_frame_index",
                "end_frame_index",
                "expected_broadcast_content_tags",
                "gameplay_probability",
                "non_gameplay_probability",
                "raw_status",
                "smoothed_status",
                "segment_status",
                "downstream_gate_status",
                "routing_decision",
                "execution_decision",
                "replay_timeline_entry_id",
                "baseline_context",
                "review_context",
                "human_review",
                "provenance_status",
                "warnings",
            ],
            "allowed_reviewed_segment_statuses": sorted(
                ALLOWED_REVIEWED_SEGMENT_STATUSES
            ),
            "allowed_reviewed_downstream_gate_statuses": sorted(
                ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES
            ),
            "allowed_review_confidence_values": sorted(ALLOWED_REVIEW_CONFIDENCE_VALUES),
            "allowed_ambiguity_flags": sorted(ALLOWED_AMBIGUITY_FLAGS),
            "allowed_review_source_values": sorted(ALLOWED_REVIEW_SOURCE_VALUES),
        },
        "review_loop_report_schema": {
            "report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_TYPE,
            "report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_VERSION,
            "summarizes_human_review_metadata": True,
            "summarizes_missing_review_fields": True,
            "summarizes_model_asset_provenance": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_review_bundle_template_shape": True,
            "validate_review_bundle_shape": True,
            "validate_review_entry_shape": True,
            "validate_allowed_statuses": True,
            "validate_allowed_confidence_values": True,
            "validate_allowed_ambiguity_flags": True,
            "validate_allowed_review_source_values": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "source_corpus_run_path_recorded_when_supplied": True,
            "source_review_dataset_path_recorded_when_supplied": True,
            "segment_id_required": True,
            "replay_url_required": True,
            "timestamp_context_preserved": True,
            "model_asset_provenance_preserved": True,
            "baseline_context_preserved_when_available": True,
            "expected_broadcast_content_tags_preserved": True,
            "warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(REVIEW_LOOP_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _collect_source_contexts(
    *,
    source_corpus_run_path: str | Path | None,
    source_review_dataset_path: str | Path | None,
) -> list[tuple[dict[str, Any], dict[str, Any], str]]:
    contexts: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    if source_review_dataset_path is not None:
        dataset = _load_optional_json(source_review_dataset_path, "source_review_dataset")
        if dataset:
            contexts.append((dataset, {}, str(Path(source_review_dataset_path))))

    corpus_run = (
        _load_optional_json(source_corpus_run_path, "source_corpus_run")
        if source_corpus_run_path is not None
        else {}
    )
    for corpus_entry in _list(corpus_run.get("entries")):
        if not isinstance(corpus_entry, dict):
            continue
        outputs = _dict(corpus_entry.get("artifact_outputs"))
        dataset_path = _string_or_none(outputs.get("gameplay_review_dataset_export"))
        if dataset_path is None:
            continue
        if (
            source_review_dataset_path is not None
            and str(source_review_dataset_path) == dataset_path
        ):
            continue
        dataset = _load_optional_json(dataset_path, "corpus_entry_review_dataset")
        if dataset:
            contexts.append((dataset, corpus_entry, dataset_path))
    return contexts


def _review_entry_from_dataset_entry(
    *,
    dataset_entry: dict[str, Any],
    dataset: dict[str, Any],
    corpus_entry: dict[str, Any],
    source_dataset_path: str,
    source_corpus_run_path: str | Path | None,
) -> dict[str, Any]:
    corpus_entry_id = corpus_entry.get("corpus_entry_id") or "standalone_review_dataset"
    review_dataset_entry_id = dataset_entry.get("review_entry_id")
    human_review = _default_human_review()
    return {
        "review_entry_id": _stable_id(
            "real_broadcast_gameplay_review_entry_v1",
            corpus_entry_id,
            review_dataset_entry_id,
            dataset_entry.get("segment_id"),
        ),
        "corpus_entry_id": corpus_entry_id,
        "review_dataset_entry_id": review_dataset_entry_id,
        "media_id": dataset_entry.get("media_id") or dataset.get("media_id"),
        "source_media_path": (
            corpus_entry.get("local_media_path")
            or dataset_entry.get("source_media_path")
            or dataset.get("source_media_path")
        ),
        "source_label": corpus_entry.get("source_label") or "standalone_review_dataset",
        "replay_url": dataset_entry.get("replay_url") or dataset.get("replay_url"),
        "segment_id": dataset_entry.get("segment_id"),
        "segment_start_ms": dataset_entry.get("segment_start_ms"),
        "segment_end_ms": dataset_entry.get("segment_end_ms"),
        "start_frame_index": dataset_entry.get("start_frame_index"),
        "end_frame_index": dataset_entry.get("end_frame_index"),
        "expected_broadcast_content_tags": _string_list(
            corpus_entry.get("expected_broadcast_content_tags")
        ),
        "gameplay_probability": dataset_entry.get("gameplay_probability"),
        "non_gameplay_probability": dataset_entry.get("non_gameplay_probability"),
        "raw_status": dataset_entry.get("raw_status"),
        "smoothed_status": dataset_entry.get("smoothed_status"),
        "segment_status": dataset_entry.get("segment_status"),
        "downstream_gate_status": dataset_entry.get("downstream_gate_status"),
        "routing_decision": dataset_entry.get("routing_decision"),
        "execution_decision": dataset_entry.get("execution_decision"),
        "replay_timeline_entry_id": dataset_entry.get("replay_timeline_entry_id"),
        "baseline_context": _dict(
            dataset_entry.get("baseline_context") or dataset.get("baseline_context")
        ),
        "review_context": {
            "source_corpus_run_path": (
                str(Path(source_corpus_run_path)) if source_corpus_run_path else None
            ),
            "source_review_dataset_path": source_dataset_path,
            "source_review_dataset_id": dataset.get("dataset_id"),
            "source_review_dataset_version": dataset.get("dataset_version"),
            "source_artifacts_are_existing_outputs": True,
            "review_metadata_only": True,
        },
        "human_review": human_review,
        "provenance_status": dataset_entry.get("provenance_status")
        or "partial_source_context",
        "warnings": {
            **dict(ENTRY_WARNINGS),
            **_dict(dataset_entry.get("warnings")),
        },
    }


def _empty_bundle(
    *,
    generated_at: datetime,
    source_corpus_run_path: str | Path | None,
    source_review_dataset_path: str | Path | None,
    source_replay_timeline_path: str | Path | None,
    source_routing_plan_path: str | Path | None,
    source_execution_plan_path: str | Path | None,
    source_regression_baseline_path: str | Path | None,
    model_asset_path: str | Path,
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    model_asset = _model_asset_ref(model_asset_path)
    source_paths = [
        source_corpus_run_path,
        source_review_dataset_path,
        source_replay_timeline_path,
        source_routing_plan_path,
        source_execution_plan_path,
        source_regression_baseline_path,
    ]
    bundle_id = _stable_id(
        "real_broadcast_gameplay_review_bundle_v1",
        [str(Path(path)) if path is not None else None for path in source_paths],
        len(entries),
        model_asset.get("model_asset_sha256"),
    )
    return {
        "review_bundle_id": bundle_id,
        "review_bundle_type": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE,
        "review_bundle_version": REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_corpus_run_path": (
            str(Path(source_corpus_run_path)) if source_corpus_run_path else None
        ),
        "source_review_dataset_path": (
            str(Path(source_review_dataset_path)) if source_review_dataset_path else None
        ),
        "source_replay_timeline_path": (
            str(Path(source_replay_timeline_path)) if source_replay_timeline_path else None
        ),
        "source_routing_plan_path": (
            str(Path(source_routing_plan_path)) if source_routing_plan_path else None
        ),
        "source_execution_plan_path": (
            str(Path(source_execution_plan_path)) if source_execution_plan_path else None
        ),
        "source_regression_baseline_path": (
            str(Path(source_regression_baseline_path))
            if source_regression_baseline_path
            else None
        ),
        "model_asset_ref": model_asset.get("model_asset_ref"),
        "model_asset_sha256": model_asset.get("model_asset_sha256"),
        "model_asset_exists": model_asset.get("model_asset_exists"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "entries": entries,
        "summary": _bundle_summary(entries),
        "warnings": dict(REVIEW_LOOP_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }


def _default_human_review() -> dict[str, Any]:
    return {
        "reviewer_id": None,
        "reviewed_at": None,
        "reviewed_segment_status": "not_reviewed",
        "reviewed_downstream_gate_status": "no_review_decision",
        "review_confidence": "not_assessed",
        "ambiguity_flags": [],
        "reviewer_notes": None,
        "needs_additional_review": False,
        "review_duration_seconds": None,
        "review_source": "not_assessed",
    }


def _bundle_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "review_bundle_entry_count": len(entries),
        "review_pending_count": sum(
            1
            for entry in entries
            if _dict(entry.get("human_review")).get("reviewed_segment_status")
            == "not_reviewed"
        ),
        "reviewable_segment_count": len(entries),
        "entries_with_replay_url_count": sum(
            1 for entry in entries if _string_or_none(entry.get("replay_url")) is not None
        ),
        "entries_with_timestamp_context_count": sum(
            1
            for entry in entries
            if entry.get("segment_start_ms") is not None
            and entry.get("segment_end_ms") is not None
        ),
        "expected_broadcast_content_tag_counts": dict(
            sorted(
                Counter(
                    tag
                    for entry in entries
                    for tag in _string_list(
                        entry.get("expected_broadcast_content_tags")
                    )
                ).items()
            )
        ),
        "classifier_correctness_not_assessed": True,
        "review_loop_is_not_truth": True,
        "automatic_relabeling_not_performed": True,
    }


def _review_loop_report_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    human_status_counts = _human_counter(entries, "reviewed_segment_status")
    downstream_status_counts = _human_counter(entries, "reviewed_downstream_gate_status")
    return {
        "review_bundle_entry_count": len(entries),
        "reviewed_entry_count": sum(
            count
            for status, count in human_status_counts.items()
            if status
            not in {
                "not_reviewed",
                "not_applicable",
            }
        ),
        "unreviewed_entry_count": human_status_counts.get("not_reviewed", 0),
        "needs_additional_review_count": _needs_additional_review_count(entries),
        "reviewed_as_gameplay_candidate_count": human_status_counts.get(
            "reviewed_as_gameplay_candidate",
            0,
        ),
        "reviewed_as_non_gameplay_candidate_count": human_status_counts.get(
            "reviewed_as_non_gameplay_candidate",
            0,
        ),
        "reviewed_as_uncertain_count": human_status_counts.get(
            "reviewed_as_uncertain",
            0,
        ),
        "downstream_allow_review_count": downstream_status_counts.get(
            "reviewer_would_allow_downstream_observation",
            0,
        ),
        "downstream_block_review_count": downstream_status_counts.get(
            "reviewer_would_block_downstream_observation",
            0,
        ),
        "ambiguity_flag_counts": _ambiguity_flag_counts(entries),
        "confidence_distribution": _human_counter(entries, "review_confidence"),
        "missing_review_field_counts": _missing_review_field_counts(entries),
        "classifier_correctness_not_assessed": True,
        "review_loop_is_not_truth": True,
        "automatic_relabeling_not_performed": True,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "review_loop_scope",
        "source_contract_refs",
        "review_bundle_template_schema",
        "review_bundle_schema",
        "review_entry_schema",
        "review_loop_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    refs = _dict(contract.get("source_contract_refs"))
    for key, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _validate_bundle_shape(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if bundle.get("review_bundle_type") != REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TYPE:
        errors.append(
            _error(
                "invalid_review_bundle_type",
                "review_bundle_type",
                bundle.get("review_bundle_type"),
            )
        )
    if bundle.get("review_bundle_version") != REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VERSION:
        errors.append(
            _error(
                "invalid_review_bundle_version",
                "review_bundle_version",
                bundle.get("review_bundle_version"),
            )
        )
    for field in (
        "review_bundle_id",
        "review_bundle_version",
        "generated_at",
        "source_corpus_run_path",
        "source_review_dataset_path",
        "source_replay_timeline_path",
        "source_routing_plan_path",
        "source_execution_plan_path",
        "source_regression_baseline_path",
        "model_asset_ref",
        "model_asset_sha256",
        "entries",
        "summary",
        "warnings",
        "non_claims",
    ):
        if field not in bundle:
            errors.append(_error("missing_review_bundle_field", field, None))
    entries = bundle.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("entries_must_be_list", "entries", entries))
        return errors
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_review_entry", f"entries[{index}]", entry))
            continue
        errors.extend(_validate_review_entry(entry=entry, index=index))
    return errors


def _validate_review_entry(
    *,
    entry: dict[str, Any],
    index: int,
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in (
        "review_entry_id",
        "corpus_entry_id",
        "review_dataset_entry_id",
        "media_id",
        "source_media_path",
        "source_label",
        "replay_url",
        "segment_id",
        "segment_start_ms",
        "segment_end_ms",
        "start_frame_index",
        "end_frame_index",
        "expected_broadcast_content_tags",
        "gameplay_probability",
        "non_gameplay_probability",
        "raw_status",
        "smoothed_status",
        "segment_status",
        "downstream_gate_status",
        "routing_decision",
        "execution_decision",
        "replay_timeline_entry_id",
        "baseline_context",
        "review_context",
        "human_review",
        "provenance_status",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_review_entry_field", f"entries[{index}].{field}", None))
    expected_tags = entry.get("expected_broadcast_content_tags")
    if not isinstance(expected_tags, list):
        errors.append(
            _error(
                "expected_broadcast_content_tags_must_be_list",
                f"entries[{index}].expected_broadcast_content_tags",
                expected_tags,
            )
        )
    provenance_status = entry.get("provenance_status")
    if provenance_status not in ALLOWED_PROVENANCE_STATUSES:
        errors.append(
            _error(
                "invalid_provenance_status",
                f"entries[{index}].provenance_status",
                provenance_status,
            )
        )
    human = _dict(entry.get("human_review"))
    if human.get("reviewed_segment_status") not in ALLOWED_REVIEWED_SEGMENT_STATUSES:
        errors.append(
            _error(
                "invalid_reviewed_segment_status",
                f"entries[{index}].human_review.reviewed_segment_status",
                human.get("reviewed_segment_status"),
            )
        )
    if (
        human.get("reviewed_downstream_gate_status")
        not in ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES
    ):
        errors.append(
            _error(
                "invalid_reviewed_downstream_gate_status",
                f"entries[{index}].human_review.reviewed_downstream_gate_status",
                human.get("reviewed_downstream_gate_status"),
            )
        )
    if human.get("review_confidence") not in ALLOWED_REVIEW_CONFIDENCE_VALUES:
        errors.append(
            _error(
                "invalid_review_confidence",
                f"entries[{index}].human_review.review_confidence",
                human.get("review_confidence"),
            )
        )
    if human.get("review_source") not in ALLOWED_REVIEW_SOURCE_VALUES:
        errors.append(
            _error(
                "invalid_review_source",
                f"entries[{index}].human_review.review_source",
                human.get("review_source"),
            )
        )
    if not isinstance(human.get("needs_additional_review"), bool):
        errors.append(
            _error(
                "needs_additional_review_must_be_boolean",
                f"entries[{index}].human_review.needs_additional_review",
                human.get("needs_additional_review"),
            )
        )
    duration = human.get("review_duration_seconds")
    if duration is not None:
        try:
            if float(duration) < 0:
                errors.append(
                    _error(
                        "review_duration_seconds_must_be_non_negative",
                        f"entries[{index}].human_review.review_duration_seconds",
                        duration,
                    )
                )
        except (TypeError, ValueError):
            errors.append(
                _error(
                    "review_duration_seconds_must_be_number",
                    f"entries[{index}].human_review.review_duration_seconds",
                    duration,
                )
            )
    flags = human.get("ambiguity_flags")
    if not isinstance(flags, list):
        errors.append(
            _error(
                "ambiguity_flags_must_be_list",
                f"entries[{index}].human_review.ambiguity_flags",
                flags,
            )
        )
    else:
        for flag in flags:
            if flag not in ALLOWED_AMBIGUITY_FLAGS:
                errors.append(
                    _error(
                        "invalid_ambiguity_flag",
                        f"entries[{index}].human_review.ambiguity_flags",
                        flag,
                    )
                )
    return errors


def _validate_source_contract_refs(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    refs = _dict(bundle.get("source_contract_refs"))
    errors = []
    for field, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(field) != expected:
            errors.append(_error("invalid_source_contract_ref", field, refs.get(field)))
    return errors


def _model_asset_ref(model_asset_path: str | Path) -> dict[str, Any]:
    path = Path(model_asset_path).expanduser()
    if not path.is_file():
        return {
            "model_asset_ref": str(model_asset_path),
            "model_asset_sha256": None,
            "model_asset_exists": False,
        }
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "model_asset_ref": str(model_asset_path),
        "model_asset_sha256": digest,
        "model_asset_exists": True,
    }


def _model_asset_provenance_from_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_asset_ref": bundle.get("model_asset_ref"),
        "model_asset_sha256": bundle.get("model_asset_sha256"),
        "model_asset_exists": bundle.get("model_asset_exists"),
        "model_assets_are_not_mutated": True,
        "classifier_correctness_not_assessed": True,
    }


def _human_counter(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter(
        str(_dict(entry.get("human_review")).get(field) or "not_assessed")
        for entry in entries
    )
    return dict(sorted(counts.items()))


def _counter(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter(str(entry.get(field) or "not_applicable") for entry in entries)
    return dict(sorted(counts.items()))


def _ambiguity_flag_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        flag
        for entry in entries
        for flag in _string_list(_dict(entry.get("human_review")).get("ambiguity_flags"))
    )
    return dict(sorted(counts.items()))


def _needs_additional_review_count(entries: list[dict[str, Any]]) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("needs_additional_review") is True
        or _dict(entry.get("human_review")).get("reviewed_segment_status")
        == "needs_additional_review"
        or _dict(entry.get("human_review")).get("reviewed_downstream_gate_status")
        == "reviewer_requests_additional_review"
    )


def _missing_review_field_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    for entry in entries:
        human = _dict(entry.get("human_review"))
        if _string_or_none(human.get("reviewer_id")) is None:
            counts["reviewer_id"] += 1
        if _string_or_none(human.get("reviewed_at")) is None:
            counts["reviewed_at"] += 1
        if human.get("reviewed_segment_status") == "not_reviewed":
            counts["reviewed_segment_status"] += 1
        if human.get("reviewed_downstream_gate_status") == "no_review_decision":
            counts["reviewed_downstream_gate_status"] += 1
        if human.get("review_confidence") == "not_assessed":
            counts["review_confidence"] += 1
        if human.get("review_source") == "not_assessed":
            counts["review_source"] += 1
    return dict(sorted(counts.items()))


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    contract = _load_required_json(
        contract_path,
        "real_broadcast_gameplay_review_loop_contract",
        errors,
    )
    return contract


def _load_required_json(
    path: str | Path | None,
    label: str,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    if path is None:
        errors.append(_error("missing_required_path", label, None))
        return {}
    result = _load_json(path, label=label)
    if result.get("ok") is False:
        errors.append(_error("json_load_failed", label, result))
        return {}
    return _dict(result.get("data"))


def _load_optional_json(path: str | Path | None, label: str) -> dict[str, Any]:
    if path is None:
        return {}
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        return {}
    result = _load_json(candidate, label=label)
    if result.get("ok") is False:
        return {}
    return _dict(result.get("data"))


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "status": "missing", "label": label, "path": str(path)}
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(path),
            "message": str(exc),
        }
    if not isinstance(data, dict):
        return {"ok": False, "status": "not_object", "label": label, "path": str(path)}
    return {"ok": True, "status": "loaded", "label": label, "path": str(path), "data": data}


def _write_bundle_result(
    *,
    bundle: dict[str, Any],
    output_path: str | Path | None,
    ok: bool,
    status: str,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    result = {
        "ok": ok,
        "status": status,
        "review_bundle_type": bundle.get("review_bundle_type"),
        "review_bundle_version": bundle.get("review_bundle_version"),
        "review_bundle_id": bundle.get("review_bundle_id"),
        "review_bundle_entry_count": len(_list(bundle.get("entries"))),
        "summary": _dict(bundle.get("summary")),
        "bundle": bundle,
        "error_count": len(errors),
        "errors": errors,
        "warnings": _dict(bundle.get("warnings")) or dict(REVIEW_LOOP_WARNINGS),
    }
    _write_json_if_requested(output_path, bundle, result, "review_bundle_output")
    return result


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None:
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result[result_key] = str(path)


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    _collect_forbidden_token_errors(value=value, path=path, errors=errors)
    return errors


def _collect_forbidden_token_errors(
    *,
    value: Any,
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_REVIEW_LOOP_TOKENS:
                errors.append(_error("forbidden_field_or_value", f"{path}.{key_text}", key_text))
            _collect_forbidden_token_errors(
                value=nested,
                path=f"{path}.{key_text}",
                errors=errors,
            )
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _collect_forbidden_token_errors(
                value=nested,
                path=f"{path}[{index}]",
                errors=errors,
            )
    elif isinstance(value, str) and value in FORBIDDEN_REVIEW_LOOP_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))


def _stable_id(*parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if value is None:
        return []
    return [str(value)]


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "field": field, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "blueprint": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_BLUEPRINT,
        "blueprint_name": REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_BLUEPRINT_NAME,
        "project_version": "0.0.0",
    }
