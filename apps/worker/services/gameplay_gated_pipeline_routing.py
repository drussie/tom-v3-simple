from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_segment_gate import (
    GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
    GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
)

GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE = "gameplay_gated_pipeline_routing_contract"
GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION = "v1"
GAMEPLAY_GATED_ROUTING_PLAN_TYPE = "gameplay_gated_pipeline_routing_plan"
GAMEPLAY_GATED_ROUTING_PLAN_VERSION = "v1"
GAMEPLAY_GATED_ROUTING_REPORT_TYPE = "gameplay_gated_pipeline_routing_report"
GAMEPLAY_GATED_ROUTING_REPORT_VERSION = "v1"
GAMEPLAY_GATED_ROUTING_BLUEPRINT = "blueprint_39"
GAMEPLAY_GATED_ROUTING_BLUEPRINT_NAME = (
    "gameplay_gated_evidence_pipeline_routing_v1"
)

DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_gated_pipeline_routing_contract_v1.json"
)
DEFAULT_GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT = (
    ".data/exports/gameplay_gated_routing_plan.current.json"
)
DEFAULT_GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_gated_routing_plan.validation.json"
)
DEFAULT_GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT = (
    ".data/exports/gameplay_gated_routing_report.current.json"
)

GAMEPLAY_GATED_ROUTING_EXPORTED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)

DEFAULT_DOWNSTREAM_STAGES = [
    "media_indexing",
    "replay_indexing",
    "detection_generation",
    "tracklet_generation",
    "pose_generation",
    "court_geometry_generation",
    "homography_candidate_generation",
    "projection_diagnostics_generation",
    "trajectory_3d_generation",
    "point_manifest_generation",
    "corpus_manifest_inclusion",
    "review_queue_inclusion",
]

ALLOWED_ROUTING_MODES = {
    "dry_run",
    "validate_only",
    "plan_only",
    "gated_execution_ready",
    "override_allowed_for_review_only",
}

ALLOWED_ROUTING_DECISIONS = {
    "allow_downstream_observation",
    "block_downstream_observation",
    "require_human_review",
    "skip_non_gameplay",
    "skip_uncertain",
    "preserve_existing_behavior",
    "not_assessed",
    "not_applicable",
}

ALLOWED_SKIP_REASONS = {
    "non_gameplay_segment_candidate",
    "uncertain_segment",
    "short_segment_filtered",
    "missing_gameplay_gate",
    "missing_segment_candidate",
    "unsafe_execution_mode",
    "explicit_review_required",
    "not_applicable",
}

ALLOWED_OVERRIDE_STATUSES = {
    "no_override",
    "review_only_override",
    "explicit_operator_override_required",
    "override_not_allowed",
    "not_applicable",
}

FORBIDDEN_ROUTING_TOKENS = {
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
    "confirmed_gameplay",
    "correct_gameplay",
    "point_confirmed",
    "point_truth",
    "event_truth",
    "rally_truth",
    "in_play_truth",
    "line_call_truth",
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "training_truth",
    "model_ready_truth",
}

GAMEPLAY_GATED_ROUTING_WARNINGS = {
    "routing_plan_only": True,
    "candidate_windows_only": True,
    "does_not_execute_downstream_jobs_by_default": True,
    "does_not_create_observations": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_mutate_model_assets": True,
    "does_not_claim_generalization": True,
    "does_not_claim_automatic_correctness": True,
    "does_not_convert_outputs_into_training_labels": True,
    "no_adjudication": True,
    "observation_only": True,
    "review_support_only": True,
}

SOURCE_CONTRACT_REFS = {
    "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
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


def export_gameplay_gated_routing_contract(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the Blueprint 39 gameplay-gated routing contract."""

    exported_at = exported_at or GAMEPLAY_GATED_ROUTING_EXPORTED_AT
    contract = {
        "contract_type": GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "routing_scope": {
            "purpose": "gameplay_gated_downstream_observation_routing",
            "reads_gameplay_segment_candidates": True,
            "creates_routing_plan_artifacts": True,
            "executes_downstream_jobs_by_default": False,
            "default_routing_mode": "dry_run",
            "explicit_media_input_only": True,
            "silently_discards_segments": False,
            "mutates_regression_baselines": False,
            "mutates_model_assets": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "gameplay_gate_contract_ref": {
            "contract_type": GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
            "contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
            "candidate_output_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
            "candidate_output_version": GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
        },
        "routing_plan_schema": {
            "plan_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
            "plan_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
            "required_fields": [
                "routing_plan_id",
                "media_id",
                "source_media_path",
                "gameplay_segment_source_path",
                "generated_at",
                "routing_mode",
                "downstream_stages",
                "allowed_windows",
                "blocked_windows",
                "uncertain_windows",
                "routing_entries",
                "summary",
                "warnings",
            ],
            "allowed_routing_modes": sorted(ALLOWED_ROUTING_MODES),
            "allowed_routing_decisions": sorted(ALLOWED_ROUTING_DECISIONS),
        },
        "downstream_stage_schema": {
            "allowed_stages": list(DEFAULT_DOWNSTREAM_STAGES),
            "stage_entries_are_plan_rows_only": True,
            "stage_execution_requires_future_explicit_mode": True,
        },
        "skip_reason_schema": {
            "allowed_skip_reasons": sorted(ALLOWED_SKIP_REASONS),
            "skip_reasons_are_structural": True,
            "segments_must_be_preserved_with_reason": True,
        },
        "override_policy_schema": {
            "allowed_override_statuses": sorted(ALLOWED_OVERRIDE_STATUSES),
            "default_override_status": "no_override",
            "review_override_does_not_execute_jobs": True,
            "operator_override_required_for_non_allowed_windows": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_routing_plan_shape": True,
            "validate_allowed_routing_modes": True,
            "validate_allowed_routing_decisions": True,
            "validate_allowed_skip_reasons": True,
            "validate_allowed_override_statuses": True,
            "validate_referenced_gameplay_segment_gate_contract": True,
            "reject_forbidden_exact_tokens": True,
            "structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "routing_plan_id_required": True,
            "media_id_required": True,
            "gameplay_segment_source_path_required": True,
            "segment_id_required": True,
            "downstream_stage_required": True,
            "routing_decision_required": True,
            "skip_reason_required": True,
            "override_status_required": True,
            "segment_warnings_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_gated_routing_plan(
    *,
    gameplay_segments_path: str | Path,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT,
    gameplay_gate_contract_path: str | Path | None = None,
    routing_mode: str = "dry_run",
    downstream_stages: list[str] | str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural downstream routing plan from gameplay segment candidates."""

    generated_at = generated_at or datetime.now(UTC)
    mode_error = _validate_routing_mode(routing_mode)
    if mode_error:
        return mode_error

    stages = _normalize_downstream_stages(downstream_stages)
    if not stages:
        return _failed("missing_downstream_stages", "at least one downstream stage is required")
    invalid_stages = [stage for stage in stages if stage not in DEFAULT_DOWNSTREAM_STAGES]
    if invalid_stages:
        return _failed("invalid_downstream_stage", f"unsupported stages: {invalid_stages}")

    segments_load = _load_json(gameplay_segments_path, label="gameplay_segment_candidates")
    if segments_load.get("ok") is False:
        return segments_load
    gameplay_segments = _dict(segments_load.get("data"))
    if gameplay_segments.get("output_type") != GAMEPLAY_SEGMENT_CANDIDATES_TYPE:
        return _failed(
            "invalid_gameplay_segment_output_type",
            "gameplay segment source must be a Blueprint 38 candidate artifact",
        )

    source_segments = _list(gameplay_segments.get("segment_candidates"))
    media_id = str(gameplay_segments.get("media_id") or "unknown_media")
    source_media_path = gameplay_segments.get("source_media_path")
    routing_plan_id = _stable_id(
        "gameplay_gated_routing_plan_v1",
        media_id,
        str(Path(gameplay_segments_path)),
        routing_mode,
        ",".join(stages),
        len(source_segments),
    )
    entries: list[dict[str, Any]] = []
    windows = _windows_by_status(media_id=media_id, segments=source_segments)
    for segment in source_segments:
        if not isinstance(segment, dict):
            continue
        for stage in stages:
            entries.append(
                _routing_entry(
                    media_id=media_id,
                    segment=segment,
                    downstream_stage=stage,
                    routing_mode=routing_mode,
                )
            )

    plan = {
        "plan_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
        "plan_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
        "routing_plan_id": routing_plan_id,
        "media_id": media_id,
        "source_media_path": source_media_path,
        "source_uri": gameplay_segments.get("source_uri"),
        "gameplay_segment_source_path": str(Path(gameplay_segments_path)),
        "gameplay_gate_contract_path": (
            str(Path(gameplay_gate_contract_path))
            if gameplay_gate_contract_path is not None
            else None
        ),
        "generated_at": generated_at.isoformat(),
        "routing_mode": routing_mode,
        "downstream_stages": stages,
        "allowed_windows": windows["allowed_windows"],
        "blocked_windows": windows["blocked_windows"],
        "uncertain_windows": windows["uncertain_windows"],
        "routing_entries": entries,
        "summary": _routing_summary(
            source_segments=source_segments,
            entries=entries,
            downstream_stages=stages,
        ),
        "replay_timeline": _replay_timeline(media_id, windows),
        "source_gameplay_summary": _dict(gameplay_segments.get("summary")),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "plan_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
        "plan_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
        "routing_plan_id": routing_plan_id,
        "media_id": media_id,
        "routing_mode": routing_mode,
        "downstream_stage_count": len(stages),
        "segment_count": len(source_segments),
        "routing_entry_count": len(entries),
        "summary": plan["summary"],
        "plan": plan,
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    _write_json_if_requested(output_path, plan, result, "plan_output")
    return result


def validate_gameplay_gated_routing_plan(
    *,
    plan_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    gameplay_gate_contract_path: str | Path | None = None,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate gameplay-gated routing plans structurally."""

    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []

    contract_load = _load_json(contract_path, label="gameplay_gated_routing_contract")
    if contract_load.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", contract_load))
        contract = {}
    else:
        contract = _dict(contract_load.get("data"))
        errors.extend(_validate_contract_shape(contract))

    plan_load = _load_json(plan_path, label="gameplay_gated_routing_plan")
    if plan_load.get("ok") is False:
        errors.append(_error("plan_load_failed", "plan_path", plan_load))
        plan = {}
    else:
        plan = _dict(plan_load.get("data"))
        errors.extend(_validate_plan_shape(plan))

    gate_contract_ref = gameplay_gate_contract_path or plan.get("gameplay_gate_contract_path")
    if gate_contract_ref:
        gate_contract_load = _load_json(
            gate_contract_ref,
            label="gameplay_segment_gate_contract",
        )
        if gate_contract_load.get("ok") is False:
            errors.append(
                _error(
                    "gameplay_gate_contract_load_failed",
                    "gameplay_gate_contract_path",
                    gate_contract_load,
                )
            )
        else:
            gate_contract = _dict(gate_contract_load.get("data"))
            if gate_contract.get("contract_type") != GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE:
                errors.append(
                    _error(
                        "invalid_gameplay_gate_contract_type",
                        "gameplay_gate_contract.contract_type",
                        gate_contract.get("contract_type"),
                    )
                )
            if gate_contract.get("contract_version") != GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION:
                errors.append(
                    _error(
                        "invalid_gameplay_gate_contract_version",
                        "gameplay_gate_contract.contract_version",
                        gate_contract.get("contract_version"),
                    )
                )

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_gated_routing_plan_validation",
        "validation_version": GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "plan_path": str(Path(plan_path)),
        "gameplay_gate_contract_path": str(Path(gate_contract_ref)) if gate_contract_ref else None,
        "contract_type": contract.get("contract_type"),
        "contract_version": contract.get("contract_version"),
        "plan_type": plan.get("plan_type"),
        "plan_version": plan.get("plan_version"),
        "routing_mode": plan.get("routing_mode"),
        "error_count": len(errors),
        "errors": errors,
        "routing_entry_count": len(_list(plan.get("routing_entries"))),
        "tracked_exports_should_not_be_committed": True,
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed values, provenance, and exact forbidden tokens.",
            "Validation does not execute downstream jobs.",
            "Validation does not infer tennis meaning.",
            "Validation does not mutate regression baselines.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_gated_routing_report(
    *,
    plan_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    gameplay_gate_contract_path: str | Path | None = None,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural report over a gameplay-gated routing plan."""

    generated_at = generated_at or datetime.now(UTC)
    plan_load = _load_json(plan_path, label="gameplay_gated_routing_plan")
    if plan_load.get("ok") is False:
        return plan_load
    plan = _dict(plan_load.get("data"))
    validation = validate_gameplay_gated_routing_plan(
        plan_path=plan_path,
        contract_path=contract_path,
        gameplay_gate_contract_path=gameplay_gate_contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_plan",
            "error_count": validation.get("error_count"),
            "errors": validation.get("errors", []),
            "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
        }

    entries = _list(plan.get("routing_entries"))
    report = {
        "report_type": GAMEPLAY_GATED_ROUTING_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_ROUTING_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_plan_path": str(Path(plan_path)),
        "source_contract_path": str(Path(contract_path)),
        "media_id": plan.get("media_id"),
        "routing_plan_id": plan.get("routing_plan_id"),
        "routing_mode": plan.get("routing_mode"),
        "summary": {
            **_routing_report_summary(entries),
            "validation_status": validation.get("status"),
            "validation_error_count": validation.get("error_count"),
        },
        "stage_summaries": _stage_summaries(entries),
        "window_summary": {
            "allowed_window_count": len(_list(plan.get("allowed_windows"))),
            "blocked_window_count": len(_list(plan.get("blocked_windows"))),
            "uncertain_window_count": len(_list(plan.get("uncertain_windows"))),
        },
        "replay_timeline": plan.get("replay_timeline"),
        "next_pipeline_contract": {
            "this_report_executes_downstream_jobs": False,
            "allowed_entries_can_gate_future_jobs": True,
            "blocked_entries_should_not_run_future_downstream_observation_jobs": True,
            "review_required_entries_need_operator_inspection": True,
        },
        "validation_snapshot": validation,
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": GAMEPLAY_GATED_ROUTING_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_ROUTING_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _routing_entry(
    *,
    media_id: str,
    segment: dict[str, Any],
    downstream_stage: str,
    routing_mode: str,
) -> dict[str, Any]:
    segment_id = str(segment.get("segment_id") or "missing_segment_candidate")
    segment_status = str(segment.get("segment_status") or "not_assessed")
    downstream_gate_status = str(segment.get("downstream_gate_status") or "not_assessed")
    decision, skip_reason = _decision_and_reason(
        segment_status=segment_status,
        downstream_gate_status=downstream_gate_status,
    )
    if routing_mode == "validate_only":
        decision = "not_assessed"
        skip_reason = "unsafe_execution_mode"
    override_status = _override_status(
        decision=decision,
        routing_mode=routing_mode,
    )
    provenance_status = (
        "segment_provenance_available" if segment_id != "missing_segment_candidate" else "missing"
    )
    return {
        "routing_entry_id": _stable_id(
            "gameplay_gated_route_v1",
            media_id,
            segment_id,
            downstream_stage,
            routing_mode,
        ),
        "media_id": media_id,
        "segment_id": segment_id,
        "segment_start_ms": segment.get("segment_start_ms"),
        "segment_end_ms": segment.get("segment_end_ms"),
        "segment_status": segment_status,
        "downstream_gate_status": downstream_gate_status,
        "downstream_stage": downstream_stage,
        "routing_decision": decision,
        "skip_reason": skip_reason,
        "override_status": override_status,
        "provenance_status": provenance_status,
        "source_segment_warnings": _dict(segment.get("warnings")),
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
    }


def _decision_and_reason(
    *,
    segment_status: str,
    downstream_gate_status: str,
) -> tuple[str, str]:
    if downstream_gate_status == "allowed_for_downstream_observation":
        return "allow_downstream_observation", "not_applicable"
    if segment_status == "short_segment_filtered":
        return "skip_non_gameplay", "short_segment_filtered"
    if segment_status == "non_gameplay_segment_candidate":
        return "skip_non_gameplay", "non_gameplay_segment_candidate"
    if downstream_gate_status == "blocked_from_downstream_observation":
        return "block_downstream_observation", "non_gameplay_segment_candidate"
    if segment_status == "uncertain_segment":
        return "require_human_review", "uncertain_segment"
    if downstream_gate_status == "requires_human_review":
        return "require_human_review", "explicit_review_required"
    if segment_status in {"not_assessed", "not_applicable"}:
        return segment_status, "not_applicable"
    return "not_assessed", "missing_segment_candidate"


def _override_status(*, decision: str, routing_mode: str) -> str:
    if decision in {"not_assessed", "not_applicable"}:
        return "not_applicable"
    if decision == "allow_downstream_observation":
        return "no_override"
    if routing_mode == "override_allowed_for_review_only":
        return "review_only_override"
    if routing_mode == "gated_execution_ready":
        return "override_not_allowed"
    return "explicit_operator_override_required"


def _windows_by_status(
    *,
    media_id: str,
    segments: list[Any],
) -> dict[str, list[dict[str, Any]]]:
    windows = {
        "allowed_windows": [],
        "blocked_windows": [],
        "uncertain_windows": [],
    }
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        window = {
            "window_id": _stable_id(
                "gameplay_routing_window_v1",
                media_id,
                segment.get("segment_id"),
                segment.get("segment_start_ms"),
                segment.get("segment_end_ms"),
            ),
            "media_id": media_id,
            "segment_id": segment.get("segment_id"),
            "segment_start_ms": segment.get("segment_start_ms"),
            "segment_end_ms": segment.get("segment_end_ms"),
            "segment_status": segment.get("segment_status"),
            "downstream_gate_status": segment.get("downstream_gate_status"),
            "source_segment_warnings": _dict(segment.get("warnings")),
            "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
        }
        downstream_gate_status = segment.get("downstream_gate_status")
        segment_status = segment.get("segment_status")
        if downstream_gate_status == "allowed_for_downstream_observation":
            windows["allowed_windows"].append(window)
        elif (
            downstream_gate_status == "requires_human_review"
            or segment_status == "uncertain_segment"
        ):
            windows["uncertain_windows"].append(window)
        else:
            windows["blocked_windows"].append(window)
    return windows


def _routing_summary(
    *,
    source_segments: list[Any],
    entries: list[dict[str, Any]],
    downstream_stages: list[str],
) -> dict[str, Any]:
    decision_counts = Counter(entry["routing_decision"] for entry in entries)
    skip_counts = Counter(entry["skip_reason"] for entry in entries)
    override_counts = Counter(entry["override_status"] for entry in entries)
    stage_counts = Counter(entry["downstream_stage"] for entry in entries)
    segment_counts = Counter(
        segment.get("segment_status")
        for segment in source_segments
        if isinstance(segment, dict) and segment.get("segment_status")
    )
    return {
        "source_segment_count": len(source_segments),
        "downstream_stage_count": len(downstream_stages),
        "routing_entry_count": len(entries),
        "routing_decision_counts": dict(sorted(decision_counts.items())),
        "skip_reason_counts": dict(sorted(skip_counts.items())),
        "override_status_counts": dict(sorted(override_counts.items())),
        "downstream_stage_entry_counts": dict(sorted(stage_counts.items())),
        "source_segment_status_counts": dict(sorted(segment_counts.items())),
        "downstream_jobs_executed": False,
    }


def _routing_report_summary(entries: list[Any]) -> dict[str, Any]:
    decision_counts = Counter(
        entry.get("routing_decision")
        for entry in entries
        if isinstance(entry, dict) and entry.get("routing_decision")
    )
    skip_counts = Counter(
        entry.get("skip_reason")
        for entry in entries
        if isinstance(entry, dict) and entry.get("skip_reason")
    )
    return {
        "routing_entry_count": len(entries),
        "allow_entry_count": decision_counts.get("allow_downstream_observation", 0),
        "block_entry_count": (
            decision_counts.get("block_downstream_observation", 0)
            + decision_counts.get("skip_non_gameplay", 0)
            + decision_counts.get("skip_uncertain", 0)
        ),
        "review_required_entry_count": decision_counts.get("require_human_review", 0),
        "routing_decision_counts": dict(sorted(decision_counts.items())),
        "skip_reason_counts": dict(sorted(skip_counts.items())),
        "downstream_jobs_executed": False,
    }


def _stage_summaries(entries: list[Any]) -> list[dict[str, Any]]:
    by_stage: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        by_stage.setdefault(str(entry.get("downstream_stage")), []).append(entry)
    summaries = []
    for stage, stage_entries in sorted(by_stage.items()):
        decision_counts = Counter(entry.get("routing_decision") for entry in stage_entries)
        summaries.append(
            {
                "downstream_stage": stage,
                "routing_entry_count": len(stage_entries),
                "routing_decision_counts": dict(sorted(decision_counts.items())),
                "downstream_jobs_executed": False,
            }
        )
    return summaries


def _replay_timeline(media_id: str, windows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    items = []
    for lane_name, status in (
        ("allowed_windows", "allowed_gameplay_window"),
        ("blocked_windows", "blocked_non_gameplay_window"),
        ("uncertain_windows", "review_required_gameplay_window"),
    ):
        for window in windows[lane_name]:
            items.append(
                {
                    "id": window["window_id"],
                    "segment_id": window["segment_id"],
                    "start_ms": window["segment_start_ms"],
                    "end_ms": window["segment_end_ms"],
                    "status": status,
                    "segment_status": window["segment_status"],
                    "downstream_gate_status": window["downstream_gate_status"],
                }
            )
    items.sort(key=lambda item: (item.get("start_ms") or 0, str(item.get("id"))))
    return {
        "timeline_type": "gameplay_gated_routing_timeline",
        "timeline_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
        "media_id": media_id,
        "lane": {
            "lane_id": "gameplay_gated_pipeline_routing",
            "label": "Gameplay-gated routing windows",
            "display_only": True,
            "items": items,
        },
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "routing_scope",
        "source_contract_refs",
        "gameplay_gate_contract_ref",
        "routing_plan_schema",
        "downstream_stage_schema",
        "skip_reason_schema",
        "override_policy_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    refs = _dict(contract.get("source_contract_refs"))
    if refs.get("gameplay_segment_gate_contract_version") != GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_source_gameplay_gate_version",
                "source_contract_refs.gameplay_segment_gate_contract_version",
                refs.get("gameplay_segment_gate_contract_version"),
            )
        )
    return errors


def _validate_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(plan, path="plan")
    if plan.get("plan_type") != GAMEPLAY_GATED_ROUTING_PLAN_TYPE:
        errors.append(_error("invalid_plan_type", "plan_type", plan.get("plan_type")))
    if plan.get("plan_version") != GAMEPLAY_GATED_ROUTING_PLAN_VERSION:
        errors.append(
            _error("invalid_plan_version", "plan_version", plan.get("plan_version"))
        )
    for section in (
        "routing_plan_id",
        "media_id",
        "source_media_path",
        "gameplay_segment_source_path",
        "generated_at",
        "routing_mode",
        "downstream_stages",
        "allowed_windows",
        "blocked_windows",
        "uncertain_windows",
        "routing_entries",
        "summary",
        "warnings",
    ):
        if section not in plan:
            errors.append(_error("missing_plan_section", section, None))
    if plan.get("routing_mode") not in ALLOWED_ROUTING_MODES:
        errors.append(
            _error("invalid_routing_mode", "routing_mode", plan.get("routing_mode"))
        )
    for index, stage in enumerate(_list(plan.get("downstream_stages"))):
        if stage not in DEFAULT_DOWNSTREAM_STAGES:
            errors.append(
                _error("invalid_downstream_stage", f"downstream_stages[{index}]", stage)
            )
    for collection_name in ("allowed_windows", "blocked_windows", "uncertain_windows"):
        for index, window in enumerate(_list(plan.get(collection_name))):
            if not isinstance(window, dict):
                errors.append(_error("invalid_window", f"{collection_name}[{index}]", window))
                continue
            if not window.get("segment_id"):
                errors.append(
                    _error("missing_window_segment_id", f"{collection_name}[{index}]", None)
                )
    for index, entry in enumerate(_list(plan.get("routing_entries"))):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_routing_entry", f"routing_entries[{index}]", entry))
            continue
        decision = entry.get("routing_decision")
        skip_reason = entry.get("skip_reason")
        override_status = entry.get("override_status")
        stage = entry.get("downstream_stage")
        if decision not in ALLOWED_ROUTING_DECISIONS:
            errors.append(
                _error(
                    "invalid_routing_decision",
                    f"routing_entries[{index}].routing_decision",
                    decision,
                )
            )
        if skip_reason not in ALLOWED_SKIP_REASONS:
            errors.append(
                _error(
                    "invalid_skip_reason",
                    f"routing_entries[{index}].skip_reason",
                    skip_reason,
                )
            )
        if override_status not in ALLOWED_OVERRIDE_STATUSES:
            errors.append(
                _error(
                    "invalid_override_status",
                    f"routing_entries[{index}].override_status",
                    override_status,
                )
            )
        if stage not in DEFAULT_DOWNSTREAM_STAGES:
            errors.append(
                _error(
                    "invalid_routing_entry_stage",
                    f"routing_entries[{index}].downstream_stage",
                    stage,
                )
            )
        if not entry.get("segment_id"):
            errors.append(_error("missing_entry_segment_id", f"routing_entries[{index}]", None))
        if not entry.get("routing_entry_id"):
            errors.append(_error("missing_entry_id", f"routing_entries[{index}]", None))
    return errors


def _normalize_downstream_stages(value: list[str] | str | None) -> list[str]:
    if value is None:
        return list(DEFAULT_DOWNSTREAM_STAGES)
    if isinstance(value, str):
        if not value.strip():
            return list(DEFAULT_DOWNSTREAM_STAGES)
        return [item.strip() for item in value.split(",") if item.strip()]
    return [item.strip() for item in value if item and item.strip()]


def _validate_routing_mode(mode: str) -> dict[str, Any] | None:
    if mode not in ALLOWED_ROUTING_MODES:
        return _failed("invalid_routing_mode", f"unsupported routing mode: {mode}")
    return None


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_ROUTING_TOKENS:
                errors.append(_error("forbidden_token_key", child_path, key))
            errors.extend(_forbidden_token_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_ROUTING_TOKENS:
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
        "warnings": dict(GAMEPLAY_GATED_ROUTING_WARNINGS),
        **extra,
    }


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_GATED_ROUTING_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATED_ROUTING_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
