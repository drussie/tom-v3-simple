from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_application_execution_review_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_blocked_execution_resolution_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_TYPE = (
    "controlled_runtime_calibration_blocked_execution_resolution_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_TYPE = (
    "controlled_runtime_calibration_blocked_execution_resolution_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_TYPE = (
    "controlled_runtime_calibration_blocker_resolution_checklist"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ACTION_PLAN_TYPE = (
    "controlled_runtime_calibration_operator_action_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_REQUIREMENTS_TYPE = (
    "controlled_runtime_calibration_candidate_selection_requirements"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PLAN_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_PLAN_TYPE = (
    "controlled_runtime_calibration_reexecution_readiness_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_BLUEPRINT = (
    "blueprint_65"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_blocked_execution_resolution_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_blocked_execution_resolution_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_blocked_execution_resolution_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_blocked_execution_resolution_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_blocked_execution_resolution_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_blocked_execution_resolution_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_blocker_resolution_checklist.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ACTION_PLAN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_operator_action_plan.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_REQUIREMENTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_candidate_selection_requirements.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PLAN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_final_gate_rerun_plan.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_PLAN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_readiness_plan.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_application_execution_review_packet_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_application_execution_contract_version": "v1",
    "controlled_runtime_calibration_pre_application_final_gate_contract_version": "v1",
    "controlled_runtime_calibration_runtime_application_staging_contract_version": "v1",
    "controlled_runtime_calibration_application_plan_contract_version": "v1",
    "controlled_runtime_calibration_human_approval_gate_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_review_packet_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_execution_contract_version": "v1",
    "controlled_runtime_calibration_change_request_contract_version": "v1",
    "real_broadcast_gameplay_calibration_decision_phase_freeze_version": "v1",
    "calibration_candidate_config_freeze_contract_version": "v1",
    "calibration_candidate_decision_packet_contract_version": "v1",
    "review_guided_gameplay_calibration_sandbox_regression_contract_version": "v1",
    "review_guided_gameplay_calibration_evaluation_sandbox_contract_version": "v1",
    "review_guided_gameplay_calibration_proposal_contract_version": "v1",
    "real_broadcast_gameplay_review_metrics_contract_version": "v1",
    "real_broadcast_gameplay_review_loop_contract_version": "v1",
    "real_broadcast_gameplay_corpus_run_contract_version": "v1",
    "gameplay_gate_review_dataset_export_contract_version": "v1",
    "gameplay_gate_pathway_completion_freeze_version": "v1",
    "gameplay_gate_regression_baseline_contract_version": "v1",
    "gameplay_segment_replay_review_contract_version": "v1",
    "gameplay_gated_many_point_smoke_contract_version": "v1",
    "gameplay_gated_perception_execution_contract_version": "v1",
    "gameplay_gated_pipeline_routing_contract_version": "v1",
    "gameplay_segment_gate_contract_version": "v1",
    "many_point_ingestion_gate_contract_version": "v1",
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

ALLOWED_RESOLUTION_PACKET_STATUSES = [
    "resolution_packet_created_for_blocked_execution",
    "resolution_packet_created_with_warnings",
    "resolution_packet_blocked_missing_review_packet",
    "resolution_packet_blocked_missing_execution_artifact",
    "resolution_packet_blocked_missing_blocker_summary",
    "resolution_packet_informational_only",
    "not_applicable",
]
ALLOWED_BLOCKER_RESOLUTION_STATUSES = [
    "blockers_identified_resolution_required",
    "blockers_partially_identified",
    "blockers_missing",
    "blockers_already_resolved_external_artifact_required",
    "blocker_resolution_not_applicable",
    "not_applicable",
]
ALLOWED_OPERATOR_ACTION_STATUSES = [
    "operator_signoff_required",
    "operator_action_required",
    "operator_action_plan_created",
    "operator_action_blocked",
    "operator_action_not_applicable",
    "not_applicable",
]
ALLOWED_CANDIDATE_SELECTION_STATUSES = [
    "selected_candidate_required",
    "candidate_selection_required",
    "candidate_selection_plan_created",
    "candidate_selection_blocked",
    "candidate_selection_not_applicable",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_STATUSES = [
    "final_gate_rerun_required",
    "final_gate_rerun_plan_created",
    "final_gate_rerun_blocked",
    "final_gate_rerun_not_applicable",
    "not_applicable",
]
ALLOWED_REEXECUTION_READINESS_STATUSES = [
    "reexecution_not_ready_blockers_unresolved",
    "reexecution_readiness_plan_created",
    "reexecution_ready_after_required_artifacts",
    "reexecution_blocked",
    "reexecution_not_applicable",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "resolve_operator_signoff_before_reapplying",
    "select_candidate_before_reapplying",
    "create_operator_signoff_artifact",
    "create_selected_candidate_artifact",
    "rerun_final_gate_after_resolution",
    "rerun_application_execution_after_final_gate_passes",
    "prepare_resolution_followup_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

RESOLUTION_PACKET_INPUT_REQUIRED_FIELDS = [
    "resolution_packet_input_id",
    "resolution_packet_input_type",
    "resolution_packet_input_version",
    "generated_at",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_runtime_config_artifact_path",
    "source_rollback_package_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_phase_freeze_path",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "application_execution_status",
    "application_outcome_status",
    "runtime_application_status",
    "runtime_config_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "blocker_types",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]

RESOLUTION_PACKET_REQUIRED_FIELDS = [
    "resolution_packet_id",
    "resolution_packet_type",
    "resolution_packet_version",
    "generated_at",
    "source_resolution_packet_input_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "application_execution_status",
    "application_outcome_status",
    "runtime_application_status",
    "runtime_config_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "resolution_packet_status",
    "blocker_resolution_status",
    "operator_action_status",
    "candidate_selection_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "blocker_resolution_checklist",
    "operator_action_plan",
    "candidate_selection_requirements",
    "final_gate_rerun_plan",
    "reexecution_readiness_plan",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]

BLOCKER_RESOLUTION_CHECKLIST_ITEMS = [
    "inspect_bp64_review_packet",
    "inspect_bp62_execution_artifact",
    "confirm_application_blocked_safely",
    "confirm_runtime_config_unchanged",
    "confirm_no_runtime_mutation",
    "confirm_model_weights_not_modified",
    "confirm_baselines_not_replaced",
    "identify_missing_operator_signoff",
    "identify_missing_selected_candidate",
    "identify_final_gate_not_passed",
    "require_operator_signoff_artifact",
    "require_selected_candidate_artifact",
    "require_final_gate_rerun",
    "require_reexecution_only_after_final_gate_passes",
]
OPERATOR_ACTION_PLAN_REQUIRED_FIELDS = [
    "operator_action_plan_id",
    "operator_action_plan_version",
    "generated_at",
    "source_resolution_packet_id",
    "required_operator_artifacts",
    "required_operator_decisions",
    "operator_review_checklist",
    "operator_action_status",
    "warnings",
    "non_claims",
]
CANDIDATE_SELECTION_REQUIREMENTS_REQUIRED_FIELDS = [
    "candidate_selection_requirements_id",
    "candidate_selection_requirements_version",
    "generated_at",
    "source_resolution_packet_id",
    "required_candidate_refs",
    "candidate_selection_constraints",
    "candidate_selection_status",
    "warnings",
    "non_claims",
]
FINAL_GATE_RERUN_PLAN_REQUIRED_FIELDS = [
    "final_gate_rerun_plan_id",
    "final_gate_rerun_plan_version",
    "generated_at",
    "source_resolution_packet_id",
    "required_inputs",
    "required_preconditions",
    "required_regression_gates",
    "final_gate_rerun_status",
    "warnings",
    "non_claims",
]
REEXECUTION_READINESS_PLAN_REQUIRED_FIELDS = [
    "reexecution_readiness_plan_id",
    "reexecution_readiness_plan_version",
    "generated_at",
    "source_resolution_packet_id",
    "required_inputs",
    "required_preconditions",
    "required_regression_gates",
    "required_rollback_artifacts",
    "required_post_execution_review",
    "reexecution_readiness_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "blocked_execution_resolution_packet_is_not_truth": True,
    "blocked_execution_resolution_packet_is_not_accuracy_scoring": True,
    "blocked_execution_resolution_packet_is_not_model_training": True,
    "blocked_execution_resolution_packet_is_not_runtime_application": True,
    "resolution_packet_does_not_create_operator_signoff": True,
    "resolution_packet_does_not_select_candidate": True,
    "resolution_packet_does_not_rerun_final_gate": True,
    "resolution_packet_does_not_execute_application": True,
    "controlled_runtime_config_update_not_performed": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_not_modified": True,
    "classifier_correctness_not_assessed": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_resolution_required": True,
}

WARNINGS = {
    "controlled_blocked_execution_resolution_packet": True,
    "operator_signoff_required": True,
    "selected_candidate_required": True,
    "final_gate_rerun_required": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "human_resolution_required": True,
    "application_blocked_safely_before_runtime_mutation": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "no_runtime_mutation_due_to_blocker": True,
    **NON_CLAIMS,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_RESOLUTION_PACKET_TOKENS = {
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
    "accuracy",
    "precision",
    "recall",
    "f1",
    "auc",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_quality",
    _forbidden_token("model", "updated"),
    _forbidden_token("model", "weights", "modified"),
    _forbidden_token("baseline", "replaced"),
    _forbidden_token("auto", "approved"),
    _forbidden_token("auto", "rejected"),
    _forbidden_token("production", "config", "created"),
    _forbidden_token("uncontrolled", "runtime", "config", "update"),
    _forbidden_token("runtime", "application", "without", "final", "gate"),
    _forbidden_token("runtime", "application", "without", "rollback", "package"),
    _forbidden_token("runtime", "application", "without", "post", "apply", "verification"),
    _forbidden_token("fake", "operator", "signoff"),
    _forbidden_token("fake", "candidate", "selection"),
}


def export_controlled_runtime_calibration_blocked_execution_resolution_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "resolution_packet_scope": {
            "packages_blocked_execution_resolution_requirements": True,
            "does_not_write_runtime_config": True,
            "does_not_create_operator_signoff": True,
            "does_not_select_candidate": True,
            "does_not_rerun_final_gate": True,
            "does_not_execute_application": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
            "does_not_create_production_config": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "resolution_packet_input_schema": {
            "input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_TYPE
            ),
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_VERSION
            ),
            "required_fields": list(RESOLUTION_PACKET_INPUT_REQUIRED_FIELDS),
        },
        "resolution_packet_schema": {
            "packet_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_TYPE,
            "packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(RESOLUTION_PACKET_REQUIRED_FIELDS),
            "allowed_resolution_packet_statuses": list(
                ALLOWED_RESOLUTION_PACKET_STATUSES
            ),
            "allowed_blocker_resolution_statuses": list(
                ALLOWED_BLOCKER_RESOLUTION_STATUSES
            ),
            "allowed_operator_action_statuses": list(ALLOWED_OPERATOR_ACTION_STATUSES),
            "allowed_candidate_selection_statuses": list(
                ALLOWED_CANDIDATE_SELECTION_STATUSES
            ),
            "allowed_final_gate_rerun_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(
                ALLOWED_REEXECUTION_READINESS_STATUSES
            ),
            "allowed_next_action_recommendations": list(
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS
            ),
        },
        "blocker_resolution_checklist_schema": {
            "checklist_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_TYPE,
            "checklist_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_items": list(BLOCKER_RESOLUTION_CHECKLIST_ITEMS),
        },
        "operator_action_plan_schema": {
            "plan_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ACTION_PLAN_TYPE,
            "plan_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(OPERATOR_ACTION_PLAN_REQUIRED_FIELDS),
        },
        "candidate_selection_requirements_schema": {
            "requirements_type": (
                CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_REQUIREMENTS_TYPE
            ),
            "requirements_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(CANDIDATE_SELECTION_REQUIREMENTS_REQUIRED_FIELDS),
        },
        "final_gate_rerun_plan_schema": {
            "plan_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PLAN_TYPE,
            "plan_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(FINAL_GATE_RERUN_PLAN_REQUIRED_FIELDS),
        },
        "reexecution_readiness_plan_schema": {
            "plan_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_PLAN_TYPE,
            "plan_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(REEXECUTION_READINESS_PLAN_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_resolution_packet_input_shape": True,
            "validate_resolution_packet_artifact_shape": True,
            "validate_blocker_resolution_checklist_shape": True,
            "validate_operator_action_plan_shape": True,
            "validate_candidate_selection_requirements_shape": True,
            "validate_final_gate_rerun_plan_shape": True,
            "validate_reexecution_readiness_plan_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_blocked_hashes_match_when_present": True,
            "validate_runtime_config_changed_is_false_for_blocked_execution": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_operator_signoff_required_but_not_created": True,
            "validate_candidate_selection_required_but_not_created": True,
            "validate_final_gate_rerun_required_but_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_review_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_runtime_config": True,
        },
        "provenance_requirements": {
            "bp64_review_packet_path_required": True,
            "bp62_execution_path_required": True,
            "bp61_final_gate_path_required": True,
            "bp60_staging_path_required": True,
            "bp59_application_plan_path_required": True,
            "bp58_human_approval_gate_path_required": True,
            "bp57_dry_run_review_packet_path_required": True,
            "bp56_dry_run_execution_report_path_required": True,
            "bp55_change_request_path_required": True,
            "runtime_config_hashes_preserved_when_available": True,
            "model_asset_hash_required": True,
            "non_claims_preserved": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    _write_json_if_requested(output_path, contract)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": contract["contract_type"],
        "contract_version": contract["contract_version"],
        "contract": contract,
        "contract_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    source_application_execution_review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    source_application_execution_review_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    review_packet = _load_json(source_application_execution_review_packet_path)
    outcome = _dict(review_packet.get("execution_outcome_summary"))
    blocker_summary = _dict(review_packet.get("blocker_summary"))
    next_action = _dict(review_packet.get("next_action_recommendation"))
    runtime_ref = _dict(review_packet.get("runtime_config_target_ref"))
    artifact_refs = _dict(review_packet.get("source_artifact_refs"))
    rollback_ref = _dict(_dict(review_packet.get("rollback_summary")).get("rollback_package_ref"))
    before = review_packet.get("runtime_config_target_sha256_before") or outcome.get(
        "runtime_config_sha_before"
    )
    after = review_packet.get("runtime_config_target_sha256_after") or outcome.get(
        "runtime_config_sha_after"
    )
    blockers = _resolution_blockers(blocker_summary, review_packet)
    recommendations = _resolution_next_actions(blockers, next_action)
    model_asset_ref = review_packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = review_packet.get("model_asset_sha256") or _sha256_file(
        Path(model_asset_ref)
    )
    inputs = {
        "resolution_packet_input_id": _stable_id(
            "controlled_runtime_calibration_blocked_execution_resolution_packet_inputs_v1",
            review_packet.get("review_packet_id"),
            outcome.get("application_outcome_status"),
            before,
            after,
        ),
        "resolution_packet_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_TYPE
        ),
        "resolution_packet_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_review_packet_path": str(
            Path(source_application_execution_review_packet_path)
        ),
        "source_application_execution_review_packet_contract_path": str(
            Path(source_application_execution_review_packet_contract_path)
        ),
        "source_application_execution_path": review_packet.get(
            "source_application_execution_path"
        ),
        "source_runtime_config_artifact_path": runtime_ref.get("path"),
        "source_rollback_package_path": rollback_ref.get("rollback_package_path"),
        "source_pre_application_final_gate_path": review_packet.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": review_packet.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": review_packet.get("source_application_plan_path"),
        "source_human_approval_gate_path": review_packet.get(
            "source_human_approval_gate_path"
        ),
        "source_dry_run_review_packet_path": review_packet.get(
            "source_dry_run_review_packet_path"
        ),
        "source_dry_run_execution_report_path": review_packet.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": review_packet.get("source_change_request_path"),
        "source_candidate_config_freeze_path": _artifact_path(
            artifact_refs,
            "candidate_config_freeze",
        ),
        "source_manual_approval_packet_path": _artifact_path(
            artifact_refs,
            "manual_approval_packet",
        ),
        "source_decision_packet_path": _artifact_path(artifact_refs, "decision_packet"),
        "source_phase_freeze_path": _artifact_path(artifact_refs, "phase_freeze"),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_ref,
        "runtime_config_target_sha256_before": before,
        "runtime_config_target_sha256_after": after,
        "application_execution_status": review_packet.get("application_execution_status"),
        "application_outcome_status": outcome.get("application_outcome_status"),
        "runtime_application_status": review_packet.get("runtime_application_status"),
        "runtime_config_status": review_packet.get("runtime_config_status"),
        "mutation_status": review_packet.get("mutation_status"),
        "production_config_status": review_packet.get("production_config_status"),
        "baseline_update_status": review_packet.get("baseline_update_status"),
        "model_update_status": review_packet.get("model_update_status"),
        "blocker_types": blockers,
        "next_action_recommendation": recommendations,
        "selected_candidate_config_ref": _dict(
            review_packet.get("selected_candidate_config_ref")
        ),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_packet_status": review_packet.get("review_packet_status"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": {
            "application_execution_review_packet": _artifact_ref(
                source_application_execution_review_packet_path,
                review_packet,
            ),
            "application_execution_review_packet_contract": _artifact_ref(
                source_application_execution_review_packet_contract_path,
                _load_json_if_exists(
                    source_application_execution_review_packet_contract_path
                ),
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_resolution_packet_inputs",
        "resolution_packet_input_id": inputs["resolution_packet_input_id"],
        "application_outcome_status": inputs["application_outcome_status"],
        "runtime_config_changed": _runtime_config_changed(inputs),
        "mutation_status": inputs["mutation_status"],
        "blocker_count": len(blockers),
        "next_action_recommendation": recommendations,
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_blocked_execution_resolution_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(resolution_packet_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_blocked_execution_resolution_packet_inputs_validation"
        ),
        payload_path=resolution_packet_inputs_path,
        payload_type=inputs.get("resolution_packet_input_type"),
        payload_version=inputs.get("resolution_packet_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_blocked_execution_resolution_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(resolution_packet_inputs_path)
    statuses = _resolution_statuses(inputs)
    packet_id = _stable_id(
        "controlled_runtime_calibration_blocked_execution_resolution_packet_v1",
        inputs.get("resolution_packet_input_id"),
        inputs.get("application_outcome_status"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    packet = {
        "resolution_packet_id": packet_id,
        "resolution_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_TYPE
        ),
        "resolution_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_input_path": str(Path(resolution_packet_inputs_path)),
        "source_application_execution_review_packet_path": inputs.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": inputs.get(
            "source_application_execution_path"
        ),
        "source_pre_application_final_gate_path": inputs.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": inputs.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": inputs.get("source_application_plan_path"),
        "source_human_approval_gate_path": inputs.get(
            "source_human_approval_gate_path"
        ),
        "source_dry_run_review_packet_path": inputs.get(
            "source_dry_run_review_packet_path"
        ),
        "source_dry_run_execution_report_path": inputs.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "selected_candidate_config_ref": _dict(
            inputs.get("selected_candidate_config_ref")
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": _runtime_config_changed(inputs),
        "application_execution_status": inputs.get("application_execution_status"),
        "application_outcome_status": inputs.get("application_outcome_status"),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_status": inputs.get("runtime_config_status"),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        **statuses,
        "blocker_resolution_checklist": _blocker_resolution_checklist(
            packet_id,
            inputs,
            generated_at,
        ),
        "operator_action_plan": _operator_action_plan(packet_id, inputs, generated_at),
        "candidate_selection_requirements": _candidate_selection_requirements(
            packet_id,
            inputs,
            generated_at,
        ),
        "final_gate_rerun_plan": _final_gate_rerun_plan(
            packet_id,
            inputs,
            generated_at,
        ),
        "reexecution_readiness_plan": _reexecution_readiness_plan(
            packet_id,
            inputs,
            generated_at,
        ),
        "next_action_recommendation": _list(inputs.get("next_action_recommendation")),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_inputs_shape(inputs))
    errors.extend(_validate_resolution_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_resolution_packet",
        "resolution_packet_id": packet["resolution_packet_id"],
        "resolution_packet_status": packet["resolution_packet_status"],
        "application_outcome_status": packet["application_outcome_status"],
        "runtime_config_changed": packet["runtime_config_changed"],
        "mutation_status": packet["mutation_status"],
        "blocker_resolution_status": packet["blocker_resolution_status"],
        "operator_action_status": packet["operator_action_status"],
        "candidate_selection_status": packet["candidate_selection_status"],
        "final_gate_rerun_status": packet["final_gate_rerun_status"],
        "reexecution_readiness_status": packet["reexecution_readiness_status"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "resolution_packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_blocked_execution_resolution_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_blocked_execution_resolution_packet_validation"
        ),
        payload_path=resolution_packet_path,
        payload_type=packet.get("resolution_packet_type"),
        payload_version=packet.get("resolution_packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_blocker_resolution_checklist(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    checklist = _dict(packet.get("blocker_resolution_checklist"))
    report = {
        "checklist_report_id": _stable_id(
            "controlled_runtime_calibration_blocker_resolution_checklist_report_v1",
            packet.get("resolution_packet_id"),
        ),
        "checklist_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_TYPE
        ),
        "checklist_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet.get("resolution_packet_id"),
        "source_resolution_packet_path": str(Path(resolution_packet_path)),
        "blocker_resolution_checklist": checklist,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_blocker_resolution_checklist",
        "checklist_report_id": report["checklist_report_id"],
        "check_count": len(BLOCKER_RESOLUTION_CHECKLIST_ITEMS),
        "checklist_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_operator_action_plan(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ACTION_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    plan = {
        **_dict(packet.get("operator_action_plan")),
        "exported_at": generated_at.isoformat(),
        "source_resolution_packet_path": str(Path(resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    errors.extend(_validate_operator_action_plan_shape(plan))
    _write_json_if_requested(output_path, plan)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_action_plan",
        "operator_action_plan_id": plan.get("operator_action_plan_id"),
        "operator_action_status": plan.get("operator_action_status"),
        "operator_action_plan_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_candidate_selection_requirements(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_REQUIREMENTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    requirements = {
        **_dict(packet.get("candidate_selection_requirements")),
        "exported_at": generated_at.isoformat(),
        "source_resolution_packet_path": str(Path(resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    errors.extend(_validate_candidate_selection_requirements_shape(requirements))
    _write_json_if_requested(output_path, requirements)
    return {
        "ok": not errors,
        "status": (
            "completed" if not errors else "invalid_candidate_selection_requirements"
        ),
        "candidate_selection_requirements_id": requirements.get(
            "candidate_selection_requirements_id"
        ),
        "candidate_selection_status": requirements.get("candidate_selection_status"),
        "candidate_selection_requirements_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_final_gate_rerun_plan(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    plan = {
        **_dict(packet.get("final_gate_rerun_plan")),
        "exported_at": generated_at.isoformat(),
        "source_resolution_packet_path": str(Path(resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    errors.extend(_validate_final_gate_rerun_plan_shape(plan))
    _write_json_if_requested(output_path, plan)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_final_gate_rerun_plan",
        "final_gate_rerun_plan_id": plan.get("final_gate_rerun_plan_id"),
        "final_gate_rerun_status": plan.get("final_gate_rerun_status"),
        "final_gate_rerun_plan_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_reexecution_readiness_plan(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(resolution_packet_path)
    plan = {
        **_dict(packet.get("reexecution_readiness_plan")),
        "exported_at": generated_at.isoformat(),
        "source_resolution_packet_path": str(Path(resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_resolution_packet_shape(packet))
    errors.extend(_validate_reexecution_readiness_plan_shape(plan))
    _write_json_if_requested(output_path, plan)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_readiness_plan",
        "reexecution_readiness_plan_id": plan.get("reexecution_readiness_plan_id"),
        "reexecution_readiness_status": plan.get("reexecution_readiness_status"),
        "reexecution_readiness_plan_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _resolution_statuses(inputs: dict[str, Any]) -> dict[str, str]:
    if inputs.get("application_outcome_status") == (
        "application_blocked_safely_before_runtime_mutation"
    ):
        return {
            "resolution_packet_status": (
                "resolution_packet_created_for_blocked_execution"
            ),
            "blocker_resolution_status": "blockers_identified_resolution_required",
            "operator_action_status": "operator_signoff_required",
            "candidate_selection_status": "selected_candidate_required",
            "final_gate_rerun_status": "final_gate_rerun_required",
            "reexecution_readiness_status": (
                "reexecution_not_ready_blockers_unresolved"
            ),
        }
    return {
        "resolution_packet_status": "resolution_packet_informational_only",
        "blocker_resolution_status": "blocker_resolution_not_applicable",
        "operator_action_status": "operator_action_not_applicable",
        "candidate_selection_status": "candidate_selection_not_applicable",
        "final_gate_rerun_status": "final_gate_rerun_not_applicable",
        "reexecution_readiness_status": "reexecution_not_applicable",
    }


def _blocker_resolution_checklist(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    checklist = {
        "checklist_id": _stable_id(
            "controlled_runtime_calibration_blocker_resolution_checklist_v1",
            packet_id,
        ),
        "checklist_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKER_RESOLUTION_CHECKLIST_TYPE,
        "checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet_id,
        "blocker_types": _list(inputs.get("blocker_types")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    for item in BLOCKER_RESOLUTION_CHECKLIST_ITEMS:
        checklist[item] = {
            "required": True,
            "status": _check_status(item, inputs),
        }
    return checklist


def _operator_action_plan(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "operator_action_plan_id": _stable_id(
            "controlled_runtime_calibration_operator_action_plan_v1",
            packet_id,
        ),
        "operator_action_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet_id,
        "required_operator_artifacts": {
            "operator_signoff_ref": {
                "required": True,
                "status": "operator_signoff_required",
                "created_by_blueprint_65": False,
            },
            "selected_candidate_config_ref": {
                "required": True,
                "status": "selected_candidate_required",
                "created_by_blueprint_65": False,
            },
            "final_gate_rerun_request_ref": {
                "required": True,
                "status": "final_gate_rerun_required",
                "created_by_blueprint_65": False,
            },
            "reexecution_request_ref_for_future_blueprint": {
                "required": True,
                "status": "reexecution_not_ready_blockers_unresolved",
                "created_by_blueprint_65": False,
            },
        },
        "required_operator_decisions": [
            "provide real operator signoff artifact before any future application attempt",
            "provide selected candidate config artifact before final gate rerun",
            "request final gate rerun only after required artifacts exist",
            "request application execution only after final gate allows it",
        ],
        "operator_review_checklist": [
            "review BP64 packet and BP62 execution status",
            "verify runtime config target hashes match",
            "verify model asset hash remains unchanged",
            "verify baselines remain unchanged",
            "verify no production config exists",
        ],
        "operator_action_status": "operator_signoff_required",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_selection_requirements(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "candidate_selection_requirements_id": _stable_id(
            "controlled_runtime_calibration_candidate_selection_requirements_v1",
            packet_id,
        ),
        "candidate_selection_requirements_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet_id,
        "required_candidate_refs": {
            "selected_candidate_config_ref": {
                "required": True,
                "current_value": _dict(inputs.get("selected_candidate_config_ref")),
                "status": "selected_candidate_required",
            },
            "source_candidate_config_freeze_path": {
                "required": True,
                "path": inputs.get("source_candidate_config_freeze_path"),
            },
        },
        "candidate_selection_constraints": [
            (
                "candidate must reference an existing frozen candidate config "
                "or explicit controlled candidate artifact"
            ),
            "candidate must not be inferred from model output",
            "candidate must not be invented by Codex",
            "candidate must preserve source path, candidate id, version, and provenance",
            "candidate must be reviewed by human operator before final gate rerun",
        ],
        "candidate_selection_status": "selected_candidate_required",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_rerun_plan(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "final_gate_rerun_plan_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_plan_v1",
            packet_id,
        ),
        "final_gate_rerun_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet_id,
        "required_inputs": {
            "operator_signoff_ref": "required_external_artifact",
            "selected_candidate_config_ref": "required_external_artifact",
            "source_pre_application_final_gate_path": inputs.get(
                "source_pre_application_final_gate_path"
            ),
            "source_runtime_application_staging_path": inputs.get(
                "source_runtime_application_staging_path"
            ),
            "source_application_plan_path": inputs.get("source_application_plan_path"),
        },
        "required_preconditions": [
            "operator signoff artifact exists",
            "selected candidate artifact exists",
            "runtime config target hash still matches blocked execution hash",
            "model asset hash still matches recorded hash",
            "protected baselines remain unchanged",
        ],
        "required_regression_gates": _required_regression_gates(),
        "final_gate_rerun_status": "final_gate_rerun_required",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_readiness_plan(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "reexecution_readiness_plan_id": _stable_id(
            "controlled_runtime_calibration_reexecution_readiness_plan_v1",
            packet_id,
        ),
        "reexecution_readiness_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_resolution_packet_id": packet_id,
        "required_inputs": {
            "final_gate_rerun_result": "required_future_artifact",
            "operator_signoff_ref": "required_external_artifact",
            "selected_candidate_config_ref": "required_external_artifact",
            "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        },
        "required_preconditions": [
            "final gate permits future application execution",
            "runtime config target remains unchanged until reexecution",
            "rollback package exists",
            "post execution review packet path is prepared",
            "no model asset mutation is present",
            "no baseline replacement is present",
            "no production config is present",
        ],
        "required_regression_gates": _required_regression_gates(),
        "required_rollback_artifacts": {
            "rollback_package_ref": inputs.get("source_rollback_package_path"),
            "rollback_ready_before_reexecution": True,
        },
        "required_post_execution_review": {
            "post_execution_review_packet_required": True,
            "operator_review_required": True,
        },
        "reexecution_readiness_status": "reexecution_not_ready_blockers_unresolved",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _resolution_blockers(
    blocker_summary: dict[str, Any],
    review_packet: dict[str, Any],
) -> list[str]:
    blockers = _unique_strings(_list(blocker_summary.get("blocker_types")))
    if blocker_summary.get("operator_signoff_missing") is True:
        blockers.append("missing_operator_signoff")
    if blocker_summary.get("selected_candidate_missing") is True:
        blockers.append("no_selected_candidate")
    if blocker_summary.get("final_gate_not_passed") is True:
        blockers.append("final_gate_not_passed")
    if review_packet.get("application_execution_status") == (
        "application_blocked_final_gate_not_passed"
    ):
        blockers.append("application_blocked_final_gate_not_passed")
    return _unique_strings(blockers)


def _resolution_next_actions(
    blockers: list[str],
    bp64_next_action: dict[str, Any],
) -> list[str]:
    recommendations = _unique_strings([bp64_next_action.get("recommendation")])
    if _contains_any(blockers, ["operator_signoff"]):
        recommendations.append("resolve_operator_signoff_before_reapplying")
    if _contains_any(blockers, ["candidate"]):
        recommendations.append("select_candidate_before_reapplying")
    if _contains_any(blockers, ["final_gate"]):
        recommendations.append("rerun_final_gate_after_resolution")
    if not recommendations:
        recommendations.append("no_runtime_action_recommended")
    return _unique_strings(recommendations)


def _check_status(item: str, inputs: dict[str, Any]) -> str:
    if item in {
        "confirm_application_blocked_safely",
        "confirm_runtime_config_unchanged",
        "confirm_no_runtime_mutation",
        "confirm_model_weights_not_modified",
        "confirm_baselines_not_replaced",
    }:
        return "confirmed_from_bp64_review_packet"
    if item.startswith("identify_") or item.startswith("require_"):
        return "required_for_future_resolution"
    return "inspection_required"


def _required_regression_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate": "multi_point_regression_matrix",
            "required": True,
            "expected_drift_detected": False,
        },
        {
            "gate": "protected_sample_point_reviewed_3d_debug",
            "required": True,
            "expected_drift_detected": False,
        },
        {
            "gate": "gameplay_gate_regression_baseline",
            "required": True,
            "expected_drift_detected": False,
        },
        {
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "required": True,
            "expected_drift_detected": False,
        },
    ]


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "resolution_packet_scope",
        "source_contract_refs",
        "resolution_packet_input_schema",
        "resolution_packet_schema",
        "blocker_resolution_checklist_schema",
        "operator_action_plan_schema",
        "candidate_selection_requirements_schema",
        "final_gate_rerun_plan_schema",
        "reexecution_readiness_plan_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors.extend(_missing_required(contract, required, "contract"))
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_resolution_packet_inputs_shape(
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        inputs,
        RESOLUTION_PACKET_INPUT_REQUIRED_FIELDS,
        "resolution_packet_inputs",
    )
    errors.extend(_validate_blocked_statuses(inputs))
    errors.extend(_validate_next_actions(_list(inputs.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_resolution_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, RESOLUTION_PACKET_REQUIRED_FIELDS, "resolution_packet")
    errors.extend(
        _validate_status(
            "resolution_packet_status",
            packet.get("resolution_packet_status"),
            ALLOWED_RESOLUTION_PACKET_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "blocker_resolution_status",
            packet.get("blocker_resolution_status"),
            ALLOWED_BLOCKER_RESOLUTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_action_status",
            packet.get("operator_action_status"),
            ALLOWED_OPERATOR_ACTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "candidate_selection_status",
            packet.get("candidate_selection_status"),
            ALLOWED_CANDIDATE_SELECTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            packet.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            packet.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(_validate_blocked_statuses(packet))
    errors.extend(_validate_next_actions(_list(packet.get("next_action_recommendation"))))
    errors.extend(_validate_checklist_shape(_dict(packet.get("blocker_resolution_checklist"))))
    errors.extend(_validate_operator_action_plan_shape(_dict(packet.get("operator_action_plan"))))
    errors.extend(
        _validate_candidate_selection_requirements_shape(
            _dict(packet.get("candidate_selection_requirements"))
        )
    )
    errors.extend(_validate_final_gate_rerun_plan_shape(_dict(packet.get("final_gate_rerun_plan"))))
    errors.extend(
        _validate_reexecution_readiness_plan_shape(
            _dict(packet.get("reexecution_readiness_plan"))
        )
    )
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_blocked_statuses(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if payload.get("model_update_status") != "not_modified":
        errors.append(
            _error(
                "model_update_status_must_remain_not_modified",
                "model_update_status",
                payload.get("model_update_status"),
            )
        )
    if payload.get("production_config_status") != "not_created":
        errors.append(
            _error(
                "production_config_status_must_remain_not_created",
                "production_config_status",
                payload.get("production_config_status"),
            )
        )
    if payload.get("baseline_update_status") != "not_replaced":
        errors.append(
            _error(
                "baseline_update_status_must_remain_not_replaced",
                "baseline_update_status",
                payload.get("baseline_update_status"),
            )
        )
    if payload.get("application_outcome_status") != (
        "application_blocked_safely_before_runtime_mutation"
    ):
        return errors
    if payload.get("runtime_application_status") != "blocked_from_runtime_application":
        errors.append(
            _error(
                "blocked_execution_runtime_application_status_invalid",
                "runtime_application_status",
                payload.get("runtime_application_status"),
            )
        )
    if payload.get("runtime_config_status") != "unchanged_due_to_blocker":
        errors.append(
            _error(
                "blocked_execution_runtime_config_status_invalid",
                "runtime_config_status",
                payload.get("runtime_config_status"),
            )
        )
    if payload.get("mutation_status") != "no_runtime_mutation_due_to_blocker":
        errors.append(
            _error(
                "blocked_execution_mutation_status_invalid",
                "mutation_status",
                payload.get("mutation_status"),
            )
        )
    if _runtime_config_changed(payload):
        errors.append(
            _error(
                "blocked_execution_runtime_config_changed",
                "runtime_config_changed",
                True,
            )
        )
    if payload.get("runtime_config_changed") is True:
        errors.append(
            _error(
                "blocked_execution_runtime_config_changed_flag",
                "runtime_config_changed",
                payload.get("runtime_config_changed"),
            )
        )
    return errors


def _validate_checklist_shape(checklist: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "checklist_id",
        "checklist_type",
        "checklist_version",
        "generated_at",
        "source_resolution_packet_id",
        "blocker_types",
        "warnings",
        "non_claims",
        *BLOCKER_RESOLUTION_CHECKLIST_ITEMS,
    ]
    return _missing_required(checklist, required, "blocker_resolution_checklist")


def _validate_operator_action_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(plan, OPERATOR_ACTION_PLAN_REQUIRED_FIELDS, "operator_action_plan")
    errors.extend(
        _validate_status(
            "operator_action_status",
            plan.get("operator_action_status"),
            ALLOWED_OPERATOR_ACTION_STATUSES,
        )
    )
    return errors


def _validate_candidate_selection_requirements_shape(
    requirements: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        requirements,
        CANDIDATE_SELECTION_REQUIREMENTS_REQUIRED_FIELDS,
        "candidate_selection_requirements",
    )
    errors.extend(
        _validate_status(
            "candidate_selection_status",
            requirements.get("candidate_selection_status"),
            ALLOWED_CANDIDATE_SELECTION_STATUSES,
        )
    )
    return errors


def _validate_final_gate_rerun_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(plan, FINAL_GATE_RERUN_PLAN_REQUIRED_FIELDS, "final_gate_rerun_plan")
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            plan.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    return errors


def _validate_reexecution_readiness_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        plan,
        REEXECUTION_READINESS_PLAN_REQUIRED_FIELDS,
        "reexecution_readiness_plan",
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            plan.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    return errors


def _validate_next_actions(recommendations: list[str]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for index, recommendation in enumerate(recommendations):
        errors.extend(
            _validate_status(
                f"next_action_recommendation[{index}]",
                recommendation,
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS,
            )
        )
    return errors


def _validate_non_claims(non_claims: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(
                _error("missing_non_claim", f"non_claims.{key}", non_claims.get(key))
            )
    return errors


def _validate_status(field: str, value: Any, allowed: list[str]) -> list[dict[str, Any]]:
    if value in allowed:
        return []
    return [_error("invalid_status", field, value)]


def _validate_no_forbidden_tokens(payload: Any, path: str = "$") -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_RESOLUTION_PACKET_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_RESOLUTION_PACKET_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "resolution_packet_status",
        "application_execution_status",
        "application_outcome_status",
        "runtime_application_status",
        "runtime_config_status",
        "mutation_status",
        "production_config_status",
        "baseline_update_status",
        "model_update_status",
        "blocker_resolution_status",
        "operator_action_status",
        "candidate_selection_status",
        "final_gate_rerun_status",
        "reexecution_readiness_status",
    ]
    return {key: payload.get(key) for key in keys if key in payload}


def _runtime_config_changed(payload: dict[str, Any]) -> bool:
    before = payload.get("runtime_config_target_sha256_before")
    after = payload.get("runtime_config_target_sha256_after")
    return bool(before and after and before != after)


def _contains_any(values: list[str], needles: list[str]) -> bool:
    return any(any(needle in value for needle in needles) for value in values)


def _artifact_path(artifact_refs: dict[str, Any], key: str) -> str | None:
    return _dict(artifact_refs.get(key)).get("path")


def _artifact_ref(path: str | Path | None, payload: dict[str, Any]) -> dict[str, Any]:
    if path is None:
        return {"path": None, "exists": False}
    return {
        "path": str(Path(path)),
        "exists": Path(path).exists(),
        "artifact_type": (
            payload.get("review_packet_type")
            or payload.get("contract_type")
            or payload.get("resolution_packet_type")
        ),
        "artifact_version": (
            payload.get("review_packet_version")
            or payload.get("contract_version")
            or payload.get("resolution_packet_version")
        ),
    }


def _missing_required(
    payload: dict[str, Any],
    required_fields: list[str],
    context: str,
) -> list[dict[str, Any]]:
    return [
        _error("missing_required_field", f"{context}.{field}", None)
        for field in required_fields
        if field not in payload
    ]


def _validation_result(
    *,
    validation_type: str,
    payload_path: str | Path,
    payload_type: Any,
    payload_version: Any,
    contract_path: str | Path,
    validated_at: datetime,
    errors: list[dict[str, Any]],
    status_fields: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": validation_type,
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "contract_path": str(Path(contract_path)),
        "error_count": len(errors),
        "errors": errors,
        **status_fields,
        "warnings": dict(WARNINGS),
    }


def _error(code: str, field: str, value: Any) -> dict[str, Any]:
    return {"code": code, "field": field, "value": value}


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _load_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    json_path = Path(path)
    if not json_path.exists():
        return {}
    return _load_json(json_path)


def _write_json_if_requested(path: str | Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _path_string(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value is None:
            continue
        text = str(value)
        if text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_BLUEPRINT_NAME
        ),
    }
