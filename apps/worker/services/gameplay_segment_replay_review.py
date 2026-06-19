from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_perception_execution import (
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
    GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
    GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
)
from apps.worker.services.gameplay_segment_gate import (
    GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
    GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
)

GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE = (
    "gameplay_segment_replay_review_contract"
)
GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION = "v1"
GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE = "gameplay_segment_replay_timeline"
GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION = "v1"
GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE = "gameplay_segment_review_bundle"
GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION = "v1"
GAMEPLAY_SEGMENT_REVIEW_REPORT_TYPE = "gameplay_segment_review_report"
GAMEPLAY_SEGMENT_REVIEW_REPORT_VERSION = "v1"
GAMEPLAY_SEGMENT_REPLAY_REVIEW_BLUEPRINT = "blueprint_41"
GAMEPLAY_SEGMENT_REPLAY_REVIEW_BLUEPRINT_NAME = (
    "gameplay_segment_replay_timeline_review_v1"
)

DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_segment_replay_review_contract_v1.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REPLAY_TIMELINE_OUTPUT = (
    ".data/exports/gameplay_segment_replay_timeline.current.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_segment_replay_timeline.validation.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REVIEW_TEMPLATE_OUTPUT = (
    ".data/exports/gameplay_segment_review_template.current.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_segment_review_bundle.validation.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REVIEW_REPORT_OUTPUT = (
    ".data/exports/gameplay_segment_review_report.current.json"
)

GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

ALLOWED_LANE_TYPES = {
    "gameplay_segment_candidate",
    "non_gameplay_segment_candidate",
    "uncertain_segment",
    "downstream_allowed",
    "downstream_blocked",
    "downstream_review_required",
    "perception_execution_window",
    "perception_skipped_window",
    "not_applicable",
}

ALLOWED_REVIEW_STATUSES = {
    "not_reviewed",
    "review_optional",
    "review_needed",
    "reviewed_as_gameplay_candidate",
    "reviewed_as_non_gameplay_candidate",
    "reviewed_as_uncertain",
    "needs_additional_review",
    "not_applicable",
}

ALLOWED_PROVENANCE_STATUSES = {
    "gameplay_segment_provenance_available",
    "routing_plan_provenance_available",
    "execution_plan_provenance_available",
    "review_template_provenance_available",
    "missing",
    "not_applicable",
}

FORBIDDEN_REPLAY_REVIEW_TOKENS = {
    "in_out",
    "score",
    "winner",
    "point_winner",
    "player_identity",
    "server",
    "receiver",
    "adjudication",
    "adjudicated",
    "accepted",
    "rejected",
    "correct",
    "incorrect",
    "truth",
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
    "reviewer_score",
    "reviewer_rank",
    "resolved",
}

GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS = {
    "replay_review_surface_only": True,
    "timeline_lane_only": True,
    "candidate_windows_only": True,
    "human_review_metadata_only": True,
    "does_not_claim_classifier_correctness": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_mutate_model_assets": True,
    "does_not_run_gpu_or_model_inference": True,
    "does_not_claim_generalization": True,
    "does_not_claim_automatic_correctness": True,
    "does_not_convert_outputs_into_training_labels": True,
    "no_adjudication": True,
    "observation_only": True,
    "review_support_only": True,
}

SOURCE_CONTRACT_REFS = {
    "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    "gameplay_gated_pipeline_routing_contract_version": (
        GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
    ),
    "gameplay_gated_perception_execution_contract_version": (
        GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
    ),
    "observation_quality_taxonomy_version": "v1",
    "review_label_schema_version": "v1",
    "reviewer_confidence_schema_version": "v1",
    "multi_reviewer_disagreement_schema_version": "v1",
    "intennse_label_alignment_contract_version": "v1",
    "versioned_dataset_corpus_contract_version": "v1",
    "coverage_sampling_strategy_contract_version": "v1",
    "many_point_ingestion_gate_contract_version": "v1",
    "review_ops_metrics_contract_version": "v1",
    "label_feedback_evaluation_contract_version": "v1",
    "camera_geometry_calibration_provenance_contract_version": "v1",
    "tom_v3_expansion_completion_freeze_version": "v1",
    "multi_point_regression_matrix_version": "v0",
    "point_manifest_version": "v0",
}


def export_gameplay_segment_replay_review_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the Blueprint 41 gameplay segment replay/review contract."""

    exported_at = exported_at or GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXPORTED_AT
    contract = {
        "contract_type": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "replay_review_scope": {
            "purpose": "gameplay_segment_replay_timeline_operator_review",
            "reads_gameplay_segment_candidates": True,
            "reads_gameplay_gated_routing_plan_when_supplied": True,
            "reads_gameplay_gated_perception_execution_plan_when_supplied": True,
            "creates_replay_timeline_artifacts": True,
            "creates_review_template_artifacts": True,
            "persists_database_review_notes": False,
            "executes_gpu_or_model_inference": False,
            "writes_observations": False,
            "mutates_regression_baselines": False,
            "mutates_model_assets": False,
            "review_status_is_human_metadata_only": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_contract_artifacts": {
            "gameplay_segment_gate_contract": {
                "contract_type": GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
                "contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
                "candidate_output_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
                "candidate_output_version": GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
            },
            "gameplay_gated_pipeline_routing_contract": {
                "contract_type": GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
                "contract_version": GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
                "plan_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
                "plan_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
            },
            "gameplay_gated_perception_execution_contract": {
                "contract_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE,
                "contract_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
                "plan_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
                "plan_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
            },
        },
        "timeline_lane_schema": {
            "timeline_type": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE,
            "timeline_version": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION,
            "allowed_lane_types": sorted(ALLOWED_LANE_TYPES),
            "allowed_review_statuses": sorted(ALLOWED_REVIEW_STATUSES),
            "allowed_provenance_statuses": sorted(ALLOWED_PROVENANCE_STATUSES),
            "required_entry_fields": [
                "timeline_entry_id",
                "media_id",
                "segment_id",
                "start_ms",
                "end_ms",
                "start_frame_index",
                "end_frame_index",
                "lane_type",
                "segment_status",
                "downstream_gate_status",
                "routing_decision",
                "execution_decision",
                "review_status",
                "display_label",
                "provenance_status",
                "warnings",
            ],
        },
        "review_template_schema": {
            "review_bundle_type": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE,
            "review_bundle_version": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION,
            "optional_human_note_fields": [
                "reviewer_id",
                "reviewed_at",
                "review_note",
            ],
            "review_notes_are_metadata_only": True,
            "reviewer_ids_are_freeform_metadata_only": True,
        },
        "review_bundle_schema": {
            "allowed_review_statuses": sorted(ALLOWED_REVIEW_STATUSES),
            "review_status_does_not_imply_classifier_accuracy": True,
            "review_status_does_not_imply_tennis_meaning": True,
            "review_status_does_not_adjudicate": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_timeline_shape": True,
            "validate_review_template_shape": True,
            "validate_review_bundle_shape": True,
            "validate_allowed_lane_types": True,
            "validate_allowed_review_statuses": True,
            "validate_allowed_provenance_statuses": True,
            "validate_referenced_gameplay_segment_file": True,
            "validate_referenced_routing_plan_when_available": True,
            "validate_referenced_execution_plan_when_available": True,
            "reject_forbidden_exact_tokens": True,
            "structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "timeline_id_required": True,
            "media_id_required": True,
            "replay_url_required": True,
            "gameplay_segment_source_path_required": True,
            "segment_id_required": True,
            "window_timestamps_required": True,
            "lane_type_required": True,
            "review_status_required": True,
            "provenance_status_required": True,
            "source_warnings_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_segment_replay_timeline(
    *,
    gameplay_segments_path: str | Path,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_REPLAY_TIMELINE_OUTPUT,
    routing_plan_path: str | Path | None = None,
    execution_plan_path: str | Path | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a replay timeline lane artifact from gameplay gate provenance."""

    generated_at = generated_at or datetime.now(UTC)
    gameplay_load = _load_json(
        gameplay_segments_path,
        label="gameplay_segment_candidates",
    )
    if gameplay_load.get("ok") is False:
        return gameplay_load
    gameplay_segments = _dict(gameplay_load.get("data"))
    if gameplay_segments.get("output_type") != GAMEPLAY_SEGMENT_CANDIDATES_TYPE:
        return _failed(
            "invalid_gameplay_segment_output_type",
            "gameplay segment source must be a Blueprint 38 candidate artifact",
        )

    routing_plan = {}
    if routing_plan_path:
        routing_load = _load_json(routing_plan_path, label="gameplay_gated_routing_plan")
        if routing_load.get("ok") is False:
            return routing_load
        routing_plan = _dict(routing_load.get("data"))
        if routing_plan.get("plan_type") != GAMEPLAY_GATED_ROUTING_PLAN_TYPE:
            return _failed(
                "invalid_routing_plan_type",
                "routing source must be a Blueprint 39 routing plan artifact",
            )

    execution_plan = {}
    if execution_plan_path:
        execution_load = _load_json(
            execution_plan_path,
            label="gameplay_gated_perception_execution_plan",
        )
        if execution_load.get("ok") is False:
            return execution_load
        execution_plan = _dict(execution_load.get("data"))
        if execution_plan.get("plan_type") != GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE:
            return _failed(
                "invalid_execution_plan_type",
                "execution source must be a Blueprint 40 execution plan artifact",
            )

    segments = [
        segment
        for segment in _list(gameplay_segments.get("segment_candidates"))
        if isinstance(segment, dict)
    ]
    media_id = str(gameplay_segments.get("media_id") or "unknown_media")
    replay_url = _replay_url(
        media_id=media_id,
        viewer_base_url=viewer_base_url,
        source_replay_url=gameplay_segments.get("replay_url"),
    )
    segment_by_id = {str(segment.get("segment_id")): segment for segment in segments}
    entries = [
        *_segment_timeline_entries(media_id, segments),
        *_routing_timeline_entries(media_id, routing_plan, segment_by_id),
        *_execution_timeline_entries(media_id, execution_plan, segment_by_id),
    ]
    timeline_id = _stable_id(
        "gameplay_segment_replay_timeline_v1",
        media_id,
        str(Path(gameplay_segments_path)),
        str(Path(routing_plan_path)) if routing_plan_path else "",
        str(Path(execution_plan_path)) if execution_plan_path else "",
        len(entries),
    )
    timeline = {
        "timeline_type": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE,
        "timeline_version": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION,
        "timeline_id": timeline_id,
        "media_id": media_id,
        "source_media_path": gameplay_segments.get("source_media_path"),
        "source_uri": gameplay_segments.get("source_uri"),
        "replay_url": replay_url,
        "gameplay_segment_source_path": str(Path(gameplay_segments_path)),
        "routing_plan_source_path": (
            str(Path(routing_plan_path)) if routing_plan_path else None
        ),
        "execution_plan_source_path": (
            str(Path(execution_plan_path)) if execution_plan_path else None
        ),
        "generated_at": generated_at.isoformat(),
        "lanes": _timeline_lanes(entries),
        "timeline_entries": entries,
        "summary": _timeline_summary(
            entries=entries,
            source_segment_count=len(segments),
            routing_plan=routing_plan,
            execution_plan=execution_plan,
        ),
        "source_summaries": {
            "gameplay_segments": _dict(gameplay_segments.get("summary")),
            "routing_plan": _dict(routing_plan.get("summary")),
            "execution_plan": _dict(execution_plan.get("summary")),
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "timeline_type": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE,
        "timeline_version": GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION,
        "timeline_id": timeline_id,
        "media_id": media_id,
        "timeline_entry_count": len(entries),
        "summary": timeline["summary"],
        "timeline": timeline,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    _write_json_if_requested(output_path, timeline, result, "timeline_output")
    return result


def validate_gameplay_segment_replay_timeline(
    *,
    timeline_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
    gameplay_segments_path: str | Path | None = None,
    routing_plan_path: str | Path | None = None,
    execution_plan_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a gameplay segment replay timeline structurally."""

    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []

    contract = _load_contract(contract_path, errors)
    timeline = _load_timeline(timeline_path, errors)
    if timeline:
        _validate_referenced_sources(
            errors=errors,
            timeline=timeline,
            gameplay_segments_path=gameplay_segments_path,
            routing_plan_path=routing_plan_path,
            execution_plan_path=execution_plan_path,
        )

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_segment_replay_timeline_validation",
        "validation_version": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "timeline_path": str(Path(timeline_path)),
        "contract_type": contract.get("contract_type"),
        "contract_version": contract.get("contract_version"),
        "timeline_type": timeline.get("timeline_type"),
        "timeline_version": timeline.get("timeline_version"),
        "media_id": timeline.get("media_id"),
        "error_count": len(errors),
        "errors": errors,
        "timeline_entry_count": len(_list(timeline.get("timeline_entries"))),
        "tracked_exports_should_not_be_committed": True,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed values, provenance, and exact forbidden tokens.",
            "Validation does not infer gameplay correctness.",
            "Validation does not execute perception jobs.",
            "Validation does not mutate regression baselines.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_segment_review_template(
    *,
    timeline_path: str | Path,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_REVIEW_TEMPLATE_OUTPUT,
    reviewer_id: str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a human-review metadata template from a replay timeline."""

    generated_at = generated_at or datetime.now(UTC)
    timeline_load = _load_json(timeline_path, label="gameplay_segment_replay_timeline")
    if timeline_load.get("ok") is False:
        return timeline_load
    timeline = _dict(timeline_load.get("data"))
    if timeline.get("timeline_type") != GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE:
        return _failed(
            "invalid_timeline_type",
            "timeline source must be a Blueprint 41 replay timeline artifact",
        )

    entries = [
        _review_entry(entry, reviewer_id=reviewer_id)
        for entry in _list(timeline.get("timeline_entries"))
        if isinstance(entry, dict)
    ]
    review_bundle_id = _stable_id(
        "gameplay_segment_review_bundle_v1",
        timeline.get("timeline_id"),
        timeline.get("media_id"),
        len(entries),
    )
    bundle = {
        "review_bundle_type": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE,
        "review_bundle_version": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION,
        "review_bundle_id": review_bundle_id,
        "template_type": "gameplay_segment_review_template",
        "template_version": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION,
        "timeline_id": timeline.get("timeline_id"),
        "media_id": timeline.get("media_id"),
        "source_timeline_path": str(Path(timeline_path)),
        "replay_url": timeline.get("replay_url"),
        "generated_at": generated_at.isoformat(),
        "reviewer_id": reviewer_id,
        "review_entries": entries,
        "summary": _review_bundle_summary(entries),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "review_bundle_type": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE,
        "review_bundle_version": GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION,
        "review_bundle_id": review_bundle_id,
        "review_entry_count": len(entries),
        "summary": bundle["summary"],
        "review_bundle": bundle,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    _write_json_if_requested(output_path, bundle, result, "review_template_output")
    return result


def validate_gameplay_segment_review_bundle(
    *,
    bundle_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
    timeline_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a gameplay segment review bundle structurally."""

    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []

    contract = _load_contract(contract_path, errors)
    bundle_load = _load_json(bundle_path, label="gameplay_segment_review_bundle")
    if bundle_load.get("ok") is False:
        errors.append(_error("bundle_load_failed", "bundle_path", bundle_load))
        bundle = {}
    else:
        bundle = _dict(bundle_load.get("data"))
        errors.extend(_validate_review_bundle_shape(bundle))

    timeline_ref = timeline_path or bundle.get("source_timeline_path")
    timeline = {}
    if timeline_ref:
        timeline = _load_timeline(timeline_ref, errors)
        if timeline and bundle.get("timeline_id") != timeline.get("timeline_id"):
            errors.append(
                _error(
                    "timeline_id_mismatch",
                    "review_bundle.timeline_id",
                    bundle.get("timeline_id"),
                )
            )

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_segment_review_bundle_validation",
        "validation_version": GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "bundle_path": str(Path(bundle_path)),
        "timeline_path": str(Path(timeline_ref)) if timeline_ref else None,
        "contract_type": contract.get("contract_type"),
        "contract_version": contract.get("contract_version"),
        "review_bundle_type": bundle.get("review_bundle_type"),
        "review_bundle_version": bundle.get("review_bundle_version"),
        "timeline_type": timeline.get("timeline_type"),
        "timeline_version": timeline.get("timeline_version"),
        "media_id": bundle.get("media_id"),
        "error_count": len(errors),
        "errors": errors,
        "review_entry_count": len(_list(bundle.get("review_entries"))),
        "tracked_exports_should_not_be_committed": True,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
        "known_limitations": [
            "Validation checks review metadata structure only.",
            "Validation does not decide whether any candidate is gameplay.",
            "Validation does not rank or score reviewers.",
            "Validation does not create truth.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_segment_review_report(
    *,
    timeline_path: str | Path,
    bundle_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_REVIEW_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural report over gameplay segment replay/review artifacts."""

    generated_at = generated_at or datetime.now(UTC)
    timeline_validation = validate_gameplay_segment_replay_timeline(
        contract_path=contract_path,
        timeline_path=timeline_path,
        output_path=None,
        validated_at=generated_at,
    )
    if timeline_validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_timeline",
            "error_count": timeline_validation.get("error_count"),
            "errors": timeline_validation.get("errors", []),
            "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
        }
    bundle_validation = validate_gameplay_segment_review_bundle(
        contract_path=contract_path,
        timeline_path=timeline_path,
        bundle_path=bundle_path,
        output_path=None,
        validated_at=generated_at,
    )
    if bundle_validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_review_bundle",
            "error_count": bundle_validation.get("error_count"),
            "errors": bundle_validation.get("errors", []),
            "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
        }

    timeline = _dict(_load_json(timeline_path, label="timeline").get("data"))
    bundle = _dict(_load_json(bundle_path, label="review_bundle").get("data"))
    timeline_entries = _list(timeline.get("timeline_entries"))
    review_entries = _list(bundle.get("review_entries"))
    report = {
        "report_type": GAMEPLAY_SEGMENT_REVIEW_REPORT_TYPE,
        "report_version": GAMEPLAY_SEGMENT_REVIEW_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_timeline_path": str(Path(timeline_path)),
        "source_review_bundle_path": str(Path(bundle_path)),
        "source_contract_path": str(Path(contract_path)),
        "media_id": timeline.get("media_id"),
        "timeline_id": timeline.get("timeline_id"),
        "review_bundle_id": bundle.get("review_bundle_id"),
        "replay_url": timeline.get("replay_url"),
        "summary": {
            **_review_report_summary(timeline_entries, review_entries),
            "timeline_validation_status": timeline_validation.get("status"),
            "timeline_validation_error_count": timeline_validation.get("error_count"),
            "review_bundle_validation_status": bundle_validation.get("status"),
            "review_bundle_validation_error_count": bundle_validation.get("error_count"),
        },
        "lane_summaries": _lane_summaries(timeline_entries),
        "review_status_summaries": _review_status_summaries(review_entries),
        "next_review_contract": {
            "this_report_persists_review_notes": False,
            "review_metadata_can_seed_future_review_workflows": True,
            "review_statuses_do_not_create_truth": True,
            "operators_should_inspect_review_needed_windows": True,
        },
        "timeline_validation_snapshot": timeline_validation,
        "review_bundle_validation_snapshot": bundle_validation,
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": GAMEPLAY_SEGMENT_REVIEW_REPORT_TYPE,
        "report_version": GAMEPLAY_SEGMENT_REVIEW_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _segment_timeline_entries(
    media_id: str,
    segments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    entries = []
    for segment in segments:
        lane_type = _segment_lane_type(segment)
        entries.append(
            _timeline_entry(
                media_id=media_id,
                segment=segment,
                lane_type=lane_type,
                display_label=_display_label(lane_type, segment),
                provenance_status="gameplay_segment_provenance_available",
                routing_decision="not_applicable",
                execution_decision="not_applicable",
                source_ref={
                    "source_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
                    "source_entry_id": segment.get("segment_id"),
                },
            )
        )
    return entries


def _routing_timeline_entries(
    media_id: str,
    routing_plan: dict[str, Any],
    segment_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not routing_plan:
        return []
    entries = []
    collections = [
        ("allowed_windows", "downstream_allowed", "allow_downstream_observation"),
        ("blocked_windows", "downstream_blocked", "skip_non_gameplay"),
        ("uncertain_windows", "downstream_review_required", "require_human_review"),
    ]
    for collection_name, lane_type, routing_decision in collections:
        for window in _list(routing_plan.get(collection_name)):
            if not isinstance(window, dict):
                continue
            segment = {
                **segment_by_id.get(str(window.get("segment_id")), {}),
                **_window_as_segment(window),
            }
            entries.append(
                _timeline_entry(
                    media_id=media_id,
                    segment=segment,
                    lane_type=lane_type,
                    display_label=_display_label(lane_type, segment),
                    provenance_status="routing_plan_provenance_available",
                    routing_decision=routing_decision,
                    execution_decision="not_applicable",
                    source_ref={
                        "source_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
                        "source_collection": collection_name,
                        "source_entry_id": window.get("window_id"),
                    },
                    source_warnings=_dict(window.get("warnings")),
                )
            )
    return entries


def _execution_timeline_entries(
    media_id: str,
    execution_plan: dict[str, Any],
    segment_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not execution_plan:
        return []
    entries = []
    collections = [
        ("allowed_execution_windows", "perception_execution_window"),
        ("skipped_windows", "perception_skipped_window"),
        ("review_required_windows", "perception_skipped_window"),
    ]
    for collection_name, lane_type in collections:
        for window in _list(execution_plan.get(collection_name)):
            if not isinstance(window, dict):
                continue
            segment = {
                **segment_by_id.get(str(window.get("segment_id")), {}),
                **_window_as_segment(window),
            }
            entries.append(
                _timeline_entry(
                    media_id=media_id,
                    segment=segment,
                    lane_type=lane_type,
                    display_label=_display_label(lane_type, segment),
                    provenance_status="execution_plan_provenance_available",
                    routing_decision="not_applicable",
                    execution_decision=str(
                        window.get("execution_decision") or "not_applicable"
                    ),
                    source_ref={
                        "source_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
                        "source_collection": collection_name,
                        "source_entry_id": window.get("execution_window_id"),
                    },
                    source_warnings=_dict(window.get("warnings")),
                )
            )
    return entries


def _timeline_entry(
    *,
    media_id: str,
    segment: dict[str, Any],
    lane_type: str,
    display_label: str,
    provenance_status: str,
    routing_decision: str,
    execution_decision: str,
    source_ref: dict[str, Any],
    source_warnings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    segment_id = str(segment.get("segment_id") or "missing_segment_candidate")
    start_ms = segment.get("segment_start_ms")
    end_ms = segment.get("segment_end_ms")
    return {
        "timeline_entry_id": _stable_id(
            "gameplay_segment_timeline_entry_v1",
            media_id,
            segment_id,
            lane_type,
            start_ms,
            end_ms,
            source_ref.get("source_entry_id"),
        ),
        "media_id": media_id,
        "segment_id": segment_id,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "start_frame_index": segment.get("start_frame_index"),
        "end_frame_index": segment.get("end_frame_index"),
        "lane_type": lane_type,
        "segment_status": segment.get("segment_status") or "not_applicable",
        "downstream_gate_status": (
            segment.get("downstream_gate_status") or "not_applicable"
        ),
        "routing_decision": routing_decision,
        "execution_decision": execution_decision,
        "review_status": _review_status_for_lane(lane_type, segment),
        "display_label": display_label,
        "provenance_status": provenance_status,
        "source_ref": source_ref,
        "source_warnings": source_warnings or _dict(segment.get("warnings")),
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }


def _review_entry(
    timeline_entry: dict[str, Any],
    *,
    reviewer_id: str | None,
) -> dict[str, Any]:
    return {
        "review_entry_id": _stable_id(
            "gameplay_segment_review_entry_v1",
            timeline_entry.get("timeline_entry_id"),
            timeline_entry.get("media_id"),
            timeline_entry.get("segment_id"),
        ),
        "timeline_entry_id": timeline_entry.get("timeline_entry_id"),
        "media_id": timeline_entry.get("media_id"),
        "segment_id": timeline_entry.get("segment_id"),
        "start_ms": timeline_entry.get("start_ms"),
        "end_ms": timeline_entry.get("end_ms"),
        "lane_type": timeline_entry.get("lane_type"),
        "display_label": timeline_entry.get("display_label"),
        "suggested_review_status": timeline_entry.get("review_status"),
        "review_status": "not_reviewed",
        "operator_review": {
            "review_status": "not_reviewed",
            "reviewer_id": reviewer_id,
            "reviewed_at": None,
            "review_note": None,
            "review_note_is_optional": True,
            "human_metadata_only": True,
        },
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "replay_review_scope",
        "source_contract_refs",
        "timeline_lane_schema",
        "review_template_schema",
        "review_bundle_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    refs = _dict(contract.get("source_contract_refs"))
    expected_refs = {
        "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "gameplay_gated_pipeline_routing_contract_version": (
            GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
        ),
        "gameplay_gated_perception_execution_contract_version": (
            GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
        ),
    }
    for key, expected in expected_refs.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _validate_timeline_shape(timeline: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(timeline, path="timeline")
    if timeline.get("timeline_type") != GAMEPLAY_SEGMENT_REPLAY_TIMELINE_TYPE:
        errors.append(
            _error("invalid_timeline_type", "timeline_type", timeline.get("timeline_type"))
        )
    if timeline.get("timeline_version") != GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VERSION:
        errors.append(
            _error(
                "invalid_timeline_version",
                "timeline_version",
                timeline.get("timeline_version"),
            )
        )
    for field in (
        "timeline_id",
        "media_id",
        "source_media_path",
        "replay_url",
        "gameplay_segment_source_path",
        "generated_at",
        "lanes",
        "timeline_entries",
        "summary",
        "warnings",
    ):
        if field not in timeline:
            errors.append(_error("missing_timeline_field", field, None))
    for index, entry in enumerate(_list(timeline.get("timeline_entries"))):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_timeline_entry", f"timeline_entries[{index}]", entry))
            continue
        _validate_timeline_entry(errors, index, entry)
    return errors


def _validate_review_bundle_shape(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(bundle, path="review_bundle")
    if bundle.get("review_bundle_type") != GAMEPLAY_SEGMENT_REVIEW_BUNDLE_TYPE:
        errors.append(
            _error(
                "invalid_review_bundle_type",
                "review_bundle_type",
                bundle.get("review_bundle_type"),
            )
        )
    if bundle.get("review_bundle_version") != GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VERSION:
        errors.append(
            _error(
                "invalid_review_bundle_version",
                "review_bundle_version",
                bundle.get("review_bundle_version"),
            )
        )
    for field in (
        "review_bundle_id",
        "timeline_id",
        "media_id",
        "source_timeline_path",
        "replay_url",
        "generated_at",
        "review_entries",
        "summary",
        "warnings",
    ):
        if field not in bundle:
            errors.append(_error("missing_review_bundle_field", field, None))
    for index, entry in enumerate(_list(bundle.get("review_entries"))):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_review_entry", f"review_entries[{index}]", entry))
            continue
        _validate_review_entry(errors, index, entry)
    return errors


def _validate_timeline_entry(
    errors: list[dict[str, Any]],
    index: int,
    entry: dict[str, Any],
) -> None:
    lane_type = entry.get("lane_type")
    review_status = entry.get("review_status")
    provenance_status = entry.get("provenance_status")
    if lane_type not in ALLOWED_LANE_TYPES:
        errors.append(_error("invalid_lane_type", f"timeline_entries[{index}]", lane_type))
    if review_status not in ALLOWED_REVIEW_STATUSES:
        errors.append(
            _error(
                "invalid_review_status",
                f"timeline_entries[{index}].review_status",
                review_status,
            )
        )
    if provenance_status not in ALLOWED_PROVENANCE_STATUSES:
        errors.append(
            _error(
                "invalid_provenance_status",
                f"timeline_entries[{index}].provenance_status",
                provenance_status,
            )
        )
    for field in (
        "timeline_entry_id",
        "media_id",
        "segment_id",
        "start_ms",
        "end_ms",
        "display_label",
    ):
        if entry.get(field) is None:
            errors.append(_error("missing_timeline_entry_field", field, None))


def _validate_review_entry(
    errors: list[dict[str, Any]],
    index: int,
    entry: dict[str, Any],
) -> None:
    lane_type = entry.get("lane_type")
    review_status = entry.get("review_status")
    suggested_review_status = entry.get("suggested_review_status")
    if lane_type not in ALLOWED_LANE_TYPES:
        errors.append(_error("invalid_lane_type", f"review_entries[{index}]", lane_type))
    if review_status not in ALLOWED_REVIEW_STATUSES:
        errors.append(
            _error(
                "invalid_review_status",
                f"review_entries[{index}].review_status",
                review_status,
            )
        )
    if suggested_review_status not in ALLOWED_REVIEW_STATUSES:
        errors.append(
            _error(
                "invalid_suggested_review_status",
                f"review_entries[{index}].suggested_review_status",
                suggested_review_status,
            )
        )
    operator_review = entry.get("operator_review")
    if not isinstance(operator_review, dict):
        errors.append(
            _error(
                "missing_operator_review",
                f"review_entries[{index}].operator_review",
                operator_review,
            )
        )
    elif operator_review.get("review_status") not in ALLOWED_REVIEW_STATUSES:
        errors.append(
            _error(
                "invalid_operator_review_status",
                f"review_entries[{index}].operator_review.review_status",
                operator_review.get("review_status"),
            )
        )
    for field in (
        "review_entry_id",
        "timeline_entry_id",
        "media_id",
        "segment_id",
        "start_ms",
        "end_ms",
    ):
        if entry.get(field) is None:
            errors.append(_error("missing_review_entry_field", field, None))


def _validate_referenced_sources(
    *,
    errors: list[dict[str, Any]],
    timeline: dict[str, Any],
    gameplay_segments_path: str | Path | None,
    routing_plan_path: str | Path | None,
    execution_plan_path: str | Path | None,
) -> None:
    gameplay_ref = gameplay_segments_path or timeline.get("gameplay_segment_source_path")
    if gameplay_ref:
        gameplay_load = _load_json(gameplay_ref, label="gameplay_segment_candidates")
        if gameplay_load.get("ok") is False:
            errors.append(_error("gameplay_segments_load_failed", "gameplay_ref", gameplay_load))
        elif (
            _dict(gameplay_load.get("data")).get("output_type")
            != GAMEPLAY_SEGMENT_CANDIDATES_TYPE
        ):
            errors.append(
                _error(
                    "invalid_gameplay_segment_output_type",
                    "gameplay_ref.output_type",
                    _dict(gameplay_load.get("data")).get("output_type"),
                )
            )
    routing_ref = routing_plan_path or timeline.get("routing_plan_source_path")
    if routing_ref:
        routing_load = _load_json(routing_ref, label="gameplay_gated_routing_plan")
        if routing_load.get("ok") is False:
            errors.append(_error("routing_plan_load_failed", "routing_ref", routing_load))
        elif _dict(routing_load.get("data")).get("plan_type") != GAMEPLAY_GATED_ROUTING_PLAN_TYPE:
            errors.append(
                _error(
                    "invalid_routing_plan_type",
                    "routing_ref.plan_type",
                    _dict(routing_load.get("data")).get("plan_type"),
                )
            )
    execution_ref = execution_plan_path or timeline.get("execution_plan_source_path")
    if execution_ref:
        execution_load = _load_json(
            execution_ref,
            label="gameplay_gated_perception_execution_plan",
        )
        if execution_load.get("ok") is False:
            errors.append(
                _error("execution_plan_load_failed", "execution_ref", execution_load)
            )
        elif (
            _dict(execution_load.get("data")).get("plan_type")
            != GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE
        ):
            errors.append(
                _error(
                    "invalid_execution_plan_type",
                    "execution_ref.plan_type",
                    _dict(execution_load.get("data")).get("plan_type"),
                )
            )


def _load_contract(
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    contract_load = _load_json(contract_path, label="gameplay_segment_replay_review_contract")
    if contract_load.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", contract_load))
        return {}
    contract = _dict(contract_load.get("data"))
    errors.extend(_validate_contract_shape(contract))
    return contract


def _load_timeline(
    timeline_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    timeline_load = _load_json(timeline_path, label="gameplay_segment_replay_timeline")
    if timeline_load.get("ok") is False:
        errors.append(_error("timeline_load_failed", "timeline_path", timeline_load))
        return {}
    timeline = _dict(timeline_load.get("data"))
    errors.extend(_validate_timeline_shape(timeline))
    return timeline


def _segment_lane_type(segment: dict[str, Any]) -> str:
    status = str(segment.get("segment_status") or "not_applicable")
    downstream_status = str(segment.get("downstream_gate_status") or "not_applicable")
    if status == "gameplay_segment_candidate":
        return "gameplay_segment_candidate"
    if status == "uncertain_segment" or downstream_status == "requires_human_review":
        return "uncertain_segment"
    if status in {"non_gameplay_segment_candidate", "short_segment_filtered"}:
        return "non_gameplay_segment_candidate"
    return "not_applicable"


def _review_status_for_lane(lane_type: str, segment: dict[str, Any]) -> str:
    if lane_type in {"uncertain_segment", "downstream_review_required"}:
        return "review_needed"
    if str(segment.get("downstream_gate_status")) == "requires_human_review":
        return "review_needed"
    if lane_type == "perception_skipped_window" and str(
        segment.get("execution_decision")
    ) == "require_human_review":
        return "review_needed"
    if lane_type == "not_applicable":
        return "not_applicable"
    return "review_optional"


def _display_label(lane_type: str, segment: dict[str, Any]) -> str:
    if lane_type == "gameplay_segment_candidate":
        return "Gameplay candidate"
    if lane_type == "non_gameplay_segment_candidate":
        if segment.get("segment_status") == "short_segment_filtered":
            return "Short segment filtered"
        return "Non-gameplay candidate"
    if lane_type == "uncertain_segment":
        return "Uncertain segment"
    if lane_type == "downstream_allowed":
        return "Downstream allowed"
    if lane_type == "downstream_blocked":
        return "Downstream blocked"
    if lane_type == "downstream_review_required":
        return "Downstream review required"
    if lane_type == "perception_execution_window":
        return "Perception execution window"
    if lane_type == "perception_skipped_window":
        if segment.get("execution_decision") == "require_human_review":
            return "Perception review required"
        return "Perception skipped window"
    return "Not applicable"


def _window_as_segment(window: dict[str, Any]) -> dict[str, Any]:
    return {
        "segment_id": window.get("segment_id"),
        "segment_start_ms": window.get("segment_start_ms"),
        "segment_end_ms": window.get("segment_end_ms"),
        "segment_status": window.get("segment_status"),
        "downstream_gate_status": window.get("downstream_gate_status"),
        "execution_decision": window.get("execution_decision"),
        "warnings": window.get("source_segment_warnings") or window.get("warnings"),
    }


def _timeline_lanes(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lane_counts = Counter(entry["lane_type"] for entry in entries)
    return [
        {
            "lane_type": lane_type,
            "display_label": _display_label(lane_type, {}),
            "entry_count": lane_counts.get(lane_type, 0),
            "review_visibility_only": True,
        }
        for lane_type in sorted(lane_counts)
    ]


def _timeline_summary(
    *,
    entries: list[dict[str, Any]],
    source_segment_count: int,
    routing_plan: dict[str, Any],
    execution_plan: dict[str, Any],
) -> dict[str, Any]:
    lane_counts = Counter(entry["lane_type"] for entry in entries)
    review_counts = Counter(entry["review_status"] for entry in entries)
    provenance_counts = Counter(entry["provenance_status"] for entry in entries)
    return {
        "source_segment_count": source_segment_count,
        "timeline_entry_count": len(entries),
        "lane_counts": dict(sorted(lane_counts.items())),
        "review_status_counts": dict(sorted(review_counts.items())),
        "provenance_status_counts": dict(sorted(provenance_counts.items())),
        "routing_plan_attached": bool(routing_plan),
        "execution_plan_attached": bool(execution_plan),
        "review_needed_entry_count": review_counts.get("review_needed", 0),
        "review_optional_entry_count": review_counts.get("review_optional", 0),
        "timeline_is_review_visibility_only": True,
        "does_not_persist_review_notes": True,
    }


def _review_bundle_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(entry.get("review_status") for entry in entries)
    suggested_counts = Counter(entry.get("suggested_review_status") for entry in entries)
    lane_counts = Counter(entry.get("lane_type") for entry in entries)
    return {
        "review_entry_count": len(entries),
        "review_status_counts": dict(sorted(status_counts.items())),
        "suggested_review_status_counts": dict(sorted(suggested_counts.items())),
        "lane_counts": dict(sorted(lane_counts.items())),
        "human_reviewed_entry_count": 0,
        "review_notes_present_count": 0,
        "review_metadata_only": True,
    }


def _review_report_summary(
    timeline_entries: list[Any],
    review_entries: list[Any],
) -> dict[str, Any]:
    timeline_lane_counts = Counter(
        entry.get("lane_type")
        for entry in timeline_entries
        if isinstance(entry, dict) and entry.get("lane_type")
    )
    review_status_counts = Counter(
        entry.get("review_status")
        for entry in review_entries
        if isinstance(entry, dict) and entry.get("review_status")
    )
    suggested_counts = Counter(
        entry.get("suggested_review_status")
        for entry in review_entries
        if isinstance(entry, dict) and entry.get("suggested_review_status")
    )
    return {
        "timeline_entry_count": len(timeline_entries),
        "review_entry_count": len(review_entries),
        "timeline_lane_counts": dict(sorted(timeline_lane_counts.items())),
        "review_status_counts": dict(sorted(review_status_counts.items())),
        "suggested_review_status_counts": dict(sorted(suggested_counts.items())),
        "review_needed_entry_count": suggested_counts.get("review_needed", 0),
        "human_reviewed_entry_count": 0,
        "review_notes_present_count": 0,
        "report_is_review_visibility_only": True,
    }


def _lane_summaries(entries: list[Any]) -> list[dict[str, Any]]:
    by_lane: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if isinstance(entry, dict):
            by_lane.setdefault(str(entry.get("lane_type")), []).append(entry)
    summaries = []
    for lane_type, lane_entries in sorted(by_lane.items()):
        review_counts = Counter(entry.get("review_status") for entry in lane_entries)
        summaries.append(
            {
                "lane_type": lane_type,
                "display_label": _display_label(lane_type, {}),
                "entry_count": len(lane_entries),
                "review_status_counts": dict(sorted(review_counts.items())),
            }
        )
    return summaries


def _review_status_summaries(entries: list[Any]) -> list[dict[str, Any]]:
    by_status: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if isinstance(entry, dict):
            by_status.setdefault(str(entry.get("review_status")), []).append(entry)
    return [
        {
            "review_status": review_status,
            "entry_count": len(status_entries),
            "review_status_is_metadata_only": True,
        }
        for review_status, status_entries in sorted(by_status.items())
    ]


def _replay_url(
    *,
    media_id: str,
    viewer_base_url: str,
    source_replay_url: Any,
) -> str:
    if isinstance(source_replay_url, str) and source_replay_url.strip():
        return source_replay_url
    return f"{viewer_base_url.rstrip('/')}/replay/{media_id}"


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_REPLAY_REVIEW_TOKENS:
                errors.append(_error("forbidden_token_key", child_path, key))
            errors.extend(_forbidden_token_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_REPLAY_REVIEW_TOKENS:
        errors.append(_error("forbidden_token_value", path, value))
    return errors


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        json.dumps([str(part) for part in parts], sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return f"{prefix}_{digest}"


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


def _write_json_if_requested(
    output_path: str | Path | None,
    data: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None or not str(output_path).strip():
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result[result_key] = str(path)


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(GAMEPLAY_SEGMENT_REPLAY_REVIEW_WARNINGS),
        **extra,
    }


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_SEGMENT_REPLAY_REVIEW_BLUEPRINT,
        "blueprint_name": GAMEPLAY_SEGMENT_REPLAY_REVIEW_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
