from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.real_broadcast_gameplay_calibration_decision_phase_freeze import (
    FORBIDDEN_PHASE_FREEZE_CLAIMS,
    FROZEN_CONTRACT_REFS,
    NON_CLAIMS,
    PROTECTED_BASELINE_REFS,
    REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE,
    REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION,
    REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_TYPE,
    build_real_broadcast_gameplay_calibration_decision_phase_freeze,
    build_real_broadcast_gameplay_calibration_next_phase_readiness_report,
    validate_real_broadcast_gameplay_calibration_decision_phase_freeze,
)


def test_build_real_broadcast_gameplay_calibration_decision_phase_freeze(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_source_artifacts(paths)

    result = build_real_broadcast_gameplay_calibration_decision_phase_freeze(
        candidate_config_freeze_path=paths["candidate_config_freeze"],
        manual_approval_packet_path=paths["manual_approval_packet"],
        output_path=paths["freeze"],
        current_main_commit="133ddb23bdcdcb9eba153711f503cf95c0d87e94",
        generated_at=datetime(2026, 6, 20, 4, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["freeze_type"]
        == REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_TYPE
    )
    assert (
        result["freeze_version"]
        == REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION
    )

    freeze = json.loads(paths["freeze"].read_text(encoding="utf-8"))
    assert freeze["generated_at"] == "2026-06-20T04:00:00+00:00"
    assert freeze["latest_completed_blueprint"]["blueprint"] == "blueprint_53"
    assert len(freeze["completed_phase_blueprints"]) == 8
    assert {item["path"] for item in freeze["frozen_contract_refs"]} == set(
        FROZEN_CONTRACT_REFS
    )
    assert {item["path"] for item in freeze["protected_baseline_refs"]} == {
        item["path"] for item in PROTECTED_BASELINE_REFS
    }
    assert (
        freeze["decision_support_summary"]["candidate_settings_remain_not_applied"]
        is True
    )
    assert (
        freeze["decision_support_summary"]["runtime_application_supported_in_this_phase"]
        is False
    )
    assert freeze["manual_approval_summary"]["approval_required"] is True
    assert freeze["manual_approval_summary"]["runtime_application_status"] == "not_applied"
    assert (
        freeze["manual_approval_summary"]["automatic_approval_occurred"] is False
    )
    assert (
        freeze["manual_approval_summary"]["automatic_rejection_occurred"] is False
    )
    assert (
        freeze["manual_approval_summary"]["deployable_runtime_configuration_created"]
        is False
    )
    assert freeze["non_claims"] == NON_CLAIMS
    assert (
        freeze["next_phase_recommendations"][0]["recommended_blueprint"]
        == "Blueprint 55 - Controlled Runtime Calibration Change Request v1"
    )
    assert (
        freeze["next_phase_recommendations"][0]["implementation_in_blueprint_54"]
        is False
    )
    assert not (FORBIDDEN_PHASE_FREEZE_CLAIMS & _walk_exact_strings_and_keys(freeze))


def test_validate_real_broadcast_gameplay_calibration_decision_phase_freeze(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_source_artifacts(paths)
    build_real_broadcast_gameplay_calibration_decision_phase_freeze(
        candidate_config_freeze_path=paths["candidate_config_freeze"],
        manual_approval_packet_path=paths["manual_approval_packet"],
        output_path=paths["freeze"],
        current_main_commit="133ddb23bdcdcb9eba153711f503cf95c0d87e94",
    )

    result = validate_real_broadcast_gameplay_calibration_decision_phase_freeze(
        freeze_path=paths["freeze"],
        output_path=paths["validation"],
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert len(result["frozen_contract_validations"]) == len(FROZEN_CONTRACT_REFS)
    assert all(item["ok"] for item in result["frozen_contract_validations"])
    assert len(result["protected_baseline_validations"]) == len(PROTECTED_BASELINE_REFS)
    assert all(item["ok"] for item in result["protected_baseline_validations"])
    assert result["tracked_exports"] == []
    assert result["gameplay_classifier_asset_validation"]["worktree_clean"] is True
    assert result["gameplay_classifier_asset_validation"]["index_clean"] is True


def test_build_real_broadcast_gameplay_calibration_next_phase_readiness_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    _write_source_artifacts(paths)
    build_real_broadcast_gameplay_calibration_decision_phase_freeze(
        candidate_config_freeze_path=paths["candidate_config_freeze"],
        manual_approval_packet_path=paths["manual_approval_packet"],
        output_path=paths["freeze"],
    )

    result = build_real_broadcast_gameplay_calibration_next_phase_readiness_report(
        freeze_path=paths["freeze"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 20, 5, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert (
        result["report_type"]
        == REAL_BROADCAST_GAMEPLAY_CALIBRATION_NEXT_PHASE_READINESS_REPORT_TYPE
    )
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-20T05:00:00+00:00"
    assert report["summary"]["completed_phase_blueprint_count"] == 8
    assert report["summary"]["frozen_contract_ref_count"] == len(FROZEN_CONTRACT_REFS)
    assert report["readiness_assessment"]["ready_for_blueprint_55_change_request_design"]
    assert report["readiness_assessment"]["ready_for_direct_runtime_mutation"] is False
    assert report["readiness_assessment"]["does_not_implement_blueprint_55"] is True


def test_phase_freeze_validation_rejects_forbidden_claims(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _write_source_artifacts(paths)
    build_real_broadcast_gameplay_calibration_decision_phase_freeze(
        candidate_config_freeze_path=paths["candidate_config_freeze"],
        manual_approval_packet_path=paths["manual_approval_packet"],
        output_path=paths["freeze"],
    )
    freeze = json.loads(paths["freeze"].read_text(encoding="utf-8"))
    freeze["validation_summary"]["bad_claim"] = "true_gameplay"
    paths["freeze"].write_text(json.dumps(freeze), encoding="utf-8")

    result = validate_real_broadcast_gameplay_calibration_decision_phase_freeze(
        freeze_path=paths["freeze"],
        output_path=paths["validation"],
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(
        error["error_type"] == "forbidden_claim_value" for error in result["errors"]
    )


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "candidate_config_freeze": tmp_path / "candidate_config_freeze.json",
        "manual_approval_packet": tmp_path / "manual_approval_packet.json",
        "freeze": tmp_path / "phase_freeze.json",
        "validation": tmp_path / "phase_freeze.validation.json",
        "report": tmp_path / "next_phase_readiness_report.json",
    }


def _write_source_artifacts(paths: dict[str, Path]) -> None:
    paths["candidate_config_freeze"].write_text(
        json.dumps(
            {
                "candidate_config_freeze_id": "candidate_config_freeze_fixture",
                "candidate_config_status": "frozen_for_manual_review",
                "approval_required": True,
                "approval_blockers": ["missing_operator_review"],
                "runtime_application_status": "not_applied",
                "not_applied": True,
                "review_coverage_summary": {
                    "ready_for_human_decision_count": 1,
                    "operator_review_required_count": 1,
                },
                "regression_gate_summary": {
                    "status": "completed",
                    "drift_detected": False,
                    "breaking_drift_detected": False,
                    "runtime_application_status": "not_applied",
                },
                "required_preconditions": [
                    "reviewed_candidate_packet",
                    "confirmed_no_runtime_application",
                    "confirmed_model_weights_unchanged",
                    "confirmed_baselines_unchanged",
                    "confirmed_human_approval_required",
                ],
            }
        ),
        encoding="utf-8",
    )
    paths["manual_approval_packet"].write_text(
        json.dumps(
            {
                "manual_approval_packet_id": "manual_approval_packet_fixture",
                "approval_required": True,
                "runtime_application_status": "not_applied",
                "operator_checklist": [
                    {"checklist_item": "reviewed_candidate_packet"},
                    {"checklist_item": "confirmed_no_runtime_application"},
                ],
            }
        ),
        encoding="utf-8",
    )


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
