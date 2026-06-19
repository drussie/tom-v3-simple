from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tom_v3_video.probe import FfprobeError, probe_video
from tom_v3_video.time_index import frame_to_timestamp_ms

GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE = "gameplay_segment_gate_contract"
GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION = "v1"
GAMEPLAY_SEGMENT_CANDIDATES_TYPE = "gameplay_segment_candidates"
GAMEPLAY_SEGMENT_CANDIDATES_VERSION = "v1"
GAMEPLAY_SEGMENT_REPORT_TYPE = "gameplay_segment_gate_report"
GAMEPLAY_SEGMENT_REPORT_VERSION = "v1"
GAMEPLAY_SEGMENT_GATE_BLUEPRINT = "blueprint_38"
GAMEPLAY_SEGMENT_GATE_BLUEPRINT_NAME = (
    "gameplay_segment_gate_tom_v1_view_classifier_v1"
)

DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT = (
    ".data/contracts/gameplay_segment_gate_contract_v1.json"
)
DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH = (
    "model_assets/tom_v1/view_classifier_gameplay.pt"
)
DEFAULT_GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT = (
    ".data/exports/gameplay_classifier_asset_inspection.current.json"
)
DEFAULT_GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT = (
    ".data/exports/gameplay_segment_candidates.current.json"
)
DEFAULT_GAMEPLAY_SEGMENT_VALIDATION_OUTPUT = (
    ".data/exports/gameplay_segment_candidates.validation.json"
)
DEFAULT_GAMEPLAY_SEGMENT_REPORT_OUTPUT = (
    ".data/exports/gameplay_segment_report.current.json"
)

GAMEPLAY_SEGMENT_GATE_EXPORTED_AT = datetime(2026, 6, 19, 0, 0, tzinfo=UTC)
DEFAULT_CLASSIFIER_NAME = "tom-v1-view-classifier-gameplay"
DEFAULT_CLASSIFIER_VERSION = "v1-local"
DEFAULT_THRESHOLD = 0.55
DEFAULT_SMOOTHING_WINDOW = 3
DEFAULT_HYSTERESIS_ENTER = 0.60
DEFAULT_HYSTERESIS_EXIT = 0.45
DEFAULT_FRAME_SAMPLE_RATE = 30
DEFAULT_MAX_FRAMES = 240
DEFAULT_MIN_SEGMENT_DURATION_MS = 500
DEFAULT_INFERENCE_MODE = "provenance_fixture"

ALLOWED_RAW_CLASSIFICATION_STATUSES = {
    "gameplay_candidate",
    "non_gameplay_candidate",
    "uncertain",
    "not_assessed",
    "not_applicable",
}
ALLOWED_SEGMENT_STATUSES = {
    "gameplay_segment_candidate",
    "non_gameplay_segment_candidate",
    "uncertain_segment",
    "short_segment_filtered",
    "needs_review",
    "not_assessed",
    "not_applicable",
}
ALLOWED_DOWNSTREAM_GATE_STATUSES = {
    "allowed_for_downstream_observation",
    "blocked_from_downstream_observation",
    "requires_human_review",
    "not_assessed",
    "not_applicable",
}
ALLOWED_REVIEW_STATUSES = {
    "not_assessed",
    "requires_human_review",
    "review_ready",
    "not_applicable",
}
ALLOWED_INFERENCE_MODES = {
    "provenance_fixture",
    "fixture_probabilities",
    "asset_inspection_only",
}

FORBIDDEN_GAMEPLAY_GATE_TOKENS = {
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
}

GAMEPLAY_SEGMENT_GATE_WARNINGS = {
    "candidate_evidence_only": True,
    "classification_is_structural_suitability_evidence": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_event_labels": True,
    "does_not_create_point_labels": True,
    "does_not_run_downstream_perception": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_claim_generalization": True,
    "does_not_claim_automatic_correctness": True,
    "does_not_convert_outputs_into_training_labels": True,
    "no_adjudication": True,
    "observation_only": True,
    "review_support_only": True,
}


def export_gameplay_segment_gate_contract(
    *,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the Blueprint 38 gameplay segment gate contract."""

    exported_at = exported_at or GAMEPLAY_SEGMENT_GATE_EXPORTED_AT
    contract = {
        "contract_type": GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "gate_scope": {
            "purpose": "gameplay_observation_suitability_gate",
            "reads_explicit_media_input_only": True,
            "uses_existing_tom_v1_classifier_asset": True,
            "creates_segment_candidate_artifacts": True,
            "runs_downstream_perception": False,
            "auto_discovers_media": False,
            "silently_ingests_media": False,
            "mutates_regression_baselines": False,
        },
        "model_asset_contract": {
            "default_model_asset_path": DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
            "classifier_name": DEFAULT_CLASSIFIER_NAME,
            "classifier_version": DEFAULT_CLASSIFIER_VERSION,
            "required_hash_algorithm": "sha256",
            "model_asset_may_be_missing_in_ci": True,
            "model_weights_are_local_ignored_assets": True,
            "model_asset_is_not_copied_or_committed": True,
            "safe_inference_modes": sorted(ALLOWED_INFERENCE_MODES),
        },
        "gameplay_classification_schema": {
            "output_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
            "output_version": GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
            "required_fields": [
                "media_id",
                "frame_index",
                "time_ms",
                "model_asset_ref",
                "model_asset_sha256",
                "class_name",
                "gameplay_probability",
                "non_gameplay_probability",
                "threshold",
                "raw_status",
                "smoothed_status",
                "warnings",
            ],
            "allowed_raw_statuses": sorted(ALLOWED_RAW_CLASSIFICATION_STATUSES),
        },
        "segment_candidate_schema": {
            "required_fields": [
                "segment_id",
                "media_id",
                "segment_start_ms",
                "segment_end_ms",
                "start_frame_index",
                "end_frame_index",
                "duration_ms",
                "mean_gameplay_probability",
                "min_gameplay_probability",
                "max_gameplay_probability",
                "segment_status",
                "downstream_gate_status",
                "review_status",
                "warnings",
            ],
            "allowed_segment_statuses": sorted(ALLOWED_SEGMENT_STATUSES),
            "allowed_downstream_gate_statuses": sorted(ALLOWED_DOWNSTREAM_GATE_STATUSES),
            "allowed_review_statuses": sorted(ALLOWED_REVIEW_STATUSES),
        },
        "temporal_smoothing_schema": {
            "default_threshold": DEFAULT_THRESHOLD,
            "default_smoothing_window": DEFAULT_SMOOTHING_WINDOW,
            "default_hysteresis_enter": DEFAULT_HYSTERESIS_ENTER,
            "default_hysteresis_exit": DEFAULT_HYSTERESIS_EXIT,
            "default_min_segment_duration_ms": DEFAULT_MIN_SEGMENT_DURATION_MS,
            "smoothing_is_structural_only": True,
            "hysteresis_is_gate_stability_only": True,
        },
        "downstream_gate_schema": {
            "allowed_statuses": sorted(ALLOWED_DOWNSTREAM_GATE_STATUSES),
            "allowed_status_meaning": {
                "allowed_for_downstream_observation": (
                    "Segment appears suitable for future downstream observation jobs."
                ),
                "blocked_from_downstream_observation": (
                    "Segment is structurally blocked from future downstream observation jobs."
                ),
                "requires_human_review": (
                    "Segment is uncertain and should be inspected before downstream use."
                ),
                "not_assessed": "No downstream suitability assessment was made.",
                "not_applicable": "Downstream gating does not apply to this row.",
            },
            "future_downstream_jobs_are_not_executed_by_this_contract": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_classifier_asset_provenance_shape": True,
            "validate_segment_candidate_output_shape": True,
            "validate_allowed_statuses": True,
            "require_hash_when_asset_exists": True,
            "reject_handoff_forbidden_exact_tokens": True,
            "structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_create_event_labels": True,
            "does_not_create_point_labels": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "media_id_required": True,
            "source_media_path_or_uri_required": True,
            "model_asset_path_required": True,
            "model_asset_sha256_required_when_asset_exists": True,
            "classifier_name_required": True,
            "classifier_version_required": True,
            "threshold_required": True,
            "smoothing_window_required": True,
            "hysteresis_settings_required": True,
            "inference_mode_required": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE,
        "contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def inspect_gameplay_classifier_asset(
    *,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT,
    classifier_name: str = DEFAULT_CLASSIFIER_NAME,
    classifier_version: str = DEFAULT_CLASSIFIER_VERSION,
) -> dict[str, Any]:
    """Inspect and hash the local TOM v1 gameplay classifier asset if present."""

    inspection = _inspect_model_asset(
        model_asset_path=model_asset_path,
        classifier_name=classifier_name,
        classifier_version=classifier_version,
    )
    result = {
        "ok": True,
        "status": "completed" if inspection["model_asset_exists"] else "missing_asset",
        **inspection,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    _write_json_if_requested(output_path, result, result, "inspection_output")
    return result


def build_gameplay_segment_candidates(
    *,
    local_media_path: str | Path,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT,
    media_id: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    classifier_name: str = DEFAULT_CLASSIFIER_NAME,
    classifier_version: str = DEFAULT_CLASSIFIER_VERSION,
    threshold: float = DEFAULT_THRESHOLD,
    smoothing_window: int = DEFAULT_SMOOTHING_WINDOW,
    hysteresis_enter: float = DEFAULT_HYSTERESIS_ENTER,
    hysteresis_exit: float = DEFAULT_HYSTERESIS_EXIT,
    frame_sample_rate: int = DEFAULT_FRAME_SAMPLE_RATE,
    max_frames: int | None = DEFAULT_MAX_FRAMES,
    min_segment_duration_ms: int = DEFAULT_MIN_SEGMENT_DURATION_MS,
    inference_mode: str = DEFAULT_INFERENCE_MODE,
    viewer_base_url: str = "http://127.0.0.1:3000",
    generated_at: datetime | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    """Build candidate gameplay/non-gameplay segments from explicit media input."""

    generated_at = generated_at or datetime.now(UTC)
    media_path = Path(local_media_path).expanduser()
    if not media_path.is_file():
        return _failed(
            "media_path_not_found",
            f"local media path not found: {media_path}",
            output_type=GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
        )
    config_error = _validate_gate_config(
        threshold=threshold,
        smoothing_window=smoothing_window,
        hysteresis_enter=hysteresis_enter,
        hysteresis_exit=hysteresis_exit,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        min_segment_duration_ms=min_segment_duration_ms,
        inference_mode=inference_mode,
    )
    if config_error:
        return config_error

    try:
        probe = probe_video(media_path, runner=probe_runner)
    except (FileNotFoundError, FfprobeError, OSError) as exc:
        return _failed(
            "media_probe_failed",
            str(exc),
            output_type=GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
        )

    asset = _inspect_model_asset(
        model_asset_path=model_asset_path,
        classifier_name=classifier_name,
        classifier_version=classifier_version,
    )
    media_id = media_id or _stable_id("media", str(media_path.resolve(strict=False)))
    sampled_frames = _sample_frame_indices(
        frame_count=probe.frame_count,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
    )
    classifications = _build_classifications(
        media_id=media_id,
        sampled_frames=sampled_frames,
        fps=probe.fps,
        frame_count=probe.frame_count,
        duration_ms=probe.duration_ms,
        threshold=threshold,
        smoothing_window=smoothing_window,
        hysteresis_enter=hysteresis_enter,
        hysteresis_exit=hysteresis_exit,
        asset=asset,
    )
    segments = _build_segments(
        media_id=media_id,
        classifications=classifications,
        fps=probe.fps,
        frame_count=probe.frame_count,
        min_segment_duration_ms=min_segment_duration_ms,
    )
    output = {
        "output_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
        "output_version": GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
        "generated_at": generated_at.isoformat(),
        "media_id": media_id,
        "source_media_path": str(media_path),
        "source_uri": media_path.resolve(strict=False).as_uri(),
        "media_probe": {
            "duration_ms": probe.duration_ms,
            "frame_count": probe.frame_count,
            "fps": probe.fps,
            "width": probe.width,
            "height": probe.height,
            "frame_count_source": probe.frame_count_source,
        },
        "model_asset": asset,
        "classifier": {
            "classifier_name": classifier_name,
            "classifier_version": classifier_version,
            "inference_mode": inference_mode,
            "runtime_dependency_required_for_smoke": False,
            "gpu_required": False,
            "external_download_required": False,
        },
        "gate_config": {
            "threshold": threshold,
            "smoothing_window": smoothing_window,
            "hysteresis": {
                "enter_gameplay_probability": hysteresis_enter,
                "exit_gameplay_probability": hysteresis_exit,
            },
            "frame_sample_rate": frame_sample_rate,
            "max_frames": max_frames,
            "min_segment_duration_ms": min_segment_duration_ms,
        },
        "classifications": classifications,
        "segment_candidates": segments,
        "summary": _candidate_summary(classifications, segments),
        "replay_timeline": _replay_timeline(media_id, segments, viewer_base_url),
        "downstream_gate_summary": _downstream_gate_summary(segments),
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "validation_does_not_infer_tennis_meaning": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "output_type": GAMEPLAY_SEGMENT_CANDIDATES_TYPE,
        "output_version": GAMEPLAY_SEGMENT_CANDIDATES_VERSION,
        "media_id": media_id,
        "classification_count": len(classifications),
        "segment_candidate_count": len(segments),
        "model_asset_exists": asset["model_asset_exists"],
        "model_asset_sha256": asset["model_asset_sha256"],
        "candidates": output,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    _write_json_if_requested(output_path, output, result, "candidates_output")
    return result


def validate_gameplay_segment_candidates(
    *,
    candidates_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate gameplay segment candidate artifacts structurally."""

    validated_at = validated_at or datetime.now(UTC)
    contract_load = _load_json(contract_path, label="gameplay_segment_gate_contract")
    candidates_load = _load_json(candidates_path, label="gameplay_segment_candidates")
    errors: list[dict[str, Any]] = []
    if contract_load.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", contract_load))
        contract = {}
    else:
        contract = _dict(contract_load.get("data"))
        errors.extend(_validate_contract_shape(contract))
    if candidates_load.get("ok") is False:
        errors.append(_error("candidates_load_failed", "candidates_path", candidates_load))
        candidates = {}
    else:
        candidates = _dict(candidates_load.get("data"))
        errors.extend(_validate_candidates_shape(candidates))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "gameplay_segment_candidates_validation",
        "validation_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "candidates_path": str(Path(candidates_path)),
        "contract_type": contract.get("contract_type"),
        "contract_version": contract.get("contract_version"),
        "output_type": candidates.get("output_type"),
        "output_version": candidates.get("output_version"),
        "error_count": len(errors),
        "errors": errors,
        "classification_count": len(_list(candidates.get("classifications"))),
        "segment_candidate_count": len(_list(candidates.get("segment_candidates"))),
        "tracked_exports_should_not_be_committed": True,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
        "known_limitations": [
            "Validation checks structure, statuses, provenance, and exact forbidden tokens.",
            "Validation does not run the classifier.",
            "Validation does not run downstream perception jobs.",
            "Validation does not infer tennis meaning.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_gameplay_segment_report(
    *,
    candidates_path: str | Path,
    contract_path: str | Path = DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_GAMEPLAY_SEGMENT_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a read-only report over gameplay segment candidate outputs."""

    generated_at = generated_at or datetime.now(UTC)
    candidates_load = _load_json(candidates_path, label="gameplay_segment_candidates")
    if candidates_load.get("ok") is False:
        return candidates_load
    candidates = _dict(candidates_load.get("data"))
    validation = validate_gameplay_segment_candidates(
        candidates_path=candidates_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_candidates",
            "error_count": validation.get("error_count"),
            "errors": validation.get("errors", []),
            "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
        }

    segments = _list(candidates.get("segment_candidates"))
    classifications = _list(candidates.get("classifications"))
    report = {
        "report_type": GAMEPLAY_SEGMENT_REPORT_TYPE,
        "report_version": GAMEPLAY_SEGMENT_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_candidates_path": str(Path(candidates_path)),
        "source_contract_path": str(Path(contract_path)),
        "media_id": candidates.get("media_id"),
        "model_asset": _dict(candidates.get("model_asset")),
        "classifier": _dict(candidates.get("classifier")),
        "summary": {
            **_candidate_summary(classifications, segments),
            "validation_status": validation.get("status"),
            "validation_error_count": validation.get("error_count"),
        },
        "downstream_gate_summary": _downstream_gate_summary(segments),
        "replay_timeline": candidates.get("replay_timeline"),
        "next_pipeline_contract": {
            "allowed_segments_can_gate_future_jobs": True,
            "blocked_segments_should_not_run_future_downstream_observation_jobs": True,
            "requires_human_review_segments_need_operator_inspection": True,
            "this_report_runs_downstream_jobs": False,
        },
        "validation_snapshot": validation,
        "tom_provenance": _tom_provenance(),
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": GAMEPLAY_SEGMENT_REPORT_TYPE,
        "report_version": GAMEPLAY_SEGMENT_REPORT_VERSION,
        "summary": report["summary"],
        "report": report,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _inspect_model_asset(
    *,
    model_asset_path: str | Path,
    classifier_name: str,
    classifier_version: str,
) -> dict[str, Any]:
    original_path = str(model_asset_path)
    path = Path(model_asset_path).expanduser()
    resolved = path.resolve(strict=False)
    exists = resolved.is_file()
    size = resolved.stat().st_size if exists else None
    sha256 = _sha256_file(resolved) if exists else None
    return {
        "model_asset_path": original_path,
        "model_asset_resolved_path": str(resolved),
        "model_asset_exists": exists,
        "model_asset_size_bytes": size,
        "model_asset_sha256": sha256,
        "model_asset_ref": (
            _stable_id("tom_v1_gameplay_classifier", sha256)
            if sha256
            else "tom_v1_gameplay_classifier_missing_asset"
        ),
        "model_asset_suffix": resolved.suffix.lower() or None,
        "classifier_name": classifier_name,
        "classifier_version": classifier_version,
        "model_asset_contract_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "hash_algorithm": "sha256",
        "asset_is_local_ignored_weight": True,
        "asset_loaded_for_inference": False,
        "asset_hash_available": bool(sha256),
    }


def _build_classifications(
    *,
    media_id: str,
    sampled_frames: list[int],
    fps: float | None,
    frame_count: int | None,
    duration_ms: int | None,
    threshold: float,
    smoothing_window: int,
    hysteresis_enter: float,
    hysteresis_exit: float,
    asset: dict[str, Any],
) -> list[dict[str, Any]]:
    probabilities = [
        _fixture_gameplay_probability(frame_index, frame_count, duration_ms)
        for frame_index in sampled_frames
    ]
    smoothed = _rolling_mean(probabilities, smoothing_window)
    classifications: list[dict[str, Any]] = []
    for frame_index, probability, smoothed_probability in zip(
        sampled_frames,
        probabilities,
        smoothed,
        strict=True,
    ):
        raw_status = _raw_classification_status(probability, threshold)
        smoothed_status = _smoothed_classification_status(
            smoothed_probability,
            hysteresis_enter,
            hysteresis_exit,
        )
        classifications.append(
            {
                "media_id": media_id,
                "frame_index": frame_index,
                "time_ms": _time_ms(fps, frame_index),
                "model_asset_ref": asset["model_asset_ref"],
                "model_asset_sha256": asset["model_asset_sha256"],
                "class_name": (
                    "appears_suitable_for_gameplay_observation"
                    if raw_status == "gameplay_candidate"
                    else "non_gameplay_or_uncertain"
                ),
                "gameplay_probability": round(probability, 6),
                "non_gameplay_probability": round(1.0 - probability, 6),
                "smoothed_gameplay_probability": round(smoothed_probability, 6),
                "threshold": threshold,
                "raw_status": raw_status,
                "smoothed_status": smoothed_status,
                "warnings": {
                    "classification_is_candidate_evidence": True,
                    "frame_time_owner": "media_indexing",
                    "no_downstream_job_ran": True,
                },
            }
        )
    return classifications


def _build_segments(
    *,
    media_id: str,
    classifications: list[dict[str, Any]],
    fps: float | None,
    frame_count: int | None,
    min_segment_duration_ms: int,
) -> list[dict[str, Any]]:
    if not classifications:
        return []
    spans: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = [classifications[0]]
    for row in classifications[1:]:
        if row["smoothed_status"] == current[-1]["smoothed_status"]:
            current.append(row)
        else:
            spans.append(current)
            current = [row]
    spans.append(current)

    last_frame = max(0, (frame_count or 1) - 1)
    segments: list[dict[str, Any]] = []
    for index, span in enumerate(spans):
        start_frame = int(span[0]["frame_index"])
        if index + 1 < len(spans):
            end_frame = max(start_frame, int(spans[index + 1][0]["frame_index"]) - 1)
        else:
            end_frame = last_frame
        start_ms = _time_ms(fps, start_frame)
        end_ms = _time_ms(fps, end_frame)
        duration_ms = max(0, end_ms - start_ms)
        probabilities = [float(item["smoothed_gameplay_probability"]) for item in span]
        segment_status = _segment_status_from_raw_status(span[0]["smoothed_status"])
        if 0 < duration_ms < min_segment_duration_ms:
            segment_status = "short_segment_filtered"
        downstream_status = _downstream_status_from_segment_status(segment_status)
        segment = {
            "segment_id": _stable_id(
                "gameplay_segment_candidate_v1",
                media_id,
                start_frame,
                end_frame,
                segment_status,
            ),
            "media_id": media_id,
            "segment_start_ms": start_ms,
            "segment_end_ms": end_ms,
            "start_frame_index": start_frame,
            "end_frame_index": end_frame,
            "duration_ms": duration_ms,
            "mean_gameplay_probability": round(sum(probabilities) / len(probabilities), 6),
            "min_gameplay_probability": round(min(probabilities), 6),
            "max_gameplay_probability": round(max(probabilities), 6),
            "segment_status": segment_status,
            "downstream_gate_status": downstream_status,
            "review_status": (
                "requires_human_review"
                if downstream_status == "requires_human_review"
                else "not_assessed"
            ),
            "warnings": {
                "candidate_segment_only": True,
                "display_only_until_reviewed": True,
                "downstream_gate_is_structural": True,
            },
        }
        segments.append(segment)
    return segments


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != GAMEPLAY_SEGMENT_GATE_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION:
        errors.append(
            _error("invalid_contract_version", "contract_version", contract.get("contract_version"))
        )
    for section in (
        "gate_scope",
        "model_asset_contract",
        "gameplay_classification_schema",
        "segment_candidate_schema",
        "temporal_smoothing_schema",
        "downstream_gate_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_candidates_shape(candidates: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(candidates, path="candidates")
    if candidates.get("output_type") != GAMEPLAY_SEGMENT_CANDIDATES_TYPE:
        errors.append(_error("invalid_output_type", "output_type", candidates.get("output_type")))
    if candidates.get("output_version") != GAMEPLAY_SEGMENT_CANDIDATES_VERSION:
        errors.append(
            _error("invalid_output_version", "output_version", candidates.get("output_version"))
        )
    for section in (
        "media_id",
        "source_media_path",
        "model_asset",
        "classifier",
        "gate_config",
        "classifications",
        "segment_candidates",
        "summary",
        "downstream_gate_summary",
        "warnings",
    ):
        if section not in candidates:
            errors.append(_error("missing_candidates_section", section, None))

    asset = _dict(candidates.get("model_asset"))
    if asset.get("model_asset_exists") is True and not asset.get("model_asset_sha256"):
        errors.append(_error("missing_model_asset_sha256", "model_asset.model_asset_sha256", None))
    classifier = _dict(candidates.get("classifier"))
    if classifier.get("inference_mode") not in ALLOWED_INFERENCE_MODES:
        errors.append(
            _error(
                "invalid_inference_mode",
                "classifier.inference_mode",
                classifier.get("inference_mode"),
            )
        )

    for index, row in enumerate(_list(candidates.get("classifications"))):
        if not isinstance(row, dict):
            errors.append(_error("invalid_classification_row", f"classifications[{index}]", row))
            continue
        raw_status = row.get("raw_status")
        smoothed_status = row.get("smoothed_status")
        if raw_status not in ALLOWED_RAW_CLASSIFICATION_STATUSES:
            errors.append(
                _error("invalid_raw_status", f"classifications[{index}].raw_status", raw_status)
            )
        if smoothed_status not in ALLOWED_RAW_CLASSIFICATION_STATUSES:
            errors.append(
                _error(
                    "invalid_smoothed_status",
                    f"classifications[{index}].smoothed_status",
                    smoothed_status,
                )
            )
        if asset.get("model_asset_exists") is True and not row.get("model_asset_sha256"):
            errors.append(
                _error(
                    "classification_missing_model_asset_sha256",
                    f"classifications[{index}].model_asset_sha256",
                    None,
                )
            )
    for index, row in enumerate(_list(candidates.get("segment_candidates"))):
        if not isinstance(row, dict):
            errors.append(_error("invalid_segment_row", f"segment_candidates[{index}]", row))
            continue
        segment_status = row.get("segment_status")
        downstream_status = row.get("downstream_gate_status")
        review_status = row.get("review_status")
        if segment_status not in ALLOWED_SEGMENT_STATUSES:
            errors.append(
                _error(
                    "invalid_segment_status",
                    f"segment_candidates[{index}].segment_status",
                    segment_status,
                )
            )
        if downstream_status not in ALLOWED_DOWNSTREAM_GATE_STATUSES:
            errors.append(
                _error(
                    "invalid_downstream_gate_status",
                    f"segment_candidates[{index}].downstream_gate_status",
                    downstream_status,
                )
            )
        if review_status not in ALLOWED_REVIEW_STATUSES:
            errors.append(
                _error(
                    "invalid_review_status",
                    f"segment_candidates[{index}].review_status",
                    review_status,
                )
            )
    return errors


def _validate_gate_config(
    *,
    threshold: float,
    smoothing_window: int,
    hysteresis_enter: float,
    hysteresis_exit: float,
    frame_sample_rate: int,
    max_frames: int | None,
    min_segment_duration_ms: int,
    inference_mode: str,
) -> dict[str, Any] | None:
    if not 0 < threshold < 1:
        return _failed("invalid_threshold", "threshold must be between 0 and 1")
    if smoothing_window < 1:
        return _failed("invalid_smoothing_window", "smoothing_window must be >= 1")
    if not 0 <= hysteresis_exit <= hysteresis_enter <= 1:
        return _failed(
            "invalid_hysteresis",
            "hysteresis must satisfy 0 <= exit <= enter <= 1",
        )
    if frame_sample_rate < 1:
        return _failed("invalid_frame_sample_rate", "frame_sample_rate must be >= 1")
    if max_frames is not None and max_frames < 1:
        return _failed("invalid_max_frames", "max_frames must be >= 1 when provided")
    if min_segment_duration_ms < 0:
        return _failed(
            "invalid_min_segment_duration_ms",
            "min_segment_duration_ms must be >= 0",
        )
    if inference_mode not in ALLOWED_INFERENCE_MODES:
        return _failed("invalid_inference_mode", f"unsupported inference mode: {inference_mode}")
    return None


def _fixture_gameplay_probability(
    frame_index: int,
    frame_count: int | None,
    duration_ms: int | None,
) -> float:
    del duration_ms
    denominator = max(1, (frame_count or 120) - 1)
    position = max(0.0, min(1.0, frame_index / denominator))
    if position <= 0.30:
        return 0.82
    if position <= 0.40:
        return 0.24
    if position <= 0.48:
        return 0.52
    if position <= 0.90:
        return 0.84
    return 0.28


def _sample_frame_indices(
    *,
    frame_count: int | None,
    frame_sample_rate: int,
    max_frames: int | None,
) -> list[int]:
    count = max(1, frame_count or frame_sample_rate * 4)
    indices = list(range(0, count, frame_sample_rate))
    if not indices:
        indices = [0]
    if max_frames is not None:
        indices = indices[:max_frames]
    return indices


def _rolling_mean(values: list[float], window: int) -> list[float]:
    smoothed = []
    for index in range(len(values)):
        start = max(0, index - window + 1)
        chunk = values[start : index + 1]
        rolling = sum(chunk) / len(chunk)
        smoothed.append((values[index] * 0.7) + (rolling * 0.3))
    return smoothed


def _raw_classification_status(probability: float, threshold: float) -> str:
    if probability >= threshold:
        return "gameplay_candidate"
    if probability <= 1.0 - threshold:
        return "non_gameplay_candidate"
    return "uncertain"


def _smoothed_classification_status(
    probability: float,
    hysteresis_enter: float,
    hysteresis_exit: float,
) -> str:
    if probability >= hysteresis_enter:
        return "gameplay_candidate"
    if probability <= hysteresis_exit:
        return "non_gameplay_candidate"
    return "uncertain"


def _segment_status_from_raw_status(status: str) -> str:
    if status == "gameplay_candidate":
        return "gameplay_segment_candidate"
    if status == "non_gameplay_candidate":
        return "non_gameplay_segment_candidate"
    if status == "uncertain":
        return "uncertain_segment"
    return "not_assessed"


def _downstream_status_from_segment_status(status: str) -> str:
    if status == "gameplay_segment_candidate":
        return "allowed_for_downstream_observation"
    if status in {"non_gameplay_segment_candidate", "short_segment_filtered"}:
        return "blocked_from_downstream_observation"
    if status in {"uncertain_segment", "needs_review"}:
        return "requires_human_review"
    return "not_assessed"


def _time_ms(fps: float | None, frame_index: int) -> int:
    if fps is None or fps <= 0:
        return 0
    return frame_to_timestamp_ms(fps, frame_index)


def _candidate_summary(
    classifications: list[Any],
    segments: list[Any],
) -> dict[str, Any]:
    raw_counts = Counter(
        item.get("raw_status")
        for item in classifications
        if isinstance(item, dict) and item.get("raw_status")
    )
    smoothed_counts = Counter(
        item.get("smoothed_status")
        for item in classifications
        if isinstance(item, dict) and item.get("smoothed_status")
    )
    segment_counts = Counter(
        item.get("segment_status")
        for item in segments
        if isinstance(item, dict) and item.get("segment_status")
    )
    downstream_counts = Counter(
        item.get("downstream_gate_status")
        for item in segments
        if isinstance(item, dict) and item.get("downstream_gate_status")
    )
    return {
        "classification_count": len(classifications),
        "segment_candidate_count": len(segments),
        "raw_status_counts": dict(sorted(raw_counts.items())),
        "smoothed_status_counts": dict(sorted(smoothed_counts.items())),
        "segment_status_counts": dict(sorted(segment_counts.items())),
        "downstream_gate_status_counts": dict(sorted(downstream_counts.items())),
        "allowed_downstream_segment_count": downstream_counts.get(
            "allowed_for_downstream_observation",
            0,
        ),
        "blocked_downstream_segment_count": downstream_counts.get(
            "blocked_from_downstream_observation",
            0,
        ),
        "human_review_segment_count": downstream_counts.get("requires_human_review", 0),
    }


def _downstream_gate_summary(segments: list[Any]) -> dict[str, Any]:
    return {
        "gate_is_structural_only": True,
        "runs_downstream_jobs": False,
        "allowed_segment_ids": [
            item["segment_id"]
            for item in segments
            if isinstance(item, dict)
            and item.get("downstream_gate_status") == "allowed_for_downstream_observation"
        ],
        "blocked_segment_ids": [
            item["segment_id"]
            for item in segments
            if isinstance(item, dict)
            and item.get("downstream_gate_status") == "blocked_from_downstream_observation"
        ],
        "human_review_segment_ids": [
            item["segment_id"]
            for item in segments
            if isinstance(item, dict)
            and item.get("downstream_gate_status") == "requires_human_review"
        ],
    }


def _replay_timeline(
    media_id: str,
    segments: list[dict[str, Any]],
    viewer_base_url: str,
) -> dict[str, Any]:
    return {
        "timeline_type": "gameplay_segment_gate_timeline",
        "timeline_version": GAMEPLAY_SEGMENT_GATE_CONTRACT_VERSION,
        "media_id": media_id,
        "replay_url": f"{viewer_base_url.rstrip('/')}/replay/{media_id}",
        "lane": {
            "lane_id": "gameplay_segment_gate",
            "label": "Gameplay segment candidates",
            "display_only": True,
            "items": [
                {
                    "id": segment["segment_id"],
                    "start_ms": segment["segment_start_ms"],
                    "end_ms": segment["segment_end_ms"],
                    "status": segment["segment_status"],
                    "downstream_gate_status": segment["downstream_gate_status"],
                }
                for segment in segments
            ],
        },
    }


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_GAMEPLAY_GATE_TOKENS:
                errors.append(_error("forbidden_token_key", child_path, key))
            errors.extend(_forbidden_token_errors(nested, path=child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_GAMEPLAY_GATE_TOKENS:
        errors.append(_error("forbidden_token_value", path, value))
    return errors


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        json.dumps([str(part) for part in parts], sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return f"{prefix}_{digest}"


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


def _write_json_if_requested(
    output_path: str | Path | None,
    data: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None or not str(output_path).strip():
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    result[result_key] = str(path)


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(GAMEPLAY_SEGMENT_GATE_WARNINGS),
        **extra,
    }


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": GAMEPLAY_SEGMENT_GATE_BLUEPRINT,
        "blueprint_name": GAMEPLAY_SEGMENT_GATE_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
