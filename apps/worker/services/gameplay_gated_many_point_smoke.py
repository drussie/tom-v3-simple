from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
    MANY_POINT_INGESTION_MANIFEST_VERSION,
    run_many_point_ingestion_gate,
)

GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE = (
    "gameplay_gated_many_point_smoke_contract"
)
GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION = "v1"
GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE = (
    "gameplay_gated_many_point_smoke_manifest"
)
GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION = "v1"
GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE = (
    "gameplay_gated_many_point_smoke_report"
)
GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION = "v1"
GAMEPLAY_GATED_MANY_POINT_SMOKE_BLUEPRINT = "blueprint_42"
GAMEPLAY_GATED_MANY_POINT_SMOKE_BLUEPRINT_NAME = (
    "gameplay_gated_many_point_ingestion_smoke_v1"
)

DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_gated_many_point_smoke_contract_v1.json"
)
DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_OUTPUT = (
    ".data/exports/gameplay_gated_many_point_smoke_manifest.template.json"
)
DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_gated_many_point_smoke_manifest.validation.json"
)
DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT_DIR = (
    ".data/exports/gameplay_gated_many_point_smoke"
)
DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT = (
    ".data/exports/gameplay_gated_many_point_smoke.current.json"
)
DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_OUTPUT = (
    ".data/exports/gameplay_gated_many_point_smoke_report.current.json"
)

GAMEPLAY_GATED_MANY_POINT_SMOKE_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

DEFAULT_EXPECTED_MEDIA_TYPE = "local_video_file"
DEFAULT_SMOKE_MODE = "fixture_only"
DEFAULT_SOURCE_LABEL = "gameplay_gated_smoke_point"

ALLOWED_SMOKE_MODES = {
    "dry_run",
    "validate_only",
    "fixture_only",
    "structural_smoke",
}
ALLOWED_SMOKE_STEPS = {
    "validate_media_path",
    "inspect_gameplay_classifier_asset",
    "build_gameplay_segment_candidates",
    "build_gameplay_gated_routing_plan",
    "build_gameplay_gated_execution_plan",
    "build_gameplay_replay_timeline",
    "summarize_smoke_readiness",
}
DEFAULT_REQUESTED_SMOKE_STEPS = [
    "validate_media_path",
    "inspect_gameplay_classifier_asset",
    "build_gameplay_segment_candidates",
    "build_gameplay_gated_routing_plan",
    "build_gameplay_gated_execution_plan",
    "build_gameplay_replay_timeline",
    "summarize_smoke_readiness",
]
DISALLOWED_SMOKE_STEPS = {
    "create_truth",
    "score_point",
    "identify_players",
    "adjudicate",
    "line_call",
    "generate_training_labels",
    "prove_generalization",
}
ALLOWED_ENTRY_STATUSES = {
    "dry_run_planned",
    "failed",
    "fixture_smoke_completed",
    "skipped",
    "structural_smoke_completed",
    "validated",
}
ALLOWED_REPORT_STATUSES = {
    "completed",
    "completed_with_errors",
    "invalid_smoke_manifest",
    "invalid_smoke_report",
}

FORBIDDEN_SMOKE_TOKENS = {
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
    "generalization_proven",
}

SMOKE_WARNINGS = {
    "smoke_only": True,
    "structural_smoke_only": True,
    "explicit_media_manifest_only": True,
    "fixture_mode_available": True,
    "fixture_reuse_only": False,
    "not_distinct_real_points": False,
    "does_not_claim_generalization": True,
    "does_not_claim_automatic_correctness": True,
    "does_not_create_line_call_truth": True,
    "does_not_create_event_truth": True,
    "does_not_create_point_truth": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_mutate_model_assets": True,
    "does_not_run_gpu_or_model_inference_by_default": True,
    "does_not_convert_outputs_into_training_labels": True,
    "no_adjudication": True,
    "observation_only": True,
    "review_support_only": True,
}

SMOKE_ENTRY_WARNINGS = {
    "smoke_entry_is_not_truth": True,
    "structural_evidence_chain_only": True,
    "explicit_media_path_only": True,
    "fixture_mode_does_not_prove_real_point_distinctness": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "no_adjudication": True,
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


def export_gameplay_gated_many_point_smoke_contract(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen Blueprint 42 gameplay-gated many-point smoke contract."""

    exported_at = exported_at or GAMEPLAY_GATED_MANY_POINT_SMOKE_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
        "manifest_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
        "manifest_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
        "report_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
        "contract": contract,
        "warnings": dict(SMOKE_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_gated_many_point_smoke_manifest_template(
    *,
    local_media_paths: list[str | Path] | None = None,
    source_label: str = DEFAULT_SOURCE_LABEL,
    requested_smoke_steps: list[str] | None = None,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_OUTPUT
    ),
    generated_at: datetime | None = None,
    allow_fixture_mode: bool = True,
) -> dict[str, Any]:
    """Build a user-editable explicit many-point gameplay smoke manifest."""

    generated_at = generated_at or datetime.now(UTC)
    steps = requested_smoke_steps or list(DEFAULT_REQUESTED_SMOKE_STEPS)
    paths = [str(path) for path in (local_media_paths or []) if str(path).strip()]
    entries = [
        _manifest_entry(
            local_media_path=path,
            source_label=_source_label_for_index(source_label=source_label, index=index),
            requested_smoke_steps=steps,
            allow_fixture_mode=allow_fixture_mode,
        )
        for index, path in enumerate(paths)
    ]
    if not entries:
        entries = [
            _manifest_entry(
                local_media_path="",
                source_label=source_label,
                requested_smoke_steps=[
                    "validate_media_path",
                    "summarize_smoke_readiness",
                ],
                allow_fixture_mode=allow_fixture_mode,
            )
        ]
    warnings = _warnings_with_fixture_reuse(entries)
    manifest = {
        "manifest_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
        "manifest_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "default_smoke_mode": DEFAULT_SMOKE_MODE,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "entry_count": len(entries),
        "entries": entries,
        "warnings": warnings,
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "manifest_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
        "manifest_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
        "entry_count": len(entries),
        "manifest": manifest,
        "warnings": warnings,
    }
    _write_json_if_requested(output_path, manifest, result, "manifest_output")
    return result


def validate_gameplay_gated_many_point_smoke_manifest(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a Blueprint 42 explicit gameplay-gated smoke manifest structurally."""

    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    manifest = _load_manifest(manifest_path=manifest_path, errors=errors)
    if manifest:
        result = _validate_manifest_shape(manifest)
        errors.extend(_list(result.get("errors")))
        structural_warnings.extend(_list(result.get("structural_warnings")))
    validation = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_gated_many_point_smoke_manifest_validation",
        "validation_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "manifest_path": str(Path(manifest_path)),
        "contract_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
        "manifest_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
        "manifest_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
        "entry_count": len(_manifest_entries(manifest)),
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "warnings": _warnings_with_fixture_reuse(_manifest_entries(manifest)),
    }
    _write_json_if_requested(output_path, validation, validation, "validation_output")
    return validation


def run_gameplay_gated_many_point_smoke(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    smoke_mode: str = DEFAULT_SMOKE_MODE,
    output_dir: str | Path = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT_DIR,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    many_point_contract_path: str | Path = DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    gameplay_segment_contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    routing_contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    execution_contract_path: str | Path = (
        DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT
    ),
    replay_review_contract_path: str | Path = (
        DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT
    ),
    viewer_base_url: str = "http://127.0.0.1:3000",
    frame_sample_rate: int = 30,
    max_frames: int | None = 240,
    generated_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    """Run the structural BP42 gameplay-gated many-point smoke workflow."""

    generated_at = generated_at or datetime.now(UTC)
    if smoke_mode not in ALLOWED_SMOKE_MODES:
        return _failed_report(
            status="invalid_smoke_manifest",
            message=f"unsupported smoke mode: {smoke_mode}",
            manifest_path=manifest_path,
            smoke_mode=smoke_mode,
            generated_at=generated_at,
            output_path=output_path,
        )

    validation = validate_gameplay_gated_many_point_smoke_manifest(
        contract_path=contract_path,
        manifest_path=manifest_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        report = _smoke_report(
            generated_at=generated_at,
            smoke_mode=smoke_mode,
            manifest_path=manifest_path,
            entries=[],
            validation=validation,
            many_point_ingestion_gate=None,
            status="invalid_smoke_manifest",
        )
        return _write_smoke_result(report=report, output_path=output_path, ok=False)

    manifest = _load_manifest(manifest_path=manifest_path, errors=[])
    output_root = Path(output_dir).expanduser()
    output_root.mkdir(parents=True, exist_ok=True)
    many_point_manifest_path = output_root / "many_point_ingestion_manifest.json"
    many_point_gate_path = output_root / "many_point_ingestion_gate.current.json"
    _write_json(
        many_point_manifest_path,
        _many_point_manifest_from_smoke_manifest(
            manifest=manifest,
            generated_at=generated_at,
        ),
    )
    many_point_gate = run_many_point_ingestion_gate(
        contract_path=many_point_contract_path,
        manifest_path=many_point_manifest_path,
        mode="dry_run",
        output_path=many_point_gate_path,
        generated_at=generated_at,
    )

    entries = [
        _run_smoke_entry(
            entry=entry,
            smoke_mode=smoke_mode,
            output_root=output_root,
            model_asset_path=model_asset_path,
            gameplay_segment_contract_path=gameplay_segment_contract_path,
            routing_contract_path=routing_contract_path,
            execution_contract_path=execution_contract_path,
            replay_review_contract_path=replay_review_contract_path,
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
        or many_point_gate.get("ok") is False
        else "completed"
    )
    report = _smoke_report(
        generated_at=generated_at,
        smoke_mode=smoke_mode,
        manifest_path=manifest_path,
        entries=entries,
        validation=validation,
        many_point_ingestion_gate={
            "output_path": str(many_point_gate_path),
            "ok": many_point_gate.get("ok"),
            "status": many_point_gate.get("status"),
            "mode": many_point_gate.get("mode"),
        },
        status=status,
    )
    return _write_smoke_result(report=report, output_path=output_path, ok=status == "completed")


def build_gameplay_gated_many_point_smoke_report(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
    smoke_report_path: str | Path,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a validated structural readiness report from a BP42 smoke run output."""

    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    report = _load_report(smoke_report_path=smoke_report_path, errors=errors)
    if report:
        errors.extend(_validate_report_shape(report))

    if errors:
        status = "invalid_smoke_report"
        report = _smoke_report(
            generated_at=generated_at,
            smoke_mode=str(report.get("smoke_mode") or DEFAULT_SMOKE_MODE),
            manifest_path=str(report.get("source_manifest_path") or ""),
            entries=[],
            validation={"ok": False, "status": "invalid", "errors": errors},
            many_point_ingestion_gate=None,
            status=status,
        )
    else:
        status = str(report.get("status") or "completed")
        report = dict(report)
        report["report_built_at"] = generated_at.isoformat()
        report["report_source_path"] = str(Path(smoke_report_path))
        report["validation_summary"] = {
            "status": "valid",
            "error_count": 0,
            "report_shape_valid": True,
            "validation_is_structural_only": True,
        }
        report["warnings"] = {
            **dict(SMOKE_WARNINGS),
            **_dict(report.get("warnings")),
        }

    result = {
        "ok": status != "invalid_smoke_report",
        "status": status,
        "report_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
        "smoke_report_id": report.get("smoke_report_id"),
        "entry_count": report.get("entry_count", 0),
        "summary": report.get("summary", {}),
        "report": report,
        "warnings": _dict(report.get("warnings")) or dict(SMOKE_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "smoke_scope": {
            "purpose": "gameplay_gated_many_point_structural_smoke",
            "default_smoke_mode": DEFAULT_SMOKE_MODE,
            "allowed_smoke_modes": sorted(ALLOWED_SMOKE_MODES),
            "explicit_media_manifest_required": True,
            "automatic_media_discovery_allowed": False,
            "silent_ingestion_allowed": False,
            "uses_many_point_ingestion_gate_dry_run": True,
            "uses_gameplay_segment_gate_fixture_mode": True,
            "uses_gameplay_gated_routing_plan": True,
            "uses_gameplay_gated_execution_plan": True,
            "uses_gameplay_replay_timeline": True,
            "runs_gpu_or_model_inference_by_default": False,
            "requires_external_downloads": False,
            "mutates_model_assets": False,
            "mutates_regression_baselines": False,
            "creates_labels_or_tennis_conclusions": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "smoke_manifest_schema": {
            "manifest_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE,
            "manifest_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION,
            "entries_required": True,
            "explicit_local_media_paths_required": True,
            "fixture_reuse_requires_warning": True,
            "allowed_requested_smoke_steps": sorted(ALLOWED_SMOKE_STEPS),
            "disallowed_requested_smoke_steps": sorted(DISALLOWED_SMOKE_STEPS),
        },
        "smoke_entry_schema": {
            "required_fields": [
                "smoke_entry_id",
                "local_media_path",
                "source_label",
                "expected_media_type",
                "allow_fixture_mode",
                "requested_smoke_steps",
                "notes",
                "warnings",
            ],
            "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
            "allowed_statuses": sorted(ALLOWED_ENTRY_STATUSES),
        },
        "smoke_report_schema": {
            "report_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
            "report_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
            "allowed_report_statuses": sorted(ALLOWED_REPORT_STATUSES),
            "required_fields": [
                "smoke_report_id",
                "generated_at",
                "smoke_mode",
                "source_manifest_path",
                "entry_count",
                "validated_entry_count",
                "gameplay_candidate_entry_count",
                "blocked_entry_count",
                "review_required_entry_count",
                "failed_entry_count",
                "entries",
                "summary",
                "warnings",
            ],
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_smoke_manifest_shape": True,
            "validate_smoke_report_shape": True,
            "validate_allowed_smoke_modes": True,
            "validate_allowed_statuses": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_exact_tokens": True,
            "reject_disallowed_requested_smoke_steps": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "source_manifest_path_required": True,
            "smoke_entry_id_required": True,
            "local_media_path_required": True,
            "path_exists_recorded": True,
            "model_asset_hash_recorded_when_available": True,
            "gameplay_segment_output_path_recorded_when_built": True,
            "routing_plan_output_path_recorded_when_built": True,
            "execution_plan_output_path_recorded_when_built": True,
            "replay_timeline_output_path_recorded_when_built": True,
            "fixture_reuse_warnings_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(SMOKE_WARNINGS),
    }


def _manifest_entry(
    *,
    local_media_path: str,
    source_label: str,
    requested_smoke_steps: list[str],
    allow_fixture_mode: bool,
) -> dict[str, Any]:
    return {
        "smoke_entry_id": _stable_id(
            "gameplay_gated_many_point_smoke_entry_v1",
            local_media_path,
            source_label,
        ),
        "local_media_path": local_media_path,
        "source_label": source_label,
        "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
        "allow_fixture_mode": allow_fixture_mode,
        "requested_smoke_steps": list(requested_smoke_steps),
        "notes": "Explicit media entry for structural gameplay-gated many-point smoke.",
        "warnings": dict(SMOKE_ENTRY_WARNINGS),
    }


def _run_smoke_entry(
    *,
    entry: dict[str, Any],
    smoke_mode: str,
    output_root: Path,
    model_asset_path: str | Path,
    gameplay_segment_contract_path: str | Path,
    routing_contract_path: str | Path,
    execution_contract_path: str | Path,
    replay_review_contract_path: str | Path,
    viewer_base_url: str,
    frame_sample_rate: int,
    max_frames: int | None,
    generated_at: datetime,
    probe_runner: Any | None,
) -> dict[str, Any]:
    entry_id = str(entry.get("smoke_entry_id") or _stable_id("smoke_entry", entry))
    paths = _entry_artifact_paths(output_root=output_root, entry_id=entry_id)
    steps = set(_string_list(entry.get("requested_smoke_steps")))
    local_media_path = str(entry.get("local_media_path") or "")
    path_exists = Path(local_media_path).expanduser().is_file()
    media_id = _stable_id("gameplay_gated_smoke_media_v1", entry_id, local_media_path)
    report_entry = _base_report_entry(
        entry=entry,
        media_id=media_id,
        path_exists=path_exists,
        smoke_mode=smoke_mode,
    )

    if smoke_mode == "validate_only":
        report_entry["status"] = "validated"
        return report_entry
    if smoke_mode == "dry_run":
        report_entry["status"] = "dry_run_planned"
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

    report_entry["status"] = (
        "structural_smoke_completed"
        if smoke_mode == "structural_smoke"
        else "fixture_smoke_completed"
    )
    report_entry["contract_paths"] = {
        "gameplay_segment_gate": str(gameplay_segment_contract_path),
        "gameplay_gated_routing": str(routing_contract_path),
        "gameplay_gated_execution": str(execution_contract_path),
        "gameplay_segment_replay_review": str(replay_review_contract_path),
    }
    return report_entry


def _base_report_entry(
    *,
    entry: dict[str, Any],
    media_id: str,
    path_exists: bool,
    smoke_mode: str,
) -> dict[str, Any]:
    return {
        "smoke_entry_id": entry.get("smoke_entry_id"),
        "local_media_path": entry.get("local_media_path"),
        "path_exists": path_exists,
        "media_id": media_id,
        "gameplay_segment_candidate_count": 0,
        "downstream_allowed_window_count": 0,
        "downstream_blocked_window_count": 0,
        "downstream_review_required_window_count": 0,
        "perception_execution_window_count": 0,
        "perception_skipped_window_count": 0,
        "replay_timeline_entry_count": 0,
        "status": "skipped",
        "smoke_mode": smoke_mode,
        "requested_smoke_steps": _string_list(entry.get("requested_smoke_steps")),
        "artifact_outputs": {},
        "contract_paths": {},
        "model_asset": {},
        "errors": [],
        "warnings": dict(SMOKE_ENTRY_WARNINGS),
    }


def _smoke_report(
    *,
    generated_at: datetime,
    smoke_mode: str,
    manifest_path: str | Path,
    entries: list[dict[str, Any]],
    validation: dict[str, Any],
    many_point_ingestion_gate: dict[str, Any] | None,
    status: str,
) -> dict[str, Any]:
    summary = _report_summary(entries=entries, validation=validation)
    warnings = _warnings_with_fixture_reuse(entries)
    report_id = _stable_id(
        "gameplay_gated_many_point_smoke_report_v1",
        str(Path(manifest_path)),
        smoke_mode,
        len(entries),
        json.dumps(summary, sort_keys=True),
    )
    return {
        "report_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
        "smoke_report_id": report_id,
        "generated_at": generated_at.isoformat(),
        "smoke_mode": smoke_mode,
        "source_manifest_path": str(Path(manifest_path)),
        "entry_count": len(entries),
        "validated_entry_count": summary["validated_entry_count"],
        "gameplay_candidate_entry_count": summary["gameplay_candidate_entry_count"],
        "blocked_entry_count": summary["blocked_entry_count"],
        "review_required_entry_count": summary["review_required_entry_count"],
        "failed_entry_count": summary["failed_entry_count"],
        "entries": entries,
        "summary": summary,
        "many_point_ingestion_gate": many_point_ingestion_gate,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
        "status": status,
        "warnings": warnings,
    }


def _report_summary(
    *,
    entries: list[dict[str, Any]],
    validation: dict[str, Any],
) -> dict[str, Any]:
    status_counts = Counter(str(entry.get("status")) for entry in entries)
    return {
        "entry_count": len(entries),
        "validated_entry_count": sum(1 for entry in entries if entry.get("path_exists") is True),
        "gameplay_candidate_entry_count": sum(
            1 for entry in entries if int(entry.get("gameplay_segment_candidate_count") or 0) > 0
        ),
        "blocked_entry_count": sum(
            1 for entry in entries if int(entry.get("downstream_blocked_window_count") or 0) > 0
        ),
        "review_required_entry_count": sum(
            1
            for entry in entries
            if int(entry.get("downstream_review_required_window_count") or 0) > 0
        ),
        "failed_entry_count": status_counts.get("failed", 0),
        "status_counts": dict(sorted(status_counts.items())),
        "manifest_validation_status": validation.get("status"),
        "manifest_validation_error_count": validation.get("error_count", 0),
        "smoke_is_structural_only": True,
        "does_not_create_tennis_truth": True,
        "does_not_mutate_model_assets": True,
        "does_not_mutate_regression_baselines": True,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "smoke_scope",
        "source_contract_refs",
        "smoke_manifest_schema",
        "smoke_entry_schema",
        "smoke_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    refs = _dict(contract.get("source_contract_refs"))
    for key, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _validate_manifest_shape(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_token_errors(manifest, path="smoke_manifest")
    structural_warnings: list[dict[str, Any]] = []
    if manifest.get("manifest_type") != GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_TYPE:
        errors.append(
            _error("invalid_manifest_type", "manifest_type", manifest.get("manifest_type"))
        )
    if manifest.get("manifest_version") != GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_VERSION:
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
    duplicate_paths = _duplicate_paths([entry for entry in entries if isinstance(entry, dict)])
    seen_entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("smoke_entry_must_be_object", path, entry))
            continue
        entry_errors, entry_warnings = _validate_manifest_entry(
            entry=entry,
            path=path,
            duplicate_paths=duplicate_paths,
        )
        errors.extend(entry_errors)
        structural_warnings.extend(entry_warnings)
        entry_id = _string_or_none(entry.get("smoke_entry_id"))
        if entry_id in seen_entry_ids:
            errors.append(_error("duplicate_smoke_entry_id", f"{path}.smoke_entry_id", entry_id))
        if entry_id is not None:
            seen_entry_ids.add(entry_id)
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_manifest_entry(
    *,
    entry: dict[str, Any],
    path: str,
    duplicate_paths: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    errors = _forbidden_token_errors(entry, path=path)
    structural_warnings: list[dict[str, Any]] = []
    for field in (
        "smoke_entry_id",
        "local_media_path",
        "source_label",
        "expected_media_type",
        "allow_fixture_mode",
        "requested_smoke_steps",
        "notes",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_smoke_entry_field", f"{path}.{field}", None))
    local_media_path = _string_or_none(entry.get("local_media_path"))
    if local_media_path is None:
        errors.append(_error("local_media_path_missing", f"{path}.local_media_path", None))
    else:
        media_path = Path(local_media_path).expanduser()
        if not media_path.is_file():
            errors.append(
                _error("local_media_path_not_found", f"{path}.local_media_path", local_media_path)
            )
        if str(media_path) in duplicate_paths:
            if entry.get("allow_fixture_mode") is True:
                structural_warnings.append(
                    _warning("fixture_media_reuse", path, local_media_path)
                )
            else:
                errors.append(
                    _error(
                        "duplicate_media_without_fixture_mode",
                        path,
                        local_media_path,
                    )
                )
    if _string_or_none(entry.get("smoke_entry_id")) is None:
        errors.append(_error("invalid_smoke_entry_id", f"{path}.smoke_entry_id", None))
    if _string_or_none(entry.get("source_label")) is None:
        errors.append(_error("source_label_missing", f"{path}.source_label", None))
    if entry.get("expected_media_type") != DEFAULT_EXPECTED_MEDIA_TYPE:
        errors.append(
            _error(
                "unsupported_expected_media_type",
                f"{path}.expected_media_type",
                entry.get("expected_media_type"),
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
    steps = entry.get("requested_smoke_steps")
    if not isinstance(steps, list) or not steps:
        errors.append(
            _error("requested_smoke_steps_must_be_list", f"{path}.requested_smoke_steps", steps)
        )
    else:
        for step in steps:
            if step in DISALLOWED_SMOKE_STEPS:
                errors.append(
                    _error("disallowed_requested_smoke_step", f"{path}.requested_smoke_steps", step)
                )
            elif step not in ALLOWED_SMOKE_STEPS:
                errors.append(
                    _error(
                        "unsupported_requested_smoke_step",
                        f"{path}.requested_smoke_steps",
                        step,
                    )
                )
    if not isinstance(entry.get("warnings"), dict):
        errors.append(_error("warnings_must_be_object", f"{path}.warnings", entry.get("warnings")))
    return errors, structural_warnings


def _validate_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, path="smoke_report")
    if report.get("report_type") != GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE:
        errors.append(_error("invalid_report_type", "report_type", report.get("report_type")))
    if report.get("report_version") != GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION:
        errors.append(
            _error("invalid_report_version", "report_version", report.get("report_version"))
        )
    if report.get("smoke_mode") not in ALLOWED_SMOKE_MODES:
        errors.append(_error("invalid_smoke_mode", "smoke_mode", report.get("smoke_mode")))
    if report.get("status") not in ALLOWED_REPORT_STATUSES:
        errors.append(_error("invalid_report_status", "status", report.get("status")))
    for field in (
        "smoke_report_id",
        "generated_at",
        "source_manifest_path",
        "entry_count",
        "validated_entry_count",
        "gameplay_candidate_entry_count",
        "blocked_entry_count",
        "review_required_entry_count",
        "failed_entry_count",
        "entries",
        "summary",
        "warnings",
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
        "smoke_entry_id",
        "local_media_path",
        "path_exists",
        "gameplay_segment_candidate_count",
        "downstream_allowed_window_count",
        "downstream_blocked_window_count",
        "downstream_review_required_window_count",
        "perception_execution_window_count",
        "perception_skipped_window_count",
        "replay_timeline_entry_count",
        "warnings",
    ):
        if field not in entry:
            errors.append(_error("missing_report_entry_field", f"entries[{index}].{field}", None))
    return errors


def _many_point_manifest_from_smoke_manifest(
    *,
    manifest: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    entries = [
        {
            "ingestion_entry_id": _stable_id(
                "many_point_ingestion_entry_for_smoke_v1",
                entry.get("smoke_entry_id"),
                entry.get("local_media_path"),
            ),
            "local_media_path": entry.get("local_media_path"),
            "source_label": entry.get("source_label"),
            "external_reference_id": entry.get("smoke_entry_id"),
            "intended_point_id": None,
            "collection_notes": "Generated from BP42 smoke manifest for BP33 dry-run gate.",
            "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
            "allow_duplicate_media": entry.get("allow_fixture_mode") is True,
            "requested_actions": ["validate_path", "build_replay_url"],
            "warnings": dict(SMOKE_ENTRY_WARNINGS),
        }
        for entry in _manifest_entries(manifest)
    ]
    return {
        "manifest_type": "many_point_ingestion_manifest",
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_contract_refs": {
            "observation_quality_taxonomy_version": "v1",
            "review_label_schema_version": "v1",
            "reviewer_confidence_schema_version": "v1",
            "multi_reviewer_disagreement_schema_version": "v1",
            "intennse_label_alignment_contract_version": "v1",
            "versioned_dataset_corpus_contract_version": "v1",
            "coverage_sampling_strategy_contract_version": "v1",
            "multi_point_regression_matrix_version": "v0",
            "point_manifest_version": "v0",
        },
        "entry_count": len(entries),
        "entries": entries,
        "warnings": {
            **dict(SMOKE_WARNINGS),
            "generated_from_gameplay_gated_many_point_smoke_manifest": True,
        },
    }


def _add_candidate_counts(report_entry: dict[str, Any], candidates_path: Path) -> None:
    candidates = _dict(_load_json(candidates_path, label="gameplay_segments").get("data"))
    segments = [
        segment
        for segment in _list(candidates.get("segment_candidates"))
        if isinstance(segment, dict)
    ]
    report_entry["gameplay_segment_candidate_count"] = sum(
        1 for segment in segments if segment.get("segment_status") == "gameplay_segment_candidate"
    )


def _add_routing_counts(report_entry: dict[str, Any], routing_plan_path: Path) -> None:
    routing_plan = _dict(_load_json(routing_plan_path, label="routing_plan").get("data"))
    report_entry["downstream_allowed_window_count"] = len(
        _list(routing_plan.get("allowed_windows"))
    )
    report_entry["downstream_blocked_window_count"] = len(
        _list(routing_plan.get("blocked_windows"))
    )
    report_entry["downstream_review_required_window_count"] = len(
        _list(routing_plan.get("uncertain_windows"))
    )


def _add_execution_counts(report_entry: dict[str, Any], execution_plan_path: Path) -> None:
    execution_plan = _dict(_load_json(execution_plan_path, label="execution_plan").get("data"))
    report_entry["perception_execution_window_count"] = len(
        _list(execution_plan.get("allowed_execution_windows"))
    )
    report_entry["perception_skipped_window_count"] = len(
        _list(execution_plan.get("skipped_windows"))
    )


def _mark_step_failed(
    report_entry: dict[str, Any],
    step: str,
    result: dict[str, Any],
) -> None:
    report_entry["status"] = "failed"
    report_entry["errors"].append(_error("smoke_step_failed", step, result.get("status")))


def _mark_step_skipped(report_entry: dict[str, Any], step: str) -> None:
    report_entry["errors"].append(_warning("smoke_step_skipped", step, None))


def _entry_artifact_paths(*, output_root: Path, entry_id: str) -> dict[str, Path]:
    entry_root = output_root / _slug(entry_id)
    entry_root.mkdir(parents=True, exist_ok=True)
    return {
        "model_asset_inspection": entry_root / "gameplay_classifier_asset_inspection.json",
        "gameplay_segments": entry_root / "gameplay_segment_candidates.json",
        "routing_plan": entry_root / "gameplay_gated_routing_plan.json",
        "execution_plan": entry_root / "gameplay_gated_execution_plan.json",
        "replay_timeline": entry_root / "gameplay_segment_replay_timeline.json",
    }


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(contract_path, label="gameplay_gated_many_point_smoke_contract")
    if loaded.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", loaded))
        return {}
    contract = _dict(loaded.get("data"))
    errors.extend(_validate_contract_shape(contract))
    return contract


def _load_manifest(
    *,
    manifest_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(manifest_path, label="gameplay_gated_many_point_smoke_manifest")
    if loaded.get("ok") is False:
        errors.append(_error("manifest_load_failed", "manifest_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _load_report(
    *,
    smoke_report_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(smoke_report_path, label="gameplay_gated_many_point_smoke_report")
    if loaded.get("ok") is False:
        errors.append(_error("report_load_failed", "smoke_report_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _failed_report(
    *,
    status: str,
    message: str,
    manifest_path: str | Path,
    smoke_mode: str,
    generated_at: datetime,
    output_path: str | Path | None,
) -> dict[str, Any]:
    report = _smoke_report(
        generated_at=generated_at,
        smoke_mode=smoke_mode,
        manifest_path=manifest_path,
        entries=[],
        validation={
            "ok": False,
            "status": "invalid",
            "error_count": 1,
            "errors": [_error(status, "smoke_mode", message)],
        },
        many_point_ingestion_gate=None,
        status=status,
    )
    return _write_smoke_result(report=report, output_path=output_path, ok=False)


def _write_smoke_result(
    *,
    report: dict[str, Any],
    output_path: str | Path | None,
    ok: bool,
) -> dict[str, Any]:
    result = {
        "ok": ok,
        "status": report.get("status"),
        "report_type": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_TYPE,
        "report_version": GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_VERSION,
        "smoke_report_id": report.get("smoke_report_id"),
        "entry_count": report.get("entry_count"),
        "summary": report.get("summary"),
        "report": report,
        "warnings": _dict(report.get("warnings")) or dict(SMOKE_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None or not str(output_path).strip():
        return
    path = Path(output_path).expanduser()
    _write_json(path, payload)
    result[result_key] = str(path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {
            "ok": False,
            "status": "missing_file",
            "label": label,
            "path": str(path),
        }
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(path),
            "error": str(exc),
        }
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "status": "invalid_json_shape",
            "label": label,
            "path": str(path),
        }
    return {"ok": True, "status": "loaded", "label": label, "path": str(path), "data": payload}


def _manifest_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in _list(manifest.get("entries"))
        if isinstance(entry, dict)
    ]


def _duplicate_paths(entries: list[dict[str, Any]]) -> set[str]:
    counts = Counter(
        str(Path(str(entry.get("local_media_path") or "")).expanduser())
        for entry in entries
        if str(entry.get("local_media_path") or "").strip()
    )
    return {path for path, count in counts.items() if count > 1}


def _warnings_with_fixture_reuse(entries: list[Any]) -> dict[str, Any]:
    entry_dicts = [entry for entry in entries if isinstance(entry, dict)]
    duplicate_paths = _duplicate_paths(entry_dicts)
    sample_point_reused = any(
        Path(path).name == "sample_point.mp4"
        for path in duplicate_paths
    )
    fixture_reuse = bool(duplicate_paths)
    warnings = dict(SMOKE_WARNINGS)
    warnings["fixture_reuse_only"] = fixture_reuse or sample_point_reused
    warnings["not_distinct_real_points"] = fixture_reuse or sample_point_reused
    warnings["does_not_claim_generalization"] = True
    return warnings


def _source_label_for_index(*, source_label: str, index: int) -> str:
    if index == 0:
        return source_label
    return f"{source_label}_{index + 1}"


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        "::".join(str(part) for part in parts).encode("utf-8")
    ).hexdigest()[:16]
    return f"{prefix}_{digest}"


def _slug(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)
    return safe[:96] or "entry"


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_GATED_MANY_POINT_SMOKE_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATED_MANY_POINT_SMOKE_BLUEPRINT_NAME,
    }


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_SMOKE_TOKENS:
                errors.append(_error("forbidden_token_key", nested_path, key_text))
            errors.extend(_forbidden_token_errors(nested, path=nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_SMOKE_TOKENS:
        errors.append(_error("forbidden_token_value", path, value))
    return errors


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
        "structural_only": True,
    }


def _warning(warning_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "warning_type": warning_type,
        "path": path,
        "value": value,
        "structural_only": True,
    }
