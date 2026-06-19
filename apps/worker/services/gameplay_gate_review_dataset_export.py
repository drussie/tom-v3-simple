from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
    DEFAULT_GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT,
    GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_many_point_smoke import (
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_perception_execution import (
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
    build_gameplay_gated_perception_execution_plan,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
    build_gameplay_gated_routing_plan,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    build_gameplay_segment_candidates,
)
from apps.worker.services.gameplay_segment_replay_review import (
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
    build_gameplay_segment_replay_timeline,
)
from apps.worker.services.many_point_ingestion_gate import (
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)

GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE = (
    "gameplay_gate_review_dataset_export_contract"
)
GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION = "v1"
GAMEPLAY_GATE_REVIEW_DATASET_TYPE = "gameplay_gate_review_dataset"
GAMEPLAY_GATE_REVIEW_DATASET_VERSION = "v1"
GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_TYPE = (
    "gameplay_gate_review_dataset_validation"
)
GAMEPLAY_GATE_REVIEW_DATASET_REPORT_TYPE = "gameplay_gate_review_dataset_report"
GAMEPLAY_GATE_REVIEW_DATASET_BLUEPRINT = "blueprint_44"
GAMEPLAY_GATE_REVIEW_DATASET_BLUEPRINT_NAME = (
    "gameplay_gate_review_dataset_export_v1"
)

DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_gate_review_dataset_export_contract_v1.json"
)
DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT = (
    ".data/exports/gameplay_gate_review_dataset.current.json"
)
DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_gate_review_dataset.validation.json"
)
DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_REPORT_OUTPUT = (
    ".data/exports/gameplay_gate_review_dataset.report.json"
)
DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_WORK_DIR = (
    ".data/exports/gameplay_gate_review_dataset"
)
DEFAULT_GAMEPLAY_GATE_REVIEW_FIXTURE_MEDIA_PATH = "demo_assets/sample_point.mp4"
DEFAULT_VIEWER_BASE_URL = "http://127.0.0.1:3000"

GAMEPLAY_GATE_REVIEW_DATASET_EXPORTED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)

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
    "warmup_or_practice_possible",
    "camera_cut_unclear",
    "short_segment_unclear",
    "classifier_boundary_unclear",
    "not_applicable",
}
ALLOWED_PROVENANCE_STATUSES = {
    "source_artifacts_available",
    "partial_source_context",
    "missing_source_context",
}

FORBIDDEN_REVIEW_DATASET_TOKENS = {
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
    "generalization_proven",
    "production_ready_truth",
    "classifier_accuracy_claim",
    "reviewer_score",
    "reviewer_rank",
}

REVIEW_DATASET_WARNINGS = {
    "dataset_is_not_truth": True,
    "review_dataset_export_only": True,
    "human_review_metadata_only": True,
    "classifier_correctness_not_assessed": True,
    "generalization_not_claimed": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_model_assets": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_relabel_automatically": True,
    "no_adjudication": True,
    "observation_only": True,
    "review_support_only": True,
}

NON_CLAIMS = {
    "not_classifier_correctness_benchmark": True,
    "not_point_detection": True,
    "not_scoring": True,
    "not_line_calling": True,
    "not_generalization_claim": True,
    "not_production_readiness_claim": True,
    "not_training_label_source": True,
}

SOURCE_CONTRACT_REFS = {
    "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    "gameplay_gated_pipeline_routing_contract_version": (
        GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
    ),
    "gameplay_gated_perception_execution_contract_version": (
        GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
    ),
    "gameplay_segment_replay_review_contract_version": (
        GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION
    ),
    "gameplay_gated_many_point_smoke_contract_version": (
        GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION
    ),
    "gameplay_gate_regression_baseline_contract_version": (
        GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION
    ),
    "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
    "observation_quality_taxonomy_version": "v1",
    "review_label_schema_version": "v1",
    "reviewer_confidence_schema_version": "v1",
    "multi_reviewer_disagreement_schema_version": "v1",
    "intennse_label_alignment_contract_version": "v1",
    "versioned_dataset_corpus_contract_version": "v1",
    "coverage_sampling_strategy_contract_version": "v1",
    "review_ops_metrics_contract_version": "v1",
    "label_feedback_evaluation_contract_version": "v1",
    "camera_geometry_calibration_provenance_contract_version": "v1",
    "tom_v3_expansion_completion_freeze_version": "v1",
    "multi_point_regression_matrix_version": "v0",
    "point_manifest_version": "v0",
}


def export_gameplay_gate_review_dataset_contract(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or GAMEPLAY_GATE_REVIEW_DATASET_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
        "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
        "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
        "contract": contract,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_gate_review_dataset(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT,
    gameplay_segments_path: str | Path | None = None,
    routing_plan_path: str | Path | None = None,
    execution_plan_path: str | Path | None = None,
    replay_timeline_path: str | Path | None = None,
    regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    regression_verification_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT
    ),
    work_dir: str | Path = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_WORK_DIR,
    fixture_media_path: str | Path = DEFAULT_GAMEPLAY_GATE_REVIEW_FIXTURE_MEDIA_PATH,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    viewer_base_url: str = DEFAULT_VIEWER_BASE_URL,
    generated_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_build("contract_invalid", errors, output_path)

    paths_result = _ensure_source_artifacts(
        gameplay_segments_path=gameplay_segments_path,
        routing_plan_path=routing_plan_path,
        execution_plan_path=execution_plan_path,
        replay_timeline_path=replay_timeline_path,
        work_dir=work_dir,
        fixture_media_path=fixture_media_path,
        model_asset_path=model_asset_path,
        viewer_base_url=viewer_base_url,
        generated_at=generated_at,
        probe_runner=probe_runner,
    )
    if paths_result.get("ok") is False:
        return _failed_build(
            "source_artifact_build_failed",
            _list(paths_result.get("errors")),
            output_path,
        )
    source_paths = _dict(paths_result.get("source_paths"))

    gameplay = _load_required_json(
        source_paths.get("gameplay_segments_path"),
        "gameplay_segment_candidates",
        errors,
    )
    routing = _load_optional_json(source_paths.get("routing_plan_path"), "routing_plan")
    execution = _load_optional_json(
        source_paths.get("execution_plan_path"),
        "execution_plan",
    )
    timeline = _load_optional_json(
        source_paths.get("replay_timeline_path"),
        "replay_timeline",
    )
    baseline = _load_optional_json(regression_baseline_path, "regression_baseline")
    verification = _load_optional_json(
        regression_verification_path,
        "regression_verification",
    )
    if errors:
        return _failed_build("source_artifact_invalid", errors, output_path)

    dataset = _dataset_from_sources(
        contract=contract,
        gameplay=gameplay,
        routing=routing,
        execution=execution,
        timeline=timeline,
        baseline=baseline,
        verification=verification,
        source_paths={
            **source_paths,
            "contract_path": str(Path(contract_path)),
            "regression_baseline_path": (
                str(Path(regression_baseline_path))
                if regression_baseline_path is not None
                and Path(regression_baseline_path).expanduser().is_file()
                else None
            ),
            "regression_verification_path": (
                str(Path(regression_verification_path))
                if regression_verification_path is not None
                and Path(regression_verification_path).expanduser().is_file()
                else None
            ),
        },
        generated_at=generated_at,
        viewer_base_url=viewer_base_url,
    )
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
        "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
        "dataset_id": dataset["dataset_id"],
        "entry_count": len(_list(dataset.get("entries"))),
        "summary": dataset["summary"],
        "dataset": dataset,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
    }
    _write_json_if_requested(output_path, dataset, result, "dataset_output")
    return result


def validate_gameplay_gate_review_dataset(
    *,
    dataset_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    dataset = _load_required_json(dataset_path, "gameplay_gate_review_dataset", errors)
    if dataset:
        errors.extend(_validate_dataset_shape(dataset))
        errors.extend(_forbidden_token_errors(dataset, path="dataset"))
        errors.extend(_validate_source_contract_refs(dataset))
    if contract:
        errors.extend(_forbidden_token_errors(contract, path="contract"))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_TYPE,
        "validation_version": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "dataset_path": str(Path(dataset_path)),
        "contract_type": contract.get("contract_type") if contract else None,
        "contract_version": contract.get("contract_version") if contract else None,
        "dataset_type": dataset.get("dataset_type") if dataset else None,
        "dataset_version": dataset.get("dataset_version") if dataset else None,
        "entry_count": len(_list(dataset.get("entries"))) if dataset else 0,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed review metadata values, provenance refs, "
            "and exact forbidden tokens.",
            "Validation does not infer review labels.",
            "Validation does not assess classifier correctness.",
            "Validation does not create event labels or point labels.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_gate_review_dataset_report(
    *,
    dataset_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    dataset_load = _load_json(dataset_path, label="gameplay_gate_review_dataset")
    if dataset_load.get("ok") is False:
        return dataset_load
    dataset = _dict(dataset_load.get("data"))
    validation = validate_gameplay_gate_review_dataset(
        dataset_path=dataset_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_dataset",
            "error_count": validation.get("error_count"),
            "errors": validation.get("errors", []),
            "warnings": dict(REVIEW_DATASET_WARNINGS),
        }

    entries = [entry for entry in _list(dataset.get("entries")) if isinstance(entry, dict)]
    report = {
        "report_type": GAMEPLAY_GATE_REVIEW_DATASET_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_dataset_path": str(Path(dataset_path)),
        "source_contract_path": str(Path(contract_path)),
        "dataset_id": dataset.get("dataset_id"),
        "dataset_version": dataset.get("dataset_version"),
        "entry_count": len(entries),
        "summary": _report_summary(dataset=dataset, entries=entries),
        "model_asset_provenance": {
            "model_asset_ref": dataset.get("model_asset_ref"),
            "model_asset_sha256": dataset.get("model_asset_sha256"),
            "model_asset_exists": dataset.get("model_asset_exists"),
        },
        "status_distributions": {
            "segment_status": _counter(entries, "segment_status"),
            "downstream_gate_status": _counter(entries, "downstream_gate_status"),
            "review_status": _counter(entries, "review_status"),
            "review_confidence": _counter_human_review(entries, "review_confidence"),
        },
        "ambiguity_field_distribution": _ambiguity_flag_distribution(entries),
        "missing_source_context": _missing_source_context(entries),
        "validation_snapshot": validation,
        "warnings": {
            **dict(REVIEW_DATASET_WARNINGS),
            **_dict(dataset.get("warnings")),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": GAMEPLAY_GATE_REVIEW_DATASET_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
        "dataset_id": dataset.get("dataset_id"),
        "entry_count": len(entries),
        "summary": report["summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "dataset_scope": {
            "purpose": "gameplay_gate_human_review_dataset_export",
            "reads_gameplay_segment_candidates": True,
            "reads_routing_plan_when_supplied": True,
            "reads_execution_plan_when_supplied": True,
            "reads_replay_timeline_when_supplied": True,
            "reads_regression_context_when_supplied": True,
            "creates_review_dataset_export": True,
            "creates_review_labels": False,
            "runs_gpu_or_model_inference": False,
            "mutates_model_assets": False,
            "mutates_regression_baselines": False,
            "automatic_relabeling_allowed": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "dataset_schema": {
            "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
            "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
            "required_fields": [
                "dataset_id",
                "dataset_version",
                "generated_at",
                "source_paths",
                "model_asset_ref",
                "model_asset_sha256",
                "threshold",
                "smoothing_window",
                "hysteresis_settings",
                "entries",
                "summary",
                "warnings",
                "non_claims",
            ],
        },
        "review_entry_schema": {
            "required_fields": [
                "review_entry_id",
                "media_id",
                "source_media_path",
                "replay_url",
                "segment_id",
                "segment_start_ms",
                "segment_end_ms",
                "start_frame_index",
                "end_frame_index",
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
                "review_status",
                "human_review_fields",
                "provenance_status",
                "warnings",
            ],
            "allowed_reviewed_segment_statuses": sorted(ALLOWED_REVIEWED_SEGMENT_STATUSES),
            "allowed_reviewed_downstream_gate_statuses": sorted(
                ALLOWED_REVIEWED_DOWNSTREAM_GATE_STATUSES
            ),
            "allowed_review_confidence_values": sorted(ALLOWED_REVIEW_CONFIDENCE_VALUES),
            "allowed_ambiguity_flags": sorted(ALLOWED_AMBIGUITY_FLAGS),
        },
        "review_annotation_template_schema": {
            "fields": [
                "reviewer_id",
                "reviewed_at",
                "reviewed_segment_status",
                "reviewed_downstream_gate_status",
                "review_confidence",
                "ambiguity_flags",
                "reviewer_notes",
                "needs_additional_review",
            ],
            "human_review_fields_are_metadata_only": True,
            "review_values_do_not_modify_source_artifacts": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_review_dataset_shape": True,
            "validate_review_entry_shape": True,
            "validate_allowed_statuses": True,
            "validate_allowed_confidence_values": True,
            "validate_allowed_ambiguity_flags": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "source_paths_required": True,
            "segment_id_required": True,
            "replay_url_required": True,
            "model_asset_provenance_preserved": True,
            "gate_config_preserved": True,
            "baseline_context_preserved_when_available": True,
            "warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(REVIEW_DATASET_WARNINGS),
    }


def _ensure_source_artifacts(
    *,
    gameplay_segments_path: str | Path | None,
    routing_plan_path: str | Path | None,
    execution_plan_path: str | Path | None,
    replay_timeline_path: str | Path | None,
    work_dir: str | Path,
    fixture_media_path: str | Path,
    model_asset_path: str | Path,
    viewer_base_url: str,
    generated_at: datetime,
    probe_runner: Any | None,
) -> dict[str, Any]:
    root = Path(work_dir).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, Any]] = []

    gameplay_path = Path(gameplay_segments_path).expanduser() if gameplay_segments_path else None
    if gameplay_path is None or not gameplay_path.is_file():
        gameplay_path = root / "gameplay_segment_candidates.json"
        result = build_gameplay_segment_candidates(
            local_media_path=fixture_media_path,
            output_path=gameplay_path,
            media_id="gameplay_gate_review_dataset_fixture_media",
            model_asset_path=model_asset_path,
            viewer_base_url=viewer_base_url,
            generated_at=generated_at,
            probe_runner=probe_runner,
        )
        if result.get("ok") is False:
            errors.append(_error("gameplay_segment_build_failed", "gameplay_segments", result))

    routing_path = Path(routing_plan_path).expanduser() if routing_plan_path else None
    if not errors and (routing_path is None or not routing_path.is_file()):
        routing_path = root / "gameplay_gated_routing_plan.json"
        result = build_gameplay_gated_routing_plan(
            gameplay_segments_path=gameplay_path,
            gameplay_gate_contract_path=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
            output_path=routing_path,
            routing_mode="dry_run",
            generated_at=generated_at,
        )
        if result.get("ok") is False:
            errors.append(_error("routing_plan_build_failed", "routing_plan", result))

    execution_path = Path(execution_plan_path).expanduser() if execution_plan_path else None
    if not errors and (execution_path is None or not execution_path.is_file()):
        execution_path = root / "gameplay_gated_execution_plan.json"
        result = build_gameplay_gated_perception_execution_plan(
            routing_plan_path=routing_path,
            routing_contract_path=DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
            output_path=execution_path,
            execution_mode="dry_run",
            generated_at=generated_at,
        )
        if result.get("ok") is False:
            errors.append(_error("execution_plan_build_failed", "execution_plan", result))

    timeline_path = Path(replay_timeline_path).expanduser() if replay_timeline_path else None
    if not errors and (timeline_path is None or not timeline_path.is_file()):
        timeline_path = root / "gameplay_segment_replay_timeline.json"
        result = build_gameplay_segment_replay_timeline(
            gameplay_segments_path=gameplay_path,
            routing_plan_path=routing_path,
            execution_plan_path=execution_path,
            viewer_base_url=viewer_base_url,
            output_path=timeline_path,
            generated_at=generated_at,
        )
        if result.get("ok") is False:
            errors.append(_error("replay_timeline_build_failed", "replay_timeline", result))

    if errors:
        return {"ok": False, "errors": errors}
    return {
        "ok": True,
        "source_paths": {
            "gameplay_segments_path": str(gameplay_path),
            "routing_plan_path": str(routing_path) if routing_path else None,
            "execution_plan_path": str(execution_path) if execution_path else None,
            "replay_timeline_path": str(timeline_path) if timeline_path else None,
        },
    }


def _dataset_from_sources(
    *,
    contract: dict[str, Any],
    gameplay: dict[str, Any],
    routing: dict[str, Any],
    execution: dict[str, Any],
    timeline: dict[str, Any],
    baseline: dict[str, Any],
    verification: dict[str, Any],
    source_paths: dict[str, Any],
    generated_at: datetime,
    viewer_base_url: str,
) -> dict[str, Any]:
    segments = [
        item for item in _list(gameplay.get("segment_candidates")) if isinstance(item, dict)
    ]
    classifications = [
        item for item in _list(gameplay.get("classifications")) if isinstance(item, dict)
    ]
    routing_by_segment = _first_by_segment(_list(routing.get("routing_entries")))
    execution_by_segment = _first_by_segment(_list(execution.get("execution_entries")))
    timeline_by_segment = _timeline_by_segment(_list(timeline.get("timeline_entries")))
    baseline_context = _baseline_context(baseline=baseline, verification=verification)
    config = _dict(gameplay.get("gate_config"))
    model_asset = _dict(gameplay.get("model_asset"))
    media_id = str(gameplay.get("media_id") or "unknown_media")
    replay_url = str(
        timeline.get("replay_url")
        or gameplay.get("replay_url")
        or f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
    )
    entries = [
        _review_entry(
            segment=segment,
            classification=_classification_for_segment(segment, classifications),
            routing_entry=routing_by_segment.get(str(segment.get("segment_id")), {}),
            execution_entry=execution_by_segment.get(str(segment.get("segment_id")), {}),
            timeline_entry=timeline_by_segment.get(str(segment.get("segment_id")), {}),
            baseline_context=baseline_context,
            replay_url=replay_url,
            source_media_path=gameplay.get("source_media_path"),
        )
        for segment in segments
    ]
    dataset_id = _stable_id(
        "gameplay_gate_review_dataset_v1",
        media_id,
        source_paths,
        model_asset.get("model_asset_sha256"),
        len(entries),
    )
    return {
        "dataset_id": dataset_id,
        "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
        "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_paths": source_paths,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "contract_version": contract.get("contract_version"),
        "media_id": media_id,
        "source_media_path": gameplay.get("source_media_path"),
        "source_uri": gameplay.get("source_uri"),
        "replay_url": replay_url,
        "model_asset_ref": model_asset.get("model_asset_ref"),
        "model_asset_sha256": model_asset.get("model_asset_sha256"),
        "model_asset_exists": model_asset.get("model_asset_exists") is True,
        "threshold": config.get("threshold"),
        "smoothing_window": config.get("smoothing_window"),
        "hysteresis_settings": _dict(config.get("hysteresis")),
        "entries": entries,
        "summary": _dataset_summary(entries),
        "review_annotation_template": _default_human_review_fields(),
        "baseline_context": baseline_context,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }


def _review_entry(
    *,
    segment: dict[str, Any],
    classification: dict[str, Any],
    routing_entry: dict[str, Any],
    execution_entry: dict[str, Any],
    timeline_entry: dict[str, Any],
    baseline_context: dict[str, Any],
    replay_url: str,
    source_media_path: Any,
) -> dict[str, Any]:
    segment_id = str(segment.get("segment_id") or "missing_segment_candidate")
    gameplay_probability = _probability(segment.get("mean_gameplay_probability"))
    return {
        "review_entry_id": _stable_id(
            "gameplay_gate_review_entry_v1",
            segment.get("media_id"),
            segment_id,
            segment.get("segment_start_ms"),
            segment.get("segment_end_ms"),
        ),
        "media_id": segment.get("media_id"),
        "source_media_path": source_media_path,
        "replay_url": _segment_replay_url(replay_url, segment),
        "segment_id": segment_id,
        "segment_start_ms": segment.get("segment_start_ms"),
        "segment_end_ms": segment.get("segment_end_ms"),
        "start_frame_index": segment.get("start_frame_index"),
        "end_frame_index": segment.get("end_frame_index"),
        "gameplay_probability": gameplay_probability,
        "non_gameplay_probability": round(1.0 - gameplay_probability, 6),
        "raw_status": classification.get("raw_status") or _raw_status_from_segment(segment),
        "smoothed_status": (
            classification.get("smoothed_status") or _raw_status_from_segment(segment)
        ),
        "segment_status": segment.get("segment_status") or "not_applicable",
        "downstream_gate_status": (
            segment.get("downstream_gate_status") or "not_applicable"
        ),
        "routing_decision": routing_entry.get("routing_decision") or "not_applicable",
        "execution_decision": execution_entry.get("execution_decision") or "not_applicable",
        "replay_timeline_entry_id": timeline_entry.get("timeline_entry_id"),
        "baseline_context": baseline_context,
        "review_status": "not_reviewed",
        "human_review_fields": _default_human_review_fields(),
        "provenance_status": _provenance_status(routing_entry, execution_entry, timeline_entry),
        "warnings": {
            **dict(REVIEW_DATASET_WARNINGS),
            "gameplay_candidate_for_review": segment.get("segment_status")
            == "gameplay_segment_candidate",
            "non_gameplay_candidate_for_review": segment.get("segment_status")
            == "non_gameplay_segment_candidate",
            "uncertain_segment_for_review": segment.get("segment_status")
            == "uncertain_segment",
            "human_review_pending": True,
        },
    }


def _default_human_review_fields() -> dict[str, Any]:
    return {
        "reviewer_id": None,
        "reviewed_at": None,
        "reviewed_segment_status": "not_reviewed",
        "reviewed_downstream_gate_status": "no_review_decision",
        "review_confidence": "not_assessed",
        "ambiguity_flags": [],
        "reviewer_notes": None,
        "needs_additional_review": False,
    }


def _dataset_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "entry_count": len(entries),
        "review_entry_present_count": len(entries),
        "human_review_pending_count": sum(
            1 for entry in entries if entry.get("review_status") == "not_reviewed"
        ),
        "gameplay_candidate_for_review_count": sum(
            1
            for entry in entries
            if entry.get("segment_status") == "gameplay_segment_candidate"
        ),
        "non_gameplay_candidate_for_review_count": sum(
            1
            for entry in entries
            if entry.get("segment_status") == "non_gameplay_segment_candidate"
        ),
        "uncertain_segment_for_review_count": sum(
            1 for entry in entries if entry.get("segment_status") == "uncertain_segment"
        ),
        "missing_source_context_count": len(_missing_source_context(entries)),
        "classifier_correctness_not_assessed": True,
        "dataset_is_not_truth": True,
    }


def _report_summary(dataset: dict[str, Any], entries: list[dict[str, Any]]) -> dict[str, Any]:
    summary = _dataset_summary(entries)
    return {
        **summary,
        "dataset_id": dataset.get("dataset_id"),
        "model_asset_sha256_present": bool(dataset.get("model_asset_sha256")),
        "baseline_context_present": bool(_dict(dataset.get("baseline_context")).get("baseline_id")),
        "review_dataset_export_only": True,
        "classifier_correctness_not_assessed": True,
        "dataset_is_not_truth": True,
    }


def _validate_dataset_shape(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if dataset.get("dataset_type") != GAMEPLAY_GATE_REVIEW_DATASET_TYPE:
        errors.append(_error("invalid_dataset_type", "dataset_type", dataset.get("dataset_type")))
    if dataset.get("dataset_version") != GAMEPLAY_GATE_REVIEW_DATASET_VERSION:
        errors.append(
            _error("invalid_dataset_version", "dataset_version", dataset.get("dataset_version"))
        )
    required = [
        "dataset_id",
        "generated_at",
        "source_paths",
        "entries",
        "summary",
        "warnings",
        "non_claims",
    ]
    for field in required:
        if field not in dataset:
            errors.append(_error("missing_dataset_field", field, None))
    entries = dataset.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("entries_must_be_list", "entries", entries))
        return errors
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_review_entry", f"entries[{index}]", entry))
            continue
        errors.extend(_validate_review_entry(entry, index))
    return errors


def _validate_review_entry(entry: dict[str, Any], index: int) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    required = [
        "review_entry_id",
        "media_id",
        "source_media_path",
        "replay_url",
        "segment_id",
        "segment_start_ms",
        "segment_end_ms",
        "start_frame_index",
        "end_frame_index",
        "gameplay_probability",
        "non_gameplay_probability",
        "raw_status",
        "smoothed_status",
        "segment_status",
        "downstream_gate_status",
        "routing_decision",
        "execution_decision",
        "baseline_context",
        "review_status",
        "human_review_fields",
        "provenance_status",
        "warnings",
    ]
    for field in required:
        if field not in entry:
            errors.append(_error("missing_review_entry_field", f"entries[{index}].{field}", None))
    if entry.get("review_status") != "not_reviewed":
        errors.append(
            _error(
                "invalid_review_status",
                f"entries[{index}].review_status",
                entry.get("review_status"),
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
    human = _dict(entry.get("human_review_fields"))
    if human.get("reviewed_segment_status") not in ALLOWED_REVIEWED_SEGMENT_STATUSES:
        errors.append(
            _error(
                "invalid_reviewed_segment_status",
                f"entries[{index}].human_review_fields.reviewed_segment_status",
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
                f"entries[{index}].human_review_fields.reviewed_downstream_gate_status",
                human.get("reviewed_downstream_gate_status"),
            )
        )
    if human.get("review_confidence") not in ALLOWED_REVIEW_CONFIDENCE_VALUES:
        errors.append(
            _error(
                "invalid_review_confidence",
                f"entries[{index}].human_review_fields.review_confidence",
                human.get("review_confidence"),
            )
        )
    flags = human.get("ambiguity_flags")
    if not isinstance(flags, list):
        errors.append(
            _error(
                "ambiguity_flags_must_be_list",
                f"entries[{index}].human_review_fields.ambiguity_flags",
                flags,
            )
        )
    else:
        for flag in flags:
            if flag not in ALLOWED_AMBIGUITY_FLAGS:
                errors.append(
                    _error(
                        "invalid_ambiguity_flag",
                        f"entries[{index}].human_review_fields.ambiguity_flags",
                        flag,
                    )
                )
    return errors


def _validate_source_contract_refs(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    refs = _dict(dataset.get("source_contract_refs"))
    errors = []
    for field, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(field) != expected:
            errors.append(_error("invalid_source_contract_ref", field, refs.get(field)))
    return errors


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    contract = _load_required_json(contract_path, "gameplay_gate_review_dataset_contract", errors)
    if contract:
        if contract.get("contract_type") != GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_TYPE:
            errors.append(
                _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
            )
        if contract.get("contract_version") != GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION:
            errors.append(
                _error(
                    "invalid_contract_version",
                    "contract_version",
                    contract.get("contract_version"),
                )
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


def _failed_build(
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
        "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
    }
    payload = {
        "dataset_type": GAMEPLAY_GATE_REVIEW_DATASET_TYPE,
        "dataset_version": GAMEPLAY_GATE_REVIEW_DATASET_VERSION,
        "status": status,
        "errors": errors,
        "warnings": dict(REVIEW_DATASET_WARNINGS),
    }
    _write_json_if_requested(output_path, payload, result, "dataset_output")
    return result


def _first_by_segment(items: list[Any]) -> dict[str, dict[str, Any]]:
    by_segment: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        segment_id = str(item.get("segment_id") or "")
        if segment_id and segment_id not in by_segment:
            by_segment[segment_id] = item
    return by_segment


def _timeline_by_segment(items: list[Any]) -> dict[str, dict[str, Any]]:
    preferred_lanes = {
        "gameplay_segment_candidate",
        "non_gameplay_segment_candidate",
        "uncertain_segment",
    }
    by_segment: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        segment_id = str(item.get("segment_id") or "")
        if not segment_id:
            continue
        if segment_id not in by_segment or item.get("lane_type") in preferred_lanes:
            by_segment[segment_id] = item
    return by_segment


def _classification_for_segment(
    segment: dict[str, Any],
    classifications: list[dict[str, Any]],
) -> dict[str, Any]:
    start = _int_or_none(segment.get("start_frame_index"))
    end = _int_or_none(segment.get("end_frame_index"))
    if start is None or end is None:
        return {}
    for item in classifications:
        frame_index = _int_or_none(item.get("frame_index"))
        if frame_index is not None and start <= frame_index <= end:
            return item
    return {}


def _baseline_context(*, baseline: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    summary = _dict(baseline.get("summary"))
    return {
        "baseline_id": baseline.get("baseline_id"),
        "baseline_version": baseline.get("baseline_version"),
        "baseline_type": baseline.get("baseline_type"),
        "verification_status": verification.get("status") or "not_supplied",
        "drift_detected": verification.get("drift_detected"),
        "breaking_drift_detected": verification.get("breaking_drift_detected"),
        "baseline_is_not_truth": True,
        "gameplay_gate_is_not_truth": True,
        "classifier_correctness_not_assessed": True,
        "generalization_not_claimed": True,
        "model_asset_sha256": baseline.get("model_asset_sha256")
        or summary.get("model_asset_sha256"),
        "threshold": baseline.get("threshold") or summary.get("threshold"),
        "smoothing_window": baseline.get("smoothing_window") or summary.get("smoothing_window"),
        "hysteresis_settings": _dict(
            baseline.get("hysteresis_settings") or summary.get("hysteresis_settings")
        ),
    }


def _probability(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 0.0
    return round(max(0.0, min(1.0, numeric)), 6)


def _raw_status_from_segment(segment: dict[str, Any]) -> str:
    segment_status = str(segment.get("segment_status") or "")
    if segment_status == "gameplay_segment_candidate":
        return "gameplay_candidate"
    if segment_status == "non_gameplay_segment_candidate":
        return "non_gameplay_candidate"
    if segment_status == "uncertain_segment":
        return "uncertain"
    return "not_applicable"


def _segment_replay_url(replay_url: str, segment: dict[str, Any]) -> str:
    separator = "&" if "?" in replay_url else "?"
    start_ms = segment.get("segment_start_ms")
    end_ms = segment.get("segment_end_ms")
    segment_id = segment.get("segment_id")
    return f"{replay_url}{separator}segmentId={segment_id}&startMs={start_ms}&endMs={end_ms}"


def _provenance_status(
    routing_entry: dict[str, Any],
    execution_entry: dict[str, Any],
    timeline_entry: dict[str, Any],
) -> str:
    available = sum(bool(item) for item in (routing_entry, execution_entry, timeline_entry))
    if available == 3:
        return "source_artifacts_available"
    if available:
        return "partial_source_context"
    return "missing_source_context"


def _counter(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(Counter(str(entry.get(field) or "missing") for entry in entries))


def _counter_human_review(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(
        Counter(
            str(_dict(entry.get("human_review_fields")).get(field) or "missing")
            for entry in entries
        )
    )


def _ambiguity_flag_distribution(entries: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for entry in entries:
        flags = _dict(entry.get("human_review_fields")).get("ambiguity_flags")
        if not flags:
            counts["not_assessed"] += 1
            continue
        for flag in _list(flags):
            counts[str(flag)] += 1
    return dict(counts)


def _missing_source_context(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = []
    for entry in entries:
        if entry.get("provenance_status") != "source_artifacts_available":
            missing.append(
                {
                    "review_entry_id": entry.get("review_entry_id"),
                    "segment_id": entry.get("segment_id"),
                    "provenance_status": entry.get("provenance_status"),
                }
            )
    return missing


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_REVIEW_DATASET_TOKENS:
                errors.append(_error("forbidden_field_or_value", f"{path}.{key_text}", key_text))
            errors.extend(_forbidden_token_errors(nested, path=f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_REVIEW_DATASET_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))
    return errors


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None or not str(output_path).strip():
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result[result_key] = str(path)


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def _tom_provenance() -> dict[str, Any]:
    return {
        "blueprint": GAMEPLAY_GATE_REVIEW_DATASET_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATE_REVIEW_DATASET_BLUEPRINT_NAME,
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
    }


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "no_adjudication": True,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
