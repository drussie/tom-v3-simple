from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_pre_application_final_gate import (
    CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION,
    CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_TYPE,
    FORBIDDEN_FINAL_GATE_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_final_gate_artifact_checklist,
    build_controlled_runtime_calibration_final_gate_blocker_report,
    build_controlled_runtime_calibration_final_gate_readiness_report,
    build_controlled_runtime_calibration_final_gate_regression_checklist,
    build_controlled_runtime_calibration_pre_application_final_gate,
    build_controlled_runtime_calibration_pre_application_final_gate_inputs,
    export_controlled_runtime_calibration_pre_application_final_gate_contract,
    validate_controlled_runtime_calibration_pre_application_final_gate,
    validate_controlled_runtime_calibration_pre_application_final_gate_inputs,
)


def test_export_controlled_runtime_calibration_pre_application_final_gate_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = export_controlled_runtime_calibration_pre_application_final_gate_contract(
        output_path=paths["contract"],
        exported_at=datetime(2026, 6, 20, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION
    )
    contract = json.loads(paths["contract"].read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-20T00:00:00+00:00"
    assert contract["final_gate_scope"]["creates_readiness_verdict_for_future_blueprint"]
    assert contract["final_gate_scope"]["runtime_application_supported_in_this_blueprint"] is False
    assert contract["final_gate_scope"]["updates_runtime_configuration"] is False
    assert contract["final_gate_scope"]["creates_production_configuration"] is False
    assert contract["final_gate_scope"]["updates_model_weights"] is False
    assert contract["final_gate_scope"]["replaces_regression_baselines"] is False
    assert (
        contract["final_gate_artifact_schema"]["required_runtime_config_status"]
        == "not_updated"
    )
    assert contract["warnings"]["controlled_pre_application_final_gate"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_TOKENS & _walk_exact_strings_and_keys(contract))


def test_build_and_validate_controlled_runtime_calibration_pre_application_final_gate_inputs(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)

    result = build_controlled_runtime_calibration_pre_application_final_gate_inputs(
        contract_path=paths["contract"],
        source_runtime_application_staging_path=paths["staging"],
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
        output_path=paths["final_gate_inputs"],
        generated_at=datetime(2026, 6, 20, 1, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    inputs = json.loads(paths["final_gate_inputs"].read_text(encoding="utf-8"))
    assert inputs["generated_at"] == "2026-06-20T01:00:00+00:00"
    assert inputs["model_asset_sha256"] == _sha256(b"model fixture")
    assert inputs["staged_config_delta_ref"]["delta_status"] == (
        "staged_for_future_blueprint"
    )
    assert inputs["operator_signoff_ref"]["operator_signoff_artifact_present"] is True
    assert inputs["source_artifact_presence"]["manual_approval_packet"]["present"] is True
    assert inputs["blockers"] == []
    assert inputs["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_TOKENS & _walk_exact_strings_and_keys(inputs))

    validation = validate_controlled_runtime_calibration_pre_application_final_gate_inputs(
        contract_path=paths["contract"],
        final_gate_inputs_path=paths["final_gate_inputs"],
        output_path=paths["final_gate_inputs_validation"],
        validated_at=datetime(2026, 6, 20, 1, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["status"] == "valid"
    assert validation["error_count"] == 0


def test_build_and_validate_controlled_runtime_calibration_pre_application_final_gate(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_final_gate_inputs(paths)

    result = build_controlled_runtime_calibration_pre_application_final_gate(
        contract_path=paths["contract"],
        final_gate_inputs_path=paths["final_gate_inputs"],
        output_path=paths["final_gate"],
        generated_at=datetime(2026, 6, 20, 2, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["final_gate_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_TYPE
    )
    assert result["final_gate_status"] == "final_gate_passed_not_applied"
    assert (
        result["readiness_status"]
        == "ready_with_warnings_for_future_runtime_application_blueprint"
    )
    assert result["runtime_application_status"] == "final_gate_passed_not_applied"
    assert result["mutation_status"] == "no_runtime_mutation"
    assert result["runtime_config_status"] == "not_updated"
    assert result["production_config_status"] == "not_created"
    assert result["baseline_update_status"] == "not_replaced"
    assert result["model_update_status"] == "not_modified"
    assert result["future_blueprint_required_for_runtime_application"] is True

    final_gate = json.loads(paths["final_gate"].read_text(encoding="utf-8"))
    assert final_gate["generated_at"] == "2026-06-20T02:00:00+00:00"
    assert final_gate["artifact_checklist_status"] == "all_required_artifacts_present"
    assert final_gate["regression_checklist_status"] == (
        "all_required_regression_gate_refs_present"
    )
    assert final_gate["rollback_readiness_status"] == (
        "rollback_ready_for_future_application_blueprint"
    )
    assert final_gate["post_application_verification_readiness_status"] == (
        "post_application_verification_plan_ready"
    )
    assert final_gate["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_FINAL_GATE_TOKENS & _walk_exact_strings_and_keys(final_gate))

    validation = validate_controlled_runtime_calibration_pre_application_final_gate(
        contract_path=paths["contract"],
        final_gate_path=paths["final_gate"],
        output_path=paths["final_gate_validation"],
        validated_at=datetime(2026, 6, 20, 2, 5, tzinfo=UTC),
    )
    assert validation["ok"] is True
    assert validation["error_count"] == 0
    assert validation["runtime_application_status"] == "final_gate_passed_not_applied"
    assert validation["mutation_status"] == "no_runtime_mutation"
    assert validation["future_blueprint_required_for_runtime_application"] is True


def test_pre_application_final_gate_blocks_missing_selected_candidate(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_sources(paths)
    staging = json.loads(paths["staging"].read_text(encoding="utf-8"))
    staging["selected_candidate_config_ref"] = {
        "candidate_packet_id": None,
        "candidate_setting_id": None,
        "source_proposal_item_id": None,
    }
    staging["staged_candidate_settings"] = {
        "staged_candidate_threshold": None,
        "staged_candidate_smoothing_window": None,
        "staged_candidate_hysteresis_settings": {},
        "candidate_type": "not_applicable",
        "candidate_source": {},
        "staged_not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }
    staging["blockers"] = ["no_candidate_selected"]
    paths["staging"].write_text(json.dumps(staging), encoding="utf-8")
    _build_final_gate_inputs_from_sources(paths)

    result = build_controlled_runtime_calibration_pre_application_final_gate(
        contract_path=paths["contract"],
        final_gate_inputs_path=paths["final_gate_inputs"],
        output_path=paths["final_gate"],
        generated_at=datetime(2026, 6, 20, 2, 30, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["final_gate_status"] == "final_gate_blocked_missing_candidate_config"
    assert result["runtime_application_status"] == "blocked_from_runtime_application"
    final_gate = json.loads(paths["final_gate"].read_text(encoding="utf-8"))
    assert "no_candidate_selected" in final_gate["blockers"]
    assert final_gate["mutation_status"] == "no_runtime_mutation"
    assert final_gate["runtime_config_status"] == "not_updated"


def test_build_pre_application_final_gate_reports(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _build_final_gate(paths)

    readiness_result = build_controlled_runtime_calibration_final_gate_readiness_report(
        contract_path=paths["contract"],
        final_gate_path=paths["final_gate"],
        output_path=paths["readiness_report"],
        generated_at=datetime(2026, 6, 20, 3, 0, tzinfo=UTC),
    )
    assert readiness_result["ok"] is True
    readiness = json.loads(paths["readiness_report"].read_text(encoding="utf-8"))
    assert readiness["runtime_application_status"] == "final_gate_passed_not_applied"

    blocker_result = build_controlled_runtime_calibration_final_gate_blocker_report(
        contract_path=paths["contract"],
        final_gate_path=paths["final_gate"],
        output_path=paths["blocker_report"],
        generated_at=datetime(2026, 6, 20, 3, 5, tzinfo=UTC),
    )
    assert blocker_result["ok"] is True
    blocker = json.loads(paths["blocker_report"].read_text(encoding="utf-8"))
    assert blocker["blocker_status"] == "no_unresolved_blockers_reported"

    artifact_result = build_controlled_runtime_calibration_final_gate_artifact_checklist(
        contract_path=paths["contract"],
        final_gate_path=paths["final_gate"],
        output_path=paths["artifact_checklist"],
        generated_at=datetime(2026, 6, 20, 3, 10, tzinfo=UTC),
    )
    assert artifact_result["ok"] is True
    artifact = json.loads(paths["artifact_checklist"].read_text(encoding="utf-8"))
    assert artifact["artifact_checklist_status"] == "all_required_artifacts_present"

    regression_result = (
        build_controlled_runtime_calibration_final_gate_regression_checklist(
            contract_path=paths["contract"],
            final_gate_path=paths["final_gate"],
            output_path=paths["regression_checklist"],
            generated_at=datetime(2026, 6, 20, 3, 15, tzinfo=UTC),
        )
    )
    assert regression_result["ok"] is True
    regression = json.loads(paths["regression_checklist"].read_text(encoding="utf-8"))
    assert regression["regression_checklist_status"] == (
        "all_required_regression_gate_refs_present"
    )


def test_pre_application_final_gate_validation_rejects_forbidden_runtime_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _build_final_gate(paths)
    final_gate = json.loads(paths["final_gate"].read_text(encoding="utf-8"))
    final_gate["runtime_application_performed"] = True
    paths["final_gate"].write_text(json.dumps(final_gate), encoding="utf-8")

    result = validate_controlled_runtime_calibration_pre_application_final_gate(
        contract_path=paths["contract"],
        final_gate_path=paths["final_gate"],
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
        "staging": tmp_path / "staging.json",
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
        "final_gate_inputs": tmp_path / "final_gate_inputs.json",
        "final_gate_inputs_validation": tmp_path / "final_gate_inputs.validation.json",
        "final_gate": tmp_path / "final_gate.json",
        "final_gate_validation": tmp_path / "final_gate.validation.json",
        "readiness_report": tmp_path / "readiness_report.json",
        "blocker_report": tmp_path / "blocker_report.json",
        "artifact_checklist": tmp_path / "artifact_checklist.json",
        "regression_checklist": tmp_path / "regression_checklist.json",
    }


def _write_sources(paths: dict[str, Path]) -> None:
    export_controlled_runtime_calibration_pre_application_final_gate_contract(
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
    selected_candidate_config_ref = {
        "candidate_packet_id": "candidate_fixture",
        "candidate_setting_id": "candidate_setting_fixture",
        "source_proposal_item_id": "proposal_fixture",
    }
    staged_candidate_settings = {
        "staged_candidate_threshold": 0.58,
        "staged_candidate_smoothing_window": 5,
        "staged_candidate_hysteresis_settings": {
            "enter_gameplay_probability": 0.62,
            "exit_gameplay_probability": 0.43,
        },
        "candidate_type": "threshold_candidate",
        "candidate_source": {"candidate_packet_id": "candidate_fixture"},
        "staged_not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
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
    staged_config_delta = {
        "staged_config_delta_id": "staged_delta_fixture",
        "staged_config_delta_type": "controlled_runtime_calibration_staged_config_delta",
        "staged_config_delta_version": "v1",
        "delta_status": "staged_for_future_blueprint",
        "delta_fields": [
            {
                "field": "threshold",
                "current_value": 0.55,
                "staged_value": 0.58,
                "change_present": True,
                "runtime_application_status": "staged_not_applied",
                "mutation_status": "no_runtime_mutation",
                "runtime_config_status": "not_updated",
            }
        ],
        "runtime_application_status": "staged_not_applied",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "mutation_status": "no_runtime_mutation",
    }
    paths["staging"].write_text(
        json.dumps(
            {
                "staging_id": "staging_fixture",
                "staging_type": "controlled_runtime_calibration_runtime_application_staging",
                "staging_version": "v1",
                "generated_at": "2026-06-20T00:30:00+00:00",
                "source_application_plan_path": str(paths["application_plan"]),
                "source_human_approval_gate_path": str(paths["human_gate"]),
                "source_dry_run_review_packet_path": str(paths["review_packet"]),
                "source_dry_run_execution_report_path": str(paths["dry_run_report"]),
                "source_change_request_path": str(paths["change_request"]),
                "selected_candidate_config_ref": selected_candidate_config_ref,
                "model_asset_ref": str(paths["model_asset"]),
                "model_asset_sha256": _sha256(b"model fixture"),
                "current_settings": current_settings,
                "staged_candidate_settings": staged_candidate_settings,
                "staged_config_delta": staged_config_delta,
                "pre_apply_manifest": {
                    "pre_apply_manifest_id": "pre_apply_manifest_fixture",
                    "pre_apply_manifest_version": "v1",
                    "manifest_status": "pre_apply_manifest_defined",
                    "missing_requirements": [],
                    "required_artifacts": [],
                    "required_operator_artifacts": required_operator_artifacts,
                    "required_regression_gates": required_regression_gates,
                    "blockers": [],
                    "runtime_application_status": "staged_not_applied",
                    "runtime_config_status": "not_updated",
                    "production_config_status": "not_created",
                    "baseline_update_status": "not_replaced",
                    "mutation_status": "no_runtime_mutation",
                },
                "rollback_staging_record": {
                    "rollback_staging_id": "rollback_fixture",
                    "rollback_staging_version": "v1",
                    "rollback_staging_status": "rollback_staging_record_defined",
                    "runtime_application_status": "staged_not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "post_application_verification_staging_record": {
                    "post_application_verification_staging_id": "verification_fixture",
                    "post_application_verification_staging_version": "v1",
                    "verification_staging_status": "post_application_verification_staged",
                    "runtime_application_status": "staged_not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "future_baseline_candidate_staging_policy": {
                    "future_baseline_policy_status": (
                        "future_baseline_candidate_staging_policy_defined"
                    ),
                    "future_baseline_candidate_not_created_in_this_blueprint": True,
                    "future_baseline_candidate_requires_post_application_review": True,
                    "baseline_update_status": "not_replaced",
                    "runtime_application_status": "staged_not_applied",
                    "mutation_status": "no_runtime_mutation",
                },
                "required_regression_gates": required_regression_gates,
                "required_operator_artifacts": required_operator_artifacts,
                "blockers": [],
                "runtime_application_status": "staged_not_applied",
                "runtime_config_status": "not_updated",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "mutation_status": "no_runtime_mutation",
                "future_blueprint_required_for_runtime_application": True,
                "warnings": {"runtime_application_status_staged_not_applied": True},
                "non_claims": {"staging_artifact_is_not_runtime_application": True},
            }
        ),
        encoding="utf-8",
    )
    source_payloads = {
        "application_plan": {
            "application_plan_id": "application_plan_fixture",
            "application_plan_type": "controlled_runtime_calibration_application_plan",
            "selected_candidate_config_ref": selected_candidate_config_ref,
            "current_settings": current_settings,
        },
        "human_gate": {
            "approval_gate_id": "human_gate_fixture",
            "approval_gate_type": "controlled_runtime_calibration_human_approval_gate",
            "operator_signoff_status": "operator_signoff_recorded",
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
        "decision_packet": {
            "decision_packet_id": "decision_packet_fixture",
            "decision_packet_type": "calibration_candidate_decision_packet",
        },
        "phase_freeze": {
            "phase_freeze_id": "phase_freeze_fixture",
            "freeze_type": "real_broadcast_gameplay_calibration_freeze",
        },
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


def _build_final_gate_inputs(paths: dict[str, Path]) -> None:
    _write_sources(paths)
    _build_final_gate_inputs_from_sources(paths)


def _build_final_gate_inputs_from_sources(paths: dict[str, Path]) -> None:
    build_controlled_runtime_calibration_pre_application_final_gate_inputs(
        contract_path=paths["contract"],
        source_runtime_application_staging_path=paths["staging"],
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
        output_path=paths["final_gate_inputs"],
    )


def _build_final_gate(paths: dict[str, Path]) -> None:
    _build_final_gate_inputs(paths)
    build_controlled_runtime_calibration_pre_application_final_gate(
        contract_path=paths["contract"],
        final_gate_inputs_path=paths["final_gate_inputs"],
        output_path=paths["final_gate"],
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
