from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel

EVENT_CANDIDATE_3D_DIAGNOSTIC_TYPE = "event_candidate_3d_diagnostic_evidence"
EVENT_CANDIDATE_3D_DIAGNOSTIC_VERSION = "v0"


class EventCandidate3DDiagnosticSchemaError(ValueError):
    pass


class EventCandidate3DDiagnosticStatus(StrEnum):
    not_evaluated = "not_evaluated"
    evaluated = "evaluated"
    cannot_evaluate = "cannot_evaluate"
    insufficient_3d_evidence = "insufficient_3d_evidence"
    height_unknown = "height_unknown"


class EventCandidate3DDiagnosticLabel(StrEnum):
    supports_candidate_context = "supports_candidate_context"
    weakens_candidate_context = "weakens_candidate_context"
    neutral_context = "neutral_context"
    cannot_evaluate = "cannot_evaluate"
    insufficient_evidence = "insufficient_evidence"
    height_unknown = "height_unknown"


TRUTH_LIKE_EVENT_3D_LABELS = {
    "confirmed_hit",
    "confirmed_bounce",
    "false_positive",
    "true_positive",
    "verified_3d",
    "actual_contact",
    "actual_bounce",
    "truth",
    "accepted",
    "confirmed",
    "verified",
}


DEFAULT_EVENT_CANDIDATE_3D_DIAGNOSTIC_WARNINGS = {
    "diagnostic_only": True,
    "not_truth": True,
    "not_3d_truth": True,
    "height_not_verified": True,
    "does_not_change_event_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


class EventCandidate3DDiagnosticCreate(TOMBaseModel):
    media_id: str
    event_candidate_run_id: str
    event_observation_id: str
    candidate_type: str
    trajectory_3d_run_id: str | None = None
    camera_geometry_id: str | None = None
    frame: int
    timestamp_ms: int
    nearest_3d_candidate_id: str | None = None
    nearest_3d_frame: int | None = None
    nearest_3d_timestamp_ms: int | None = None
    nearest_time_delta_ms: int | None = None
    nearest_court_x_m: float | None = None
    nearest_court_y_m: float | None = None
    nearest_court_z_m: float | None = None
    height_status: str = "unknown"
    diagnostic_status: str = EventCandidate3DDiagnosticStatus.not_evaluated.value
    diagnostic_label: str = EventCandidate3DDiagnosticLabel.cannot_evaluate.value
    diagnostic_confidence: float | None = None
    pre_window_sample_count: int = 0
    post_window_sample_count: int = 0
    local_window_sample_count: int = 0
    local_velocity_available: bool = False
    local_speed_mps: float | None = None
    local_direction_delta_degrees: float | None = None
    diagnostics_jsonb: dict[str, Any] = Field(default_factory=dict)
    warnings_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_diagnostic(self) -> EventCandidate3DDiagnosticCreate:
        validate_diagnostic_status(self.diagnostic_status)
        validate_diagnostic_label(self.diagnostic_label)
        self.warnings_jsonb = {
            **DEFAULT_EVENT_CANDIDATE_3D_DIAGNOSTIC_WARNINGS,
            **self.warnings_jsonb,
        }
        self.metadata_jsonb.setdefault(
            "diagnostic_type",
            EVENT_CANDIDATE_3D_DIAGNOSTIC_TYPE,
        )
        self.metadata_jsonb.setdefault(
            "diagnostic_version",
            EVENT_CANDIDATE_3D_DIAGNOSTIC_VERSION,
        )
        self.metadata_jsonb.setdefault("diagnostic_only", True)
        self.metadata_jsonb.setdefault("not_truth", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        return self


class EventCandidate3DDiagnosticRead(EventCandidate3DDiagnosticCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class EventCandidate3DDiagnosticSummary(TOMBaseModel):
    available: bool
    event_candidate_run_id: str | None = None
    trajectory_3d_run_id: str | None = None
    camera_geometry_id: str | None = None
    diagnostic_count: int = 0
    hit_candidate_diagnostic_count: int = 0
    bounce_candidate_diagnostic_count: int = 0
    nearest_3d_sample_found_count: int = 0
    height_unknown_count: int = 0
    cannot_evaluate_count: int = 0
    supports_candidate_context_count: int = 0
    weakens_candidate_context_count: int = 0
    neutral_context_count: int = 0
    diagnostic_only: bool = True
    not_truth: bool = True
    not_3d_truth: bool = True
    no_adjudication: bool = True


def validate_diagnostic_status(status: str) -> str:
    if status in TRUTH_LIKE_EVENT_3D_LABELS:
        raise EventCandidate3DDiagnosticSchemaError(
            f"truth-like 3D diagnostic status is not allowed: {status}"
        )
    if status not in {item.value for item in EventCandidate3DDiagnosticStatus}:
        raise EventCandidate3DDiagnosticSchemaError(
            f"invalid 3D diagnostic status: {status}"
        )
    return status


def validate_diagnostic_label(label: str) -> str:
    if label in TRUTH_LIKE_EVENT_3D_LABELS:
        raise EventCandidate3DDiagnosticSchemaError(
            f"truth-like 3D diagnostic label is not allowed: {label}"
        )
    if label not in {item.value for item in EventCandidate3DDiagnosticLabel}:
        raise EventCandidate3DDiagnosticSchemaError(f"invalid 3D diagnostic label: {label}")
    return label
