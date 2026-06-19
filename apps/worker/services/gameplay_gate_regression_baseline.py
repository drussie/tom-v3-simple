from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gated_many_point_smoke import (
    DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
    GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION,
    build_gameplay_gated_many_point_smoke_manifest_template,
    run_gameplay_gated_many_point_smoke,
)
from apps.worker.services.gameplay_gated_perception_execution import (
    DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT,
    GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_gated_pipeline_routing import (
    DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
)
from apps.worker.services.gameplay_segment_replay_review import (
    DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
    GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION,
)
from apps.worker.services.many_point_ingestion_gate import (
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)

GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE = "gameplay_gate_regression_baseline_contract"
GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION = "v1"
GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE = "gameplay_gate_regression_baseline"
GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION = "v1"
GAMEPLAY_GATE_REGRESSION_VERIFICATION_TYPE = "gameplay_gate_regression_verification"
GAMEPLAY_GATE_REGRESSION_REPORT_TYPE = "gameplay_gate_regression_report"
GAMEPLAY_GATE_REGRESSION_BLUEPRINT = "blueprint_43"
GAMEPLAY_GATE_REGRESSION_BLUEPRINT_NAME = "gameplay_gate_regression_baseline_v1"

DEFAULT_GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_gate_regression_baseline_contract_v1.json"
)
DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT = (
    ".data/baselines/gameplay_gate_regression.baseline.json"
)
DEFAULT_GAMEPLAY_GATE_REGRESSION_CURRENT_OUTPUT = (
    ".data/exports/gameplay_gate_regression.current.json"
)
DEFAULT_GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT = (
    ".data/exports/gameplay_gate_regression.verification.json"
)
DEFAULT_GAMEPLAY_GATE_REGRESSION_REPORT_OUTPUT = (
    ".data/exports/gameplay_gate_regression.report.json"
)
DEFAULT_GAMEPLAY_GATE_REGRESSION_WORK_DIR = ".data/exports/gameplay_gate_regression"
DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH = "demo_assets/sample_point.mp4"
DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_SOURCE_LABEL = "gameplay_gate_regression_fixture"

GAMEPLAY_GATE_REGRESSION_EXPORTED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)
GAMEPLAY_GATE_REGRESSION_BASELINE_GENERATED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)

ALLOWED_VERIFICATION_STATUSES = {
    "baseline_invalid",
    "baseline_missing",
    "breaking_drift_detected",
    "completed",
    "current_output_invalid",
    "drift_detected",
    "verification_failed",
}
ALLOWED_DRIFT_SEVERITIES = {"info", "warning", "breaking"}

FORBIDDEN_REGRESSION_TOKENS = {
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
}

REGRESSION_WARNINGS = {
    "baseline_is_not_truth": True,
    "gameplay_gate_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "generalization_not_claimed": True,
    "regression_protection_only": True,
    "structural_outputs_only": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_mutate_model_assets": True,
    "does_not_mutate_regression_baselines_except_this_baseline": True,
    "no_adjudication": True,
    "observation_only": True,
}

NON_CLAIMS = {
    "not_classifier_accuracy_benchmark": True,
    "not_point_detection": True,
    "not_scoring": True,
    "not_line_calling": True,
    "not_generalization_claim": True,
    "not_production_readiness_claim": True,
    "not_training_label_source": True,
}

SOURCE_CONTRACT_REFS = {
    "gameplay_segment_gate_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
    "gameplay_gated_pipeline_routing_contract_version": (
        GAMEPLAY_GATED_ROUTING_CONTRACT_VERSION
    ),
    "gameplay_gated_perception_execution_contract_version": (
        GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_VERSION
    ),
    "gameplay_segment_replay_review_contract_version": (
        GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_VERSION
    ),
    "gameplay_gated_many_point_smoke_contract_version": (
        GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_VERSION
    ),
    "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
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


def export_gameplay_gate_regression_baseline_contract(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or GAMEPLAY_GATE_REGRESSION_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
        "baseline_type": GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE,
        "baseline_version": GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION,
        "contract": contract,
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_gameplay_gate_regression_baseline(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
    smoke_manifest_path: str | Path | None = None,
    work_dir: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_WORK_DIR,
    fixture_media_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    generated_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or GAMEPLAY_GATE_REGRESSION_BASELINE_GENERATED_AT
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_build("baseline_invalid", errors, output_path)
    current = _build_current_summary(
        smoke_manifest_path=smoke_manifest_path,
        work_dir=work_dir,
        fixture_media_path=fixture_media_path,
        model_asset_path=model_asset_path,
        generated_at=generated_at,
        probe_runner=probe_runner,
    )
    if current.get("ok") is False:
        return _failed_build("current_output_invalid", _list(current.get("errors")), output_path)
    baseline = _baseline_from_current(
        current=_dict(current.get("current")),
        generated_at=generated_at,
    )
    result = {
        "ok": True,
        "status": "completed",
        "baseline_type": GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE,
        "baseline_version": GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION,
        "baseline_id": baseline["baseline_id"],
        "baseline": baseline,
        "summary": baseline["summary"],
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, baseline, result, "baseline_output")
    return result


def verify_gameplay_gate_regression_baseline(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT,
    baseline_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT,
    smoke_manifest_path: str | Path | None = None,
    work_dir: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_WORK_DIR,
    fixture_media_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    verified_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    verified_at = verified_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    baseline = _load_baseline(baseline_path=baseline_path, errors=errors)
    if errors:
        status = "baseline_missing" if not baseline else "baseline_invalid"
        verification = _verification_payload(
            status=status,
            baseline=baseline,
            current={},
            drift_items=errors,
            verified_at=verified_at,
        )
        return _write_verification(verification, output_path)
    current_result = _build_current_summary(
        smoke_manifest_path=smoke_manifest_path or baseline.get("source_manifest_path"),
        work_dir=work_dir,
        fixture_media_path=fixture_media_path,
        model_asset_path=model_asset_path,
        generated_at=verified_at,
        probe_runner=probe_runner,
    )
    if current_result.get("ok") is False:
        verification = _verification_payload(
            status="current_output_invalid",
            baseline=baseline,
            current={},
            drift_items=_list(current_result.get("errors")),
            verified_at=verified_at,
        )
        return _write_verification(verification, output_path)
    current = _dict(current_result.get("current"))
    drift_items = _compare_summaries(
        baseline_summary=_dict(baseline.get("summary")),
        current_summary=_dict(current.get("summary")),
    )
    drift_detected = bool(drift_items)
    breaking_drift = any(item.get("severity") == "breaking" for item in drift_items)
    status = (
        "breaking_drift_detected"
        if breaking_drift
        else "drift_detected"
        if drift_detected
        else "completed"
    )
    verification = _verification_payload(
        status=status,
        baseline=baseline,
        current=current,
        drift_items=drift_items,
        verified_at=verified_at,
    )
    return _write_verification(verification, output_path)


def build_gameplay_gate_regression_report(
    *,
    contract_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT,
    baseline_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
    verification_path: str | Path = DEFAULT_GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REGRESSION_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    baseline = _load_baseline(baseline_path=baseline_path, errors=errors)
    verification = _load_verification(verification_path=verification_path, errors=errors)
    if verification:
        errors.extend(_validate_verification_shape(verification))
    report = {
        "report_type": GAMEPLAY_GATE_REGRESSION_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "baseline_path": str(Path(baseline_path)),
        "verification_path": str(Path(verification_path)),
        "baseline_id": baseline.get("baseline_id"),
        "verification_status": verification.get("status"),
        "drift_detected": verification.get("drift_detected"),
        "breaking_drift_detected": verification.get("breaking_drift_detected"),
        "drift_items": _list(verification.get("drift_items")),
        "summary": {
            "baseline_summary": _dict(verification.get("baseline_summary")),
            "current_summary": _dict(verification.get("current_summary")),
            "error_count": len(errors),
            "report_is_structural_only": True,
        },
        "errors": errors,
        "warnings": dict(REGRESSION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "verification_failed",
        "report_type": GAMEPLAY_GATE_REGRESSION_REPORT_TYPE,
        "report_version": GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
        "baseline_id": baseline.get("baseline_id"),
        "report": report,
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "baseline_scope": {
            "purpose": "gameplay_gate_structural_regression_protection",
            "explicit_fixture_media_only": True,
            "default_fixture_media_path": DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH,
            "freezes_structural_counts": True,
            "freezes_model_asset_provenance": True,
            "freezes_gate_config": True,
            "does_not_assess_classifier_correctness": True,
            "does_not_claim_generalization": True,
            "does_not_mutate_model_assets": True,
            "does_not_mutate_non_gameplay_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "baseline_schema": {
            "baseline_type": GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE,
            "baseline_version": GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION,
            "required_fields": [
                "baseline_id",
                "baseline_version",
                "generated_at",
                "source_manifest_path",
                "fixture_mode",
                "model_asset_ref",
                "model_asset_sha256",
                "classifier_asset_exists",
                "threshold",
                "smoothing_window",
                "hysteresis_settings",
                "entry_count",
                "gameplay_segment_candidate_count",
                "non_gameplay_segment_candidate_count",
                "uncertain_segment_count",
                "downstream_allowed_window_count",
                "downstream_blocked_window_count",
                "downstream_review_required_window_count",
                "perception_execution_window_count",
                "perception_skipped_window_count",
                "replay_timeline_entry_count",
                "smoke_entry_count",
                "warnings",
                "non_claims",
            ],
        },
        "verification_schema": {
            "verification_type": GAMEPLAY_GATE_REGRESSION_VERIFICATION_TYPE,
            "allowed_statuses": sorted(ALLOWED_VERIFICATION_STATUSES),
            "allowed_result_fields": [
                "ok",
                "status",
                "baseline_id",
                "current_summary",
                "baseline_summary",
                "drift_detected",
                "breaking_drift_detected",
                "drift_items",
                "warnings",
                "baseline_is_not_truth",
                "gameplay_gate_is_not_truth",
                "classifier_correctness_not_assessed",
                "generalization_not_claimed",
            ],
        },
        "drift_detection_schema": {
            "allowed_severities": sorted(ALLOWED_DRIFT_SEVERITIES),
            "compares_contract_version_refs": True,
            "compares_model_asset_sha": True,
            "compares_gate_config": True,
            "compares_count_fields": True,
            "compares_warning_categories": True,
            "compares_status_distributions": True,
            "drift_is_not_correctness_failure": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_baseline_shape": True,
            "validate_verification_report_shape": True,
            "validate_allowed_statuses": True,
            "validate_allowed_severities": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_existing_non_gameplay_baselines": True,
        },
        "provenance_requirements": {
            "source_manifest_path_required": True,
            "fixture_mode_required": True,
            "model_asset_provenance_required": True,
            "gate_config_required": True,
            "source_contract_refs_required": True,
            "warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(REGRESSION_WARNINGS),
    }


def _build_current_summary(
    *,
    smoke_manifest_path: str | Path | None,
    work_dir: str | Path,
    fixture_media_path: str | Path,
    model_asset_path: str | Path,
    generated_at: datetime,
    probe_runner: Any | None,
) -> dict[str, Any]:
    root = Path(work_dir).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(smoke_manifest_path).expanduser() if smoke_manifest_path else None
    if manifest_path is None or not manifest_path.is_file():
        manifest_path = root / "gameplay_gate_regression_fixture_manifest.json"
        build_gameplay_gated_many_point_smoke_manifest_template(
            local_media_paths=[fixture_media_path, fixture_media_path],
            source_label=DEFAULT_GAMEPLAY_GATE_REGRESSION_FIXTURE_SOURCE_LABEL,
            output_path=manifest_path,
            generated_at=generated_at,
            allow_fixture_mode=True,
        )
    smoke_output = root / "gameplay_gate_regression_smoke.current.json"
    smoke_result = run_gameplay_gated_many_point_smoke(
        contract_path=DEFAULT_GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT,
        manifest_path=manifest_path,
        smoke_mode="fixture_only",
        output_dir=root / "smoke_artifacts",
        output_path=smoke_output,
        model_asset_path=model_asset_path,
        many_point_contract_path=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        gameplay_segment_contract_path=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        routing_contract_path=DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
        execution_contract_path=DEFAULT_GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT,
        replay_review_contract_path=DEFAULT_GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT,
        generated_at=generated_at,
        probe_runner=probe_runner,
    )
    if smoke_result.get("ok") is False:
        return {
            "ok": False,
            "errors": [_error("smoke_run_failed", "smoke_result", smoke_result.get("status"))],
        }
    smoke_report = _dict(smoke_result.get("report"))
    return {
        "ok": True,
        "current": _current_from_smoke_report(
            smoke_report=smoke_report,
            smoke_output_path=smoke_output,
            manifest_path=manifest_path,
        ),
    }


def _current_from_smoke_report(
    *,
    smoke_report: dict[str, Any],
    smoke_output_path: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    entries = [entry for entry in _list(smoke_report.get("entries")) if isinstance(entry, dict)]
    candidate_artifacts = [
        _dict(entry.get("artifact_outputs")).get("gameplay_segment_candidates")
        for entry in entries
    ]
    candidate_payloads = [
        _dict(_load_json(path, label="gameplay_segment_candidates").get("data"))
        for path in candidate_artifacts
        if path
    ]
    segment_counts = _segment_counts(candidate_payloads)
    gate_config = _first_gate_config(candidate_payloads)
    model_asset = _first_model_asset(entries, candidate_payloads)
    summary = {
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "model_asset_sha256": model_asset.get("model_asset_sha256"),
        "classifier_asset_exists": model_asset.get("model_asset_exists") is True,
        "threshold": gate_config.get("threshold"),
        "smoothing_window": gate_config.get("smoothing_window"),
        "hysteresis_settings": _dict(gate_config.get("hysteresis")),
        "entry_count": int(smoke_report.get("entry_count") or 0),
        "gameplay_segment_candidate_count": segment_counts["gameplay_segment_candidate"],
        "non_gameplay_segment_candidate_count": segment_counts["non_gameplay_segment_candidate"],
        "uncertain_segment_count": segment_counts["uncertain_segment"],
        "downstream_allowed_window_count": sum(
            int(entry.get("downstream_allowed_window_count") or 0) for entry in entries
        ),
        "downstream_blocked_window_count": sum(
            int(entry.get("downstream_blocked_window_count") or 0) for entry in entries
        ),
        "downstream_review_required_window_count": sum(
            int(entry.get("downstream_review_required_window_count") or 0) for entry in entries
        ),
        "perception_execution_window_count": sum(
            int(entry.get("perception_execution_window_count") or 0) for entry in entries
        ),
        "perception_skipped_window_count": sum(
            int(entry.get("perception_skipped_window_count") or 0) for entry in entries
        ),
        "replay_timeline_entry_count": sum(
            int(entry.get("replay_timeline_entry_count") or 0) for entry in entries
        ),
        "smoke_entry_count": len(entries),
        "warning_categories": sorted(_dict(smoke_report.get("warnings")).keys()),
        "status_distribution": dict(
            sorted(Counter(str(entry.get("status")) for entry in entries).items())
        ),
    }
    return {
        "source_manifest_path": str(manifest_path),
        "smoke_output_path": str(smoke_output_path),
        "fixture_mode": str(smoke_report.get("smoke_mode") or "fixture_only"),
        "model_asset_ref": model_asset.get("model_asset_ref"),
        "model_asset_sha256": summary["model_asset_sha256"],
        "classifier_asset_exists": summary["classifier_asset_exists"],
        "threshold": summary["threshold"],
        "smoothing_window": summary["smoothing_window"],
        "hysteresis_settings": summary["hysteresis_settings"],
        "summary": summary,
        "warnings": _dict(smoke_report.get("warnings")),
        "non_claims": dict(NON_CLAIMS),
    }


def _baseline_from_current(
    *,
    current: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    summary = _dict(current.get("summary"))
    baseline_id = _stable_id(
        "gameplay_gate_regression_baseline_v1",
        json.dumps(summary, sort_keys=True),
    )
    return {
        "baseline_type": GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE,
        "baseline_id": baseline_id,
        "baseline_version": GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_manifest_path": current.get("source_manifest_path"),
        "smoke_output_path": current.get("smoke_output_path"),
        "fixture_mode": current.get("fixture_mode"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "model_asset_ref": current.get("model_asset_ref"),
        "model_asset_sha256": current.get("model_asset_sha256"),
        "classifier_asset_exists": current.get("classifier_asset_exists"),
        "threshold": current.get("threshold"),
        "smoothing_window": current.get("smoothing_window"),
        "hysteresis_settings": current.get("hysteresis_settings"),
        "entry_count": summary.get("entry_count"),
        "gameplay_segment_candidate_count": summary.get("gameplay_segment_candidate_count"),
        "non_gameplay_segment_candidate_count": summary.get(
            "non_gameplay_segment_candidate_count"
        ),
        "uncertain_segment_count": summary.get("uncertain_segment_count"),
        "downstream_allowed_window_count": summary.get("downstream_allowed_window_count"),
        "downstream_blocked_window_count": summary.get("downstream_blocked_window_count"),
        "downstream_review_required_window_count": summary.get(
            "downstream_review_required_window_count"
        ),
        "perception_execution_window_count": summary.get("perception_execution_window_count"),
        "perception_skipped_window_count": summary.get("perception_skipped_window_count"),
        "replay_timeline_entry_count": summary.get("replay_timeline_entry_count"),
        "smoke_entry_count": summary.get("smoke_entry_count"),
        "summary": summary,
        "warnings": _dict(current.get("warnings")),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }


def _compare_summaries(
    *,
    baseline_summary: dict[str, Any],
    current_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    drift_items: list[dict[str, Any]] = []
    fields = [
        ("source_contract_refs", "breaking"),
        ("model_asset_sha256", "warning"),
        ("classifier_asset_exists", "warning"),
        ("threshold", "breaking"),
        ("smoothing_window", "breaking"),
        ("hysteresis_settings", "breaking"),
        ("entry_count", "breaking"),
        ("gameplay_segment_candidate_count", "breaking"),
        ("non_gameplay_segment_candidate_count", "breaking"),
        ("uncertain_segment_count", "breaking"),
        ("downstream_allowed_window_count", "breaking"),
        ("downstream_blocked_window_count", "breaking"),
        ("downstream_review_required_window_count", "breaking"),
        ("perception_execution_window_count", "breaking"),
        ("perception_skipped_window_count", "breaking"),
        ("replay_timeline_entry_count", "breaking"),
        ("smoke_entry_count", "breaking"),
        ("warning_categories", "warning"),
        ("status_distribution", "breaking"),
    ]
    for field, severity in fields:
        expected = baseline_summary.get(field)
        actual = current_summary.get(field)
        if expected != actual:
            drift_items.append(
                {
                    "field": field,
                    "expected": expected,
                    "actual": actual,
                    "severity": severity,
                    "reason": "structural_regression_baseline_mismatch",
                }
            )
    return drift_items


def _verification_payload(
    *,
    status: str,
    baseline: dict[str, Any],
    current: dict[str, Any],
    drift_items: list[dict[str, Any]],
    verified_at: datetime,
) -> dict[str, Any]:
    breaking = any(item.get("severity") == "breaking" for item in drift_items)
    return {
        "verification_type": GAMEPLAY_GATE_REGRESSION_VERIFICATION_TYPE,
        "verification_version": GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION,
        "verified_at": verified_at.isoformat(),
        "ok": status == "completed",
        "status": status,
        "baseline_id": baseline.get("baseline_id"),
        "current_summary": _dict(current.get("summary")),
        "baseline_summary": _dict(baseline.get("summary")),
        "drift_detected": bool(drift_items),
        "breaking_drift_detected": breaking,
        "drift_items": drift_items,
        "warnings": dict(REGRESSION_WARNINGS),
        "baseline_is_not_truth": True,
        "gameplay_gate_is_not_truth": True,
        "classifier_correctness_not_assessed": True,
        "generalization_not_claimed": True,
        "tom_provenance": _tom_provenance(),
    }


def _write_verification(
    verification: dict[str, Any],
    output_path: str | Path | None,
) -> dict[str, Any]:
    result = dict(verification)
    _write_json_if_requested(output_path, verification, result, "verification_output")
    return result


def _validate_baseline_shape(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(baseline, path="baseline")
    if baseline.get("baseline_type") != GAMEPLAY_GATE_REGRESSION_BASELINE_TYPE:
        errors.append(
            _error(
                "invalid_baseline_type",
                "baseline_type",
                baseline.get("baseline_type"),
            )
        )
    if baseline.get("baseline_version") != GAMEPLAY_GATE_REGRESSION_BASELINE_VERSION:
        errors.append(
            _error("invalid_baseline_version", "baseline_version", baseline.get("baseline_version"))
        )
    for field in _contract_payload(exported_at=GAMEPLAY_GATE_REGRESSION_EXPORTED_AT)[
        "baseline_schema"
    ]["required_fields"]:
        if field not in baseline:
            errors.append(_error("missing_baseline_field", field, None))
    return errors


def _validate_verification_shape(verification: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(verification, path="verification")
    if verification.get("status") not in ALLOWED_VERIFICATION_STATUSES:
        errors.append(_error("invalid_verification_status", "status", verification.get("status")))
    for item in _list(verification.get("drift_items")):
        if not isinstance(item, dict):
            errors.append(_error("invalid_drift_item", "drift_items", item))
            continue
        if item.get("severity") not in ALLOWED_DRIFT_SEVERITIES:
            errors.append(_error("invalid_drift_severity", "drift_items.severity", item))
    return errors


def _load_contract(contract_path: str | Path, errors: list[dict[str, Any]]) -> dict[str, Any]:
    loaded = _load_json(contract_path, label="gameplay_gate_regression_contract")
    if loaded.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", loaded))
        return {}
    contract = _dict(loaded.get("data"))
    errors.extend(_validate_contract_shape(contract))
    return contract


def _load_baseline(baseline_path: str | Path, errors: list[dict[str, Any]]) -> dict[str, Any]:
    loaded = _load_json(baseline_path, label="gameplay_gate_regression_baseline")
    if loaded.get("ok") is False:
        errors.append(_error("baseline_load_failed", "baseline_path", loaded))
        return {}
    baseline = _dict(loaded.get("data"))
    errors.extend(_validate_baseline_shape(baseline))
    return baseline


def _load_verification(
    *,
    verification_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(verification_path, label="gameplay_gate_regression_verification")
    if loaded.get("ok") is False:
        errors.append(_error("verification_load_failed", "verification_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_GATE_REGRESSION_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != GAMEPLAY_GATE_REGRESSION_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for key, expected in SOURCE_CONTRACT_REFS.items():
        actual = _dict(contract.get("source_contract_refs")).get(key)
        if actual != expected:
            errors.append(_error("invalid_source_contract_ref", key, actual))
    return errors


def _segment_counts(candidate_payloads: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for payload in candidate_payloads:
        for segment in _list(payload.get("segment_candidates")):
            if isinstance(segment, dict):
                counts[str(segment.get("segment_status"))] += 1
    return counts


def _first_gate_config(candidate_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    for payload in candidate_payloads:
        config = _dict(payload.get("gate_config"))
        if config:
            return config
    return {}


def _first_model_asset(
    entries: list[dict[str, Any]],
    candidate_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    for payload in candidate_payloads:
        asset = _dict(payload.get("model_asset"))
        if asset:
            return asset
    for entry in entries:
        model_asset = _dict(entry.get("model_asset"))
        if model_asset:
            return {
                "model_asset_exists": model_asset.get("exists"),
                "model_asset_sha256": model_asset.get("sha256"),
                "model_asset_ref": model_asset.get("path"),
            }
    return {}


def _failed_build(
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
) -> dict[str, Any]:
    payload = {
        "ok": False,
        "status": status,
        "errors": errors,
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, payload, payload, "baseline_output")
    return payload


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


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "status": "missing_file", "label": label, "path": str(path)}
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(path),
            "error": str(exc),
        }
    if not isinstance(data, dict):
        return {"ok": False, "status": "invalid_json_shape", "label": label}
    return {"ok": True, "status": "loaded", "label": label, "data": data}


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_REGRESSION_TOKENS:
                errors.append(_error("forbidden_token_key", nested_path, key_text))
            errors.extend(_forbidden_token_errors(nested, path=nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_REGRESSION_TOKENS:
        errors.append(_error("forbidden_token_value", path, value))
    return errors


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        "::".join(str(part) for part in parts).encode("utf-8")
    ).hexdigest()[:16]
    return f"{prefix}_{digest}"


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_GATE_REGRESSION_BLUEPRINT,
        "blueprint_name": GAMEPLAY_GATE_REGRESSION_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
        "structural_only": True,
    }
