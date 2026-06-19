from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_pathway_completion_freeze import (
    GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gate_review_dataset_export import (
    DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT,
    GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION,
    build_gameplay_gate_review_dataset,
)
from apps.worker.services.gameplay_gated_many_point_smoke import (
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_perception_execution import (
    DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT,
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
    inspect_gameplay_classifier_asset,
)
from apps.worker.services.gameplay_segment_replay_review import (
    DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
    build_gameplay_segment_replay_timeline,
)
from apps.worker.services.many_point_ingestion_gate import (
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)

REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE = (
    "real_broadcast_gameplay_corpus_run_contract"
)
REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE = (
    "real_broadcast_gameplay_corpus_manifest"
)
REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE = "real_broadcast_gameplay_corpus_run"
REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE = (
    "real_broadcast_gameplay_corpus_report"
)
REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CORPUS_BLUEPRINT = "blueprint_46"
REAL_BROADCAST_GAMEPLAY_CORPUS_BLUEPRINT_NAME = (
    "real_broadcast_gameplay_gate_corpus_run_v1"
)

DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT = (
    ".data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_corpus_manifest.template.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VALIDATION_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_corpus_manifest.validation.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT_DIR = (
    ".data/exports/real_broadcast_gameplay_corpus_run"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_corpus_run.current.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_corpus_report.current.json"
)

REAL_BROADCAST_GAMEPLAY_CORPUS_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

DEFAULT_EXPECTED_MEDIA_TYPE = "local_broadcast_video_file"
DEFAULT_RUN_MODE = "dry_run"
DEFAULT_SOURCE_LABEL = "real_broadcast_gameplay_corpus_entry"
DEFAULT_VIEWER_BASE_URL = "http://127.0.0.1:3000"

ALLOWED_EXPECTED_BROADCAST_CONTENT_TAGS = {
    "live_gameplay",
    "replay_package",
    "broadcast_graphic",
    "commercial",
    "crowd_cutaway",
    "player_closeup",
    "bench_or_coach_shot",
    "changeover",
    "interview",
    "warmup_or_practice",
    "unknown",
}
ALLOWED_REQUESTED_STEPS = {
    "validate_media_path",
    "inspect_gameplay_classifier_asset",
    "build_gameplay_segment_candidates",
    "build_gameplay_gated_routing_plan",
    "build_gameplay_gated_execution_plan",
    "build_gameplay_replay_timeline",
    "build_gameplay_review_dataset_export",
    "summarize_corpus_run",
}
DEFAULT_REQUESTED_STEPS = [
    "validate_media_path",
    "inspect_gameplay_classifier_asset",
    "build_gameplay_segment_candidates",
    "build_gameplay_gated_routing_plan",
    "build_gameplay_gated_execution_plan",
    "build_gameplay_replay_timeline",
    "build_gameplay_review_dataset_export",
    "summarize_corpus_run",
]
DISALLOWED_REQUESTED_STEPS = {
    "create_truth",
    "score_point",
    "identify_players",
    "adjudicate",
    "line_call",
    "generate_training_labels",
    "prove_generalization",
    "calculate_classifier_accuracy",
}
ALLOWED_RUN_MODES = {
    "dry_run",
    "validate_only",
    "fixture_only",
    "structural_real_data_run",
    "explicit_local_media_run",
}
REAL_MEDIA_RUN_MODES = {
    "structural_real_data_run",
    "explicit_local_media_run",
}
ALLOWED_ENTRY_STATUSES = {
    "dry_run_planned",
    "failed",
    "fixture_completed",
    "planned",
    "processed",
    "skipped",
    "validated",
}
ALLOWED_REPORT_STATUSES = {
    "completed",
    "completed_with_errors",
    "invalid_corpus_manifest",
    "invalid_corpus_report",
}

FORBIDDEN_CORPUS_TOKENS = {
    "in_out",
    "score",
    "winner",
    "point_winner",
    "player_identity",
    "server",
    "receiver",
    "rally_state",
    "line_call_truth",
    "point_truth",
    "event_truth",
    "gameplay_truth",
    "adjudication",
    "adjudicated",
    "accepted",
    "rejected",
    "correct",
    "incorrect",
    "truth",
    "true_gameplay",
    "confirmed_gameplay",
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "training_truth",
    "production_truth",
    "production_ready_truth",
    "model_ready_truth",
    "generalization_proven",
    "classifier_accuracy_claim",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_quality_score",
}

CORPUS_WARNINGS = {
    "corpus_run_is_not_truth": True,
    "controlled_real_data_readiness_only": True,
    "explicit_media_manifest_only": True,
    "no_silent_folder_scan": True,
    "default_mode_is_dry_run": True,
    "content_tags_are_operator_context_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_claimed": True,
    "generalization_not_claimed": True,
    "does_not_create_line_call_truth": True,
    "does_not_create_event_truth": True,
    "does_not_create_point_truth": True,
    "does_not_create_gameplay_truth": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_mutate_model_assets": True,
    "does_not_train_classifier": True,
    "does_not_convert_outputs_into_training_labels": True,
    "no_adjudication": True,
    "observation_only": True,
    "provenance_only": True,
    "review_support_only": True,
}

ENTRY_WARNINGS = {
    "corpus_entry_is_not_truth": True,
    "broadcast_context_tags_are_not_truth": True,
    "structural_evidence_chain_only": True,
    "explicit_media_path_only": True,
    "human_review_required_for_readiness": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "no_adjudication": True,
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
    "gameplay_gate_review_dataset_export_contract_version": (
        GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_VERSION
    ),
    "gameplay_gate_pathway_completion_freeze_version": (
        GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION
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


def export_real_broadcast_gameplay_corpus_run_contract(
    *,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or REAL_BROADCAST_GAMEPLAY_CORPUS_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
        "manifest_type": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
        "manifest_version": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
        "report_type": REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION,
        "contract": contract,
        "warnings": dict(CORPUS_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_real_broadcast_gameplay_corpus_manifest_template(
    *,
    local_media_paths: list[str | Path] | None = None,
    source_label: str = DEFAULT_SOURCE_LABEL,
    expected_broadcast_content_tags: list[str] | None = None,
    requested_steps: list[str] | None = None,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_OUTPUT
    ),
    generated_at: datetime | None = None,
    allow_fixture_mode: bool = False,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    paths = [str(path) for path in (local_media_paths or []) if str(path).strip()]
    steps = requested_steps or list(DEFAULT_REQUESTED_STEPS)
    tags = expected_broadcast_content_tags or ["unknown"]
    entries = [
        _manifest_entry(
            local_media_path=path,
            source_label=_source_label_for_index(source_label=source_label, index=index),
            expected_broadcast_content_tags=tags,
            requested_steps=steps,
            allow_fixture_mode=allow_fixture_mode,
        )
        for index, path in enumerate(paths)
    ]
    if not entries:
        entries = [
            _manifest_entry(
                local_media_path="",
                source_label=source_label,
                expected_broadcast_content_tags=tags,
                requested_steps=[
                    "validate_media_path",
                    "summarize_corpus_run",
                ],
                allow_fixture_mode=allow_fixture_mode,
            )
        ]
    manifest = {
        "manifest_type": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
        "manifest_version": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "default_run_mode": DEFAULT_RUN_MODE,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "entry_count": len(entries),
        "entries": entries,
        "warnings": _warnings_for_entries(entries),
        "non_claims": dict(NON_CLAIMS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "manifest_type": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
        "manifest_version": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
        "entry_count": len(entries),
        "manifest": manifest,
        "warnings": manifest["warnings"],
    }
    _write_json_if_requested(output_path, manifest, result, "manifest_output")
    return result


def validate_real_broadcast_gameplay_corpus_manifest(
    *,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VALIDATION_OUTPUT
    ),
    run_mode: str = DEFAULT_RUN_MODE,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    manifest = _load_manifest(manifest_path=manifest_path, errors=errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if run_mode not in ALLOWED_RUN_MODES:
        errors.append(_error("unsupported_run_mode", "run_mode", run_mode))
    if manifest:
        validation = _validate_manifest_shape(manifest=manifest, run_mode=run_mode)
        errors.extend(_list(validation.get("errors")))
        structural_warnings.extend(_list(validation.get("structural_warnings")))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "real_broadcast_gameplay_corpus_manifest_validation",
        "validation_version": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "run_mode": run_mode,
        "contract_path": str(Path(contract_path)),
        "manifest_path": str(Path(manifest_path)),
        "contract_type": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
        "manifest_type": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
        "manifest_version": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
        "entry_count": len(_manifest_entries(manifest)),
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "warnings": _warnings_for_entries(_manifest_entries(manifest)),
        "non_claims": dict(NON_CLAIMS),
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def run_real_broadcast_gameplay_corpus(
    *,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    run_mode: str = DEFAULT_RUN_MODE,
    output_dir: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT_DIR,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    gameplay_segment_contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    routing_contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    execution_contract_path: str | Path = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT
    ),
    replay_review_contract_path: str | Path = (
        DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT
    ),
    review_dataset_contract_path: str | Path = (
        DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT
    ),
    viewer_base_url: str = DEFAULT_VIEWER_BASE_URL,
    frame_sample_rate: int = 30,
    max_frames: int | None = 240,
    generated_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    if run_mode not in ALLOWED_RUN_MODES:
        report = _corpus_run_report(
            generated_at=generated_at,
            run_mode=run_mode,
            manifest_path=manifest_path,
            entries=[],
            validation={
                "ok": False,
                "status": "invalid",
                "errors": [_error("unsupported_run_mode", "run_mode", run_mode)],
                "error_count": 1,
            },
            status="invalid_corpus_manifest",
            model_asset_path=model_asset_path,
        )
        return _write_run_result(report=report, output_path=output_path, ok=False)

    validation = validate_real_broadcast_gameplay_corpus_manifest(
        contract_path=contract_path,
        manifest_path=manifest_path,
        output_path=None,
        run_mode=run_mode,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        report = _corpus_run_report(
            generated_at=generated_at,
            run_mode=run_mode,
            manifest_path=manifest_path,
            entries=[],
            validation=validation,
            status="invalid_corpus_manifest",
            model_asset_path=model_asset_path,
        )
        return _write_run_result(report=report, output_path=output_path, ok=False)

    manifest = _load_manifest(manifest_path=manifest_path, errors=[])
    output_root = Path(output_dir).expanduser()
    output_root.mkdir(parents=True, exist_ok=True)
    entries = [
        _run_corpus_entry(
            entry=entry,
            run_mode=run_mode,
            output_root=output_root,
            model_asset_path=model_asset_path,
            gameplay_segment_contract_path=gameplay_segment_contract_path,
            routing_contract_path=routing_contract_path,
            execution_contract_path=execution_contract_path,
            replay_review_contract_path=replay_review_contract_path,
            review_dataset_contract_path=review_dataset_contract_path,
            viewer_base_url=viewer_base_url,
            frame_sample_rate=frame_sample_rate,
            max_frames=max_frames,
            generated_at=generated_at,
            probe_runner=probe_runner,
        )
        for entry in _manifest_entries(manifest)
    ]
    status = (
        "completed_with_errors"
        if any(entry.get("status") == "failed" for entry in entries)
        else "completed"
    )
    report = _corpus_run_report(
        generated_at=generated_at,
        run_mode=run_mode,
        manifest_path=manifest_path,
        entries=entries,
        validation=validation,
        status=status,
        model_asset_path=model_asset_path,
    )
    return _write_run_result(report=report, output_path=output_path, ok=status == "completed")


def build_real_broadcast_gameplay_corpus_report(
    *,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT,
    corpus_run_path: str | Path,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    run_report = _load_report(corpus_run_path=corpus_run_path, errors=errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if run_report:
        errors.extend(_validate_report_shape(run_report))

    if errors:
        status = "invalid_corpus_report"
        report = _corpus_run_report(
            generated_at=generated_at,
            run_mode=str(run_report.get("run_mode") or DEFAULT_RUN_MODE),
            manifest_path=str(run_report.get("source_manifest_path") or ""),
            entries=[],
            validation={"ok": False, "status": "invalid", "errors": errors},
            status=status,
            model_asset_path=DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
        )
    else:
        status = str(run_report.get("status") or "completed")
        report = dict(run_report)
        report["report_type"] = REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE
        report["report_version"] = REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION
        report["report_built_at"] = generated_at.isoformat()
        report["report_source_path"] = str(Path(corpus_run_path))
        report["human_review_readiness"] = _human_review_readiness(report)
        report["validation_summary"] = {
            "status": "valid",
            "error_count": 0,
            "report_shape_valid": True,
            "validation_is_structural_only": True,
        }
        report["warnings"] = {
            **dict(CORPUS_WARNINGS),
            **_dict(report.get("warnings")),
            "report_is_human_review_readiness_only": True,
        }
        report["non_claims"] = dict(NON_CLAIMS)

    result = {
        "ok": status != "invalid_corpus_report",
        "status": status,
        "report_type": REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION,
        "corpus_run_id": report.get("corpus_run_id"),
        "entry_count": report.get("entry_count", 0),
        "summary": report.get("summary", {}),
        "report": report,
        "warnings": _dict(report.get("warnings")) or dict(CORPUS_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "corpus_run_scope": {
            "purpose": "controlled_real_broadcast_gameplay_gate_corpus_run",
            "default_run_mode": DEFAULT_RUN_MODE,
            "allowed_run_modes": sorted(ALLOWED_RUN_MODES),
            "explicit_input_manifest_required": True,
            "explicit_real_local_media_required_for_real_run": True,
            "automatic_media_discovery_allowed": False,
            "silent_folder_scan_allowed": False,
            "uses_existing_tom_v1_classifier_asset": True,
            "trains_or_modifies_classifier": False,
            "commits_model_weights": False,
            "uses_gameplay_segment_gate": True,
            "uses_gameplay_gated_routing_plan": True,
            "uses_gameplay_gated_execution_plan": True,
            "uses_gameplay_replay_timeline": True,
            "uses_gameplay_review_dataset_export": True,
            "mutates_regression_baselines": False,
            "creates_tennis_conclusions": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "input_manifest_schema": {
            "manifest_type": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE,
            "manifest_version": REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION,
            "entries_required": True,
            "explicit_local_media_paths_required": True,
            "default_run_mode": DEFAULT_RUN_MODE,
            "allowed_run_modes": sorted(ALLOWED_RUN_MODES),
            "allowed_expected_broadcast_content_tags": sorted(
                ALLOWED_EXPECTED_BROADCAST_CONTENT_TAGS
            ),
            "content_tags_are_expected_context_only": True,
            "allowed_requested_steps": sorted(ALLOWED_REQUESTED_STEPS),
            "disallowed_requested_steps": sorted(DISALLOWED_REQUESTED_STEPS),
        },
        "corpus_entry_schema": {
            "required_fields": [
                "corpus_entry_id",
                "local_media_path",
                "source_label",
                "source_notes",
                "expected_media_type",
                "expected_broadcast_content_tags",
                "allow_fixture_mode",
                "requested_steps",
                "warnings",
            ],
            "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
            "allowed_statuses": sorted(ALLOWED_ENTRY_STATUSES),
        },
        "corpus_run_report_schema": {
            "report_type": REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE,
            "report_version": REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION,
            "allowed_report_statuses": sorted(ALLOWED_REPORT_STATUSES),
            "required_fields": [
                "corpus_run_id",
                "corpus_run_version",
                "generated_at",
                "run_mode",
                "source_manifest_path",
                "entry_count",
                "validated_entry_count",
                "processed_entry_count",
                "skipped_entry_count",
                "failed_entry_count",
                "model_asset_ref",
                "model_asset_sha256",
                "entries",
                "summary",
                "warnings",
                "non_claims",
            ],
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_manifest_shape": True,
            "validate_report_shape": True,
            "validate_allowed_run_modes": True,
            "validate_allowed_expected_broadcast_content_tags": True,
            "validate_allowed_requested_steps": True,
            "reject_disallowed_requested_steps": True,
            "reject_forbidden_exact_tokens": True,
            "require_explicit_manifest_for_real_run": True,
            "require_explicit_media_paths_for_real_run": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "source_manifest_path_required": True,
            "corpus_entry_id_required": True,
            "local_media_path_required": True,
            "path_exists_recorded": True,
            "operator_source_label_preserved": True,
            "operator_source_notes_preserved": True,
            "expected_broadcast_content_tags_preserved": True,
            "model_asset_ref_recorded": True,
            "model_asset_sha256_recorded_when_available": True,
            "gameplay_segment_output_path_recorded_when_built": True,
            "routing_plan_output_path_recorded_when_built": True,
            "execution_plan_output_path_recorded_when_built": True,
            "replay_timeline_output_path_recorded_when_built": True,
            "review_dataset_output_path_recorded_when_built": True,
            "warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(CORPUS_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _manifest_entry(
    *,
    local_media_path: str,
    source_label: str,
    expected_broadcast_content_tags: list[str],
    requested_steps: list[str],
    allow_fixture_mode: bool,
) -> dict[str, Any]:
    return {
        "corpus_entry_id": _stable_id(
            "real_broadcast_gameplay_corpus_entry_v1",
            local_media_path,
            source_label,
        ),
        "local_media_path": local_media_path,
        "source_label": source_label,
        "source_notes": "Explicit local broadcast-style media entry for structural review.",
        "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
        "expected_broadcast_content_tags": list(expected_broadcast_content_tags),
        "allow_fixture_mode": allow_fixture_mode,
        "requested_steps": list(requested_steps),
        "warnings": dict(ENTRY_WARNINGS),
    }


def _run_corpus_entry(
    *,
    entry: dict[str, Any],
    run_mode: str,
    output_root: Path,
    model_asset_path: str | Path,
    gameplay_segment_contract_path: str | Path,
    routing_contract_path: str | Path,
    execution_contract_path: str | Path,
    replay_review_contract_path: str | Path,
    review_dataset_contract_path: str | Path,
    viewer_base_url: str,
    frame_sample_rate: int,
    max_frames: int | None,
    generated_at: datetime,
    probe_runner: Any | None,
) -> dict[str, Any]:
    entry_id = str(entry.get("corpus_entry_id") or _stable_id("corpus_entry", entry))
    paths = _entry_artifact_paths(output_root=output_root, entry_id=entry_id)
    steps = set(_string_list(entry.get("requested_steps")))
    local_media_path = str(entry.get("local_media_path") or "")
    path_exists = Path(local_media_path).expanduser().is_file()
    media_id = _stable_id("real_broadcast_gameplay_corpus_media_v1", entry_id, local_media_path)
    report_entry = _base_report_entry(
        entry=entry,
        media_id=media_id,
        path_exists=path_exists,
        run_mode=run_mode,
    )

    if run_mode == "validate_only":
        report_entry["status"] = "validated"
        return report_entry
    if run_mode == "dry_run":
        report_entry["status"] = "dry_run_planned"
        return report_entry
    if run_mode == "fixture_only" and entry.get("allow_fixture_mode") is not True:
        report_entry["status"] = "failed"
        report_entry["errors"].append(
            _error(
                "fixture_mode_not_allowed_for_entry",
                "allow_fixture_mode",
                entry.get("allow_fixture_mode"),
            )
        )
        return report_entry
    if not path_exists:
        report_entry["status"] = "failed"
        report_entry["errors"].append(
            _error("local_media_path_not_found", "local_media_path", local_media_path)
        )
        return report_entry

    if "inspect_gameplay_classifier_asset" in steps:
        inspection = inspect_gameplay_classifier_asset(
            model_asset_path=model_asset_path,
            output_path=paths["model_asset_inspection"],
        )
        report_entry["artifact_outputs"]["model_asset_inspection"] = str(
            paths["model_asset_inspection"]
        )
        report_entry["model_asset"] = {
            "path": str(model_asset_path),
            "exists": inspection.get("model_asset_exists"),
            "sha256": inspection.get("model_asset_sha256"),
            "status": inspection.get("status"),
        }

    if "build_gameplay_segment_candidates" in steps:
        result = build_gameplay_segment_candidates(
            local_media_path=local_media_path,
            media_id=media_id,
            output_path=paths["gameplay_segments"],
            model_asset_path=model_asset_path,
            inference_mode="provenance_fixture",
            viewer_base_url=viewer_base_url,
            frame_sample_rate=frame_sample_rate,
            max_frames=max_frames,
            generated_at=generated_at,
            probe_runner=probe_runner,
        )
        report_entry["artifact_outputs"]["gameplay_segment_candidates"] = str(
            paths["gameplay_segments"]
        )
        if result.get("ok") is False:
            _mark_step_failed(report_entry, "build_gameplay_segment_candidates", result)
            return report_entry
        _add_candidate_counts(report_entry, paths["gameplay_segments"])

    if "build_gameplay_gated_routing_plan" in steps:
        if "gameplay_segment_candidates" not in report_entry["artifact_outputs"]:
            _mark_step_skipped(report_entry, "build_gameplay_gated_routing_plan")
        else:
            result = build_gameplay_gated_routing_plan(
                gameplay_segments_path=paths["gameplay_segments"],
                gameplay_gate_contract_path=gameplay_segment_contract_path,
                output_path=paths["routing_plan"],
                routing_mode="dry_run",
                generated_at=generated_at,
            )
            report_entry["artifact_outputs"]["gameplay_gated_routing_plan"] = str(
                paths["routing_plan"]
            )
            if result.get("ok") is False:
                _mark_step_failed(report_entry, "build_gameplay_gated_routing_plan", result)
                return report_entry
            _add_routing_counts(report_entry, paths["routing_plan"])

    if "build_gameplay_gated_execution_plan" in steps:
        if "gameplay_gated_routing_plan" not in report_entry["artifact_outputs"]:
            _mark_step_skipped(report_entry, "build_gameplay_gated_execution_plan")
        else:
            result = build_gameplay_gated_perception_execution_plan(
                routing_plan_path=paths["routing_plan"],
                routing_contract_path=routing_contract_path,
                output_path=paths["execution_plan"],
                execution_mode="dry_run",
                generated_at=generated_at,
            )
            report_entry["artifact_outputs"]["gameplay_gated_execution_plan"] = str(
                paths["execution_plan"]
            )
            if result.get("ok") is False:
                _mark_step_failed(report_entry, "build_gameplay_gated_execution_plan", result)
                return report_entry
            _add_execution_counts(report_entry, paths["execution_plan"])

    if "build_gameplay_replay_timeline" in steps:
        if "gameplay_segment_candidates" not in report_entry["artifact_outputs"]:
            _mark_step_skipped(report_entry, "build_gameplay_replay_timeline")
        else:
            result = build_gameplay_segment_replay_timeline(
                gameplay_segments_path=paths["gameplay_segments"],
                routing_plan_path=(
                    paths["routing_plan"]
                    if "gameplay_gated_routing_plan" in report_entry["artifact_outputs"]
                    else None
                ),
                execution_plan_path=(
                    paths["execution_plan"]
                    if "gameplay_gated_execution_plan" in report_entry["artifact_outputs"]
                    else None
                ),
                viewer_base_url=viewer_base_url,
                output_path=paths["replay_timeline"],
                generated_at=generated_at,
            )
            report_entry["artifact_outputs"]["gameplay_replay_timeline"] = str(
                paths["replay_timeline"]
            )
            if result.get("ok") is False:
                _mark_step_failed(report_entry, "build_gameplay_replay_timeline", result)
                return report_entry
            report_entry["replay_timeline_entry_count"] = int(
                result.get("timeline_entry_count") or 0
            )

    if "build_gameplay_review_dataset_export" in steps:
        if "gameplay_segment_candidates" not in report_entry["artifact_outputs"]:
            _mark_step_skipped(report_entry, "build_gameplay_review_dataset_export")
        else:
            result = build_gameplay_gate_review_dataset(
                contract_path=review_dataset_contract_path,
                gameplay_segments_path=paths["gameplay_segments"],
                routing_plan_path=(
                    paths["routing_plan"]
                    if "gameplay_gated_routing_plan" in report_entry["artifact_outputs"]
                    else None
                ),
                execution_plan_path=(
                    paths["execution_plan"]
                    if "gameplay_gated_execution_plan" in report_entry["artifact_outputs"]
                    else None
                ),
                replay_timeline_path=(
                    paths["replay_timeline"]
                    if "gameplay_replay_timeline" in report_entry["artifact_outputs"]
                    else None
                ),
                work_dir=paths["review_dataset_work_dir"],
                fixture_media_path=local_media_path,
                model_asset_path=model_asset_path,
                viewer_base_url=viewer_base_url,
                output_path=paths["review_dataset"],
                generated_at=generated_at,
                probe_runner=probe_runner,
            )
            report_entry["artifact_outputs"]["gameplay_review_dataset_export"] = str(
                paths["review_dataset"]
            )
            if result.get("ok") is False:
                _mark_step_failed(report_entry, "build_gameplay_review_dataset_export", result)
                return report_entry
            report_entry["review_dataset_entry_count"] = int(result.get("entry_count") or 0)

    report_entry["status"] = "fixture_completed" if run_mode == "fixture_only" else "processed"
    report_entry["contract_paths"] = {
        "gameplay_segment_gate": str(gameplay_segment_contract_path),
        "gameplay_gated_routing": str(routing_contract_path),
        "gameplay_gated_execution": str(execution_contract_path),
        "gameplay_segment_replay_review": str(replay_review_contract_path),
        "gameplay_gate_review_dataset_export": str(review_dataset_contract_path),
    }
    return report_entry


def _base_report_entry(
    *,
    entry: dict[str, Any],
    media_id: str,
    path_exists: bool,
    run_mode: str,
) -> dict[str, Any]:
    return {
        "corpus_entry_id": entry.get("corpus_entry_id"),
        "local_media_path": entry.get("local_media_path"),
        "source_label": entry.get("source_label"),
        "source_notes": entry.get("source_notes"),
        "expected_media_type": entry.get("expected_media_type"),
        "expected_broadcast_content_tags": _string_list(
            entry.get("expected_broadcast_content_tags")
        ),
        "path_exists": path_exists,
        "media_id": media_id,
        "gameplay_segment_candidate_count": 0,
        "downstream_allowed_window_count": 0,
        "downstream_blocked_window_count": 0,
        "downstream_review_required_window_count": 0,
        "perception_execution_window_count": 0,
        "perception_skipped_window_count": 0,
        "replay_timeline_entry_count": 0,
        "review_dataset_entry_count": 0,
        "status": "skipped",
        "run_mode": run_mode,
        "requested_steps": _string_list(entry.get("requested_steps")),
        "artifact_outputs": {},
        "contract_paths": {},
        "model_asset": {},
        "errors": [],
        "warnings": dict(ENTRY_WARNINGS),
    }


def _corpus_run_report(
    *,
    generated_at: datetime,
    run_mode: str,
    manifest_path: str | Path,
    entries: list[dict[str, Any]],
    validation: dict[str, Any],
    status: str,
    model_asset_path: str | Path,
) -> dict[str, Any]:
    summary = _report_summary(entries=entries, validation=validation)
    model_asset = _model_asset_ref(model_asset_path)
    corpus_run_id = _stable_id(
        "real_broadcast_gameplay_corpus_run_v1",
        str(Path(manifest_path)),
        run_mode,
        len(entries),
        json.dumps(summary, sort_keys=True),
    )
    return {
        "report_type": REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE,
        "report_version": REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION,
        "corpus_run_id": corpus_run_id,
        "corpus_run_version": REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION,
        "generated_at": generated_at.isoformat(),
        "run_mode": run_mode,
        "source_manifest_path": str(Path(manifest_path)),
        "entry_count": len(entries),
        "validated_entry_count": summary["validated_entry_count"],
        "processed_entry_count": summary["processed_entry_count"],
        "skipped_entry_count": summary["skipped_entry_count"],
        "failed_entry_count": summary["failed_entry_count"],
        "model_asset_ref": model_asset["model_asset_ref"],
        "model_asset_sha256": model_asset["model_asset_sha256"],
        "model_asset_exists": model_asset["model_asset_exists"],
        "entries": entries,
        "summary": summary,
        "manifest_validation": validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
        "status": status,
        "warnings": _warnings_for_entries(entries),
        "non_claims": dict(NON_CLAIMS),
    }


def _report_summary(
    *,
    entries: list[dict[str, Any]],
    validation: dict[str, Any],
) -> dict[str, Any]:
    status_counts = Counter(str(entry.get("status")) for entry in entries)
    tag_counts = Counter(
        tag
        for entry in entries
        for tag in _string_list(entry.get("expected_broadcast_content_tags"))
    )
    return {
        "entry_count": len(entries),
        "validated_entry_count": sum(1 for entry in entries if entry.get("path_exists") is True),
        "processed_entry_count": sum(
            1 for entry in entries if entry.get("status") in {"processed", "fixture_completed"}
        ),
        "skipped_entry_count": status_counts.get("skipped", 0)
        + status_counts.get("dry_run_planned", 0)
        + status_counts.get("planned", 0),
        "failed_entry_count": status_counts.get("failed", 0),
        "gameplay_candidate_entry_count": sum(
            1 for entry in entries if int(entry.get("gameplay_segment_candidate_count") or 0) > 0
        ),
        "review_dataset_entry_count": sum(
            int(entry.get("review_dataset_entry_count") or 0) for entry in entries
        ),
        "review_ready_entry_count": sum(
            1 for entry in entries if int(entry.get("replay_timeline_entry_count") or 0) > 0
        ),
        "status_counts": dict(sorted(status_counts.items())),
        "expected_broadcast_content_tag_counts": dict(sorted(tag_counts.items())),
        "manifest_validation_status": validation.get("status"),
        "manifest_validation_error_count": validation.get("error_count", 0),
        "corpus_run_is_structural_only": True,
        "does_not_create_tennis_truth": True,
        "does_not_mutate_model_assets": True,
        "does_not_mutate_regression_baselines": True,
    }


def _human_review_readiness(report: dict[str, Any]) -> dict[str, Any]:
    entries = [entry for entry in _list(report.get("entries")) if isinstance(entry, dict)]
    return {
        "ready_for_human_review": any(
            int(entry.get("replay_timeline_entry_count") or 0) > 0 for entry in entries
        ),
        "entry_count": len(entries),
        "replay_timeline_entry_count": sum(
            int(entry.get("replay_timeline_entry_count") or 0) for entry in entries
        ),
        "review_dataset_entry_count": sum(
            int(entry.get("review_dataset_entry_count") or 0) for entry in entries
        ),
        "failed_entry_count": sum(1 for entry in entries if entry.get("status") == "failed"),
        "requires_human_review": True,
        "readiness_is_not_correctness": True,
        "review_dataset_is_metadata_only": True,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "corpus_run_scope",
        "source_contract_refs",
        "input_manifest_schema",
        "corpus_entry_schema",
        "corpus_run_report_schema",
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


def _validate_manifest_shape(
    *,
    manifest: dict[str, Any],
    run_mode: str,
) -> dict[str, Any]:
    errors = _forbidden_token_errors(manifest, path="corpus_manifest")
    structural_warnings: list[dict[str, Any]] = []
    if manifest.get("manifest_type") != REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_TYPE:
        errors.append(
            _error("invalid_manifest_type", "manifest_type", manifest.get("manifest_type"))
        )
    if manifest.get("manifest_version") != REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VERSION:
        errors.append(
            _error(
                "invalid_manifest_version",
                "manifest_version",
                manifest.get("manifest_version"),
            )
        )
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("entries_must_be_list", "entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}
    if not entries:
        errors.append(_error("entries_required", "entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}
    seen_entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("corpus_entry_must_be_object", path, entry))
            continue
        entry_errors, entry_warnings = _validate_manifest_entry(
            entry=entry,
            path=path,
            run_mode=run_mode,
        )
        errors.extend(entry_errors)
        structural_warnings.extend(entry_warnings)
        entry_id = _string_or_none(entry.get("corpus_entry_id"))
        if entry_id in seen_entry_ids:
            errors.append(_error("duplicate_corpus_entry_id", f"{path}.corpus_entry_id", entry_id))
        if entry_id is not None:
            seen_entry_ids.add(entry_id)
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_manifest_entry(
    *,
    entry: dict[str, Any],
    path: str,
    run_mode: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    errors = _forbidden_token_errors(entry, path=path)
    structural_warnings: list[dict[str, Any]] = []
    for field in (
        "corpus_entry_id",
        "local_media_path",
        "source_label",
        "source_notes",
        "expected_media_type",
        "expected_broadcast_content_tags",
        "allow_fixture_mode",
        "requested_steps",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_corpus_entry_field", f"{path}.{field}", None))
    local_media_path = _string_or_none(entry.get("local_media_path"))
    if local_media_path is None:
        if run_mode in REAL_MEDIA_RUN_MODES:
            errors.append(_error("local_media_path_missing", f"{path}.local_media_path", None))
        else:
            structural_warnings.append(
                _warning("local_media_path_empty_for_non_real_run", path, local_media_path)
            )
    else:
        media_path = Path(local_media_path).expanduser()
        if not media_path.is_file():
            if run_mode in {"dry_run", "validate_only"}:
                structural_warnings.append(
                    _warning(
                        "local_media_path_not_found_for_non_processing_run",
                        path,
                        local_media_path,
                    )
                )
            else:
                errors.append(
                    _error(
                        "local_media_path_not_found",
                        f"{path}.local_media_path",
                        local_media_path,
                    )
                )
    if _string_or_none(entry.get("corpus_entry_id")) is None:
        errors.append(_error("invalid_corpus_entry_id", f"{path}.corpus_entry_id", None))
    if _string_or_none(entry.get("source_label")) is None:
        errors.append(_error("source_label_missing", f"{path}.source_label", None))
    if not isinstance(entry.get("source_notes"), str):
        errors.append(_error("source_notes_must_be_string", f"{path}.source_notes", None))
    if entry.get("expected_media_type") != DEFAULT_EXPECTED_MEDIA_TYPE:
        errors.append(
            _error(
                "unsupported_expected_media_type",
                f"{path}.expected_media_type",
                entry.get("expected_media_type"),
            )
        )
    tags = entry.get("expected_broadcast_content_tags")
    if not isinstance(tags, list) or not tags:
        errors.append(
            _error(
                "expected_broadcast_content_tags_must_be_list",
                f"{path}.expected_broadcast_content_tags",
                tags,
            )
        )
    else:
        for tag in tags:
            if tag not in ALLOWED_EXPECTED_BROADCAST_CONTENT_TAGS:
                errors.append(
                    _error(
                        "unsupported_expected_broadcast_content_tag",
                        f"{path}.expected_broadcast_content_tags",
                        tag,
                    )
                )
    if not isinstance(entry.get("allow_fixture_mode"), bool):
        errors.append(
            _error(
                "allow_fixture_mode_must_be_boolean",
                f"{path}.allow_fixture_mode",
                entry.get("allow_fixture_mode"),
            )
        )
    if run_mode == "fixture_only" and entry.get("allow_fixture_mode") is not True:
        errors.append(
            _error(
                "fixture_run_requires_entry_allow_fixture_mode",
                f"{path}.allow_fixture_mode",
                entry.get("allow_fixture_mode"),
            )
        )
    steps = entry.get("requested_steps")
    if not isinstance(steps, list) or not steps:
        errors.append(_error("requested_steps_must_be_list", f"{path}.requested_steps", steps))
    else:
        for step in steps:
            if step in DISALLOWED_REQUESTED_STEPS:
                errors.append(
                    _error("disallowed_requested_step", f"{path}.requested_steps", step)
                )
            elif step not in ALLOWED_REQUESTED_STEPS:
                errors.append(
                    _error("unsupported_requested_step", f"{path}.requested_steps", step)
                )
    if not isinstance(entry.get("warnings"), dict):
        errors.append(_error("warnings_must_be_object", f"{path}.warnings", entry.get("warnings")))
    return errors, structural_warnings


def _validate_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, path="corpus_report")
    if report.get("report_type") not in {
        REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_TYPE,
        REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_TYPE,
    }:
        errors.append(_error("invalid_report_type", "report_type", report.get("report_type")))
    if report.get("report_version") not in {
        REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_VERSION,
        REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_VERSION,
    }:
        errors.append(
            _error("invalid_report_version", "report_version", report.get("report_version"))
        )
    if report.get("run_mode") not in ALLOWED_RUN_MODES:
        errors.append(_error("invalid_run_mode", "run_mode", report.get("run_mode")))
    if report.get("status") not in ALLOWED_REPORT_STATUSES:
        errors.append(_error("invalid_report_status", "status", report.get("status")))
    for field in (
        "corpus_run_id",
        "corpus_run_version",
        "generated_at",
        "run_mode",
        "source_manifest_path",
        "entry_count",
        "validated_entry_count",
        "processed_entry_count",
        "skipped_entry_count",
        "failed_entry_count",
        "model_asset_ref",
        "model_asset_sha256",
        "entries",
        "summary",
        "warnings",
        "non_claims",
    ):
        if field not in report:
            errors.append(_error("missing_report_field", field, None))
    for index, entry in enumerate(_list(report.get("entries"))):
        if not isinstance(entry, dict):
            errors.append(_error("invalid_report_entry", f"entries[{index}]", entry))
            continue
        errors.extend(_validate_report_entry(entry=entry, index=index))
    return errors


def _validate_report_entry(
    *,
    entry: dict[str, Any],
    index: int,
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(entry, path=f"entries[{index}]")
    if entry.get("status") not in ALLOWED_ENTRY_STATUSES:
        errors.append(
            _error(
                "invalid_entry_status",
                f"entries[{index}].status",
                entry.get("status"),
            )
        )
    for field in (
        "corpus_entry_id",
        "local_media_path",
        "source_label",
        "expected_broadcast_content_tags",
        "path_exists",
        "gameplay_segment_candidate_count",
        "downstream_allowed_window_count",
        "downstream_blocked_window_count",
        "downstream_review_required_window_count",
        "perception_execution_window_count",
        "perception_skipped_window_count",
        "replay_timeline_entry_count",
        "review_dataset_entry_count",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_report_entry_field", f"entries[{index}].{field}", None))
    return errors


def _entry_artifact_paths(*, output_root: Path, entry_id: str) -> dict[str, Path]:
    safe_entry_id = "".join(
        char if char.isalnum() or char in {"-", "_"} else "_" for char in entry_id
    )
    entry_dir = output_root / safe_entry_id
    entry_dir.mkdir(parents=True, exist_ok=True)
    return {
        "model_asset_inspection": entry_dir / "gameplay_classifier_asset_inspection.json",
        "gameplay_segments": entry_dir / "gameplay_segment_candidates.json",
        "routing_plan": entry_dir / "gameplay_gated_routing_plan.json",
        "execution_plan": entry_dir / "gameplay_gated_execution_plan.json",
        "replay_timeline": entry_dir / "gameplay_segment_replay_timeline.json",
        "review_dataset": entry_dir / "gameplay_gate_review_dataset.json",
        "review_dataset_work_dir": entry_dir / "review_dataset_artifacts",
    }


def _add_candidate_counts(report_entry: dict[str, Any], path: Path) -> None:
    data = _load_json_file(path)
    report_entry["gameplay_segment_candidate_count"] = len(_list(data.get("segment_candidates")))


def _add_routing_counts(report_entry: dict[str, Any], path: Path) -> None:
    data = _load_json_file(path)
    report_entry["downstream_allowed_window_count"] = int(
        len(_list(data.get("allowed_windows")))
    )
    report_entry["downstream_blocked_window_count"] = int(
        len(_list(data.get("blocked_windows")))
    )
    report_entry["downstream_review_required_window_count"] = int(
        len(_list(data.get("uncertain_windows")))
    )


def _add_execution_counts(report_entry: dict[str, Any], path: Path) -> None:
    data = _load_json_file(path)
    summary = _dict(data.get("summary"))
    report_entry["perception_execution_window_count"] = int(
        summary.get("allowed_execution_window_count") or 0
    )
    report_entry["perception_skipped_window_count"] = int(
        summary.get("skipped_window_count") or 0
    )


def _mark_step_failed(
    report_entry: dict[str, Any],
    step: str,
    result: dict[str, Any],
) -> None:
    report_entry["status"] = "failed"
    report_entry["errors"].append(_error("step_failed", step, result))


def _mark_step_skipped(report_entry: dict[str, Any], step: str) -> None:
    report_entry["errors"].append(
        _error("step_skipped_missing_source_artifact", step, "required source artifact absent")
    )


def _write_run_result(
    *,
    report: dict[str, Any],
    output_path: str | Path | None,
    ok: bool,
) -> dict[str, Any]:
    result = {
        "ok": ok,
        "status": report.get("status"),
        "report_type": report.get("report_type"),
        "report_version": report.get("report_version"),
        "corpus_run_id": report.get("corpus_run_id"),
        "entry_count": report.get("entry_count", 0),
        "processed_entry_count": report.get("processed_entry_count", 0),
        "failed_entry_count": report.get("failed_entry_count", 0),
        "summary": report.get("summary", {}),
        "report": report,
        "warnings": _dict(report.get("warnings")) or dict(CORPUS_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "corpus_run_output")
    return result


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(contract_path, label="real_broadcast_gameplay_corpus_contract")
    if loaded.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", loaded))
        return {}
    contract = _dict(loaded.get("data"))
    return contract


def _load_manifest(
    *,
    manifest_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(manifest_path, label="real_broadcast_gameplay_corpus_manifest")
    if loaded.get("ok") is False:
        errors.append(_error("manifest_load_failed", "manifest_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _load_report(
    *,
    corpus_run_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(corpus_run_path, label="real_broadcast_gameplay_corpus_run")
    if loaded.get("ok") is False:
        errors.append(_error("report_load_failed", "corpus_run_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _manifest_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in _list(manifest.get("entries")) if isinstance(entry, dict)]


def _warnings_for_entries(entries: list[dict[str, Any]]) -> dict[str, bool]:
    warnings = dict(CORPUS_WARNINGS)
    warnings["fixture_mode_used"] = any(
        entry.get("allow_fixture_mode") is True or entry.get("run_mode") == "fixture_only"
        for entry in entries
    )
    warnings["real_media_processing_requires_explicit_mode"] = True
    return warnings


def _model_asset_ref(model_asset_path: str | Path) -> dict[str, Any]:
    path = Path(model_asset_path).expanduser()
    if not path.is_file():
        return {
            "model_asset_ref": str(model_asset_path),
            "model_asset_exists": False,
            "model_asset_sha256": None,
        }
    return {
        "model_asset_ref": str(model_asset_path),
        "model_asset_exists": True,
        "model_asset_sha256": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_label_for_index(*, source_label: str, index: int) -> str:
    if index == 0:
        return source_label
    return f"{source_label}_{index + 1}"


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_CORPUS_TOKENS:
                errors.append(_error("forbidden_token_key", f"{path}.{key_text}", key_text))
            errors.extend(_forbidden_token_errors(nested, path=f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_forbidden_token_errors(item, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_CORPUS_TOKENS:
        errors.append(_error("forbidden_token_value", path, value))
    return errors


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    json_path = Path(path).expanduser()
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "status": "missing", "label": label, "path": str(json_path)}
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(json_path),
            "error": str(exc),
        }
    return {"ok": True, "status": "loaded", "label": label, "path": str(json_path), "data": data}


def _load_json_file(path: Path) -> dict[str, Any]:
    try:
        return _dict(json.loads(path.read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


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


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        json.dumps(parts, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "field": field, "value": value}


def _warning(warning_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"warning_type": warning_type, "field": field, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": REAL_BROADCAST_GAMEPLAY_CORPUS_BLUEPRINT,
        "blueprint_name": REAL_BROADCAST_GAMEPLAY_CORPUS_BLUEPRINT_NAME,
    }
