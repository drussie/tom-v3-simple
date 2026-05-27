import argparse
import json
from collections.abc import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    YoloClassMappingError,
    YoloWeightsValidationError,
)
from tom_v3_observations.synthetic import BASELINE_SCENARIO_NAME, verify_synthetic_run
from tom_v3_schema.exports import (
    PoseReviewDatasetExportRequest,
    TrackletReviewDatasetExportRequest,
)
from tom_v3_schema.pose import PoseQueryFilters
from tom_v3_schema.tracklets import TrackletQueryFilters
from tom_v3_storage.db_models import Base

from apps.api.services.pose_review_export import export_pose_review_dataset
from apps.api.services.tracklet_review_export import export_tracklet_review_dataset
from apps.worker.config import settings
from apps.worker.pipelines.synthetic_seed import seed_synthetic_run
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
from apps.worker.services.gameplay_adapter import run_gameplay_adapter
from apps.worker.services.local_demo import run_local_fixture_demo
from apps.worker.services.media_indexer import index_media
from apps.worker.services.pose_adapter import run_pose_adapter
from apps.worker.services.real_yolo_smoke import run_real_yolo_local_smoke
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run
from apps.worker.services.yolo_model_registry import register_yolo_model


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
    detection_parser.add_argument("--model-registry-id")
    detection_parser.add_argument("--device")
    detection_parser.add_argument("--image-size", type=int)
    detection_parser.add_argument("--confidence-threshold", type=float, default=0.25)
    detection_parser.add_argument("--iou-threshold", type=float, default=0.7)
    detection_parser.add_argument("--max-det", type=int, default=50)
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
    index_detection_parser.add_argument("--model-registry-id")
    index_detection_parser.add_argument("--device")
    index_detection_parser.add_argument("--image-size", type=int)
    index_detection_parser.add_argument("--confidence-threshold", type=float, default=0.25)
    index_detection_parser.add_argument("--iou-threshold", type=float, default=0.7)
    index_detection_parser.add_argument("--max-det", type=int, default=50)
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

    pose_parser = subcommands.add_parser(
        "run-pose-adapter",
        help="Run a fixture pose adapter for an indexed media asset.",
    )
    pose_parser.add_argument("--media-id", required=True)
    pose_parser.add_argument("--adapter", default="fixture", choices=["fixture"])
    pose_parser.add_argument("--frame-sample-rate", type=int, default=30)
    pose_parser.add_argument("--max-frames", type=int, default=3)
    pose_parser.add_argument("--source-detection-run-id")
    pose_parser.add_argument(
        "--link-source-detections",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    pose_parser.add_argument("--run-name", default="fixture-pose-run")
    pose_parser.add_argument("--config-name", default="pose-adapter-config")
    pose_parser.add_argument("--config-version", default="v0")
    pose_parser.add_argument("--skip-create-db", action="store_true")
    pose_parser.set_defaults(handler=_handle_run_pose_adapter)

    export_parser = subcommands.add_parser(
        "export-tracklet-review-dataset",
        help="Export candidate tracklet evidence bundles as a review dataset artifact.",
    )
    export_parser.add_argument(
        "--tracklet-id",
        action="append",
        dest="tracklet_ids",
        default=[],
        help="Tracklet candidate id to export. May be supplied more than once.",
    )
    export_parser.add_argument(
        "--query-json",
        help="Structured tracklet query JSON. Reuses the tracklet query service.",
    )
    export_parser.add_argument("--output-root", default=".data/exports")
    export_parser.add_argument("--format", default="json", choices=["json"])
    export_parser.add_argument(
        "--include-frame-artifacts",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    export_parser.add_argument(
        "--include-annotations",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    export_parser.add_argument("--query-name")
    export_parser.add_argument("--created-by", default="tom-v3-worker")
    export_parser.add_argument("--skip-create-db", action="store_true")
    export_parser.set_defaults(handler=_handle_export_tracklet_review_dataset)

    pose_export_parser = subcommands.add_parser(
        "export-pose-review-dataset",
        help="Export pose observations as a TOM-native review dataset artifact.",
    )
    pose_export_parser.add_argument(
        "--pose-observation-id",
        action="append",
        dest="pose_observation_ids",
        default=[],
        help="Pose observation id to export. May be supplied more than once.",
    )
    pose_export_parser.add_argument("--run-id")
    pose_export_parser.add_argument("--media-id")
    pose_export_parser.add_argument(
        "--query-json",
        help="Structured pose query JSON. Reuses the pose query service.",
    )
    pose_export_parser.add_argument("--output-root", default=".data/exports")
    pose_export_parser.add_argument("--format", default="json", choices=["json"])
    pose_export_parser.add_argument(
        "--include-annotations",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    pose_export_parser.add_argument(
        "--include-artifacts",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    pose_export_parser.add_argument("--query-name")
    pose_export_parser.add_argument("--created-by", default="tom-v3-worker")
    pose_export_parser.add_argument("--skip-create-db", action="store_true")
    pose_export_parser.set_defaults(handler=_handle_export_pose_review_dataset)

    yolo_probe_parser = subcommands.add_parser(
        "yolo-runtime-probe",
        help="Inspect optional YOLO runtime dependencies and device resolution.",
    )
    yolo_probe_parser.add_argument(
        "--device",
        default="auto",
        help="Requested YOLO device: auto, cpu, mps, cuda, cuda:0, or 0.",
    )
    yolo_probe_parser.add_argument(
        "--no-mps",
        action="store_true",
        help="Disable MPS when resolving --device auto or explicit mps.",
    )
    yolo_probe_parser.add_argument(
        "--json",
        action="store_true",
        help="Reserved for compatibility. Worker output is JSON by default.",
    )
    yolo_probe_parser.set_defaults(handler=_handle_yolo_runtime_probe, skip_create_db=True)

    yolo_register_parser = subcommands.add_parser(
        "register-yolo-model",
        help="Validate local YOLO weights and register model metadata.",
    )
    yolo_register_parser.add_argument("--weights-path", required=True)
    yolo_register_parser.add_argument("--model-name")
    yolo_register_parser.add_argument("--model-version", default="v0")
    yolo_register_parser.add_argument("--required-sha256")
    yolo_register_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    yolo_register_parser.add_argument("--class-map-json")
    yolo_register_parser.add_argument("--probe-model", action="store_true")
    yolo_register_parser.add_argument("--device", default="cpu")
    yolo_register_parser.add_argument("--created-by", default="tom-v3-worker")
    yolo_register_parser.add_argument("--skip-create-db", action="store_true")
    yolo_register_parser.set_defaults(handler=_handle_register_yolo_model)

    yolo_smoke_parser = subcommands.add_parser(
        "smoke-real-yolo-local",
        help="Run or plan the optional local real-YOLO detection smoke path.",
    )
    yolo_smoke_parser.add_argument("--source-path")
    yolo_smoke_parser.add_argument("--weights-path")
    yolo_smoke_parser.add_argument("--model-name", default="local-yolo-smoke")
    yolo_smoke_parser.add_argument("--model-version", default="local-v0")
    yolo_smoke_parser.add_argument("--device", default="cpu")
    yolo_smoke_parser.add_argument("--frame-sample-rate", type=int, default=30)
    yolo_smoke_parser.add_argument("--max-frames", type=int, default=3)
    yolo_smoke_parser.add_argument("--output-root", default=".data/artifacts")
    yolo_smoke_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    yolo_smoke_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    yolo_smoke_parser.add_argument(
        "--run-tracklets",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    yolo_smoke_parser.add_argument(
        "--output-debug-artifact",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    yolo_smoke_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the smoke plan without probing runtime or touching local assets.",
    )
    yolo_smoke_parser.add_argument("--skip-create-db", action="store_true")
    yolo_smoke_parser.set_defaults(handler=_handle_smoke_real_yolo_local)

    demo_parser = subcommands.add_parser(
        "run-demo",
        help="Run the canonical local fixture demo path without YOLO or pose weights.",
    )
    demo_parser.add_argument("--source-path")
    demo_parser.add_argument("--storage-root", default=".data/media")
    demo_parser.add_argument("--artifact-root", default=".data/artifacts")
    demo_parser.add_argument("--export-root", default=".data/exports")
    demo_parser.add_argument("--frame-sample-rate", type=int, default=30)
    demo_parser.add_argument("--max-frames", type=int, default=3)
    demo_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    demo_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    demo_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the fixture demo plan without touching local data.",
    )
    demo_parser.add_argument("--skip-create-db", action="store_true")
    demo_parser.set_defaults(handler=_handle_run_demo)

    args = parser.parse_args()
    create_db = not args.skip_create_db and not getattr(args, "plan_only", False)
    with _session_factory(create_db=create_db)() as session:
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
        model_registry_id=args.model_registry_id,
        device=args.device,
        image_size=args.image_size,
        confidence_threshold=args.confidence_threshold,
        iou_threshold=args.iou_threshold,
        max_det=args.max_det,
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
        model_registry_id=args.model_registry_id,
        device=args.device,
        image_size=args.image_size,
        confidence_threshold=args.confidence_threshold,
        iou_threshold=args.iou_threshold,
        max_det=args.max_det,
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


def _handle_run_pose_adapter(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return run_pose_adapter(
        session=session,
        media_id=args.media_id,
        adapter_name=args.adapter,
        run_name=args.run_name,
        config_name=args.config_name,
        config_version=args.config_version,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        source_detection_run_id=args.source_detection_run_id,
        link_source_detections=args.link_source_detections,
    )


def _handle_export_tracklet_review_dataset(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    query = TrackletQueryFilters(**json.loads(args.query_json)) if args.query_json else None
    request = TrackletReviewDatasetExportRequest(
        tracklet_ids=args.tracklet_ids,
        query=query,
        include_frame_artifacts=args.include_frame_artifacts,
        include_annotations=args.include_annotations,
        format=args.format,
        output_root=args.output_root,
        query_name=args.query_name,
        created_by=args.created_by,
    )
    return export_tracklet_review_dataset(session, request).model_dump()


def _handle_export_pose_review_dataset(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    query = PoseQueryFilters(**json.loads(args.query_json)) if args.query_json else None
    request = PoseReviewDatasetExportRequest(
        pose_observation_ids=args.pose_observation_ids,
        query=query,
        run_id=args.run_id,
        media_id=args.media_id,
        include_annotations=args.include_annotations,
        include_artifacts=args.include_artifacts,
        format=args.format,
        output_root=args.output_root,
        query_name=args.query_name,
        created_by=args.created_by,
    )
    return export_pose_review_dataset(session, request).model_dump()


def _handle_yolo_runtime_probe(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return probe_yolo_runtime(
        requested_device=args.device,
        allow_mps=not args.no_mps,
    )


def _handle_register_yolo_model(session: Session, args: argparse.Namespace) -> dict[str, object]:
    try:
        class_map = json.loads(args.class_map_json) if args.class_map_json else None
        return register_yolo_model(
            session=session,
            weights_path=args.weights_path,
            model_name=args.model_name,
            model_version=args.model_version,
            required_sha256=args.required_sha256,
            allowed_roots=args.allowed_roots,
            class_map=class_map,
            probe_model=args.probe_model,
            device=args.device,
            created_by=args.created_by,
        )
    except YoloWeightsValidationError as exc:
        return {
            "ok": False,
            "status": exc.result.status,
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "weights_validation": exc.result.as_dict(),
        }
    except YoloClassMappingError as exc:
        return {
            "ok": False,
            "status": "invalid_class_mapping",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
        }
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_class_mapping",
            "error_type": exc.__class__.__name__,
            "message": f"class-map-json is invalid JSON: {exc}",
        }


def _handle_smoke_real_yolo_local(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_real_yolo_local_smoke(
        session=session,
        source_path=args.source_path,
        weights_path=args.weights_path,
        model_name=args.model_name,
        model_version=args.model_version,
        device=args.device,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        output_root=args.output_root,
        allowed_roots=args.allowed_roots,
        copy_to_storage=args.copy_to_storage,
        run_tracklets=args.run_tracklets,
        output_debug_artifact=args.output_debug_artifact,
        plan_only=args.plan_only,
    )


def _handle_run_demo(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return run_local_fixture_demo(
        session=session,
        source_path=args.source_path,
        storage_root=args.storage_root,
        artifact_root=args.artifact_root,
        export_root=args.export_root,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        viewer_base_url=args.viewer_base_url,
        copy_to_storage=args.copy_to_storage,
        plan_only=args.plan_only,
    )


if __name__ == "__main__":
    main()
