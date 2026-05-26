import argparse
import json
from collections.abc import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tom_v3_observations.synthetic import BASELINE_SCENARIO_NAME, verify_synthetic_run
from tom_v3_storage.db_models import Base

from apps.worker.config import settings
from apps.worker.pipelines.synthetic_seed import seed_synthetic_run
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
from apps.worker.services.gameplay_adapter import run_gameplay_adapter
from apps.worker.services.media_indexer import index_media
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run


def main() -> None:
    parser = argparse.ArgumentParser(prog="tom-v3-worker")
    subcommands = parser.add_subparsers(dest="command", required=True)

    seed_parser = subcommands.add_parser(
        "seed-synthetic-run",
        help="Seed a rich synthetic run for viewer/API development.",
    )
    seed_parser.add_argument("--scenario", default=BASELINE_SCENARIO_NAME)
    seed_parser.add_argument(
        "--source-uri",
        default="file:///dev/synthetic-tennis-clip.mp4",
    )
    seed_parser.add_argument("--run-name", default="synthetic-baseline-run")
    seed_parser.add_argument(
        "--reuse-media",
        action="store_true",
        help="Reuse an existing media asset with the same source URI and checksum.",
    )
    seed_parser.add_argument(
        "--skip-create-db",
        action="store_true",
        help="Do not create tables before seeding.",
    )
    seed_parser.set_defaults(handler=_handle_seed)

    verify_parser = subcommands.add_parser(
        "verify-synthetic-run",
        help="Verify that a seeded run has viewer-ready synthetic evidence.",
    )
    verify_parser.add_argument("--run-id", required=True)
    verify_parser.add_argument("--skip-create-db", action="store_true")
    verify_parser.set_defaults(handler=_handle_verify)

    index_parser = subcommands.add_parser(
        "index-media",
        help="Index a real local media file and create a media asset.",
    )
    index_parser.add_argument("--source-path", required=True)
    index_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Copy the source file into local TOM v3 media storage.",
    )
    index_parser.add_argument("--media-name")
    index_parser.add_argument("--storage-root", default=".data/media")
    index_parser.add_argument("--skip-create-db", action="store_true")
    index_parser.set_defaults(handler=_handle_index_media)

    gameplay_parser = subcommands.add_parser(
        "run-gameplay-adapter",
        help="Run a gameplay/view-state adapter for an indexed media asset.",
    )
    gameplay_parser.add_argument("--media-id", required=True)
    gameplay_parser.add_argument("--adapter", default="fixture", choices=["fixture", "tom-v1"])
    gameplay_parser.add_argument("--run-name", default="gameplay-adapter-run")
    gameplay_parser.add_argument("--config-name", default="gameplay-adapter-config")
    gameplay_parser.add_argument("--config-version", default="v0")
    gameplay_parser.add_argument("--tom-v1-path")
    gameplay_parser.add_argument("--window-seconds", type=float, default=2.0)
    gameplay_parser.add_argument("--stride-seconds", type=float, default=1.0)
    gameplay_parser.add_argument("--output-debug-artifact", action="store_true")
    gameplay_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_parser.set_defaults(handler=_handle_run_gameplay_adapter)

    index_gameplay_parser = subcommands.add_parser(
        "index-and-run-gameplay",
        help="Index a local media file, then run a gameplay adapter.",
    )
    index_gameplay_parser.add_argument("--source-path", required=True)
    index_gameplay_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    index_gameplay_parser.add_argument("--media-name")
    index_gameplay_parser.add_argument("--storage-root", default=".data/media")
    index_gameplay_parser.add_argument(
        "--adapter", default="fixture", choices=["fixture", "tom-v1"]
    )
    index_gameplay_parser.add_argument("--run-name", default="gameplay-adapter-run")
    index_gameplay_parser.add_argument("--config-name", default="gameplay-adapter-config")
    index_gameplay_parser.add_argument("--config-version", default="v0")
    index_gameplay_parser.add_argument("--tom-v1-path")
    index_gameplay_parser.add_argument("--window-seconds", type=float, default=2.0)
    index_gameplay_parser.add_argument("--stride-seconds", type=float, default=1.0)
    index_gameplay_parser.add_argument("--output-debug-artifact", action="store_true")
    index_gameplay_parser.add_argument("--skip-create-db", action="store_true")
    index_gameplay_parser.set_defaults(handler=_handle_index_and_run_gameplay)

    detection_parser = subcommands.add_parser(
        "run-detection-adapter",
        help="Run a ball/player detection adapter for an indexed media asset.",
    )
    detection_parser.add_argument("--media-id", required=True)
    detection_parser.add_argument("--adapter", default="fixture", choices=["fixture", "yolo"])
    detection_parser.add_argument("--model-path")
    detection_parser.add_argument("--device")
    detection_parser.add_argument("--image-size", type=int)
    detection_parser.add_argument("--confidence-threshold", type=float, default=0.25)
    detection_parser.add_argument("--frame-sample-rate", type=int, default=30)
    detection_parser.add_argument("--max-frames", type=int, default=5)
    detection_parser.add_argument("--gameplay-run-id")
    detection_parser.add_argument("--run-name", default="detection-adapter-run")
    detection_parser.add_argument("--config-name", default="detection-adapter-config")
    detection_parser.add_argument("--config-version", default="v0")
    detection_parser.add_argument("--output-debug-artifact", action="store_true")
    detection_parser.add_argument("--skip-create-db", action="store_true")
    detection_parser.set_defaults(handler=_handle_run_detection_adapter)

    index_detection_parser = subcommands.add_parser(
        "index-and-run-detection",
        help="Index a local media file, then run a detection adapter.",
    )
    index_detection_parser.add_argument("--source-path", required=True)
    index_detection_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    index_detection_parser.add_argument("--media-name")
    index_detection_parser.add_argument("--storage-root", default=".data/media")
    index_detection_parser.add_argument(
        "--adapter", default="fixture", choices=["fixture", "yolo"]
    )
    index_detection_parser.add_argument("--model-path")
    index_detection_parser.add_argument("--device")
    index_detection_parser.add_argument("--image-size", type=int)
    index_detection_parser.add_argument("--confidence-threshold", type=float, default=0.25)
    index_detection_parser.add_argument("--frame-sample-rate", type=int, default=30)
    index_detection_parser.add_argument("--max-frames", type=int, default=5)
    index_detection_parser.add_argument("--gameplay-run-id")
    index_detection_parser.add_argument("--run-name", default="detection-adapter-run")
    index_detection_parser.add_argument("--config-name", default="detection-adapter-config")
    index_detection_parser.add_argument("--config-version", default="v0")
    index_detection_parser.add_argument("--output-debug-artifact", action="store_true")
    index_detection_parser.add_argument("--skip-create-db", action="store_true")
    index_detection_parser.set_defaults(handler=_handle_index_and_run_detection)

    frame_artifacts_parser = subcommands.add_parser(
        "extract-frame-artifacts",
        help="Extract frame image artifacts for detection observations in a run.",
    )
    frame_artifacts_parser.add_argument("--run-id", required=True)
    frame_artifacts_parser.add_argument("--observation-id")
    frame_artifacts_parser.add_argument(
        "--observation-type",
        action="append",
        choices=["ball_detection", "player_detection"],
        help="Limit extraction to an observation type. May be supplied more than once.",
    )
    frame_artifacts_parser.add_argument("--max-frames", type=int)
    frame_artifacts_parser.add_argument("--output-root", default=".data/artifacts")
    frame_artifacts_parser.add_argument("--image-format", default="jpg")
    frame_artifacts_parser.add_argument("--overwrite", action="store_true")
    frame_artifacts_parser.add_argument("--skip-create-db", action="store_true")
    frame_artifacts_parser.set_defaults(handler=_handle_extract_frame_artifacts)

    tracklet_parser = subcommands.add_parser(
        "build-tracklets",
        help="Build candidate tracklets from persisted detection observations.",
    )
    tracklet_parser.add_argument("--detection-run-id", required=True)
    tracklet_parser.add_argument("--run-name", default="tracklet-builder-run")
    tracklet_parser.add_argument("--config-name", default="tracklet-builder-config")
    tracklet_parser.add_argument("--config-version", default="v0")
    tracklet_parser.add_argument("--max-gap-frames", type=int, default=30)
    tracklet_parser.add_argument("--max-center-distance-px", type=float, default=120.0)
    tracklet_parser.add_argument("--grouping-method", default="simple-frame-gap")
    tracklet_parser.add_argument(
        "--include-ball",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    tracklet_parser.add_argument(
        "--include-players",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    tracklet_parser.add_argument("--skip-create-db", action="store_true")
    tracklet_parser.set_defaults(handler=_handle_build_tracklets)

    args = parser.parse_args()
    with _session_factory(create_db=not args.skip_create_db)() as session:
        result = args.handler(session, args)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("ok") is False:
        raise SystemExit(1)


def _session_factory(create_db: bool) -> Callable[[], Session]:
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
    if create_db:
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def _handle_seed(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return seed_synthetic_run(
        session=session,
        scenario_name=args.scenario,
        source_uri=args.source_uri,
        run_name=args.run_name,
        reuse_media=args.reuse_media,
    )


def _handle_verify(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return verify_synthetic_run(session, args.run_id)


def _handle_index_media(session: Session, args: argparse.Namespace) -> dict[str, object]:
    media = index_media(
        session=session,
        source_path=args.source_path,
        copy_to_storage=args.copy_to_storage,
        media_name=args.media_name,
        storage_root=args.storage_root,
    )
    return {
        "media_id": media.id,
        "source_uri": media.source_uri,
        "stored_uri": media.metadata_jsonb.get("stored_uri"),
        "stored_path": media.metadata_jsonb.get("stored_path"),
        "storage_mode": media.metadata_jsonb.get("storage_mode"),
        "checksum": media.checksum,
        "checksum_algorithm": media.metadata_jsonb.get("checksum_algorithm"),
        "fps": media.fps,
        "frame_count": media.frame_count,
        "duration_ms": media.duration_ms,
        "width": media.width,
        "height": media.height,
        "frame_time_summary": media.metadata_jsonb.get("frame_time_index"),
    }


def _handle_run_gameplay_adapter(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return run_gameplay_adapter(
        session=session,
        media_id=args.media_id,
        adapter_name=args.adapter,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        tom_v1_path=args.tom_v1_path,
        output_debug_artifact=args.output_debug_artifact,
        window_seconds=args.window_seconds,
        stride_seconds=args.stride_seconds,
    )


def _handle_index_and_run_gameplay(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    media = index_media(
        session=session,
        source_path=args.source_path,
        copy_to_storage=args.copy_to_storage,
        media_name=args.media_name,
        storage_root=args.storage_root,
    )
    result = run_gameplay_adapter(
        session=session,
        media_id=media.id,
        adapter_name=args.adapter,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        tom_v1_path=args.tom_v1_path,
        output_debug_artifact=args.output_debug_artifact,
        window_seconds=args.window_seconds,
        stride_seconds=args.stride_seconds,
    )
    return {
        "indexed_media": {
            "media_id": media.id,
            "source_uri": media.source_uri,
            "stored_uri": media.metadata_jsonb.get("stored_uri"),
            "checksum": media.checksum,
        },
        **result,
    }


def _handle_run_detection_adapter(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return run_detection_adapter(
        session=session,
        media_id=args.media_id,
        adapter_name=args.adapter,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        model_path=args.model_path,
        device=args.device,
        image_size=args.image_size,
        confidence_threshold=args.confidence_threshold,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        gameplay_run_id=args.gameplay_run_id,
        output_debug_artifact=args.output_debug_artifact,
    )


def _handle_index_and_run_detection(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    media = index_media(
        session=session,
        source_path=args.source_path,
        copy_to_storage=args.copy_to_storage,
        media_name=args.media_name,
        storage_root=args.storage_root,
    )
    result = run_detection_adapter(
        session=session,
        media_id=media.id,
        adapter_name=args.adapter,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        model_path=args.model_path,
        device=args.device,
        image_size=args.image_size,
        confidence_threshold=args.confidence_threshold,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        gameplay_run_id=args.gameplay_run_id,
        output_debug_artifact=args.output_debug_artifact,
    )
    return {
        "indexed_media": {
            "media_id": media.id,
            "source_uri": media.source_uri,
            "stored_uri": media.metadata_jsonb.get("stored_uri"),
            "checksum": media.checksum,
        },
        **result,
    }


def _handle_extract_frame_artifacts(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    return extract_frame_artifacts_for_run(
        session=session,
        run_id=args.run_id,
        observation_id=args.observation_id,
        observation_types=args.observation_type,
        max_frames=args.max_frames,
        output_root=args.output_root,
        image_format=args.image_format,
        overwrite=args.overwrite,
    )


def _handle_build_tracklets(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return build_tracklets_from_detection_run(
        session=session,
        detection_run_id=args.detection_run_id,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        max_gap_frames=args.max_gap_frames,
        max_center_distance_px=args.max_center_distance_px,
        grouping_method=args.grouping_method,
        include_ball=args.include_ball,
        include_players=args.include_players,
    )


if __name__ == "__main__":
    main()
