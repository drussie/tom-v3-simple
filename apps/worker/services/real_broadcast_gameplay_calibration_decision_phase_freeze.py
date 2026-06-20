from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE = (
    "real_broadcast_gameplay_calibration_decision_phase_freeze"
)
REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_TYPE = (
    "real_broadcast_gameplay_calibration_next_phase_readiness_report"
)
REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_BLUEPRINT = "blueprint_54"
REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_BLUEPRINT_NAME = (
    "real_broadcast_gameplay_calibration_decision_phase_freeze_v1"
)

DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT = (
    ".data/contracts/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VALIDATION_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_calibration_decision_phase_freeze.validation.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_calibration_next_phase_readiness_report.current.json"
)

PHASE_FREEZE_GENERATED_AT = datetime(2026, 6, 20, 0, 0, tzinfo=UTC)
CURRENT_MAIN_COMMIT = "133ddb23bdcdcb9eba153711f503cf95c0d87e94"
LATEST_COMPLETED_BLUEPRINT = {
    "blueprint": "blueprint_53",
    "title": "Candidate Config Freeze / Manual Approval Packet v1",
    "commit": CURRENT_MAIN_COMMIT,
    "tag": "tom-v3-blueprint-53-candidate-config-freeze-manual-approval-packet-v1",
}

GAMEPLAY_CLASSIFIER_ASSET_PATH = "model_assets/tom_v1/view_classifier_gameplay.pt"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_REF = (
    ".data/contracts/calibration_candidate_config_freeze_v1.json"
)
CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_REF = (
    ".data/exports/calibration_candidate_manual_approval_packet.current.json"
)

COMPLETED_PHASE_BLUEPRINTS = [
    ("blueprint_46", "Real Broadcast Gameplay Gate Corpus Run"),
    ("blueprint_47", "Real Broadcast Gameplay Review Loop"),
    ("blueprint_48", "Real Broadcast Gameplay Review Metrics / QA Dashboard"),
    ("blueprint_49", "Review-Guided Gameplay Gate Calibration Proposal"),
    ("blueprint_50", "Review-Guided Gameplay Calibration Evaluation Sandbox"),
    ("blueprint_51", "Calibration Evaluation Sandbox Regression Gate"),
    ("blueprint_52", "Calibration Candidate Decision Packet"),
    ("blueprint_53", "Candidate Config Freeze / Manual Approval Packet"),
]

FROZEN_CONTRACT_REFS = [
    ".data/contracts/tom_v3_expansion_completion_freeze_v1.json",
    ".data/contracts/gameplay_gate_pathway_completion_freeze_v1.json",
    ".data/contracts/gameplay_segment_gate_contract_v1.json",
    ".data/contracts/gameplay_gated_pipeline_routing_contract_v1.json",
    ".data/contracts/gameplay_gated_perception_execution_contract_v1.json",
    ".data/contracts/gameplay_segment_replay_review_contract_v1.json",
    ".data/contracts/gameplay_gated_many_point_smoke_contract_v1.json",
    ".data/contracts/gameplay_gate_regression_baseline_contract_v1.json",
    ".data/contracts/gameplay_gate_review_dataset_export_contract_v1.json",
    ".data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json",
    ".data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json",
    ".data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json",
    ".data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json",
    ".data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json",
    ".data/contracts/review_guided_gameplay_calibration_sandbox_regression_contract_v1.json",
    ".data/contracts/calibration_candidate_decision_packet_contract_v1.json",
    ".data/contracts/calibration_candidate_config_freeze_contract_v1.json",
    CALIBRATION_CANDIDATE_CONFIG_FREEZE_REF,
]

PROTECTED_BASELINE_REFS = [
    {
        "path": ".data/baselines/multi_point_regression_matrix.baseline.json",
        "baseline_type": "multi_point_regression_matrix_baseline",
        "tracked_required": True,
    },
    {
        "path": ".data/baselines/gameplay_gate_regression.baseline.json",
        "baseline_type": "gameplay_gate_regression_baseline",
        "tracked_required": True,
    },
    {
        "path": ".data/baselines/review_guided_gameplay_calibration_sandbox.baseline.json",
        "baseline_type": "review_guided_gameplay_calibration_sandbox_regression_baseline",
        "tracked_required": True,
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
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
        },
        "protected_sample_point_identifiers": {
            "media_id": "9518fb01-0da1-4344-9a84-ff88ec8e9b1e",
            "event_candidate_run_id": "1b946366-7ec1-426f-8b40-494535a9b3fb",
            "trajectory_3d_run_id": "ea76ccab-c51d-4a63-9682-9fd0bbb83f14",
            "camera_geometry_id": "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97",
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
    {
        "gate_id": "calibration_sandbox_regression_baseline_gate",
        "make_target": (
            "tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline"
        ),
        "expected": {
            "ok": True,
            "status": "completed",
            "drift_detected": False,
            "breaking_drift_detected": False,
            "baseline_is_not_truth": True,
            "sandbox_is_not_truth": True,
            "sandbox_is_not_accuracy_scoring": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
            "runtime_config_not_updated": True,
            "model_weights_not_modified": True,
            "baseline_not_replaced": True,
            "classifier_correctness_not_assessed": True,
            "generalization_not_claimed": True,
        },
    },
]

CAPABILITY_SUMMARY = [
    "explicit real broadcast gameplay corpus run structure",
    "real broadcast gameplay review loop",
    "real broadcast gameplay review metrics / QA dashboard",
    "review-guided calibration proposal",
    "offline calibration evaluation sandbox",
    "sandbox regression gate",
    "calibration candidate decision packet",
    "candidate config freeze / manual approval packet",
]

NON_CLAIMS = {
    "phase_freeze_is_not_truth": True,
    "gameplay_gate_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_assessed": True,
    "calibration_decision_phase_is_not_runtime_calibration": True,
    "candidate_config_freeze_is_not_runtime_config": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_operator_approval_required": True,
}

KNOWN_LIMITATIONS = [
    "Phase is decision-support complete, not runtime-calibration complete.",
    (
        "Real broadcast support is structurally ready but still depends on explicit "
        "local media manifests."
    ),
    "Human review remains required.",
    "Candidate configs are frozen for manual review only.",
    "No candidate setting is applied to runtime behavior.",
    "No classifier accuracy metrics are claimed.",
    "No production or generalization claims are made.",
    (
        "Future runtime calibration requires a separate controlled phase and explicit "
        "human approval."
    ),
]

NEXT_PHASE_RECOMMENDATION = {
    "recommended_blueprint": "Blueprint 55 - Controlled Runtime Calibration Change Request v1",
    "implementation_in_blueprint_54": False,
    "goal": "controlled_runtime_calibration_change_request",
    "requirements": [
        "explicit_human_approval_artifact",
        "selected_candidate_config_freeze",
        "all_regression_gates_passing",
        "no_unresolved_blockers",
        "explicit_rollback_plan",
        "runtime_config_change_request_not_direct_runtime_mutation",
        "dry_run_first",
        "review_after_application",
        "post_change_regression_baseline_candidate_only_after_validation",
        "still_no_truth_or_accuracy_claims",
    ],
}

PHASE_FREEZE_WARNINGS = {
    **NON_CLAIMS,
    "phase_freeze_is_structural_only": True,
    "decision_support_only": True,
    "manual_approval_packet_required_before_future_runtime_change": True,
    "does_not_create_evidence": True,
    "does_not_create_observations": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_training_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_model_assets": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_train_classifier": True,
    "no_adjudication": True,
    "observation_only": True,
    "provenance_only": True,
    "review_support_only": True,
}

FORBIDDEN_PHASE_FREEZE_CLAIMS = {
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
    "accuracy",
    "precision",
    "recall",
    "f1",
    "auc",
    "training_truth",
    "model_ready_truth",
    "generalization_proven",
    "production_ready_truth",
    "threshold_applied",
    "smoothing_applied",
    "hysteresis_applied",
    "threshold_changes_applied",
    "smoothing_changes_applied",
    "hysteresis_changes_applied",
    "model_updated",
    "model_weights_modified",
    "runtime_config_updated",
    "baseline_replaced",
    "auto_approved",
    "auto_rejected",
    "production_config",
}

REQUIRED_FREEZE_SECTIONS = [
    "freeze_type",
    "freeze_version",
    "generated_at",
    "current_main_commit",
    "latest_completed_blueprint",
    "completed_phase_blueprints",
    "frozen_contract_refs",
    "protected_baseline_refs",
    "required_regression_gates",
    "capability_summary",
    "decision_support_summary",
    "manual_approval_summary",
    "non_claims",
    "known_limitations",
    "next_phase_recommendations",
    "validation_summary",
    "warnings",
]


def build_real_broadcast_gameplay_calibration_decision_phase_freeze(
    *,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT
    ),
    repo_root: str | Path = ".",
    current_main_commit: str | None = None,
    candidate_config_freeze_path: str | Path = CALIBRATION_CANDIDATE_CONFIG_FREEZE_REF,
    manual_approval_packet_path: str | Path = CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_REF,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or PHASE_FREEZE_GENERATED_AT
    current_main_commit = (
        current_main_commit
        or _git_output(["rev-parse", "main"], repo_root=repo_root)
        or CURRENT_MAIN_COMMIT
    )
    candidate_config_freeze = _optional_json(candidate_config_freeze_path)
    manual_approval_packet = _optional_json(manual_approval_packet_path)
    freeze = {
        "freeze_type": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE,
        "freeze_version": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION,
        "generated_at": generated_at.isoformat(),
        "current_main_commit": current_main_commit,
        "latest_completed_blueprint": dict(LATEST_COMPLETED_BLUEPRINT),
        "completed_phase_blueprints": [
            {"blueprint": blueprint, "title": title, "status": "complete"}
            for blueprint, title in COMPLETED_PHASE_BLUEPRINTS
        ],
        "frozen_contract_refs": _frozen_contract_refs(),
        "protected_baseline_refs": list(PROTECTED_BASELINE_REFS),
        "gameplay_classifier_asset_ref": {
            "path": GAMEPLAY_CLASSIFIER_ASSET_PATH,
            "existing_model_asset": True,
            "must_not_be_committed": True,
            "must_not_be_modified": True,
            "must_not_be_tuned": True,
        },
        "required_regression_gates": list(REQUIRED_REGRESSION_GATES),
        "capability_summary": [
            {"capability": capability, "status": "structurally_supported"}
            for capability in CAPABILITY_SUMMARY
        ],
        "decision_support_summary": _decision_support_summary(candidate_config_freeze),
        "manual_approval_summary": _manual_approval_summary(
            candidate_config_freeze=candidate_config_freeze,
            candidate_config_freeze_path=candidate_config_freeze_path,
            manual_approval_packet=manual_approval_packet,
            manual_approval_packet_path=manual_approval_packet_path,
        ),
        "non_claims": dict(NON_CLAIMS),
        "known_limitations": list(KNOWN_LIMITATIONS),
        "next_phase_recommendations": [dict(NEXT_PHASE_RECOMMENDATION)],
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "validation_does_not_create_truth": True,
            "validation_does_not_score_classifier": True,
            "validation_does_not_apply_candidate_settings": True,
            "runtime_application_status": "not_applied",
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(PHASE_FREEZE_WARNINGS),
    }
    errors = _validate_freeze_shape(freeze)
    result: dict[str, Any] = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid",
        "freeze_type": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE,
        "freeze_version": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION,
        "completed_phase_blueprint_count": len(COMPLETED_PHASE_BLUEPRINTS),
        "frozen_contract_ref_count": len(FROZEN_CONTRACT_REFS),
        "protected_baseline_ref_count": len(PROTECTED_BASELINE_REFS),
        "error_count": len(errors),
        "errors": errors,
        "freeze": freeze,
        "warnings": dict(PHASE_FREEZE_WARNINGS),
    }
    _write_json_if_requested(output_path, freeze, result, "freeze_output")
    return result


def validate_real_broadcast_gameplay_calibration_decision_phase_freeze(
    *,
    freeze_path: str | Path,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VALIDATION_OUTPUT
    ),
    repo_root: str | Path = ".",
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    loaded = _load_json(
        freeze_path,
        label="real_broadcast_gameplay_calibration_decision_phase_freeze",
    )
    if loaded.get("ok") is False:
        return loaded
    freeze = _dict(loaded.get("data"))
    errors = _validate_freeze_shape(freeze)
    structural_warnings: list[dict[str, Any]] = []

    frozen_contract_validations = _validate_tracked_refs(
        refs=_paths_from_refs(freeze.get("frozen_contract_refs")),
        repo_root=repo_root,
        ref_type="frozen_contract_ref",
    )
    protected_baseline_validations = _validate_tracked_refs(
        refs=[item["path"] for item in PROTECTED_BASELINE_REFS],
        repo_root=repo_root,
        ref_type="protected_baseline_ref",
    )
    for validation in frozen_contract_validations + protected_baseline_validations:
        if validation["ok"] is not True:
            errors.append(_error("missing_or_untracked_ref", validation["path"], validation))

    manual_summary = _dict(freeze.get("manual_approval_summary"))
    if not manual_summary.get("candidate_config_freeze_referenced"):
        errors.append(
            _error(
                "candidate_config_freeze_not_referenced",
                "manual_approval_summary.candidate_config_freeze_referenced",
                manual_summary.get("candidate_config_freeze_referenced"),
            )
        )
    if not manual_summary.get("manual_approval_packet_referenced"):
        errors.append(
            _error(
                "manual_approval_packet_not_referenced",
                "manual_approval_summary.manual_approval_packet_referenced",
                manual_summary.get("manual_approval_packet_referenced"),
            )
        )

    tracked_exports = _tracked_files(".data/exports", repo_root=repo_root)
    if tracked_exports:
        errors.append(_error("generated_exports_tracked", ".data/exports", tracked_exports))

    clean_refs = _tracked_refs_clean(
        refs=[
            *_paths_from_refs(freeze.get("frozen_contract_refs")),
            *[item["path"] for item in PROTECTED_BASELINE_REFS],
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
        "validation_type": (
            "real_broadcast_gameplay_calibration_decision_phase_freeze_validation"
        ),
        "validation_version": (
            REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "freeze_path": str(Path(freeze_path)),
        "freeze_type": freeze.get("freeze_type"),
        "freeze_version": freeze.get("freeze_version"),
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "frozen_contract_validations": frozen_contract_validations,
        "protected_baseline_validations": protected_baseline_validations,
        "gameplay_classifier_asset_validation": model_asset_validation,
        "tracked_exports": tracked_exports,
        "tracked_contract_baseline_clean_validations": clean_refs,
        "manual_approval_summary": manual_summary,
        "git_status_short": status_short,
        "warnings": dict(PHASE_FREEZE_WARNINGS),
        "known_limitations": [
            "Validation checks structure, expected tracked refs, model asset state, "
            "forbidden exact tokens, and generated export tracking.",
            "Validation does not run regression gates; run the protected Make gates separately.",
            "Validation does not create evidence, labels, truth, or classifier scores.",
            "Validation does not approve or reject a candidate.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_real_broadcast_gameplay_calibration_next_phase_readiness_report(
    *,
    freeze_path: str | Path = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_OUTPUT
    ),
    repo_root: str | Path = ".",
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    loaded = _load_json(
        freeze_path,
        label="real_broadcast_gameplay_calibration_decision_phase_freeze",
    )
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
            "warnings": dict(PHASE_FREEZE_WARNINGS),
        }
    validation = validate_real_broadcast_gameplay_calibration_decision_phase_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
        validated_at=generated_at,
    )
    report = {
        "report_type": REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": (
            REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_freeze_path": str(Path(freeze_path)),
        "freeze_type": freeze.get("freeze_type"),
        "freeze_version": freeze.get("freeze_version"),
        "current_main_commit": freeze.get("current_main_commit"),
        "latest_completed_blueprint": _dict(freeze.get("latest_completed_blueprint")),
        "summary": {
            "completed_phase_blueprint_count": len(
                _list(freeze.get("completed_phase_blueprints"))
            ),
            "frozen_contract_ref_count": len(_list(freeze.get("frozen_contract_refs"))),
            "protected_baseline_ref_count": len(
                _list(freeze.get("protected_baseline_refs"))
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
            "runtime_application_status": "not_applied",
        },
        "readiness_assessment": {
            "bp46_through_bp53_phase_complete": True,
            "phase_contracts_frozen": True,
            "protected_baselines_identified": True,
            "candidate_settings_remain_not_applied": True,
            "manual_approval_required_before_future_runtime_change": True,
            "ready_for_blueprint_55_change_request_design": True,
            "ready_for_direct_runtime_mutation": False,
            "readiness_is_structural_only": True,
            "does_not_implement_blueprint_55": True,
        },
        "decision_support_summary": _dict(freeze.get("decision_support_summary")),
        "manual_approval_summary": _dict(freeze.get("manual_approval_summary")),
        "next_phase_recommendations": _list(freeze.get("next_phase_recommendations")),
        "capability_summary": _list(freeze.get("capability_summary")),
        "non_claims": _dict(freeze.get("non_claims")),
        "known_limitations": _list(freeze.get("known_limitations")),
        "validation_snapshot": validation,
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(PHASE_FREEZE_WARNINGS),
            "report_is_next_phase_readiness_only": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_TYPE,
        "report_version": (
            REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_VERSION
        ),
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
        for path in FROZEN_CONTRACT_REFS
    ]


def _decision_support_summary(candidate_config_freeze: dict[str, Any]) -> dict[str, Any]:
    review_coverage_summary = _dict(candidate_config_freeze.get("review_coverage_summary"))
    regression_gate_summary = _dict(candidate_config_freeze.get("regression_gate_summary"))
    return {
        "candidates_packaged_for_human_review": True,
        "candidate_settings_remain_not_applied": True,
        "runtime_application_supported_in_this_phase": False,
        "manual_approval_required_before_future_runtime_calibration": True,
        "human_review_coverage_summary": review_coverage_summary,
        "approval_blockers": _list(candidate_config_freeze.get("approval_blockers")),
        "drift_summary": regression_gate_summary,
        "regression_gates_required_before_future_consideration": True,
        "candidate_config_status": candidate_config_freeze.get(
            "candidate_config_status",
            "unknown",
        ),
        "runtime_application_status": candidate_config_freeze.get(
            "runtime_application_status",
            "not_applied",
        ),
        "not_applied": candidate_config_freeze.get("not_applied", True) is True,
    }


def _manual_approval_summary(
    *,
    candidate_config_freeze: dict[str, Any],
    candidate_config_freeze_path: str | Path,
    manual_approval_packet: dict[str, Any],
    manual_approval_packet_path: str | Path,
) -> dict[str, Any]:
    checklist = _list(manual_approval_packet.get("operator_checklist"))
    return {
        "candidate_config_freeze_path": str(Path(candidate_config_freeze_path)),
        "candidate_config_freeze_referenced": True,
        "candidate_config_freeze_exists": bool(candidate_config_freeze),
        "candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
        "manual_approval_packet_path": str(Path(manual_approval_packet_path)),
        "manual_approval_packet_referenced": True,
        "manual_approval_packet_exists": bool(manual_approval_packet),
        "manual_approval_packet_id": manual_approval_packet.get("manual_approval_packet_id"),
        "approval_required": True,
        "source_candidate_approval_required": candidate_config_freeze.get(
            "approval_required"
        ),
        "runtime_application_status": "not_applied",
        "operator_checklist_requirements_present": bool(checklist)
        or "required_preconditions" in candidate_config_freeze,
        "operator_checklist_item_count": len(checklist),
        "automatic_approval_occurred": False,
        "automatic_rejection_occurred": False,
        "deployable_runtime_configuration_created": False,
        "human_operator_approval_required": True,
        "known_blockers": _list(candidate_config_freeze.get("approval_blockers")),
    }


def _validate_freeze_shape(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_claim_errors(freeze, path="freeze")
    if (
        freeze.get("freeze_type")
        != REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE
    ):
        errors.append(_error("invalid_freeze_type", "freeze_type", freeze.get("freeze_type")))
    if (
        freeze.get("freeze_version")
        != REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION
    ):
        errors.append(
            _error("invalid_freeze_version", "freeze_version", freeze.get("freeze_version"))
        )
    for section in REQUIRED_FREEZE_SECTIONS:
        if section not in freeze:
            errors.append(_error("missing_freeze_section", section, None))
    if len(_list(freeze.get("completed_phase_blueprints"))) != len(
        COMPLETED_PHASE_BLUEPRINTS
    ):
        errors.append(
            _error(
                "completed_phase_blueprint_count_mismatch",
                "completed_phase_blueprints",
                len(_list(freeze.get("completed_phase_blueprints"))),
            )
        )
    if set(_paths_from_refs(freeze.get("frozen_contract_refs"))) != set(
        FROZEN_CONTRACT_REFS
    ):
        errors.append(
            _error(
                "frozen_contract_refs_mismatch",
                "frozen_contract_refs",
                _paths_from_refs(freeze.get("frozen_contract_refs")),
            )
        )
    protected_paths = {
        item.get("path")
        for item in _list(freeze.get("protected_baseline_refs"))
        if isinstance(item, dict)
    }
    expected_protected_paths = {item["path"] for item in PROTECTED_BASELINE_REFS}
    if protected_paths != expected_protected_paths:
        errors.append(
            _error(
                "protected_baseline_refs_mismatch",
                "protected_baseline_refs",
                sorted(protected_paths),
            )
        )
    non_claims = _dict(freeze.get("non_claims"))
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(_error("missing_non_claim", f"non_claims.{key}", None))
    recommendations = _list(freeze.get("next_phase_recommendations"))
    if not recommendations:
        errors.append(
            _error("missing_next_phase_recommendation", "next_phase_recommendations", None)
        )
    else:
        first = _dict(recommendations[0])
        if (
            first.get("recommended_blueprint")
            != "Blueprint 55 - Controlled Runtime Calibration Change Request v1"
        ):
            errors.append(
                _error(
                    "invalid_next_phase_recommendation",
                    "next_phase_recommendations[0].recommended_blueprint",
                    first.get("recommended_blueprint"),
                )
            )
        if first.get("implementation_in_blueprint_54") is not False:
            errors.append(
                _error(
                    "blueprint_55_implemented_in_freeze",
                    "next_phase_recommendations[0].implementation_in_blueprint_54",
                    first.get("implementation_in_blueprint_54"),
                )
            )
    decision_support_summary = _dict(freeze.get("decision_support_summary"))
    if decision_support_summary.get("candidate_settings_remain_not_applied") is not True:
        errors.append(
            _error(
                "candidate_settings_not_not_applied",
                "decision_support_summary.candidate_settings_remain_not_applied",
                decision_support_summary.get("candidate_settings_remain_not_applied"),
            )
        )
    manual_approval_summary = _dict(freeze.get("manual_approval_summary"))
    if manual_approval_summary.get("runtime_application_status") != "not_applied":
        errors.append(
            _error(
                "manual_approval_runtime_application_not_not_applied",
                "manual_approval_summary.runtime_application_status",
                manual_approval_summary.get("runtime_application_status"),
            )
        )
    if manual_approval_summary.get("automatic_approval_occurred") is not False:
        errors.append(
            _error(
                "automatic_approval_occurred",
                "manual_approval_summary.automatic_approval_occurred",
                manual_approval_summary.get("automatic_approval_occurred"),
            )
        )
    if manual_approval_summary.get("automatic_rejection_occurred") is not False:
        errors.append(
            _error(
                "automatic_rejection_occurred",
                "manual_approval_summary.automatic_rejection_occurred",
                manual_approval_summary.get("automatic_rejection_occurred"),
            )
        )
    if (
        manual_approval_summary.get("deployable_runtime_configuration_created")
        is not False
    ):
        errors.append(
            _error(
                "deployable_runtime_configuration_created",
                "manual_approval_summary.deployable_runtime_configuration_created",
                manual_approval_summary.get("deployable_runtime_configuration_created"),
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
    worktree_clean = _git_quiet(
        ["diff", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH],
        repo_root,
    )
    index_clean = _git_quiet(
        ["diff", "--cached", "--quiet", "--", GAMEPLAY_CLASSIFIER_ASSET_PATH],
        repo_root,
    )
    return {
        "path": GAMEPLAY_CLASSIFIER_ASSET_PATH,
        "exists": (Path(repo_root) / GAMEPLAY_CLASSIFIER_ASSET_PATH).is_file(),
        "tracked": _is_tracked(GAMEPLAY_CLASSIFIER_ASSET_PATH, repo_root=repo_root),
        "worktree_clean": worktree_clean,
        "index_clean": index_clean,
        "ok": worktree_clean and index_clean,
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


def _paths_from_refs(value: Any) -> list[str]:
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
            if str(key) in FORBIDDEN_PHASE_FREEZE_CLAIMS:
                errors.append(_error("forbidden_claim_key", child_path, key))
            errors.extend(_forbidden_claim_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_claim_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_PHASE_FREEZE_CLAIMS:
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


def _optional_json(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    loaded = _load_json(path, label=str(path))
    if loaded.get("ok") is not True:
        return {}
    return _dict(loaded.get("data"))


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
        "blueprint": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_BLUEPRINT,
        "blueprint_name": REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_BLUEPRINT_NAME,
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
