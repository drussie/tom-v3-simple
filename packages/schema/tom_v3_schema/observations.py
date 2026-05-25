from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.artifacts import EvidenceArtifactCreate, EvidenceArtifactRead
from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.enums import (
    AtomicKind,
    CoordinateSpace,
    DerivedKind,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
    ViewState,
    ViewStateSubtype,
)


class GameplayObservationCreate(TOMBaseModel):
    view_state: ViewState
    view_state_subtype: ViewStateSubtype | None = None
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class GameplayObservationRead(GameplayObservationCreate):
    observation_id: str


class AtomicObservationCreate(TOMBaseModel):
    atomic_kind: AtomicKind | str
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class AtomicObservationRead(AtomicObservationCreate):
    observation_id: str


class DerivedObservationCreate(TOMBaseModel):
    derived_kind: DerivedKind | str
    derivation_payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class DerivedObservationRead(DerivedObservationCreate):
    observation_id: str


class ObservationLineageCreate(TOMBaseModel):
    parent_observation_id: str
    relationship_type: RelationshipType
    processing_step_id: str | None = None
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class ObservationLineageRead(ObservationLineageCreate):
    id: str
    child_observation_id: str
    created_at: datetime


class ObservationCreate(TOMBaseModel):
    media_id: str
    run_id: str
    observation_family: ObservationFamily | str
    observation_type: str
    granularity: ObservationGranularity | str
    frame_start: int | None = None
    frame_end: int | None = None
    timestamp_start_ms: int | None = None
    timestamp_end_ms: int | None = None
    confidence: float | None = None
    model_id: str | None = None
    runtime_config_id: str | None = None
    coordinate_space: CoordinateSpace | str | None = CoordinateSpace.none
    schema_version: int = 1
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None
    gameplay: GameplayObservationCreate | None = None
    atomic: AtomicObservationCreate | None = None
    derived: DerivedObservationCreate | None = None
    lineage: list[ObservationLineageCreate] = Field(default_factory=list)
    artifacts: list[EvidenceArtifactCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_frame_and_time_ranges(self) -> "ObservationCreate":
        if (
            self.frame_start is not None
            and self.frame_end is not None
            and self.frame_end < self.frame_start
        ):
            raise ValueError("frame_end must be greater than or equal to frame_start")
        if (
            self.timestamp_start_ms is not None
            and self.timestamp_end_ms is not None
            and self.timestamp_end_ms < self.timestamp_start_ms
        ):
            raise ValueError("timestamp_end_ms must be greater than or equal to timestamp_start_ms")
        return self


class ObservationCoreRead(TOMBaseModel):
    id: str
    media_id: str
    run_id: str
    observation_family: str
    observation_type: str
    granularity: str
    frame_start: int | None = None
    frame_end: int | None = None
    timestamp_start_ms: int | None = None
    timestamp_end_ms: int | None = None
    confidence: float | None = None
    model_id: str | None = None
    runtime_config_id: str | None = None
    coordinate_space: str | None = None
    schema_version: int
    payload_jsonb: dict[str, Any]
    idempotency_key: str | None = None
    created_at: datetime


class ObservationDetailRead(ObservationCoreRead):
    gameplay: GameplayObservationRead | None = None
    atomic: AtomicObservationRead | None = None
    derived: DerivedObservationRead | None = None
    artifacts: list[EvidenceArtifactRead] = Field(default_factory=list)


class ObservationBatchCreate(TOMBaseModel):
    observations: list[ObservationCreate]


class ObservationBatchRead(TOMBaseModel):
    observations: list[ObservationDetailRead]


class ObservationQueryFilters(TOMBaseModel):
    media_id: str | None = None
    run_id: str | None = None
    observation_family: str | None = None
    observation_type: str | None = None
    frame_start_gte: int | None = None
    frame_end_lte: int | None = None
    timestamp_start_gte: int | None = None
    timestamp_end_lte: int | None = None
    confidence_gte: float | None = None
    confidence_lte: float | None = None
    gameplay_label: ViewState | None = None
    tracklet_id: str | None = None
    limit: int = Field(default=100, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class ObservationQueryResponse(TOMBaseModel):
    count: int
    observations: list[ObservationDetailRead]


class ObservationLineageResponse(TOMBaseModel):
    parents: list[ObservationLineageRead]
    children: list[ObservationLineageRead]


class TrackPointCreate(TOMBaseModel):
    observation_id: str | None = None
    frame_number: int
    timestamp_ms: int | None = None
    x: float
    y: float
    width: float | None = None
    height: float | None = None
    confidence: float | None = None
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class TrackletCreate(TOMBaseModel):
    media_id: str
    run_id: str
    track_family: str
    subject_ref: str | None = None
    frame_start: int | None = None
    frame_end: int | None = None
    confidence: float | None = None
    observation_id: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)
    points: list[TrackPointCreate] = Field(default_factory=list)


class TrackPointRead(TrackPointCreate):
    id: str
    tracklet_id: str


class TrackletRead(TrackletCreate):
    id: str
    points: list[TrackPointRead] = Field(default_factory=list)
