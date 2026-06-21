from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_application_execution_review_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_TYPE,
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION,
    FORBIDDEN_REVIEW_PACKET_TOKENS,
    NON_CLAIMS,
    build_controlled_runtime_calibration_application_execution_review_packet,
    build_controlled_runtime_calibration_application_execution_review_packet_inputs,
    build_controlled_runtime_calibration_post_execution_blocker_report,
    build_controlled_runtime_calibration_post_execution_next_action_report,
    build_controlled_runtime_calibration_post_execution_operator_checklist,
    build_controlled_runtime_calibration_post_execution_summary,
    export_controlled_runtime_calibration_application_execution_review_packet_contract,
    validate_controlled_runtime_calibration_application_execution_review_packet,
    validate_controlled_runtime_calibration_application_execution_review_packet_inputs,
)


def test_export_application_execution_review_packet_contract_is_stable(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = (
        export_controlled_runtime_calibration_application_execution_review_packet_contract(
            output_path=paths["contract"],
            exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
        )
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["contract_type"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_TYPE
    )
    assert (
        result["contract_version"]
        == CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION
    )
    contract = _read(paths["contract"])
    assert contract["exported_at"] == "2026-06-21T00:00:00+00:00"
    assert contract["review_packet_scope"]["supports_blocked_execution_review"] is True
    assert contract["review_packet_scope"]["supports_controlled_application_review"] is True
    assert contract["review_packet_scope"]["does_not_write_runtime_config"] is True
    assert contract["review_packet_scope"]["does_not_create_production_config"] is True
    assert contract["review_packet_scope"]["does_not_modify_model_weights"] is True
    assert contract["review_packet_scope"]["does_not_replace_baselines"] is True
    assert contract["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(contract))


def test_current_bp62_blocked_execution_builds_review_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)

    inputs_result = (
        build_controlled_runtime_calibration_application_execution_review_packet_inputs(
            contract_path=paths["contract"],
            source_application_execution_path=(
                ".data/contracts/controlled_runtime_calibration_application_execution_v1.json"
            ),
            source_application_execution_contract_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_application_execution_contract_v1.json"
            ),
            source_runtime_config_artifact_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_applied_runtime_config_v1.json"
            ),
            source_rollback_package_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_application_rollback_package_v1.json"
            ),
            source_pre_application_final_gate_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_pre_application_final_gate_v1.json"
            ),
            source_runtime_application_staging_path=(
                ".data/contracts/"
                "controlled_runtime_calibration_runtime_application_staging_v1.json"
            ),
            source_application_plan_path=(
                ".data/contracts/controlled_runtime_calibration_application_plan_v1.json"
            ),
            source_human_approval_gate_path=(
                ".data/contracts/controlled_runtime_calibration_human_approval_gate_v1.json"
            ),
            source_dry_run_review_packet_path=(
                ".data/contracts/controlled_runtime_calibration_dry_run_review_packet_v1.json"
            ),
            source_dry_run_execution_report_path=(
                ".data/exports/controlled_runtime_calibration_dry_run_execution.current.json"
            ),
            source_change_request_path=(
                ".data/contracts/controlled_runtime_calibration_change_request_v1.json"
            ),
            source_candidate_config_freeze_path=(
                ".data/contracts/calibration_candidate_config_freeze_v1.json"
            ),
            source_manual_approval_packet_path=(
                ".data/exports/calibration_candidate_manual_approval_packet.current.json"
            ),
            source_decision_packet_path=(
                ".data/exports/calibration_candidate_decision_packet.current.json"
            ),
            source_phase_freeze_path=(
                ".data/contracts/"
                "real_broadcast_gameplay_calibration_decision_phase_freeze_v1.json"
            ),
            source_gameplay_gate_regression_baseline_path=(
                ".data/baselines/gameplay_gate_regression.baseline.json"
            ),
            source_calibration_sandbox_baseline_path=(
                ".data/baselines/"
                "review_guided_gameplay_calibration_sandbox.baseline.json"
            ),
            model_asset_path="model_assets/tom_v1/view_classifier_gameplay.pt",
            output_path=paths["inputs"],
            generated_at=datetime(2026, 6, 21, 1, 0, tzinfo=UTC),
        )
    )

    assert inputs_result["ok"] is True
    assert inputs_result["application_execution_status"] == (
        "application_blocked_final_gate_not_passed"
    )
    assert inputs_result["runtime_application_status"] == (
        "blocked_from_runtime_application"
    )
    assert inputs_result["runtime_config_status"] == "unchanged_due_to_blocker"
    assert inputs_result["mutation_status"] == "no_runtime_mutation_due_to_blocker"
    assert inputs_result["runtime_config_target_sha256_before"] == (
        inputs_result["runtime_config_target_sha256_after"]
    )

    inputs_validation = (
        validate_controlled_runtime_calibration_application_execution_review_packet_inputs(
            contract_path=paths["contract"],
            review_packet_inputs_path=paths["inputs"],
            output_path=paths["inputs_validation"],
            validated_at=datetime(2026, 6, 21, 1, 5, tzinfo=UTC),
        )
    )
    assert inputs_validation["ok"] is True
    assert inputs_validation["status"] == "valid"

    packet_result = build_controlled_runtime_calibration_application_execution_review_packet(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 2, 0, tzinfo=UTC),
    )

    assert packet_result["ok"] is True
    assert packet_result["review_packet_status"] == (
        "review_packet_created_for_blocked_execution"
    )
    assert packet_result["application_outcome_status"] == (
        "application_blocked_safely_before_runtime_mutation"
    )
    assert packet_result["runtime_config_changed"] is False
    assert packet_result["next_action_recommendation"] == (
        "resolve_operator_signoff_before_reapplying"
    )
    packet = _read(paths["packet"])
    assert packet["runtime_config_target_sha256_before"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["runtime_config_target_sha256_after"] == (
        "8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0"
    )
    assert packet["production_config_status"] == "not_created"
    assert packet["baseline_update_status"] == "not_replaced"
    assert packet["model_update_status"] == "not_modified"
    assert packet["atomic_write_status"] == "atomic_write_blocked"
    assert packet["runtime_readback_status"] == "readback_blocked"
    assert packet["rollback_summary"]["rollback_needed"] is False
    assert packet["rollback_summary"]["rollback_ready"] is True
    assert packet["verification_summary"]["verification_summary_status"] == (
        "verification_passed_for_blocked_execution"
    )
    assert packet["blocker_summary"]["operator_signoff_missing"] is True
    assert packet["blocker_summary"]["selected_candidate_missing"] is True
    assert "human_operator_approval_required" in packet["blocker_summary"]["blocker_types"]
    assert "no_candidate_selected" in packet["blocker_summary"]["blocker_types"]
    assert packet["non_claims"] == NON_CLAIMS
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(packet))

    packet_validation = (
        validate_controlled_runtime_calibration_application_execution_review_packet(
            contract_path=paths["contract"],
            review_packet_path=paths["packet"],
            output_path=paths["packet_validation"],
            validated_at=datetime(2026, 6, 21, 2, 5, tzinfo=UTC),
        )
    )
    assert packet_validation["ok"] is True
    assert packet_validation["status"] == "valid"
    assert packet_validation["review_packet_status"] == (
        "review_packet_created_for_blocked_execution"
    )

    _assert_post_execution_reports(paths)


def test_controlled_application_shaped_inputs_build_review_packet(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    _write_controlled_application_inputs(paths)

    result = build_controlled_runtime_calibration_application_execution_review_packet(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 3, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["review_packet_status"] == (
        "review_packet_created_for_controlled_application"
    )
    assert result["application_outcome_status"] == (
        "application_executed_controlled_runtime_config_write"
    )
    assert result["runtime_config_changed"] is True
    assert result["next_action_recommendation"] == (
        "proceed_to_post_application_review_after_controlled_apply"
    )
    packet = _read(paths["packet"])
    assert packet["runtime_application_status"] == "applied_by_controlled_blueprint"
    assert packet["runtime_config_status"] == "updated_by_controlled_application"
    assert packet["mutation_status"] == "controlled_runtime_config_mutation_performed"
    assert packet["rollback_summary"]["rollback_needed"] is True
    assert packet["rollback_summary"]["rollback_ready"] is True
    assert packet["verification_summary"]["verification_summary_status"] == (
        "verification_passed_for_controlled_application"
    )
    assert packet["production_config_status"] == "not_created"
    assert packet["baseline_update_status"] == "not_replaced"
    assert packet["model_update_status"] == "not_modified"
    assert not (FORBIDDEN_REVIEW_PACKET_TOKENS & _walk_exact_strings_and_keys(packet))


def test_review_packet_validation_rejects_forbidden_runtime_application_terms(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _export_contract(paths)
    _write_controlled_application_inputs(paths)
    build_controlled_runtime_calibration_application_execution_review_packet(
        contract_path=paths["contract"],
        review_packet_inputs_path=paths["inputs"],
        output_path=paths["packet"],
        generated_at=datetime(2026, 6, 21, 4, 0, tzinfo=UTC),
    )
    packet = _read(paths["packet"])
    packet["uncontrolled" + "_runtime_config_update"] = True
    _write(paths["packet"], packet)

    validation = validate_controlled_runtime_calibration_application_execution_review_packet(
        contract_path=paths["contract"],
        review_packet_path=paths["packet"],
        output_path=paths["packet_validation"],
        validated_at=datetime(2026, 6, 21, 4, 5, tzinfo=UTC),
    )

    assert validation["ok"] is False
    assert validation["status"] == "invalid"
    assert any(error["code"] == "forbidden_key" for error in validation["errors"])


def _assert_post_execution_reports(paths: dict[str, Path]) -> None:
    summary = build_controlled_runtime_calibration_post_execution_summary(
        contract_path=paths["contract"],
        review_packet_path=paths["packet"],
        output_path=paths["summary"],
        generated_at=datetime(2026, 6, 21, 2, 10, tzinfo=UTC),
    )
    assert summary["ok"] is True
    assert summary["application_outcome_status"] == (
        "application_blocked_safely_before_runtime_mutation"
    )
    assert summary["runtime_config_changed"] is False

    blocker = build_controlled_runtime_calibration_post_execution_blocker_report(
        contract_path=paths["contract"],
        review_packet_path=paths["packet"],
        output_path=paths["blocker"],
        generated_at=datetime(2026, 6, 21, 2, 15, tzinfo=UTC),
    )
    assert blocker["ok"] is True
    assert blocker["blocked_reason_count"] >= 1

    checklist = build_controlled_runtime_calibration_post_execution_operator_checklist(
        contract_path=paths["contract"],
        review_packet_path=paths["packet"],
        output_path=paths["checklist"],
        generated_at=datetime(2026, 6, 21, 2, 20, tzinfo=UTC),
    )
    assert checklist["ok"] is True
    assert checklist["check_count"] == 14

    next_action = build_controlled_runtime_calibration_post_execution_next_action_report(
        contract_path=paths["contract"],
        review_packet_path=paths["packet"],
        output_path=paths["next_action"],
        generated_at=datetime(2026, 6, 21, 2, 25, tzinfo=UTC),
    )
    assert next_action["ok"] is True
    assert next_action["next_action_recommendation"] == (
        "resolve_operator_signoff_before_reapplying"
    )


def _export_contract(paths: dict[str, Path]) -> None:
    result = (
        export_controlled_runtime_calibration_application_execution_review_packet_contract(
            output_path=paths["contract"],
            exported_at=datetime(2026, 6, 21, 0, 0, tzinfo=UTC),
        )
    )
    assert result["ok"] is True


def _write_controlled_application_inputs(paths: dict[str, Path]) -> None:
    paths["model_asset"].write_bytes(b"model fixture")
    payload = {
        "review_packet_input_id": "review_packet_inputs_fixture",
        "review_packet_input_type": (
            "controlled_runtime_calibration_application_execution_review_packet_inputs"
        ),
        "review_packet_input_version": "v1",
        "generated_at": "2026-06-21T03:00:00+00:00",
        "source_application_execution_path": "execution_fixture.json",
        "source_application_execution_contract_path": "execution_contract_fixture.json",
        "source_runtime_config_artifact_path": "runtime_config_fixture.json",
        "source_rollback_package_path": "rollback_package_fixture.json",
        "source_pre_application_final_gate_path": "final_gate_fixture.json",
        "source_runtime_application_staging_path": "staging_fixture.json",
        "source_application_plan_path": "application_plan_fixture.json",
        "source_human_approval_gate_path": "human_gate_fixture.json",
        "source_dry_run_review_packet_path": "dry_run_review_fixture.json",
        "source_dry_run_execution_report_path": "dry_run_execution_fixture.json",
        "source_change_request_path": "change_request_fixture.json",
        "source_candidate_config_freeze_path": "candidate_freeze_fixture.json",
        "source_manual_approval_packet_path": "manual_packet_fixture.json",
        "source_decision_packet_path": "decision_packet_fixture.json",
        "source_phase_freeze_path": "phase_freeze_fixture.json",
        "source_gameplay_gate_regression_baseline_path": "gameplay_baseline_fixture.json",
        "source_calibration_sandbox_baseline_path": "sandbox_baseline_fixture.json",
        "model_asset_ref": str(paths["model_asset"]),
        "model_asset_sha256": _sha256(b"model fixture"),
        "runtime_config_target_ref": {"path": "runtime_config_fixture.json"},
        "runtime_config_target_sha256_before": "a" * 64,
        "runtime_config_target_sha256_after": "b" * 64,
        "application_execution_status": (
            "application_executed_controlled_runtime_config_write"
        ),
        "runtime_application_status": "applied_by_controlled_blueprint",
        "runtime_config_status": "updated_by_controlled_application",
        "mutation_status": "controlled_runtime_config_mutation_performed",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "atomic_write_status": "atomic_write_completed",
        "runtime_readback_status": "readback_verified",
        "rollback_package_status": "rollback_package_created",
        "post_apply_verification_status": "post_apply_verification_passed",
        "source_application_execution_id": "application_execution_fixture",
        "source_pre_application_final_gate_status": "final_gate_passed_not_applied",
        "selected_candidate_config_ref": {"candidate_setting_id": "candidate_fixture"},
        "operator_signoff_ref": {"operator_signoff_status": "operator_signoff_recorded"},
        "application_execution_blockers": [],
        "final_gate_blockers": [],
        "applied_config_delta": {
            "delta_applied": [{"field": "threshold", "change_applied": True}]
        },
        "post_apply_verification_report": {
            "multi_point_regression_gate_result": {"drift_detected": False},
            "protected_sample_point_gate_result": {"drift_detected": False},
            "gameplay_gate_regression_baseline_result": {"drift_detected": False},
            "calibration_sandbox_regression_baseline_result": {
                "drift_detected": False
            },
            "runtime_readback_result": {
                "runtime_readback_status": "readback_verified"
            },
            "baseline_replacement_check": {
                "status": "not_replaced",
                "baseline_not_replaced": True,
            },
            "production_config_check": {
                "status": "not_created",
                "production_config_not_created": True,
            },
        },
        "rollback_package_ref": {"rollback_package_id": "rollback_fixture"},
        "rollback_package": {
            "rollback_status": "rollback_package_created",
            "rollback_verification_gates": [{"gate": "runtime_readback"}],
        },
        "warnings": {},
        "non_claims": dict(NON_CLAIMS),
    }
    _write(paths["inputs"], payload)


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "contract": tmp_path / "contract.json",
        "inputs": tmp_path / "inputs.json",
        "inputs_validation": tmp_path / "inputs.validation.json",
        "packet": tmp_path / "packet.json",
        "packet_validation": tmp_path / "packet.validation.json",
        "summary": tmp_path / "summary.json",
        "blocker": tmp_path / "blocker.json",
        "checklist": tmp_path / "checklist.json",
        "next_action": tmp_path / "next_action.json",
        "model_asset": tmp_path / "view_classifier_gameplay.pt",
    }


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    exact: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            exact.add(str(key))
            exact.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, list):
        for child in value:
            exact.update(_walk_exact_strings_and_keys(child))
    elif isinstance(value, str):
        exact.add(value)
    return exact
