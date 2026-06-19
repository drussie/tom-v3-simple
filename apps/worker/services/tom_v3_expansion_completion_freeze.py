from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE = "tom_v3_expansion_completion_freeze"
TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION = "v1"
TOM_V3_NEXT_PHASE_READINESS_REPORT_TYPE = "tom_v3_next_phase_readiness_report"
TOM_V3_NEXT_PHASE_READINESS_REPORT_VERSION = "v1"
TOM_V3_EXPANSION_COMPLETION_BLUEPRINT = "blueprint_37"
TOM_V3_EXPANSION_COMPLETION_BLUEPRINT_NAME = (
    "tom_v3_expansion_completion_freeze_v1"
)

DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT = (
    ".data/contracts/tom_v3_expansion_completion_freeze_v1.json"
)
DEFAULT_TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT = (
    ".data/exports/tom_v3_expansion_completion_freeze.validation.json"
)
DEFAULT_TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT = (
    ".data/exports/tom_v3_next_phase_readiness_report.current.json"
)

FREEZE_GENERATED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)
CURRENT_MAIN_COMMIT = "bb90aac8"
LATEST_COMPLETED_BLUEPRINT = {
    "blueprint": "blueprint_36",
    "title": "Camera Geometry Confidence / Calibration Provenance v1",
    "commit": "bb90aac8",
    "tag": "tom-v3-blueprint-36-camera-geometry-confidence-calibration-provenance-v1",
}

PROTECTED_SAMPLE_POINT_IDS = {
    "media_id": "9518fb01-0da1-4344-9a84-ff88ec8e9b1e",
    "event_candidate_run_id": "1b946366-7ec1-426f-8b40-494535a9b3fb",
    "trajectory_3d_run_id": "ea76ccab-c51d-4a63-9682-9fd0bbb83f14",
    "camera_geometry_id": "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97",
}

COMPLETED_BLUEPRINTS = [
    ("blueprint_22", "Second Point Evidence Parity / Protected Baseline Gate"),
    ("blueprint_23", "Point Manifest / Evidence Provenance Contract"),
    ("blueprint_24", "Multi-Point Replay Navigation / Review Surface"),
    ("blueprint_25", "Multi-Point Regression Matrix / Baseline Expansion"),
    ("blueprint_26", "Observation Quality Taxonomy"),
    ("blueprint_27", "Structured Review Label Schema"),
    ("blueprint_28", "Reviewer Confidence / Ambiguity Capture"),
    ("blueprint_29", "Multi-Reviewer / Disagreement Foundation"),
    ("blueprint_30", "INTENNSE Label Alignment Contract"),
    ("blueprint_31", "Versioned Dataset Corpus"),
    ("blueprint_32", "Coverage-Driven Sampling Strategy"),
    ("blueprint_33", "Many-Point Evidence Ingestion Gate"),
    ("blueprint_34", "Review Ops Metrics / Label Throughput Dashboard"),
    ("blueprint_35", "Label Feedback Loop into Evaluation Harness"),
    ("blueprint_36", "Camera Geometry Confidence / Calibration Provenance"),
]

FROZEN_CONTRACT_REFS = [
    ".data/contracts/observation_quality_taxonomy_v1.json",
    ".data/contracts/review_label_schema_v1.json",
    ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json",
    ".data/contracts/multi_reviewer_disagreement_schema_v1.json",
    ".data/contracts/intennse_label_alignment_contract_v1.json",
    ".data/contracts/versioned_dataset_corpus_contract_v1.json",
    ".data/contracts/coverage_sampling_strategy_contract_v1.json",
    ".data/contracts/many_point_ingestion_gate_contract_v1.json",
    ".data/contracts/review_ops_metrics_contract_v1.json",
    ".data/contracts/label_feedback_evaluation_contract_v1.json",
    ".data/contracts/camera_geometry_calibration_provenance_contract_v1.json",
]

PROTECTED_BASELINE_REFS = [
    {
        "path": ".data/baselines/multi_point_regression_matrix.baseline.json",
        "baseline_type": "multi_point_regression_matrix_baseline",
        "tracked_required": True,
    },
    {
        "baseline_type": "protected_sample_point_reviewed_3d_debug_baseline",
        "tracked_required": False,
        "identifiers": dict(PROTECTED_SAMPLE_POINT_IDS),
        "baseline_path": ".data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.json",
        "note": (
            "Protected sample baseline path may be locally generated while identifiers "
            "remain frozen."
        ),
    },
]

REQUIRED_REGRESSION_GATES = [
    {
        "gate_id": "multi_point_regression_matrix_gate",
        "make_target": "tom-v1-verify-multi-point-regression-matrix",
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
            "matrix_is_not_truth": True,
        },
    },
    {
        "gate_id": "protected_sample_point_reviewed_3d_debug_gate",
        "make_target": "tom-v1-verify-reviewed-3d-debug-baseline",
        "identifiers": dict(PROTECTED_SAMPLE_POINT_IDS),
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
        },
    },
]

CAPABILITY_SUMMARY = [
    "evidence persistence",
    "replay workstation",
    "review annotations",
    "point manifests",
    "multi-point replay index",
    "regression matrix protection",
    "observation quality taxonomy",
    "structured review label schema",
    "reviewer confidence and ambiguity schema",
    "multi-reviewer disagreement structure",
    "INTENNSE alignment contract",
    "versioned dataset corpus contract",
    "coverage-driven sampling strategy",
    "many-point ingestion gate",
    "review operations metrics",
    "label feedback loop into evaluation harness",
    "camera geometry calibration provenance",
]

NON_CLAIMS = [
    "line calling correctness",
    "in/out truth",
    "scoring truth",
    "player identity truth",
    "event truth",
    "rally truth",
    "match truth",
    "coaching conclusions",
    "tactical recommendations",
    "betting or prediction edge",
    "training-ready truth labels",
    "real-world generalization from sample or demo data",
    "fully automated broadcast filtering yet",
]

KNOWN_LIMITATIONS = [
    "The expansion is structurally complete but not production-generalized.",
    "Sample and demo assets still dominate protected regression examples.",
    "A real many-point corpus still needs controlled data expansion.",
    "Human review remains required.",
    "INTENNSE alignment is structural and not automatic expert interpretation.",
    "Camera calibration confidence is structural/provenance confidence only.",
    "Gameplay and broadcast filtering are not yet first-class in TOM v3.",
]

NEXT_PHASE_RECOMMENDATION = {
    "recommended_first_blueprint": (
        "Gameplay Segment Gate / TOM v1 View Classifier Integration v1"
    ),
    "existing_asset": "model_assets/tom_v1/view_classifier_gameplay.pt",
    "asset_treatment": "existing_proven_tom_v1_classifier",
    "recommended_flow": [
        "raw video",
        "TOM v1 gameplay classifier",
        "frame/window gameplay probabilities",
        "temporal smoothing / hysteresis",
        "gameplay segment candidates",
        "replay-visible gameplay timeline",
        "downstream processing gate",
        "detections / tracklets / pose / court / 3D only on allowed gameplay windows",
    ],
    "implementation_in_blueprint_37": False,
}

FORBIDDEN_FREEZE_CLAIMS = {
    "in_out_truth",
    "score_truth",
    "point_winner_truth",
    "player_identity_truth",
    "adjudicated",
    "correct",
    "incorrect",
    "accepted",
    "rejected",
    "training_truth",
    "model_ready_truth",
    "calibration_truth",
    "generalization_proven",
    "production_ready_truth",
}

FREEZE_WARNINGS = {
    "completion_freeze_is_not_truth": True,
    "system_readiness_is_structural_only": True,
    "does_not_create_evidence": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_review_labels": True,
    "does_not_convert_reviews_into_training_labels": True,
    "does_not_create_calibration_conclusions": True,
    "does_not_execute_sampling": True,
    "does_not_ingest_media": True,
    "does_not_retrain_models": True,
    "does_not_wire_gameplay_classifier": True,
    "does_not_claim_generalization": True,
    "no_adjudication": True,
    "observation_only": True,
    "provenance_only": True,
    "review_support_only": True,
}


def build_tom_v3_expansion_completion_freeze(
    *,
    output_path: str | Path | None = DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT,
    repo_root: str | Path = ".",
    current_main_commit: str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build the Blueprint 37 expansion completion freeze manifest."""

    generated_at = generated_at or FREEZE_GENERATED_AT
    current_main_commit = (
        current_main_commit
        or _git_output(["rev-parse", "--short", "main"], repo_root=repo_root)
        or CURRENT_MAIN_COMMIT
    )
    freeze = {
        "freeze_type": TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE,
        "freeze_version": TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
        "generated_at": generated_at.isoformat(),
        "current_main_commit": current_main_commit,
        "latest_completed_blueprint": dict(LATEST_COMPLETED_BLUEPRINT),
        "completed_blueprints": [
            {"blueprint": blueprint, "title": title, "status": "complete"}
            for blueprint, title in COMPLETED_BLUEPRINTS
        ],
        "frozen_contract_refs": _frozen_contract_refs(),
        "protected_baseline_refs": list(PROTECTED_BASELINE_REFS),
        "required_regression_gates": list(REQUIRED_REGRESSION_GATES),
        "capability_summary": [
            {"capability": capability, "status": "structurally_supported"}
            for capability in CAPABILITY_SUMMARY
        ],
        "non_claims": [
            {"claim": claim, "claimed": False, "structural_boundary": True}
            for claim in NON_CLAIMS
        ],
        "known_limitations": list(KNOWN_LIMITATIONS),
        "next_phase_recommendations": [dict(NEXT_PHASE_RECOMMENDATION)],
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "structural_warning_count": 0,
            "validation_does_not_create_truth": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(FREEZE_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "freeze_type": TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE,
        "freeze_version": TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
        "completed_blueprint_count": len(COMPLETED_BLUEPRINTS),
        "frozen_contract_count": len(FROZEN_CONTRACT_REFS),
        "freeze": freeze,
        "warnings": dict(FREEZE_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(freeze, indent=2, sort_keys=True), encoding="utf-8")
        result["freeze_output"] = str(path)
    return result


def validate_tom_v3_expansion_completion_freeze(
    *,
    freeze_path: str | Path,
    output_path: str | Path | None = DEFAULT_TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT,
    repo_root: str | Path = ".",
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate the Blueprint 37 completion freeze without changing repo state."""

    validated_at = validated_at or datetime.now(UTC)
    loaded = _load_json(freeze_path, label="tom_v3_expansion_completion_freeze")
    if loaded.get("ok") is False:
        return loaded
    freeze = _dict(loaded.get("data"))
    errors = _validate_freeze_shape(freeze)
    structural_warnings: list[dict[str, Any]] = []
    contract_validations = _validate_tracked_refs(
        refs=_paths_from_contract_refs(freeze.get("frozen_contract_refs")),
        repo_root=repo_root,
        ref_type="frozen_contract_ref",
    )
    baseline_validations = _validate_tracked_refs(
        refs=[".data/baselines/multi_point_regression_matrix.baseline.json"],
        repo_root=repo_root,
        ref_type="protected_baseline_ref",
    )
    for validation in contract_validations + baseline_validations:
        if validation["ok"] is not True:
            errors.append(
                _error(
                    "missing_or_untracked_ref",
                    validation["path"],
                    validation,
                )
            )

    tracked_exports = _tracked_files(".data/exports", repo_root=repo_root)
    if tracked_exports:
        errors.append(_error("generated_exports_tracked", ".data/exports", tracked_exports))

    contract_clean = _tracked_refs_clean(
        refs=_paths_from_contract_refs(freeze.get("frozen_contract_refs")),
        repo_root=repo_root,
    )
    for validation in contract_clean:
        if validation["clean"] is not True:
            errors.append(_error("frozen_contract_dirty", validation["path"], validation))

    known_status = _git_status_short(repo_root=repo_root)
    unexpected_status = [
        line
        for line in known_status
        if line.strip()
        and line.strip() != "?? tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak"
    ]
    if unexpected_status:
        structural_warnings.append(
            _warning("working_tree_has_non_backup_status", "git_status", unexpected_status)
        )

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "tom_v3_expansion_completion_freeze_validation",
        "validation_version": TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
        "validated_at": validated_at.isoformat(),
        "freeze_path": str(Path(freeze_path)),
        "freeze_type": TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE,
        "freeze_version": TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "frozen_contract_validations": contract_validations,
        "protected_baseline_validations": baseline_validations,
        "tracked_exports": tracked_exports,
        "tracked_contract_clean_validations": contract_clean,
        "git_status_short": known_status,
        "warnings": dict(FREEZE_WARNINGS),
        "known_limitations": [
            (
                "Validation checks freeze shape, expected refs, tracked refs, and "
                "forbidden claim tokens."
            ),
            "Validation does not run regression gates; run the protected Make gates separately.",
            "Validation does not create evidence, labels, training truth, or gameplay segments.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_tom_v3_next_phase_readiness_report(
    *,
    freeze_path: str | Path = DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT,
    output_path: str | Path | None = DEFAULT_TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT,
    repo_root: str | Path = ".",
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build the read-only next-phase readiness report from the freeze manifest."""

    generated_at = generated_at or datetime.now(UTC)
    loaded = _load_json(freeze_path, label="tom_v3_expansion_completion_freeze")
    if loaded.get("ok") is False:
        return loaded
    freeze = _dict(loaded.get("data"))
    errors = _validate_freeze_shape(freeze)
    if errors:
        return {
            "ok": False,
            "status": "invalid_freeze",
            "error_count": len(errors),
            "errors": errors,
            "warnings": dict(FREEZE_WARNINGS),
        }

    validation = validate_tom_v3_expansion_completion_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
        validated_at=generated_at,
    )
    report = {
        "report_type": TOM_V3_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": TOM_V3_NEXT_PHASE_READINESS_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_freeze_path": str(Path(freeze_path)),
        "freeze_type": freeze.get("freeze_type"),
        "freeze_version": freeze.get("freeze_version"),
        "current_main_commit": freeze.get("current_main_commit"),
        "latest_completed_blueprint": _dict(freeze.get("latest_completed_blueprint")),
        "summary": {
            "completed_blueprint_count": len(_list(freeze.get("completed_blueprints"))),
            "frozen_contract_count": len(_list(freeze.get("frozen_contract_refs"))),
            "protected_baseline_count": len(_list(freeze.get("protected_baseline_refs"))),
            "required_regression_gate_count": len(
                _list(freeze.get("required_regression_gates"))
            ),
            "capability_count": len(_list(freeze.get("capability_summary"))),
            "known_limitation_count": len(_list(freeze.get("known_limitations"))),
            "next_phase_recommendation_count": len(
                _list(freeze.get("next_phase_recommendations"))
            ),
            "freeze_validation_status": validation.get("status"),
            "freeze_validation_error_count": validation.get("error_count"),
        },
        "next_phase_recommendations": _list(freeze.get("next_phase_recommendations")),
        "readiness_assessment": {
            "bp22_through_bp36_path_complete": True,
            "standard_contracts_frozen": True,
            "protected_regression_gates_required": True,
            "ready_for_gameplay_segment_gate_blueprint": True,
            "readiness_is_structural_only": True,
        },
        "non_claims": _list(freeze.get("non_claims")),
        "known_limitations": _list(freeze.get("known_limitations")),
        "validation_snapshot": validation,
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(FREEZE_WARNINGS),
            "report_is_next_phase_readiness_only": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": TOM_V3_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": TOM_V3_NEXT_PHASE_READINESS_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": dict(FREEZE_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _frozen_contract_refs() -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "tracked_required": True,
            "frozen": True,
            "generated_exports_are_not_tracked": True,
        }
        for path in FROZEN_CONTRACT_REFS
    ]


def _validate_freeze_shape(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_claim_errors(freeze, path="freeze")
    if freeze.get("freeze_type") != TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE:
        errors.append(_error("invalid_freeze_type", "freeze_type", freeze.get("freeze_type")))
    if freeze.get("freeze_version") != TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION:
        errors.append(
            _error("invalid_freeze_version", "freeze_version", freeze.get("freeze_version"))
        )
    for section in (
        "current_main_commit",
        "latest_completed_blueprint",
        "completed_blueprints",
        "frozen_contract_refs",
        "protected_baseline_refs",
        "required_regression_gates",
        "capability_summary",
        "non_claims",
        "known_limitations",
        "next_phase_recommendations",
        "validation_summary",
        "warnings",
    ):
        if section not in freeze:
            errors.append(_error("missing_freeze_section", section, None))
    if len(_list(freeze.get("completed_blueprints"))) != len(COMPLETED_BLUEPRINTS):
        errors.append(
            _error(
                "completed_blueprint_count_mismatch",
                "completed_blueprints",
                len(_list(freeze.get("completed_blueprints"))),
            )
        )
    if set(_paths_from_contract_refs(freeze.get("frozen_contract_refs"))) != set(
        FROZEN_CONTRACT_REFS
    ):
        errors.append(
            _error(
                "frozen_contract_refs_mismatch",
                "frozen_contract_refs",
                _paths_from_contract_refs(freeze.get("frozen_contract_refs")),
            )
        )
    non_claim_text = " | ".join(
        str(item.get("claim", "")).lower()
        for item in _list(freeze.get("non_claims"))
        if isinstance(item, dict)
    )
    for phrase in (
        "line calling correctness",
        "in/out truth",
        "scoring truth",
        "player identity truth",
        "event truth",
        "rally truth",
        "match truth",
        "coaching conclusions",
        "tactical recommendations",
        "training-ready truth labels",
        "real-world generalization",
        "fully automated broadcast filtering",
    ):
        if phrase not in non_claim_text:
            errors.append(_error("missing_non_claim", "non_claims", phrase))
    recommendations = _list(freeze.get("next_phase_recommendations"))
    if not recommendations:
        errors.append(
            _error("missing_next_phase_recommendation", "next_phase_recommendations", None)
        )
    else:
        first = _dict(recommendations[0])
        if (
            first.get("recommended_first_blueprint")
            != "Gameplay Segment Gate / TOM v1 View Classifier Integration v1"
        ):
            errors.append(
                _error(
                    "invalid_first_next_phase_recommendation",
                    "next_phase_recommendations[0].recommended_first_blueprint",
                    first.get("recommended_first_blueprint"),
                )
            )
        if first.get("implementation_in_blueprint_37") is not False:
            errors.append(
                _error(
                    "next_phase_implemented_in_freeze",
                    "next_phase_recommendations[0].implementation_in_blueprint_37",
                    first.get("implementation_in_blueprint_37"),
                )
            )
    return errors


def _validate_tracked_refs(
    *,
    refs: list[str],
    repo_root: str | Path,
    ref_type: str,
) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    root = Path(repo_root)
    for ref in refs:
        exists = (root / ref).is_file()
        tracked = _is_tracked(ref, repo_root=repo_root)
        validations.append(
            {
                "ref_type": ref_type,
                "path": ref,
                "exists": exists,
                "tracked": tracked,
                "ok": exists and tracked,
            }
        )
    return validations


def _tracked_refs_clean(
    *,
    refs: list[str],
    repo_root: str | Path,
) -> list[dict[str, Any]]:
    return [
        {
            "path": ref,
            "worktree_clean": _git_quiet(["diff", "--quiet", "--", ref], repo_root),
            "index_clean": _git_quiet(["diff", "--cached", "--quiet", "--", ref], repo_root),
            "clean": _git_quiet(["diff", "--quiet", "--", ref], repo_root)
            and _git_quiet(["diff", "--cached", "--quiet", "--", ref], repo_root),
        }
        for ref in refs
    ]


def _paths_from_contract_refs(value: Any) -> list[str]:
    paths: list[str] = []
    for item in _list(value):
        if isinstance(item, dict):
            path = _string_or_none(item.get("path"))
            if path:
                paths.append(path)
        else:
            path = _string_or_none(item)
            if path:
                paths.append(path)
    return paths


def _forbidden_claim_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_FREEZE_CLAIMS:
                errors.append(_error("forbidden_claim_key", child_path, key))
            errors.extend(_forbidden_claim_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_claim_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_FREEZE_CLAIMS:
        errors.append(_error("forbidden_claim_value", path, value))
    return errors


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


def _tracked_files(pathspec: str, *, repo_root: str | Path) -> list[str]:
    output = _git_output(["ls-files", pathspec], repo_root=repo_root)
    return [line for line in output.splitlines() if line.strip()] if output else []


def _is_tracked(path: str, *, repo_root: str | Path) -> bool:
    return _git_quiet(["ls-files", "--error-unmatch", path], repo_root)


def _git_status_short(*, repo_root: str | Path) -> list[str]:
    output = _git_output(["status", "--short"], repo_root=repo_root)
    return [line for line in output.splitlines() if line.strip()] if output else []


def _git_output(args: list[str], *, repo_root: str | Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _git_quiet(args: list[str], repo_root: str | Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return result.returncode == 0


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _warning(warning_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"warning_type": warning_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": TOM_V3_EXPANSION_COMPLETION_BLUEPRINT,
        "blueprint_name": TOM_V3_EXPANSION_COMPLETION_BLUEPRINT_NAME,
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
