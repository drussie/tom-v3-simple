from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tom_v3_schema.artifacts import EvidenceArtifactRead
from tom_v3_schema.observations import (
    AtomicObservationRead,
    DerivedObservationRead,
    GameplayObservationRead,
    ObservationCreate,
    ObservationDetailRead,
)
from tom_v3_storage.db_models import (
    AtomicObservation,
    DerivedObservation,
    EvidenceArtifact,
    GameplayObservation,
    Observation,
    ObservationLineage,
)


class ObservationWriterError(ValueError):
    pass


def enum_value(value: Any) -> Any:
    return getattr(value, "value", value)


def artifact_read_from_model(artifact: EvidenceArtifact) -> EvidenceArtifactRead:
    return EvidenceArtifactRead.model_validate(artifact)


def observation_detail_from_model(observation: Observation) -> ObservationDetailRead:
    gameplay = None
    if observation.gameplay_detail is not None:
        gameplay = GameplayObservationRead.model_validate(observation.gameplay_detail)

    atomic = None
    if observation.atomic_detail is not None:
        atomic = AtomicObservationRead.model_validate(observation.atomic_detail)

    derived = None
    if observation.derived_detail is not None:
        derived = DerivedObservationRead.model_validate(observation.derived_detail)

    return ObservationDetailRead(
        id=observation.id,
        media_id=observation.media_id,
        run_id=observation.run_id,
        observation_family=observation.observation_family,
        observation_type=observation.observation_type,
        granularity=observation.granularity,
        frame_start=observation.frame_start,
        frame_end=observation.frame_end,
        timestamp_start_ms=observation.timestamp_start_ms,
        timestamp_end_ms=observation.timestamp_end_ms,
        confidence=observation.confidence,
        model_id=observation.model_id,
        runtime_config_id=observation.runtime_config_id,
        coordinate_space=observation.coordinate_space,
        schema_version=observation.schema_version,
        payload_jsonb=observation.payload_jsonb,
        idempotency_key=observation.idempotency_key,
        created_at=observation.created_at,
        gameplay=gameplay,
        atomic=atomic,
        derived=derived,
        artifacts=[artifact_read_from_model(artifact) for artifact in observation.artifacts],
    )


def get_observation_detail(session: Session, observation_id: str) -> ObservationDetailRead | None:
    observation = session.get(Observation, observation_id)
    if observation is None:
        return None
    return observation_detail_from_model(observation)


class ObservationWriter:
    def __init__(self, session: Session):
        self.session = session

    def write(self, request: ObservationCreate) -> ObservationDetailRead:
        if request.idempotency_key:
            existing = self._find_by_idempotency_key(request.idempotency_key)
            if existing is not None:
                return observation_detail_from_model(existing)

        self._validate_typed_extension(request)
        observation = Observation(
            media_id=request.media_id,
            run_id=request.run_id,
            observation_family=str(enum_value(request.observation_family)),
            observation_type=request.observation_type,
            granularity=str(enum_value(request.granularity)),
            frame_start=request.frame_start,
            frame_end=request.frame_end,
            timestamp_start_ms=request.timestamp_start_ms,
            timestamp_end_ms=request.timestamp_end_ms,
            confidence=request.confidence,
            model_id=request.model_id,
            runtime_config_id=request.runtime_config_id,
            coordinate_space=(
                str(enum_value(request.coordinate_space)) if request.coordinate_space else None
            ),
            schema_version=request.schema_version,
            payload_jsonb=request.payload_jsonb,
            idempotency_key=request.idempotency_key,
        )

        try:
            self.session.add(observation)
            self.session.flush()
            self._insert_typed_extension(observation, request)
            self._insert_lineage(observation, request)
            self._insert_artifacts(observation, request)
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            if request.idempotency_key:
                existing = self._find_by_idempotency_key(request.idempotency_key)
                if existing is not None:
                    return observation_detail_from_model(existing)
            raise ObservationWriterError(str(exc)) from exc

        self.session.refresh(observation)
        return observation_detail_from_model(observation)

    def write_many(self, requests: list[ObservationCreate]) -> list[ObservationDetailRead]:
        return [self.write(request) for request in requests]

    def _find_by_idempotency_key(self, idempotency_key: str) -> Observation | None:
        return self.session.scalar(
            select(Observation).where(Observation.idempotency_key == idempotency_key)
        )

    def _validate_typed_extension(self, request: ObservationCreate) -> None:
        typed_count = sum(
            detail is not None for detail in (request.gameplay, request.atomic, request.derived)
        )
        if typed_count > 1:
            raise ObservationWriterError(
                "only one typed observation extension can be written at once"
            )

        family = str(enum_value(request.observation_family))
        if request.gameplay is not None and family != "gameplay":
            raise ObservationWriterError("gameplay detail requires observation_family=gameplay")
        if request.atomic is not None and family != "atomic":
            raise ObservationWriterError("atomic detail requires observation_family=atomic")
        if request.derived is not None and family != "derived":
            raise ObservationWriterError("derived detail requires observation_family=derived")

    def _insert_typed_extension(
        self, observation: Observation, request: ObservationCreate
    ) -> None:
        if request.gameplay is not None:
            self.session.add(
                GameplayObservation(
                    observation_id=observation.id,
                    view_state=str(enum_value(request.gameplay.view_state)),
                    view_state_subtype=(
                        str(enum_value(request.gameplay.view_state_subtype))
                        if request.gameplay.view_state_subtype
                        else None
                    ),
                    payload_jsonb=request.gameplay.payload_jsonb,
                )
            )
        if request.atomic is not None:
            self.session.add(
                AtomicObservation(
                    observation_id=observation.id,
                    atomic_kind=str(enum_value(request.atomic.atomic_kind)),
                    payload_jsonb=request.atomic.payload_jsonb,
                )
            )
        if request.derived is not None:
            self.session.add(
                DerivedObservation(
                    observation_id=observation.id,
                    derived_kind=str(enum_value(request.derived.derived_kind)),
                    derivation_payload_jsonb=request.derived.derivation_payload_jsonb,
                )
            )

    def _insert_lineage(self, observation: Observation, request: ObservationCreate) -> None:
        for lineage in request.lineage:
            self.session.add(
                ObservationLineage(
                    child_observation_id=observation.id,
                    parent_observation_id=lineage.parent_observation_id,
                    relationship_type=str(enum_value(lineage.relationship_type)),
                    processing_step_id=lineage.processing_step_id,
                    payload_jsonb=lineage.payload_jsonb,
                )
            )

    def _insert_artifacts(self, observation: Observation, request: ObservationCreate) -> None:
        for artifact in request.artifacts:
            self.session.add(
                EvidenceArtifact(
                    media_id=artifact.media_id or observation.media_id,
                    run_id=artifact.run_id or observation.run_id,
                    target_observation_id=artifact.target_observation_id or observation.id,
                    artifact_type=artifact.artifact_type,
                    uri=artifact.uri,
                    frame_start=artifact.frame_start,
                    frame_end=artifact.frame_end,
                    timestamp_start_ms=artifact.timestamp_start_ms,
                    timestamp_end_ms=artifact.timestamp_end_ms,
                    checksum=artifact.checksum,
                    metadata_jsonb=artifact.metadata_jsonb,
                )
            )
