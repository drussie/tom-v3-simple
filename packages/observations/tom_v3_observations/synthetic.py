from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_schema.observations import (
    AtomicObservationCreate,
    DerivedObservationCreate,
    GameplayObservationCreate,
    ObservationCreate,
    ObservationLineageCreate,
)
from tom_v3_storage.db_models import (
    EvidenceArtifact,
    GameplayObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

from tom_v3_observations.writer import ObservationWriter

BASELINE_SCENARIO_NAME = "baseline-tennis-clip"


@dataclass(frozen=True)
class SyntheticMediaFixture:
    source_uri: str = "file:///dev/synthetic-tennis-clip.mp4"
    media_type: str = "video"
    duration_ms: int = 120_000
    frame_count: int = 3_600
    fps: float = 30.0
    width: int = 1920
    height: int = 1080
    checksum: str = "synthetic-dev"


@dataclass(frozen=True)
class SyntheticScenario:
    name: str
    media: SyntheticMediaFixture = field(default_factory=SyntheticMediaFixture)
    runtime_config_name: str = "synthetic-baseline-config"
    runtime_config_version: str = "v0"
    model_name: str = "synthetic-observation-generator"
    model_version: str = "0.1.0"
    run_name: str = "synthetic-baseline-run"
    processing_steps: tuple[str, ...] = (
        "synthetic_media_indexing",
        "synthetic_gameplay_classification",
        "synthetic_detection_generation",
        "synthetic_tracking_generation",
        "synthetic_homography_generation",
        "synthetic_candidate_generation",
        "synthetic_artifact_generation",
    )


def baseline_tennis_clip_scenario(
    source_uri: str | None = None,
    run_name: str | None = None,
) -> SyntheticScenario:
    media = SyntheticMediaFixture(source_uri=source_uri or SyntheticMediaFixture().source_uri)
    return SyntheticScenario(
        name=BASELINE_SCENARIO_NAME,
        media=media,
        run_name=run_name or "synthetic-baseline-run",
    )


def create_synthetic_run(
    session: Session,
    scenario: str | SyntheticScenario = BASELINE_SCENARIO_NAME,
    source_uri: str | None = None,
    run_name: str | None = None,
    reuse_media: bool = False,
) -> dict[str, object]:
    scenario_def = scenario if isinstance(scenario, SyntheticScenario) else get_scenario(scenario)
    if source_uri or run_name:
        scenario_def = baseline_tennis_clip_scenario(
            source_uri=source_uri or scenario_def.media.source_uri,
            run_name=run_name or scenario_def.run_name,
        )
    return seed_synthetic_run(session, scenario_def, reuse_media=reuse_media)


def get_scenario(name: str) -> SyntheticScenario:
    if name != BASELINE_SCENARIO_NAME:
        raise ValueError(f"unknown synthetic scenario: {name}")
    return baseline_tennis_clip_scenario()


def seed_synthetic_run(
    session: Session,
    scenario: SyntheticScenario,
    reuse_media: bool = False,
) -> dict[str, object]:
    media = _create_media(session, scenario, reuse_media=reuse_media)
    runtime_config = _create_runtime_config(session, scenario)
    model = _create_model(session, scenario)
    run = _create_run(session, scenario, media, runtime_config)
    steps = _create_processing_steps(session, scenario, run, runtime_config)

    writer = ObservationWriter(session)
    context = _SeedContext(
        session=session,
        writer=writer,
        scenario=scenario,
        media=media,
        runtime_config=runtime_config,
        model=model,
        run=run,
        steps=steps,
    )

    gameplay = _write_gameplay_segments(context)
    homography = _write_homography_placeholders(context, gameplay)
    ball = _write_ball_track(context, gameplay, homography)
    near_player = _write_player_track(context, gameplay, subject_ref="near_player")
    far_player = _write_player_track(context, gameplay, subject_ref="far_player")
    candidates = _write_candidates(context, gameplay, homography, ball, near_player, far_player)

    return _build_seed_result(
        session=session,
        scenario=scenario,
        media=media,
        runtime_config=runtime_config,
        model=model,
        run=run,
        steps=steps,
        gameplay=gameplay,
        homography=homography,
        ball=ball,
        near_player=near_player,
        far_player=far_player,
        candidates=candidates,
    )


def verify_synthetic_run(session: Session, run_id: str) -> dict[str, object]:
    view_state_rows = session.execute(
        select(GameplayObservation.view_state, func.count())
        .join(Observation, Observation.id == GameplayObservation.observation_id)
        .where(Observation.run_id == run_id)
        .group_by(GameplayObservation.view_state)
    ).all()
    view_state_counts = {row[0]: row[1] for row in view_state_rows}
    observation_type_counts = _observation_type_counts(session, run_id)
    tracklet_count = _count(
        session,
        select(func.count()).select_from(Tracklet).where(Tracklet.run_id == run_id),
    )
    track_point_count = _count_track_points(session, run_id)
    lineage_count = _count_lineage(session, run_id)
    artifact_count = _count(
        session,
        select(func.count())
        .select_from(EvidenceArtifact)
        .where(EvidenceArtifact.run_id == run_id),
    )
    checks = {
        "gameplay_observations": view_state_counts.get("gameplay", 0) >= 2,
        "non_gameplay_observations": view_state_counts.get("non_gameplay", 0) >= 1,
        "uncertain_observations": view_state_counts.get("uncertain", 0) >= 1,
        "ball_observations": observation_type_counts.get("ball_detection", 0) >= 4,
        "player_observations": observation_type_counts.get("player_detection", 0) >= 4,
        "homography_placeholders": observation_type_counts.get("homography_placeholder", 0) >= 2,
        "bounce_candidates": observation_type_counts.get("bounce_candidate", 0) >= 1,
        "tracking_gap_candidates": observation_type_counts.get("tracking_gap_candidate", 0) >= 1,
        "tracklets": tracklet_count >= 3,
        "track_points": track_point_count >= 10,
        "lineage": lineage_count >= 8,
        "artifacts": artifact_count >= 3,
    }
    return {
        "run_id": run_id,
        "ok": all(checks.values()),
        "checks": checks,
        "view_state_counts": view_state_counts,
        "observation_type_counts": observation_type_counts,
        "tracklet_count": tracklet_count,
        "track_point_count": track_point_count,
        "lineage_count": lineage_count,
        "artifact_count": artifact_count,
    }


@dataclass
class _SeedContext:
    session: Session
    writer: ObservationWriter
    scenario: SyntheticScenario
    media: MediaAsset
    runtime_config: RuntimeConfig
    model: ModelRegistry
    run: ProcessingRun
    steps: dict[str, ProcessingStep]


@dataclass
class _TrackSeed:
    tracklet: Tracklet
    observations_by_frame: dict[int, str]


def _create_media(
    session: Session, scenario: SyntheticScenario, reuse_media: bool
) -> MediaAsset:
    if reuse_media:
        media = session.scalar(
            select(MediaAsset).where(
                MediaAsset.source_uri == scenario.media.source_uri,
                MediaAsset.checksum == scenario.media.checksum,
            )
        )
        if media is not None:
            return media

    media = MediaAsset(
        source_uri=scenario.media.source_uri,
        media_type=scenario.media.media_type,
        duration_ms=scenario.media.duration_ms,
        frame_count=scenario.media.frame_count,
        fps=scenario.media.fps,
        width=scenario.media.width,
        height=scenario.media.height,
        checksum=scenario.media.checksum,
        metadata_jsonb={
            "scenario": scenario.name,
            "synthetic": True,
            "note": "metadata fixture only; no real video file required",
        },
    )
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


def _create_runtime_config(session: Session, scenario: SyntheticScenario) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name=scenario.runtime_config_name,
        config_version=scenario.runtime_config_version,
        payload_jsonb={
            "scenario": scenario.name,
            "seed_version": "0C",
            "rerun_behavior": "new processing run by default",
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_model(session: Session, scenario: SyntheticScenario) -> ModelRegistry:
    model = ModelRegistry(
        name=scenario.model_name,
        version=scenario.model_version,
        model_family="synthetic",
        source="apps.worker.synthetic_seed",
        metadata_jsonb={"scenario": scenario.name, "milestone": "0C"},
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_run(
    session: Session,
    scenario: SyntheticScenario,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media.id,
        run_name=scenario.run_name,
        run_status="completed",
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "scenario": scenario.name,
            "source": "worker synthetic seeder",
            "rerun_behavior": "new run",
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_processing_steps(
    session: Session,
    scenario: SyntheticScenario,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
) -> dict[str, ProcessingStep]:
    steps: dict[str, ProcessingStep] = {}
    for step_name in scenario.processing_steps:
        step = ProcessingStep(
            run_id=run.id,
            step_name=step_name,
            step_status="completed",
            runtime_config_id=runtime_config.id,
            metadata_jsonb={"scenario": scenario.name, "synthetic": True},
        )
        session.add(step)
        steps[step_name] = step
    session.commit()
    for step in steps.values():
        session.refresh(step)
    return steps


def _write_gameplay_segments(context: _SeedContext) -> dict[str, str]:
    segments = [
        ("gameplay_100_800", "gameplay", "active_point", 100, 800, 0.96),
        ("non_gameplay_801_950", "non_gameplay", "between_points", 801, 950, 0.9),
        ("uncertain_951_1050", "uncertain", "camera_cut", 951, 1050, 0.57),
        ("gameplay_1051_1500", "gameplay", "active_point", 1051, 1500, 0.94),
    ]
    ids: dict[str, str] = {}
    for key, view_state, subtype, start, end, confidence in segments:
        observation = context.writer.write(
            ObservationCreate(
                media_id=context.media.id,
                run_id=context.run.id,
                observation_family="gameplay",
                observation_type="view_state",
                granularity="frame_range",
                frame_start=start,
                frame_end=end,
                timestamp_start_ms=_timestamp_ms(start, context.scenario),
                timestamp_end_ms=_timestamp_ms(end, context.scenario),
                confidence=confidence,
                model_id=context.model.id,
                runtime_config_id=context.runtime_config.id,
                coordinate_space="none",
                payload_jsonb={
                    "scenario": context.scenario.name,
                    "viewer_row": "Gameplay",
                    "coverage_state": view_state,
                },
                idempotency_key=f"{context.run.id}:view-state:{start}-{end}",
                gameplay=GameplayObservationCreate(
                    view_state=view_state,
                    view_state_subtype=subtype,
                    payload_jsonb={
                        "reason_codes": [f"synthetic_{subtype}"],
                        "source": "synthetic scenario",
                    },
                ),
            )
        )
        ids[key] = observation.id
    return ids


def _write_homography_placeholders(
    context: _SeedContext, gameplay: dict[str, str]
) -> dict[str, str]:
    intervals = [
        ("homography_valid_100_800", "valid", 100, 800, 0.86, gameplay["gameplay_100_800"]),
        ("homography_missing_801_950", "missing", 801, 950, 0.0, gameplay["non_gameplay_801_950"]),
        ("homography_valid_1051_1500", "valid", 1051, 1500, 0.82, gameplay["gameplay_1051_1500"]),
    ]
    ids: dict[str, str] = {}
    for key, status, start, end, confidence, gameplay_id in intervals:
        observation = context.writer.write(
            ObservationCreate(
                media_id=context.media.id,
                run_id=context.run.id,
                observation_family="atomic",
                observation_type="homography_placeholder",
                granularity="frame_range",
                frame_start=start,
                frame_end=end,
                timestamp_start_ms=_timestamp_ms(start, context.scenario),
                timestamp_end_ms=_timestamp_ms(end, context.scenario),
                confidence=confidence,
                model_id=context.model.id,
                runtime_config_id=context.runtime_config.id,
                coordinate_space="court_plane",
                payload_jsonb={
                    "homography_status": status,
                    "matrix_3x3": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                    "court_space": "placeholder_court_2d",
                    "note": "synthetic placeholder only",
                    "viewer_row": "Homography",
                },
                idempotency_key=f"{context.run.id}:homography:{status}:{start}-{end}",
                atomic=AtomicObservationCreate(
                    atomic_kind="homography_placeholder",
                    payload_jsonb={"homography_status": status},
                ),
                lineage=[
                    ObservationLineageCreate(
                        parent_observation_id=gameplay_id,
                        relationship_type="scoped_by",
                        processing_step_id=context.steps["synthetic_homography_generation"].id,
                    )
                ],
            )
        )
        ids[key] = observation.id
    return ids


def _write_ball_track(
    context: _SeedContext, gameplay: dict[str, str], homography: dict[str, str]
) -> _TrackSeed:
    frames = [
        (120, 906, 426, 0.86),
        (240, 960, 452, 0.88),
        (360, 1015, 494, 0.82),
        (480, 1086, 536, 0.8),
        (600, 1160, 590, 0.78),
        (720, 1240, 640, 0.74),
        (780, 1284, 670, 0.44),
    ]
    observations_by_frame: dict[int, str] = {}
    for frame, x, y, confidence in frames:
        parent_gameplay = _gameplay_for_frame(gameplay, frame)
        observation = context.writer.write(
            ObservationCreate(
                media_id=context.media.id,
                run_id=context.run.id,
                observation_family="atomic",
                observation_type="ball_detection",
                granularity="frame",
                frame_start=frame,
                frame_end=frame,
                timestamp_start_ms=_timestamp_ms(frame, context.scenario),
                timestamp_end_ms=_timestamp_ms(frame, context.scenario),
                confidence=confidence,
                model_id=context.model.id,
                runtime_config_id=context.runtime_config.id,
                coordinate_space="image_pixels",
                payload_jsonb={
                    "center": [x, y],
                    "bbox": [x - 6, y - 6, 12, 12],
                    "viewer_row": "Ball track",
                    "coverage_state": "low_confidence" if confidence < 0.5 else "tracked",
                },
                idempotency_key=f"{context.run.id}:ball-detection:{frame}",
                atomic=AtomicObservationCreate(
                    atomic_kind="ball_detection",
                    payload_jsonb={"center": [x, y], "radius_px": 6},
                ),
                lineage=[
                    ObservationLineageCreate(
                        parent_observation_id=parent_gameplay,
                        relationship_type="scoped_by",
                        processing_step_id=context.steps["synthetic_detection_generation"].id,
                    ),
                    ObservationLineageCreate(
                        parent_observation_id=homography["homography_valid_100_800"],
                        relationship_type="projected_using",
                        processing_step_id=context.steps["synthetic_detection_generation"].id,
                    ),
                ],
            )
        )
        observations_by_frame[frame] = observation.id

    tracklet = _create_tracklet(
        context=context,
        track_family="ball",
        subject_ref="ball",
        frame_start=120,
        frame_end=780,
        confidence=0.77,
        observation_id=observations_by_frame[120],
        metadata={
            "viewer_row": "Ball track",
            "coverage_segments": [
                {"state": "tracked", "frame_start": 120, "frame_end": 500},
                {"state": "gap", "frame_start": 501, "frame_end": 580},
                {"state": "tracked", "frame_start": 581, "frame_end": 760},
                {"state": "low_confidence", "frame_start": 761, "frame_end": 800},
            ],
        },
    )
    _add_track_points(context, tracklet, observations_by_frame, frames)
    return _TrackSeed(tracklet=tracklet, observations_by_frame=observations_by_frame)


def _write_player_track(
    context: _SeedContext, gameplay: dict[str, str], subject_ref: str
) -> _TrackSeed:
    if subject_ref == "near_player":
        frames = [
            (120, 760, 260, 160, 420, 0.91),
            (360, 785, 270, 158, 418, 0.9),
            (600, 810, 285, 162, 415, 0.86),
            (820, 830, 300, 160, 410, 0.78),
        ]
        coverage_segments = [
            {"state": "tracked", "frame_start": 100, "frame_end": 700},
            {"state": "gap", "frame_start": 701, "frame_end": 760},
            {"state": "tracked", "frame_start": 761, "frame_end": 950},
        ]
    else:
        frames = [
            (300, 1160, 190, 140, 365, 0.82),
            (600, 1130, 200, 145, 370, 0.84),
            (900, 1100, 210, 145, 372, 0.72),
            (1200, 1060, 220, 148, 375, 0.79),
        ]
        coverage_segments = [
            {"state": "gap", "frame_start": 100, "frame_end": 240},
            {"state": "tracked", "frame_start": 241, "frame_end": 900},
            {"state": "tracked", "frame_start": 901, "frame_end": 1500},
        ]

    observations_by_frame: dict[int, str] = {}
    for frame, x, y, width, height, confidence in frames:
        observation = context.writer.write(
            ObservationCreate(
                media_id=context.media.id,
                run_id=context.run.id,
                observation_family="atomic",
                observation_type="player_detection",
                granularity="frame",
                frame_start=frame,
                frame_end=frame,
                timestamp_start_ms=_timestamp_ms(frame, context.scenario),
                timestamp_end_ms=_timestamp_ms(frame, context.scenario),
                confidence=confidence,
                model_id=context.model.id,
                runtime_config_id=context.runtime_config.id,
                coordinate_space="image_pixels",
                payload_jsonb={
                    "bbox": [x, y, width, height],
                    "subject_ref": subject_ref,
                    "viewer_row": "Near player" if subject_ref == "near_player" else "Far player",
                    "coverage_state": "tracked",
                },
                idempotency_key=f"{context.run.id}:player-detection:{subject_ref}:{frame}",
                atomic=AtomicObservationCreate(
                    atomic_kind="player_detection",
                    payload_jsonb={"subject_ref": subject_ref, "bbox": [x, y, width, height]},
                ),
                lineage=[
                    ObservationLineageCreate(
                        parent_observation_id=_gameplay_for_frame(gameplay, frame),
                        relationship_type="scoped_by",
                        processing_step_id=context.steps["synthetic_detection_generation"].id,
                    )
                ],
            )
        )
        observations_by_frame[frame] = observation.id

    tracklet = _create_tracklet(
        context=context,
        track_family="player",
        subject_ref=subject_ref,
        frame_start=min(observations_by_frame),
        frame_end=max(observations_by_frame),
        confidence=0.84,
        observation_id=next(iter(observations_by_frame.values())),
        metadata={
            "viewer_row": "Near player" if subject_ref == "near_player" else "Far player",
            "coverage_segments": coverage_segments,
        },
    )
    point_rows = [
        (frame, x + width / 2, y + height, width, height, confidence)
        for frame, x, y, width, height, confidence in frames
    ]
    _add_track_points(context, tracklet, observations_by_frame, point_rows)
    return _TrackSeed(tracklet=tracklet, observations_by_frame=observations_by_frame)


def _write_candidates(
    context: _SeedContext,
    gameplay: dict[str, str],
    homography: dict[str, str],
    ball: _TrackSeed,
    near_player: _TrackSeed,
    far_player: _TrackSeed,
) -> dict[str, str]:
    bounce = context.writer.write(
        ObservationCreate(
            media_id=context.media.id,
            run_id=context.run.id,
            observation_family="derived",
            observation_type="bounce_candidate",
            granularity="frame",
            frame_start=420,
            frame_end=420,
            timestamp_start_ms=_timestamp_ms(420, context.scenario),
            timestamp_end_ms=_timestamp_ms(420, context.scenario),
            confidence=0.58,
            model_id=context.model.id,
            runtime_config_id=context.runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={
                "candidate_marker": "bounce_candidate",
                "viewer_row": "Candidates",
                "note": "synthetic candidate only",
            },
            idempotency_key=f"{context.run.id}:candidate:bounce:420",
            derived=DerivedObservationCreate(
                derived_kind="bounce_candidate",
                derivation_payload_jsonb={
                    "supporting_frames": [360, 480],
                    "synthetic_only": True,
                },
            ),
            lineage=[
                _lineage(ball.observations_by_frame[360], "derived_from", context, "candidate"),
                _lineage(ball.observations_by_frame[480], "derived_from", context, "candidate"),
                _lineage(gameplay["gameplay_100_800"], "scoped_by", context, "candidate"),
                _lineage(
                    homography["homography_valid_100_800"],
                    "projected_using",
                    context,
                    "candidate",
                ),
            ],
            artifacts=[
                _artifact(
                    "overlay_frame",
                    "file:///dev/artifacts/synthetic/bounce-420-overlay.png",
                    420,
                ),
                _artifact(
                    "overlay_clip",
                    "file:///dev/artifacts/synthetic/bounce-420-clip.mp4",
                    390,
                    450,
                ),
                _artifact(
                    "trajectory_plot",
                    "file:///dev/artifacts/synthetic/ball-trajectory-420.png",
                    360,
                    480,
                ),
            ],
        )
    )

    tracking_gap = context.writer.write(
        ObservationCreate(
            media_id=context.media.id,
            run_id=context.run.id,
            observation_family="derived",
            observation_type="tracking_gap_candidate",
            granularity="frame_range",
            frame_start=501,
            frame_end=580,
            timestamp_start_ms=_timestamp_ms(501, context.scenario),
            timestamp_end_ms=_timestamp_ms(580, context.scenario),
            confidence=0.97,
            model_id=context.model.id,
            runtime_config_id=context.runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={
                "candidate_marker": "tracking_gap_candidate",
                "viewer_row": "Ball track",
                "track_family": "ball",
                "missingness_state": "gap",
                "note": "synthetic missingness interval",
            },
            idempotency_key=f"{context.run.id}:candidate:tracking-gap:501-580",
            derived=DerivedObservationCreate(
                derived_kind="tracking_gap_candidate",
                derivation_payload_jsonb={
                    "tracklet_id": ball.tracklet.id,
                    "gap_frame_start": 501,
                    "gap_frame_end": 580,
                },
            ),
            lineage=[
                _lineage(ball.observations_by_frame[480], "tracked_from", context, "candidate"),
                _lineage(ball.observations_by_frame[600], "tracked_from", context, "candidate"),
                _lineage(gameplay["gameplay_100_800"], "scoped_by", context, "candidate"),
            ],
            artifacts=[
                _artifact(
                    "debug_json",
                    "file:///dev/artifacts/synthetic/ball-track-debug.json",
                    501,
                    580,
                ),
                _artifact(
                    "timeline_export",
                    "file:///dev/artifacts/synthetic/timeline-gap-501-580.json",
                    501,
                    580,
                ),
            ],
        )
    )

    hit = context.writer.write(
        ObservationCreate(
            media_id=context.media.id,
            run_id=context.run.id,
            observation_family="derived",
            observation_type="hit_candidate",
            granularity="frame",
            frame_start=610,
            frame_end=610,
            timestamp_start_ms=_timestamp_ms(610, context.scenario),
            timestamp_end_ms=_timestamp_ms(610, context.scenario),
            confidence=0.49,
            model_id=context.model.id,
            runtime_config_id=context.runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb={
                "candidate_marker": "hit_candidate",
                "viewer_row": "Candidates",
                "note": "synthetic candidate only",
            },
            idempotency_key=f"{context.run.id}:candidate:hit:610",
            derived=DerivedObservationCreate(
                derived_kind="hit_candidate",
                derivation_payload_jsonb={"supporting_frames": [600], "synthetic_only": True},
            ),
            lineage=[
                _lineage(ball.observations_by_frame[600], "derived_from", context, "candidate"),
                _lineage(
                    near_player.observations_by_frame[600],
                    "grouped_with",
                    context,
                    "candidate",
                ),
                _lineage(
                    far_player.observations_by_frame[600],
                    "grouped_with",
                    context,
                    "candidate",
                ),
                _lineage(gameplay["gameplay_100_800"], "scoped_by", context, "candidate"),
            ],
            artifacts=[
                _artifact(
                    "overlay_frame",
                    "file:///dev/artifacts/synthetic/hit-610-overlay.png",
                    610,
                ),
            ],
        )
    )
    return {
        "bounce_candidate": bounce.id,
        "tracking_gap_candidate": tracking_gap.id,
        "hit_candidate": hit.id,
    }


def _create_tracklet(
    context: _SeedContext,
    track_family: str,
    subject_ref: str,
    frame_start: int,
    frame_end: int,
    confidence: float,
    observation_id: str,
    metadata: dict[str, Any],
) -> Tracklet:
    tracklet = Tracklet(
        media_id=context.media.id,
        run_id=context.run.id,
        track_family=track_family,
        subject_ref=subject_ref,
        frame_start=frame_start,
        frame_end=frame_end,
        confidence=confidence,
        observation_id=observation_id,
        metadata_jsonb={
            "scenario": context.scenario.name,
            "synthetic": True,
            **metadata,
        },
    )
    context.session.add(tracklet)
    context.session.commit()
    context.session.refresh(tracklet)
    return tracklet


def _add_track_points(
    context: _SeedContext,
    tracklet: Tracklet,
    observations_by_frame: dict[int, str],
    rows: list[
        tuple[int, float, float, float, float | None]
        | tuple[int, float, float, float, float, float]
    ],
) -> None:
    points: list[TrackPoint] = []
    for row in rows:
        if len(row) == 4:
            frame, x, y, confidence = row
            width = 12.0
            height = 12.0
        else:
            frame, x, y, width, height, confidence = row
        points.append(
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=observations_by_frame[int(frame)],
                frame_number=int(frame),
                timestamp_ms=_timestamp_ms(int(frame), context.scenario),
                x=float(x),
                y=float(y),
                width=float(width) if width is not None else None,
                height=float(height) if height is not None else None,
                confidence=float(confidence),
                payload_jsonb={
                    "scenario": context.scenario.name,
                    "synthetic": True,
                    "coverage_state": "low_confidence" if float(confidence) < 0.5 else "tracked",
                },
            )
        )
    context.session.add_all(points)
    context.session.commit()


def _build_seed_result(
    session: Session,
    scenario: SyntheticScenario,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    model: ModelRegistry,
    run: ProcessingRun,
    steps: dict[str, ProcessingStep],
    gameplay: dict[str, str],
    homography: dict[str, str],
    ball: _TrackSeed,
    near_player: _TrackSeed,
    far_player: _TrackSeed,
    candidates: dict[str, str],
) -> dict[str, object]:
    observation_ids_by_type = _observation_ids_by_type(session, run.id)
    return {
        "scenario": scenario.name,
        "seed_version": "0C",
        "rerun_behavior": "new_run_by_default",
        "media_id": media.id,
        "runtime_config_id": runtime_config.id,
        "model_id": model.id,
        "run_id": run.id,
        "processing_step_id": steps["synthetic_media_indexing"].id,
        "processing_step_ids": {name: step.id for name, step in steps.items()},
        "gameplay_observation_ids": gameplay,
        "homography_observation_ids": homography,
        "candidate_observation_ids": candidates,
        "observation_ids_by_type": observation_ids_by_type,
        "observation_ids": [
            observation_id
            for ids in observation_ids_by_type.values()
            for observation_id in ids
        ],
        "tracklet_id": ball.tracklet.id,
        "tracklet_ids": {
            "ball": ball.tracklet.id,
            "near_player": near_player.tracklet.id,
            "far_player": far_player.tracklet.id,
        },
        "track_point_count": _count_track_points(session, run.id),
        "artifact_count": _count(
            session,
            select(func.count())
            .select_from(EvidenceArtifact)
            .where(EvidenceArtifact.run_id == run.id),
        ),
        "lineage_count": _count_lineage(session, run.id),
        "verification": verify_synthetic_run(session, run.id),
    }


def _observation_ids_by_type(session: Session, run_id: str) -> dict[str, list[str]]:
    rows = session.execute(
        select(Observation.observation_type, Observation.id)
        .where(Observation.run_id == run_id)
        .order_by(Observation.frame_start, Observation.observation_type)
    ).all()
    grouped: dict[str, list[str]] = {}
    for observation_type, observation_id in rows:
        grouped.setdefault(observation_type, []).append(observation_id)
    return grouped


def _observation_type_counts(session: Session, run_id: str) -> dict[str, int]:
    rows = session.execute(
        select(Observation.observation_type, func.count())
        .where(Observation.run_id == run_id)
        .group_by(Observation.observation_type)
    ).all()
    return {row[0]: row[1] for row in rows}


def _count_track_points(session: Session, run_id: str) -> int:
    return _count(
        session,
        select(func.count())
        .select_from(TrackPoint)
        .join(Tracklet, Tracklet.id == TrackPoint.tracklet_id)
        .where(Tracklet.run_id == run_id),
    )


def _count_lineage(session: Session, run_id: str) -> int:
    child_ids = select(Observation.id).where(Observation.run_id == run_id)
    return _count(
        session,
        select(func.count())
        .select_from(ObservationLineage)
        .where(ObservationLineage.child_observation_id.in_(child_ids)),
    )


def _count(session: Session, stmt: Any) -> int:
    return int(session.scalar(stmt) or 0)


def _timestamp_ms(frame: int, scenario: SyntheticScenario) -> int:
    return round(frame * 1000 / scenario.media.fps)


def _gameplay_for_frame(gameplay: dict[str, str], frame: int) -> str:
    if 100 <= frame <= 800:
        return gameplay["gameplay_100_800"]
    if 801 <= frame <= 950:
        return gameplay["non_gameplay_801_950"]
    if 951 <= frame <= 1050:
        return gameplay["uncertain_951_1050"]
    return gameplay["gameplay_1051_1500"]


def _lineage(
    parent_observation_id: str,
    relationship_type: str,
    context: _SeedContext,
    step_group: str,
) -> ObservationLineageCreate:
    step_name = {
        "candidate": "synthetic_candidate_generation",
        "tracking": "synthetic_tracking_generation",
        "artifact": "synthetic_artifact_generation",
    }.get(step_group, "synthetic_candidate_generation")
    return ObservationLineageCreate(
        parent_observation_id=parent_observation_id,
        relationship_type=relationship_type,
        processing_step_id=context.steps[step_name].id,
        payload_jsonb={"scenario": context.scenario.name, "synthetic": True},
    )


def _artifact(
    artifact_type: str,
    uri: str,
    frame_start: int,
    frame_end: int | None = None,
) -> dict[str, Any]:
    return {
        "artifact_type": artifact_type,
        "uri": uri,
        "frame_start": frame_start,
        "frame_end": frame_end or frame_start,
        "metadata_jsonb": {
            "synthetic": True,
            "note": "placeholder artifact metadata only",
        },
    }
