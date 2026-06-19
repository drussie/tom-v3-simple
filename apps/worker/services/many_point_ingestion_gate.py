from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_CONTRACT_VERSION,
)
from apps.worker.services.intennse_label_alignment import (
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.media_indexer import index_media
from apps.worker.services.multi_point_regression_matrix import (
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    build_multi_point_replay_index,
)
from apps.worker.services.multi_reviewer_disagreement import (
    MULTI_REVIEWER_SCHEMA_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    OBSERVATION_QUALITY_TAXONOMY_VERSION,
)
from apps.worker.services.point_manifest import (
    POINT_MANIFEST_OUTPUT_DIR,
    POINT_MANIFEST_VERSION,
    build_point_manifest,
)
from apps.worker.services.review_label_schema import (
    REVIEW_LABEL_SCHEMA_VERSION,
)
from apps.worker.services.reviewer_confidence_schema import (
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_CONTRACT_VERSION,
    DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    build_versioned_dataset_corpus_manifest,
)

MANY_POINT_INGESTION_CONTRACT_TYPE = "many_point_ingestion_gate_contract"
MANY_POINT_INGESTION_CONTRACT_VERSION = "v1"
MANY_POINT_INGESTION_MANIFEST_TYPE = "many_point_ingestion_manifest"
MANY_POINT_INGESTION_MANIFEST_VERSION = "v1"
MANY_POINT_INGESTION_PLAN_TYPE = "many_point_ingestion_plan"
MANY_POINT_INGESTION_PLAN_VERSION = "v1"
MANY_POINT_INGESTION_GATE_TYPE = "many_point_ingestion_gate_report"
MANY_POINT_INGESTION_GATE_VERSION = "v1"
MANY_POINT_INGESTION_BLUEPRINT = "blueprint_33"
MANY_POINT_INGESTION_BLUEPRINT_NAME = "many_point_evidence_ingestion_gate_v1"

DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT = (
    ".data/contracts/many_point_ingestion_gate_contract_v1.json"
)
DEFAULT_MANY_POINT_INGESTION_MANIFEST_TEMPLATE_OUTPUT = (
    ".data/exports/many_point_ingestion_manifest.template.json"
)
DEFAULT_MANY_POINT_INGESTION_VALIDATION_OUTPUT = (
    ".data/exports/many_point_ingestion_manifest.validation.json"
)
DEFAULT_MANY_POINT_INGESTION_PLAN_OUTPUT = (
    ".data/exports/many_point_ingestion_plan.current.json"
)
DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT = (
    ".data/exports/many_point_ingestion_gate.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)
DEFAULT_EXPECTED_MEDIA_TYPE = "local_video_file"
DEFAULT_SOURCE_LABEL = "local_point_video"

REQUESTED_ACTION_VALUES = [
    "validate_path",
    "index_media",
    "build_replay_url",
    "build_point_manifest",
    "include_in_multi_point_index",
    "include_in_dataset_corpus_manifest",
]

DISALLOWED_REQUESTED_ACTION_VALUES = [
    "generate_event_candidates",
    "arbitrate_markers",
    "generate_3d_candidates",
    "create_review_labels",
    "create_truth",
    "score_point",
    "identify_players",
]

EXECUTION_MODE_VALUES = [
    "dry_run",
    "validate_only",
    "index_only",
    "index_and_manifest",
]

WRITE_EXECUTION_MODES = {"index_only", "index_and_manifest"}

INGESTION_ENTRY_FIELDS = (
    {"key": "ingestion_entry_id", "required": True},
    {"key": "local_media_path", "required": True},
    {"key": "source_label", "required": True},
    {"key": "external_reference_id", "required": False},
    {"key": "intended_point_id", "required": False},
    {"key": "collection_notes", "required": False},
    {"key": "expected_media_type", "required": False},
    {"key": "allow_duplicate_media", "required": False},
    {"key": "requested_actions", "required": True},
    {"key": "warnings", "required": True},
)

FORBIDDEN_MANY_POINT_INGESTION_FIELDS = {
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
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "reviewer_score",
    "reviewer_rank",
    "training_truth",
    "model_ready_truth",
    "disagreement_resolution",
}

MANY_POINT_INGESTION_WARNINGS = {
    "ingestion_gate_is_not_truth": True,
    "planning_only": True,
    "provenance_only": True,
    "observation_only": True,
    "replay_support_only": True,
    "no_adjudication": True,
    "does_not_silently_ingest_media": True,
    "does_not_execute_sampling": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_review_labels": True,
    "does_not_create_training_truth": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_claim_generalization": True,
}

ENTRY_WARNINGS = {
    "many_point_ingestion_entry_is_not_truth": True,
    "planning_only": True,
    "provenance_only": True,
    "observation_only": True,
    "replay_support_only": True,
    "requested_actions_are_not_tennis_conclusions": True,
    "no_adjudication": True,
}


def export_many_point_ingestion_gate_contract(
    *,
    output_path: str | Path | None = DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen many-point ingestion gate contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": MANY_POINT_INGESTION_CONTRACT_TYPE,
        "contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "ingestion_gate_type": MANY_POINT_INGESTION_GATE_TYPE,
        "ingestion_gate_version": MANY_POINT_INGESTION_GATE_VERSION,
        "contract": contract,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_many_point_ingestion_manifest_template(
    *,
    local_media_paths: list[str | Path] | None = None,
    source_label: str = DEFAULT_SOURCE_LABEL,
    requested_actions: list[str] | None = None,
    output_path: str | Path | None = DEFAULT_MANY_POINT_INGESTION_MANIFEST_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a user-editable ingestion manifest template from explicit local paths."""

    generated_at = generated_at or datetime.now(UTC)
    actions = requested_actions or list(REQUESTED_ACTION_VALUES)
    paths = [str(path) for path in (local_media_paths or []) if str(path).strip()]
    entries = [
        _template_entry(
            local_media_path=path,
            source_label=_source_label_for_index(source_label=source_label, index=index),
            requested_actions=actions,
        )
        for index, path in enumerate(paths)
    ]
    if not entries:
        entries = [
            _template_entry(
                local_media_path="",
                source_label=source_label,
                requested_actions=["validate_path", "build_replay_url"],
            )
        ]
    manifest = {
        "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_contract_refs": _source_contract_refs(),
        "entry_count": len(entries),
        "entries": entries,
        "warnings": {
            **dict(MANY_POINT_INGESTION_WARNINGS),
            "template_may_use_demo_media_only": True,
            "template_does_not_prove_many_real_points": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "entry_count": len(entries),
        "manifest": manifest,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        result["manifest_output"] = str(path)
    return result


def validate_many_point_ingestion_manifest(
    *,
    contract_path: str | Path = DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    output_path: str | Path | None = DEFAULT_MANY_POINT_INGESTION_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate an explicit many-point ingestion manifest without indexing media."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="contract")
    manifest_loaded = _load_json(manifest_path, label="ingestion_manifest")
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []

    if contract_loaded.get("ok") is False:
        errors.append(_error("missing_or_invalid_contract", "contract_path", contract_path))
        contract = {}
    else:
        contract = _dict(contract_loaded.get("data"))
        errors.extend(_validate_contract_shape(contract))

    if manifest_loaded.get("ok") is False:
        errors.append(
            _error(
                str(manifest_loaded.get("status") or "invalid_ingestion_manifest"),
                "manifest_path",
                manifest_path,
            )
        )
        manifest = {}
    else:
        manifest = _dict(manifest_loaded.get("data"))
        manifest_result = _validate_manifest_shape(manifest=manifest)
        errors.extend(_list(manifest_result.get("errors")))
        structural_warnings.extend(_list(manifest_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "many_point_ingestion_manifest_validation",
        "validation_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "manifest_path": str(Path(manifest_path)),
        "contract_type": MANY_POINT_INGESTION_CONTRACT_TYPE,
        "contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "entry_count": len(_manifest_entries(manifest)),
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_many_point_ingestion_plan(
    *,
    contract_path: str | Path = DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    mode: str = "dry_run",
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_path: str | Path | None = DEFAULT_MANY_POINT_INGESTION_PLAN_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural plan describing what the ingestion gate would do."""

    generated_at = generated_at or datetime.now(UTC)
    if mode not in EXECUTION_MODE_VALUES:
        return _failed("unsafe_execution_mode", f"unsupported execution mode: {mode}")

    validation = validate_many_point_ingestion_manifest(
        contract_path=contract_path,
        manifest_path=manifest_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_ingestion_manifest",
            "validation": validation,
            "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
        }

    manifest_loaded = _load_json(manifest_path, label="ingestion_manifest")
    manifest = _dict(manifest_loaded.get("data"))
    entries = _manifest_entries(manifest)
    duplicate_context = _duplicate_context(entries)
    plan_entries = [
        _plan_entry(
            entry=entry,
            mode=mode,
            viewer_base_url=viewer_base_url,
            duplicate_context=duplicate_context,
        )
        for entry in entries
    ]
    plan = {
        "plan_type": MANY_POINT_INGESTION_PLAN_TYPE,
        "plan_version": MANY_POINT_INGESTION_PLAN_VERSION,
        "generated_at": generated_at.isoformat(),
        "mode": mode,
        "source_manifest_path": str(Path(manifest_path)),
        "contract_path": str(Path(contract_path)),
        "entry_count": len(plan_entries),
        "entries": plan_entries,
        "summary": _entry_summary(plan_entries),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(MANY_POINT_INGESTION_WARNINGS),
            "plan_only": True,
            "writes_enabled": mode in WRITE_EXECUTION_MODES,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "plan_type": MANY_POINT_INGESTION_PLAN_TYPE,
        "plan_version": MANY_POINT_INGESTION_PLAN_VERSION,
        "mode": mode,
        "entry_count": len(plan_entries),
        "summary": plan["summary"],
        "plan": plan,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
        result["plan_output"] = str(path)
    return result


def run_many_point_ingestion_gate(
    *,
    session: Session | None = None,
    contract_path: str | Path = DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    mode: str = "dry_run",
    viewer_base_url: str = "http://127.0.0.1:3000",
    storage_root: str | Path = ".data/media",
    copy_to_storage: bool = True,
    manifest_output_dir: str | Path = POINT_MANIFEST_OUTPUT_DIR,
    multi_point_index_output: str | Path = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    dataset_corpus_manifest_output: str | Path = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    multi_point_matrix_path: str | Path = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    output_path: str | Path | None = DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Run the ingestion gate. Defaults to dry-run and does not silently ingest media."""

    generated_at = generated_at or datetime.now(UTC)
    if mode not in EXECUTION_MODE_VALUES:
        return _failed("unsafe_execution_mode", f"unsupported execution mode: {mode}")
    if mode in WRITE_EXECUTION_MODES and session is None:
        return _failed("unsafe_execution_mode", "write execution mode requires a DB session")

    validation = validate_many_point_ingestion_manifest(
        contract_path=contract_path,
        manifest_path=manifest_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        report = _gate_report(
            mode=mode,
            manifest_path=manifest_path,
            generated_at=generated_at,
            entries=[],
            validation=validation,
            status="invalid_ingestion_manifest",
            extra_outputs={},
        )
        return _write_gate_result(report=report, output_path=output_path, ok=False)

    manifest = _dict(_load_json(manifest_path, label="ingestion_manifest").get("data"))
    duplicate_context = _duplicate_context(_manifest_entries(manifest))
    entries: list[dict[str, Any]] = []
    extra_outputs: dict[str, Any] = {}
    for entry in _manifest_entries(manifest):
        if mode in ("dry_run", "validate_only"):
            entries.append(
                _gate_dry_run_entry(
                    entry=entry,
                    mode=mode,
                    viewer_base_url=viewer_base_url,
                    duplicate_context=duplicate_context,
                )
            )
            continue
        entries.append(
            _gate_index_entry(
                session=session,
                entry=entry,
                mode=mode,
                viewer_base_url=viewer_base_url,
                storage_root=storage_root,
                copy_to_storage=copy_to_storage,
                manifest_output_dir=manifest_output_dir,
            )
        )

    if mode == "index_and_manifest":
        extra_outputs = _post_index_outputs(
            entries=entries,
            viewer_base_url=viewer_base_url,
            manifest_output_dir=manifest_output_dir,
            multi_point_index_output=multi_point_index_output,
            dataset_corpus_manifest_output=dataset_corpus_manifest_output,
            multi_point_matrix_path=multi_point_matrix_path,
        )

    status = (
        "completed_with_errors"
        if any(_entry_failed(entry) for entry in entries)
        else "completed"
    )
    report = _gate_report(
        mode=mode,
        manifest_path=manifest_path,
        generated_at=generated_at,
        entries=entries,
        validation=validation,
        status=status,
        extra_outputs=extra_outputs,
    )
    return _write_gate_result(report=report, output_path=output_path, ok=status == "completed")


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": MANY_POINT_INGESTION_CONTRACT_TYPE,
        "contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "ingestion_gate_type": MANY_POINT_INGESTION_GATE_TYPE,
        "ingestion_gate_version": MANY_POINT_INGESTION_GATE_VERSION,
        "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
        "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
        "plan_type": MANY_POINT_INGESTION_PLAN_TYPE,
        "plan_version": MANY_POINT_INGESTION_PLAN_VERSION,
        "ingestion_scope": {
            "purpose": (
                "Validate, plan, and explicitly gate indexing of multiple local point "
                "videos as replayable evidence assets."
            ),
            "default_execution_mode": "dry_run",
            "automatic_media_discovery_allowed": False,
            "silent_ingestion_allowed": False,
            "event_generation_allowed": False,
            "three_d_generation_allowed": False,
            "review_label_creation_allowed": False,
            "truth_creation_allowed": False,
            "training_truth_creation_allowed": False,
            "generalization_claim_allowed": False,
        },
        "source_contract_refs": _source_contract_refs(),
        "ingestion_manifest_schema": {
            "manifest_type": MANY_POINT_INGESTION_MANIFEST_TYPE,
            "manifest_version": MANY_POINT_INGESTION_MANIFEST_VERSION,
            "entries_required": True,
            "explicit_local_media_paths_required": True,
            "automatic_media_discovery_allowed": False,
        },
        "ingestion_entry_fields": [
            _entry_field_definition(field) for field in INGESTION_ENTRY_FIELDS
        ],
        "requested_action_values": list(REQUESTED_ACTION_VALUES),
        "disallowed_requested_action_values": list(DISALLOWED_REQUESTED_ACTION_VALUES),
        "execution_modes": [
            {
                "mode": mode,
                "writes_media_or_manifest_state": mode in WRITE_EXECUTION_MODES,
                "requires_explicit_mode": mode in WRITE_EXECUTION_MODES,
            }
            for mode in EXECUTION_MODE_VALUES
        ],
        "output_contracts": {
            "manifest_template_output": DEFAULT_MANY_POINT_INGESTION_MANIFEST_TEMPLATE_OUTPUT,
            "validation_output": DEFAULT_MANY_POINT_INGESTION_VALIDATION_OUTPUT,
            "plan_output": DEFAULT_MANY_POINT_INGESTION_PLAN_OUTPUT,
            "gate_report_output": DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
            "generated_exports_are_local_outputs": True,
        },
        "provenance_requirements": {
            "source_manifest_path_required": True,
            "local_media_path_required": True,
            "checksum_recorded_when_path_exists": True,
            "replay_url_returned_when_media_indexed": True,
            "point_manifest_returned_when_built": True,
            "duplicate_detection_by_path": True,
            "duplicate_detection_by_checksum_when_available": True,
            "requested_actions_are_planning_or_explicit_gate_actions": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "contract_version_checked": True,
            "manifest_type_version_checked": True,
            "local_media_paths_must_exist": True,
            "requested_actions_must_be_allowed": True,
            "disallowed_requested_actions_rejected": True,
            "duplicate_paths_or_checksums_rejected_unless_allowed": True,
            "write_modes_require_explicit_execution_mode": True,
            "does_not_run_event_generation": True,
            "does_not_run_marker_arbitration": True,
            "does_not_run_3d_generation": True,
            "does_not_create_review_labels": True,
            "does_not_create_truth": True,
            "does_not_create_training_truth": True,
            "forbidden_fields": sorted(FORBIDDEN_MANY_POINT_INGESTION_FIELDS),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
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
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _entry_field_definition(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": field["key"],
        "required": field["required"],
        "structural_only": True,
        "provenance_only": True,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _template_entry(
    *,
    local_media_path: str,
    source_label: str,
    requested_actions: list[str],
) -> dict[str, Any]:
    return {
        "ingestion_entry_id": _ingestion_entry_id(
            local_media_path=local_media_path,
            source_label=source_label,
        ),
        "local_media_path": local_media_path,
        "source_label": source_label,
        "external_reference_id": None,
        "intended_point_id": None,
        "collection_notes": (
            "Explicit local media path supplied by the operator. Demo assets are stand-ins only."
        ),
        "expected_media_type": DEFAULT_EXPECTED_MEDIA_TYPE,
        "allow_duplicate_media": False,
        "requested_actions": list(requested_actions),
        "warnings": dict(ENTRY_WARNINGS),
    }


def _source_label_for_index(*, source_label: str, index: int) -> str:
    if index == 0:
        return source_label
    return f"{source_label}_{index + 1}"


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != MANY_POINT_INGESTION_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != MANY_POINT_INGESTION_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "ingestion_scope",
        "source_contract_refs",
        "ingestion_manifest_schema",
        "ingestion_entry_fields",
        "validation_rules",
        "execution_modes",
        "output_contracts",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors
    errors.extend(
        _source_contract_ref_errors(
            _dict(contract.get("source_contract_refs")),
            path="contract.source_contract_refs",
        )
    )
    if set(_string_list(contract.get("requested_action_values"))) != set(
        REQUESTED_ACTION_VALUES
    ):
        errors.append(
            _error(
                "invalid_requested_action_values",
                "requested_action_values",
                contract.get("requested_action_values"),
            )
        )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "contract_version_checked",
        "manifest_type_version_checked",
        "local_media_paths_must_exist",
        "requested_actions_must_be_allowed",
        "disallowed_requested_actions_rejected",
        "duplicate_paths_or_checksums_rejected_unless_allowed",
        "write_modes_require_explicit_execution_mode",
        "does_not_run_event_generation",
        "does_not_run_marker_arbitration",
        "does_not_run_3d_generation",
        "does_not_create_review_labels",
        "does_not_create_truth",
        "does_not_create_training_truth",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_manifest_shape(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(manifest, path="ingestion_manifest")
    structural_warnings: list[dict[str, Any]] = []
    if manifest.get("manifest_type") != MANY_POINT_INGESTION_MANIFEST_TYPE:
        errors.append(
            _error("invalid_manifest_type", "manifest_type", manifest.get("manifest_type"))
        )
    if manifest.get("manifest_version") != MANY_POINT_INGESTION_MANIFEST_VERSION:
        errors.append(
            _error(
                "invalid_manifest_version",
                "manifest_version",
                manifest.get("manifest_version"),
            )
        )
    errors.extend(
        _source_contract_ref_errors(
            _dict(manifest.get("source_contract_refs")),
            path="ingestion_manifest.source_contract_refs",
        )
    )
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("entries_must_be_list", "entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}
    if not entries:
        errors.append(_error("entries_required", "entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}
    duplicate_context = _duplicate_context(
        [entry for entry in entries if isinstance(entry, dict)]
    )
    seen_entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("ingestion_entry_must_be_object", path, entry))
            continue
        entry_id = _string_or_none(entry.get("ingestion_entry_id"))
        if entry_id in seen_entry_ids:
            errors.append(
                _error(
                    "duplicate_ingestion_entry_id",
                    f"{path}.ingestion_entry_id",
                    entry_id,
                )
            )
        if entry_id is not None:
            seen_entry_ids.add(entry_id)
        result = _validate_entry(
            entry=entry,
            path=path,
            duplicate_context=duplicate_context,
        )
        errors.extend(_list(result.get("errors")))
        structural_warnings.extend(_list(result.get("structural_warnings")))
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_entry(
    *,
    entry: dict[str, Any],
    path: str,
    duplicate_context: dict[str, Any],
) -> dict[str, Any]:
    errors = _forbidden_field_errors(entry, path=path)
    structural_warnings: list[dict[str, Any]] = []
    for field in INGESTION_ENTRY_FIELDS:
        if field["required"] and field["key"] not in entry:
            errors.append(
                _error(
                    "missing_ingestion_entry_field",
                    f"{path}.{field['key']}",
                    None,
                )
            )
    if _string_or_none(entry.get("ingestion_entry_id")) is None:
        errors.append(
            _error(
                "invalid_ingestion_entry_id",
                f"{path}.ingestion_entry_id",
                entry.get("ingestion_entry_id"),
            )
        )
    local_media_path = _string_or_none(entry.get("local_media_path"))
    if local_media_path is None:
        errors.append(_error("local_media_path_missing", f"{path}.local_media_path", None))
    else:
        media_path = _expanded_path(local_media_path)
        if not media_path.is_file():
            errors.append(
                _error("local_media_path_not_found", f"{path}.local_media_path", local_media_path)
            )
    if _string_or_none(entry.get("source_label")) is None:
        errors.append(
            _error(
                "source_label_missing",
                f"{path}.source_label",
                entry.get("source_label"),
            )
        )
    if (
        entry.get("expected_media_type") or DEFAULT_EXPECTED_MEDIA_TYPE
    ) != DEFAULT_EXPECTED_MEDIA_TYPE:
        errors.append(
            _error(
                "unsupported_expected_media_type",
                f"{path}.expected_media_type",
                entry.get("expected_media_type"),
            )
        )
    if not isinstance(entry.get("allow_duplicate_media", False), bool):
        errors.append(
            _error(
                "allow_duplicate_media_must_be_boolean",
                f"{path}.allow_duplicate_media",
                entry.get("allow_duplicate_media"),
            )
        )
    actions = entry.get("requested_actions")
    if not isinstance(actions, list) or not actions:
        errors.append(
            _error("requested_actions_must_be_list", f"{path}.requested_actions", actions)
        )
    else:
        for action in actions:
            if action not in REQUESTED_ACTION_VALUES:
                errors.append(
                    _error("unsupported_requested_action", f"{path}.requested_actions", action)
                )
    if not isinstance(entry.get("warnings"), dict):
        errors.append(
            _error("warnings_must_be_object", f"{path}.warnings", entry.get("warnings"))
        )
    duplicate = _entry_duplicate(entry=entry, duplicate_context=duplicate_context)
    if duplicate and entry.get("allow_duplicate_media") is not True:
        errors.append(_error("duplicate_media_detected", path, duplicate))
    elif duplicate:
        structural_warnings.append(_warning("duplicate_media_allowed", path, duplicate))
    return {"errors": errors, "structural_warnings": structural_warnings}


def _plan_entry(
    *,
    entry: dict[str, Any],
    mode: str,
    viewer_base_url: str,
    duplicate_context: dict[str, Any],
) -> dict[str, Any]:
    path_info = _path_info(entry.get("local_media_path"))
    actions = _string_list(entry.get("requested_actions"))
    duplicate = _entry_duplicate(entry=entry, duplicate_context=duplicate_context)
    status = _planned_status(mode=mode, actions=actions)
    media_id = None
    replay_url = None
    if mode in WRITE_EXECUTION_MODES:
        status = "pending_index" if "index_media" in actions else "skipped_no_index_action"
    return {
        "ingestion_entry_id": entry.get("ingestion_entry_id"),
        "local_media_path": entry.get("local_media_path"),
        "path_exists": path_info["path_exists"],
        "checksum": path_info["checksum"],
        "duplicate_detected": duplicate is not None,
        "duplicate_reason": duplicate,
        "status": status,
        "mode": mode,
        "requested_actions": actions,
        "source_label": entry.get("source_label"),
        "expected_media_type": entry.get("expected_media_type") or DEFAULT_EXPECTED_MEDIA_TYPE,
        "allow_duplicate_media": entry.get("allow_duplicate_media") is True,
        "media_id": media_id,
        "replay_url": replay_url,
        "point_manifest_id": None,
        "point_manifest_path": None,
        "warnings": {
            **dict(ENTRY_WARNINGS),
            "writes_media_or_manifest_state": mode in WRITE_EXECUTION_MODES,
            "does_not_run_event_generation": True,
            "does_not_run_3d_generation": True,
        },
    }


def _gate_dry_run_entry(
    *,
    entry: dict[str, Any],
    mode: str,
    viewer_base_url: str,
    duplicate_context: dict[str, Any],
) -> dict[str, Any]:
    planned = _plan_entry(
        entry=entry,
        mode=mode,
        viewer_base_url=viewer_base_url,
        duplicate_context=duplicate_context,
    )
    planned["status"] = "validated" if mode == "validate_only" else "dry_run_planned"
    return planned


def _gate_index_entry(
    *,
    session: Session | None,
    entry: dict[str, Any],
    mode: str,
    viewer_base_url: str,
    storage_root: str | Path,
    copy_to_storage: bool,
    manifest_output_dir: str | Path,
) -> dict[str, Any]:
    actions = _string_list(entry.get("requested_actions"))
    path_info = _path_info(entry.get("local_media_path"))
    result = {
        "ingestion_entry_id": entry.get("ingestion_entry_id"),
        "local_media_path": entry.get("local_media_path"),
        "path_exists": path_info["path_exists"],
        "checksum": path_info["checksum"],
        "duplicate_detected": False,
        "duplicate_reason": None,
        "status": "skipped_no_index_action",
        "mode": mode,
        "requested_actions": actions,
        "source_label": entry.get("source_label"),
        "expected_media_type": entry.get("expected_media_type") or DEFAULT_EXPECTED_MEDIA_TYPE,
        "allow_duplicate_media": entry.get("allow_duplicate_media") is True,
        "media_id": None,
        "replay_url": None,
        "point_manifest_id": None,
        "point_manifest_path": None,
        "warnings": {
            **dict(ENTRY_WARNINGS),
            "writes_media_or_manifest_state": True,
            "does_not_run_event_generation": True,
            "does_not_run_3d_generation": True,
        },
    }
    if "index_media" not in actions:
        return result
    try:
        media = index_media(
            session=session,
            source_path=str(entry.get("local_media_path")),
            copy_to_storage=copy_to_storage,
            media_name=str(entry.get("source_label") or DEFAULT_SOURCE_LABEL),
            storage_root=storage_root,
        )
    except Exception as exc:  # pragma: no cover - defensive bridge around storage/probe runtime
        result["status"] = "indexing_failed"
        result["error"] = str(exc)
        return result
    result["media_id"] = media.id
    result["replay_url"] = f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
    result["status"] = "indexed"
    if mode == "index_and_manifest" and "build_point_manifest" in actions:
        manifest_result = build_point_manifest(
            session=session,
            media_id=media.id,
            viewer_base_url=viewer_base_url,
            output_dir=manifest_output_dir,
        )
        if manifest_result.get("ok") is False:
            result["status"] = "point_manifest_failed"
            result["point_manifest_error"] = manifest_result
        else:
            result["status"] = "manifest_built"
            result["point_manifest_id"] = manifest_result.get("point_manifest_id")
            result["point_manifest_path"] = manifest_result.get("manifest_output")
    return result


def _post_index_outputs(
    *,
    entries: list[dict[str, Any]],
    viewer_base_url: str,
    manifest_output_dir: str | Path,
    multi_point_index_output: str | Path,
    dataset_corpus_manifest_output: str | Path,
    multi_point_matrix_path: str | Path,
) -> dict[str, Any]:
    outputs: dict[str, Any] = {}
    if not any(entry.get("point_manifest_path") for entry in entries):
        return outputs
    wants_index = any(
        "include_in_multi_point_index" in _string_list(entry.get("requested_actions"))
        for entry in entries
    )
    wants_corpus = any(
        "include_in_dataset_corpus_manifest" in _string_list(entry.get("requested_actions"))
        for entry in entries
    )
    if wants_index:
        index_result = build_multi_point_replay_index(
            manifest_root=manifest_output_dir,
            output_path=multi_point_index_output,
            viewer_base_url=viewer_base_url,
        )
        outputs["multi_point_replay_index"] = index_result
    if wants_corpus:
        if not Path(multi_point_matrix_path).expanduser().is_file():
            outputs["dataset_corpus_manifest"] = {
                "ok": False,
                "status": "source_matrix_not_found",
                "source_matrix_path": str(multi_point_matrix_path),
                "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
            }
        else:
            outputs["dataset_corpus_manifest"] = build_versioned_dataset_corpus_manifest(
                source_index_path=multi_point_index_output,
                source_matrix_path=multi_point_matrix_path,
                output_path=dataset_corpus_manifest_output,
            )
    return outputs


def _gate_report(
    *,
    mode: str,
    manifest_path: str | Path,
    generated_at: datetime,
    entries: list[dict[str, Any]],
    validation: dict[str, Any],
    status: str,
    extra_outputs: dict[str, Any],
) -> dict[str, Any]:
    summary = _entry_summary(entries)
    return {
        "ingestion_gate_type": MANY_POINT_INGESTION_GATE_TYPE,
        "ingestion_gate_version": MANY_POINT_INGESTION_GATE_VERSION,
        "generated_at": generated_at.isoformat(),
        "mode": mode,
        "source_manifest_path": str(Path(manifest_path)),
        "entry_count": len(entries),
        "validated_entry_count": summary["validated_entry_count"],
        "indexed_entry_count": summary["indexed_entry_count"],
        "skipped_entry_count": summary["skipped_entry_count"],
        "failed_entry_count": summary["failed_entry_count"],
        "entries": entries,
        "summary": summary,
        "validation": validation,
        "status": status,
        "post_index_outputs": extra_outputs,
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(MANY_POINT_INGESTION_WARNINGS),
            "writes_media_or_manifest_state": mode in WRITE_EXECUTION_MODES,
        },
    }


def _write_gate_result(
    *,
    report: dict[str, Any],
    output_path: str | Path | None,
    ok: bool,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": ok,
        "status": report.get("status"),
        "ingestion_gate_type": MANY_POINT_INGESTION_GATE_TYPE,
        "ingestion_gate_version": MANY_POINT_INGESTION_GATE_VERSION,
        "mode": report.get("mode"),
        "entry_count": report.get("entry_count"),
        "validated_entry_count": report.get("validated_entry_count"),
        "indexed_entry_count": report.get("indexed_entry_count"),
        "skipped_entry_count": report.get("skipped_entry_count"),
        "failed_entry_count": report.get("failed_entry_count"),
        "summary": report.get("summary"),
        "report": report,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _planned_status(*, mode: str, actions: list[str]) -> str:
    if mode == "validate_only":
        return "validated"
    if mode == "dry_run":
        return "would_index" if "index_media" in actions else "dry_run_validated"
    return "pending_index" if "index_media" in actions else "skipped_no_index_action"


def _entry_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    statuses = Counter(str(entry.get("status") or "unknown") for entry in entries)
    indexed_statuses = {"indexed", "manifest_built"}
    failed_statuses = {"indexing_failed", "point_manifest_failed"}
    skipped_statuses = {"skipped_no_index_action"}
    return {
        "entry_count": len(entries),
        "validated_entry_count": sum(
            1
            for entry in entries
            if entry.get("status") in {"validated", "dry_run_planned", "would_index"}
            or entry.get("path_exists") is True
        ),
        "indexed_entry_count": sum(
            1 for entry in entries if entry.get("status") in indexed_statuses
        ),
        "skipped_entry_count": sum(
            1 for entry in entries if entry.get("status") in skipped_statuses
        ),
        "failed_entry_count": sum(
            1 for entry in entries if entry.get("status") in failed_statuses
        ),
        **{f"{status}_count": count for status, count in sorted(statuses.items())},
    }


def _entry_failed(entry: dict[str, Any]) -> bool:
    return str(entry.get("status")) in {"indexing_failed", "point_manifest_failed"}


def _source_contract_ref_errors(refs: dict[str, Any], *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    expected = _source_contract_refs()
    for key, expected_value in expected.items():
        if refs.get(key) != expected_value:
            errors.append(
                _error("invalid_source_contract_ref", f"{path}.{key}", refs.get(key))
            )
    return errors


def _duplicate_context(entries: list[dict[str, Any]]) -> dict[str, Any]:
    path_keys: list[str] = []
    checksums: list[str] = []
    entry_path_keys: dict[str, str] = {}
    entry_checksums: dict[str, str] = {}
    for entry in entries:
        entry_id = str(entry.get("ingestion_entry_id") or "")
        path_value = _string_or_none(entry.get("local_media_path"))
        if path_value is None:
            continue
        path_key = _path_key(path_value)
        path_keys.append(path_key)
        entry_path_keys[entry_id] = path_key
        media_path = _expanded_path(path_value)
        if media_path.is_file():
            checksum = _sha256(media_path)
            checksums.append(checksum)
            entry_checksums[entry_id] = checksum
    return {
        "path_counts": Counter(path_keys),
        "checksum_counts": Counter(checksums),
        "entry_path_keys": entry_path_keys,
        "entry_checksums": entry_checksums,
    }


def _entry_duplicate(
    *,
    entry: dict[str, Any],
    duplicate_context: dict[str, Any],
) -> dict[str, Any] | None:
    entry_id = str(entry.get("ingestion_entry_id") or "")
    path_key = _dict(duplicate_context.get("entry_path_keys")).get(entry_id)
    checksum = _dict(duplicate_context.get("entry_checksums")).get(entry_id)
    path_counts = duplicate_context.get("path_counts") or {}
    checksum_counts = duplicate_context.get("checksum_counts") or {}
    if path_key and path_counts.get(path_key, 0) > 1:
        return {"duplicate_type": "local_media_path", "value": path_key}
    if checksum and checksum_counts.get(checksum, 0) > 1:
        return {"duplicate_type": "checksum", "value": checksum}
    return None


def _path_info(value: object) -> dict[str, Any]:
    path_value = _string_or_none(value)
    if path_value is None:
        return {"path_exists": False, "checksum": None}
    media_path = _expanded_path(path_value)
    if not media_path.is_file():
        return {"path_exists": False, "checksum": None}
    return {"path_exists": True, "checksum": _sha256(media_path)}


def _path_key(path: str | Path) -> str:
    expanded = _expanded_path(path)
    try:
        return str(expanded.resolve())
    except OSError:
        return str(expanded)


def _expanded_path(path: str | Path) -> Path:
    return Path(path).expanduser()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ingestion_entry_id(*, local_media_path: str, source_label: str) -> str:
    payload = json.dumps(
        {
            "local_media_path": local_media_path,
            "source_label": source_label,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"many_point_ingestion_entry_v1_{digest}"


def _manifest_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in _list(manifest.get("entries")) if isinstance(entry, dict)]


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": MANY_POINT_INGESTION_BLUEPRINT,
        "blueprint_name": MANY_POINT_INGESTION_BLUEPRINT_NAME,
    }


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _failed(f"{label}_not_found", f"{label} JSON not found: {path}")
    except json.JSONDecodeError as exc:
        return _failed(f"invalid_{label}", f"{label} JSON is not valid: {path}: {exc}")
    if not isinstance(data, dict):
        return _failed(f"invalid_{label}", f"{label} JSON must be an object: {path}")
    return {"ok": True, "data": data}


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "contract_type": MANY_POINT_INGESTION_CONTRACT_TYPE,
        "contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "warnings": dict(MANY_POINT_INGESTION_WARNINGS),
    }


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in FORBIDDEN_MANY_POINT_INGESTION_FIELDS:
                errors.append(_error("forbidden_field", next_path, key))
            errors.extend(_forbidden_field_errors(item, path=next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_forbidden_field_errors(item, path=f"{path}[{index}]"))
    return errors


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "provenance_only": True,
        "no_adjudication": True,
    }


def _warning(warning_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "warning_type": warning_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "provenance_only": True,
        "no_adjudication": True,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]
