from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_runtime_application_staging import (
    CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE,
    FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_pre_apply_manifest,
    build_controlled_runtime_calibration_runtime_application_staging,
    build_controlled_runtime_calibration_runtime_application_staging_inputs,
    build_controlled_runtime_calibration_staged_config_delta,
    build_controlled_runtime_calibration_staged_post_application_verification_report,
    build_controlled_runtime_calibration_staged_rollback_report,
    export_controlled_runtime_calibration_runtime_application_staging_contract,
    validate_controlled_runtime_calibration_runtime_application_staging,
    validate_controlled_runtime_calibration_runtime_application_staging_inputs,
    validate_controlled_runtime_calibration_staged_config_delta,
)


def test_export_controlled_runtime_calibration_runtime_application_staging_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_runtime_application_staging_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION
    )

    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["staging_scope"]["consumes_application_plan"] is True
    assert contract["staging_scope"]["creates_staged_config_delta"] is True
    assert contract["staging_scope"]["applies_threshold_changes"] is False
    assert contract["staging_scope"]["updates_runtime_configuration"] is False
    assert contract["staging_scope"]["creates_production_configuration"] is False
    assert contract["staging_scope"]["updates_model_weights"] is False
    assert contract["staging_scope"]["mutates_regression_baselines"] is False
    assert (
        contract["staging_artifact_schema"]["required_runtime_application_status"]
        == "staged_not_applied"
    )
    assert contract["staging_artifact_schema"]["required_runtime_config_status"] == (
        "not_updated"
    )
    assert contract["warnings"]["controlled_runtime_application_staging"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS
        & _walk_exact_strings_and_keys(contract)
    )


def test_build_and_validate_controlled_runtime_calibration_runtime_application_staging_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_runtime_application_staging_inputs(
        contract_path=paths["contract"],
        source_application_plan_path=paths["application_plan"],
        source_human_approval_gate_path=paths["human_gate"],
        source_dry_run_review_packet_path=paths["review_packet"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        current_runtime_settings_ref="runtime_settings_fixture",
        output_path=paths["staging_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["staging_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["current_threshold"] == 0.55
    assert inputs["staged_candidate_threshold"] == 0.58
    assert result["runtime_application_status"] == "staged_not_applied"
    assert inputs["source_artifact_presence"]["application_plan"]["present"] is True
    assert inputs["missing_source_refs"] == []
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS
        & _walk_exact_strings_and_keys(inputs)
    )

    validation = (
        validate_controlled_runtime_calibration_runtime_application_staging_inputs(
            contract_path=paths["contract"],
            staging_inputs_path=paths["staging_inputs"],
            output_path=paths["staging_inputs_validation"],
            validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
        )
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_runtime_application_staging(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_staging_inputs(paths)

    result = build_controlled_runtime_calibration_runtime_application_staging(
        contract_path=paths["contract"],
        staging_inputs_path=paths["staging_inputs"],
        output_path=paths["staging"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["staging_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
    )
    assert result["staging_status"] == "staging_artifact_created"
    assert result["staged_config_delta_status"] == "staged_for_future_blueprint"
    assert result["pre_apply_manifest_status"] == "pre_apply_manifest_defined"
    assert result["rollback_staging_status"] == "rollback_staging_record_defined"
    assert result["post_application_verification_staging_status"] == (
        "post_application_verification_staged"
    )
    assert result["runtime_application_status"] == "staged_not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["runtime_config_status"] == "not_updated"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"
    assert result["future_blueprint_required_for_runtime_application"] is True

    staging = json.loads(paths["staging"].read_text(encoding="utf-8"))
    assert staging["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert staging["staged_config_delta"]["runtime_config_status"] == "not_updated"
    assert staging["pre_apply_manifest"]["missing_requirements"] == []
    assert staging["rollback_staging_record"]["runtime_application_status"] == (
        "staged_not_applied"
    )
    assert staging["future_baseline_candidate_staging_policy"][
        "future_baseline_candidate_not_created_in_this_blueprint"
    ] is True
    assert staging["non_claims"] == NON_CLAIMS
    assert not (
        FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS
        & _walk_exact_strings_and_keys(staging)
    )

    validation = validate_controlled_runtime_calibration_runtime_application_staging(
        contract_path=paths["contract"],
        staging_path=paths["staging"],
        output_path=paths["staging_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "staged_not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"
    assert validation["future_blueprint_required_for_runtime_application"] is True


def test_runtime_application_staging_does_not_mark_empty_candidate_settings_as_change(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)
    application_plan = json.loads(paths["application_plan"].read_text(encoding="utf-8"))
    application_plan["selected_candidate_config_ref"] = {}
    application_plan["proposed_candidate_settings"] = {}
    application_plan["blockers"] = ["no_candidate_selected"]
    application_plan["pre_application_gate"]["blockers"] = ["no_candidate_selected"]
    paths["application_plan"].write_text(
        json.dumps(application_plan),
        encoding="utf-8",
    )
    _build_staging_inputs_from_sources(paths)

    result = build_controlled_runtime_calibration_runtime_application_staging(
        contract_path=paths["contract"],
        staging_inputs_path=paths["staging_inputs"],
        output_path=paths["staging"],
        generated_at=datetime(2026, 6, 20, 2, 30, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["staging_status"] == "staging_blocked_unresolved_blockers"
    assert result["staged_config_delta_status"] == (
        "staged_blocked_missing_candidate_settings"
    )
    staging = json.loads(paths["staging"].read_text(encoding="utf-8"))
    assert not any(
        delta["change_present"] is True
        for delta in staging["staged_config_delta"]["delta_fields"]
    )
    hysteresis_delta = next(
        delta
        for delta in staging["staged_config_delta"]["delta_fields"]
        if delta["field"] == "hysteresis_settings"
    )
    assert hysteresis_delta["staged_value"] == {}
    assert hysteresis_delta["change_present"] is False


def test_build_runtime_application_staging_reports(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_staging(paths)

    staged_delta_result = build_controlled_runtime_calibration_staged_config_delta(
        contract_path=paths["contract"],
        staging_path=paths["staging"],
        output_path=paths["staged_delta"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert staged_delta_result["ok"] is True
    staged_delta = json.loads(paths["staged_delta"].read_text(encoding="utf-8"))
    assert staged_delta["delta_status"] == "staged_for_future_blueprint"
    assert staged_delta["runtime_config_status"] == "not_updated"

    staged_delta_validation = validate_controlled_runtime_calibration_staged_config_delta(
        contract_path=paths["contract"],
        staged_config_delta_path=paths["staged_delta"],
        output_path=paths["staged_delta_validation"],
        validated_at=datetime(2026, 6, 20, 3, 1, tzinfo=UTC),
    )
    assert staged_delta_validation["ok"] is True

    manifest_result = build_controlled_runtime_calibration_pre_apply_manifest(
        contract_path=paths["contract"],
        staging_path=paths["staging"],
        output_path=paths["pre_apply_manifest"],
        generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
    )
    assert manifest_result["ok"] is True
    manifest = json.loads(paths["pre_apply_manifest"].read_text(encoding="utf-8"))
    assert manifest["manifest_status"] == "pre_apply_manifest_defined"

    rollback_result = build_controlled_runtime_calibration_staged_rollback_report(
        contract_path=paths["contract"],
        staging_path=paths["staging"],
        output_path=paths["rollback_report"],
        generated_at=datetime(2026, 6, 20, 3, 10, tzinfo=UTC),
    )
    assert rollback_result["ok"] is True
    rollback = json.loads(paths["rollback_report"].read_text(encoding="utf-8"))
    assert rollback["rollback_staging_status"] == "rollback_staging_record_defined"

    verification_result = (
        build_controlled_runtime_calibration_staged_post_application_verification_report(
            contract_path=paths["contract"],
            staging_path=paths["staging"],
            output_path=paths["verification_report"],
            generated_at=datetime(2026, 6, 20, 3, 15, tzinfo=UTC),
        )
    )
    assert verification_result["ok"] is True
    verification = json.loads(paths["verification_report"].read_text(encoding="utf-8"))
    assert verification["verification_staging_status"] == (
        "post_application_verification_staged"
    )
    assert verification["non_claims"] == NON_CLAIMS


def test_runtime_application_staging_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_staging(paths)
    staging = json.loads(paths["staging"].read_text(encoding="utf-8"))
    staging["runtime_application_performed"] = True
    paths["staging"].write_text(json.dumps(staging), encoding="utf-8")

    result = validate_controlled_runtime_calibration_runtime_application_staging(
        contract_path=paths["contract"],
        staging_path=paths["staging"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(
        error["error_type"] == "forbidden_field_or_value"
        for error in result["errors"]
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "application_plan": tmp_path / "application_plan.json",
        "human_gate": tmp_path / "human_gate.json",
        "review_packet": tmp_path / "review_packet.json",
        "dry_run_report": tmp_path / "dry_run_report.json",
        "change_request": tmp_path / "change_request.json",
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_packet": tmp_path / "manual_packet.json",
        "decision_packet": tmp_path / "decision_packet.json",
        "phase_freeze": tmp_path / "phase_freeze.json",
        "gameplay_baseline": tmp_path / "gameplay_baseline.json",
        "sandbox_baseline": tmp_path / "sandbox_baseline.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
        "staging_inputs": tmp_path / "staging_inputs.json",
        "staging_inputs_validation": tmp_path / "staging_inputs.validation.json",
        "staging": tmp_path / "staging.json",
        "staging_validation": tmp_path / "staging.validation.json",
        "staged_delta": tmp_path / "staged_delta.json",
        "staged_delta_validation": tmp_path / "staged_delta.validation.json",
        "pre_apply_manifest": tmp_path / "pre_apply_manifest.json",
        "rollback_report": tmp_path / "rollback_report.json",
        "verification_report": tmp_path / "verification_report.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_runtime_application_staging_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )
    paths["model_asset"].write_bytes(b"model fixture")
    current_settings = {
        "current_threshold": 0.55,
        "current_smoothing_window": 3,
        "current_hysteresis_settings": {
            "enter_gameplay_probability": 0.6,
            "exit_gameplay_probability": 0.45,
        },
        "runtime_application_status": "not_applied",
    }
    proposed_candidate_settings = {
        "proposed_candidate_threshold": 0.58,
        "proposed_candidate_smoothing_window": 5,
        "proposed_candidate_hysteresis_settings": {
            "enter_gameplay_probability": 0.62,
            "exit_gameplay_probability": 0.43,
        },
        "candidate_type": "threshold_candidate",
        "candidate_source": {"candidate_packet_id": "candidate_fixture"},
        "not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }
    selected_candidate_config_ref = {
        "candidate_packet_id": "candidate_fixture",
        "candidate_setting_id": "candidate_setting_fixture",
        "source_proposal_item_id": "proposal_fixture",
    }
    required_regression_gates = [
        {"gate": "multi_point_regression_matrix", "required": True},
        {"gate": "protected_sample_point_reviewed_3d_debug", "required": True},
        {"gate": "gameplay_gate_regression_baseline", "required": True},
        {
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "required": True,
        },
    ]
    required_operator_artifacts = [
        {"artifact": "human_approval_gate", "required": True},
        {"artifact": "operator_signoff_record", "required": True},
        {"artifact": "dry_run_review_packet", "required": True},
        {"artifact": "future_runtime_application_blueprint", "required": True},
    ]
    paths["application_plan"].write_text(
        json.dumps(
            {
                "application_plan_id": "application_plan_fixture",
                "application_plan_type": "controlled_runtime_calibration_application_plan",
                "application_plan_version": "v1",
                "generated_at": "2026-06-20T02:00:00+00:00",
                "source_application_plan_input_path": str(paths["application_plan"]),
                "source_human_approval_gate_path": str(paths["human_gate"]),
                "source_dry_run_review_packet_path": str(paths["review_packet"]),
                "source_dry_run_execution_report_path": str(paths["dry_run_report"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "proposed_candidate_settings": proposed_candidate_settings,
                "config_delta_proposal": {
                    "delta_status": "config_delta_proposed_for_future_blueprint",
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "pre_application_gate": {
                    "pre_application_gate_status": "pre_application_gates_defined",
                    "requirements": [],
                    "missing_requirements": [],
                    "blockers": [],
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                    "production_config_status": "not_created",
                    "baseline_update_status": "not_replaced",
                    "model_update_status": "not_modified",
                    "future_blueprint_required_for_runtime_application": True,
                },
                "rollback_plan": {
                    "rollback_status": "rollback_plan_defined",
                    "rollback_scope": {
                        "future_blueprint_only": True,
                        "runtime_application_status": "not_applied",
                        "mutation_status": "no_runtime_mutation",
                    },
                    "rollback_target_settings": current_settings,
                    "rollback_trigger_conditions": [
                        "operator requests rollback after separate future runtime application"
                    ],
                    "rollback_execution_steps_for_future_blueprint": [
                        "capture pre-application runtime settings"
                    ],
                    "rollback_verification_gates": required_regression_gates,
                    "rollback_artifact_refs": {
                        "source_application_plan_path": str(paths["application_plan"])
                    },
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "post_application_verification_plan": {
                    "verification_status": "post_application_verification_plan_defined",
                    "verification_scope": {
                        "separate_future_runtime_application_required": True,
                        "runtime_application_status": "not_applied",
                        "mutation_status": "no_runtime_mutation",
                    },
                    "required_regression_gates": required_regression_gates,
                    "required_replay_checks": [
                        "manifest-backed multi-point replay review"
                    ],
                    "required_review_packet_after_application": True,
                    "required_operator_review_after_application": True,
                    "required_rollback_readiness_check": True,
                    "future_baseline_candidate_conditions": [
                        "separate future runtime application exists"
                    ],
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "future_baseline_candidate_policy": {
                    "baseline_not_replaced_in_this_blueprint": True,
                    (
                        "future_baseline_candidate_may_be_considered_only_after_"
                        "runtime_application"
                    ): True,
                    "future_baseline_candidate_requires_post_application_review": True,
                    "future_baseline_candidate_requires_regression_gates": True,
                    "future_baseline_candidate_requires_human_review": True,
                    "future_baseline_candidate_not_truth": True,
                    "future_baseline_policy_status": (
                        "future_baseline_candidate_policy_defined"
                    ),
                    "baseline_update_status": "not_replaced",
                },
                "application_plan_status": "application_plan_created",
                "pre_application_gate_status": "pre_application_gates_defined",
                "rollback_plan_status": "rollback_plan_defined",
                "post_application_verification_status": (
                    "post_application_verification_plan_defined"
                ),
                "future_baseline_policy_status": (
                    "future_baseline_candidate_policy_defined"
                ),
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "future_blueprint_required_for_runtime_application": True,
                "required_regression_gates": required_regression_gates,
                "required_operator_artifacts": required_operator_artifacts,
                "blockers": [],
                "warnings": {"runtime_application_status_not_applied": True},
                "non_claims": {"application_plan_is_not_runtime_application": True},
            }
        ),
        encoding="utf-8",
    )
    source_payloads = {
        "human_gate": {
            "approval_gate_id": "human_gate_fixture",
            "approval_gate_type": "controlled_runtime_calibration_human_approval_gate",
        },
        "review_packet": {
            "review_packet_id": "review_packet_fixture",
            "review_packet_type": "controlled_runtime_calibration_dry_run_review_packet",
        },
        "dry_run_report": {
            "dry_run_id": "dry_run_fixture",
            "dry_run_type": "controlled_runtime_calibration_dry_run_execution",
        },
        "change_request": {
            "change_request_id": "change_request_fixture",
            "change_request_type": "controlled_runtime_calibration_change_request",
        },
        "candidate_config_freeze": {
            "candidate_config_freeze_id": "candidate_config_freeze_fixture",
            "candidate_config_freeze_type": "calibration_candidate_config_freeze",
        },
        "manual_packet": {
            "manual_approval_packet_id": "manual_packet_fixture",
            "manual_approval_packet_type": "calibration_candidate_manual_approval_packet",
        },
        "decision_packet": {"decision_packet_type": "calibration_candidate_decision_packet"},
        "phase_freeze": {"freeze_type": "real_broadcast_gameplay_calibration_freeze"},
        "gameplay_baseline": {"baseline_type": "gameplay_gate_regression_baseline"},
        "sandbox_baseline": {
            "baseline_type": "review_guided_gameplay_calibration_sandbox_baseline"
        },
    }
    for key, payload in source_payloads.items():
        paths[key].write_text(
            json.dumps(
                {
                    **payload,
                    "runtime_application_status": "not_applied",
                    "mutation_status": "no_runtime_mutation",
                    "warnings": {"classifier_correctness_not_assessed": True},
                }
            ),
            encoding="utf-8",
        )


def _build_staging_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    _build_staging_inputs_from_sources(paths)


def _build_staging_inputs_from_sources(paths: dict[str, Path]) -> None:
    build_controlled_runtime_calibration_runtime_application_staging_inputs(
        contract_path=paths["contract"],
        source_application_plan_path=paths["application_plan"],
        source_human_approval_gate_path=paths["human_gate"],
        source_dry_run_review_packet_path=paths["review_packet"],
        source_dry_run_execution_report_path=paths["dry_run_report"],
        source_change_request_path=paths["change_request"],
        source_candidate_config_freeze_path=paths["candidate_config_freeze"],
        source_manual_approval_packet_path=paths["manual_packet"],
        source_decision_packet_path=paths["decision_packet"],
        source_phase_freeze_path=paths["phase_freeze"],
        source_gameplay_gate_regression_baseline_path=paths["gameplay_baseline"],
        source_calibration_sandbox_baseline_path=paths["sandbox_baseline"],
        model_asset_path=paths["model_asset"],
        output_path=paths["staging_inputs"],
    )


def _build_staging(paths: dict[str, Path]) -> None:
    _build_staging_inputs(paths)
    build_controlled_runtime_calibration_runtime_application_staging(
        contract_path=paths["contract"],
        staging_inputs_path=paths["staging_inputs"],
        output_path=paths["staging"],
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            found.add(str(key))
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        found.add(value)
    return found
