from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE = (
    "gameplay_gate_pathway_completion_freeze"
)
GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION = "v1"
GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_TYPE = (
    "gameplay_gate_next_phase_readiness_report"
)
GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_VERSION = "v1"
GAMEPLAY_GATE_PATHWAY_COMPLETION_BLUEPRINT = "blueprint_45"
GAMEPLAY_GATE_PATHWAY_COMPLETION_BLUEPRINT_NAME = (
    "gameplay_gate_pathway_completion_freeze_v1"
)

DEFAULT_GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT = (
    ".data/contracts/gameplay_gate_pathway_completion_freeze_v1.json"
)
DEFAULT_GAMEPLAY_GATE_PATHWAY_COMPLETION_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_gate_pathway_completion_freeze.validation.json"
)
DEFAULT_GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_OUTPUT = (
    ".data/exports/gameplay_gate_next_phase_readiness_report.current.json"
)

FREEZE_GENERATED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)
CURRENT_MAIN_COMMIT = "6d0f5441"
LATEST_COMPLETED_BLUEPRINT = {
    "blueprint": "blueprint_44",
    "title": "Gameplay Gate Review Dataset Export v1",
    "commit": "6d0f5441",
    "tag": "tom-v3-blueprint-44-gameplay-gate-review-dataset-export-v1",
}

GAMEPLAY_CLASSIFIER_ASSET_PATH = "model_assets/tom_v1/view_classifier_gameplay.pt"
EARLIER_TOM_V3_FREEZE_REF = ".data/contracts/tom_v3_expansion_completion_freeze_v1.json"
GAMEPLAY_GATE_REGRESSION_BASELINE_REF = (
    ".data/baselines/gameplay_gate_regression.baseline.json"
)

COMPLETED_GAMEPLAY_BLUEPRINTS = [
    ("blueprint_38", "Gameplay Segment Gate / TOM v1 View Classifier Integration"),
    ("blueprint_39", "Gameplay-Gated Evidence Pipeline Routing"),
    ("blueprint_40", "Gameplay-Gated Perception Execution Hook"),
    ("blueprint_41", "Gameplay Segment Replay Timeline / Operator Review"),
    ("blueprint_42", "Gameplay-Gated Many-Point Ingestion Smoke"),
    ("blueprint_43", "Gameplay Gate Regression Baseline"),
    ("blueprint_44", "Gameplay Gate Review Dataset Export"),
]

FROZEN_GAMEPLAY_CONTRACT_REFS = [
    ".data/contracts/gameplay_segment_gate_contract_v1.json",
    ".data/contracts/gameplay_gated_pipeline_routing_contract_v1.json",
    ".data/contracts/gameplay_gated_perception_execution_contract_v1.json",
    ".data/contracts/gameplay_segment_replay_review_contract_v1.json",
    ".data/contracts/gameplay_gated_many_point_smoke_contract_v1.json",
    ".data/contracts/gameplay_gate_regression_baseline_contract_v1.json",
    ".data/contracts/gameplay_gate_review_dataset_export_contract_v1.json",
]

PROTECTED_GAMEPLAY_BASELINE_REFS = [
    {
        "path": GAMEPLAY_GATE_REGRESSION_BASELINE_REF,
        "baseline_type": "gameplay_gate_regression_baseline",
        "tracked_required": True,
    }
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
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
        },
    },
    {
        "gate_id": "gameplay_gate_regression_baseline_gate",
        "make_target": "tom-v1-verify-gameplay-gate-regression-baseline",
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
            "gameplay_gate_is_not_truth": True,
            "classifier_correctness_not_assessed": True,
            "generalization_not_claimed": True,
        },
    },
]

CAPABILITY_SUMMARY = [
    "TOM v1 gameplay classifier asset provenance",
    "gameplay segment candidate contract",
    "gameplay/non-gameplay/uncertain segment structure",
    "downstream routing plan",
    "gameplay-gated perception execution plan",
    "replay timeline / operator review structure",
    "gameplay-gated many-point smoke path",
    "gameplay gate regression baseline",
    "gameplay gate review dataset export",
]

NON_CLAIMS = [
    "true gameplay",
    "classifier correctness",
    "classifier accuracy",
    "in/out truth",
    "point truth",
    "event truth",
    "rally truth",
    "score truth",
    "player identity truth",
    "production readiness",
    "real-world generalization from fixture/demo data",
    "automatic training labels",
    "automatic review correctness",
]

KNOWN_LIMITATIONS = [
    "Gameplay gate pathway is structurally complete but not yet real-data generalized.",
    "Fixture/demo assets may still dominate regression examples.",
    "Model inference may be fixture/mock-mode in CI.",
    "Human review remains required for gameplay boundary evaluation.",
    "Gameplay classifier output is structural suitability evidence, not truth.",
    "Review dataset export is pending actual reviewed human labels.",
    (
        "Downstream perception execution is safely gated/planned but may still require "
        "explicit real execution wiring per stage."
    ),
]

NEXT_PHASE_RECOMMENDATION = {
    "recommended_blueprint": "Blueprint 46 - Real Broadcast Gameplay Gate Corpus Run v1",
    "implementation_in_blueprint_45": False,
    "goal": "controlled_real_data_expansion",
    "suggested_architecture": [
        "explicit real broadcast clips",
        "gameplay segment gate",
        "gameplay-gated routing",
        "gameplay-gated perception execution",
        "replay timeline review",
        "review dataset export",
        "human review",
        "regression update candidate",
    ],
    "required_boundary": {
        "no_new_classifier_in_blueprint_45": True,
        "no_new_model_inference_in_blueprint_45": True,
        "no_production_or_generalization_claim": True,
    },
}

FORBIDDEN_GAMEPLAY_FREEZE_CLAIMS = {
    "in_out_truth",
    "score_truth",
    "point_winner_truth",
    "player_identity_truth",
    "adjudicated",
    "correct",
    "incorrect",
    "accepted",
    "rejected",
    "true_gameplay",
    "confirmed_gameplay",
    "classifier_accuracy_claim",
    "training_truth",
    "model_ready_truth",
    "generalization_proven",
    "production_ready_truth",
}

FREEZE_WARNINGS = {
    "gameplay_pathway_freeze_is_not_truth": True,
    "gameplay_gate_is_not_truth": True,
    "completion_freeze_is_structural_only": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_claimed": True,
    "generalization_not_claimed": True,
    "does_not_create_evidence": True,
    "does_not_create_observations": True,
    "does_not_create_review_labels": True,
    "does_not_create_training_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_model_assets": True,
    "does_not_mutate_gameplay_baselines": True,
    "does_not_execute_real_data_expansion": True,
    "no_adjudication": True,
    "observation_only": True,
    "provenance_only": True,
    "review_support_only": True,
}


def build_gameplay_gate_pathway_completion_freeze(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT,
    repo_root: str | Path = ".",
    current_main_commit: str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or FREEZE_GENERATED_AT
    current_main_commit = (
        current_main_commit
        or _git_output(["rev-parse", "--short", "main"], repo_root=repo_root)
        or CURRENT_MAIN_COMMIT
    )
    freeze = {
        "freeze_type": GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE,
        "freeze_version": GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
        "generated_at": generated_at.isoformat(),
        "current_main_commit": current_main_commit,
        "latest_completed_blueprint": dict(LATEST_COMPLETED_BLUEPRINT),
        "completed_gameplay_blueprints": [
            {"blueprint": blueprint, "title": title, "status": "complete"}
            for blueprint, title in COMPLETED_GAMEPLAY_BLUEPRINTS
        ],
        "frozen_gameplay_contract_refs": _frozen_contract_refs(),
        "protected_gameplay_baseline_refs": list(PROTECTED_GAMEPLAY_BASELINE_REFS),
        "earlier_tom_v3_completion_freeze_ref": {
            "path": EARLIER_TOM_V3_FREEZE_REF,
            "tracked_required": True,
            "referenced": True,
        },
        "gameplay_classifier_asset_ref": {
            "path": GAMEPLAY_CLASSIFIER_ASSET_PATH,
            "must_not_be_committed": True,
            "must_not_be_modified": True,
        },
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
            "validation_does_not_score_classifier": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(FREEZE_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "freeze_type": GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE,
        "freeze_version": GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
        "completed_gameplay_blueprint_count": len(COMPLETED_GAMEPLAY_BLUEPRINTS),
        "frozen_gameplay_contract_count": len(FROZEN_GAMEPLAY_CONTRACT_REFS),
        "freeze": freeze,
        "warnings": dict(FREEZE_WARNINGS),
    }
    _write_json_if_requested(output_path, freeze, result, "freeze_output")
    return result


def validate_gameplay_gate_pathway_completion_freeze(
    *,
    freeze_path: str | Path,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_PATHWAY_COMPLETION_VALIDATION_OUTPUT
    ),
    repo_root: str | Path = ".",
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    loaded = _load_json(freeze_path, label="gameplay_gate_pathway_completion_freeze")
    if loaded.get("ok") is False:
        return loaded
    freeze = _dict(loaded.get("data"))
    errors = _validate_freeze_shape(freeze)
    structural_warnings: list[dict[str, Any]] = []

    contract_validations = _validate_tracked_refs(
        refs=_paths_from_contract_refs(freeze.get("frozen_gameplay_contract_refs")),
        repo_root=repo_root,
        ref_type="frozen_gameplay_contract_ref",
    )
    baseline_validations = _validate_tracked_refs(
        refs=[GAMEPLAY_GATE_REGRESSION_BASELINE_REF],
        repo_root=repo_root,
        ref_type="protected_gameplay_baseline_ref",
    )
    earlier_freeze_validation = _validate_tracked_refs(
        refs=[EARLIER_TOM_V3_FREEZE_REF],
        repo_root=repo_root,
        ref_type="earlier_tom_v3_completion_freeze_ref",
    )
    for validation in (
        contract_validations + baseline_validations + earlier_freeze_validation
    ):
        if validation["ok"] is not True:
            errors.append(_error("missing_or_untracked_ref", validation["path"], validation))

    tracked_exports = _tracked_files(".data/exports", repo_root=repo_root)
    if tracked_exports:
        errors.append(_error("generated_exports_tracked", ".data/exports", tracked_exports))

    clean_refs = _tracked_refs_clean(
        refs=[
            *_paths_from_contract_refs(freeze.get("frozen_gameplay_contract_refs")),
            GAMEPLAY_GATE_REGRESSION_BASELINE_REF,
            EARLIER_TOM_V3_FREEZE_REF,
        ],
        repo_root=repo_root,
    )
    for validation in clean_refs:
        if validation["clean"] is not True:
            errors.append(_error("tracked_ref_dirty", validation["path"], validation))

    model_asset_validation = _validate_model_asset(repo_root=repo_root)
    if model_asset_validation["ok"] is not True:
        errors.append(
            _error(
                "model_asset_committed_or_modified",
                GAMEPLAY_CLASSIFIER_ASSET_PATH,
                model_asset_validation,
            )
        )

    status_short = _git_status_short(repo_root=repo_root)
    unexpected_status = [
        line
        for line in status_short
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
        "validation_type": "gameplay_gate_pathway_completion_freeze_validation",
        "validation_version": GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
        "validated_at": validated_at.isoformat(),
        "freeze_path": str(Path(freeze_path)),
        "freeze_type": freeze.get("freeze_type"),
        "freeze_version": freeze.get("freeze_version"),
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "frozen_gameplay_contract_validations": contract_validations,
        "protected_gameplay_baseline_validations": baseline_validations,
        "earlier_tom_v3_completion_freeze_validation": earlier_freeze_validation[0],
        "gameplay_classifier_asset_validation": model_asset_validation,
        "tracked_exports": tracked_exports,
        "tracked_contract_baseline_clean_validations": clean_refs,
        "git_status_short": status_short,
        "warnings": dict(FREEZE_WARNINGS),
        "known_limitations": [
            "Validation checks structure, expected tracked refs, model asset state, "
            "forbidden exact tokens, and generated export tracking.",
            "Validation does not run regression gates; run the protected Make gates separately.",
            "Validation does not create evidence, labels, truth, or classifier scores.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_gate_next_phase_readiness_report(
    *,
    freeze_path: str | Path = DEFAULT_GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT,
    output_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_OUTPUT
    ),
    repo_root: str | Path = ".",
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    loaded = _load_json(freeze_path, label="gameplay_gate_pathway_completion_freeze")
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

    validation = validate_gameplay_gate_pathway_completion_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
        validated_at=generated_at,
    )
    report = {
        "report_type": GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_freeze_path": str(Path(freeze_path)),
        "freeze_type": freeze.get("freeze_type"),
        "freeze_version": freeze.get("freeze_version"),
        "current_main_commit": freeze.get("current_main_commit"),
        "latest_completed_blueprint": _dict(freeze.get("latest_completed_blueprint")),
        "summary": {
            "completed_gameplay_blueprint_count": len(
                _list(freeze.get("completed_gameplay_blueprints"))
            ),
            "frozen_gameplay_contract_count": len(
                _list(freeze.get("frozen_gameplay_contract_refs"))
            ),
            "protected_gameplay_baseline_count": len(
                _list(freeze.get("protected_gameplay_baseline_refs"))
            ),
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
        "readiness_assessment": {
            "bp38_through_bp44_path_complete": True,
            "gameplay_contracts_frozen": True,
            "gameplay_regression_baseline_protected": True,
            "review_dataset_export_ready": True,
            "ready_for_controlled_real_broadcast_corpus_run": True,
            "readiness_is_structural_only": True,
            "does_not_implement_blueprint_46": True,
        },
        "next_phase_recommendations": _list(freeze.get("next_phase_recommendations")),
        "capability_summary": _list(freeze.get("capability_summary")),
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
        "report_type": GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _frozen_contract_refs() -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "tracked_required": True,
            "frozen": True,
            "generated_exports_are_not_tracked": True,
        }
        for path in FROZEN_GAMEPLAY_CONTRACT_REFS
    ]


def _validate_freeze_shape(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_claim_errors(freeze, path="freeze")
    if freeze.get("freeze_type") != GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE:
        errors.append(_error("invalid_freeze_type", "freeze_type", freeze.get("freeze_type")))
    if freeze.get("freeze_version") != GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION:
        errors.append(
            _error("invalid_freeze_version", "freeze_version", freeze.get("freeze_version"))
        )
    for section in (
        "current_main_commit",
        "latest_completed_blueprint",
        "completed_gameplay_blueprints",
        "frozen_gameplay_contract_refs",
        "protected_gameplay_baseline_refs",
        "earlier_tom_v3_completion_freeze_ref",
        "gameplay_classifier_asset_ref",
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
    if len(_list(freeze.get("completed_gameplay_blueprints"))) != len(
        COMPLETED_GAMEPLAY_BLUEPRINTS
    ):
        errors.append(
            _error(
                "completed_gameplay_blueprint_count_mismatch",
                "completed_gameplay_blueprints",
                len(_list(freeze.get("completed_gameplay_blueprints"))),
            )
        )
    if set(_paths_from_contract_refs(freeze.get("frozen_gameplay_contract_refs"))) != set(
        FROZEN_GAMEPLAY_CONTRACT_REFS
    ):
        errors.append(
            _error(
                "frozen_gameplay_contract_refs_mismatch",
                "frozen_gameplay_contract_refs",
                _paths_from_contract_refs(freeze.get("frozen_gameplay_contract_refs")),
            )
        )
    non_claim_text = " | ".join(
        str(item.get("claim", "")).lower()
        for item in _list(freeze.get("non_claims"))
        if isinstance(item, dict)
    )
    for phrase in NON_CLAIMS:
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
            first.get("recommended_blueprint")
            != "Blueprint 46 - Real Broadcast Gameplay Gate Corpus Run v1"
        ):
            errors.append(
                _error(
                    "invalid_next_phase_recommendation",
                    "next_phase_recommendations[0].recommended_blueprint",
                    first.get("recommended_blueprint"),
                )
            )
        if first.get("implementation_in_blueprint_45") is not False:
            errors.append(
                _error(
                    "blueprint_46_implemented_in_freeze",
                    "next_phase_recommendations[0].implementation_in_blueprint_45",
                    first.get("implementation_in_blueprint_45"),
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


def _validate_model_asset(*, repo_root: str | Path) -> dict[str, Any]:
    return {
        "path": GAMEPLAY_CLASSIFIER_ASSET_PATH,
        "exists": (Path(repo_root) / GAMEPLAY_CLASSIFIER_ASSET_PATH).is_file(),
        "tracked": _is_tracked(GAMEPLAY_CLASSIFIER_ASSET_PATH, repo_root=repo_root),
        "worktree_clean": _git_quiet(
            ["diff", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH],
            repo_root,
        ),
        "index_clean": _git_quiet(
            ["diff", "--cached", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH],
            repo_root,
        ),
        "ok": (
            not _is_tracked(GAMEPLAY_CLASSIFIER_ASSET_PATH, repo_root=repo_root)
            and _git_quiet(["diff", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH], repo_root)
            and _git_quiet(
                ["diff", "--cached", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH],
                repo_root,
            )
        ),
    }


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
            if str(key) in FORBIDDEN_GAMEPLAY_FREEZE_CLAIMS:
                errors.append(_error("forbidden_claim_key", child_path, key))
            errors.extend(_forbidden_claim_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_claim_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_GAMEPLAY_FREEZE_CLAIMS:
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


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _warning(warning_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"warning_type": warning_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_GATE_PATHWAY_COMPLETION_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATE_PATHWAY_COMPLETION_BLUEPRINT_NAME,
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
