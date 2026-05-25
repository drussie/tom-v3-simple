from sqlalchemy.orm import Session
from tom_v3_schema.observations import (
    AtomicObservationCreate,
    DerivedObservationCreate,
    GameplayObservationCreate,
    ObservationCreate,
    ObservationLineageCreate,
)
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

from tom_v3_observations.writer import ObservationWriter


def create_synthetic_run(session: Session) -> dict[str, object]:
    runtime_config = RuntimeConfig(
        config_name="synthetic-dev-config",
        config_version="v0",
        payload_jsonb={"purpose": "milestone_0b_dev_persistence_check"},
    )
    model = ModelRegistry(
        name="synthetic-observation-generator",
        version="0.0.0",
        model_family="synthetic",
        source="dev",
        metadata_jsonb={"milestone": "0B"},
    )
    media = MediaAsset(
        source_uri="file:///dev/synthetic-tennis-clip.mp4",
        media_type="video",
        duration_ms=120_000,
        frame_count=3_600,
        fps=30.0,
        width=1920,
        height=1080,
        checksum="synthetic-dev",
        metadata_jsonb={"fixture": "synthetic"},
    )
    session.add_all([runtime_config, model, media])
    session.flush()

    run = ProcessingRun(
        media_id=media.id,
        run_name="synthetic-dev-run",
        run_status="completed",
        runtime_config_id=runtime_config.id,
        metadata_jsonb={"source": "POST /dev/synthetic-run"},
    )
    session.add(run)
    session.flush()

    step = ProcessingStep(
        run_id=run.id,
        step_name="synthetic-observation-seed",
        step_status="completed",
        runtime_config_id=runtime_config.id,
        metadata_jsonb={"scope": "backend-dev"},
    )
    session.add(step)
    session.commit()

    writer = ObservationWriter(session)
    gameplay = writer.write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="gameplay",
            observation_type="view_state",
            granularity="frame_range",
            frame_start=100,
            frame_end=300,
            timestamp_start_ms=3333,
            timestamp_end_ms=10000,
            confidence=0.93,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="none",
            payload_jsonb={"source": "synthetic"},
            idempotency_key=f"{run.id}:gameplay:100-300",
            gameplay=GameplayObservationCreate(
                view_state="gameplay",
                view_state_subtype="active_point",
                payload_jsonb={"reason_codes": ["synthetic_active_point"]},
            ),
        )
    )
    non_gameplay = writer.write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="gameplay",
            observation_type="view_state",
            granularity="frame_range",
            frame_start=301,
            frame_end=420,
            timestamp_start_ms=10033,
            timestamp_end_ms=14000,
            confidence=0.88,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="none",
            payload_jsonb={"source": "synthetic"},
            idempotency_key=f"{run.id}:non-gameplay:301-420",
            gameplay=GameplayObservationCreate(
                view_state="non_gameplay",
                view_state_subtype="between_points",
                payload_jsonb={"reason_codes": ["synthetic_between_points"]},
            ),
        )
    )
    ball = writer.write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="atomic",
            observation_type="ball_detection",
            granularity="frame",
            frame_start=120,
            frame_end=120,
            timestamp_start_ms=4000,
            timestamp_end_ms=4000,
            confidence=0.81,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={"bbox": [900, 420, 12, 12]},
            idempotency_key=f"{run.id}:ball:120",
            atomic=AtomicObservationCreate(
                atomic_kind="ball_detection",
                payload_jsonb={"center": [906, 426]},
            ),
            lineage=[
                ObservationLineageCreate(
                    parent_observation_id=gameplay.id,
                    relationship_type="scoped_by",
                    processing_step_id=step.id,
                )
            ],
        )
    )
    player = writer.write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="atomic",
            observation_type="player_detection",
            granularity="frame",
            frame_start=120,
            frame_end=120,
            timestamp_start_ms=4000,
            timestamp_end_ms=4000,
            confidence=0.9,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={"bbox": [760, 260, 160, 420], "subject_ref": "near_player"},
            idempotency_key=f"{run.id}:player:near:120",
            atomic=AtomicObservationCreate(
                atomic_kind="player_detection",
                payload_jsonb={"subject_ref": "near_player"},
            ),
            lineage=[
                ObservationLineageCreate(
                    parent_observation_id=gameplay.id,
                    relationship_type="scoped_by",
                    processing_step_id=step.id,
                )
            ],
        )
    )

    tracklet = Tracklet(
        media_id=media.id,
        run_id=run.id,
        track_family="ball",
        subject_ref="ball",
        frame_start=120,
        frame_end=123,
        confidence=0.79,
        observation_id=ball.id,
        metadata_jsonb={"source": "synthetic"},
    )
    session.add(tracklet)
    session.flush()
    session.add_all(
        [
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=ball.id,
                frame_number=120,
                timestamp_ms=4000,
                x=906,
                y=426,
                width=12,
                height=12,
                confidence=0.81,
                payload_jsonb={"source": "synthetic"},
            ),
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=ball.id,
                frame_number=121,
                timestamp_ms=4033,
                x=916,
                y=433,
                width=12,
                height=12,
                confidence=0.8,
                payload_jsonb={"source": "synthetic"},
            ),
        ]
    )
    session.commit()

    derived = writer.write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="derived",
            observation_type="bounce_candidate",
            granularity="frame",
            frame_start=122,
            frame_end=122,
            timestamp_start_ms=4067,
            timestamp_end_ms=4067,
            confidence=0.51,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={"candidate_source": "synthetic_placeholder"},
            idempotency_key=f"{run.id}:bounce-candidate:122",
            derived=DerivedObservationCreate(
                derived_kind="bounce_candidate",
                derivation_payload_jsonb={"note": "placeholder candidate only"},
            ),
            lineage=[
                ObservationLineageCreate(
                    parent_observation_id=ball.id,
                    relationship_type="derived_from",
                    processing_step_id=step.id,
                ),
                ObservationLineageCreate(
                    parent_observation_id=player.id,
                    relationship_type="grouped_with",
                    processing_step_id=step.id,
                ),
            ],
            artifacts=[
                {
                    "artifact_type": "overlay_frame",
                    "uri": "file:///dev/artifacts/synthetic-bounce-candidate-122.png",
                    "frame_start": 122,
                    "frame_end": 122,
                    "metadata_jsonb": {"source": "synthetic"},
                }
            ],
        )
    )

    return {
        "media_id": media.id,
        "runtime_config_id": runtime_config.id,
        "model_id": model.id,
        "run_id": run.id,
        "processing_step_id": step.id,
        "observation_ids": [gameplay.id, non_gameplay.id, ball.id, player.id, derived.id],
        "tracklet_id": tracklet.id,
        "artifact_count": len(derived.artifacts),
    }
