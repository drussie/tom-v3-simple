import argparse
import json
from collections.abc import Callable
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tom_v3_model_adapters.court_keypoints import probe_tom_v1_court_keypoint_model
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    YoloClassMappingError,
    YoloWeightsValidationError,
)
from tom_v3_observations.synthetic import BASELINE_SCENARIO_NAME, verify_synthetic_run
from tom_v3_schema.exports import (
    CourtReviewDatasetExportRequest,
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
from apps.worker.services.ball_court_trajectory import build_ball_court_trajectory
from apps.worker.services.ball_trajectory_3d import build_3d_ball_trajectory_candidates
from apps.worker.services.camera_geometry import declare_camera_geometry
from apps.worker.services.camera_geometry_calibration_provenance import (
    DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
    DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT,
    DEFAULT_CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT,
    DEFAULT_CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT,
    build_camera_geometry_calibration_profile,
    build_camera_geometry_calibration_report,
    export_camera_geometry_calibration_provenance_contract,
    validate_camera_geometry_calibration_profile,
)
from apps.worker.services.completion_audit import run_completion_audit
from apps.worker.services.court_adapter import run_fixture_court_adapter
from apps.worker.services.court_review_export import export_court_review_dataset
from apps.worker.services.coverage_driven_sampling_strategy import (
    DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_VALIDATION_OUTPUT,
    build_coverage_sampling_profile,
    build_coverage_sampling_report,
    export_coverage_sampling_strategy_contract,
    validate_coverage_sampling_profile,
)
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.event_candidate_3d_diagnostics import (
    build_event_candidate_3d_diagnostics,
)
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
from apps.worker.services.gameplay_adapter import run_gameplay_adapter
from apps.worker.services.gameplay_gated_pipeline_routing import (
    DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
    DEFAULT_GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT,
    DEFAULT_GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT,
    DEFAULT_GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT,
    build_gameplay_gated_routing_plan,
    build_gameplay_gated_routing_report,
    export_gameplay_gated_routing_contract,
    validate_gameplay_gated_routing_plan,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    DEFAULT_GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT,
    DEFAULT_GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT,
    DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
    DEFAULT_GAMEPLAY_SEGMENT_REPORT_OUTPUT,
    DEFAULT_GAMEPLAY_SEGMENT_VALIDATION_OUTPUT,
    build_gameplay_segment_candidates,
    build_gameplay_segment_report,
    export_gameplay_segment_gate_contract,
    inspect_gameplay_classifier_asset,
    validate_gameplay_segment_candidates,
)
from apps.worker.services.hit_bounce_candidates import build_hit_bounce_candidates
from apps.worker.services.homography_candidate_builder import build_homography_candidates
from apps.worker.services.intennse_label_alignment import (
    DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    DEFAULT_INTENNSE_ALIGNMENT_REPORT_OUTPUT,
    DEFAULT_INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT,
    DEFAULT_INTENNSE_ALIGNMENT_VALIDATION_OUTPUT,
    build_intennse_alignment_report,
    build_intennse_alignment_template,
    export_intennse_label_alignment_contract,
    validate_intennse_alignment_bundle,
)
from apps.worker.services.label_feedback_evaluation import (
    DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
    DEFAULT_LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT,
    DEFAULT_LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT,
    build_label_feedback_evaluation_inputs,
    build_label_feedback_evaluation_report,
    export_label_feedback_evaluation_contract,
    validate_label_feedback_evaluation_inputs,
)
from apps.worker.services.local_demo import run_local_fixture_demo
from apps.worker.services.main_player_track_assignment import assign_main_player_tracks
from apps.worker.services.main_subject_filter import select_main_player_subjects
from apps.worker.services.many_point_ingestion_gate import (
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
    DEFAULT_MANY_POINT_INGESTION_MANIFEST_TEMPLATE_OUTPUT,
    DEFAULT_MANY_POINT_INGESTION_PLAN_OUTPUT,
    DEFAULT_MANY_POINT_INGESTION_VALIDATION_OUTPUT,
    build_many_point_ingestion_manifest_template,
    build_many_point_ingestion_plan,
    export_many_point_ingestion_gate_contract,
    run_many_point_ingestion_gate,
    validate_many_point_ingestion_manifest,
)
from apps.worker.services.media_indexer import index_media
from apps.worker.services.motion_smoothing import smooth_motion_candidates
from apps.worker.services.multi_point_regression_matrix import (
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_BASELINE,
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION,
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN,
    build_multi_point_regression_matrix,
    compare_multi_point_regression_matrices,
    verify_multi_point_regression_matrix,
)
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    build_multi_point_replay_index,
)
from apps.worker.services.multi_reviewer_disagreement import (
    DEFAULT_MULTI_REVIEWER_REVIEW_SET_TEMPLATE_OUTPUT,
    DEFAULT_MULTI_REVIEWER_REVIEW_SET_VALIDATION_OUTPUT,
    DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    DEFAULT_REVIEWER_DISAGREEMENT_REPORT_OUTPUT,
    build_multi_reviewer_review_set_template,
    build_reviewer_disagreement_report,
    export_multi_reviewer_disagreement_schema,
    validate_multi_reviewer_review_set,
)
from apps.worker.services.object_court_projection import project_objects_to_court
from apps.worker.services.observation_quality_taxonomy import (
    DEFAULT_OBSERVATION_QUALITY_PROFILE_OUTPUT,
    DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
    build_observation_quality_profile,
    export_observation_quality_taxonomy,
)
from apps.worker.services.point_candidate_evaluation import evaluate_point_candidates
from apps.worker.services.point_evidence_snapshot import build_point_evidence_snapshot
from apps.worker.services.point_manifest import build_point_manifest
from apps.worker.services.pose_adapter import run_pose_adapter
from apps.worker.services.projection_diagnostic_builder import build_projection_diagnostics
from apps.worker.services.real_court_keypoint_replay import run_real_court_keypoint_replay
from apps.worker.services.real_detection_replay import run_real_detection_replay
from apps.worker.services.real_pose_replay import run_real_pose_replay
from apps.worker.services.real_yolo_smoke import run_real_yolo_local_smoke
from apps.worker.services.review_label_schema import (
    DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    DEFAULT_REVIEW_LABEL_TEMPLATE_OUTPUT,
    build_review_label_template,
    export_review_label_schema,
    validate_review_label_bundle,
)
from apps.worker.services.review_ops_metrics import (
    DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT,
    DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
    DEFAULT_REVIEW_OPS_METRICS_VALIDATION_OUTPUT,
    build_review_ops_dashboard_data,
    build_review_ops_metrics_report,
    export_review_ops_metrics_contract,
    validate_review_ops_metrics_report,
)
from apps.worker.services.reviewed_3d_debug_baseline import (
    DEFAULT_BASELINE_FILE_STEM,
    DEFAULT_BASELINE_NAME,
    freeze_reviewed_3d_debug_baseline,
    verify_reviewed_3d_debug_baseline,
)
from apps.worker.services.reviewed_3d_debug_dataset_export import (
    export_reviewed_3d_debug_dataset,
)
from apps.worker.services.reviewed_3d_debug_dataset_regression import (
    compare_reviewed_3d_debug_dataset_exports,
)
from apps.worker.services.reviewer_confidence_schema import (
    DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    DEFAULT_REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT,
    build_reviewer_confidence_template,
    export_reviewer_confidence_schema,
    validate_reviewer_confidence_bundle,
)
from apps.worker.services.second_point_evidence_parity import (
    DEFAULT_SECOND_POINT_PARITY_MANIFEST,
    build_second_point_evidence_parity,
)
from apps.worker.services.second_point_smoke import run_second_point_ingestion_smoke
from apps.worker.services.tom_v3_expansion_completion_freeze import (
    DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT,
    DEFAULT_TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT,
    DEFAULT_TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT,
    build_tom_v3_expansion_completion_freeze,
    build_tom_v3_next_phase_readiness_report,
    validate_tom_v3_expansion_completion_freeze,
)
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run
from apps.worker.services.versioned_dataset_corpus import (
    DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    DEFAULT_DATASET_CORPUS_REPORT_OUTPUT,
    DEFAULT_DATASET_CORPUS_VALIDATION_OUTPUT,
    build_versioned_dataset_corpus_manifest,
    build_versioned_dataset_corpus_report,
    export_versioned_dataset_corpus_contract,
    validate_versioned_dataset_corpus_manifest,
)
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

    second_point_smoke_parser = subcommands.add_parser(
        "ingest-second-point-smoke",
        help="Index one additional local point/video for replay smoke only.",
    )
    second_point_smoke_parser.add_argument("--media-path")
    second_point_smoke_parser.add_argument(
        "--run-name",
        default="second-point-ingestion-smoke-v0",
    )
    second_point_smoke_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    second_point_smoke_parser.add_argument("--storage-root", default=".data/media")
    second_point_smoke_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    second_point_smoke_parser.add_argument("--manifest-output")
    second_point_smoke_parser.add_argument("--skip-create-db", action="store_true")
    second_point_smoke_parser.set_defaults(handler=_handle_ingest_second_point_smoke)

    second_point_parity_parser = subcommands.add_parser(
        "build-second-point-evidence-parity",
        help="Index one additional local point/video and write a parity baseline manifest.",
    )
    second_point_parity_parser.add_argument("--media-path")
    second_point_parity_parser.add_argument(
        "--run-name",
        default="second-point-evidence-parity-v0",
    )
    second_point_parity_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    second_point_parity_parser.add_argument("--storage-root", default=".data/media")
    second_point_parity_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    second_point_parity_parser.add_argument(
        "--baseline-manifest-output",
        default=DEFAULT_SECOND_POINT_PARITY_MANIFEST,
    )
    second_point_parity_parser.add_argument("--skip-create-db", action="store_true")
    second_point_parity_parser.set_defaults(handler=_handle_build_second_point_evidence_parity)

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
    tracklet_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
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

    court_export_parser = subcommands.add_parser(
        "export-court-review-dataset",
        help="Export court/homography/projection diagnostic evidence for review.",
    )
    court_export_parser.add_argument("--media-id", required=True)
    court_export_parser.add_argument("--court-run-id")
    court_export_parser.add_argument("--homography-run-id")
    court_export_parser.add_argument("--projection-diagnostic-run-id")
    court_export_parser.add_argument("--output-root", default=".data/exports")
    court_export_parser.add_argument("--format", default="json", choices=["json"])
    court_export_parser.add_argument(
        "--include-annotations",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    court_export_parser.add_argument(
        "--include-artifacts",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    court_export_parser.add_argument("--query-name")
    court_export_parser.add_argument("--created-by", default="tom-v3-worker")
    court_export_parser.add_argument("--skip-create-db", action="store_true")
    court_export_parser.set_defaults(handler=_handle_export_court_review_dataset)

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

    real_detection_parser = subcommands.add_parser(
        "run-real-detection",
        help="Run real YOLO detection on indexed media for replay overlay evidence.",
    )
    real_detection_parser.add_argument("--media-id", required=True)
    real_detection_parser.add_argument("--weights", required=True)
    real_detection_parser.add_argument("--model-name")
    real_detection_parser.add_argument("--model-version", default="v0")
    real_detection_parser.add_argument("--required-sha256")
    real_detection_parser.add_argument("--device", default="auto")
    real_detection_parser.add_argument("--imgsz", type=int)
    real_detection_parser.add_argument("--conf", type=float, default=0.25)
    real_detection_parser.add_argument("--iou", type=float, default=0.7)
    real_detection_parser.add_argument("--every-n-frames", type=int, default=1)
    real_detection_parser.add_argument("--frame-start", type=int)
    real_detection_parser.add_argument("--frame-end", type=int)
    real_detection_parser.add_argument("--max-frames", type=int, default=120)
    real_detection_parser.add_argument("--class-map-json")
    real_detection_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    real_detection_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    real_detection_parser.add_argument(
        "--output-debug-artifact",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    real_detection_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the real detection replay plan without probing runtime or touching assets.",
    )
    real_detection_parser.add_argument("--skip-create-db", action="store_true")
    real_detection_parser.set_defaults(handler=_handle_run_real_detection)

    real_pose_parser = subcommands.add_parser(
        "run-real-pose",
        help="Run real pose inference on indexed media for replay overlay evidence.",
    )
    real_pose_parser.add_argument("--media-id", required=True)
    real_pose_parser.add_argument("--weights", required=True)
    real_pose_parser.add_argument("--source-detection-run-id")
    real_pose_parser.add_argument("--source-subject-run-id")
    real_pose_parser.add_argument(
        "--source-track-run-id",
        "--source-main-player-track-run-id",
        dest="source_track_run_id",
    )
    real_pose_parser.add_argument("--model-name")
    real_pose_parser.add_argument("--model-version", default="v0")
    real_pose_parser.add_argument("--required-sha256")
    real_pose_parser.add_argument("--device", default="auto")
    real_pose_parser.add_argument("--imgsz", type=int)
    real_pose_parser.add_argument("--conf", type=float, default=0.25)
    real_pose_parser.add_argument("--iou", type=float, default=0.7)
    real_pose_parser.add_argument("--every-n-frames", type=int, default=1)
    real_pose_parser.add_argument("--frame-start", type=int)
    real_pose_parser.add_argument("--frame-end", type=int)
    real_pose_parser.add_argument("--max-frames", type=int, default=120)
    real_pose_parser.add_argument(
        "--mode",
        default="crop_from_player_detection",
        choices=["crop_from_player_detection", "full_frame"],
    )
    real_pose_parser.add_argument(
        "--fallback-to-full-frame",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    real_pose_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    real_pose_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    real_pose_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the real pose replay plan without probing runtime or touching assets.",
    )
    real_pose_parser.add_argument("--skip-create-db", action="store_true")
    real_pose_parser.set_defaults(handler=_handle_run_real_pose)

    main_subject_parser = subcommands.add_parser(
        "select-main-player-subjects",
        help="Select near/far main tennis-player subject candidates from player detections.",
    )
    main_subject_parser.add_argument("--media-id", required=True)
    main_subject_parser.add_argument("--source-detection-run-id", required=True)
    main_subject_parser.add_argument("--run-name", default="main-player-subject-filter-v0")
    main_subject_parser.add_argument("--every-n-frames", type=int, default=1)
    main_subject_parser.add_argument("--frame-start", type=int)
    main_subject_parser.add_argument("--frame-end", type=int)
    main_subject_parser.add_argument("--max-frames", type=int, default=214)
    main_subject_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    main_subject_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the main subject filter plan without touching observations.",
    )
    main_subject_parser.add_argument("--skip-create-db", action="store_true")
    main_subject_parser.set_defaults(handler=_handle_select_main_player_subjects)

    main_track_parser = subcommands.add_parser(
        "assign-main-player-tracks",
        help="Assign near/far main tennis-player track candidates from subject candidates.",
    )
    main_track_parser.add_argument("--media-id", required=True)
    main_track_parser.add_argument("--source-detection-run-id", required=True)
    main_track_parser.add_argument("--source-subject-run-id", required=True)
    main_track_parser.add_argument("--run-name", default="main-player-track-assignment-v01")
    main_track_parser.add_argument("--every-n-frames", type=int, default=1)
    main_track_parser.add_argument("--frame-start", type=int)
    main_track_parser.add_argument("--frame-end", type=int)
    main_track_parser.add_argument("--max-frames", type=int, default=214)
    main_track_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    main_track_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the main player track assignment plan without touching observations.",
    )
    main_track_parser.add_argument("--skip-create-db", action="store_true")
    main_track_parser.set_defaults(handler=_handle_assign_main_player_tracks)

    motion_smoothing_parser = subcommands.add_parser(
        "smooth-motion-candidates",
        help="Build derived smoothed ball/player/pose replay candidate observations.",
    )
    motion_smoothing_parser.add_argument("--media-id", required=True)
    motion_smoothing_parser.add_argument("--detection-run-id")
    motion_smoothing_parser.add_argument("--tracklet-run-id")
    motion_smoothing_parser.add_argument("--main-player-track-run-id")
    motion_smoothing_parser.add_argument("--pose-run-id")
    motion_smoothing_parser.add_argument(
        "--run-name",
        default="motion-smoothing-stable-replay-candidates-v0",
    )
    motion_smoothing_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    motion_smoothing_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the motion smoothing plan without touching observations.",
    )
    motion_smoothing_parser.add_argument("--skip-create-db", action="store_true")
    motion_smoothing_parser.set_defaults(handler=_handle_smooth_motion_candidates)

    object_court_projection_parser = subcommands.add_parser(
        "project-objects-to-court",
        help="Project smoothed ball/player candidates into candidate court-template coordinates.",
    )
    object_court_projection_parser.add_argument("--media-id", required=True)
    object_court_projection_parser.add_argument("--motion-smoothing-run-id", required=True)
    object_court_projection_parser.add_argument("--homography-run-id", required=True)
    object_court_projection_parser.add_argument(
        "--run-name",
        default="object-to-court-projection-candidates-v0",
    )
    object_court_projection_parser.add_argument(
        "--homography-max-gap-ms",
        type=int,
        default=1500,
    )
    object_court_projection_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    object_court_projection_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the object-to-court projection plan without touching observations.",
    )
    object_court_projection_parser.add_argument("--skip-create-db", action="store_true")
    object_court_projection_parser.set_defaults(handler=_handle_project_objects_to_court)

    ball_court_trajectory_parser = subcommands.add_parser(
        "build-ball-court-trajectory",
        help="Build derived court-space ball trajectory candidate observations.",
    )
    ball_court_trajectory_parser.add_argument("--media-id", required=True)
    ball_court_trajectory_parser.add_argument("--court-projection-run-id", required=True)
    ball_court_trajectory_parser.add_argument(
        "--run-name",
        default="ball-trajectory-court-candidate-v0",
    )
    ball_court_trajectory_parser.add_argument("--max-gap-frames", type=int, default=6)
    ball_court_trajectory_parser.add_argument("--max-gap-ms", type=int, default=250)
    ball_court_trajectory_parser.add_argument("--min-points-per-segment", type=int, default=3)
    ball_court_trajectory_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    ball_court_trajectory_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the ball court trajectory plan without touching observations.",
    )
    ball_court_trajectory_parser.add_argument("--skip-create-db", action="store_true")
    ball_court_trajectory_parser.set_defaults(handler=_handle_build_ball_court_trajectory)

    ball_trajectory_3d_parser = subcommands.add_parser(
        "build-3d-ball-trajectory-candidates",
        help="Build provisional 3D ball trajectory candidate evidence from declared geometry.",
    )
    ball_trajectory_3d_parser.add_argument("--media-id", required=True)
    ball_trajectory_3d_parser.add_argument("--ball-trajectory-run-id", required=True)
    ball_trajectory_3d_parser.add_argument("--court-projection-run-id")
    ball_trajectory_3d_parser.add_argument("--camera-geometry-id")
    ball_trajectory_3d_parser.add_argument(
        "--height-model",
        default="none_unknown",
    )
    ball_trajectory_3d_parser.add_argument(
        "--run-name",
        default="3d-ball-trajectory-candidate-evidence-v0",
    )
    ball_trajectory_3d_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    ball_trajectory_3d_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="3D candidate payload format. JSON is always returned; markdown adds a report body.",
    )
    ball_trajectory_3d_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown 3D candidate artifact.",
    )
    ball_trajectory_3d_parser.add_argument("--skip-create-db", action="store_true")
    ball_trajectory_3d_parser.set_defaults(handler=_handle_build_3d_ball_trajectory_candidates)

    hit_bounce_parser = subcommands.add_parser(
        "build-hit-bounce-candidates",
        help="Build first-pass hit/bounce candidate evidence observations.",
    )
    hit_bounce_parser.add_argument("--media-id", required=True)
    hit_bounce_parser.add_argument("--ball-trajectory-run-id", required=True)
    hit_bounce_parser.add_argument("--court-projection-run-id", required=True)
    hit_bounce_parser.add_argument(
        "--run-name",
        default="hit-bounce-candidate-evidence-v0",
    )
    hit_bounce_parser.add_argument(
        "--hit-player-distance-max-template",
        type=float,
        default=0.18,
    )
    hit_bounce_parser.add_argument(
        "--bounce-player-distance-min-template",
        type=float,
        default=0.18,
    )
    hit_bounce_parser.add_argument(
        "--hit-min-direction-delta-degrees",
        type=float,
        default=25.0,
    )
    hit_bounce_parser.add_argument(
        "--bounce-min-direction-delta-degrees",
        type=float,
        default=20.0,
    )
    hit_bounce_parser.add_argument(
        "--hit-min-net-axis-delta-template",
        type=float,
        default=0.015,
    )
    hit_bounce_parser.add_argument(
        "--bounce-min-image-y-delta-pixels",
        type=float,
        default=2.0,
    )
    hit_bounce_parser.add_argument(
        "--bounce-min-speed-reduction-fraction",
        type=float,
        default=0.05,
    )
    hit_bounce_parser.add_argument(
        "--hit-player-time-window-ms",
        type=int,
        default=300,
    )
    hit_bounce_parser.add_argument(
        "--hit-contact-fallback-min-speed-delta-fraction",
        type=float,
        default=0.45,
    )
    hit_bounce_parser.add_argument(
        "--hit-contact-fallback-min-direction-delta-degrees",
        type=float,
        default=5.0,
    )
    hit_bounce_parser.add_argument(
        "--bounce-fallback-enabled",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    hit_bounce_parser.add_argument(
        "--bounce-fallback-min-speed-reduction-fraction",
        type=float,
        default=0.35,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-enabled",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-lookback-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-lookahead-ms",
        type=int,
        default=1300,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-distance-max-template",
        type=float,
        default=0.24,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-min-net-axis-delta-template",
        type=float,
        default=0.015,
    )
    hit_bounce_parser.add_argument(
        "--player-anchored-hit-min-pre-post-gap-ms",
        type=int,
        default=60,
    )
    hit_bounce_parser.add_argument(
        "--event-overlap-distance-template",
        type=float,
        default=0.08,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-hit-enabled",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-lookback-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-lookahead-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-min-delta-template",
        type=float,
        default=0.015,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-min-pre-post-gap-ms",
        type=int,
        default=60,
    )
    hit_bounce_parser.add_argument(
        "--net-axis-reversal-dedupe-distance-template",
        type=float,
        default=0.08,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-hit-enabled",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-lookback-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-lookahead-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-min-delta-pixels",
        type=float,
        default=4.0,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-min-pre-post-gap-ms",
        type=int,
        default=60,
    )
    hit_bounce_parser.add_argument(
        "--image-space-net-axis-dedupe-distance-pixels",
        type=float,
        default=18.0,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-hit-enabled",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-lookback-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-lookahead-ms",
        type=int,
        default=700,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-min-vector-pixels",
        type=float,
        default=8.0,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-min-delta-degrees",
        type=float,
        default=45.0,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-min-pre-post-gap-ms",
        type=int,
        default=60,
    )
    hit_bounce_parser.add_argument(
        "--image-space-direction-change-dedupe-distance-pixels",
        type=float,
        default=18.0,
    )
    hit_bounce_parser.add_argument("--candidate-dedupe-ms", type=int, default=500)
    hit_bounce_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    hit_bounce_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the hit/bounce candidate plan without touching observations.",
    )
    hit_bounce_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the full legacy hit/bounce diagnostic response.",
    )
    hit_bounce_parser.add_argument(
        "--include-observation-ids",
        action="store_true",
        help="Include persisted observation ids in compact hit/bounce output.",
    )
    hit_bounce_parser.add_argument(
        "--diagnostic-summary",
        choices=["none", "compact", "full"],
        default="compact",
        help="Control diagnostic detail in hit/bounce CLI output.",
    )
    hit_bounce_parser.add_argument("--skip-create-db", action="store_true")
    hit_bounce_parser.set_defaults(handler=_handle_build_hit_bounce_candidates)

    point_snapshot_parser = subcommands.add_parser(
        "build-point-evidence-snapshot",
        help="Build a compact point evidence snapshot for a final event candidate run.",
    )
    point_snapshot_parser.add_argument("--media-id", required=True)
    point_snapshot_parser.add_argument("--event-candidate-run-id", required=True)
    point_snapshot_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    point_snapshot_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Snapshot payload format. JSON is always returned; markdown adds a report body.",
    )
    point_snapshot_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown snapshot artifact.",
    )
    point_snapshot_parser.add_argument("--skip-create-db", action="store_true")
    point_snapshot_parser.set_defaults(handler=_handle_build_point_evidence_snapshot)

    point_manifest_parser = subcommands.add_parser(
        "build-point-manifest",
        help="Build a point-level evidence provenance manifest without changing evidence.",
    )
    point_manifest_parser.add_argument("--media-id", required=True)
    point_manifest_parser.add_argument("--event-candidate-run-id")
    point_manifest_parser.add_argument("--trajectory-3d-run-id")
    point_manifest_parser.add_argument("--camera-geometry-id")
    point_manifest_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    point_manifest_parser.add_argument(
        "--output",
        help="Optional JSON manifest path. Defaults to .data/manifests/<manifest-id>.json.",
    )
    point_manifest_parser.add_argument("--skip-create-db", action="store_true")
    point_manifest_parser.set_defaults(handler=_handle_build_point_manifest)

    multi_point_index_parser = subcommands.add_parser(
        "build-multi-point-replay-index",
        help="Build a read-only replay navigation index from existing point manifests.",
    )
    multi_point_index_parser.add_argument(
        "--manifest-root",
        default=".data/manifests",
        help="Directory containing point manifest JSON files.",
    )
    multi_point_index_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    multi_point_index_parser.add_argument(
        "--output",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="JSON index output path.",
    )
    multi_point_index_parser.add_argument("--skip-create-db", action="store_true")
    multi_point_index_parser.set_defaults(handler=_handle_build_multi_point_replay_index)

    multi_point_matrix_parser = subcommands.add_parser(
        "build-multi-point-regression-matrix",
        help="Build a read-only regression matrix from an existing multi-point replay index.",
    )
    multi_point_matrix_parser.add_argument(
        "--index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Blueprint 24 multi-point replay index JSON path.",
    )
    multi_point_matrix_parser.add_argument(
        "--output",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
        help="JSON matrix output path.",
    )
    multi_point_matrix_parser.add_argument("--skip-create-db", action="store_true")
    multi_point_matrix_parser.set_defaults(
        handler=_handle_build_multi_point_regression_matrix,
        skip_create_db=True,
    )

    multi_point_matrix_compare_parser = subcommands.add_parser(
        "compare-multi-point-regression-matrix",
        help="Compare multi-point regression matrix JSON files and report drift.",
    )
    multi_point_matrix_compare_parser.add_argument("--baseline", required=True)
    multi_point_matrix_compare_parser.add_argument("--current", required=True)
    multi_point_matrix_compare_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Multi-point regression report format.",
    )
    multi_point_matrix_compare_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown regression report.",
    )
    multi_point_matrix_compare_parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Treat additive or non-protected drift as breaking.",
    )
    multi_point_matrix_compare_parser.add_argument("--skip-create-db", action="store_true")
    multi_point_matrix_compare_parser.set_defaults(
        handler=_handle_compare_multi_point_regression_matrix,
        skip_create_db=True,
    )

    multi_point_matrix_verify_parser = subcommands.add_parser(
        "verify-multi-point-regression-matrix",
        help="Build current matrix and compare it against a frozen baseline matrix.",
    )
    multi_point_matrix_verify_parser.add_argument(
        "--index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Blueprint 24 multi-point replay index JSON path.",
    )
    multi_point_matrix_verify_parser.add_argument(
        "--baseline",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_BASELINE,
    )
    multi_point_matrix_verify_parser.add_argument(
        "--current-output",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    )
    multi_point_matrix_verify_parser.add_argument(
        "--regression-output",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION,
    )
    multi_point_matrix_verify_parser.add_argument(
        "--regression-markdown-output",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN,
    )
    multi_point_matrix_verify_parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Treat additive or non-protected drift as breaking.",
    )
    multi_point_matrix_verify_parser.add_argument("--skip-create-db", action="store_true")
    multi_point_matrix_verify_parser.set_defaults(
        handler=_handle_verify_multi_point_regression_matrix,
        skip_create_db=True,
    )

    observation_quality_taxonomy_parser = subcommands.add_parser(
        "export-observation-quality-taxonomy",
        help="Export the read-only observation-quality taxonomy contract.",
    )
    observation_quality_taxonomy_parser.add_argument(
        "--output",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="JSON taxonomy contract output path.",
    )
    observation_quality_taxonomy_parser.add_argument("--skip-create-db", action="store_true")
    observation_quality_taxonomy_parser.set_defaults(
        handler=_handle_export_observation_quality_taxonomy,
        skip_create_db=True,
    )

    observation_quality_profile_parser = subcommands.add_parser(
        "build-observation-quality-profile",
        help="Build a conservative observation-quality profile from an existing replay index.",
    )
    observation_quality_profile_parser.add_argument(
        "--index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Blueprint 24 multi-point replay index JSON path.",
    )
    observation_quality_profile_parser.add_argument(
        "--output",
        default=DEFAULT_OBSERVATION_QUALITY_PROFILE_OUTPUT,
        help="JSON observation-quality profile output path.",
    )
    observation_quality_profile_parser.add_argument("--skip-create-db", action="store_true")
    observation_quality_profile_parser.set_defaults(
        handler=_handle_build_observation_quality_profile,
        skip_create_db=True,
    )

    review_label_schema_parser = subcommands.add_parser(
        "export-review-label-schema",
        help="Export the structured human-review label schema contract.",
    )
    review_label_schema_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="JSON review-label schema output path.",
    )
    review_label_schema_parser.add_argument("--skip-create-db", action="store_true")
    review_label_schema_parser.set_defaults(
        handler=_handle_export_review_label_schema,
        skip_create_db=True,
    )

    review_label_template_parser = subcommands.add_parser(
        "build-review-label-template",
        help="Build a blank structured human-review label bundle template.",
    )
    review_label_template_parser.add_argument("--point-manifest-id")
    review_label_template_parser.add_argument("--media-id")
    review_label_template_parser.add_argument("--replay-url")
    review_label_template_parser.add_argument("--event-candidate-run-id")
    review_label_template_parser.add_argument("--trajectory-3d-run-id")
    review_label_template_parser.add_argument("--camera-geometry-id")
    review_label_template_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_LABEL_TEMPLATE_OUTPUT,
        help="JSON review-label template output path.",
    )
    review_label_template_parser.add_argument("--skip-create-db", action="store_true")
    review_label_template_parser.set_defaults(
        handler=_handle_build_review_label_template,
        skip_create_db=True,
    )

    review_label_validate_parser = subcommands.add_parser(
        "validate-review-label-bundle",
        help="Validate a structured review-label bundle against the schema.",
    )
    review_label_validate_parser.add_argument(
        "--schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Structured review-label schema JSON path.",
    )
    review_label_validate_parser.add_argument("--bundle", required=True)
    review_label_validate_parser.add_argument(
        "--output",
        help="Optional JSON validation report path.",
    )
    review_label_validate_parser.add_argument("--skip-create-db", action="store_true")
    review_label_validate_parser.set_defaults(
        handler=_handle_validate_review_label_bundle,
        skip_create_db=True,
    )

    reviewer_confidence_schema_parser = subcommands.add_parser(
        "export-reviewer-confidence-schema",
        help="Export the reviewer confidence and ambiguity schema contract.",
    )
    reviewer_confidence_schema_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="JSON reviewer confidence schema output path.",
    )
    reviewer_confidence_schema_parser.add_argument("--skip-create-db", action="store_true")
    reviewer_confidence_schema_parser.set_defaults(
        handler=_handle_export_reviewer_confidence_schema,
        skip_create_db=True,
    )

    reviewer_confidence_template_parser = subcommands.add_parser(
        "build-reviewer-confidence-template",
        help="Build a blank reviewer confidence and ambiguity bundle template.",
    )
    reviewer_confidence_template_parser.add_argument("--point-manifest-id")
    reviewer_confidence_template_parser.add_argument("--media-id")
    reviewer_confidence_template_parser.add_argument("--replay-url")
    reviewer_confidence_template_parser.add_argument("--event-candidate-run-id")
    reviewer_confidence_template_parser.add_argument("--trajectory-3d-run-id")
    reviewer_confidence_template_parser.add_argument("--camera-geometry-id")
    reviewer_confidence_template_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT,
        help="JSON reviewer confidence template output path.",
    )
    reviewer_confidence_template_parser.add_argument("--skip-create-db", action="store_true")
    reviewer_confidence_template_parser.set_defaults(
        handler=_handle_build_reviewer_confidence_template,
        skip_create_db=True,
    )

    reviewer_confidence_validate_parser = subcommands.add_parser(
        "validate-reviewer-confidence-bundle",
        help="Validate a reviewer confidence and ambiguity bundle against the schema.",
    )
    reviewer_confidence_validate_parser.add_argument(
        "--schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Reviewer confidence schema JSON path.",
    )
    reviewer_confidence_validate_parser.add_argument("--bundle", required=True)
    reviewer_confidence_validate_parser.add_argument(
        "--review-label-schema",
        help="Optional Blueprint 27 review label schema JSON path for label_key validation.",
    )
    reviewer_confidence_validate_parser.add_argument(
        "--output",
        help="Optional JSON validation report path.",
    )
    reviewer_confidence_validate_parser.add_argument("--skip-create-db", action="store_true")
    reviewer_confidence_validate_parser.set_defaults(
        handler=_handle_validate_reviewer_confidence_bundle,
        skip_create_db=True,
    )

    multi_reviewer_schema_parser = subcommands.add_parser(
        "export-multi-reviewer-disagreement-schema",
        help="Export the multi-reviewer disagreement schema contract.",
    )
    multi_reviewer_schema_parser.add_argument(
        "--output",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="JSON multi-reviewer disagreement schema output path.",
    )
    multi_reviewer_schema_parser.add_argument("--skip-create-db", action="store_true")
    multi_reviewer_schema_parser.set_defaults(
        handler=_handle_export_multi_reviewer_disagreement_schema,
        skip_create_db=True,
    )

    multi_reviewer_template_parser = subcommands.add_parser(
        "build-multi-reviewer-review-set-template",
        help="Build a blank multi-reviewer review-set template.",
    )
    multi_reviewer_template_parser.add_argument("--point-manifest-id")
    multi_reviewer_template_parser.add_argument("--media-id")
    multi_reviewer_template_parser.add_argument("--replay-url")
    multi_reviewer_template_parser.add_argument("--event-candidate-run-id")
    multi_reviewer_template_parser.add_argument("--trajectory-3d-run-id")
    multi_reviewer_template_parser.add_argument("--camera-geometry-id")
    multi_reviewer_template_parser.add_argument(
        "--reviewer-count",
        type=int,
        default=2,
        help="Number of blank reviewer entries to include.",
    )
    multi_reviewer_template_parser.add_argument(
        "--output",
        default=DEFAULT_MULTI_REVIEWER_REVIEW_SET_TEMPLATE_OUTPUT,
        help="JSON multi-reviewer review-set template output path.",
    )
    multi_reviewer_template_parser.add_argument("--skip-create-db", action="store_true")
    multi_reviewer_template_parser.set_defaults(
        handler=_handle_build_multi_reviewer_review_set_template,
        skip_create_db=True,
    )

    multi_reviewer_validate_parser = subcommands.add_parser(
        "validate-multi-reviewer-review-set",
        help="Validate a multi-reviewer review set against the schema.",
    )
    multi_reviewer_validate_parser.add_argument(
        "--schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Multi-reviewer disagreement schema JSON path.",
    )
    multi_reviewer_validate_parser.add_argument("--review-set", required=True)
    multi_reviewer_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    multi_reviewer_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    multi_reviewer_validate_parser.add_argument(
        "--output",
        default=DEFAULT_MULTI_REVIEWER_REVIEW_SET_VALIDATION_OUTPUT,
        help="Optional JSON validation report path.",
    )
    multi_reviewer_validate_parser.add_argument("--skip-create-db", action="store_true")
    multi_reviewer_validate_parser.set_defaults(
        handler=_handle_validate_multi_reviewer_review_set,
        skip_create_db=True,
    )

    reviewer_disagreement_report_parser = subcommands.add_parser(
        "build-reviewer-disagreement-report",
        help="Build a structural reviewer disagreement report from a review set.",
    )
    reviewer_disagreement_report_parser.add_argument(
        "--schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Multi-reviewer disagreement schema JSON path.",
    )
    reviewer_disagreement_report_parser.add_argument("--review-set", required=True)
    reviewer_disagreement_report_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    reviewer_disagreement_report_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    reviewer_disagreement_report_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEWER_DISAGREEMENT_REPORT_OUTPUT,
        help="JSON reviewer disagreement report output path.",
    )
    reviewer_disagreement_report_parser.add_argument("--skip-create-db", action="store_true")
    reviewer_disagreement_report_parser.set_defaults(
        handler=_handle_build_reviewer_disagreement_report,
        skip_create_db=True,
    )

    intennse_alignment_contract_parser = subcommands.add_parser(
        "export-intennse-label-alignment-contract",
        help="Export the INTENNSE label alignment contract.",
    )
    intennse_alignment_contract_parser.add_argument(
        "--output",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="JSON INTENNSE label alignment contract output path.",
    )
    intennse_alignment_contract_parser.add_argument("--skip-create-db", action="store_true")
    intennse_alignment_contract_parser.set_defaults(
        handler=_handle_export_intennse_label_alignment_contract,
        skip_create_db=True,
    )

    intennse_alignment_template_parser = subcommands.add_parser(
        "build-intennse-alignment-template",
        help="Build a blank INTENNSE alignment bundle template.",
    )
    intennse_alignment_template_parser.add_argument("--point-manifest-id")
    intennse_alignment_template_parser.add_argument("--media-id")
    intennse_alignment_template_parser.add_argument("--replay-url")
    intennse_alignment_template_parser.add_argument("--event-candidate-run-id")
    intennse_alignment_template_parser.add_argument("--trajectory-3d-run-id")
    intennse_alignment_template_parser.add_argument("--camera-geometry-id")
    intennse_alignment_template_parser.add_argument("--tom-review-label-bundle-ref")
    intennse_alignment_template_parser.add_argument("--tom-reviewer-confidence-bundle-ref")
    intennse_alignment_template_parser.add_argument("--tom-multi-reviewer-review-set-ref")
    intennse_alignment_template_parser.add_argument("--tom-disagreement-report-ref")
    intennse_alignment_template_parser.add_argument("--intennse-label-bundle-ref")
    intennse_alignment_template_parser.add_argument("--intennse-schema-version")
    intennse_alignment_template_parser.add_argument(
        "--output",
        default=DEFAULT_INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT,
        help="JSON INTENNSE alignment bundle template output path.",
    )
    intennse_alignment_template_parser.add_argument("--skip-create-db", action="store_true")
    intennse_alignment_template_parser.set_defaults(
        handler=_handle_build_intennse_alignment_template,
        skip_create_db=True,
    )

    intennse_alignment_validate_parser = subcommands.add_parser(
        "validate-intennse-alignment-bundle",
        help="Validate an INTENNSE alignment bundle against the contract.",
    )
    intennse_alignment_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="INTENNSE label alignment contract JSON path.",
    )
    intennse_alignment_validate_parser.add_argument("--bundle", required=True)
    intennse_alignment_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    intennse_alignment_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    intennse_alignment_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    intennse_alignment_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    intennse_alignment_validate_parser.add_argument(
        "--output",
        default=DEFAULT_INTENNSE_ALIGNMENT_VALIDATION_OUTPUT,
        help="Optional JSON INTENNSE alignment validation report path.",
    )
    intennse_alignment_validate_parser.add_argument("--skip-create-db", action="store_true")
    intennse_alignment_validate_parser.set_defaults(
        handler=_handle_validate_intennse_alignment_bundle,
        skip_create_db=True,
    )

    intennse_alignment_report_parser = subcommands.add_parser(
        "build-intennse-alignment-report",
        help="Build a structural INTENNSE alignment report from a bundle.",
    )
    intennse_alignment_report_parser.add_argument(
        "--contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="INTENNSE label alignment contract JSON path.",
    )
    intennse_alignment_report_parser.add_argument("--bundle", required=True)
    intennse_alignment_report_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    intennse_alignment_report_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    intennse_alignment_report_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    intennse_alignment_report_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    intennse_alignment_report_parser.add_argument(
        "--output",
        default=DEFAULT_INTENNSE_ALIGNMENT_REPORT_OUTPUT,
        help="JSON INTENNSE alignment report output path.",
    )
    intennse_alignment_report_parser.add_argument("--skip-create-db", action="store_true")
    intennse_alignment_report_parser.set_defaults(
        handler=_handle_build_intennse_alignment_report,
        skip_create_db=True,
    )

    dataset_corpus_contract_parser = subcommands.add_parser(
        "export-versioned-dataset-corpus-contract",
        help="Export the versioned dataset corpus contract.",
    )
    dataset_corpus_contract_parser.add_argument(
        "--output",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="JSON versioned dataset corpus contract output path.",
    )
    dataset_corpus_contract_parser.add_argument("--skip-create-db", action="store_true")
    dataset_corpus_contract_parser.set_defaults(
        handler=_handle_export_versioned_dataset_corpus_contract,
        skip_create_db=True,
    )

    dataset_corpus_manifest_parser = subcommands.add_parser(
        "build-versioned-dataset-corpus-manifest",
        help="Build a versioned dataset corpus manifest from existing TOM artifacts.",
    )
    dataset_corpus_manifest_parser.add_argument(
        "--index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Multi-point replay index JSON path.",
    )
    dataset_corpus_manifest_parser.add_argument(
        "--matrix",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
        help="Multi-point regression matrix JSON path.",
    )
    dataset_corpus_manifest_parser.add_argument("--corpus-id")
    dataset_corpus_manifest_parser.add_argument(
        "--corpus-version",
        default="v1",
        help="Version label for the generated corpus manifest.",
    )
    dataset_corpus_manifest_parser.add_argument(
        "--output",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
        help="JSON versioned dataset corpus manifest output path.",
    )
    dataset_corpus_manifest_parser.add_argument("--skip-create-db", action="store_true")
    dataset_corpus_manifest_parser.set_defaults(
        handler=_handle_build_versioned_dataset_corpus_manifest,
        skip_create_db=True,
    )

    dataset_corpus_validate_parser = subcommands.add_parser(
        "validate-versioned-dataset-corpus-manifest",
        help="Validate a versioned dataset corpus manifest structurally.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Versioned dataset corpus contract JSON path.",
    )
    dataset_corpus_validate_parser.add_argument("--manifest", required=True)
    dataset_corpus_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    dataset_corpus_validate_parser.add_argument(
        "--output",
        default=DEFAULT_DATASET_CORPUS_VALIDATION_OUTPUT,
        help="Optional JSON corpus validation report path.",
    )
    dataset_corpus_validate_parser.add_argument("--skip-create-db", action="store_true")
    dataset_corpus_validate_parser.set_defaults(
        handler=_handle_validate_versioned_dataset_corpus_manifest,
        skip_create_db=True,
    )

    dataset_corpus_report_parser = subcommands.add_parser(
        "build-versioned-dataset-corpus-report",
        help="Build a structural versioned dataset corpus report.",
    )
    dataset_corpus_report_parser.add_argument(
        "--contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Versioned dataset corpus contract JSON path.",
    )
    dataset_corpus_report_parser.add_argument("--manifest", required=True)
    dataset_corpus_report_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    dataset_corpus_report_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    dataset_corpus_report_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    dataset_corpus_report_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    dataset_corpus_report_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    dataset_corpus_report_parser.add_argument(
        "--output",
        default=DEFAULT_DATASET_CORPUS_REPORT_OUTPUT,
        help="JSON corpus report output path.",
    )
    dataset_corpus_report_parser.add_argument("--skip-create-db", action="store_true")
    dataset_corpus_report_parser.set_defaults(
        handler=_handle_build_versioned_dataset_corpus_report,
        skip_create_db=True,
    )

    coverage_sampling_contract_parser = subcommands.add_parser(
        "export-coverage-sampling-strategy-contract",
        help="Export the coverage-driven sampling strategy contract.",
    )
    coverage_sampling_contract_parser.add_argument(
        "--output",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="JSON coverage sampling strategy contract output path.",
    )
    coverage_sampling_contract_parser.add_argument("--skip-create-db", action="store_true")
    coverage_sampling_contract_parser.set_defaults(
        handler=_handle_export_coverage_sampling_strategy_contract,
        skip_create_db=True,
    )

    coverage_sampling_profile_parser = subcommands.add_parser(
        "build-coverage-sampling-profile",
        help="Build a coverage sampling profile from existing TOM corpus artifacts.",
    )
    coverage_sampling_profile_parser.add_argument(
        "--corpus-manifest",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
        help="Versioned dataset corpus manifest JSON path.",
    )
    coverage_sampling_profile_parser.add_argument(
        "--index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Optional multi-point replay index JSON path.",
    )
    coverage_sampling_profile_parser.add_argument(
        "--matrix",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
        help="Optional multi-point regression matrix JSON path.",
    )
    coverage_sampling_profile_parser.add_argument(
        "--output",
        default=DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
        help="JSON coverage sampling profile output path.",
    )
    coverage_sampling_profile_parser.add_argument("--skip-create-db", action="store_true")
    coverage_sampling_profile_parser.set_defaults(
        handler=_handle_build_coverage_sampling_profile,
        skip_create_db=True,
    )

    coverage_sampling_validate_parser = subcommands.add_parser(
        "validate-coverage-sampling-profile",
        help="Validate a coverage sampling profile structurally.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="Coverage sampling strategy contract JSON path.",
    )
    coverage_sampling_validate_parser.add_argument("--profile", required=True)
    coverage_sampling_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--dataset-corpus-contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Blueprint 31 versioned dataset corpus contract JSON path.",
    )
    coverage_sampling_validate_parser.add_argument(
        "--output",
        default=DEFAULT_COVERAGE_SAMPLING_VALIDATION_OUTPUT,
        help="Optional JSON coverage sampling validation report path.",
    )
    coverage_sampling_validate_parser.add_argument("--skip-create-db", action="store_true")
    coverage_sampling_validate_parser.set_defaults(
        handler=_handle_validate_coverage_sampling_profile,
        skip_create_db=True,
    )

    coverage_sampling_report_parser = subcommands.add_parser(
        "build-coverage-sampling-report",
        help="Build a structural coverage sampling report.",
    )
    coverage_sampling_report_parser.add_argument(
        "--contract",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="Coverage sampling strategy contract JSON path.",
    )
    coverage_sampling_report_parser.add_argument("--profile", required=True)
    coverage_sampling_report_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--dataset-corpus-contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Blueprint 31 versioned dataset corpus contract JSON path.",
    )
    coverage_sampling_report_parser.add_argument(
        "--output",
        default=DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
        help="JSON coverage sampling report output path.",
    )
    coverage_sampling_report_parser.add_argument("--skip-create-db", action="store_true")
    coverage_sampling_report_parser.set_defaults(
        handler=_handle_build_coverage_sampling_report,
        skip_create_db=True,
    )

    many_point_contract_parser = subcommands.add_parser(
        "export-many-point-ingestion-gate-contract",
        help="Export the many-point evidence ingestion gate contract.",
    )
    many_point_contract_parser.add_argument(
        "--output",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="JSON many-point ingestion gate contract output path.",
    )
    many_point_contract_parser.add_argument("--skip-create-db", action="store_true")
    many_point_contract_parser.set_defaults(
        handler=_handle_export_many_point_ingestion_gate_contract,
        skip_create_db=True,
    )

    many_point_template_parser = subcommands.add_parser(
        "build-many-point-ingestion-manifest-template",
        help="Build a many-point ingestion manifest template from explicit local paths.",
    )
    many_point_template_parser.add_argument(
        "--local-media-path",
        action="append",
        default=[],
        help="Explicit local point/video path. May be supplied more than once.",
    )
    many_point_template_parser.add_argument(
        "--source-label",
        default="local_point_video",
        help="Source label prefix for generated entries.",
    )
    many_point_template_parser.add_argument(
        "--requested-action",
        action="append",
        default=[],
        help="Requested action to include. Defaults to all BP33 safe actions.",
    )
    many_point_template_parser.add_argument(
        "--output",
        default=DEFAULT_MANY_POINT_INGESTION_MANIFEST_TEMPLATE_OUTPUT,
        help="JSON many-point ingestion manifest template output path.",
    )
    many_point_template_parser.add_argument("--skip-create-db", action="store_true")
    many_point_template_parser.set_defaults(
        handler=_handle_build_many_point_ingestion_manifest_template,
        skip_create_db=True,
    )

    many_point_validate_parser = subcommands.add_parser(
        "validate-many-point-ingestion-manifest",
        help="Validate a many-point ingestion manifest structurally.",
    )
    many_point_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Many-point ingestion gate contract JSON path.",
    )
    many_point_validate_parser.add_argument("--manifest", required=True)
    many_point_validate_parser.add_argument(
        "--output",
        default=DEFAULT_MANY_POINT_INGESTION_VALIDATION_OUTPUT,
        help="Optional JSON many-point ingestion validation output path.",
    )
    many_point_validate_parser.add_argument("--skip-create-db", action="store_true")
    many_point_validate_parser.set_defaults(
        handler=_handle_validate_many_point_ingestion_manifest,
        skip_create_db=True,
    )

    many_point_plan_parser = subcommands.add_parser(
        "build-many-point-ingestion-plan",
        help="Build a many-point ingestion plan without indexing media.",
    )
    many_point_plan_parser.add_argument(
        "--contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Many-point ingestion gate contract JSON path.",
    )
    many_point_plan_parser.add_argument("--manifest", required=True)
    many_point_plan_parser.add_argument(
        "--mode",
        choices=["dry_run", "validate_only", "index_only", "index_and_manifest"],
        default="dry_run",
    )
    many_point_plan_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    many_point_plan_parser.add_argument(
        "--output",
        default=DEFAULT_MANY_POINT_INGESTION_PLAN_OUTPUT,
        help="JSON many-point ingestion plan output path.",
    )
    many_point_plan_parser.add_argument("--skip-create-db", action="store_true")
    many_point_plan_parser.set_defaults(
        handler=_handle_build_many_point_ingestion_plan,
        skip_create_db=True,
    )

    many_point_gate_parser = subcommands.add_parser(
        "run-many-point-ingestion-gate",
        help="Run the many-point ingestion gate. Defaults to dry-run.",
    )
    many_point_gate_parser.add_argument(
        "--contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Many-point ingestion gate contract JSON path.",
    )
    many_point_gate_parser.add_argument("--manifest", required=True)
    many_point_gate_parser.add_argument(
        "--mode",
        choices=["dry_run", "validate_only", "index_only", "index_and_manifest"],
        default="dry_run",
    )
    many_point_gate_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    many_point_gate_parser.add_argument("--storage-root", default=".data/media")
    many_point_gate_parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    many_point_gate_parser.add_argument("--manifest-output-dir", default=".data/manifests")
    many_point_gate_parser.add_argument(
        "--multi-point-index-output",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
    )
    many_point_gate_parser.add_argument(
        "--dataset-corpus-manifest-output",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    )
    many_point_gate_parser.add_argument(
        "--multi-point-matrix",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    )
    many_point_gate_parser.add_argument(
        "--output",
        default=DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
        help="JSON many-point ingestion gate report output path.",
    )
    many_point_gate_parser.add_argument("--skip-create-db", action="store_true")
    many_point_gate_parser.set_defaults(handler=_handle_run_many_point_ingestion_gate)

    review_ops_contract_parser = subcommands.add_parser(
        "export-review-ops-metrics-contract",
        help="Export the review operations metrics contract.",
    )
    review_ops_contract_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
        help="JSON review operations metrics contract output path.",
    )
    review_ops_contract_parser.add_argument("--skip-create-db", action="store_true")
    review_ops_contract_parser.set_defaults(
        handler=_handle_export_review_ops_metrics_contract,
        skip_create_db=True,
    )

    review_ops_report_parser = subcommands.add_parser(
        "build-review-ops-metrics-report",
        help="Build a read-only structural review operations metrics report.",
    )
    review_ops_report_parser.add_argument(
        "--contract",
        default=DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
        help="Review operations metrics contract JSON path.",
    )
    review_ops_report_parser.add_argument(
        "--corpus-manifest",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
        help="Versioned dataset corpus manifest JSON path.",
    )
    review_ops_report_parser.add_argument(
        "--coverage-sampling-profile",
        default=DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
        help="Coverage sampling profile JSON path.",
    )
    review_ops_report_parser.add_argument(
        "--coverage-sampling-report",
        default=DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
        help="Coverage sampling report JSON path.",
    )
    review_ops_report_parser.add_argument(
        "--many-point-ingestion-gate",
        default=DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
        help="Many-point ingestion gate report JSON path.",
    )
    review_ops_report_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
        help="JSON review operations metrics report output path.",
    )
    review_ops_report_parser.add_argument("--skip-create-db", action="store_true")
    review_ops_report_parser.set_defaults(
        handler=_handle_build_review_ops_metrics_report,
        skip_create_db=True,
    )

    review_ops_validate_parser = subcommands.add_parser(
        "validate-review-ops-metrics-report",
        help="Validate a review operations metrics report structurally.",
    )
    review_ops_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
        help="Review operations metrics contract JSON path.",
    )
    review_ops_validate_parser.add_argument("--report", required=True)
    review_ops_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--dataset-corpus-contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Blueprint 31 versioned dataset corpus contract JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--coverage-sampling-contract",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="Blueprint 32 coverage sampling strategy contract JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--many-point-ingestion-contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Blueprint 33 many-point ingestion gate contract JSON path.",
    )
    review_ops_validate_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_OPS_METRICS_VALIDATION_OUTPUT,
        help="Optional JSON review operations metrics validation output path.",
    )
    review_ops_validate_parser.add_argument("--skip-create-db", action="store_true")
    review_ops_validate_parser.set_defaults(
        handler=_handle_validate_review_ops_metrics_report,
        skip_create_db=True,
    )

    review_ops_dashboard_parser = subcommands.add_parser(
        "build-review-ops-dashboard-data",
        help="Build read-only dashboard JSON from a review operations metrics report.",
    )
    review_ops_dashboard_parser.add_argument(
        "--report",
        default=DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
        help="Review operations metrics report JSON path.",
    )
    review_ops_dashboard_parser.add_argument(
        "--output",
        default=DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT,
        help="JSON review operations dashboard data output path.",
    )
    review_ops_dashboard_parser.add_argument("--skip-create-db", action="store_true")
    review_ops_dashboard_parser.set_defaults(
        handler=_handle_build_review_ops_dashboard_data,
        skip_create_db=True,
    )

    label_feedback_contract_parser = subcommands.add_parser(
        "export-label-feedback-evaluation-contract",
        help="Export the label feedback evaluation bridge contract.",
    )
    label_feedback_contract_parser.add_argument(
        "--output",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
        help="JSON label feedback evaluation contract output path.",
    )
    label_feedback_contract_parser.add_argument("--skip-create-db", action="store_true")
    label_feedback_contract_parser.set_defaults(
        handler=_handle_export_label_feedback_evaluation_contract,
        skip_create_db=True,
    )

    label_feedback_inputs_parser = subcommands.add_parser(
        "build-label-feedback-evaluation-inputs",
        help="Build structural label feedback inputs for the evaluation harness.",
    )
    label_feedback_inputs_parser.add_argument(
        "--contract",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
        help="Label feedback evaluation contract JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--corpus-manifest",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
        help="Versioned dataset corpus manifest JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--review-ops-metrics-report",
        default=DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
        help="Review operations metrics report JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--review-ops-dashboard-data",
        default=DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT,
        help="Review operations dashboard data JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--coverage-sampling-profile",
        default=DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
        help="Coverage sampling profile JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--coverage-sampling-report",
        default=DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
        help="Coverage sampling report JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--multi-point-regression-matrix",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
        help="Multi-point regression matrix JSON path.",
    )
    label_feedback_inputs_parser.add_argument(
        "--output",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
        help="JSON label feedback evaluation inputs output path.",
    )
    label_feedback_inputs_parser.add_argument("--skip-create-db", action="store_true")
    label_feedback_inputs_parser.set_defaults(
        handler=_handle_build_label_feedback_evaluation_inputs,
        skip_create_db=True,
    )

    label_feedback_validate_parser = subcommands.add_parser(
        "validate-label-feedback-evaluation-inputs",
        help="Validate label feedback evaluation inputs structurally.",
    )
    label_feedback_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
        help="Label feedback evaluation contract JSON path.",
    )
    label_feedback_validate_parser.add_argument("--feedback-inputs", required=True)
    label_feedback_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--dataset-corpus-contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Blueprint 31 versioned dataset corpus contract JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--coverage-sampling-contract",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="Blueprint 32 coverage sampling strategy contract JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--many-point-ingestion-contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Blueprint 33 many-point ingestion gate contract JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--review-ops-metrics-contract",
        default=DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
        help="Blueprint 34 review operations metrics contract JSON path.",
    )
    label_feedback_validate_parser.add_argument(
        "--output",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT,
        help="Optional JSON label feedback evaluation validation output path.",
    )
    label_feedback_validate_parser.add_argument("--skip-create-db", action="store_true")
    label_feedback_validate_parser.set_defaults(
        handler=_handle_validate_label_feedback_evaluation_inputs,
        skip_create_db=True,
    )

    label_feedback_report_parser = subcommands.add_parser(
        "build-label-feedback-evaluation-report",
        help="Build a structural label feedback evaluation report.",
    )
    label_feedback_report_parser.add_argument(
        "--contract",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
        help="Label feedback evaluation contract JSON path.",
    )
    label_feedback_report_parser.add_argument(
        "--feedback-inputs",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
        help="Label feedback evaluation inputs JSON path.",
    )
    label_feedback_report_parser.add_argument(
        "--output",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT,
        help="JSON label feedback evaluation report output path.",
    )
    label_feedback_report_parser.add_argument("--skip-create-db", action="store_true")
    label_feedback_report_parser.set_defaults(
        handler=_handle_build_label_feedback_evaluation_report,
        skip_create_db=True,
    )

    camera_calibration_contract_parser = subcommands.add_parser(
        "export-camera-geometry-calibration-provenance-contract",
        help="Export the camera geometry calibration provenance contract.",
    )
    camera_calibration_contract_parser.add_argument(
        "--output",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
        help="JSON camera geometry calibration provenance contract output path.",
    )
    camera_calibration_contract_parser.add_argument(
        "--skip-create-db",
        action="store_true",
    )
    camera_calibration_contract_parser.set_defaults(
        handler=_handle_export_camera_geometry_calibration_provenance_contract,
        skip_create_db=True,
    )

    camera_calibration_profile_parser = subcommands.add_parser(
        "build-camera-geometry-calibration-profile",
        help="Build a structural camera geometry calibration provenance profile.",
    )
    camera_calibration_profile_parser.add_argument(
        "--contract",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
        help="Camera geometry calibration provenance contract JSON path.",
    )
    camera_calibration_profile_parser.add_argument(
        "--replay-index",
        default=MULTI_POINT_REPLAY_INDEX_OUTPUT,
        help="Multi-point replay index JSON path.",
    )
    camera_calibration_profile_parser.add_argument(
        "--regression-matrix",
        default=DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
        help="Multi-point regression matrix JSON path.",
    )
    camera_calibration_profile_parser.add_argument(
        "--corpus-manifest",
        default=DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
        help="Versioned dataset corpus manifest JSON path.",
    )
    camera_calibration_profile_parser.add_argument(
        "--label-feedback-inputs",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
        help="Label feedback evaluation inputs JSON path.",
    )
    camera_calibration_profile_parser.add_argument(
        "--output",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT,
        help="JSON camera geometry calibration profile output path.",
    )
    camera_calibration_profile_parser.add_argument("--skip-create-db", action="store_true")
    camera_calibration_profile_parser.set_defaults(
        handler=_handle_build_camera_geometry_calibration_profile,
        skip_create_db=True,
    )

    camera_calibration_validate_parser = subcommands.add_parser(
        "validate-camera-geometry-calibration-profile",
        help="Validate a camera geometry calibration provenance profile structurally.",
    )
    camera_calibration_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
        help="Camera geometry calibration provenance contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument("--profile", required=True)
    camera_calibration_validate_parser.add_argument(
        "--observation-quality-taxonomy",
        default=DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
        help="Blueprint 26 observation-quality taxonomy JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--review-label-schema",
        default=DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
        help="Blueprint 27 review label schema JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--reviewer-confidence-schema",
        default=DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
        help="Blueprint 28 reviewer confidence schema JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--multi-reviewer-schema",
        default=DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
        help="Blueprint 29 multi-reviewer disagreement schema JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--intennse-alignment-contract",
        default=DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
        help="Blueprint 30 INTENNSE alignment contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--dataset-corpus-contract",
        default=DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
        help="Blueprint 31 versioned dataset corpus contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--coverage-sampling-contract",
        default=DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
        help="Blueprint 32 coverage sampling strategy contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--many-point-ingestion-contract",
        default=DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
        help="Blueprint 33 many-point ingestion gate contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--review-ops-metrics-contract",
        default=DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
        help="Blueprint 34 review operations metrics contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--label-feedback-contract",
        default=DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
        help="Blueprint 35 label feedback evaluation contract JSON path.",
    )
    camera_calibration_validate_parser.add_argument(
        "--output",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT,
        help="Optional JSON camera geometry calibration validation output path.",
    )
    camera_calibration_validate_parser.add_argument("--skip-create-db", action="store_true")
    camera_calibration_validate_parser.set_defaults(
        handler=_handle_validate_camera_geometry_calibration_profile,
        skip_create_db=True,
    )

    camera_calibration_report_parser = subcommands.add_parser(
        "build-camera-geometry-calibration-report",
        help="Build a structural camera geometry calibration provenance report.",
    )
    camera_calibration_report_parser.add_argument(
        "--contract",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT,
        help="Camera geometry calibration provenance contract JSON path.",
    )
    camera_calibration_report_parser.add_argument(
        "--profile",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT,
        help="Camera geometry calibration profile JSON path.",
    )
    camera_calibration_report_parser.add_argument(
        "--output",
        default=DEFAULT_CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT,
        help="JSON camera geometry calibration report output path.",
    )
    camera_calibration_report_parser.add_argument("--skip-create-db", action="store_true")
    camera_calibration_report_parser.set_defaults(
        handler=_handle_build_camera_geometry_calibration_report,
        skip_create_db=True,
    )

    expansion_freeze_parser = subcommands.add_parser(
        "build-tom-v3-expansion-completion-freeze",
        help="Build the Blueprint 37 TOM v3 expansion completion freeze manifest.",
    )
    expansion_freeze_parser.add_argument(
        "--output",
        default=DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT,
        help="JSON TOM v3 expansion completion freeze output path.",
    )
    expansion_freeze_parser.add_argument(
        "--current-main-commit",
        help="Override the main commit recorded in the freeze manifest.",
    )
    expansion_freeze_parser.add_argument("--skip-create-db", action="store_true")
    expansion_freeze_parser.set_defaults(
        handler=_handle_build_tom_v3_expansion_completion_freeze,
        skip_create_db=True,
    )

    expansion_freeze_validate_parser = subcommands.add_parser(
        "validate-tom-v3-expansion-completion-freeze",
        help="Validate the Blueprint 37 TOM v3 expansion completion freeze manifest.",
    )
    expansion_freeze_validate_parser.add_argument(
        "--freeze",
        required=True,
        help="TOM v3 expansion completion freeze JSON path.",
    )
    expansion_freeze_validate_parser.add_argument(
        "--output",
        default=DEFAULT_TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT,
        help="Optional JSON TOM v3 expansion completion validation output path.",
    )
    expansion_freeze_validate_parser.add_argument("--skip-create-db", action="store_true")
    expansion_freeze_validate_parser.set_defaults(
        handler=_handle_validate_tom_v3_expansion_completion_freeze,
        skip_create_db=True,
    )

    next_phase_readiness_parser = subcommands.add_parser(
        "build-tom-v3-next-phase-readiness-report",
        help="Build the Blueprint 37 TOM v3 next-phase readiness report.",
    )
    next_phase_readiness_parser.add_argument(
        "--freeze",
        default=DEFAULT_TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT,
        help="TOM v3 expansion completion freeze JSON path.",
    )
    next_phase_readiness_parser.add_argument(
        "--output",
        default=DEFAULT_TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT,
        help="JSON TOM v3 next-phase readiness report output path.",
    )
    next_phase_readiness_parser.add_argument("--skip-create-db", action="store_true")
    next_phase_readiness_parser.set_defaults(
        handler=_handle_build_tom_v3_next_phase_readiness_report,
        skip_create_db=True,
    )

    gameplay_gate_contract_parser = subcommands.add_parser(
        "export-gameplay-segment-gate-contract",
        help="Export the Blueprint 38 gameplay segment gate contract.",
    )
    gameplay_gate_contract_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="JSON gameplay segment gate contract output path.",
    )
    gameplay_gate_contract_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_gate_contract_parser.set_defaults(
        handler=_handle_export_gameplay_segment_gate_contract,
        skip_create_db=True,
    )

    gameplay_asset_parser = subcommands.add_parser(
        "inspect-gameplay-classifier-asset",
        help="Inspect and hash the local TOM v1 gameplay classifier asset.",
    )
    gameplay_asset_parser.add_argument(
        "--model-asset-path",
        default=DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
        help="Local TOM v1 gameplay classifier asset path.",
    )
    gameplay_asset_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT,
        help="Optional JSON classifier asset inspection output path.",
    )
    gameplay_asset_parser.add_argument("--classifier-name", default=None)
    gameplay_asset_parser.add_argument("--classifier-version", default=None)
    gameplay_asset_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_asset_parser.set_defaults(
        handler=_handle_inspect_gameplay_classifier_asset,
        skip_create_db=True,
    )

    gameplay_candidates_parser = subcommands.add_parser(
        "build-gameplay-segment-candidates",
        help="Build gameplay segment candidate gate artifacts from explicit media.",
    )
    gameplay_candidates_parser.add_argument("--local-media-path", required=True)
    gameplay_candidates_parser.add_argument("--media-id")
    gameplay_candidates_parser.add_argument(
        "--model-asset-path",
        default=DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
        help="Local TOM v1 gameplay classifier asset path.",
    )
    gameplay_candidates_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT,
        help="JSON gameplay segment candidates output path.",
    )
    gameplay_candidates_parser.add_argument("--threshold", type=float, default=0.55)
    gameplay_candidates_parser.add_argument("--smoothing-window", type=int, default=3)
    gameplay_candidates_parser.add_argument("--hysteresis-enter", type=float, default=0.60)
    gameplay_candidates_parser.add_argument("--hysteresis-exit", type=float, default=0.45)
    gameplay_candidates_parser.add_argument("--frame-sample-rate", type=int, default=30)
    gameplay_candidates_parser.add_argument("--max-frames", type=int, default=240)
    gameplay_candidates_parser.add_argument("--min-segment-duration-ms", type=int, default=500)
    gameplay_candidates_parser.add_argument(
        "--inference-mode",
        default="provenance_fixture",
        help="Safe local inference mode for candidate artifact generation.",
    )
    gameplay_candidates_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    gameplay_candidates_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_candidates_parser.set_defaults(
        handler=_handle_build_gameplay_segment_candidates,
        skip_create_db=True,
    )

    gameplay_validate_parser = subcommands.add_parser(
        "validate-gameplay-segment-candidates",
        help="Validate gameplay segment candidate artifacts structurally.",
    )
    gameplay_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="Gameplay segment gate contract JSON path.",
    )
    gameplay_validate_parser.add_argument("--candidates", required=True)
    gameplay_validate_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_SEGMENT_VALIDATION_OUTPUT,
        help="Optional JSON gameplay segment validation output path.",
    )
    gameplay_validate_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_validate_parser.set_defaults(
        handler=_handle_validate_gameplay_segment_candidates,
        skip_create_db=True,
    )

    gameplay_report_parser = subcommands.add_parser(
        "build-gameplay-segment-report",
        help="Build a structural gameplay segment gate report.",
    )
    gameplay_report_parser.add_argument(
        "--contract",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="Gameplay segment gate contract JSON path.",
    )
    gameplay_report_parser.add_argument("--candidates", required=True)
    gameplay_report_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_SEGMENT_REPORT_OUTPUT,
        help="JSON gameplay segment report output path.",
    )
    gameplay_report_parser.add_argument("--skip-create-db", action="store_true")
    gameplay_report_parser.set_defaults(
        handler=_handle_build_gameplay_segment_report,
        skip_create_db=True,
    )

    gated_routing_contract_parser = subcommands.add_parser(
        "export-gameplay-gated-routing-contract",
        help="Export the Blueprint 39 gameplay-gated routing contract.",
    )
    gated_routing_contract_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
        help="JSON gameplay-gated routing contract output path.",
    )
    gated_routing_contract_parser.add_argument("--skip-create-db", action="store_true")
    gated_routing_contract_parser.set_defaults(
        handler=_handle_export_gameplay_gated_routing_contract,
        skip_create_db=True,
    )

    gated_routing_plan_parser = subcommands.add_parser(
        "build-gameplay-gated-routing-plan",
        help="Build a gameplay-gated downstream routing plan.",
    )
    gated_routing_plan_parser.add_argument(
        "--gameplay-segments",
        required=True,
        help="Blueprint 38 gameplay segment candidates JSON path.",
    )
    gated_routing_plan_parser.add_argument(
        "--gameplay-segment-contract",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="Blueprint 38 gameplay segment gate contract JSON path.",
    )
    gated_routing_plan_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT,
        help="JSON gameplay-gated routing plan output path.",
    )
    gated_routing_plan_parser.add_argument(
        "--routing-mode",
        default="dry_run",
        help="Routing mode for structural plan generation.",
    )
    gated_routing_plan_parser.add_argument(
        "--downstream-stages",
        default=None,
        help="Optional comma-separated downstream stage list.",
    )
    gated_routing_plan_parser.add_argument("--skip-create-db", action="store_true")
    gated_routing_plan_parser.set_defaults(
        handler=_handle_build_gameplay_gated_routing_plan,
        skip_create_db=True,
    )

    gated_routing_validate_parser = subcommands.add_parser(
        "validate-gameplay-gated-routing-plan",
        help="Validate a gameplay-gated routing plan structurally.",
    )
    gated_routing_validate_parser.add_argument(
        "--contract",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
        help="Gameplay-gated routing contract JSON path.",
    )
    gated_routing_validate_parser.add_argument(
        "--plan",
        required=True,
        help="Gameplay-gated routing plan JSON path.",
    )
    gated_routing_validate_parser.add_argument(
        "--gameplay-segment-contract",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="Blueprint 38 gameplay segment gate contract JSON path.",
    )
    gated_routing_validate_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT,
        help="Optional JSON gameplay-gated routing validation output path.",
    )
    gated_routing_validate_parser.add_argument("--skip-create-db", action="store_true")
    gated_routing_validate_parser.set_defaults(
        handler=_handle_validate_gameplay_gated_routing_plan,
        skip_create_db=True,
    )

    gated_routing_report_parser = subcommands.add_parser(
        "build-gameplay-gated-routing-report",
        help="Build a structural gameplay-gated routing report.",
    )
    gated_routing_report_parser.add_argument(
        "--contract",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT,
        help="Gameplay-gated routing contract JSON path.",
    )
    gated_routing_report_parser.add_argument(
        "--plan",
        required=True,
        help="Gameplay-gated routing plan JSON path.",
    )
    gated_routing_report_parser.add_argument(
        "--gameplay-segment-contract",
        default=DEFAULT_GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT,
        help="Blueprint 38 gameplay segment gate contract JSON path.",
    )
    gated_routing_report_parser.add_argument(
        "--output",
        default=DEFAULT_GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT,
        help="JSON gameplay-gated routing report output path.",
    )
    gated_routing_report_parser.add_argument("--skip-create-db", action="store_true")
    gated_routing_report_parser.set_defaults(
        handler=_handle_build_gameplay_gated_routing_report,
        skip_create_db=True,
    )

    point_evaluation_parser = subcommands.add_parser(
        "evaluate-point-candidates",
        help="Evaluate generated point candidate markers using operator review metadata.",
    )
    point_evaluation_parser.add_argument("--media-id", required=True)
    point_evaluation_parser.add_argument("--event-candidate-run-id", required=True)
    point_evaluation_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    point_evaluation_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Evaluation payload format. JSON is always returned; markdown adds a report body.",
    )
    point_evaluation_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown evaluation artifact.",
    )
    point_evaluation_parser.add_argument("--skip-create-db", action="store_true")
    point_evaluation_parser.set_defaults(handler=_handle_evaluate_point_candidates)

    event_candidate_3d_parser = subcommands.add_parser(
        "build-event-candidate-3d-diagnostics",
        help="Build diagnostic-only 3D context for final hit/bounce event markers.",
    )
    event_candidate_3d_parser.add_argument("--media-id", required=True)
    event_candidate_3d_parser.add_argument("--event-candidate-run-id", required=True)
    event_candidate_3d_parser.add_argument("--trajectory-3d-run-id", required=True)
    event_candidate_3d_parser.add_argument("--camera-geometry-id")
    event_candidate_3d_parser.add_argument("--time-window-ms", type=int, default=250)
    event_candidate_3d_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    event_candidate_3d_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Diagnostic payload format. JSON is always returned; markdown adds a report body.",
    )
    event_candidate_3d_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown diagnostic artifact.",
    )
    event_candidate_3d_parser.add_argument("--skip-create-db", action="store_true")
    event_candidate_3d_parser.set_defaults(
        handler=_handle_build_event_candidate_3d_diagnostics
    )

    reviewed_3d_export_parser = subcommands.add_parser(
        "export-reviewed-3d-debug-dataset",
        help="Export reviewed 3D debug evidence as an offline JSON/Markdown dataset package.",
    )
    reviewed_3d_export_parser.add_argument("--media-id", required=True)
    reviewed_3d_export_parser.add_argument("--event-candidate-run-id", required=True)
    reviewed_3d_export_parser.add_argument("--trajectory-3d-run-id", required=True)
    reviewed_3d_export_parser.add_argument("--camera-geometry-id", required=True)
    reviewed_3d_export_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    reviewed_3d_export_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Reviewed 3D debug dataset format.",
    )
    reviewed_3d_export_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown export artifact.",
    )
    reviewed_3d_export_parser.add_argument("--skip-create-db", action="store_true")
    reviewed_3d_export_parser.set_defaults(
        handler=_handle_export_reviewed_3d_debug_dataset
    )

    reviewed_3d_regression_parser = subcommands.add_parser(
        "compare-reviewed-3d-debug-dataset",
        help="Compare reviewed 3D debug dataset exports and report deterministic drift.",
    )
    reviewed_3d_regression_parser.add_argument("--baseline", required=True)
    reviewed_3d_regression_parser.add_argument("--current", required=True)
    reviewed_3d_regression_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Reviewed 3D debug regression report format.",
    )
    reviewed_3d_regression_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown regression report.",
    )
    reviewed_3d_regression_parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Return a failed regression status when drift is detected.",
    )
    reviewed_3d_regression_parser.add_argument(
        "--allow-id-drift",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Ignore UUID-like field drift when comparing exported rows.",
    )
    reviewed_3d_regression_parser.add_argument(
        "--allow-float-drift",
        type=float,
        default=0.000001,
        help="Absolute tolerance for float comparisons.",
    )
    reviewed_3d_regression_parser.add_argument("--skip-create-db", action="store_true")
    reviewed_3d_regression_parser.set_defaults(
        handler=_handle_compare_reviewed_3d_debug_dataset,
        skip_create_db=True,
    )

    freeze_reviewed_3d_baseline_parser = subcommands.add_parser(
        "freeze-reviewed-3d-debug-baseline",
        help="Freeze a local reviewed 3D debug baseline export and manifest.",
    )
    freeze_reviewed_3d_baseline_parser.add_argument("--media-id", required=True)
    freeze_reviewed_3d_baseline_parser.add_argument("--event-candidate-run-id", required=True)
    freeze_reviewed_3d_baseline_parser.add_argument("--trajectory-3d-run-id", required=True)
    freeze_reviewed_3d_baseline_parser.add_argument("--camera-geometry-id", required=True)
    freeze_reviewed_3d_baseline_parser.add_argument(
        "--baseline-dir",
        default=".data/baselines",
    )
    freeze_reviewed_3d_baseline_parser.add_argument(
        "--baseline-name",
        default=DEFAULT_BASELINE_NAME,
    )
    freeze_reviewed_3d_baseline_parser.add_argument(
        "--file-stem",
        default=DEFAULT_BASELINE_FILE_STEM,
    )
    freeze_reviewed_3d_baseline_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    freeze_reviewed_3d_baseline_parser.add_argument("--skip-create-db", action="store_true")
    freeze_reviewed_3d_baseline_parser.set_defaults(
        handler=_handle_freeze_reviewed_3d_debug_baseline
    )

    verify_reviewed_3d_baseline_parser = subcommands.add_parser(
        "verify-reviewed-3d-debug-baseline",
        help="Export current reviewed 3D debug data and compare it with a baseline.",
    )
    verify_reviewed_3d_baseline_parser.add_argument("--media-id", required=True)
    verify_reviewed_3d_baseline_parser.add_argument("--event-candidate-run-id", required=True)
    verify_reviewed_3d_baseline_parser.add_argument("--trajectory-3d-run-id", required=True)
    verify_reviewed_3d_baseline_parser.add_argument("--camera-geometry-id", required=True)
    verify_reviewed_3d_baseline_parser.add_argument("--baseline", required=True)
    verify_reviewed_3d_baseline_parser.add_argument(
        "--current-output",
        default=".data/exports/reviewed_3d_debug_dataset_sample_point.current.json",
    )
    verify_reviewed_3d_baseline_parser.add_argument(
        "--regression-output",
        default=".data/exports/reviewed_3d_debug_dataset_sample_point.regression.json",
    )
    verify_reviewed_3d_baseline_parser.add_argument(
        "--regression-markdown-output",
        default=None,
    )
    verify_reviewed_3d_baseline_parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Return a failed regression status when drift is detected.",
    )
    verify_reviewed_3d_baseline_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    verify_reviewed_3d_baseline_parser.add_argument("--skip-create-db", action="store_true")
    verify_reviewed_3d_baseline_parser.set_defaults(
        handler=_handle_verify_reviewed_3d_debug_baseline
    )

    camera_geometry_parser = subcommands.add_parser(
        "declare-camera-geometry",
        help="Declare camera/court geometry evidence for future 3D readiness.",
    )
    camera_geometry_parser.add_argument("--media-id", required=True)
    camera_geometry_parser.add_argument("--court-run-id")
    camera_geometry_parser.add_argument("--court-projection-run-id")
    camera_geometry_parser.add_argument("--homography-run-id")
    camera_geometry_parser.add_argument(
        "--court-model",
        default="itf_standard_tennis_court",
    )
    camera_geometry_parser.add_argument(
        "--camera-model",
        default="homography_backed_court_plane",
    )
    camera_geometry_parser.add_argument("--geometry-status", default="declared")
    camera_geometry_parser.add_argument(
        "--viewer-base-url",
        default="http://127.0.0.1:3000",
    )
    camera_geometry_parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Geometry payload format. JSON is always returned; markdown adds a report body.",
    )
    camera_geometry_parser.add_argument(
        "--output",
        help="Optional file path for the JSON or markdown geometry artifact.",
    )
    camera_geometry_parser.add_argument("--skip-create-db", action="store_true")
    camera_geometry_parser.set_defaults(handler=_handle_declare_camera_geometry)

    fixture_court_parser = subcommands.add_parser(
        "run-fixture-court",
        help="Run deterministic fixture court keypoint/line/camera-view evidence.",
    )
    fixture_court_parser.add_argument("--media-id", required=True)
    fixture_court_parser.add_argument("--frame-sample-rate", type=int, default=30)
    fixture_court_parser.add_argument("--max-frames", type=int, default=30)
    fixture_court_parser.add_argument("--run-name", default="fixture-court-evidence")
    fixture_court_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    fixture_court_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the fixture court evidence plan without touching the database.",
    )
    fixture_court_parser.add_argument("--skip-create-db", action="store_true")
    fixture_court_parser.set_defaults(handler=_handle_run_fixture_court)

    court_keypoint_probe_parser = subcommands.add_parser(
        "tom-v1-court-keypoints-probe",
        help="Inspect local TOM v1 court keypoint weights without writing observations.",
    )
    court_keypoint_probe_parser.add_argument("--weights", required=True)
    court_keypoint_probe_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    court_keypoint_probe_parser.add_argument("--skip-create-db", action="store_true")
    court_keypoint_probe_parser.set_defaults(
        handler=_handle_tom_v1_court_keypoints_probe,
        skip_create_db=True,
    )

    real_court_keypoints_parser = subcommands.add_parser(
        "run-real-court-keypoints",
        help="Run local TOM v1 court keypoint model output into court evidence observations.",
    )
    real_court_keypoints_parser.add_argument("--media-id", required=True)
    real_court_keypoints_parser.add_argument("--weights", required=True)
    real_court_keypoints_parser.add_argument("--model-name", default="tom-v1-court-keypoints")
    real_court_keypoints_parser.add_argument("--model-version", default="v1-local")
    real_court_keypoints_parser.add_argument("--run-name", default="real-court-keypoints-replay")
    real_court_keypoints_parser.add_argument("--device", default="auto")
    real_court_keypoints_parser.add_argument("--img-size", type=int, default=224)
    real_court_keypoints_parser.add_argument("--every-n-frames", type=int, default=30)
    real_court_keypoints_parser.add_argument("--frame-start", type=int)
    real_court_keypoints_parser.add_argument("--frame-end", type=int)
    real_court_keypoints_parser.add_argument("--max-frames", type=int, default=214)
    real_court_keypoints_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    real_court_keypoints_parser.add_argument(
        "--preprocessing-mode",
        default="full_frame_resize_224",
        help="Court keypoint preprocessing assumption. Currently only full_frame_resize_224.",
    )
    real_court_keypoints_parser.add_argument(
        "--coordinate-interpretation",
        default="output_as_pixels_224",
        help="Court keypoint output coordinate assumption. Currently only output_as_pixels_224.",
    )
    real_court_keypoints_parser.add_argument(
        "--emit-debug-artifacts",
        action="store_true",
        help="Persist calibration debug JSON metadata artifacts for sampled frames.",
    )
    real_court_keypoints_parser.add_argument(
        "--derive-lines",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    real_court_keypoints_parser.add_argument(
        "--allowed-root",
        action="append",
        dest="allowed_roots",
        help="Allowed local root for weights. May be supplied more than once.",
    )
    real_court_keypoints_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the real court keypoint plan without touching observations.",
    )
    real_court_keypoints_parser.add_argument("--skip-create-db", action="store_true")
    real_court_keypoints_parser.set_defaults(handler=_handle_run_real_court_keypoints)

    homography_parser = subcommands.add_parser(
        "build-homography-candidates",
        help="Build candidate homography observations from persisted court evidence.",
    )
    homography_parser.add_argument("--media-id", required=True)
    homography_parser.add_argument("--court-run-id", required=True)
    homography_parser.add_argument("--run-name", default="homography-candidate-builder")
    homography_parser.add_argument("--frame-start", type=int)
    homography_parser.add_argument("--frame-end", type=int)
    homography_parser.add_argument("--min-keypoint-confidence", type=float, default=0.0)
    homography_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    homography_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the homography candidate plan without touching the database.",
    )
    homography_parser.add_argument("--skip-create-db", action="store_true")
    homography_parser.set_defaults(handler=_handle_build_homography_candidates)

    projection_parser = subcommands.add_parser(
        "build-projection-diagnostics",
        help="Build projection diagnostic observations from homography candidates.",
    )
    projection_parser.add_argument("--media-id", required=True)
    projection_parser.add_argument("--homography-run-id", required=True)
    projection_parser.add_argument("--run-name", default="projection-diagnostic-builder")
    projection_parser.add_argument("--frame-start", type=int)
    projection_parser.add_argument("--frame-end", type=int)
    projection_parser.add_argument("--viewer-base-url", default="http://127.0.0.1:3000")
    projection_parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the projection diagnostic plan without touching the database.",
    )
    projection_parser.add_argument("--skip-create-db", action="store_true")
    projection_parser.set_defaults(handler=_handle_build_projection_diagnostics)

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

    audit_parser = subcommands.add_parser(
        "completion-audit",
        help="Audit local evidence/provenance structure without judging model correctness.",
    )
    audit_parser.add_argument("--media-id")
    audit_parser.add_argument(
        "--demo-only",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Scope audit to media marked as TOM v3 demo evidence.",
    )
    audit_parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Treat warning-severity audit findings as command failures.",
    )
    audit_parser.add_argument(
        "--json",
        action="store_true",
        help="Reserved for compatibility. Worker output is JSON by default.",
    )
    audit_parser.add_argument("--skip-create-db", action="store_true")
    audit_parser.set_defaults(handler=_handle_completion_audit)

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


def _handle_ingest_second_point_smoke(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_second_point_ingestion_smoke(
        session=session,
        media_path=args.media_path,
        run_name=args.run_name,
        viewer_base_url=args.viewer_base_url,
        storage_root=args.storage_root,
        copy_to_storage=args.copy_to_storage,
        manifest_output=args.manifest_output,
    )


def _handle_build_second_point_evidence_parity(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_second_point_evidence_parity(
        session=session,
        media_path=args.media_path,
        run_name=args.run_name,
        viewer_base_url=args.viewer_base_url,
        storage_root=args.storage_root,
        copy_to_storage=args.copy_to_storage,
        baseline_manifest_output=args.baseline_manifest_output,
    )


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
        viewer_base_url=args.viewer_base_url,
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


def _handle_export_court_review_dataset(
    session: Session, args: argparse.Namespace
) -> dict[str, object]:
    request = CourtReviewDatasetExportRequest(
        media_id=args.media_id,
        court_run_id=args.court_run_id,
        homography_run_id=args.homography_run_id,
        projection_diagnostic_run_id=args.projection_diagnostic_run_id,
        include_annotations=args.include_annotations,
        include_artifacts=args.include_artifacts,
        format=args.format,
        output_root=args.output_root,
        query_name=args.query_name,
        created_by=args.created_by,
    )
    return export_court_review_dataset(session, request).model_dump()


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


def _handle_run_real_detection(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    try:
        class_map = json.loads(args.class_map_json) if args.class_map_json else None
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_class_mapping",
            "error_type": exc.__class__.__name__,
            "message": f"class-map-json is invalid JSON: {exc}",
        }

    return run_real_detection_replay(
        session=session,
        media_id=args.media_id,
        weights_path=args.weights,
        model_name=args.model_name,
        model_version=args.model_version,
        required_sha256=args.required_sha256,
        device=args.device,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        every_n_frames=args.every_n_frames,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        max_frames=args.max_frames,
        class_map=class_map,
        allowed_roots=args.allowed_roots,
        viewer_base_url=args.viewer_base_url,
        output_debug_artifact=args.output_debug_artifact,
        plan_only=args.plan_only,
    )


def _handle_run_real_pose(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_real_pose_replay(
        session=session,
        media_id=args.media_id,
        weights_path=args.weights,
        source_detection_run_id=args.source_detection_run_id,
        source_subject_run_id=getattr(args, "source_subject_run_id", None),
        source_track_run_id=getattr(args, "source_track_run_id", None),
        model_name=args.model_name,
        model_version=args.model_version,
        required_sha256=args.required_sha256,
        device=args.device,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        every_n_frames=args.every_n_frames,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        max_frames=args.max_frames,
        mode=args.mode,
        fallback_to_full_frame=args.fallback_to_full_frame,
        allowed_roots=args.allowed_roots,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_select_main_player_subjects(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return select_main_player_subjects(
        session=session,
        media_id=args.media_id,
        source_detection_run_id=args.source_detection_run_id,
        run_name=args.run_name,
        every_n_frames=args.every_n_frames,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        max_frames=args.max_frames,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_assign_main_player_tracks(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return assign_main_player_tracks(
        session=session,
        media_id=args.media_id,
        source_detection_run_id=args.source_detection_run_id,
        source_subject_run_id=args.source_subject_run_id,
        run_name=args.run_name,
        every_n_frames=args.every_n_frames,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        max_frames=args.max_frames,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_smooth_motion_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return smooth_motion_candidates(
        session=session,
        media_id=args.media_id,
        detection_run_id=args.detection_run_id,
        tracklet_run_id=args.tracklet_run_id,
        main_player_track_run_id=args.main_player_track_run_id,
        pose_run_id=args.pose_run_id,
        run_name=args.run_name,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_run_fixture_court(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_fixture_court_adapter(
        session=session,
        media_id=args.media_id,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        run_name=args.run_name,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_tom_v1_court_keypoints_probe(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return probe_tom_v1_court_keypoint_model(
        weights_path=args.weights,
        allowed_roots=args.allowed_roots,
    )


def _handle_run_real_court_keypoints(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_real_court_keypoint_replay(
        session=session,
        media_id=args.media_id,
        weights_path=args.weights,
        model_name=args.model_name,
        model_version=args.model_version,
        run_name=args.run_name,
        device=args.device,
        img_size=args.img_size,
        every_n_frames=args.every_n_frames,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        max_frames=args.max_frames,
        allowed_roots=args.allowed_roots,
        viewer_base_url=args.viewer_base_url,
        derive_lines=args.derive_lines,
        preprocessing_mode=args.preprocessing_mode,
        coordinate_interpretation=args.coordinate_interpretation,
        emit_debug_artifacts=args.emit_debug_artifacts,
        plan_only=args.plan_only,
    )


def _handle_build_homography_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_homography_candidates(
        session=session,
        media_id=args.media_id,
        court_run_id=args.court_run_id,
        run_name=args.run_name,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        min_keypoint_confidence=args.min_keypoint_confidence,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_build_projection_diagnostics(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_projection_diagnostics(
        session=session,
        media_id=args.media_id,
        homography_run_id=args.homography_run_id,
        run_name=args.run_name,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_project_objects_to_court(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return project_objects_to_court(
        session=session,
        media_id=args.media_id,
        motion_smoothing_run_id=args.motion_smoothing_run_id,
        homography_run_id=args.homography_run_id,
        run_name=args.run_name,
        homography_max_gap_ms=args.homography_max_gap_ms,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_build_ball_court_trajectory(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_ball_court_trajectory(
        session=session,
        media_id=args.media_id,
        court_projection_run_id=args.court_projection_run_id,
        run_name=args.run_name,
        max_gap_frames=args.max_gap_frames,
        max_gap_ms=args.max_gap_ms,
        min_points_per_segment=args.min_points_per_segment,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )


def _handle_build_3d_ball_trajectory_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_3d_ball_trajectory_candidates(
        session=session,
        media_id=args.media_id,
        ball_trajectory_run_id=args.ball_trajectory_run_id,
        court_projection_run_id=args.court_projection_run_id,
        camera_geometry_id=args.camera_geometry_id,
        height_model=args.height_model,
        run_name=args.run_name,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_build_hit_bounce_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    result = build_hit_bounce_candidates(
        session=session,
        media_id=args.media_id,
        ball_trajectory_run_id=args.ball_trajectory_run_id,
        court_projection_run_id=args.court_projection_run_id,
        run_name=args.run_name,
        hit_player_distance_max_template=args.hit_player_distance_max_template,
        bounce_player_distance_min_template=args.bounce_player_distance_min_template,
        hit_min_direction_delta_degrees=args.hit_min_direction_delta_degrees,
        bounce_min_direction_delta_degrees=args.bounce_min_direction_delta_degrees,
        hit_min_net_axis_delta_template=args.hit_min_net_axis_delta_template,
        bounce_min_image_y_delta_pixels=args.bounce_min_image_y_delta_pixels,
        bounce_min_speed_reduction_fraction=args.bounce_min_speed_reduction_fraction,
        hit_player_time_window_ms=args.hit_player_time_window_ms,
        hit_contact_fallback_min_speed_delta_fraction=(
            args.hit_contact_fallback_min_speed_delta_fraction
        ),
        hit_contact_fallback_min_direction_delta_degrees=(
            args.hit_contact_fallback_min_direction_delta_degrees
        ),
        bounce_fallback_enabled=args.bounce_fallback_enabled,
        bounce_fallback_min_speed_reduction_fraction=(
            args.bounce_fallback_min_speed_reduction_fraction
        ),
        player_anchored_hit_enabled=args.player_anchored_hit_enabled,
        player_anchored_hit_lookback_ms=args.player_anchored_hit_lookback_ms,
        player_anchored_hit_lookahead_ms=args.player_anchored_hit_lookahead_ms,
        player_anchored_hit_distance_max_template=(
            args.player_anchored_hit_distance_max_template
        ),
        player_anchored_hit_min_net_axis_delta_template=(
            args.player_anchored_hit_min_net_axis_delta_template
        ),
        player_anchored_hit_min_pre_post_gap_ms=(
            args.player_anchored_hit_min_pre_post_gap_ms
        ),
        event_overlap_distance_template=getattr(
            args,
            "event_overlap_distance_template",
            0.08,
        ),
        net_axis_reversal_hit_enabled=getattr(
            args,
            "net_axis_reversal_hit_enabled",
            True,
        ),
        net_axis_reversal_lookback_ms=getattr(
            args,
            "net_axis_reversal_lookback_ms",
            700,
        ),
        net_axis_reversal_lookahead_ms=getattr(
            args,
            "net_axis_reversal_lookahead_ms",
            700,
        ),
        net_axis_reversal_min_delta_template=getattr(
            args,
            "net_axis_reversal_min_delta_template",
            0.015,
        ),
        net_axis_reversal_min_pre_post_gap_ms=getattr(
            args,
            "net_axis_reversal_min_pre_post_gap_ms",
            60,
        ),
        net_axis_reversal_dedupe_distance_template=getattr(
            args,
            "net_axis_reversal_dedupe_distance_template",
            0.08,
        ),
        image_space_net_axis_hit_enabled=getattr(
            args,
            "image_space_net_axis_hit_enabled",
            True,
        ),
        image_space_net_axis_lookback_ms=getattr(
            args,
            "image_space_net_axis_lookback_ms",
            700,
        ),
        image_space_net_axis_lookahead_ms=getattr(
            args,
            "image_space_net_axis_lookahead_ms",
            700,
        ),
        image_space_net_axis_min_delta_pixels=getattr(
            args,
            "image_space_net_axis_min_delta_pixels",
            4.0,
        ),
        image_space_net_axis_min_pre_post_gap_ms=getattr(
            args,
            "image_space_net_axis_min_pre_post_gap_ms",
            60,
        ),
        image_space_net_axis_dedupe_distance_pixels=getattr(
            args,
            "image_space_net_axis_dedupe_distance_pixels",
            18.0,
        ),
        image_space_direction_change_hit_enabled=getattr(
            args,
            "image_space_direction_change_hit_enabled",
            True,
        ),
        image_space_direction_change_lookback_ms=getattr(
            args,
            "image_space_direction_change_lookback_ms",
            700,
        ),
        image_space_direction_change_lookahead_ms=getattr(
            args,
            "image_space_direction_change_lookahead_ms",
            700,
        ),
        image_space_direction_change_min_vector_pixels=getattr(
            args,
            "image_space_direction_change_min_vector_pixels",
            8.0,
        ),
        image_space_direction_change_min_delta_degrees=getattr(
            args,
            "image_space_direction_change_min_delta_degrees",
            45.0,
        ),
        image_space_direction_change_min_pre_post_gap_ms=getattr(
            args,
            "image_space_direction_change_min_pre_post_gap_ms",
            60,
        ),
        image_space_direction_change_dedupe_distance_pixels=getattr(
            args,
            "image_space_direction_change_dedupe_distance_pixels",
            18.0,
        ),
        candidate_dedupe_ms=args.candidate_dedupe_ms,
        viewer_base_url=args.viewer_base_url,
        plan_only=args.plan_only,
    )
    return _format_hit_bounce_cli_result(
        result,
        verbose=getattr(args, "verbose", False),
        include_observation_ids=getattr(args, "include_observation_ids", False),
        diagnostic_summary=getattr(args, "diagnostic_summary", "compact"),
    )


def _handle_build_point_evidence_snapshot(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_point_evidence_snapshot(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_build_point_manifest(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_point_manifest(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        trajectory_3d_run_id=args.trajectory_3d_run_id,
        camera_geometry_id=args.camera_geometry_id,
        viewer_base_url=args.viewer_base_url,
        output_path=args.output,
    )


def _handle_build_multi_point_replay_index(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_multi_point_replay_index(
        manifest_root=args.manifest_root,
        viewer_base_url=args.viewer_base_url,
        output_path=args.output,
    )


def _handle_build_multi_point_regression_matrix(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_multi_point_regression_matrix(
        source_index_path=args.index,
        output_path=args.output,
    )


def _handle_compare_multi_point_regression_matrix(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return compare_multi_point_regression_matrices(
        baseline_path=args.baseline,
        current_path=args.current,
        strict=args.strict,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_verify_multi_point_regression_matrix(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return verify_multi_point_regression_matrix(
        source_index_path=args.index,
        baseline_path=args.baseline,
        current_output=args.current_output,
        regression_output=args.regression_output,
        regression_markdown_output=args.regression_markdown_output,
        strict=args.strict,
    )


def _handle_export_observation_quality_taxonomy(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_observation_quality_taxonomy(output_path=args.output)


def _handle_build_observation_quality_profile(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_observation_quality_profile(
        source_index_path=args.index,
        output_path=args.output,
    )


def _handle_export_review_label_schema(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_review_label_schema(output_path=args.output)


def _handle_build_review_label_template(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    associated_run_ids = {
        key: value
        for key, value in {
            "event_candidate_run_id": args.event_candidate_run_id,
            "trajectory_3d_run_id": args.trajectory_3d_run_id,
            "camera_geometry_id": args.camera_geometry_id,
        }.items()
        if value
    }
    return build_review_label_template(
        point_manifest_id=args.point_manifest_id,
        media_id=args.media_id,
        replay_url=args.replay_url,
        associated_run_ids=associated_run_ids,
        output_path=args.output,
    )


def _handle_validate_review_label_bundle(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_review_label_bundle(
        schema_path=args.schema,
        bundle_path=args.bundle,
        output_path=args.output,
    )


def _handle_export_reviewer_confidence_schema(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_reviewer_confidence_schema(output_path=args.output)


def _handle_build_reviewer_confidence_template(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    associated_run_ids = {
        key: value
        for key, value in {
            "event_candidate_run_id": args.event_candidate_run_id,
            "trajectory_3d_run_id": args.trajectory_3d_run_id,
            "camera_geometry_id": args.camera_geometry_id,
        }.items()
        if value
    }
    return build_reviewer_confidence_template(
        point_manifest_id=args.point_manifest_id,
        media_id=args.media_id,
        replay_url=args.replay_url,
        associated_run_ids=associated_run_ids,
        output_path=args.output,
    )


def _handle_validate_reviewer_confidence_bundle(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_reviewer_confidence_bundle(
        schema_path=args.schema,
        bundle_path=args.bundle,
        review_label_schema_path=args.review_label_schema,
        output_path=args.output,
    )


def _handle_export_multi_reviewer_disagreement_schema(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_multi_reviewer_disagreement_schema(output_path=args.output)


def _handle_build_multi_reviewer_review_set_template(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    associated_run_ids = {
        key: value
        for key, value in {
            "event_candidate_run_id": args.event_candidate_run_id,
            "trajectory_3d_run_id": args.trajectory_3d_run_id,
            "camera_geometry_id": args.camera_geometry_id,
        }.items()
        if value
    }
    return build_multi_reviewer_review_set_template(
        point_manifest_id=args.point_manifest_id,
        media_id=args.media_id,
        replay_url=args.replay_url,
        associated_run_ids=associated_run_ids,
        reviewer_count=args.reviewer_count,
        output_path=args.output,
    )


def _handle_validate_multi_reviewer_review_set(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_multi_reviewer_review_set(
        schema_path=args.schema,
        review_set_path=args.review_set,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        output_path=args.output,
    )


def _handle_build_reviewer_disagreement_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_reviewer_disagreement_report(
        schema_path=args.schema,
        review_set_path=args.review_set,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        output_path=args.output,
    )


def _handle_export_intennse_label_alignment_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_intennse_label_alignment_contract(output_path=args.output)


def _handle_build_intennse_alignment_template(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    associated_run_ids = {
        key: value
        for key, value in {
            "event_candidate_run_id": args.event_candidate_run_id,
            "trajectory_3d_run_id": args.trajectory_3d_run_id,
            "camera_geometry_id": args.camera_geometry_id,
        }.items()
        if value
    }
    return build_intennse_alignment_template(
        point_manifest_id=args.point_manifest_id,
        media_id=args.media_id,
        replay_url=args.replay_url,
        associated_run_ids=associated_run_ids,
        tom_review_label_bundle_ref=args.tom_review_label_bundle_ref,
        tom_reviewer_confidence_bundle_ref=args.tom_reviewer_confidence_bundle_ref,
        tom_multi_reviewer_review_set_ref=args.tom_multi_reviewer_review_set_ref,
        tom_disagreement_report_ref=args.tom_disagreement_report_ref,
        intennse_label_bundle_ref=args.intennse_label_bundle_ref,
        intennse_schema_version=args.intennse_schema_version,
        output_path=args.output,
    )


def _handle_validate_intennse_alignment_bundle(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_intennse_alignment_bundle(
        contract_path=args.contract,
        bundle_path=args.bundle,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        output_path=args.output,
    )


def _handle_build_intennse_alignment_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_intennse_alignment_report(
        contract_path=args.contract,
        bundle_path=args.bundle,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        output_path=args.output,
    )


def _handle_export_versioned_dataset_corpus_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_versioned_dataset_corpus_contract(output_path=args.output)


def _handle_build_versioned_dataset_corpus_manifest(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_versioned_dataset_corpus_manifest(
        source_index_path=args.index,
        source_matrix_path=args.matrix,
        corpus_id=args.corpus_id,
        corpus_version=args.corpus_version,
        output_path=args.output,
    )


def _handle_validate_versioned_dataset_corpus_manifest(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_versioned_dataset_corpus_manifest(
        contract_path=args.contract,
        manifest_path=args.manifest,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        output_path=args.output,
    )


def _handle_build_versioned_dataset_corpus_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_versioned_dataset_corpus_report(
        contract_path=args.contract,
        manifest_path=args.manifest,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        output_path=args.output,
    )


def _handle_export_coverage_sampling_strategy_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_coverage_sampling_strategy_contract(output_path=args.output)


def _handle_build_coverage_sampling_profile(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_coverage_sampling_profile(
        source_corpus_manifest_path=args.corpus_manifest,
        source_index_path=args.index,
        source_matrix_path=args.matrix,
        output_path=args.output,
    )


def _handle_validate_coverage_sampling_profile(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_coverage_sampling_profile(
        contract_path=args.contract,
        profile_path=args.profile,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        dataset_corpus_contract_path=args.dataset_corpus_contract,
        output_path=args.output,
    )


def _handle_build_coverage_sampling_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_coverage_sampling_report(
        contract_path=args.contract,
        profile_path=args.profile,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        dataset_corpus_contract_path=args.dataset_corpus_contract,
        output_path=args.output,
    )


def _handle_export_many_point_ingestion_gate_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_many_point_ingestion_gate_contract(output_path=args.output)


def _handle_build_many_point_ingestion_manifest_template(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_many_point_ingestion_manifest_template(
        local_media_paths=args.local_media_path,
        source_label=args.source_label,
        requested_actions=args.requested_action or None,
        output_path=args.output,
    )


def _handle_validate_many_point_ingestion_manifest(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_many_point_ingestion_manifest(
        contract_path=args.contract,
        manifest_path=args.manifest,
        output_path=args.output,
    )


def _handle_build_many_point_ingestion_plan(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_many_point_ingestion_plan(
        contract_path=args.contract,
        manifest_path=args.manifest,
        mode=args.mode,
        viewer_base_url=args.viewer_base_url,
        output_path=args.output,
    )


def _handle_run_many_point_ingestion_gate(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_many_point_ingestion_gate(
        session=session,
        contract_path=args.contract,
        manifest_path=args.manifest,
        mode=args.mode,
        viewer_base_url=args.viewer_base_url,
        storage_root=args.storage_root,
        copy_to_storage=args.copy_to_storage,
        manifest_output_dir=args.manifest_output_dir,
        multi_point_index_output=args.multi_point_index_output,
        dataset_corpus_manifest_output=args.dataset_corpus_manifest_output,
        multi_point_matrix_path=args.multi_point_matrix,
        output_path=args.output,
    )


def _handle_export_review_ops_metrics_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_review_ops_metrics_contract(output_path=args.output)


def _handle_build_review_ops_metrics_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_review_ops_metrics_report(
        contract_path=args.contract,
        corpus_manifest_path=args.corpus_manifest,
        coverage_sampling_profile_path=args.coverage_sampling_profile,
        coverage_sampling_report_path=args.coverage_sampling_report,
        many_point_ingestion_gate_path=args.many_point_ingestion_gate,
        output_path=args.output,
    )


def _handle_validate_review_ops_metrics_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_review_ops_metrics_report(
        contract_path=args.contract,
        report_path=args.report,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        dataset_corpus_contract_path=args.dataset_corpus_contract,
        coverage_sampling_contract_path=args.coverage_sampling_contract,
        many_point_ingestion_contract_path=args.many_point_ingestion_contract,
        output_path=args.output,
    )


def _handle_build_review_ops_dashboard_data(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_review_ops_dashboard_data(
        report_path=args.report,
        output_path=args.output,
    )


def _handle_export_label_feedback_evaluation_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_label_feedback_evaluation_contract(output_path=args.output)


def _handle_build_label_feedback_evaluation_inputs(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_label_feedback_evaluation_inputs(
        contract_path=args.contract,
        corpus_manifest_path=args.corpus_manifest,
        review_ops_metrics_report_path=args.review_ops_metrics_report,
        review_ops_dashboard_data_path=args.review_ops_dashboard_data,
        coverage_sampling_profile_path=args.coverage_sampling_profile,
        coverage_sampling_report_path=args.coverage_sampling_report,
        multi_point_regression_matrix_path=args.multi_point_regression_matrix,
        output_path=args.output,
    )


def _handle_validate_label_feedback_evaluation_inputs(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_label_feedback_evaluation_inputs(
        contract_path=args.contract,
        feedback_inputs_path=args.feedback_inputs,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        dataset_corpus_contract_path=args.dataset_corpus_contract,
        coverage_sampling_contract_path=args.coverage_sampling_contract,
        many_point_ingestion_contract_path=args.many_point_ingestion_contract,
        review_ops_metrics_contract_path=args.review_ops_metrics_contract,
        output_path=args.output,
    )


def _handle_build_label_feedback_evaluation_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_label_feedback_evaluation_report(
        contract_path=args.contract,
        feedback_inputs_path=args.feedback_inputs,
        output_path=args.output,
    )


def _handle_export_camera_geometry_calibration_provenance_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_camera_geometry_calibration_provenance_contract(output_path=args.output)


def _handle_build_camera_geometry_calibration_profile(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_camera_geometry_calibration_profile(
        contract_path=args.contract,
        replay_index_path=args.replay_index,
        regression_matrix_path=args.regression_matrix,
        corpus_manifest_path=args.corpus_manifest,
        label_feedback_inputs_path=args.label_feedback_inputs,
        output_path=args.output,
    )


def _handle_validate_camera_geometry_calibration_profile(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_camera_geometry_calibration_profile(
        contract_path=args.contract,
        profile_path=args.profile,
        observation_quality_taxonomy_path=args.observation_quality_taxonomy,
        review_label_schema_path=args.review_label_schema,
        reviewer_confidence_schema_path=args.reviewer_confidence_schema,
        multi_reviewer_schema_path=args.multi_reviewer_schema,
        intennse_alignment_contract_path=args.intennse_alignment_contract,
        dataset_corpus_contract_path=args.dataset_corpus_contract,
        coverage_sampling_contract_path=args.coverage_sampling_contract,
        many_point_ingestion_contract_path=args.many_point_ingestion_contract,
        review_ops_metrics_contract_path=args.review_ops_metrics_contract,
        label_feedback_contract_path=args.label_feedback_contract,
        output_path=args.output,
    )


def _handle_build_camera_geometry_calibration_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_camera_geometry_calibration_report(
        contract_path=args.contract,
        profile_path=args.profile,
        output_path=args.output,
    )


def _handle_build_tom_v3_expansion_completion_freeze(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_tom_v3_expansion_completion_freeze(
        output_path=args.output,
        current_main_commit=args.current_main_commit,
    )


def _handle_validate_tom_v3_expansion_completion_freeze(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_tom_v3_expansion_completion_freeze(
        freeze_path=args.freeze,
        output_path=args.output,
    )


def _handle_build_tom_v3_next_phase_readiness_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_tom_v3_next_phase_readiness_report(
        freeze_path=args.freeze,
        output_path=args.output,
    )


def _handle_export_gameplay_segment_gate_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_gameplay_segment_gate_contract(output_path=args.output)


def _handle_inspect_gameplay_classifier_asset(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return inspect_gameplay_classifier_asset(
        model_asset_path=args.model_asset_path,
        output_path=args.output,
        classifier_name=args.classifier_name or "tom-v1-view-classifier-gameplay",
        classifier_version=args.classifier_version or "v1-local",
    )


def _handle_build_gameplay_segment_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_gameplay_segment_candidates(
        local_media_path=args.local_media_path,
        output_path=args.output,
        media_id=args.media_id,
        model_asset_path=args.model_asset_path,
        threshold=args.threshold,
        smoothing_window=args.smoothing_window,
        hysteresis_enter=args.hysteresis_enter,
        hysteresis_exit=args.hysteresis_exit,
        frame_sample_rate=args.frame_sample_rate,
        max_frames=args.max_frames,
        min_segment_duration_ms=args.min_segment_duration_ms,
        inference_mode=args.inference_mode,
        viewer_base_url=args.viewer_base_url,
    )


def _handle_validate_gameplay_segment_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_gameplay_segment_candidates(
        contract_path=args.contract,
        candidates_path=args.candidates,
        output_path=args.output,
    )


def _handle_build_gameplay_segment_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_gameplay_segment_report(
        contract_path=args.contract,
        candidates_path=args.candidates,
        output_path=args.output,
    )


def _handle_export_gameplay_gated_routing_contract(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return export_gameplay_gated_routing_contract(output_path=args.output)


def _handle_build_gameplay_gated_routing_plan(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_gameplay_gated_routing_plan(
        gameplay_segments_path=args.gameplay_segments,
        gameplay_gate_contract_path=args.gameplay_segment_contract,
        output_path=args.output,
        routing_mode=args.routing_mode,
        downstream_stages=args.downstream_stages,
    )


def _handle_validate_gameplay_gated_routing_plan(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return validate_gameplay_gated_routing_plan(
        contract_path=args.contract,
        plan_path=args.plan,
        gameplay_gate_contract_path=args.gameplay_segment_contract,
        output_path=args.output,
    )


def _handle_build_gameplay_gated_routing_report(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return build_gameplay_gated_routing_report(
        contract_path=args.contract,
        plan_path=args.plan,
        gameplay_gate_contract_path=args.gameplay_segment_contract,
        output_path=args.output,
    )


def _handle_evaluate_point_candidates(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return evaluate_point_candidates(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_build_event_candidate_3d_diagnostics(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return build_event_candidate_3d_diagnostics(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        trajectory_3d_run_id=args.trajectory_3d_run_id,
        camera_geometry_id=args.camera_geometry_id,
        time_window_ms=args.time_window_ms,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_export_reviewed_3d_debug_dataset(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return export_reviewed_3d_debug_dataset(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        trajectory_3d_run_id=args.trajectory_3d_run_id,
        camera_geometry_id=args.camera_geometry_id,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _handle_compare_reviewed_3d_debug_dataset(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    del session
    return compare_reviewed_3d_debug_dataset_exports(
        baseline_path=args.baseline,
        current_path=args.current,
        strict=args.strict,
        output_format=args.format,
        output_path=args.output,
        allow_id_drift=args.allow_id_drift,
        allow_float_drift=args.allow_float_drift,
    )


def _handle_freeze_reviewed_3d_debug_baseline(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return freeze_reviewed_3d_debug_baseline(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        trajectory_3d_run_id=args.trajectory_3d_run_id,
        camera_geometry_id=args.camera_geometry_id,
        baseline_dir=args.baseline_dir,
        baseline_name=args.baseline_name,
        file_stem=args.file_stem,
        viewer_base_url=args.viewer_base_url,
    )


def _handle_verify_reviewed_3d_debug_baseline(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return verify_reviewed_3d_debug_baseline(
        session=session,
        media_id=args.media_id,
        event_candidate_run_id=args.event_candidate_run_id,
        trajectory_3d_run_id=args.trajectory_3d_run_id,
        camera_geometry_id=args.camera_geometry_id,
        baseline_path=args.baseline,
        current_output=args.current_output,
        regression_output=args.regression_output,
        regression_markdown_output=args.regression_markdown_output,
        strict=args.strict,
        viewer_base_url=args.viewer_base_url,
    )


def _handle_declare_camera_geometry(
    session: Session,
    args: argparse.Namespace,
) -> dict[str, object]:
    return declare_camera_geometry(
        session=session,
        media_id=args.media_id,
        court_run_id=args.court_run_id,
        court_projection_run_id=args.court_projection_run_id,
        homography_run_id=args.homography_run_id,
        court_model=args.court_model,
        camera_model=args.camera_model,
        geometry_status=args.geometry_status,
        viewer_base_url=args.viewer_base_url,
        output_format=args.format,
        output_path=args.output,
    )


def _format_hit_bounce_cli_result(
    result: dict[str, Any],
    *,
    verbose: bool = False,
    include_observation_ids: bool = False,
    diagnostic_summary: str = "compact",
) -> dict[str, Any]:
    """Return operator-focused hit/bounce CLI output without changing service data."""

    if verbose or result.get("status") == "planned" or result.get("ok") is False:
        return result

    if diagnostic_summary not in {"none", "compact", "full"}:
        raise ValueError(f"unsupported diagnostic_summary: {diagnostic_summary}")

    candidate_summary = result.get("candidate_summary")
    if not isinstance(candidate_summary, dict):
        candidate_summary = {}
    observations = result.get("observations")
    if not isinstance(observations, dict):
        observations = {}

    compact: dict[str, Any] = {}
    for key in (
        "ok",
        "status",
        "message",
        "media_id",
        "run_id",
        "event_candidate_run_id",
        "processing_step_id",
        "runtime_config_id",
        "replay_url",
    ):
        if key in result:
            compact[key] = result[key]

    if "source_run_ids" in result:
        compact["source_run_ids"] = result["source_run_ids"]
    compact["observations"] = observations

    active_versions = _compact_hit_bounce_active_versions(candidate_summary)
    if diagnostic_summary != "none" and active_versions:
        compact["active_versions"] = active_versions

    marker_summary = _compact_hit_bounce_marker_summary(
        result.get("marker_summary"),
        include_observation_ids=include_observation_ids,
    )
    compact["summary_counts"] = {
        "final_hit_candidates": observations.get("hit_candidate", 0),
        "final_bounce_candidates": observations.get("bounce_candidate", 0),
        "rejection_diagnostics": observations.get(
            "event_candidate_rejection_diagnostic",
            0,
        ),
        "marker_count": len(marker_summary),
    }

    if diagnostic_summary != "none":
        compact["marker_summary"] = marker_summary

    if diagnostic_summary == "full":
        compact["candidate_summary"] = candidate_summary

    if include_observation_ids and "observation_ids" in result:
        compact["observation_ids"] = result["observation_ids"]

    if "warnings" in result:
        compact["warnings"] = result["warnings"]
    return compact


def _compact_hit_bounce_active_versions(
    candidate_summary: dict[str, Any],
) -> dict[str, Any]:
    version_keys = {
        "physics_heuristic": "physics_heuristic_version",
        "marker_level_arbitration": "marker_level_arbitration_version",
        "universal_hit_validity_guard": "universal_hit_validity_guard_version",
        "local_evidence_classification": (
            "local_evidence_event_type_classification_version"
        ),
        "image_space_direction_change_hit_recall": (
            "image_space_direction_change_hit_recall_version"
        ),
        "image_space_net_axis_hit_recall": "image_space_net_axis_hit_recall_version",
        "net_axis_reversal_hit_recall": "net_axis_reversal_hit_recall_version",
    }
    return {
        label: candidate_summary[source_key]
        for label, source_key in version_keys.items()
        if candidate_summary.get(source_key) is not None
    }


def _compact_hit_bounce_marker_summary(
    marker_summary: object,
    *,
    include_observation_ids: bool,
) -> list[dict[str, Any]]:
    if not isinstance(marker_summary, list):
        return []

    rows = [
        marker
        for marker in marker_summary
        if isinstance(marker, dict)
        and marker.get("candidate_type") in {"hit_candidate", "bounce_candidate"}
    ]
    rows.sort(
        key=lambda marker: (
            marker.get("timestamp_ms") if marker.get("timestamp_ms") is not None else -1,
            marker.get("frame") if marker.get("frame") is not None else -1,
            str(marker.get("candidate_type") or ""),
            str(marker.get("observation_id") or ""),
        )
    )

    compact_rows: list[dict[str, Any]] = []
    for index, marker in enumerate(rows, start=1):
        compact_marker: dict[str, Any] = {
            "index": index,
            "candidate_type": marker.get("candidate_type"),
            "frame": marker.get("frame"),
            "timestamp_ms": marker.get("timestamp_ms"),
        }
        for source_key, target_key in (
            ("source_method", "source_method"),
            ("arbitration_decision", "arbitration_decision"),
            ("arbitration_reason", "arbitration_reason"),
            ("reason", "arbitration_reason"),
            ("court_x", "court_x"),
            ("court_y", "court_y"),
            ("image_x", "image_x"),
            ("image_y", "image_y"),
            ("confidence", "confidence"),
        ):
            if target_key in compact_marker and target_key == "arbitration_reason":
                continue
            value = marker.get(source_key)
            if value is not None:
                compact_marker[target_key] = value
        if include_observation_ids and marker.get("observation_id") is not None:
            compact_marker["observation_id"] = marker["observation_id"]
        compact_rows.append(compact_marker)
    return compact_rows


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


def _handle_completion_audit(session: Session, args: argparse.Namespace) -> dict[str, object]:
    return run_completion_audit(
        session=session,
        media_id=args.media_id,
        demo_only=args.demo_only,
        strict=args.strict,
    )


if __name__ == "__main__":
    main()
