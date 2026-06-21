from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_operator_signoff_candidate_selection_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_TYPE = (
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_VERSION = (
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_TYPE = (
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_VERSION = (
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_TYPE = (
    "controlled_runtime_calibration_explicit_operator_signoff_artifact"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_REPORT_TYPE = (
    "controlled_runtime_calibration_operator_signoff_requirements_report"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ATTESTATION_TEMPLATE_TYPE = (
    "controlled_runtime_calibration_operator_attestation_template"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_operator_signoff_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_BLUEPRINT = "blueprint_67"
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_explicit_operator_signoff_artifact.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_operator_signoff_requirements_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ATTESTATION_TEMPLATE_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_operator_attestation_template.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_operator_signoff_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

OPERATOR_ATTESTATION_TEXT_TEMPLATE = (
    "I explicitly acknowledge that this operator signoff is only a review/control "
    "artifact. It does not execute runtime application, does not select a candidate "
    "unless a candidate ref is explicitly supplied separately, does not create "
    "production config, does not modify model weights, does not replace baselines, "
    "and does not assert tennis truth."
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_blocked_execution_resolution_packet_contract_version": "v1",
    "controlled_runtime_calibration_application_execution_review_packet_contract_version": "v1",  # noqa: E501
    "controlled_runtime_calibration_application_execution_contract_version": "v1",
    "controlled_runtime_calibration_pre_application_final_gate_contract_version": "v1",
    "controlled_runtime_calibration_runtime_application_staging_contract_version": "v1",
    "controlled_runtime_calibration_application_plan_contract_version": "v1",
    "controlled_runtime_calibration_human_approval_gate_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_review_packet_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_execution_contract_version": "v1",
    "controlled_runtime_calibration_change_request_contract_version": "v1",
    "calibration_candidate_config_freeze_contract_version": "v1",
    "calibration_candidate_decision_packet_contract_version": "v1",
    "real_broadcast_gameplay_calibration_decision_phase_freeze_version": "v1",
    "review_guided_gameplay_calibration_sandbox_regression_contract_version": "v1",
    "review_guided_gameplay_calibration_evaluation_sandbox_contract_version": "v1",
    "review_guided_gameplay_calibration_proposal_contract_version": "v1",
    "real_broadcast_gameplay_review_metrics_contract_version": "v1",
    "real_broadcast_gameplay_review_loop_contract_version": "v1",
    "real_broadcast_gameplay_corpus_run_contract_version": "v1",
    "gameplay_gate_review_dataset_export_contract_version": "v1",
    "gameplay_gate_pathway_completion_freeze_version": "v1",
    "gameplay_gate_regression_baseline_contract_version": "v1",
    "gameplay_segment_gate_contract_version": "v1",
    "tom_v3_expansion_completion_freeze_version": "v1",
    "multi_point_regression_matrix_version": "v0",
    "point_manifest_version": "v0",
}

ALLOWED_SIGNOFF_ARTIFACT_STATUSES = [
    "signoff_artifact_created_pending_explicit_operator_input",
    "signoff_artifact_created_with_explicit_operator_signoff",
    "signoff_artifact_created_with_warnings",
    "signoff_artifact_blocked_missing_bp66_packet",
    "signoff_artifact_blocked_invalid_operator_signoff",
    "signoff_artifact_blocked_missing_required_attestation",
    "signoff_artifact_informational_only",
    "not_applicable",
]
ALLOWED_OPERATOR_SIGNOFF_STATUSES = [
    "operator_signoff_required",
    "operator_signoff_pending",
    "operator_signoff_explicitly_recorded",
    "operator_signoff_invalid",
    "operator_signoff_blocked",
    "operator_signoff_not_applicable",
    "not_applicable",
]
ALLOWED_OPERATOR_ATTESTATION_STATUSES = [
    "operator_attestation_required",
    "operator_attestation_pending",
    "operator_attestation_explicitly_recorded",
    "operator_attestation_invalid",
    "operator_attestation_blocked",
    "not_applicable",
]
ALLOWED_OPERATOR_IDENTITY_STATUSES = [
    "operator_identity_required",
    "operator_identity_pending",
    "operator_identity_explicitly_recorded",
    "operator_identity_invalid",
    "operator_identity_blocked",
    "not_applicable",
]
ALLOWED_OPERATOR_TIMESTAMP_STATUSES = [
    "operator_timestamp_required",
    "operator_timestamp_pending",
    "operator_timestamp_explicitly_recorded",
    "operator_timestamp_invalid",
    "operator_timestamp_blocked",
    "not_applicable",
]
ALLOWED_SELECTED_CANDIDATE_STATUSES = [
    "selected_candidate_required",
    "selected_candidate_pending",
    "selected_candidate_explicitly_recorded",
    "selected_candidate_invalid",
    "selected_candidate_blocked",
    "selected_candidate_not_applicable",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_STATUSES = [
    "final_gate_rerun_required",
    "final_gate_rerun_ready_after_signoff_and_candidate_selection",
    "final_gate_rerun_blocked_missing_operator_signoff",
    "final_gate_rerun_blocked_missing_selected_candidate",
    "final_gate_rerun_not_executed",
    "not_applicable",
]
ALLOWED_REEXECUTION_READINESS_STATUSES = [
    "reexecution_not_ready_blockers_unresolved",
    "reexecution_ready_after_final_gate_rerun",
    "reexecution_blocked_missing_operator_signoff",
    "reexecution_blocked_missing_selected_candidate",
    "reexecution_blocked_final_gate_not_rerun",
    "reexecution_not_executed",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "not_executed",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "provide_explicit_operator_signoff",
    "provide_operator_identity_and_attestation",
    "provide_selected_candidate",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_signoff_and_candidate_selection",
    "prepare_selected_candidate_artifact_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

SIGNOFF_INPUT_REQUIRED_FIELDS = [
    "signoff_input_id",
    "signoff_input_type",
    "signoff_input_version",
    "generated_at",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_change_request_path",
    "candidate_option_refs",
    "explicit_operator_signoff_ref",
    "explicit_operator_identity_ref",
    "explicit_operator_signoff_timestamp",
    "explicit_operator_attestation_text",
    "explicit_operator_scope_acknowledgement",
    "operator_notes_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "runtime_application_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "selected_candidate_config_ref",
    "selected_candidate_status",
    "source_bp66_packet_id",
    "source_resolution_packet_id",
    "source_contract_refs",
    "warnings",
    "non_claims",
]
SIGNOFF_ARTIFACT_REQUIRED_FIELDS = [
    "signoff_artifact_id",
    "signoff_artifact_type",
    "signoff_artifact_version",
    "generated_at",
    "source_signoff_input_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "candidate_option_refs",
    "selected_candidate_config_ref",
    "operator_signoff_ref",
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_attestation_text",
    "operator_scope_acknowledgement",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "selected_candidate_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_config_changed",
    "mutation_status",
    "runtime_application_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "signoff_artifact_status",
    "signoff_requirements",
    "signoff_readiness",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]
SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS = [
    "signoff_requirements_id",
    "signoff_requirements_version",
    "generated_at",
    "source_signoff_artifact_id",
    "requirements",
    "operator_signoff_status",
    "warnings",
    "non_claims",
]
OPERATOR_ATTESTATION_REQUIRED_FIELDS = [
    "operator_attestation_template_id",
    "operator_attestation_template_version",
    "generated_at",
    "source_signoff_artifact_id",
    "attestation_text_template",
    "required_operator_fields",
    "operator_attestation_status",
    "warnings",
    "non_claims",
]
SIGNOFF_READINESS_REQUIRED_FIELDS = [
    "signoff_readiness_id",
    "signoff_readiness_version",
    "generated_at",
    "source_signoff_artifact_id",
    "readiness_checks",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "selected_candidate_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "operator_signoff_artifact_is_not_truth": True,
    "operator_signoff_artifact_is_not_accuracy_scoring": True,
    "operator_signoff_artifact_is_not_model_training": True,
    "operator_signoff_artifact_is_not_runtime_application": True,
    "signoff_artifact_does_not_execute_application": True,
    "signoff_artifact_does_not_rerun_final_gate": True,
    "signoff_artifact_does_not_select_candidate": True,
    "signoff_artifact_does_not_infer_operator_signoff": True,
    "operator_signoff_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
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
    "explicit_operator_signoff_artifact": True,
    "operator_signoff_required": True,
    "operator_signoff_pending": True,
    "operator_attestation_required": True,
    "operator_identity_required": True,
    "operator_timestamp_required": True,
    "selected_candidate_required": True,
    "final_gate_rerun_required": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "signoff_artifact_created_pending_explicit_operator_input": True,
    "operator_signoff_must_be_explicit": True,
    "signoff_artifact_is_not_runtime_application": True,
    "classifier_correctness_not_assessed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    **NON_CLAIMS,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_EXPLICIT_OPERATOR_SIGNOFF_TOKENS = {
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
    _forbidden_token("inferred", "operator", "signoff"),
    _forbidden_token("fake", "candidate", "selection"),
    _forbidden_token("inferred", "candidate", "selection"),
}


def export_controlled_runtime_calibration_explicit_operator_signoff_artifact_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "signoff_artifact_scope": {
            "records_explicit_operator_signoff_artifact_state": True,
            "default_state_remains_pending_without_explicit_operator_input": True,
            "does_not_write_runtime_config": True,
            "does_not_fabricate_operator_signoff": True,
            "does_not_select_candidate": True,
            "does_not_rerun_final_gate": True,
            "does_not_execute_application": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
            "does_not_create_production_config": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "signoff_input_schema": {
            "input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_TYPE
            ),
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_VERSION
            ),
            "required_fields": list(SIGNOFF_INPUT_REQUIRED_FIELDS),
        },
        "signoff_artifact_schema": {
            "artifact_type": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_TYPE
            ),
            "artifact_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
            ),
            "required_fields": list(SIGNOFF_ARTIFACT_REQUIRED_FIELDS),
            "allowed_signoff_artifact_statuses": list(ALLOWED_SIGNOFF_ARTIFACT_STATUSES),
            "allowed_operator_signoff_statuses": list(ALLOWED_OPERATOR_SIGNOFF_STATUSES),
            "allowed_operator_attestation_statuses": list(ALLOWED_OPERATOR_ATTESTATION_STATUSES),
            "allowed_operator_identity_statuses": list(ALLOWED_OPERATOR_IDENTITY_STATUSES),
            "allowed_operator_timestamp_statuses": list(ALLOWED_OPERATOR_TIMESTAMP_STATUSES),
            "allowed_selected_candidate_statuses": list(ALLOWED_SELECTED_CANDIDATE_STATUSES),
            "allowed_final_gate_rerun_statuses": list(ALLOWED_FINAL_GATE_RERUN_STATUSES),
            "allowed_reexecution_readiness_statuses": list(ALLOWED_REEXECUTION_READINESS_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "operator_attestation_schema": {
            "template_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ATTESTATION_TEMPLATE_TYPE,
            "template_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
            ),
            "required_fields": list(OPERATOR_ATTESTATION_REQUIRED_FIELDS),
        },
        "signoff_requirements_schema": {
            "requirements_type": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_REPORT_TYPE
            ),
            "requirements_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
            ),
            "required_fields": list(SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS),
        },
        "signoff_readiness_schema": {
            "readiness_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_READINESS_REPORT_TYPE,
            "readiness_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
            ),
            "required_fields": list(SIGNOFF_READINESS_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_signoff_input_shape": True,
            "validate_signoff_artifact_shape": True,
            "validate_operator_attestation_shape": True,
            "validate_signoff_requirements_shape": True,
            "validate_signoff_readiness_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_pending_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_operator_signoff_requires_explicit_ref_and_required_operator_fields": True,
            "validate_no_operator_signoff_inferred_from_codex_tests_branch_commit_tag": True,
            "validate_selected_candidate_remains_required_without_separate_candidate_ref": True,
            "validate_final_gate_rerun_required_but_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_review_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp66_packet_path_required": True,
            "bp65_resolution_packet_path_required": True,
            "bp64_review_packet_path_required": True,
            "bp62_execution_path_required": True,
            "bp61_final_gate_path_required": True,
            "bp60_staging_path_required": True,
            "bp59_application_plan_path_required": True,
            "bp58_human_approval_gate_path_required": True,
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


def build_controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    source_operator_signoff_candidate_selection_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    source_operator_signoff_candidate_selection_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    explicit_operator_signoff_ref: str | None = None,
    explicit_operator_identity_ref: str | None = None,
    explicit_operator_signoff_timestamp: str | None = None,
    explicit_operator_attestation_text: str | None = None,
    explicit_operator_scope_acknowledgement: str | None = None,
    operator_notes_ref: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    bp66_packet = _load_json(source_operator_signoff_candidate_selection_packet_path)
    explicit_signoff = _explicit_ref(explicit_operator_signoff_ref)
    model_asset_ref = bp66_packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = bp66_packet.get("model_asset_sha256") or _sha256_file(
        Path(model_asset_ref)
    )
    selected_candidate = _dict(bp66_packet.get("selected_candidate_config_ref")) or None
    inputs = {
        "signoff_input_id": _stable_id(
            "controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs_v1",
            bp66_packet.get("packet_id"),
            bp66_packet.get("runtime_config_target_sha256_before"),
            bp66_packet.get("runtime_config_target_sha256_after"),
            explicit_signoff,
            explicit_operator_identity_ref,
            explicit_operator_signoff_timestamp,
        ),
        "signoff_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_TYPE
        ),
        "signoff_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_operator_signoff_candidate_selection_packet_path": str(
            Path(source_operator_signoff_candidate_selection_packet_path)
        ),
        "source_operator_signoff_candidate_selection_packet_contract_path": str(
            Path(source_operator_signoff_candidate_selection_packet_contract_path)
        ),
        "source_blocked_execution_resolution_packet_path": bp66_packet.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": bp66_packet.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": bp66_packet.get(
            "source_application_execution_path"
        ),
        "source_pre_application_final_gate_path": bp66_packet.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": bp66_packet.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": bp66_packet.get("source_application_plan_path"),
        "source_human_approval_gate_path": bp66_packet.get(
            "source_human_approval_gate_path"
        ),
        "source_change_request_path": bp66_packet.get("source_change_request_path"),
        "candidate_option_refs": _list(bp66_packet.get("candidate_option_refs")),
        "explicit_operator_signoff_ref": explicit_signoff,
        "explicit_operator_identity_ref": explicit_operator_identity_ref,
        "explicit_operator_signoff_timestamp": explicit_operator_signoff_timestamp,
        "explicit_operator_attestation_text": explicit_operator_attestation_text,
        "explicit_operator_scope_acknowledgement": explicit_operator_scope_acknowledgement,
        "operator_notes_ref": operator_notes_ref,
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(bp66_packet.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": bp66_packet.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": bp66_packet.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": bool(bp66_packet.get("runtime_config_changed")),
        "mutation_status": bp66_packet.get("mutation_status"),
        "runtime_application_status": bp66_packet.get("runtime_application_status")
        or "not_executed",
        "production_config_status": bp66_packet.get("production_config_status"),
        "baseline_update_status": bp66_packet.get("baseline_update_status"),
        "model_update_status": bp66_packet.get("model_update_status"),
        "selected_candidate_config_ref": selected_candidate,
        "selected_candidate_status": _selected_candidate_status_from_packet(bp66_packet),
        "source_bp66_packet_id": bp66_packet.get("packet_id"),
        "source_resolution_packet_id": bp66_packet.get("source_resolution_packet_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": {
            "operator_signoff_candidate_selection_packet": _artifact_ref(
                source_operator_signoff_candidate_selection_packet_path,
                bp66_packet,
            ),
            "operator_signoff_candidate_selection_packet_contract": _artifact_ref(
                source_operator_signoff_candidate_selection_packet_contract_path,
                _load_json_if_exists(
                    source_operator_signoff_candidate_selection_packet_contract_path
                ),
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_signoff_inputs",
        "signoff_input_id": inputs["signoff_input_id"],
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": inputs["selected_candidate_status"],
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_config_changed": inputs["runtime_config_changed"],
        "mutation_status": inputs["mutation_status"],
        "runtime_application_status": inputs["runtime_application_status"],
        "next_action_recommendation": _next_actions(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(signoff_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_inputs_shape(inputs))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_explicit_operator_signoff_artifact_inputs_validation",
        payload_path=signoff_inputs_path,
        payload_type=inputs.get("signoff_input_type"),
        payload_version=inputs.get("signoff_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_explicit_operator_signoff_artifact(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(signoff_inputs_path)
    artifact_id = _stable_id(
        "controlled_runtime_calibration_explicit_operator_signoff_artifact_v1",
        inputs.get("signoff_input_id"),
        inputs.get("source_bp66_packet_id"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    artifact = {
        "signoff_artifact_id": artifact_id,
        "signoff_artifact_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_TYPE
        ),
        "signoff_artifact_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_signoff_input_path": str(Path(signoff_inputs_path)),
        "source_operator_signoff_candidate_selection_packet_path": inputs.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": inputs.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": inputs.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": inputs.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": inputs.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": inputs.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": inputs.get("source_application_plan_path"),
        "source_human_approval_gate_path": inputs.get("source_human_approval_gate_path"),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "selected_candidate_config_ref": _dict(
            inputs.get("selected_candidate_config_ref")
        )
        or None,
        "operator_signoff_ref": _dict(inputs.get("explicit_operator_signoff_ref")) or None,
        "operator_identity_ref": inputs.get("explicit_operator_identity_ref"),
        "operator_signoff_timestamp": inputs.get("explicit_operator_signoff_timestamp"),
        "operator_attestation_text": inputs.get("explicit_operator_attestation_text"),
        "operator_scope_acknowledgement": inputs.get(
            "explicit_operator_scope_acknowledgement"
        ),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": inputs.get("selected_candidate_status"),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "signoff_artifact_status": _signoff_artifact_status(inputs),
        "signoff_requirements": _signoff_requirements(artifact_id, inputs, generated_at),
        "operator_attestation_template": _operator_attestation_template(
            artifact_id,
            inputs,
            generated_at,
        ),
        "signoff_readiness": _signoff_readiness(artifact_id, inputs, generated_at),
        "next_action_recommendation": _next_actions(inputs),
        "source_bp66_packet_id": inputs.get("source_bp66_packet_id"),
        "source_resolution_packet_id": inputs.get("source_resolution_packet_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_inputs_shape(inputs))
    errors.extend(_validate_signoff_artifact_shape(artifact))
    _write_json_if_requested(output_path, artifact)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_signoff_artifact",
        "signoff_artifact_id": artifact["signoff_artifact_id"],
        "signoff_artifact_status": artifact["signoff_artifact_status"],
        "operator_signoff_status": artifact["operator_signoff_status"],
        "operator_attestation_status": artifact["operator_attestation_status"],
        "operator_identity_status": artifact["operator_identity_status"],
        "operator_timestamp_status": artifact["operator_timestamp_status"],
        "selected_candidate_status": artifact["selected_candidate_status"],
        "final_gate_rerun_status": artifact["final_gate_rerun_status"],
        "reexecution_readiness_status": artifact["reexecution_readiness_status"],
        "runtime_config_changed": artifact["runtime_config_changed"],
        "mutation_status": artifact["mutation_status"],
        "runtime_application_status": artifact["runtime_application_status"],
        "next_action_recommendation": artifact["next_action_recommendation"],
        "signoff_artifact_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_explicit_operator_signoff_artifact(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    artifact = _load_json(signoff_artifact_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_artifact_shape(artifact))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_explicit_operator_signoff_artifact_validation",
        payload_path=signoff_artifact_path,
        payload_type=artifact.get("signoff_artifact_type"),
        payload_version=artifact.get("signoff_artifact_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(artifact),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_operator_signoff_requirements_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    artifact = _load_json(signoff_artifact_path)
    report = {
        **_dict(artifact.get("signoff_requirements")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_REPORT_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_signoff_artifact_path": str(Path(signoff_artifact_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_artifact_shape(artifact))
    errors.extend(_validate_signoff_requirements_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_signoff_requirements_report",
        "signoff_requirements_id": report.get("signoff_requirements_id"),
        "operator_signoff_status": report.get("operator_signoff_status"),
        "signoff_requirements_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_operator_attestation_template(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ATTESTATION_TEMPLATE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    artifact = _load_json(signoff_artifact_path)
    template = {
        **_dict(artifact.get("operator_attestation_template")),
        "template_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_ATTESTATION_TEMPLATE_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_signoff_artifact_path": str(Path(signoff_artifact_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_artifact_shape(artifact))
    errors.extend(_validate_operator_attestation_template_shape(template))
    _write_json_if_requested(output_path, template)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_attestation_template",
        "operator_attestation_template_id": template.get(
            "operator_attestation_template_id"
        ),
        "operator_attestation_status": template.get("operator_attestation_status"),
        "operator_attestation_template_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_operator_signoff_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    signoff_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    artifact = _load_json(signoff_artifact_path)
    report = {
        **_dict(artifact.get("signoff_readiness")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_READINESS_REPORT_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_signoff_artifact_path": str(Path(signoff_artifact_path)),
        "next_action_recommendation": _list(artifact.get("next_action_recommendation")),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_signoff_artifact_shape(artifact))
    errors.extend(_validate_signoff_readiness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_signoff_readiness_report",
        "signoff_readiness_id": report.get("signoff_readiness_id"),
        "operator_signoff_status": report.get("operator_signoff_status"),
        "operator_attestation_status": report.get("operator_attestation_status"),
        "operator_identity_status": report.get("operator_identity_status"),
        "operator_timestamp_status": report.get("operator_timestamp_status"),
        "selected_candidate_status": report.get("selected_candidate_status"),
        "final_gate_rerun_status": report.get("final_gate_rerun_status"),
        "reexecution_readiness_status": report.get("reexecution_readiness_status"),
        "operator_signoff_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _operator_signoff_status(payload: dict[str, Any]) -> str:
    if not _dict(payload.get("explicit_operator_signoff_ref")):
        return "operator_signoff_required"
    if _operator_identity_status(payload) != "operator_identity_explicitly_recorded":
        return "operator_signoff_invalid"
    if _operator_timestamp_status(payload) != "operator_timestamp_explicitly_recorded":
        return "operator_signoff_invalid"
    if _operator_attestation_status(payload) != "operator_attestation_explicitly_recorded":
        return "operator_signoff_invalid"
    return "operator_signoff_explicitly_recorded"


def _operator_attestation_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_attestation_text"):
        return "operator_attestation_required"
    if payload.get("explicit_operator_scope_acknowledgement") != "acknowledged":
        return "operator_attestation_invalid"
    return "operator_attestation_explicitly_recorded"


def _operator_identity_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_identity_ref"):
        return "operator_identity_required"
    return "operator_identity_explicitly_recorded"


def _operator_timestamp_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_signoff_timestamp"):
        return "operator_timestamp_required"
    return "operator_timestamp_explicitly_recorded"


def _selected_candidate_status_from_packet(packet: dict[str, Any]) -> str:
    if packet.get("candidate_selection_status") == "selected_candidate_explicitly_recorded":
        return "selected_candidate_explicitly_recorded"
    return "selected_candidate_required"


def _final_gate_rerun_status(payload: dict[str, Any]) -> str:
    if _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded":
        return "final_gate_rerun_required"
    if payload.get("selected_candidate_status") != "selected_candidate_explicitly_recorded":
        return "final_gate_rerun_required"
    return "final_gate_rerun_ready_after_signoff_and_candidate_selection"


def _reexecution_readiness_status(payload: dict[str, Any]) -> str:
    if _final_gate_rerun_status(payload) == (
        "final_gate_rerun_ready_after_signoff_and_candidate_selection"
    ):
        return "reexecution_blocked_final_gate_not_rerun"
    return "reexecution_not_ready_blockers_unresolved"


def _signoff_artifact_status(payload: dict[str, Any]) -> str:
    signoff_status = _operator_signoff_status(payload)
    if signoff_status == "operator_signoff_invalid":
        return "signoff_artifact_blocked_invalid_operator_signoff"
    if _operator_attestation_status(payload) == "operator_attestation_invalid":
        return "signoff_artifact_blocked_missing_required_attestation"
    if signoff_status == "operator_signoff_explicitly_recorded":
        return "signoff_artifact_created_with_explicit_operator_signoff"
    return "signoff_artifact_created_pending_explicit_operator_input"


def _next_actions(payload: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded":
        actions.append("provide_explicit_operator_signoff")
    if (
        _operator_identity_status(payload) != "operator_identity_explicitly_recorded"
        or _operator_attestation_status(payload)
        != "operator_attestation_explicitly_recorded"
    ):
        actions.append("provide_operator_identity_and_attestation")
    if payload.get("selected_candidate_status") != "selected_candidate_explicitly_recorded":
        actions.append("provide_selected_candidate")
    actions.append("rerun_final_gate_after_signoff_and_candidate_selection")
    return _unique_strings(actions)


def _signoff_requirements(
    artifact_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "signoff_requirements_id": _stable_id(
            "controlled_runtime_calibration_operator_signoff_requirements_v1",
            artifact_id,
        ),
        "signoff_requirements_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_signoff_artifact_id": artifact_id,
        "requirements": {
            "operator_identity_required": {
                "required": True,
                "status": _operator_identity_status(inputs),
            },
            "operator_timestamp_required": {
                "required": True,
                "status": _operator_timestamp_status(inputs),
            },
            "explicit_attestation_text_required": {
                "required": True,
                "status": _operator_attestation_status(inputs),
            },
            "source_bp66_packet_required": {
                "required": True,
                "path": inputs.get(
                    "source_operator_signoff_candidate_selection_packet_path"
                ),
            },
            "source_bp65_resolution_packet_required": {
                "required": True,
                "path": inputs.get("source_blocked_execution_resolution_packet_path"),
            },
            "source_bp64_execution_review_packet_required": {
                "required": True,
                "path": inputs.get("source_application_execution_review_packet_path"),
            },
            "candidate_selection_still_required_before_final_gate_rerun": {
                "required": True,
                "status": inputs.get("selected_candidate_status"),
            },
            "no_runtime_application_performed_by_this_artifact": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_codex_execution": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_successful_tests": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_branch_commit_tag_or_validation_success": {  # noqa: E501
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_be_explicit": {
                "required": True,
                "status": "preserved",
            },
        },
        "operator_signoff_status": _operator_signoff_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _operator_attestation_template(
    artifact_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "operator_attestation_template_id": _stable_id(
            "controlled_runtime_calibration_operator_attestation_template_v1",
            artifact_id,
        ),
        "operator_attestation_template_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_signoff_artifact_id": artifact_id,
        "attestation_text_template": OPERATOR_ATTESTATION_TEXT_TEMPLATE,
        "required_operator_fields": {
            "explicit_operator_signoff_ref": {
                "required": True,
                "provided": bool(_dict(inputs.get("explicit_operator_signoff_ref"))),
            },
            "explicit_operator_identity_ref": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_identity_ref")),
            },
            "explicit_operator_signoff_timestamp": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_signoff_timestamp")),
            },
            "explicit_operator_attestation_text": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_attestation_text")),
            },
            "explicit_operator_scope_acknowledgement": {
                "required": True,
                "provided": inputs.get("explicit_operator_scope_acknowledgement")
                == "acknowledged",
            },
        },
        "operator_attestation_status": _operator_attestation_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _signoff_readiness(
    artifact_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "signoff_readiness_id": _stable_id(
            "controlled_runtime_calibration_operator_signoff_readiness_v1",
            artifact_id,
        ),
        "signoff_readiness_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_signoff_artifact_id": artifact_id,
        "readiness_checks": {
            "operator_signoff_explicitly_recorded": _operator_signoff_status(inputs)
            == "operator_signoff_explicitly_recorded",
            "operator_identity_explicitly_recorded": _operator_identity_status(inputs)
            == "operator_identity_explicitly_recorded",
            "operator_timestamp_explicitly_recorded": _operator_timestamp_status(inputs)
            == "operator_timestamp_explicitly_recorded",
            "operator_attestation_explicitly_recorded": _operator_attestation_status(
                inputs
            )
            == "operator_attestation_explicitly_recorded",
            "selected_candidate_explicitly_recorded": inputs.get(
                "selected_candidate_status"
            )
            == "selected_candidate_explicitly_recorded",
            "final_gate_not_rerun_by_bp67": True,
            "runtime_application_not_executed_by_bp67": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": inputs.get("selected_candidate_status"),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "signoff_artifact_scope",
        "source_contract_refs",
        "signoff_input_schema",
        "signoff_artifact_schema",
        "operator_attestation_schema",
        "signoff_requirements_schema",
        "signoff_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_signoff_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, SIGNOFF_INPUT_REQUIRED_FIELDS, "signoff_inputs")
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_explicit_operator_input(inputs))
    errors.extend(_validate_next_actions(_next_actions(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_signoff_artifact_shape(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        artifact,
        SIGNOFF_ARTIFACT_REQUIRED_FIELDS,
        "signoff_artifact",
    )
    errors.extend(
        _validate_status(
            "signoff_artifact_status",
            artifact.get("signoff_artifact_status"),
            ALLOWED_SIGNOFF_ARTIFACT_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            artifact.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_attestation_status",
            artifact.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_identity_status",
            artifact.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_timestamp_status",
            artifact.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "selected_candidate_status",
            artifact.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            artifact.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            artifact.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_application_status",
            artifact.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        )
    )
    errors.extend(_validate_blocked_runtime_state(artifact))
    errors.extend(_validate_invalid_artifact_statuses(artifact))
    errors.extend(
        _validate_signoff_requirements_shape(_dict(artifact.get("signoff_requirements")))
    )
    errors.extend(
        _validate_operator_attestation_template_shape(
            _dict(artifact.get("operator_attestation_template"))
        )
    )
    errors.extend(_validate_signoff_readiness_shape(_dict(artifact.get("signoff_readiness"))))
    errors.extend(_validate_next_actions(_list(artifact.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(artifact.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(artifact))
    return errors


def _validate_explicit_operator_input(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if _dict(payload.get("explicit_operator_signoff_ref")) and _operator_signoff_status(
        payload
    ) == "operator_signoff_invalid":
        errors.append(
            _error(
                "invalid_explicit_operator_signoff_input",
                "explicit_operator_signoff_ref",
                payload.get("explicit_operator_signoff_ref"),
            )
        )
    return errors


def _validate_invalid_artifact_statuses(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if artifact.get("operator_signoff_status") == "operator_signoff_invalid":
        errors.append(
            _error(
                "invalid_operator_signoff_status",
                "operator_signoff_status",
                artifact.get("operator_signoff_status"),
            )
        )
    if artifact.get("operator_attestation_status") == "operator_attestation_invalid":
        errors.append(
            _error(
                "invalid_operator_attestation_status",
                "operator_attestation_status",
                artifact.get("operator_attestation_status"),
            )
        )
    return errors


def _validate_blocked_runtime_state(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if payload.get("runtime_config_changed") is not False:
        errors.append(
            _error(
                "runtime_config_changed_must_remain_false",
                "runtime_config_changed",
                payload.get("runtime_config_changed"),
            )
        )
    if payload.get("mutation_status") != "no_runtime_mutation_due_to_blocker":
        errors.append(
            _error(
                "mutation_status_must_remain_blocked",
                "mutation_status",
                payload.get("mutation_status"),
            )
        )
    if payload.get("runtime_application_status") not in ALLOWED_RUNTIME_APPLICATION_STATUSES:
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_executed",
                "runtime_application_status",
                payload.get("runtime_application_status"),
            )
        )
    if payload.get("runtime_application_status") == "not_applicable":
        errors.append(
            _error(
                "runtime_application_status_must_be_explicitly_blocked",
                "runtime_application_status",
                payload.get("runtime_application_status"),
            )
        )
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
    before = payload.get("runtime_config_target_sha256_before")
    after = payload.get("runtime_config_target_sha256_after")
    if before and after and before != after:
        errors.append(
            _error(
                "runtime_config_hashes_must_match_for_pending_artifact",
                "runtime_config_target_sha256_after",
                after,
            )
        )
    return errors


def _validate_signoff_requirements_shape(requirements: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        requirements,
        SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS,
        "signoff_requirements",
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            requirements.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    return errors


def _validate_operator_attestation_template_shape(
    template: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        template,
        OPERATOR_ATTESTATION_REQUIRED_FIELDS,
        "operator_attestation_template",
    )
    errors.extend(
        _validate_status(
            "operator_attestation_status",
            template.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        )
    )
    return errors


def _validate_signoff_readiness_shape(readiness: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(readiness, SIGNOFF_READINESS_REQUIRED_FIELDS, "signoff_readiness")
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            readiness.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_attestation_status",
            readiness.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_identity_status",
            readiness.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_timestamp_status",
            readiness.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "selected_candidate_status",
            readiness.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            readiness.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            readiness.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_application_status",
            readiness.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
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
            if key in FORBIDDEN_EXPLICIT_OPERATOR_SIGNOFF_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_EXPLICIT_OPERATOR_SIGNOFF_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "signoff_artifact_status",
        "operator_signoff_status",
        "operator_attestation_status",
        "operator_identity_status",
        "operator_timestamp_status",
        "selected_candidate_status",
        "final_gate_rerun_status",
        "reexecution_readiness_status",
        "runtime_application_status",
        "runtime_config_changed",
        "mutation_status",
        "production_config_status",
        "baseline_update_status",
        "model_update_status",
    ]
    return {key: payload.get(key) for key in keys if key in payload}


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
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_VERSION
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


def _explicit_ref(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, dict):
        return loaded
    return {
        "ref": value,
        "path": value if value.endswith(".json") else None,
        "source": "explicit_cli_argument",
    }


def _artifact_ref(path: str | Path | None, payload: dict[str, Any]) -> dict[str, Any]:
    if path is None:
        return {"path": None, "exists": False}
    return {
        "path": str(Path(path)),
        "exists": Path(path).exists(),
        "artifact_type": _artifact_type(payload),
        "artifact_version": _artifact_version(payload),
    }


def _artifact_type(payload: dict[str, Any]) -> Any:
    for key in [
        "signoff_artifact_type",
        "packet_type",
        "resolution_packet_type",
        "review_packet_type",
        "contract_type",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


def _artifact_version(payload: dict[str, Any]) -> Any:
    for key in [
        "signoff_artifact_version",
        "packet_version",
        "resolution_packet_version",
        "review_packet_version",
        "contract_version",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_BLUEPRINT_NAME
        ),
    }
