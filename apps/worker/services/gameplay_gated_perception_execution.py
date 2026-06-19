from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_pipeline_routing import (
    GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
    GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
    GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
)
from apps.worker.services.gameplay_segment_gate import (
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
)

GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE = (
    "gameplay_gated_perception_execution_contract"
)
GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION = "v1"
GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE = (
    "gameplay_gated_perception_execution_plan"
)
GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION = "v1"
GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_TYPE = (
    "gameplay_gated_perception_execution_report"
)
GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_VERSION = "v1"
GAMEPLAY_GATED_PERCEPTION_EXECUTION_BLUEPRINT = "blueprint_40"
GAMEPLAY_GATED_PERCEPTION_EXECUTION_BLUEPRINT_NAME = (
    "gameplay_gated_perception_execution_hook_v1"
)

DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_gated_perception_execution_contract_v1.json"
)
DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_OUTPUT = (
    ".data/exports/gameplay_gated_perception_execution_plan.current.json"
)
DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_gated_perception_execution_plan.validation.json"
)
DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_OUTPUT = (
    ".data/exports/gameplay_gated_perception_execution_report.current.json"
)

GAMEPLAY_GATED_PERCEPTION_EXECUTION_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

DEFAULT_PERCEPTION_STAGES = [
    "detection_generation",
    "tracklet_generation",
    "pose_generation",
    "court_geometry_generation",
    "homography_candidate_generation",
    "projection_diagnostics_generation",
    "trajectory_3d_generation",
]

ALLOWED_EXECUTION_MODES = {
    "dry_run",
    "validate_only",
    "plan_only",
    "gated_execution_ready",
    "fixture_execution_only",
}

ALLOWED_EXECUTION_DECISIONS = {
    "execute_on_gameplay_window",
    "skip_non_gameplay_window",
    "skip_uncertain_window",
    "require_human_review",
    "preserve_existing_behavior",
    "not_assessed",
    "not_applicable",
}

ALLOWED_SKIP_REASONS = {
    "non_gameplay_segment_candidate",
    "uncertain_segment",
    "short_segment_filtered",
    "missing_gameplay_routing_plan",
    "missing_segment_candidate",
    "unsafe_execution_mode",
    "explicit_review_required",
    "stage_not_requested",
    "not_applicable",
}

ALLOWED_PROVENANCE_STATUSES = {
    "routing_entry_provenance_available",
    "window_provenance_available",
    "skipped_window_provenance_available",
    "missing",
    "not_applicable",
}

FORBIDDEN_EXECUTION_TOKENS = {
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
    "true_gameplay",
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
}

GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS = {
    "execution_hook_only": True,
    "routing_plan_required": True,
    "candidate_windows_only": True,
    "does_not_run_gpu_or_model_inference_by_default": True,
    "does_not_execute_heavy_perception_by_default": True,
    "does_not_create_observations_by_default": True,
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
    "gameplay_gated_pipeline_routing_contract_version": (
        GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
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


def export_gameplay_gated_perception_execution_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the Blueprint 40 gameplay-gated perception execution contract."""

    exported_at = exported_at or GAMEPLAY_GATED_PERCEPTION_EXECUTION_EXPORTED_AT
    contract = {
        "contract_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "execution_scope": {
            "purpose": "gameplay_gated_perception_execution_guard",
            "reads_gameplay_gated_routing_plan": True,
            "creates_execution_plan_artifacts": True,
            "executes_gpu_or_model_inference_by_default": False,
            "writes_observations_by_default": False,
            "default_execution_mode": "dry_run",
            "explicit_routing_plan_input_only": True,
            "silently_discards_windows": False,
            "mutates_regression_baselines": False,
            "mutates_model_assets": False,
            "preserves_existing_behavior_without_routing_plan": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "routing_plan_contract_ref": {
            "contract_type": GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE,
            "contract_version": GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
            "plan_type": GAMEPLAY_GATED_ROUTING_PLAN_TYPE,
            "plan_version": GAMEPLAY_GATED_ROUTING_PLAN_VERSION,
        },
        "perception_stage_schema": {
            "allowed_stages": list(DEFAULT_PERCEPTION_STAGES),
            "stage_entries_are_execution_plan_rows": True,
            "heavy_inference_requires_future_explicit_runner": True,
        },
        "execution_plan_schema": {
            "plan_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
            "plan_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
            "required_fields": [
                "execution_plan_id",
                "media_id",
                "source_media_path",
                "routing_plan_path",
                "generated_at",
                "execution_mode",
                "perception_stages",
                "allowed_execution_windows",
                "skipped_windows",
                "review_required_windows",
                "execution_entries",
                "summary",
                "warnings",
            ],
            "allowed_execution_modes": sorted(ALLOWED_EXECUTION_MODES),
            "allowed_execution_decisions": sorted(ALLOWED_EXECUTION_DECISIONS),
        },
        "skipped_window_schema": {
            "allowed_skip_reasons": sorted(ALLOWED_SKIP_REASONS),
            "blocked_windows_must_be_recorded": True,
            "review_required_windows_must_be_recorded": True,
            "skip_reasons_are_structural": True,
        },
        "execution_summary_schema": {
            "records_requested_stage_counts": True,
            "records_decision_counts": True,
            "records_skip_reason_counts": True,
            "records_window_counts": True,
            "records_that_jobs_executed": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_execution_plan_shape": True,
            "validate_allowed_execution_modes": True,
            "validate_allowed_execution_decisions": True,
            "validate_allowed_skip_reasons": True,
            "validate_allowed_provenance_statuses": True,
            "validate_referenced_routing_plan": True,
            "reject_forbidden_exact_tokens": True,
            "structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "execution_plan_id_required": True,
            "media_id_required": True,
            "routing_plan_path_required": True,
            "segment_id_required": True,
            "downstream_stage_required": True,
            "execution_decision_required": True,
            "skip_reason_required": True,
            "provenance_status_required": True,
            "expected_input_window_required": True,
            "routing_warnings_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_gated_perception_execution_plan(
    *,
    routing_plan_path: str | Path,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_OUTPUT
    ),
    routing_contract_path: str | Path | None = None,
    execution_mode: str = "dry_run",
    perception_stages: list[str] | str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural perception execution plan from a gameplay-gated routing plan."""

    generated_at = generated_at or datetime.now(UTC)
    mode_error = _validate_execution_mode(execution_mode)
    if mode_error:
        return mode_error

    stages = _normalize_perception_stages(perception_stages)
    if not stages:
        return _failed(
            "missing_perception_stages",
            "at least one perception stage is required",
        )
    invalid_stages = [stage for stage in stages if stage not in DEFAULT_PERCEPTION_STAGES]
    if invalid_stages:
        return _failed("invalid_perception_stage", f"unsupported stages: {invalid_stages}")

    routing_load = _load_json(routing_plan_path, label="gameplay_gated_routing_plan")
    if routing_load.get("ok") is False:
        return routing_load
    routing_plan = _dict(routing_load.get("data"))
    if routing_plan.get("plan_type") != GAMEPLAY_GATED_ROUTING_PLAN_TYPE:
        return _failed(
            "invalid_routing_plan_type",
            "routing plan source must be a Blueprint 39 routing plan artifact",
        )

    media_id = str(routing_plan.get("media_id") or "unknown_media")
    entries = [
        entry
        for entry in _list(routing_plan.get("routing_entries"))
        if isinstance(entry, dict) and entry.get("downstream_stage") in stages
    ]
    execution_entries = [
        _execution_entry(
            media_id=media_id,
            routing_entry=entry,
            execution_mode=execution_mode,
        )
        for entry in entries
    ]
    windows = _execution_windows_from_routing_plan(media_id=media_id, plan=routing_plan)
    execution_plan_id = _stable_id(
        "gameplay_gated_perception_execution_plan_v1",
        media_id,
        str(Path(routing_plan_path)),
        execution_mode,
        ",".join(stages),
        len(entries),
    )
    plan = {
        "plan_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
        "plan_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
        "execution_plan_id": execution_plan_id,
        "media_id": media_id,
        "source_media_path": routing_plan.get("source_media_path"),
        "source_uri": routing_plan.get("source_uri"),
        "routing_plan_path": str(Path(routing_plan_path)),
        "routing_contract_path": (
            str(Path(routing_contract_path)) if routing_contract_path is not None else None
        ),
        "generated_at": generated_at.isoformat(),
        "execution_mode": execution_mode,
        "perception_stages": stages,
        "allowed_execution_windows": windows["allowed_execution_windows"],
        "skipped_windows": windows["skipped_windows"],
        "review_required_windows": windows["review_required_windows"],
        "execution_entries": execution_entries,
        "summary": _execution_summary(
            entries=execution_entries,
            perception_stages=stages,
            windows=windows,
            routing_entry_count=len(entries),
        ),
        "source_routing_summary": _dict(routing_plan.get("summary")),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "plan_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE,
        "plan_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION,
        "execution_plan_id": execution_plan_id,
        "media_id": media_id,
        "execution_mode": execution_mode,
        "perception_stage_count": len(stages),
        "routing_entry_count": len(entries),
        "execution_entry_count": len(execution_entries),
        "summary": plan["summary"],
        "plan": plan,
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    _write_json_if_requested(output_path, plan, result, "plan_output")
    return result


def validate_gameplay_gated_perception_execution_plan(
    *,
    plan_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT
    ),
    routing_contract_path: str | Path | None = None,
    routing_plan_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate gameplay-gated perception execution plans structurally."""

    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []

    contract_load = _load_json(
        contract_path,
        label="gameplay_gated_perception_execution_contract",
    )
    if contract_load.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", contract_load))
        contract = {}
    else:
        contract = _dict(contract_load.get("data"))
        errors.extend(_validate_contract_shape(contract))

    plan_load = _load_json(
        plan_path,
        label="gameplay_gated_perception_execution_plan",
    )
    if plan_load.get("ok") is False:
        errors.append(_error("plan_load_failed", "plan_path", plan_load))
        plan = {}
    else:
        plan = _dict(plan_load.get("data"))
        errors.extend(_validate_plan_shape(plan))

    routing_plan_ref = routing_plan_path or plan.get("routing_plan_path")
    if routing_plan_ref:
        routing_plan_load = _load_json(
            routing_plan_ref,
            label="gameplay_gated_routing_plan",
        )
        if routing_plan_load.get("ok") is False:
            errors.append(
                _error(
                    "routing_plan_load_failed",
                    "routing_plan_path",
                    routing_plan_load,
                )
            )
        else:
            routing_plan = _dict(routing_plan_load.get("data"))
            if routing_plan.get("plan_type") != GAMEPLAY_GATED_ROUTING_PLAN_TYPE:
                errors.append(
                    _error(
                        "invalid_routing_plan_type",
                        "routing_plan.plan_type",
                        routing_plan.get("plan_type"),
                    )
                )
            if routing_plan.get("plan_version") != GAMEPLAY_GATED_ROUTING_PLAN_VERSION:
                errors.append(
                    _error(
                        "invalid_routing_plan_version",
                        "routing_plan.plan_version",
                        routing_plan.get("plan_version"),
                    )
                )

    routing_contract_ref = routing_contract_path or plan.get("routing_contract_path")
    if routing_contract_ref:
        routing_contract_load = _load_json(
            routing_contract_ref,
            label="gameplay_gated_routing_contract",
        )
        if routing_contract_load.get("ok") is False:
            errors.append(
                _error(
                    "routing_contract_load_failed",
                    "routing_contract_path",
                    routing_contract_load,
                )
            )
        else:
            routing_contract = _dict(routing_contract_load.get("data"))
            if routing_contract.get("contract_type") != GAMEPLAY_GATED_ROUTING_CONTRACT_TYPE:
                errors.append(
                    _error(
                        "invalid_routing_contract_type",
                        "routing_contract.contract_type",
                        routing_contract.get("contract_type"),
                    )
                )
            if (
                routing_contract.get("contract_version")
                != GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
            ):
                errors.append(
                    _error(
                        "invalid_routing_contract_version",
                        "routing_contract.contract_version",
                        routing_contract.get("contract_version"),
                    )
                )

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_gated_perception_execution_plan_validation",
        "validation_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "plan_path": str(Path(plan_path)),
        "routing_contract_path": (
            str(Path(routing_contract_ref)) if routing_contract_ref else None
        ),
        "routing_plan_path": str(Path(routing_plan_ref)) if routing_plan_ref else None,
        "contract_type": contract.get("contract_type"),
        "contract_version": contract.get("contract_version"),
        "plan_type": plan.get("plan_type"),
        "plan_version": plan.get("plan_version"),
        "execution_mode": plan.get("execution_mode"),
        "error_count": len(errors),
        "errors": errors,
        "execution_entry_count": len(_list(plan.get("execution_entries"))),
        "tracked_exports_should_not_be_committed": True,
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed values, provenance, and exact forbidden tokens.",
            "Validation does not execute perception jobs.",
            "Validation does not infer tennis meaning.",
            "Validation does not mutate regression baselines.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_gated_perception_execution_report(
    *,
    plan_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT
    ),
    routing_contract_path: str | Path | None = None,
    routing_plan_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural report over a gameplay-gated perception execution plan."""

    generated_at = generated_at or datetime.now(UTC)
    plan_load = _load_json(
        plan_path,
        label="gameplay_gated_perception_execution_plan",
    )
    if plan_load.get("ok") is False:
        return plan_load
    plan = _dict(plan_load.get("data"))
    validation = validate_gameplay_gated_perception_execution_plan(
        plan_path=plan_path,
        contract_path=contract_path,
        routing_contract_path=routing_contract_path,
        routing_plan_path=routing_plan_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_plan",
            "error_count": validation.get("error_count"),
            "errors": validation.get("errors", []),
            "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
        }

    entries = _list(plan.get("execution_entries"))
    report = {
        "report_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_plan_path": str(Path(plan_path)),
        "source_contract_path": str(Path(contract_path)),
        "media_id": plan.get("media_id"),
        "execution_plan_id": plan.get("execution_plan_id"),
        "execution_mode": plan.get("execution_mode"),
        "summary": {
            **_execution_report_summary(entries),
            "validation_status": validation.get("status"),
            "validation_error_count": validation.get("error_count"),
        },
        "stage_summaries": _stage_summaries(entries),
        "window_summary": {
            "allowed_execution_window_count": len(
                _list(plan.get("allowed_execution_windows"))
            ),
            "skipped_window_count": len(_list(plan.get("skipped_windows"))),
            "review_required_window_count": len(
                _list(plan.get("review_required_windows"))
            ),
        },
        "next_execution_contract": {
            "this_report_executes_perception_jobs": False,
            "allowed_windows_can_constrain_future_perception_jobs": True,
            "skipped_windows_should_not_run_future_perception_jobs": True,
            "review_required_windows_need_operator_inspection": True,
        },
        "validation_snapshot": validation,
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _execution_entry(
    *,
    media_id: str,
    routing_entry: dict[str, Any],
    execution_mode: str,
) -> dict[str, Any]:
    segment_id = str(routing_entry.get("segment_id") or "missing_segment_candidate")
    downstream_stage = str(routing_entry.get("downstream_stage") or "not_applicable")
    decision, skip_reason = _decision_and_reason(
        routing_decision=str(routing_entry.get("routing_decision") or "not_assessed"),
        routing_skip_reason=str(routing_entry.get("skip_reason") or "not_applicable"),
    )
    if execution_mode == "validate_only":
        decision = "not_assessed"
        skip_reason = "unsafe_execution_mode"
    output_ref = None
    if execution_mode == "fixture_execution_only" and decision == "execute_on_gameplay_window":
        output_ref = {
            "output_ref_type": "fixture_execution_placeholder",
            "output_ref_id": _stable_id(
                "gameplay_gated_fixture_execution_ref_v1",
                media_id,
                segment_id,
                downstream_stage,
            ),
            "writes_observations": False,
            "runs_heavy_inference": False,
        }
    return {
        "execution_entry_id": _stable_id(
            "gameplay_gated_perception_execution_entry_v1",
            media_id,
            segment_id,
            downstream_stage,
            execution_mode,
        ),
        "media_id": media_id,
        "segment_id": segment_id,
        "segment_start_ms": routing_entry.get("segment_start_ms"),
        "segment_end_ms": routing_entry.get("segment_end_ms"),
        "downstream_stage": downstream_stage,
        "execution_decision": decision,
        "execution_mode": execution_mode,
        "skip_reason": skip_reason,
        "provenance_status": (
            "routing_entry_provenance_available"
            if segment_id != "missing_segment_candidate"
            else "missing"
        ),
        "expected_input_window": {
            "media_id": media_id,
            "segment_id": segment_id,
            "start_ms": routing_entry.get("segment_start_ms"),
            "end_ms": routing_entry.get("segment_end_ms"),
            "stage": downstream_stage,
        },
        "output_ref": output_ref,
        "source_routing_entry_id": routing_entry.get("routing_entry_id"),
        "source_routing_decision": routing_entry.get("routing_decision"),
        "source_routing_skip_reason": routing_entry.get("skip_reason"),
        "source_routing_warnings": _dict(routing_entry.get("warnings")),
        "source_segment_warnings": _dict(routing_entry.get("source_segment_warnings")),
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }


def _decision_and_reason(
    *,
    routing_decision: str,
    routing_skip_reason: str,
) -> tuple[str, str]:
    if routing_decision == "allow_downstream_observation":
        return "execute_on_gameplay_window", "not_applicable"
    if routing_decision == "require_human_review":
        return "require_human_review", _normalize_skip_reason(
            routing_skip_reason,
            fallback="explicit_review_required",
        )
    if routing_decision == "skip_uncertain":
        return "skip_uncertain_window", "uncertain_segment"
    if routing_decision in {
        "skip_non_gameplay",
        "block_downstream_observation",
    }:
        return "skip_non_gameplay_window", _normalize_skip_reason(
            routing_skip_reason,
            fallback="non_gameplay_segment_candidate",
        )
    if routing_decision == "preserve_existing_behavior":
        return "preserve_existing_behavior", "not_applicable"
    if routing_decision in {"not_assessed", "not_applicable"}:
        return routing_decision, "not_applicable"
    return "not_assessed", "missing_segment_candidate"


def _execution_windows_from_routing_plan(
    *,
    media_id: str,
    plan: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    windows = {
        "allowed_execution_windows": [],
        "skipped_windows": [],
        "review_required_windows": [],
    }
    for window in _list(plan.get("allowed_windows")):
        if isinstance(window, dict):
            windows["allowed_execution_windows"].append(
                _execution_window(
                    media_id=media_id,
                    window=window,
                    window_collection="allowed_execution_windows",
                    execution_decision="execute_on_gameplay_window",
                    skip_reason="not_applicable",
                )
            )
    for window in _list(plan.get("blocked_windows")):
        if isinstance(window, dict):
            windows["skipped_windows"].append(
                _execution_window(
                    media_id=media_id,
                    window=window,
                    window_collection="skipped_windows",
                    execution_decision="skip_non_gameplay_window",
                    skip_reason=_window_skip_reason(window),
                )
            )
    for window in _list(plan.get("uncertain_windows")):
        if isinstance(window, dict):
            windows["review_required_windows"].append(
                _execution_window(
                    media_id=media_id,
                    window=window,
                    window_collection="review_required_windows",
                    execution_decision="require_human_review",
                    skip_reason=_window_skip_reason(
                        window,
                        fallback="explicit_review_required",
                    ),
                )
            )
    return windows


def _execution_window(
    *,
    media_id: str,
    window: dict[str, Any],
    window_collection: str,
    execution_decision: str,
    skip_reason: str,
) -> dict[str, Any]:
    segment_id = str(window.get("segment_id") or "missing_segment_candidate")
    return {
        "execution_window_id": _stable_id(
            "gameplay_gated_perception_execution_window_v1",
            media_id,
            segment_id,
            window_collection,
            window.get("segment_start_ms"),
            window.get("segment_end_ms"),
        ),
        "media_id": media_id,
        "segment_id": segment_id,
        "segment_start_ms": window.get("segment_start_ms"),
        "segment_end_ms": window.get("segment_end_ms"),
        "segment_status": window.get("segment_status"),
        "downstream_gate_status": window.get("downstream_gate_status"),
        "execution_decision": execution_decision,
        "skip_reason": skip_reason,
        "provenance_status": (
            "skipped_window_provenance_available"
            if window_collection == "skipped_windows"
            else "window_provenance_available"
        ),
        "source_routing_window_id": window.get("window_id"),
        "source_routing_warnings": _dict(window.get("warnings")),
        "source_segment_warnings": _dict(window.get("source_segment_warnings")),
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
    }


def _window_skip_reason(
    window: dict[str, Any],
    *,
    fallback: str = "non_gameplay_segment_candidate",
) -> str:
    segment_status = str(window.get("segment_status") or "")
    if segment_status == "short_segment_filtered":
        return "short_segment_filtered"
    if segment_status == "uncertain_segment":
        return "uncertain_segment"
    if segment_status == "non_gameplay_segment_candidate":
        return "non_gameplay_segment_candidate"
    return fallback


def _execution_summary(
    *,
    entries: list[dict[str, Any]],
    perception_stages: list[str],
    windows: dict[str, list[dict[str, Any]]],
    routing_entry_count: int,
) -> dict[str, Any]:
    decision_counts = Counter(entry["execution_decision"] for entry in entries)
    skip_counts = Counter(entry["skip_reason"] for entry in entries)
    stage_counts = Counter(entry["downstream_stage"] for entry in entries)
    provenance_counts = Counter(entry["provenance_status"] for entry in entries)
    return {
        "routing_entry_count": routing_entry_count,
        "perception_stage_count": len(perception_stages),
        "execution_entry_count": len(entries),
        "execution_decision_counts": dict(sorted(decision_counts.items())),
        "skip_reason_counts": dict(sorted(skip_counts.items())),
        "perception_stage_entry_counts": dict(sorted(stage_counts.items())),
        "provenance_status_counts": dict(sorted(provenance_counts.items())),
        "allowed_execution_window_count": len(windows["allowed_execution_windows"]),
        "skipped_window_count": len(windows["skipped_windows"]),
        "review_required_window_count": len(windows["review_required_windows"]),
        "perception_jobs_executed": False,
        "gpu_or_model_inference_executed": False,
        "observations_written": False,
    }


def _execution_report_summary(entries: list[Any]) -> dict[str, Any]:
    decision_counts = Counter(
        entry.get("execution_decision")
        for entry in entries
        if isinstance(entry, dict) and entry.get("execution_decision")
    )
    skip_counts = Counter(
        entry.get("skip_reason")
        for entry in entries
        if isinstance(entry, dict) and entry.get("skip_reason")
    )
    return {
        "execution_entry_count": len(entries),
        "execute_entry_count": decision_counts.get("execute_on_gameplay_window", 0),
        "skip_entry_count": (
            decision_counts.get("skip_non_gameplay_window", 0)
            + decision_counts.get("skip_uncertain_window", 0)
        ),
        "review_required_entry_count": decision_counts.get("require_human_review", 0),
        "execution_decision_counts": dict(sorted(decision_counts.items())),
        "skip_reason_counts": dict(sorted(skip_counts.items())),
        "perception_jobs_executed": False,
        "gpu_or_model_inference_executed": False,
        "observations_written": False,
    }


def _stage_summaries(entries: list[Any]) -> list[dict[str, Any]]:
    by_stage: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        by_stage.setdefault(str(entry.get("downstream_stage")), []).append(entry)
    summaries = []
    for stage, stage_entries in sorted(by_stage.items()):
        decision_counts = Counter(entry.get("execution_decision") for entry in stage_entries)
        summaries.append(
            {
                "downstream_stage": stage,
                "execution_entry_count": len(stage_entries),
                "execution_decision_counts": dict(sorted(decision_counts.items())),
                "perception_jobs_executed": False,
                "gpu_or_model_inference_executed": False,
                "observations_written": False,
            }
        )
    return summaries


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "execution_scope",
        "source_contract_refs",
        "routing_plan_contract_ref",
        "perception_stage_schema",
        "execution_plan_schema",
        "skipped_window_schema",
        "execution_summary_schema",
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
    if (
        refs.get("gameplay_gated_pipeline_routing_contract_version")
        != GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_source_routing_version",
                "source_contract_refs.gameplay_gated_pipeline_routing_contract_version",
                refs.get("gameplay_gated_pipeline_routing_contract_version"),
            )
        )
    return errors


def _validate_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(plan, path="plan")
    if plan.get("plan_type") != GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_TYPE:
        errors.append(_error("invalid_plan_type", "plan_type", plan.get("plan_type")))
    if plan.get("plan_version") != GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_VERSION:
        errors.append(
            _error("invalid_plan_version", "plan_version", plan.get("plan_version"))
        )
    for section in (
        "execution_plan_id",
        "media_id",
        "source_media_path",
        "routing_plan_path",
        "generated_at",
        "execution_mode",
        "perception_stages",
        "allowed_execution_windows",
        "skipped_windows",
        "review_required_windows",
        "execution_entries",
        "summary",
        "warnings",
    ):
        if section not in plan:
            errors.append(_error("missing_plan_section", section, None))
    if plan.get("execution_mode") not in ALLOWED_EXECUTION_MODES:
        errors.append(
            _error("invalid_execution_mode", "execution_mode", plan.get("execution_mode"))
        )
    for index, stage in enumerate(_list(plan.get("perception_stages"))):
        if stage not in DEFAULT_PERCEPTION_STAGES:
            errors.append(
                _error("invalid_perception_stage", f"perception_stages[{index}]", stage)
            )
    for collection_name in (
        "allowed_execution_windows",
        "skipped_windows",
        "review_required_windows",
    ):
        for index, window in enumerate(_list(plan.get(collection_name))):
            if not isinstance(window, dict):
                errors.append(_error("invalid_window", f"{collection_name}[{index}]", window))
                continue
            _validate_window_shape(errors, collection_name, index, window)
    for index, entry in enumerate(_list(plan.get("execution_entries"))):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_execution_entry", f"execution_entries[{index}]", entry))
            continue
        _validate_entry_shape(errors, index, entry)
    return errors


def _validate_window_shape(
    errors: list[dict[str, Any]],
    collection_name: str,
    index: int,
    window: dict[str, Any],
) -> None:
    decision = window.get("execution_decision")
    skip_reason = window.get("skip_reason")
    provenance_status = window.get("provenance_status")
    if not window.get("segment_id"):
        errors.append(_error("missing_window_segment_id", f"{collection_name}[{index}]", None))
    if decision not in ALLOWED_EXECUTION_DECISIONS:
        errors.append(
            _error(
                "invalid_window_execution_decision",
                f"{collection_name}[{index}].execution_decision",
                decision,
            )
        )
    if skip_reason not in ALLOWED_SKIP_REASONS:
        errors.append(
            _error(
                "invalid_window_skip_reason",
                f"{collection_name}[{index}].skip_reason",
                skip_reason,
            )
        )
    if provenance_status not in ALLOWED_PROVENANCE_STATUSES:
        errors.append(
            _error(
                "invalid_window_provenance_status",
                f"{collection_name}[{index}].provenance_status",
                provenance_status,
            )
        )


def _validate_entry_shape(
    errors: list[dict[str, Any]],
    index: int,
    entry: dict[str, Any],
) -> None:
    decision = entry.get("execution_decision")
    skip_reason = entry.get("skip_reason")
    provenance_status = entry.get("provenance_status")
    stage = entry.get("downstream_stage")
    if decision not in ALLOWED_EXECUTION_DECISIONS:
        errors.append(
            _error(
                "invalid_execution_decision",
                f"execution_entries[{index}].execution_decision",
                decision,
            )
        )
    if skip_reason not in ALLOWED_SKIP_REASONS:
        errors.append(
            _error(
                "invalid_skip_reason",
                f"execution_entries[{index}].skip_reason",
                skip_reason,
            )
        )
    if provenance_status not in ALLOWED_PROVENANCE_STATUSES:
        errors.append(
            _error(
                "invalid_provenance_status",
                f"execution_entries[{index}].provenance_status",
                provenance_status,
            )
        )
    if stage not in DEFAULT_PERCEPTION_STAGES:
        errors.append(
            _error(
                "invalid_execution_entry_stage",
                f"execution_entries[{index}].downstream_stage",
                stage,
            )
        )
    if not entry.get("segment_id"):
        errors.append(_error("missing_entry_segment_id", f"execution_entries[{index}]", None))
    if not entry.get("execution_entry_id"):
        errors.append(_error("missing_entry_id", f"execution_entries[{index}]", None))
    expected_input_window = entry.get("expected_input_window")
    if not isinstance(expected_input_window, dict):
        errors.append(
            _error(
                "missing_expected_input_window",
                f"execution_entries[{index}].expected_input_window",
                expected_input_window,
            )
        )


def _normalize_perception_stages(value: list[str] | str | None) -> list[str]:
    if value is None:
        return list(DEFAULT_PERCEPTION_STAGES)
    if isinstance(value, str):
        if not value.strip():
            return list(DEFAULT_PERCEPTION_STAGES)
        return [item.strip() for item in value.split(",") if item.strip()]
    return [item.strip() for item in value if item and item.strip()]


def _normalize_skip_reason(value: str, *, fallback: str) -> str:
    return value if value in ALLOWED_SKIP_REASONS else fallback


def _validate_execution_mode(mode: str) -> dict[str, Any] | None:
    if mode not in ALLOWED_EXECUTION_MODES:
        return _failed("invalid_execution_mode", f"unsupported execution mode: {mode}")
    return None


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_EXECUTION_TOKENS:
                errors.append(_error("forbidden_token_key", child_path, key))
            errors.extend(_forbidden_token_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_EXECUTION_TOKENS:
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
        "warnings": dict(GAMEPLAY_GATED_PERCEPTION_EXECUTION_WARNINGS),
        **extra,
    }


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_GATED_PERCEPTION_EXECUTION_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATED_PERCEPTION_EXECUTION_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
