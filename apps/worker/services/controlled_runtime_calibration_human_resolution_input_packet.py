from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_explicit_operator_signoff_artifact import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_explicit_selected_candidate_artifact import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_operator_signoff_candidate_selection_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_human_resolution_input_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TYPE = (
    "controlled_runtime_calibration_human_resolution_input_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_TYPE = (
    "controlled_runtime_calibration_human_resolution_input_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_REQUIREMENTS_REPORT_TYPE = (
    "controlled_runtime_calibration_human_resolution_requirements_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TEMPLATE_TYPE = (
    "controlled_runtime_calibration_human_resolution_input_template"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_human_resolution_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_prerequisite_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_BLUEPRINT = "blueprint_69"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_human_resolution_input_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_human_resolution_input_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_input_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_input_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_human_resolution_input_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_input_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_REQUIREMENTS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_requirements_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TEMPLATE_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_input_template.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_READINESS_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_readiness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_prerequisite_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

HUMAN_RESOLUTION_ATTESTATION_TEXT_TEMPLATE = (
    "I explicitly acknowledge that this human resolution packet is only a "
    "review/control artifact. It does not execute runtime application, does not "
    "create production config, does not modify model weights, does not replace "
    "baselines, does not assert tennis truth, and only authorizes the selected "
    "candidate to be carried into a future final-gate rerun."
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_explicit_selected_candidate_artifact_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_explicit_operator_signoff_artifact_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_blocked_execution_resolution_packet_contract_version": "v1",  # noqa: E501
    "controlled_runtime_calibration_application_execution_review_packet_contract_version": "v1",  # noqa: E501
    "controlled_runtime_calibration_application_execution_contract_version": "v1",
    "controlled_runtime_calibration_pre_application_final_gate_contract_version": "v1",
    "controlled_runtime_calibration_runtime_application_staging_contract_version": "v1",  # noqa: E501
    "controlled_runtime_calibration_application_plan_contract_version": "v1",
    "controlled_runtime_calibration_human_approval_gate_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_review_packet_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_execution_contract_version": "v1",
    "controlled_runtime_calibration_change_request_contract_version": "v1",
    "calibration_candidate_config_freeze_contract_version": "v1",
    "calibration_candidate_decision_packet_contract_version": "v1",
    "real_broadcast_gameplay_calibration_decision_phase_freeze_version": "v1",
    "review_guided_gameplay_calibration_sandbox_regression_contract_version": "v1",
    "review_guided_gameplay_calibration_evaluation_sandbox_contract_version": "v1",  # noqa: E501
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

ALLOWED_HUMAN_RESOLUTION_STATUSES = [
    "human_resolution_input_required",
    "human_resolution_input_pending",
    "human_resolution_explicit_inputs_recorded",
    "human_resolution_partially_recorded",
    "human_resolution_invalid",
    "human_resolution_blocked",
    "human_resolution_not_applicable",
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
ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES = [
    "candidate_selection_pending_explicit_input",
    "candidate_selection_valid_explicit_candidate",
    "candidate_selection_invalid_missing_ref",
    "candidate_selection_invalid_unknown_candidate",
    "candidate_selection_invalid_missing_provenance",
    "candidate_selection_invalid_inferred_selection",
    "candidate_selection_blocked",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_STATUSES = [
    "final_gate_rerun_required",
    "final_gate_rerun_ready_after_human_resolution",
    "final_gate_rerun_blocked_missing_operator_signoff",
    "final_gate_rerun_blocked_missing_selected_candidate",
    "final_gate_rerun_blocked_invalid_human_resolution",
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
    "provide_human_resolution_inputs",
    "provide_explicit_operator_signoff",
    "provide_explicit_selected_candidate",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_human_resolution",
    "prepare_final_gate_rerun_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

HUMAN_RESOLUTION_INPUT_REQUIRED_FIELDS = [
    "human_resolution_input_id",
    "human_resolution_input_type",
    "human_resolution_input_version",
    "generated_at",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_selected_candidate_artifact_contract_path",
    "source_explicit_operator_signoff_artifact_path",
    "source_explicit_operator_signoff_artifact_contract_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_operator_signoff_candidate_selection_packet_contract_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_change_request_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_phase_freeze_path",
    "candidate_option_refs",
    "explicit_operator_identity_ref",
    "explicit_operator_signoff_timestamp",
    "explicit_operator_attestation_text",
    "explicit_operator_scope_acknowledgement",
    "explicit_selected_candidate_ref",
    "explicit_selected_candidate_id",
    "explicit_selected_candidate_version",
    "explicit_selected_candidate_source_path",
    "explicit_selected_candidate_selection_reason",
    "explicit_candidate_selection_timestamp",
    "explicit_operator_reference_for_selection",
    "source_bp68_selected_candidate_artifact_status",
    "source_bp67_signoff_artifact_status",
    "source_bp66_candidate_option_count",
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
    "source_bp68_selected_candidate_artifact_id",
    "source_bp67_signoff_artifact_id",
    "source_bp66_packet_id",
    "source_resolution_packet_id",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
HUMAN_RESOLUTION_PACKET_REQUIRED_FIELDS = [
    "human_resolution_packet_id",
    "human_resolution_packet_type",
    "human_resolution_packet_version",
    "generated_at",
    "source_human_resolution_input_path",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_operator_signoff_artifact_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "candidate_option_refs",
    "candidate_option_count",
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_attestation_text",
    "operator_scope_acknowledgement",
    "selected_candidate_config_ref",
    "selected_candidate_id",
    "selected_candidate_version",
    "selected_candidate_source_path",
    "selected_candidate_settings_summary",
    "selected_candidate_provenance",
    "selected_candidate_selection_reason",
    "candidate_selection_timestamp",
    "operator_reference_for_selection",
    "human_resolution_status",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "selected_candidate_status",
    "candidate_selection_validation_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "human_resolution_requirements",
    "human_resolution_readiness",
    "final_gate_rerun_prerequisites",
    "human_resolution_input_template",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]
HUMAN_RESOLUTION_REQUIREMENTS_REQUIRED_FIELDS = [
    "human_resolution_requirements_id",
    "human_resolution_requirements_version",
    "generated_at",
    "source_human_resolution_packet_id",
    "requirements",
    "human_resolution_status",
    "operator_signoff_status",
    "selected_candidate_status",
    "warnings",
    "non_claims",
]
HUMAN_RESOLUTION_INPUT_TEMPLATE_REQUIRED_FIELDS = [
    "human_resolution_input_template_id",
    "human_resolution_input_template_version",
    "generated_at",
    "source_human_resolution_packet_id",
    "template_placeholders",
    "attestation_text_template",
    "required_operator_fields",
    "required_selected_candidate_fields",
    "human_resolution_status",
    "warnings",
    "non_claims",
]
HUMAN_RESOLUTION_READINESS_REQUIRED_FIELDS = [
    "human_resolution_readiness_id",
    "human_resolution_readiness_version",
    "generated_at",
    "source_human_resolution_packet_id",
    "readiness_checks",
    "human_resolution_status",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "selected_candidate_status",
    "candidate_selection_validation_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]
FINAL_GATE_RERUN_PREREQUISITE_REQUIRED_FIELDS = [
    "final_gate_rerun_prerequisite_id",
    "final_gate_rerun_prerequisite_version",
    "generated_at",
    "source_human_resolution_packet_id",
    "prerequisite_checks",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "human_resolution_input_packet_is_not_truth": True,
    "human_resolution_input_packet_is_not_accuracy_scoring": True,
    "human_resolution_input_packet_is_not_model_training": True,
    "human_resolution_input_packet_is_not_runtime_application": True,
    "human_resolution_packet_does_not_execute_application": True,
    "human_resolution_packet_does_not_rerun_final_gate": True,
    "human_resolution_packet_does_not_create_production_config": True,
    "human_resolution_packet_does_not_modify_model_weights": True,
    "human_resolution_packet_does_not_replace_baselines": True,
    "human_resolution_packet_does_not_infer_operator_signoff": True,
    "human_resolution_packet_does_not_infer_candidate_selection": True,
    "human_resolution_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "operator_signoff_must_be_explicit": True,
    "controlled_runtime_config_update_not_performed": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_not_modified": True,
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
    "human_resolution_input_packet": True,
    "human_resolution_input_required": True,
    "operator_signoff_required": True,
    "operator_attestation_required": True,
    "operator_identity_required": True,
    "operator_timestamp_required": True,
    "selected_candidate_required": True,
    "candidate_selection_pending_explicit_input": True,
    "final_gate_rerun_required": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "candidate_option_discovery_is_not_selection": True,
    "human_resolution_must_not_be_inferred": True,
    "runtime_config_unchanged_due_to_blocker": True,
    **NON_CLAIMS,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_HUMAN_RESOLUTION_TOKENS = {
    "in_out",
    "score",
    "winner",
    "point_winner",
    "player_identity",
    "server",
    "receiver",
    "rally_state",
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
    _forbidden_token("selected", "candidate", "inferred", "from", "single", "option"),
    _forbidden_token("fake", "human", "resolution"),
    _forbidden_token("inferred", "human", "resolution"),
}


def export_controlled_runtime_calibration_human_resolution_input_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_EXPORTED_AT
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "human_resolution_input_scope": {
            "records_combined_operator_and_selected_candidate_input_state": True,
            "default_state_remains_pending_without_explicit_human_input": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_select_candidate_from_candidate_options": True,
            "does_not_write_runtime_config": True,
            "does_not_rerun_final_gate": True,
            "does_not_execute_application": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
            "does_not_create_production_config": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "human_resolution_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TYPE,
            "input_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_VERSION,
            "required_fields": list(HUMAN_RESOLUTION_INPUT_REQUIRED_FIELDS),
        },
        "human_resolution_packet_schema": {
            "packet_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_TYPE,
            "packet_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION,
            "required_fields": list(HUMAN_RESOLUTION_PACKET_REQUIRED_FIELDS),
            "allowed_human_resolution_statuses": list(ALLOWED_HUMAN_RESOLUTION_STATUSES),
            "allowed_operator_signoff_statuses": list(ALLOWED_OPERATOR_SIGNOFF_STATUSES),
            "allowed_operator_attestation_statuses": list(
                ALLOWED_OPERATOR_ATTESTATION_STATUSES
            ),
            "allowed_operator_identity_statuses": list(ALLOWED_OPERATOR_IDENTITY_STATUSES),
            "allowed_operator_timestamp_statuses": list(
                ALLOWED_OPERATOR_TIMESTAMP_STATUSES
            ),
            "allowed_selected_candidate_statuses": list(
                ALLOWED_SELECTED_CANDIDATE_STATUSES
            ),
            "allowed_candidate_selection_validation_statuses": list(
                ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES
            ),
            "allowed_final_gate_rerun_statuses": list(ALLOWED_FINAL_GATE_RERUN_STATUSES),
            "allowed_reexecution_readiness_statuses": list(
                ALLOWED_REEXECUTION_READINESS_STATUSES
            ),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_next_action_recommendations": list(
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS
            ),
        },
        "operator_resolution_input_schema": {
            "required_explicit_fields": [
                "operator_identity_ref",
                "operator_signoff_timestamp",
                "operator_attestation_text",
                "operator_scope_acknowledgement",
            ],
            "scope_acknowledgement_value": "acknowledged",
        },
        "selected_candidate_resolution_input_schema": {
            "required_explicit_fields": [
                "selected_candidate_config_ref",
                "selected_candidate_id",
                "selected_candidate_version",
                "selected_candidate_source_path",
                "selected_candidate_selection_reason",
                "candidate_selection_timestamp",
                "operator_reference_for_selection",
            ],
            "candidate_ref_must_match_candidate_option": True,
            "candidate_option_count_does_not_create_selection": True,
        },
        "human_resolution_requirements_schema": {
            "requirements_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_REQUIREMENTS_REPORT_TYPE
            ),
            "requirements_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(HUMAN_RESOLUTION_REQUIREMENTS_REQUIRED_FIELDS),
        },
        "human_resolution_input_template_schema": {
            "template_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TEMPLATE_TYPE,
            "template_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(HUMAN_RESOLUTION_INPUT_TEMPLATE_REQUIRED_FIELDS),
        },
        "human_resolution_readiness_schema": {
            "readiness_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_READINESS_REPORT_TYPE
            ),
            "readiness_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(HUMAN_RESOLUTION_READINESS_REQUIRED_FIELDS),
        },
        "final_gate_rerun_prerequisite_schema": {
            "prerequisite_type": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE
            ),
            "prerequisite_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
            ),
            "required_fields": list(FINAL_GATE_RERUN_PREREQUISITE_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_human_resolution_input_shape": True,
            "validate_human_resolution_packet_shape": True,
            "validate_requirements_readiness_template_and_prerequisites": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_operator_signoff_requires_explicit_human_fields": True,
            "validate_selected_candidate_requires_explicit_human_fields": True,
            "validate_candidate_option_count_does_not_select_candidate": True,
            "validate_no_operator_signoff_inferred_from_codex_tests_branch_commit_tag": True,
            "validate_candidate_option_count_is_inventory_only": True,
            "validate_no_human_resolution_inferred_from_validation_success": True,
            "validate_final_gate_rerun_required_but_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp68_selected_candidate_artifact_path_required": True,
            "bp67_signoff_artifact_path_required": True,
            "bp66_packet_path_required": True,
            "bp65_resolution_packet_path_required": True,
            "bp64_review_packet_path_required": True,
            "bp62_execution_path_required": True,
            "bp61_final_gate_path_required": True,
            "bp60_staging_path_required": True,
            "bp59_application_plan_path_required": True,
            "bp58_human_approval_gate_path_required": True,
            "bp55_change_request_path_required": True,
            "candidate_options_preserved": True,
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


def build_controlled_runtime_calibration_human_resolution_input_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    source_explicit_selected_candidate_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_OUTPUT
    ),
    source_explicit_selected_candidate_artifact_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_SELECTED_CANDIDATE_ARTIFACT_CONTRACT_OUTPUT
    ),
    source_explicit_operator_signoff_artifact_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_OUTPUT
    ),
    source_explicit_operator_signoff_artifact_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_OPERATOR_SIGNOFF_ARTIFACT_CONTRACT_OUTPUT
    ),
    source_operator_signoff_candidate_selection_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    source_operator_signoff_candidate_selection_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    explicit_operator_identity_ref: str | None = None,
    explicit_operator_signoff_timestamp: str | None = None,
    explicit_operator_attestation_text: str | None = None,
    explicit_operator_scope_acknowledgement: str | None = None,
    explicit_selected_candidate_ref: str | None = None,
    explicit_selected_candidate_id: str | None = None,
    explicit_selected_candidate_version: str | None = None,
    explicit_selected_candidate_source_path: str | None = None,
    explicit_selected_candidate_selection_reason: str | None = None,
    explicit_candidate_selection_timestamp: str | None = None,
    explicit_operator_reference_for_selection: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    selected_candidate_artifact = _load_json(
        source_explicit_selected_candidate_artifact_path
    )
    signoff_artifact = _load_json(source_explicit_operator_signoff_artifact_path)
    bp66_packet = _load_json(source_operator_signoff_candidate_selection_packet_path)
    explicit_candidate_ref = _explicit_ref(explicit_selected_candidate_ref)
    candidate_option_refs = _candidate_option_refs(
        selected_candidate_artifact,
        signoff_artifact,
        bp66_packet,
    )
    model_asset_ref = _coalesce(
        selected_candidate_artifact.get("model_asset_ref"),
        signoff_artifact.get("model_asset_ref"),
        bp66_packet.get("model_asset_ref"),
        str(Path(model_asset_path)),
    )
    model_asset_sha = _coalesce(
        selected_candidate_artifact.get("model_asset_sha256"),
        signoff_artifact.get("model_asset_sha256"),
        bp66_packet.get("model_asset_sha256"),
        _sha256_file(Path(str(model_asset_ref))),
    )
    inputs = {
        "human_resolution_input_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_inputs_v1",
            selected_candidate_artifact.get("selected_candidate_artifact_id"),
            signoff_artifact.get("signoff_artifact_id"),
            bp66_packet.get("packet_id"),
            explicit_operator_identity_ref,
            explicit_operator_signoff_timestamp,
            explicit_candidate_ref,
            explicit_candidate_selection_timestamp,
        ),
        "human_resolution_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TYPE
        ),
        "human_resolution_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_explicit_selected_candidate_artifact_path": str(
            Path(source_explicit_selected_candidate_artifact_path)
        ),
        "source_explicit_selected_candidate_artifact_contract_path": str(
            Path(source_explicit_selected_candidate_artifact_contract_path)
        ),
        "source_explicit_operator_signoff_artifact_path": str(
            Path(source_explicit_operator_signoff_artifact_path)
        ),
        "source_explicit_operator_signoff_artifact_contract_path": str(
            Path(source_explicit_operator_signoff_artifact_contract_path)
        ),
        "source_operator_signoff_candidate_selection_packet_path": str(
            Path(source_operator_signoff_candidate_selection_packet_path)
        ),
        "source_operator_signoff_candidate_selection_packet_contract_path": str(
            Path(source_operator_signoff_candidate_selection_packet_contract_path)
        ),
        "source_blocked_execution_resolution_packet_path": _coalesce(
            selected_candidate_artifact.get("source_blocked_execution_resolution_packet_path"),
            signoff_artifact.get("source_blocked_execution_resolution_packet_path"),
            bp66_packet.get("source_blocked_execution_resolution_packet_path"),
        ),
        "source_application_execution_review_packet_path": _coalesce(
            selected_candidate_artifact.get("source_application_execution_review_packet_path"),
            signoff_artifact.get("source_application_execution_review_packet_path"),
            bp66_packet.get("source_application_execution_review_packet_path"),
        ),
        "source_application_execution_path": _coalesce(
            selected_candidate_artifact.get("source_application_execution_path"),
            signoff_artifact.get("source_application_execution_path"),
            bp66_packet.get("source_application_execution_path"),
        ),
        "source_pre_application_final_gate_path": _coalesce(
            selected_candidate_artifact.get("source_pre_application_final_gate_path"),
            signoff_artifact.get("source_pre_application_final_gate_path"),
            bp66_packet.get("source_pre_application_final_gate_path"),
        ),
        "source_runtime_application_staging_path": _coalesce(
            selected_candidate_artifact.get("source_runtime_application_staging_path"),
            signoff_artifact.get("source_runtime_application_staging_path"),
            bp66_packet.get("source_runtime_application_staging_path"),
        ),
        "source_application_plan_path": _coalesce(
            selected_candidate_artifact.get("source_application_plan_path"),
            signoff_artifact.get("source_application_plan_path"),
            bp66_packet.get("source_application_plan_path"),
        ),
        "source_human_approval_gate_path": _coalesce(
            selected_candidate_artifact.get("source_human_approval_gate_path"),
            signoff_artifact.get("source_human_approval_gate_path"),
            bp66_packet.get("source_human_approval_gate_path"),
        ),
        "source_change_request_path": _coalesce(
            selected_candidate_artifact.get("source_change_request_path"),
            signoff_artifact.get("source_change_request_path"),
            bp66_packet.get("source_change_request_path"),
        ),
        "source_candidate_config_freeze_path": _coalesce(
            selected_candidate_artifact.get("source_candidate_config_freeze_path"),
            bp66_packet.get("source_candidate_config_freeze_path"),
        ),
        "source_manual_approval_packet_path": _coalesce(
            selected_candidate_artifact.get("source_manual_approval_packet_path"),
            bp66_packet.get("source_manual_approval_packet_path"),
        ),
        "source_decision_packet_path": _coalesce(
            selected_candidate_artifact.get("source_decision_packet_path"),
            bp66_packet.get("source_decision_packet_path"),
        ),
        "source_phase_freeze_path": _coalesce(
            selected_candidate_artifact.get("source_phase_freeze_path"),
            bp66_packet.get("source_phase_freeze_path"),
        ),
        "candidate_option_refs": candidate_option_refs,
        "explicit_operator_identity_ref": explicit_operator_identity_ref,
        "explicit_operator_signoff_timestamp": explicit_operator_signoff_timestamp,
        "explicit_operator_attestation_text": explicit_operator_attestation_text,
        "explicit_operator_scope_acknowledgement": explicit_operator_scope_acknowledgement,
        "explicit_selected_candidate_ref": explicit_candidate_ref,
        "explicit_selected_candidate_id": explicit_selected_candidate_id,
        "explicit_selected_candidate_version": explicit_selected_candidate_version,
        "explicit_selected_candidate_source_path": explicit_selected_candidate_source_path,
        "explicit_selected_candidate_selection_reason": (
            explicit_selected_candidate_selection_reason
        ),
        "explicit_candidate_selection_timestamp": explicit_candidate_selection_timestamp,
        "explicit_operator_reference_for_selection": (
            explicit_operator_reference_for_selection
        ),
        "source_bp68_selected_candidate_artifact_status": selected_candidate_artifact.get(
            "selected_candidate_artifact_status"
        ),
        "source_bp67_signoff_artifact_status": signoff_artifact.get(
            "signoff_artifact_status"
        ),
        "source_bp66_candidate_option_count": len(_list(bp66_packet.get("candidate_option_refs"))),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(
            _coalesce(
                selected_candidate_artifact.get("runtime_config_target_ref"),
                signoff_artifact.get("runtime_config_target_ref"),
                bp66_packet.get("runtime_config_target_ref"),
            )
        ),
        "runtime_config_target_sha256_before": _coalesce(
            selected_candidate_artifact.get("runtime_config_target_sha256_before"),
            signoff_artifact.get("runtime_config_target_sha256_before"),
            bp66_packet.get("runtime_config_target_sha256_before"),
        ),
        "runtime_config_target_sha256_after": _coalesce(
            selected_candidate_artifact.get("runtime_config_target_sha256_after"),
            signoff_artifact.get("runtime_config_target_sha256_after"),
            bp66_packet.get("runtime_config_target_sha256_after"),
        ),
        "runtime_config_changed": bool(
            _coalesce(
                selected_candidate_artifact.get("runtime_config_changed"),
                signoff_artifact.get("runtime_config_changed"),
                bp66_packet.get("runtime_config_changed"),
                False,
            )
        ),
        "mutation_status": _coalesce(
            selected_candidate_artifact.get("mutation_status"),
            signoff_artifact.get("mutation_status"),
            bp66_packet.get("mutation_status"),
        ),
        "runtime_application_status": _coalesce(
            selected_candidate_artifact.get("runtime_application_status"),
            signoff_artifact.get("runtime_application_status"),
            bp66_packet.get("runtime_application_status"),
            "not_executed",
        ),
        "production_config_status": _coalesce(
            selected_candidate_artifact.get("production_config_status"),
            signoff_artifact.get("production_config_status"),
            bp66_packet.get("production_config_status"),
        ),
        "baseline_update_status": _coalesce(
            selected_candidate_artifact.get("baseline_update_status"),
            signoff_artifact.get("baseline_update_status"),
            bp66_packet.get("baseline_update_status"),
        ),
        "model_update_status": _coalesce(
            selected_candidate_artifact.get("model_update_status"),
            signoff_artifact.get("model_update_status"),
            bp66_packet.get("model_update_status"),
        ),
        "source_bp68_selected_candidate_artifact_id": selected_candidate_artifact.get(
            "selected_candidate_artifact_id"
        ),
        "source_bp67_signoff_artifact_id": signoff_artifact.get("signoff_artifact_id"),
        "source_bp66_packet_id": bp66_packet.get("packet_id"),
        "source_resolution_packet_id": _coalesce(
            selected_candidate_artifact.get("source_resolution_packet_id"),
            signoff_artifact.get("source_resolution_packet_id"),
            bp66_packet.get("source_resolution_packet_id"),
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": {
            "explicit_selected_candidate_artifact": _artifact_ref(
                source_explicit_selected_candidate_artifact_path,
                selected_candidate_artifact,
            ),
            "explicit_selected_candidate_artifact_contract": _artifact_ref(
                source_explicit_selected_candidate_artifact_contract_path,
                _load_json_if_exists(
                    source_explicit_selected_candidate_artifact_contract_path
                ),
            ),
            "explicit_operator_signoff_artifact": _artifact_ref(
                source_explicit_operator_signoff_artifact_path,
                signoff_artifact,
            ),
            "explicit_operator_signoff_artifact_contract": _artifact_ref(
                source_explicit_operator_signoff_artifact_contract_path,
                _load_json_if_exists(
                    source_explicit_operator_signoff_artifact_contract_path
                ),
            ),
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
    errors.extend(_validate_human_resolution_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_human_resolution_inputs",
        "human_resolution_input_id": inputs["human_resolution_input_id"],
        "human_resolution_status": _human_resolution_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_selection_validation_status": (
            _candidate_selection_validation_status(inputs)
        ),
        "candidate_option_count": len(candidate_option_refs),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_application_status": inputs["runtime_application_status"],
        "runtime_config_changed": inputs["runtime_config_changed"],
        "mutation_status": inputs["mutation_status"],
        "next_action_recommendation": _next_actions(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_human_resolution_input_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(human_resolution_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_inputs_shape(inputs))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_human_resolution_input_packet_inputs_validation",
        payload_path=human_resolution_inputs_path,
        payload_type=inputs.get("human_resolution_input_type"),
        payload_version=inputs.get("human_resolution_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_human_resolution_input_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(human_resolution_inputs_path)
    packet_id = _stable_id(
        "controlled_runtime_calibration_human_resolution_input_packet_v1",
        inputs.get("human_resolution_input_id"),
        inputs.get("source_bp68_selected_candidate_artifact_id"),
        inputs.get("source_bp67_signoff_artifact_id"),
        inputs.get("source_bp66_packet_id"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    selected_option = _matched_candidate_option(inputs)
    packet = {
        "human_resolution_packet_id": packet_id,
        "human_resolution_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_TYPE
        ),
        "human_resolution_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_input_path": str(Path(human_resolution_inputs_path)),
        "source_explicit_selected_candidate_artifact_path": inputs.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": inputs.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": inputs.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": inputs.get(
            "source_blocked_execution_resolution_packet_path"
        ),
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
        "source_human_approval_gate_path": inputs.get("source_human_approval_gate_path"),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "source_candidate_config_freeze_path": inputs.get(
            "source_candidate_config_freeze_path"
        ),
        "source_manual_approval_packet_path": inputs.get(
            "source_manual_approval_packet_path"
        ),
        "source_decision_packet_path": inputs.get("source_decision_packet_path"),
        "source_phase_freeze_path": inputs.get("source_phase_freeze_path"),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "operator_identity_ref": inputs.get("explicit_operator_identity_ref"),
        "operator_signoff_timestamp": inputs.get("explicit_operator_signoff_timestamp"),
        "operator_attestation_text": inputs.get("explicit_operator_attestation_text"),
        "operator_scope_acknowledgement": inputs.get(
            "explicit_operator_scope_acknowledgement"
        ),
        "selected_candidate_config_ref": _dict(
            inputs.get("explicit_selected_candidate_ref")
        )
        or None,
        "selected_candidate_id": inputs.get("explicit_selected_candidate_id"),
        "selected_candidate_version": inputs.get("explicit_selected_candidate_version"),
        "selected_candidate_source_path": inputs.get(
            "explicit_selected_candidate_source_path"
        ),
        "selected_candidate_settings_summary": (
            _dict(selected_option.get("candidate_settings_summary"))
            if selected_option
            else {}
        ),
        "selected_candidate_provenance": (
            _dict(selected_option.get("provenance_summary")) if selected_option else {}
        ),
        "selected_candidate_selection_reason": inputs.get(
            "explicit_selected_candidate_selection_reason"
        ),
        "candidate_selection_timestamp": inputs.get(
            "explicit_candidate_selection_timestamp"
        ),
        "operator_reference_for_selection": inputs.get(
            "explicit_operator_reference_for_selection"
        ),
        "source_bp68_selected_candidate_artifact_status": inputs.get(
            "source_bp68_selected_candidate_artifact_status"
        ),
        "source_bp67_signoff_artifact_status": inputs.get(
            "source_bp67_signoff_artifact_status"
        ),
        "source_bp66_candidate_option_count": inputs.get(
            "source_bp66_candidate_option_count"
        ),
        "human_resolution_status": _human_resolution_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_selection_validation_status": (
            _candidate_selection_validation_status(inputs)
        ),
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
        "human_resolution_requirements": _human_resolution_requirements(
            packet_id,
            inputs,
            generated_at,
        ),
        "human_resolution_input_template": _human_resolution_input_template(
            packet_id,
            inputs,
            generated_at,
        ),
        "human_resolution_readiness": _human_resolution_readiness(
            packet_id,
            inputs,
            generated_at,
        ),
        "final_gate_rerun_prerequisites": _final_gate_rerun_prerequisites(
            packet_id,
            inputs,
            generated_at,
        ),
        "next_action_recommendation": _next_actions(inputs),
        "source_bp68_selected_candidate_artifact_id": inputs.get(
            "source_bp68_selected_candidate_artifact_id"
        ),
        "source_bp67_signoff_artifact_id": inputs.get(
            "source_bp67_signoff_artifact_id"
        ),
        "source_bp66_packet_id": inputs.get("source_bp66_packet_id"),
        "source_resolution_packet_id": inputs.get("source_resolution_packet_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_inputs_shape(inputs))
    errors.extend(_validate_human_resolution_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_human_resolution_packet",
        "human_resolution_packet_id": packet["human_resolution_packet_id"],
        "human_resolution_status": packet["human_resolution_status"],
        "operator_signoff_status": packet["operator_signoff_status"],
        "operator_attestation_status": packet["operator_attestation_status"],
        "operator_identity_status": packet["operator_identity_status"],
        "operator_timestamp_status": packet["operator_timestamp_status"],
        "selected_candidate_status": packet["selected_candidate_status"],
        "candidate_selection_validation_status": (
            packet["candidate_selection_validation_status"]
        ),
        "candidate_option_count": packet["candidate_option_count"],
        "final_gate_rerun_status": packet["final_gate_rerun_status"],
        "reexecution_readiness_status": packet["reexecution_readiness_status"],
        "runtime_application_status": packet["runtime_application_status"],
        "runtime_config_changed": packet["runtime_config_changed"],
        "mutation_status": packet["mutation_status"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "human_resolution_packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_human_resolution_input_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(human_resolution_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_packet_shape(packet))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_human_resolution_input_packet_validation",
        payload_path=human_resolution_packet_path,
        payload_type=packet.get("human_resolution_packet_type"),
        payload_version=packet.get("human_resolution_packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_human_resolution_requirements_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_REQUIREMENTS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(human_resolution_packet_path)
    report = {
        **_dict(packet.get("human_resolution_requirements")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_REQUIREMENTS_REPORT_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_packet_path": str(Path(human_resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_packet_shape(packet))
    errors.extend(_validate_human_resolution_requirements_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_human_resolution_requirements_report",
        "human_resolution_requirements_id": report.get(
            "human_resolution_requirements_id"
        ),
        "human_resolution_status": report.get("human_resolution_status"),
        "operator_signoff_status": report.get("operator_signoff_status"),
        "selected_candidate_status": report.get("selected_candidate_status"),
        "human_resolution_requirements_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_input_template(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TEMPLATE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(human_resolution_packet_path)
    template = {
        **_dict(packet.get("human_resolution_input_template")),
        "template_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_TEMPLATE_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_packet_path": str(Path(human_resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_packet_shape(packet))
    errors.extend(_validate_human_resolution_input_template_shape(template))
    _write_json_if_requested(output_path, template)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_human_resolution_input_template",
        "human_resolution_input_template_id": template.get(
            "human_resolution_input_template_id"
        ),
        "human_resolution_status": template.get("human_resolution_status"),
        "human_resolution_input_template_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(human_resolution_packet_path)
    report = {
        **_dict(packet.get("human_resolution_readiness")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_READINESS_REPORT_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_packet_path": str(Path(human_resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_packet_shape(packet))
    errors.extend(_validate_human_resolution_readiness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_human_resolution_readiness_report",
        "human_resolution_readiness_id": report.get("human_resolution_readiness_id"),
        "human_resolution_status": report.get("human_resolution_status"),
        "operator_signoff_status": report.get("operator_signoff_status"),
        "selected_candidate_status": report.get("selected_candidate_status"),
        "final_gate_rerun_status": report.get("final_gate_rerun_status"),
        "reexecution_readiness_status": report.get("reexecution_readiness_status"),
        "human_resolution_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_OUTPUT
    ),
    human_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(human_resolution_packet_path)
    report = {
        **_dict(packet.get("final_gate_rerun_prerequisites")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE
        ),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_packet_path": str(Path(human_resolution_packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_packet_shape(packet))
    errors.extend(_validate_final_gate_rerun_prerequisites_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": (
            "completed"
            if not errors
            else "invalid_final_gate_rerun_prerequisite_report"
        ),
        "final_gate_rerun_prerequisite_id": report.get(
            "final_gate_rerun_prerequisite_id"
        ),
        "final_gate_rerun_status": report.get("final_gate_rerun_status"),
        "reexecution_readiness_status": report.get("reexecution_readiness_status"),
        "final_gate_rerun_prerequisite_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _human_resolution_requirements(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "human_resolution_requirements_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_requirements_v1",
            packet_id,
        ),
        "human_resolution_requirements_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_packet_id": packet_id,
        "requirements": {
            "explicit_operator_identity_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_identity_ref")),
            },
            "explicit_operator_timestamp_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_signoff_timestamp")),
            },
            "explicit_operator_attestation_required": {
                "required": True,
                "status": _operator_attestation_status(inputs),
            },
            "explicit_operator_scope_acknowledgement_required": {
                "required": True,
                "provided": inputs.get("explicit_operator_scope_acknowledgement")
                == "acknowledged",
            },
            "explicit_selected_candidate_ref_required": {
                "required": True,
                "provided": bool(_dict(inputs.get("explicit_selected_candidate_ref"))),
            },
            "explicit_selected_candidate_source_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_selected_candidate_source_path")),
            },
            "explicit_selected_candidate_provenance_required": {
                "required": True,
                "status": _candidate_selection_validation_status(inputs),
            },
            "explicit_selected_candidate_reason_required": {
                "required": True,
                "provided": bool(
                    inputs.get("explicit_selected_candidate_selection_reason")
                ),
            },
            "explicit_selected_candidate_timestamp_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_candidate_selection_timestamp")),
            },
            "explicit_operator_reference_for_selection_required": {
                "required": True,
                "provided": bool(
                    inputs.get("explicit_operator_reference_for_selection")
                ),
            },
            "source_bp68_artifact_required": {
                "required": True,
                "path": inputs.get(
                    "source_explicit_selected_candidate_artifact_path"
                ),
                "status": inputs.get("source_bp68_selected_candidate_artifact_status"),
            },
            "source_bp67_artifact_required": {
                "required": True,
                "path": inputs.get("source_explicit_operator_signoff_artifact_path"),
                "status": inputs.get("source_bp67_signoff_artifact_status"),
            },
            "source_bp66_packet_required": {
                "required": True,
                "path": inputs.get(
                    "source_operator_signoff_candidate_selection_packet_path"
                ),
                "candidate_option_count": inputs.get(
                    "source_bp66_candidate_option_count"
                ),
            },
            "source_bp65_packet_required": {
                "required": True,
                "path": inputs.get("source_blocked_execution_resolution_packet_path"),
            },
            "no_runtime_application_performed_by_this_packet": {
                "required": True,
                "status": "preserved",
            },
            "candidate_option_count_does_not_create_selection": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_codex_execution": {
                "required": True,
                "status": "preserved",
            },
            "selected_candidate_must_not_be_inferred_from_single_available_option": {
                "required": True,
                "status": "preserved",
            },
            "human_resolution_must_be_explicit": {
                "required": True,
                "status": "preserved",
            },
        },
        "human_resolution_status": _human_resolution_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _human_resolution_input_template(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "human_resolution_input_template_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_input_template_v1",
            packet_id,
        ),
        "human_resolution_input_template_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_packet_id": packet_id,
        "template_placeholders": {
            "operator_identity_ref": None,
            "operator_signoff_timestamp": None,
            "operator_attestation_text": HUMAN_RESOLUTION_ATTESTATION_TEXT_TEMPLATE,
            "operator_scope_acknowledgement": "acknowledged",
            "selected_candidate_config_ref": None,
            "selected_candidate_id": None,
            "selected_candidate_version": None,
            "selected_candidate_source_path": None,
            "selected_candidate_selection_reason": None,
            "candidate_selection_timestamp": None,
            "operator_reference_for_selection": None,
        },
        "attestation_text_template": HUMAN_RESOLUTION_ATTESTATION_TEXT_TEMPLATE,
        "candidate_option_refs_for_review": _list(inputs.get("candidate_option_refs")),
        "required_operator_fields": {
            "operator_identity_ref": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_identity_ref")),
            },
            "operator_signoff_timestamp": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_signoff_timestamp")),
            },
            "operator_attestation_text": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_attestation_text")),
            },
            "operator_scope_acknowledgement": {
                "required": True,
                "provided": inputs.get("explicit_operator_scope_acknowledgement")
                == "acknowledged",
            },
        },
        "required_selected_candidate_fields": {
            "selected_candidate_config_ref": {
                "required": True,
                "provided": bool(_dict(inputs.get("explicit_selected_candidate_ref"))),
            },
            "selected_candidate_id": {
                "required": True,
                "provided": bool(inputs.get("explicit_selected_candidate_id")),
            },
            "selected_candidate_version": {
                "required": True,
                "provided": bool(inputs.get("explicit_selected_candidate_version")),
            },
            "selected_candidate_source_path": {
                "required": True,
                "provided": bool(inputs.get("explicit_selected_candidate_source_path")),
            },
            "selected_candidate_selection_reason": {
                "required": True,
                "provided": bool(
                    inputs.get("explicit_selected_candidate_selection_reason")
                ),
            },
            "candidate_selection_timestamp": {
                "required": True,
                "provided": bool(inputs.get("explicit_candidate_selection_timestamp")),
            },
            "operator_reference_for_selection": {
                "required": True,
                "provided": bool(
                    inputs.get("explicit_operator_reference_for_selection")
                ),
            },
        },
        "human_resolution_status": _human_resolution_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _human_resolution_readiness(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "human_resolution_readiness_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_readiness_v1",
            packet_id,
        ),
        "human_resolution_readiness_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_packet_id": packet_id,
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
            "selected_candidate_explicitly_recorded": _selected_candidate_status(inputs)
            == "selected_candidate_explicitly_recorded",
            "candidate_selection_validation_completed": (
                _candidate_selection_validation_status(inputs)
                == "candidate_selection_valid_explicit_candidate"
            ),
            "candidate_option_count_does_not_create_selection": True,
            "human_resolution_explicitly_recorded": _human_resolution_status(inputs)
            == "human_resolution_explicit_inputs_recorded",
            "final_gate_not_rerun_by_bp69": True,
            "runtime_application_not_executed_by_bp69": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "human_resolution_status": _human_resolution_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_selection_validation_status": (
            _candidate_selection_validation_status(inputs)
        ),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "next_action_recommendation": _next_actions(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_rerun_prerequisites(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    human_ready = _human_resolution_status(inputs) == (
        "human_resolution_explicit_inputs_recorded"
    )
    return {
        "final_gate_rerun_prerequisite_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_prerequisite_v1",
            packet_id,
        ),
        "final_gate_rerun_prerequisite_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_packet_id": packet_id,
        "prerequisite_checks": {
            "explicit_operator_signoff_required_before_rerun": {
                "ready": _operator_signoff_status(inputs)
                == "operator_signoff_explicitly_recorded",
                "status": _operator_signoff_status(inputs),
            },
            "explicit_selected_candidate_required_before_rerun": {
                "ready": _selected_candidate_status(inputs)
                == "selected_candidate_explicitly_recorded",
                "status": _selected_candidate_status(inputs),
            },
            "candidate_selection_validation_required_before_rerun": {
                "ready": _candidate_selection_validation_status(inputs)
                == "candidate_selection_valid_explicit_candidate",
                "status": _candidate_selection_validation_status(inputs),
            },
            "human_resolution_required_before_rerun": {
                "ready": human_ready,
                "status": _human_resolution_status(inputs),
            },
            "final_gate_not_rerun_by_this_packet": {
                "ready": False,
                "status": "final_gate_rerun_required",
            },
            "runtime_application_not_executed_by_this_packet": {
                "ready": False,
                "status": inputs.get("runtime_application_status"),
            },
        },
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _human_resolution_status(payload: dict[str, Any]) -> str:
    operator_status = _operator_signoff_status(payload)
    selected_status = _selected_candidate_status(payload)
    if operator_status == "operator_signoff_invalid" or selected_status == (
        "selected_candidate_invalid"
    ):
        return "human_resolution_invalid"
    if (
        operator_status == "operator_signoff_explicitly_recorded"
        and selected_status == "selected_candidate_explicitly_recorded"
    ):
        return "human_resolution_explicit_inputs_recorded"
    if (
        operator_status == "operator_signoff_explicitly_recorded"
        or selected_status == "selected_candidate_explicitly_recorded"
        or _operator_input_started(payload)
        or _selected_candidate_input_started(payload)
    ):
        return "human_resolution_partially_recorded"
    return "human_resolution_input_required"


def _operator_signoff_status(payload: dict[str, Any]) -> str:
    if not _operator_input_started(payload):
        return "operator_signoff_required"
    if (
        _operator_identity_status(payload) != "operator_identity_explicitly_recorded"
        or _operator_timestamp_status(payload)
        != "operator_timestamp_explicitly_recorded"
        or _operator_attestation_status(payload)
        != "operator_attestation_explicitly_recorded"
    ):
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


def _selected_candidate_status(payload: dict[str, Any]) -> str:
    if not _selected_candidate_input_started(payload):
        return "selected_candidate_required"
    if _candidate_selection_validation_status(payload) != (
        "candidate_selection_valid_explicit_candidate"
    ):
        return "selected_candidate_invalid"
    return "selected_candidate_explicitly_recorded"


def _candidate_selection_validation_status(payload: dict[str, Any]) -> str:
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not _selected_candidate_input_started(payload):
        return "candidate_selection_pending_explicit_input"
    if not explicit_ref:
        return "candidate_selection_invalid_missing_ref"
    errors = _validate_explicit_selected_candidate_input(payload)
    error_codes = {str(error.get("code")) for error in errors}
    if "invalid_explicit_selected_candidate_ref" in error_codes:
        return "candidate_selection_invalid_unknown_candidate"
    if errors:
        return "candidate_selection_invalid_missing_provenance"
    return "candidate_selection_valid_explicit_candidate"


def _final_gate_rerun_status(payload: dict[str, Any]) -> str:
    human_status = _human_resolution_status(payload)
    if human_status == "human_resolution_invalid":
        return "final_gate_rerun_blocked_invalid_human_resolution"
    if human_status == "human_resolution_explicit_inputs_recorded":
        return "final_gate_rerun_ready_after_human_resolution"
    return "final_gate_rerun_required"


def _reexecution_readiness_status(payload: dict[str, Any]) -> str:
    if _final_gate_rerun_status(payload) == "final_gate_rerun_ready_after_human_resolution":
        return "reexecution_blocked_final_gate_not_rerun"
    return "reexecution_not_ready_blockers_unresolved"


def _next_actions(payload: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if _human_resolution_status(payload) != "human_resolution_explicit_inputs_recorded":
        actions.append("provide_human_resolution_inputs")
    if (
        _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded"
        or _selected_candidate_status(payload)
        != "selected_candidate_explicitly_recorded"
    ):
        actions.append("provide_operator_signoff_and_selected_candidate")
    actions.append("rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _operator_input_started(payload: dict[str, Any]) -> bool:
    return any(
        bool(payload.get(field))
        for field in [
            "explicit_operator_identity_ref",
            "explicit_operator_signoff_timestamp",
            "explicit_operator_attestation_text",
            "explicit_operator_scope_acknowledgement",
        ]
    )


def _selected_candidate_input_started(payload: dict[str, Any]) -> bool:
    return any(
        bool(
            _dict(payload.get(field))
            if field == "explicit_selected_candidate_ref"
            else payload.get(field)
        )
        for field in [
            "explicit_selected_candidate_ref",
            "explicit_selected_candidate_id",
            "explicit_selected_candidate_version",
            "explicit_selected_candidate_source_path",
            "explicit_selected_candidate_selection_reason",
            "explicit_candidate_selection_timestamp",
            "explicit_operator_reference_for_selection",
        ]
    )


def _candidate_option_refs(
    selected_candidate_artifact: dict[str, Any],
    signoff_artifact: dict[str, Any],
    bp66_packet: dict[str, Any],
) -> list[Any]:
    refs = _list(selected_candidate_artifact.get("candidate_option_refs"))
    if refs:
        return refs
    refs = _list(signoff_artifact.get("candidate_option_refs"))
    if refs:
        return refs
    return _list(bp66_packet.get("candidate_option_refs"))


def _matched_candidate_option(payload: dict[str, Any]) -> dict[str, Any] | None:
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not explicit_ref:
        return None
    explicit_tokens = _candidate_ref_tokens(explicit_ref)
    for option in _list(payload.get("candidate_option_refs")):
        option_dict = _dict(option)
        if explicit_tokens & _candidate_ref_tokens(option_dict):
            return option_dict
    return None


def _candidate_ref_tokens(ref: dict[str, Any]) -> set[str]:
    tokens: set[str] = set()
    for key in [
        "ref",
        "path",
        "source_path",
        "candidate_id",
        "candidate_config_freeze_id",
        "candidate_packet_id",
        "candidate_version",
        "candidate_config_freeze_version",
    ]:
        value = ref.get(key)
        if value:
            tokens.add(str(value))
    return tokens


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "human_resolution_input_scope",
        "source_contract_refs",
        "human_resolution_input_schema",
        "human_resolution_packet_schema",
        "operator_resolution_input_schema",
        "selected_candidate_resolution_input_schema",
        "human_resolution_requirements_schema",
        "human_resolution_input_template_schema",
        "human_resolution_readiness_schema",
        "final_gate_rerun_prerequisite_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_INPUT_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_human_resolution_inputs_shape(
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        inputs,
        HUMAN_RESOLUTION_INPUT_REQUIRED_FIELDS,
        "human_resolution_inputs",
    )
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_explicit_operator_input(inputs))
    errors.extend(_validate_explicit_selected_candidate_input(inputs))
    errors.extend(
        _validate_status(
            "human_resolution_status",
            _human_resolution_status(inputs),
            ALLOWED_HUMAN_RESOLUTION_STATUSES,
        )
    )
    errors.extend(_validate_next_actions(_next_actions(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_human_resolution_packet_shape(
    packet: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        packet,
        HUMAN_RESOLUTION_PACKET_REQUIRED_FIELDS,
        "human_resolution_packet",
    )
    errors.extend(
        _validate_status(
            "human_resolution_status",
            packet.get("human_resolution_status"),
            ALLOWED_HUMAN_RESOLUTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            packet.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_attestation_status",
            packet.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_identity_status",
            packet.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_timestamp_status",
            packet.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "selected_candidate_status",
            packet.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "candidate_selection_validation_status",
            packet.get("candidate_selection_validation_status"),
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
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
    errors.extend(
        _validate_status(
            "runtime_application_status",
            packet.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        )
    )
    errors.extend(_validate_blocked_runtime_state(packet))
    errors.extend(
        _validate_human_resolution_requirements_shape(
            _dict(packet.get("human_resolution_requirements"))
        )
    )
    errors.extend(
        _validate_human_resolution_input_template_shape(
            _dict(packet.get("human_resolution_input_template"))
        )
    )
    errors.extend(
        _validate_human_resolution_readiness_shape(
            _dict(packet.get("human_resolution_readiness"))
        )
    )
    errors.extend(
        _validate_final_gate_rerun_prerequisites_shape(
            _dict(packet.get("final_gate_rerun_prerequisites"))
        )
    )
    errors.extend(_validate_next_actions(_list(packet.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_explicit_operator_input(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if not _operator_input_started(payload):
        return []
    if _operator_signoff_status(payload) == "operator_signoff_explicitly_recorded":
        return []
    return [
        _error(
            "invalid_explicit_operator_resolution_input",
            "operator_resolution_input",
            _operator_signoff_status(payload),
        )
    ]


def _validate_explicit_selected_candidate_input(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not _selected_candidate_input_started(payload):
        return errors
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not explicit_ref:
        errors.append(
            _error(
                "missing_explicit_selected_candidate_ref",
                "explicit_selected_candidate_ref",
                payload.get("explicit_selected_candidate_ref"),
            )
        )
        return errors
    if not _matched_candidate_option(payload):
        errors.append(
            _error(
                "invalid_explicit_selected_candidate_ref",
                "explicit_selected_candidate_ref",
                payload.get("explicit_selected_candidate_ref"),
            )
        )
    required_when_explicit = {
        "explicit_selected_candidate_id": payload.get("explicit_selected_candidate_id"),
        "explicit_selected_candidate_version": payload.get(
            "explicit_selected_candidate_version"
        ),
        "explicit_selected_candidate_source_path": payload.get(
            "explicit_selected_candidate_source_path"
        ),
        "explicit_selected_candidate_selection_reason": payload.get(
            "explicit_selected_candidate_selection_reason"
        ),
        "explicit_candidate_selection_timestamp": payload.get(
            "explicit_candidate_selection_timestamp"
        ),
        "explicit_operator_reference_for_selection": payload.get(
            "explicit_operator_reference_for_selection"
        ),
    }
    for field, value in required_when_explicit.items():
        if not value:
            errors.append(_error("missing_explicit_candidate_provenance", field, value))
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
    if payload.get("runtime_application_status") not in {
        "not_executed",
        "blocked_from_runtime_application",
    }:
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_executed",
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


def _validate_human_resolution_requirements_shape(
    requirements: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        requirements,
        HUMAN_RESOLUTION_REQUIREMENTS_REQUIRED_FIELDS,
        "human_resolution_requirements",
    )
    errors.extend(
        _validate_status(
            "human_resolution_status",
            requirements.get("human_resolution_status"),
            ALLOWED_HUMAN_RESOLUTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            requirements.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "selected_candidate_status",
            requirements.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        )
    )
    return errors


def _validate_human_resolution_input_template_shape(
    template: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        template,
        HUMAN_RESOLUTION_INPUT_TEMPLATE_REQUIRED_FIELDS,
        "human_resolution_input_template",
    )
    errors.extend(
        _validate_status(
            "human_resolution_status",
            template.get("human_resolution_status"),
            ALLOWED_HUMAN_RESOLUTION_STATUSES,
        )
    )
    return errors


def _validate_human_resolution_readiness_shape(
    readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        readiness,
        HUMAN_RESOLUTION_READINESS_REQUIRED_FIELDS,
        "human_resolution_readiness",
    )
    for field, allowed in [
        ("human_resolution_status", ALLOWED_HUMAN_RESOLUTION_STATUSES),
        ("operator_signoff_status", ALLOWED_OPERATOR_SIGNOFF_STATUSES),
        ("operator_attestation_status", ALLOWED_OPERATOR_ATTESTATION_STATUSES),
        ("operator_identity_status", ALLOWED_OPERATOR_IDENTITY_STATUSES),
        ("operator_timestamp_status", ALLOWED_OPERATOR_TIMESTAMP_STATUSES),
        ("selected_candidate_status", ALLOWED_SELECTED_CANDIDATE_STATUSES),
        (
            "candidate_selection_validation_status",
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
        ),
        ("final_gate_rerun_status", ALLOWED_FINAL_GATE_RERUN_STATUSES),
        ("reexecution_readiness_status", ALLOWED_REEXECUTION_READINESS_STATUSES),
        ("runtime_application_status", ALLOWED_RUNTIME_APPLICATION_STATUSES),
    ]:
        errors.extend(_validate_status(field, readiness.get(field), allowed))
    errors.extend(_validate_next_actions(_list(readiness.get("next_action_recommendation"))))
    return errors


def _validate_final_gate_rerun_prerequisites_shape(
    prerequisites: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        prerequisites,
        FINAL_GATE_RERUN_PREREQUISITE_REQUIRED_FIELDS,
        "final_gate_rerun_prerequisites",
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            prerequisites.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            prerequisites.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_application_status",
            prerequisites.get("runtime_application_status"),
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
            if key in FORBIDDEN_HUMAN_RESOLUTION_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_HUMAN_RESOLUTION_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "human_resolution_status",
        "operator_signoff_status",
        "operator_attestation_status",
        "operator_identity_status",
        "operator_timestamp_status",
        "selected_candidate_status",
        "candidate_selection_validation_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PACKET_VERSION
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
        "human_resolution_packet_type",
        "selected_candidate_artifact_type",
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
        "human_resolution_packet_version",
        "selected_candidate_artifact_version",
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


def _coalesce(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_BLUEPRINT_NAME,
    }
