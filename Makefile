PYTHON ?= python
WEB_DIR := apps/web
TOM_V3_DATABASE_URL ?= sqlite+pysqlite:///./tmp_tom_v3.db
RUN_ID ?=
MEDIA_ID ?=
SOURCE_PATH ?=
STORAGE_ROOT ?= .data/media
ADAPTER ?= fixture
FRAME_SAMPLE_RATE ?= 30
MAX_FRAMES ?= 5
ARTIFACT_ROOT ?= .data/artifacts
DETECTION_RUN_ID ?=
RUN_NAME ?= tracklet-builder-run
MAX_GAP_FRAMES ?= 30
TRACKLET_ID ?=
QUERY_JSON ?=
EXPORT_ROOT ?= .data/exports
YOLO_DEVICE ?= auto
WEIGHTS_PATH ?=
YOLO_WEIGHTS_PATH ?= $(WEIGHTS_PATH)
POSE_WEIGHTS_PATH ?= $(WEIGHTS_PATH)
TOM_V1_MODEL_ROOT ?= model_assets/tom_v1
TOM_V1_BALL_CONF ?= 0.10
TOM_V1_PLAYER_CONF ?= 0.25
TOM_V1_POSE_CONF ?= 0.25
TOM_V1_COURT_KEYPOINT_IMG_SIZE ?= 224
COURT_KEYPOINT_PREPROCESSING_MODE ?= full_frame_resize_224
COURT_KEYPOINT_COORDINATE_INTERPRETATION ?= output_as_pixels_224
EMIT_DEBUG_ARTIFACTS ?= false
MODEL_NAME ?=
MODEL_VERSION ?= v0
REQUIRED_SHA256 ?=
RUN_TRACKLETS ?= false
SOURCE_DETECTION_RUN_ID ?=
SOURCE_SUBJECT_RUN_ID ?=
SOURCE_TRACK_RUN_ID ?=
MAIN_PLAYER_TRACK_RUN_ID ?=
LINK_SOURCE_DETECTIONS ?= false
DEMO_MEDIA_PATH ?=
VIEWER_BASE_URL ?= http://127.0.0.1:3000
TRACKLET_RUN_ID ?=
POSE_RUN_ID ?=
MOTION_SMOOTHING_RUN_ID ?=
COURT_PROJECTION_RUN_NAME ?= object-to-court-projection-candidates-v0
COURT_PROJECTION_RUN_ID ?=
BALL_TRAJECTORY_RUN_NAME ?= ball-trajectory-court-candidate-v0
BALL_TRAJECTORY_RUN_ID ?=
BALL_TRAJECTORY_3D_RUN_NAME ?= 3d-ball-trajectory-candidate-evidence-v0
TRAJECTORY_3D_RUN_ID ?=
CAMERA_GEOMETRY_ID ?=
HEIGHT_MODEL ?= none_unknown
TIME_WINDOW_MS ?= 250
EVENT_CANDIDATE_RUN_NAME ?= hit-bounce-candidate-evidence-v0
EVENT_CANDIDATE_RUN_ID ?=
SECOND_POINT_MEDIA_PATH ?=
SECOND_POINT_SMOKE_RUN_NAME ?= second-point-ingestion-smoke-v0
SECOND_POINT_RUN_NAME ?= second-point-evidence-parity-v0
SECOND_POINT_MANIFEST_OUTPUT ?=
SECOND_POINT_BASELINE_MANIFEST_OUTPUT ?= .data/baselines/second_point_evidence_parity.baseline_manifest.json
VERBOSE ?= false
HIT_BOUNCE_VERBOSE ?= false
INCLUDE_OBSERVATION_IDS ?= false
DIAGNOSTIC_SUMMARY ?= compact
POINT_SNAPSHOT_FORMAT ?= json
POINT_SNAPSHOT_OUTPUT ?=
POINT_MANIFEST_OUTPUT ?=
POINT_MANIFEST_ROOT ?= .data/manifests
MULTI_POINT_REPLAY_INDEX_OUTPUT ?= .data/manifests/multi_point_replay_index.json
MULTI_POINT_REGRESSION_MATRIX_OUTPUT ?= .data/exports/multi_point_regression_matrix.current.json
MULTI_POINT_REGRESSION_MATRIX_BASELINE ?= .data/baselines/multi_point_regression_matrix.baseline.json
MULTI_POINT_REGRESSION_MATRIX_CURRENT ?= .data/exports/multi_point_regression_matrix.current.json
MULTI_POINT_REGRESSION_MATRIX_REGRESSION ?= .data/exports/multi_point_regression_matrix.regression.json
MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN ?= .data/exports/multi_point_regression_matrix.regression.md
OBSERVATION_QUALITY_TAXONOMY_OUTPUT ?= .data/contracts/observation_quality_taxonomy_v1.json
OBSERVATION_QUALITY_PROFILE_SOURCE_INDEX ?= $(MULTI_POINT_REPLAY_INDEX_OUTPUT)
OBSERVATION_QUALITY_PROFILE_OUTPUT ?= .data/exports/observation_quality_profile.current.json
REVIEW_LABEL_SCHEMA_OUTPUT ?= .data/contracts/review_label_schema_v1.json
REVIEW_LABEL_TEMPLATE_OUTPUT ?= .data/exports/review_label_template.current.json
REVIEW_LABEL_BUNDLE ?=
REVIEW_LABEL_VALIDATION_OUTPUT ?= .data/exports/review_label_bundle.validation.json
REVIEWER_CONFIDENCE_SCHEMA_OUTPUT ?= .data/contracts/reviewer_confidence_ambiguity_schema_v1.json
REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT ?= .data/exports/reviewer_confidence_ambiguity_template.current.json
REVIEWER_CONFIDENCE_BUNDLE ?=
REVIEWER_CONFIDENCE_VALIDATION_OUTPUT ?= .data/exports/reviewer_confidence_ambiguity.validation.json
MULTI_REVIEWER_SCHEMA_OUTPUT ?= .data/contracts/multi_reviewer_disagreement_schema_v1.json
MULTI_REVIEWER_REVIEW_SET_OUTPUT ?= .data/exports/multi_reviewer_review_set_template.current.json
MULTI_REVIEWER_REVIEW_SET ?=
MULTI_REVIEWER_REVIEW_SET_VALIDATION_OUTPUT ?= .data/exports/multi_reviewer_review_set.validation.json
REVIEWER_DISAGREEMENT_REPORT_OUTPUT ?= .data/exports/reviewer_disagreement_report.current.json
REVIEWER_COUNT ?= 2
INTENNSE_ALIGNMENT_CONTRACT_OUTPUT ?= .data/contracts/intennse_label_alignment_contract_v1.json
INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT ?= .data/exports/intennse_alignment_template.current.json
INTENNSE_ALIGNMENT_BUNDLE ?=
INTENNSE_ALIGNMENT_VALIDATION_OUTPUT ?= .data/exports/intennse_alignment_bundle.validation.json
INTENNSE_ALIGNMENT_REPORT_OUTPUT ?= .data/exports/intennse_alignment_report.current.json
TOM_DISAGREEMENT_REPORT_REF ?=
INTENNSE_LABEL_BUNDLE_REF ?=
INTENNSE_SCHEMA_VERSION ?=
DATASET_CORPUS_CONTRACT_OUTPUT ?= .data/contracts/versioned_dataset_corpus_contract_v1.json
DATASET_CORPUS_SOURCE_INDEX ?= $(MULTI_POINT_REPLAY_INDEX_OUTPUT)
DATASET_CORPUS_SOURCE_MATRIX ?= $(MULTI_POINT_REGRESSION_MATRIX_CURRENT)
DATASET_CORPUS_MANIFEST_OUTPUT ?= .data/exports/versioned_dataset_corpus_manifest.current.json
DATASET_CORPUS_MANIFEST ?=
DATASET_CORPUS_VALIDATION_OUTPUT ?= .data/exports/versioned_dataset_corpus_manifest.validation.json
DATASET_CORPUS_REPORT_OUTPUT ?= .data/exports/versioned_dataset_corpus_report.current.json
DATASET_CORPUS_ID ?=
DATASET_CORPUS_VERSION ?= v1
COVERAGE_SAMPLING_CONTRACT_OUTPUT ?= .data/contracts/coverage_sampling_strategy_contract_v1.json
COVERAGE_SAMPLING_SOURCE_CORPUS_MANIFEST ?= $(DATASET_CORPUS_MANIFEST_OUTPUT)
COVERAGE_SAMPLING_SOURCE_INDEX ?= $(DATASET_CORPUS_SOURCE_INDEX)
COVERAGE_SAMPLING_SOURCE_MATRIX ?= $(DATASET_CORPUS_SOURCE_MATRIX)
COVERAGE_SAMPLING_PROFILE_OUTPUT ?= .data/exports/coverage_sampling_profile.current.json
COVERAGE_SAMPLING_PROFILE ?=
COVERAGE_SAMPLING_VALIDATION_OUTPUT ?= .data/exports/coverage_sampling_profile.validation.json
COVERAGE_SAMPLING_REPORT_OUTPUT ?= .data/exports/coverage_sampling_report.current.json
MANY_POINT_INGESTION_CONTRACT_OUTPUT ?= .data/contracts/many_point_ingestion_gate_contract_v1.json
MANY_POINT_INGESTION_MEDIA_PATH ?= demo_assets/sample_point.mp4
MANY_POINT_INGESTION_SOURCE_LABEL ?= demo_local_point_video
MANY_POINT_INGESTION_MANIFEST_OUTPUT ?= .data/exports/many_point_ingestion_manifest.template.json
MANY_POINT_INGESTION_MANIFEST ?=
MANY_POINT_INGESTION_VALIDATION_OUTPUT ?= .data/exports/many_point_ingestion_manifest.validation.json
MANY_POINT_INGESTION_PLAN_OUTPUT ?= .data/exports/many_point_ingestion_plan.current.json
MANY_POINT_INGESTION_GATE_OUTPUT ?= .data/exports/many_point_ingestion_gate.current.json
MANY_POINT_INGESTION_MODE ?= dry_run
MANY_POINT_INGESTION_STORAGE_ROOT ?= .data/media
MANY_POINT_INGESTION_MANIFEST_OUTPUT_DIR ?= .data/manifests
MANY_POINT_INGESTION_MULTI_POINT_INDEX_OUTPUT ?= $(MULTI_POINT_REPLAY_INDEX_OUTPUT)
MANY_POINT_INGESTION_DATASET_CORPUS_MANIFEST_OUTPUT ?= $(DATASET_CORPUS_MANIFEST_OUTPUT)
MANY_POINT_INGESTION_MULTI_POINT_MATRIX ?= $(MULTI_POINT_REGRESSION_MATRIX_CURRENT)
REVIEW_OPS_METRICS_CONTRACT_OUTPUT ?= .data/contracts/review_ops_metrics_contract_v1.json
REVIEW_OPS_SOURCE_CORPUS_MANIFEST ?= $(DATASET_CORPUS_MANIFEST_OUTPUT)
REVIEW_OPS_SOURCE_COVERAGE_PROFILE ?= $(COVERAGE_SAMPLING_PROFILE_OUTPUT)
REVIEW_OPS_SOURCE_COVERAGE_REPORT ?= $(COVERAGE_SAMPLING_REPORT_OUTPUT)
REVIEW_OPS_SOURCE_INGESTION_GATE ?= $(MANY_POINT_INGESTION_GATE_OUTPUT)
REVIEW_OPS_METRICS_REPORT_OUTPUT ?= .data/exports/review_ops_metrics_report.current.json
REVIEW_OPS_METRICS_REPORT ?=
REVIEW_OPS_METRICS_VALIDATION_OUTPUT ?= .data/exports/review_ops_metrics_report.validation.json
REVIEW_OPS_DASHBOARD_DATA_OUTPUT ?= .data/exports/review_ops_dashboard_data.current.json
LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT ?= .data/contracts/label_feedback_evaluation_contract_v1.json
LABEL_FEEDBACK_SOURCE_CORPUS_MANIFEST ?= $(DATASET_CORPUS_MANIFEST_OUTPUT)
LABEL_FEEDBACK_SOURCE_REVIEW_OPS_REPORT ?= $(REVIEW_OPS_METRICS_REPORT_OUTPUT)
LABEL_FEEDBACK_SOURCE_REVIEW_OPS_DASHBOARD ?= $(REVIEW_OPS_DASHBOARD_DATA_OUTPUT)
LABEL_FEEDBACK_SOURCE_COVERAGE_PROFILE ?= $(COVERAGE_SAMPLING_PROFILE_OUTPUT)
LABEL_FEEDBACK_SOURCE_COVERAGE_REPORT ?= $(COVERAGE_SAMPLING_REPORT_OUTPUT)
LABEL_FEEDBACK_SOURCE_REGRESSION_MATRIX ?= $(MULTI_POINT_REGRESSION_MATRIX_CURRENT)
LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT ?= .data/exports/label_feedback_evaluation_inputs.current.json
LABEL_FEEDBACK_EVALUATION_INPUTS ?=
LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT ?= .data/exports/label_feedback_evaluation_inputs.validation.json
LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT ?= .data/exports/label_feedback_evaluation_report.current.json
CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT ?= .data/contracts/camera_geometry_calibration_provenance_contract_v1.json
CAMERA_GEOMETRY_CALIBRATION_SOURCE_REPLAY_INDEX ?= $(MULTI_POINT_REPLAY_INDEX_OUTPUT)
CAMERA_GEOMETRY_CALIBRATION_SOURCE_REGRESSION_MATRIX ?= $(MULTI_POINT_REGRESSION_MATRIX_CURRENT)
CAMERA_GEOMETRY_CALIBRATION_SOURCE_CORPUS_MANIFEST ?= $(DATASET_CORPUS_MANIFEST_OUTPUT)
CAMERA_GEOMETRY_CALIBRATION_SOURCE_LABEL_FEEDBACK_INPUTS ?= $(LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT)
CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT ?= .data/exports/camera_geometry_calibration_profile.current.json
CAMERA_GEOMETRY_CALIBRATION_PROFILE ?=
CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT ?= .data/exports/camera_geometry_calibration_profile.validation.json
CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT ?= .data/exports/camera_geometry_calibration_report.current.json
TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT ?= .data/contracts/tom_v3_expansion_completion_freeze_v1.json
TOM_V3_EXPANSION_COMPLETION_FREEZE ?=
TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT ?= .data/exports/tom_v3_expansion_completion_freeze.validation.json
TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT ?= .data/exports/tom_v3_next_phase_readiness_report.current.json
GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT ?= .data/contracts/gameplay_segment_gate_contract_v1.json
GAMEPLAY_CLASSIFIER_ASSET_PATH ?= $(TOM_V1_MODEL_ROOT)/view_classifier_gameplay.pt
GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT ?= .data/exports/gameplay_classifier_asset_inspection.current.json
GAMEPLAY_SEGMENT_MEDIA_PATH ?= demo_assets/sample_point.mp4
GAMEPLAY_SEGMENT_MEDIA_ID ?=
GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT ?= .data/exports/gameplay_segment_candidates.current.json
GAMEPLAY_SEGMENT_CANDIDATES ?=
GAMEPLAY_SEGMENT_VALIDATION_OUTPUT ?= .data/exports/gameplay_segment_candidates.validation.json
GAMEPLAY_SEGMENT_REPORT_OUTPUT ?= .data/exports/gameplay_segment_report.current.json
GAMEPLAY_SEGMENT_THRESHOLD ?= 0.55
GAMEPLAY_SEGMENT_SMOOTHING_WINDOW ?= 3
GAMEPLAY_SEGMENT_HYSTERESIS_ENTER ?= 0.60
GAMEPLAY_SEGMENT_HYSTERESIS_EXIT ?= 0.45
GAMEPLAY_SEGMENT_FRAME_SAMPLE_RATE ?= 30
GAMEPLAY_SEGMENT_MAX_FRAMES ?= 240
GAMEPLAY_SEGMENT_MIN_DURATION_MS ?= 500
GAMEPLAY_SEGMENT_INFERENCE_MODE ?= provenance_fixture
GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT ?= .data/contracts/gameplay_gated_pipeline_routing_contract_v1.json
GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS ?=
GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT ?= .data/exports/gameplay_gated_routing_plan.current.json
GAMEPLAY_GATED_ROUTING_PLAN ?=
GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT ?= .data/exports/gameplay_gated_routing_plan.validation.json
GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT ?= .data/exports/gameplay_gated_routing_report.current.json
GAMEPLAY_GATED_ROUTING_MODE ?= dry_run
GAMEPLAY_GATED_ROUTING_DOWNSTREAM_STAGES ?=
GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT ?= .data/contracts/gameplay_gated_perception_execution_contract_v1.json
GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN ?=
GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_OUTPUT ?= .data/exports/gameplay_gated_perception_execution_plan.current.json
GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN ?=
GAMEPLAY_GATED_PERCEPTION_EXECUTION_VALIDATION_OUTPUT ?= .data/exports/gameplay_gated_perception_execution_plan.validation.json
GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_OUTPUT ?= .data/exports/gameplay_gated_perception_execution_report.current.json
GAMEPLAY_GATED_PERCEPTION_EXECUTION_MODE ?= dry_run
GAMEPLAY_GATED_PERCEPTION_EXECUTION_STAGES ?=
GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT ?= .data/contracts/gameplay_segment_replay_review_contract_v1.json
GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS ?=
GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN ?=
GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN ?=
GAMEPLAY_SEGMENT_REPLAY_TIMELINE_OUTPUT ?= .data/exports/gameplay_segment_replay_timeline.current.json
GAMEPLAY_SEGMENT_REPLAY_TIMELINE ?=
GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VALIDATION_OUTPUT ?= .data/exports/gameplay_segment_replay_timeline.validation.json
GAMEPLAY_SEGMENT_REVIEW_TEMPLATE_OUTPUT ?= .data/exports/gameplay_segment_review_template.current.json
GAMEPLAY_SEGMENT_REVIEW_BUNDLE ?=
GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VALIDATION_OUTPUT ?= .data/exports/gameplay_segment_review_bundle.validation.json
GAMEPLAY_SEGMENT_REVIEW_REPORT_OUTPUT ?= .data/exports/gameplay_segment_review_report.current.json
GAMEPLAY_SEGMENT_REVIEWER_ID ?=
GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT ?= .data/contracts/gameplay_gated_many_point_smoke_contract_v1.json
GAMEPLAY_GATED_MANY_POINT_SMOKE_MEDIA_PATH ?= demo_assets/sample_point.mp4
GAMEPLAY_GATED_MANY_POINT_SMOKE_SOURCE_LABEL ?= gameplay_gated_smoke_point
GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_OUTPUT ?= .data/exports/gameplay_gated_many_point_smoke_manifest.template.json
GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST ?=
GAMEPLAY_GATED_MANY_POINT_SMOKE_VALIDATION_OUTPUT ?= .data/exports/gameplay_gated_many_point_smoke_manifest.validation.json
GAMEPLAY_GATED_MANY_POINT_SMOKE_MODE ?= fixture_only
GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT_DIR ?= .data/exports/gameplay_gated_many_point_smoke
GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT ?= .data/exports/gameplay_gated_many_point_smoke.current.json
GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT ?= $(GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT)
GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_OUTPUT ?= .data/exports/gameplay_gated_many_point_smoke_report.current.json
GAMEPLAY_GATED_MANY_POINT_SMOKE_REQUESTED_STEP ?=
GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT ?= .data/contracts/gameplay_gate_regression_baseline_contract_v1.json
GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT ?= .data/baselines/gameplay_gate_regression.baseline.json
GAMEPLAY_GATE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT ?= .data/exports/gameplay_gate_regression.verification.json
GAMEPLAY_GATE_REGRESSION_REPORT_OUTPUT ?= .data/exports/gameplay_gate_regression.report.json
GAMEPLAY_GATE_REGRESSION_WORK_DIR ?= .data/exports/gameplay_gate_regression
GAMEPLAY_GATE_REGRESSION_SMOKE_MANIFEST ?=
GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH ?= demo_assets/sample_point.mp4
GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT ?= .data/contracts/gameplay_gate_review_dataset_export_contract_v1.json
GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT ?= .data/exports/gameplay_gate_review_dataset.current.json
GAMEPLAY_GATE_REVIEW_DATASET ?= $(GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT)
GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_OUTPUT ?= .data/exports/gameplay_gate_review_dataset.validation.json
GAMEPLAY_GATE_REVIEW_DATASET_REPORT_OUTPUT ?= .data/exports/gameplay_gate_review_dataset.report.json
GAMEPLAY_GATE_REVIEW_DATASET_WORK_DIR ?= .data/exports/gameplay_gate_review_dataset
GAMEPLAY_GATE_REVIEW_DATASET_GAMEPLAY_SEGMENTS ?=
GAMEPLAY_GATE_REVIEW_DATASET_ROUTING_PLAN ?=
GAMEPLAY_GATE_REVIEW_DATASET_EXECUTION_PLAN ?=
GAMEPLAY_GATE_REVIEW_DATASET_REPLAY_TIMELINE ?=
GAMEPLAY_GATE_REVIEW_DATASET_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
GAMEPLAY_GATE_REVIEW_DATASET_REGRESSION_VERIFICATION ?= $(GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT)
GAMEPLAY_GATE_REVIEW_DATASET_FIXTURE_MEDIA_PATH ?= demo_assets/sample_point.mp4
GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT ?= .data/contracts/gameplay_gate_pathway_completion_freeze_v1.json
GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE ?= $(GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT)
GAMEPLAY_GATE_PATHWAY_COMPLETION_VALIDATION_OUTPUT ?= .data/exports/gameplay_gate_pathway_completion_freeze.validation.json
GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_OUTPUT ?= .data/exports/gameplay_gate_next_phase_readiness_report.current.json
REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT ?= .data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json
REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_OUTPUT ?= .data/exports/real_broadcast_gameplay_corpus_manifest.template.json
REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_OUTPUT)
REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VALIDATION_OUTPUT ?= .data/exports/real_broadcast_gameplay_corpus_manifest.validation.json
REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT_DIR ?= .data/exports/real_broadcast_gameplay_corpus_run
REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT ?= .data/exports/real_broadcast_gameplay_corpus_run.current.json
REAL_BROADCAST_GAMEPLAY_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_OUTPUT ?= .data/exports/real_broadcast_gameplay_corpus_report.current.json
REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE ?= dry_run
REAL_BROADCAST_GAMEPLAY_CORPUS_MEDIA_PATH ?=
REAL_BROADCAST_GAMEPLAY_CORPUS_SOURCE_LABEL ?= real_broadcast_gameplay_corpus_entry
REAL_BROADCAST_GAMEPLAY_CORPUS_CONTENT_TAG ?= unknown
REAL_BROADCAST_GAMEPLAY_CORPUS_REQUESTED_STEP ?=
REAL_BROADCAST_GAMEPLAY_CORPUS_ALLOW_FIXTURE_MODE ?= false
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT ?= .data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_bundle.template.json
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_bundle.validation.json
REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_loop_report.current.json
REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_OUTPUT ?= .data/exports/real_broadcast_gameplay_human_review_readiness_report.current.json
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REVIEW_DATASET ?=
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REPLAY_TIMELINE ?=
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_ROUTING_PLAN ?=
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_EXECUTION_PLAN ?=
REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT ?= .data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_metrics_report.current.json
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_VALIDATION_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_metrics_report.validation.json
REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_qa_dashboard.current.json
REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_OUTPUT ?= .data/exports/real_broadcast_gameplay_review_next_actions.current.json
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_LOOP_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_BUNDLE ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_DATASET ?=
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT ?= .data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_inputs.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_VALIDATION_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_inputs.validation.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_proposal.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VALIDATION_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_proposal.validation.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_proposal_report.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_METRICS_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_LOOP_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_BUNDLE ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_DATASET ?= $(GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_CURRENT_THRESHOLD ?= $(GAMEPLAY_SEGMENT_THRESHOLD)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_CURRENT_SMOOTHING_WINDOW ?= $(GAMEPLAY_SEGMENT_SMOOTHING_WINDOW)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_HYSTERESIS_ENTER ?= $(GAMEPLAY_SEGMENT_HYSTERESIS_ENTER)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_HYSTERESIS_EXIT ?= $(GAMEPLAY_SEGMENT_HYSTERESIS_EXIT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT ?= .data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_evaluation_inputs.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_VALIDATION_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_evaluation_inputs.validation.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_evaluation_report.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VALIDATION_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_evaluation_report.validation.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_evaluation_summary.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_CALIBRATION_PROPOSAL ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_METRICS_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REVIEW_LOOP_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REVIEW_BUNDLE ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_CURRENT_THRESHOLD ?= $(GAMEPLAY_SEGMENT_THRESHOLD)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_CURRENT_SMOOTHING_WINDOW ?= $(GAMEPLAY_SEGMENT_SMOOTHING_WINDOW)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_HYSTERESIS_ENTER ?= $(GAMEPLAY_SEGMENT_HYSTERESIS_ENTER)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_HYSTERESIS_EXIT ?= $(GAMEPLAY_SEGMENT_HYSTERESIS_EXIT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_MODE ?= structural_offline_evaluation
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT ?= .data/contracts/review_guided_gameplay_calibration_sandbox_regression_contract_v1.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT ?= .data/baselines/review_guided_gameplay_calibration_sandbox.baseline.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_sandbox.current.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_sandbox.regression.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_OUTPUT ?= .data/exports/review_guided_gameplay_calibration_sandbox.report.json
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_INPUTS ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_REPORT ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_CONTRACT ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT ?= .data/contracts/calibration_candidate_decision_packet_contract_v1.json
CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT ?= .data/exports/calibration_candidate_decision_packet_inputs.current.json
CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS ?= $(CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_VALIDATION_OUTPUT ?= .data/exports/calibration_candidate_decision_packet_inputs.validation.json
CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT ?= .data/exports/calibration_candidate_decision_packet.current.json
CALIBRATION_CANDIDATE_DECISION_PACKET ?= $(CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_VALIDATION_OUTPUT ?= .data/exports/calibration_candidate_decision_packet.validation.json
CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_OUTPUT ?= .data/exports/calibration_candidate_decision_packet.report.json
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CALIBRATION_PROPOSAL ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_SANDBOX_EVALUATION_REPORT ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_SANDBOX_REGRESSION_VERIFICATION ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_REVIEW_METRICS_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_REVIEW_LOOP_REPORT ?= $(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CORPUS_RUN ?= $(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_GAMEPLAY_GATE_REGRESSION_BASELINE ?= $(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)
CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CALIBRATION_SANDBOX_BASELINE ?= $(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT)
EXPECTED_BRANCH ?=
EXPECTED_TAG ?=
FORMAT ?= json
OUTPUT ?=
BASELINE ?=
CURRENT ?=
BASELINE_DIR ?= .data/baselines
BASELINE_NAME ?= sample_point_reviewed_3d_debug_baseline_v0
BASELINE_FILE_STEM ?= reviewed_3d_debug_dataset_sample_point
BASELINE_JSON ?= $(BASELINE_DIR)/$(BASELINE_FILE_STEM).baseline.json
CURRENT_OUTPUT ?= .data/exports/reviewed_3d_debug_dataset_sample_point.current.json
REGRESSION ?= .data/exports/reviewed_3d_debug_dataset_sample_point.regression.json
REGRESSION_MARKDOWN ?=
STRICT ?= false
ALLOW_ID_DRIFT ?= true
ALLOW_FLOAT_DRIFT ?= 0.000001
COURT_MODEL ?= itf_standard_tennis_court
CAMERA_MODEL ?= homography_backed_court_plane
GEOMETRY_STATUS ?= declared
HOMOGRAPHY_MAX_GAP_MS ?= 1500
BALL_TRAJECTORY_MAX_GAP_FRAMES ?= 6
BALL_TRAJECTORY_MAX_GAP_MS ?= 250
BALL_TRAJECTORY_MIN_POINTS_PER_SEGMENT ?= 3
HIT_PLAYER_DISTANCE_MAX_TEMPLATE ?= 0.18
BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE ?= 0.18
HIT_MIN_DIRECTION_DELTA_DEGREES ?= 25
BOUNCE_MIN_DIRECTION_DELTA_DEGREES ?= 20
HIT_MIN_NET_AXIS_DELTA_TEMPLATE ?= 0.015
BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS ?= 2.0
BOUNCE_MIN_SPEED_REDUCTION_FRACTION ?= 0.05
HIT_PLAYER_TIME_WINDOW_MS ?= 300
HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION ?= 0.45
HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES ?= 5.0
BOUNCE_FALLBACK_ENABLED ?= true
BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION ?= 0.35
PLAYER_ANCHORED_HIT_ENABLED ?= true
PLAYER_ANCHORED_HIT_LOOKBACK_MS ?= 700
PLAYER_ANCHORED_HIT_LOOKAHEAD_MS ?= 1300
PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE ?= 0.24
PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE ?= 0.015
PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS ?= 60
EVENT_OVERLAP_DISTANCE_TEMPLATE ?= 0.08
NET_AXIS_REVERSAL_HIT_ENABLED ?= true
NET_AXIS_REVERSAL_LOOKBACK_MS ?= 700
NET_AXIS_REVERSAL_LOOKAHEAD_MS ?= 700
NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE ?= 0.015
NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS ?= 60
NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE ?= 0.08
IMAGE_SPACE_NET_AXIS_HIT_ENABLED ?= true
IMAGE_SPACE_NET_AXIS_LOOKBACK_MS ?= 700
IMAGE_SPACE_NET_AXIS_LOOKAHEAD_MS ?= 700
IMAGE_SPACE_NET_AXIS_MIN_DELTA_PIXELS ?= 4.0
IMAGE_SPACE_NET_AXIS_MIN_PRE_POST_GAP_MS ?= 60
IMAGE_SPACE_NET_AXIS_DEDUPE_DISTANCE_PIXELS ?= 18.0
IMAGE_SPACE_DIRECTION_CHANGE_HIT_ENABLED ?= true
IMAGE_SPACE_DIRECTION_CHANGE_LOOKBACK_MS ?= 700
IMAGE_SPACE_DIRECTION_CHANGE_LOOKAHEAD_MS ?= 700
IMAGE_SPACE_DIRECTION_CHANGE_MIN_VECTOR_PIXELS ?= 8.0
IMAGE_SPACE_DIRECTION_CHANGE_MIN_DELTA_DEGREES ?= 45.0
IMAGE_SPACE_DIRECTION_CHANGE_MIN_PRE_POST_GAP_MS ?= 60
IMAGE_SPACE_DIRECTION_CHANGE_DEDUPE_DISTANCE_PIXELS ?= 18.0
CANDIDATE_DEDUPE_MS ?= 500
AUDIT_DEMO_ONLY ?= true
AUDIT_STRICT ?= false
TOM_V3_AUDIT_REQUIRED ?= false
EVERY_N_FRAMES ?= 1
IMG_SIZE ?=
CONF ?= 0.25
IOU ?= 0.7
FRAME_START ?=
FRAME_END ?=
CLASS_MAP_JSON ?=
PLAN_ONLY ?= false
OUTPUT_DEBUG_ARTIFACT ?= false
POSE_MODE ?= crop_from_player_detection
FALLBACK_TO_FULL_FRAME ?= false
COURT_RUN_NAME ?= fixture-court-evidence
COURT_RUN_ID ?=
HOMOGRAPHY_RUN_NAME ?= homography-candidate-builder
HOMOGRAPHY_RUN_ID ?=
PROJECTION_DIAGNOSTIC_RUN_NAME ?= projection-diagnostic-builder
PROJECTION_DIAGNOSTIC_RUN_ID ?=
MIN_KEYPOINT_CONFIDENCE ?= 0.0
DERIVE_LINES ?= true

export TOM_V3_DATABASE_URL

.PHONY: install web-install test lint migrate api seed verify index-media run-gameplay index-and-run-gameplay run-detection index-and-run-detection extract-frame-artifacts build-tracklets run-pose export-tracklet-review-dataset court-review-export demo demo-fixture demo-plan demo-reset demo-export demo-open replay-open completion-audit completion-check yolo-probe yolo-smoke yolo-runtime-probe register-yolo-model smoke-real-yolo-local real-detection real-pose tom-v1-yolo-probe tom-v1-ball-detection tom-v1-player-detection tom-v1-tracklets tom-v1-main-subjects tom-v1-main-player-tracks tom-v1-pose tom-v1-pose-main-subjects tom-v1-pose-main-tracks tom-v1-motion-smoothing tom-v1-court-keypoints-probe tom-v1-court-keypoints tom-v1-court-keypoint-audit tom-v1-object-court-projection tom-v1-ball-court-trajectory tom-v1-build-3d-ball-trajectory-candidates tom-v1-build-event-candidate-3d-diagnostics tom-v1-export-reviewed-3d-debug-dataset tom-v1-compare-reviewed-3d-debug-dataset tom-v1-freeze-reviewed-3d-debug-baseline tom-v1-verify-reviewed-3d-debug-baseline tom-v1-hit-bounce-candidates tom-v1-hit-bounce-candidates-verbose tom-v1-point-evidence-snapshot tom-v1-build-point-manifest tom-v1-build-multi-point-replay-index tom-v1-build-multi-point-regression-matrix tom-v1-compare-multi-point-regression-matrix tom-v1-verify-multi-point-regression-matrix tom-v1-export-observation-quality-taxonomy tom-v1-build-observation-quality-profile tom-v1-export-review-label-schema tom-v1-build-review-label-template tom-v1-validate-review-label-bundle tom-v1-export-reviewer-confidence-schema tom-v1-build-reviewer-confidence-template tom-v1-validate-reviewer-confidence-bundle tom-v1-export-multi-reviewer-disagreement-schema tom-v1-build-multi-reviewer-review-set-template tom-v1-validate-multi-reviewer-review-set tom-v1-build-reviewer-disagreement-report tom-v1-export-intennse-label-alignment-contract tom-v1-build-intennse-alignment-template tom-v1-validate-intennse-alignment-bundle tom-v1-build-intennse-alignment-report tom-v1-export-versioned-dataset-corpus-contract tom-v1-build-versioned-dataset-corpus-manifest tom-v1-validate-versioned-dataset-corpus-manifest tom-v1-build-versioned-dataset-corpus-report tom-v1-export-coverage-sampling-strategy-contract tom-v1-build-coverage-sampling-profile tom-v1-validate-coverage-sampling-profile tom-v1-build-coverage-sampling-report tom-v1-export-many-point-ingestion-gate-contract tom-v1-build-many-point-ingestion-manifest-template tom-v1-validate-many-point-ingestion-manifest tom-v1-build-many-point-ingestion-plan tom-v1-run-many-point-ingestion-gate tom-v1-export-review-ops-metrics-contract tom-v1-build-review-ops-metrics-report tom-v1-validate-review-ops-metrics-report tom-v1-build-review-ops-dashboard-data tom-v1-export-label-feedback-evaluation-contract tom-v1-build-label-feedback-evaluation-inputs tom-v1-validate-label-feedback-evaluation-inputs tom-v1-build-label-feedback-evaluation-report tom-v1-export-camera-geometry-calibration-provenance-contract tom-v1-build-camera-geometry-calibration-profile tom-v1-validate-camera-geometry-calibration-profile tom-v1-build-camera-geometry-calibration-report tom-v1-build-tom-v3-expansion-completion-freeze tom-v1-validate-tom-v3-expansion-completion-freeze tom-v1-build-tom-v3-next-phase-readiness-report tom-v1-export-gameplay-segment-gate-contract tom-v1-inspect-gameplay-classifier-asset tom-v1-build-gameplay-segment-candidates tom-v1-validate-gameplay-segment-candidates tom-v1-build-gameplay-segment-report tom-v1-export-gameplay-gated-routing-contract tom-v1-build-gameplay-gated-routing-plan tom-v1-validate-gameplay-gated-routing-plan tom-v1-build-gameplay-gated-routing-report tom-v1-export-gameplay-gated-perception-execution-contract tom-v1-build-gameplay-gated-perception-execution-plan tom-v1-validate-gameplay-gated-perception-execution-plan tom-v1-build-gameplay-gated-perception-execution-report tom-v1-post-codex-validate tom-v1-evaluate-point-candidates tom-v1-declare-camera-geometry tom-v1-ingest-second-point-smoke tom-v1-build-second-point-evidence-parity court-fixture homography-candidates projection-diagnostics web web-build web-lint smoke all-checks
.PHONY: tom-v1-export-gameplay-segment-replay-review-contract tom-v1-build-gameplay-segment-replay-timeline tom-v1-validate-gameplay-segment-replay-timeline tom-v1-build-gameplay-segment-review-template tom-v1-validate-gameplay-segment-review-bundle tom-v1-build-gameplay-segment-review-report
.PHONY: tom-v1-export-gameplay-gated-many-point-smoke-contract tom-v1-build-gameplay-gated-many-point-smoke-manifest-template tom-v1-validate-gameplay-gated-many-point-smoke-manifest tom-v1-run-gameplay-gated-many-point-smoke tom-v1-build-gameplay-gated-many-point-smoke-report
.PHONY: tom-v1-export-gameplay-gate-regression-baseline-contract tom-v1-build-gameplay-gate-regression-baseline tom-v1-verify-gameplay-gate-regression-baseline tom-v1-build-gameplay-gate-regression-report
.PHONY: tom-v1-export-gameplay-gate-review-dataset-contract tom-v1-build-gameplay-gate-review-dataset tom-v1-validate-gameplay-gate-review-dataset tom-v1-build-gameplay-gate-review-dataset-report
.PHONY: tom-v1-build-gameplay-gate-pathway-completion-freeze tom-v1-validate-gameplay-gate-pathway-completion-freeze tom-v1-build-gameplay-gate-next-phase-readiness-report
.PHONY: tom-v1-export-real-broadcast-gameplay-corpus-run-contract tom-v1-build-real-broadcast-gameplay-corpus-manifest-template tom-v1-validate-real-broadcast-gameplay-corpus-manifest tom-v1-run-real-broadcast-gameplay-corpus tom-v1-build-real-broadcast-gameplay-corpus-report
.PHONY: tom-v1-export-real-broadcast-gameplay-review-loop-contract tom-v1-build-real-broadcast-gameplay-review-bundle-template tom-v1-validate-real-broadcast-gameplay-review-bundle tom-v1-build-real-broadcast-gameplay-review-loop-report tom-v1-build-real-broadcast-gameplay-human-review-readiness-report
.PHONY: tom-v1-export-real-broadcast-gameplay-review-metrics-contract tom-v1-build-real-broadcast-gameplay-review-metrics-report tom-v1-validate-real-broadcast-gameplay-review-metrics-report tom-v1-build-real-broadcast-gameplay-review-qa-dashboard tom-v1-build-real-broadcast-gameplay-review-next-actions-report
.PHONY: tom-v1-export-review-guided-gameplay-calibration-proposal-contract tom-v1-build-review-guided-gameplay-calibration-inputs tom-v1-validate-review-guided-gameplay-calibration-inputs tom-v1-build-review-guided-gameplay-calibration-proposal tom-v1-validate-review-guided-gameplay-calibration-proposal tom-v1-build-review-guided-gameplay-calibration-proposal-report
.PHONY: tom-v1-export-review-guided-gameplay-calibration-evaluation-sandbox-contract tom-v1-build-review-guided-gameplay-calibration-evaluation-inputs tom-v1-validate-review-guided-gameplay-calibration-evaluation-inputs tom-v1-run-review-guided-gameplay-calibration-evaluation-sandbox tom-v1-validate-review-guided-gameplay-calibration-evaluation-report tom-v1-build-review-guided-gameplay-calibration-evaluation-summary
.PHONY: tom-v1-export-review-guided-gameplay-calibration-sandbox-regression-contract tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-baseline tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-report
.PHONY: tom-v1-export-calibration-candidate-decision-packet-contract tom-v1-build-calibration-candidate-decision-packet-inputs tom-v1-validate-calibration-candidate-decision-packet-inputs tom-v1-build-calibration-candidate-decision-packet tom-v1-validate-calibration-candidate-decision-packet tom-v1-build-calibration-candidate-decision-packet-report

install:
	$(PYTHON) -m pip install -e ".[dev]"

web-install:
	cd $(WEB_DIR) && npm install

test:
	$(PYTHON) -m pytest -q

lint:
	ruff check .

migrate:
	alembic upgrade head

api:
	uvicorn apps.api.main:app --reload

seed:
	$(PYTHON) -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run

verify:
	@if [ -z "$(RUN_ID)" ]; then echo "RUN_ID is required: make verify RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli verify-synthetic-run --run-id $(RUN_ID)

index-media:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-media SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-media --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)"

tom-v1-ingest-second-point-smoke:
	@if [ -z "$(SECOND_POINT_MEDIA_PATH)" ]; then echo "missing_second_point_media_path: SECOND_POINT_MEDIA_PATH is required"; exit 1; fi
	$(PYTHON) -m apps.worker.cli ingest-second-point-smoke --media-path "$(SECOND_POINT_MEDIA_PATH)" --run-name "$(SECOND_POINT_SMOKE_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" --storage-root "$(STORAGE_ROOT)" $(if $(SECOND_POINT_MANIFEST_OUTPUT),--manifest-output "$(SECOND_POINT_MANIFEST_OUTPUT)",)

tom-v1-build-second-point-evidence-parity:
	@if [ -z "$(SECOND_POINT_MEDIA_PATH)" ]; then echo "missing_second_point_media_path: SECOND_POINT_MEDIA_PATH is required"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-second-point-evidence-parity --media-path "$(SECOND_POINT_MEDIA_PATH)" --run-name "$(SECOND_POINT_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" --storage-root "$(STORAGE_ROOT)" --baseline-manifest-output "$(SECOND_POINT_BASELINE_MANIFEST_OUTPUT)"

run-gameplay:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-gameplay MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-gameplay-adapter --media-id "$(MEDIA_ID)" --adapter "$(ADAPTER)"

index-and-run-gameplay:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-and-run-gameplay SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-and-run-gameplay --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)" --adapter "$(ADAPTER)"

run-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-detection-adapter --media-id "$(MEDIA_ID)" --adapter "$(ADAPTER)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)"

index-and-run-detection:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-and-run-detection SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-and-run-detection --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)" --adapter "$(ADAPTER)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)"

extract-frame-artifacts:
	@if [ -z "$(RUN_ID)" ]; then echo "RUN_ID is required: make extract-frame-artifacts RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli extract-frame-artifacts --run-id "$(RUN_ID)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)"

build-tracklets:
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make build-tracklets DETECTION_RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-tracklets --detection-run-id "$(DETECTION_RUN_ID)" --run-name "$(RUN_NAME)" --max-gap-frames "$(MAX_GAP_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

run-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-pose MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-pose-adapter --media-id "$(MEDIA_ID)" --adapter fixture --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" $(if $(SOURCE_DETECTION_RUN_ID),--source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)",) $(if $(filter true,$(LINK_SOURCE_DETECTIONS)),--link-source-detections,--no-link-source-detections)

export-tracklet-review-dataset:
	@if [ -z "$(TRACKLET_ID)" ] && [ -z "$(QUERY_JSON)" ]; then echo "TRACKLET_ID or QUERY_JSON is required"; exit 1; fi
	@if [ -n "$(TRACKLET_ID)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --tracklet-id "$(TRACKLET_ID)" --output-root "$(EXPORT_ROOT)"; else $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --query-json '$(QUERY_JSON)' --output-root "$(EXPORT_ROOT)"; fi

demo:
	$(PYTHON) -m apps.worker.cli run-demo $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-fixture:
	$(PYTHON) -m apps.worker.cli run-demo $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-plan:
	$(PYTHON) -m apps.worker.cli run-demo --plan-only $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-reset:
	@echo "demo-reset is intentionally non-destructive. TOM v3 demo runs are additive."; \
	echo "To start fresh, set TOM_V3_DATABASE_URL to a new SQLite file, for example:"; \
	echo "  TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo.db make demo"; \
	echo "Local demo outputs live under .data/demo, $(ARTIFACT_ROOT), and $(EXPORT_ROOT). Remove only files you intentionally created."

demo-export:
	@if [ -z "$(RUN_ID)" ] && [ -z "$(TRACKLET_ID)" ] && [ -z "$(QUERY_JSON)" ]; then echo "RUN_ID for pose export or TRACKLET_ID/QUERY_JSON for tracklet export is required."; exit 1; fi
	@if [ -n "$(RUN_ID)" ]; then $(PYTHON) -m apps.worker.cli export-pose-review-dataset --run-id "$(RUN_ID)" --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi
	@if [ -n "$(TRACKLET_ID)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --tracklet-id "$(TRACKLET_ID)" --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi
	@if [ -n "$(QUERY_JSON)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --query-json '$(QUERY_JSON)' --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi

demo-open:
	@echo "Open viewer URLs manually:"; \
	if [ -n "$(RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(RUN_ID)"; fi; \
	if [ -n "$(DETECTION_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(DETECTION_RUN_ID)"; fi; \
	if [ -n "$(TRACKLET_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(TRACKLET_RUN_ID)"; fi; \
	if [ -n "$(POSE_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(POSE_RUN_ID)"; fi; \
	if [ -z "$(RUN_ID)" ] && [ -z "$(DETECTION_RUN_ID)" ] && [ -z "$(TRACKLET_RUN_ID)" ] && [ -z "$(POSE_RUN_ID)" ]; then echo "Pass RUN_ID=<run_id>, DETECTION_RUN_ID=<run_id>, TRACKLET_RUN_ID=<run_id>, or POSE_RUN_ID=<run_id>."; fi

replay-open:
	@if [ -z "$(MEDIA_ID)" ]; then \
		echo "Pass MEDIA_ID=<media_id>, then open:"; \
		echo "  $(VIEWER_BASE_URL)/replay/<media_id>"; \
		echo "Optional: MODE=stream_proxy DETECTION_RUN_ID=<run_id> TRACKLET_RUN_ID=<run_id> POSE_RUN_ID=<run_id>"; \
	else \
		url="$(VIEWER_BASE_URL)/replay/$(MEDIA_ID)"; sep="?"; \
		if [ -n "$(MODE)" ]; then url="$$url$${sep}mode=$(MODE)"; sep="&"; fi; \
		if [ -n "$(DETECTION_RUN_ID)" ]; then url="$$url$${sep}detectionRunId=$(DETECTION_RUN_ID)"; sep="&"; fi; \
		if [ -n "$(TRACKLET_RUN_ID)" ]; then url="$$url$${sep}trackletRunId=$(TRACKLET_RUN_ID)"; sep="&"; fi; \
		if [ -n "$(POSE_RUN_ID)" ]; then url="$$url$${sep}poseRunId=$(POSE_RUN_ID)"; sep="&"; fi; \
		echo "$$url"; \
	fi

completion-audit:
	$(PYTHON) -m apps.worker.cli completion-audit $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(filter false,$(AUDIT_DEMO_ONLY)),--no-demo-only,--demo-only) $(if $(filter true,$(AUDIT_STRICT)),--strict,--no-strict)

completion-check:
	$(PYTHON) -m pytest -q
	ruff check .
	$(PYTHON) scripts/smoke_synthetic_viewer_data.py
	@if [ "$(TOM_V3_AUDIT_REQUIRED)" = "true" ]; then \
		$(PYTHON) -m apps.worker.cli completion-audit --demo-only; \
	else \
		echo "Run make demo then make completion-audit for the full provenance audit."; \
	fi

yolo-probe: yolo-runtime-probe

yolo-smoke:
	$(PYTHON) -m apps.worker.cli smoke-real-yolo-local --plan-only $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",) $(if $(WEIGHTS_PATH),--weights-path "$(WEIGHTS_PATH)",) $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" --device "$(YOLO_DEVICE)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)" $(if $(filter true,$(RUN_TRACKLETS)),--run-tracklets,--no-run-tracklets)

yolo-runtime-probe:
	$(PYTHON) -m apps.worker.cli yolo-runtime-probe --device "$(YOLO_DEVICE)"

register-yolo-model:
	@if [ -z "$(WEIGHTS_PATH)" ]; then echo "WEIGHTS_PATH is required: make register-yolo-model WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli register-yolo-model --weights-path "$(WEIGHTS_PATH)" --model-version "$(MODEL_VERSION)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",)

smoke-real-yolo-local:
	$(PYTHON) -m apps.worker.cli smoke-real-yolo-local $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",) $(if $(WEIGHTS_PATH),--weights-path "$(WEIGHTS_PATH)",) $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" --device "$(YOLO_DEVICE)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)" $(if $(filter true,$(RUN_TRACKLETS)),--run-tracklets,--no-run-tracklets)

real-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	@if [ -z "$(YOLO_WEIGHTS_PATH)" ]; then echo "YOLO_WEIGHTS_PATH is required: make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(YOLO_WEIGHTS_PATH)" --device "$(YOLO_DEVICE)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",) $(if $(IMG_SIZE),--imgsz "$(IMG_SIZE)",) $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

real-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make real-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<run_id> POSE_WEIGHTS_PATH=model_assets/pose/model.pt"; exit 1; fi
	@if [ -z "$(POSE_WEIGHTS_PATH)" ]; then echo "POSE_WEIGHTS_PATH is required: make real-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<run_id> POSE_WEIGHTS_PATH=model_assets/pose/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --weights "$(POSE_WEIGHTS_PATH)" $(if $(SOURCE_DETECTION_RUN_ID),--source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)",) $(if $(SOURCE_SUBJECT_RUN_ID),--source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)",) $(if $(SOURCE_TRACK_RUN_ID),--source-track-run-id "$(SOURCE_TRACK_RUN_ID)",) --mode "$(POSE_MODE)" --device "$(YOLO_DEVICE)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",) $(if $(IMG_SIZE),--imgsz "$(IMG_SIZE)",) $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-yolo-probe:
	$(PYTHON) -m apps.worker.cli yolo-runtime-probe --device "$(YOLO_DEVICE)"

tom-v1-ball-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-ball-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/best_ball_v2_1280.pt" --model-name tom-v1-best-ball-v2-1280 --model-version v1-local --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),1280)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_BALL_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-player-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-player-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x.pt" --model-name tom-v1-yolo26x-player-detector --model-version v1-local --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_PLAYER_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-tracklets:
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-tracklets DETECTION_RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-tracklets --detection-run-id "$(DETECTION_RUN_ID)" --run-name tom-v1-model-derived-tracklets --max-gap-frames "$(MAX_GAP_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

tom-v1-main-subjects:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-main-subjects MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-main-subjects DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli select-main-player-subjects --media-id "$(MEDIA_ID)" --source-detection-run-id "$(DETECTION_RUN_ID)" --run-name main-player-subject-filter-v0 --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-main-player-tracks:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-main-player-tracks MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-main-player-tracks DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-main-player-tracks SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli assign-main-player-tracks --media-id "$(MEDIA_ID)" --source-detection-run-id "$(DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --run-name main-player-track-assignment-v01 --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose-main-subjects:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose-main-subjects MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose-main-subjects SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-pose-main-subjects SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose-main-tracks:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose-main-tracks MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> SOURCE_TRACK_RUN_ID=<main_player_track_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_TRACK_RUN_ID)" ]; then echo "SOURCE_TRACK_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_TRACK_RUN_ID=<main_player_track_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --source-track-run-id "$(SOURCE_TRACK_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-motion-smoothing:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-motion-smoothing MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli smooth-motion-candidates --media-id "$(MEDIA_ID)" $(if $(DETECTION_RUN_ID),--detection-run-id "$(DETECTION_RUN_ID)",) $(if $(TRACKLET_RUN_ID),--tracklet-run-id "$(TRACKLET_RUN_ID)",) $(if $(MAIN_PLAYER_TRACK_RUN_ID),--main-player-track-run-id "$(MAIN_PLAYER_TRACK_RUN_ID)",) $(if $(POSE_RUN_ID),--pose-run-id "$(POSE_RUN_ID)",) --run-name motion-smoothing-stable-replay-candidates-v0 --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-object-court-projection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-object-court-projection MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(MOTION_SMOOTHING_RUN_ID)" ]; then echo "MOTION_SMOOTHING_RUN_ID is required: make tom-v1-object-court-projection MOTION_SMOOTHING_RUN_ID=<motion_smoothing_run_id>"; exit 1; fi
	@if [ -z "$(HOMOGRAPHY_RUN_ID)" ]; then echo "HOMOGRAPHY_RUN_ID is required: make tom-v1-object-court-projection HOMOGRAPHY_RUN_ID=<homography_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli project-objects-to-court --media-id "$(MEDIA_ID)" --motion-smoothing-run-id "$(MOTION_SMOOTHING_RUN_ID)" --homography-run-id "$(HOMOGRAPHY_RUN_ID)" --run-name "$(COURT_PROJECTION_RUN_NAME)" --homography-max-gap-ms "$(HOMOGRAPHY_MAX_GAP_MS)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-ball-court-trajectory:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-ball-court-trajectory MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(COURT_PROJECTION_RUN_ID)" ]; then echo "COURT_PROJECTION_RUN_ID is required: make tom-v1-ball-court-trajectory COURT_PROJECTION_RUN_ID=<court_projection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-ball-court-trajectory --media-id "$(MEDIA_ID)" --court-projection-run-id "$(COURT_PROJECTION_RUN_ID)" --run-name "$(BALL_TRAJECTORY_RUN_NAME)" --max-gap-frames "$(BALL_TRAJECTORY_MAX_GAP_FRAMES)" --max-gap-ms "$(BALL_TRAJECTORY_MAX_GAP_MS)" --min-points-per-segment "$(BALL_TRAJECTORY_MIN_POINTS_PER_SEGMENT)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-build-3d-ball-trajectory-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-build-3d-ball-trajectory-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(BALL_TRAJECTORY_RUN_ID)" ]; then echo "BALL_TRAJECTORY_RUN_ID is required: make tom-v1-build-3d-ball-trajectory-candidates BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id>"; exit 1; fi
	@if [ -z "$(CAMERA_GEOMETRY_ID)" ]; then echo "CAMERA_GEOMETRY_ID is required: make tom-v1-build-3d-ball-trajectory-candidates CAMERA_GEOMETRY_ID=<camera_geometry_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-3d-ball-trajectory-candidates --media-id "$(MEDIA_ID)" --ball-trajectory-run-id "$(BALL_TRAJECTORY_RUN_ID)" $(if $(COURT_PROJECTION_RUN_ID),--court-projection-run-id "$(COURT_PROJECTION_RUN_ID)",) --camera-geometry-id "$(CAMERA_GEOMETRY_ID)" --height-model "$(HEIGHT_MODEL)" --run-name "$(BALL_TRAJECTORY_3D_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",)

tom-v1-build-event-candidate-3d-diagnostics:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-build-event-candidate-3d-diagnostics MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-build-event-candidate-3d-diagnostics EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	@if [ -z "$(TRAJECTORY_3D_RUN_ID)" ]; then echo "TRAJECTORY_3D_RUN_ID is required: make tom-v1-build-event-candidate-3d-diagnostics TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-event-candidate-3d-diagnostics --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)" $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) --time-window-ms "$(TIME_WINDOW_MS)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",)

tom-v1-export-reviewed-3d-debug-dataset:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-export-reviewed-3d-debug-dataset MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-export-reviewed-3d-debug-dataset EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	@if [ -z "$(TRAJECTORY_3D_RUN_ID)" ]; then echo "TRAJECTORY_3D_RUN_ID is required: make tom-v1-export-reviewed-3d-debug-dataset TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id>"; exit 1; fi
	@if [ -z "$(CAMERA_GEOMETRY_ID)" ]; then echo "CAMERA_GEOMETRY_ID is required: make tom-v1-export-reviewed-3d-debug-dataset CAMERA_GEOMETRY_ID=<camera_geometry_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli export-reviewed-3d-debug-dataset --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)" --camera-geometry-id "$(CAMERA_GEOMETRY_ID)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",)

tom-v1-compare-reviewed-3d-debug-dataset:
	@if [ -z "$(BASELINE)" ]; then echo "BASELINE is required: make tom-v1-compare-reviewed-3d-debug-dataset BASELINE=<baseline_export.json>"; exit 1; fi
	@if [ -z "$(CURRENT)" ]; then echo "CURRENT is required: make tom-v1-compare-reviewed-3d-debug-dataset CURRENT=<current_export.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli compare-reviewed-3d-debug-dataset --baseline "$(BASELINE)" --current "$(CURRENT)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",) $(if $(filter true,$(STRICT)),--strict,--no-strict) $(if $(filter false,$(ALLOW_ID_DRIFT)),--no-allow-id-drift,--allow-id-drift) --allow-float-drift "$(ALLOW_FLOAT_DRIFT)"

tom-v1-freeze-reviewed-3d-debug-baseline:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-freeze-reviewed-3d-debug-baseline MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-freeze-reviewed-3d-debug-baseline EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	@if [ -z "$(TRAJECTORY_3D_RUN_ID)" ]; then echo "TRAJECTORY_3D_RUN_ID is required: make tom-v1-freeze-reviewed-3d-debug-baseline TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id>"; exit 1; fi
	@if [ -z "$(CAMERA_GEOMETRY_ID)" ]; then echo "CAMERA_GEOMETRY_ID is required: make tom-v1-freeze-reviewed-3d-debug-baseline CAMERA_GEOMETRY_ID=<camera_geometry_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli freeze-reviewed-3d-debug-baseline --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)" --camera-geometry-id "$(CAMERA_GEOMETRY_ID)" --baseline-dir "$(BASELINE_DIR)" --baseline-name "$(BASELINE_NAME)" --file-stem "$(BASELINE_FILE_STEM)" --viewer-base-url "$(VIEWER_BASE_URL)"

tom-v1-verify-reviewed-3d-debug-baseline:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-verify-reviewed-3d-debug-baseline MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-verify-reviewed-3d-debug-baseline EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	@if [ -z "$(TRAJECTORY_3D_RUN_ID)" ]; then echo "TRAJECTORY_3D_RUN_ID is required: make tom-v1-verify-reviewed-3d-debug-baseline TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id>"; exit 1; fi
	@if [ -z "$(CAMERA_GEOMETRY_ID)" ]; then echo "CAMERA_GEOMETRY_ID is required: make tom-v1-verify-reviewed-3d-debug-baseline CAMERA_GEOMETRY_ID=<camera_geometry_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli verify-reviewed-3d-debug-baseline --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)" --camera-geometry-id "$(CAMERA_GEOMETRY_ID)" --baseline "$(if $(BASELINE),$(BASELINE),$(BASELINE_JSON))" --current-output "$(CURRENT_OUTPUT)" --regression-output "$(REGRESSION)" $(if $(REGRESSION_MARKDOWN),--regression-markdown-output "$(REGRESSION_MARKDOWN)",) $(if $(filter true,$(STRICT)),--strict,--no-strict) --viewer-base-url "$(VIEWER_BASE_URL)"

tom-v1-hit-bounce-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-hit-bounce-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(BALL_TRAJECTORY_RUN_ID)" ]; then echo "BALL_TRAJECTORY_RUN_ID is required: make tom-v1-hit-bounce-candidates BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id>"; exit 1; fi
	@if [ -z "$(COURT_PROJECTION_RUN_ID)" ]; then echo "COURT_PROJECTION_RUN_ID is required: make tom-v1-hit-bounce-candidates COURT_PROJECTION_RUN_ID=<court_projection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-hit-bounce-candidates --media-id "$(MEDIA_ID)" --ball-trajectory-run-id "$(BALL_TRAJECTORY_RUN_ID)" --court-projection-run-id "$(COURT_PROJECTION_RUN_ID)" --run-name "$(EVENT_CANDIDATE_RUN_NAME)" --hit-player-distance-max-template "$(HIT_PLAYER_DISTANCE_MAX_TEMPLATE)" --bounce-player-distance-min-template "$(BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE)" --hit-min-direction-delta-degrees "$(HIT_MIN_DIRECTION_DELTA_DEGREES)" --bounce-min-direction-delta-degrees "$(BOUNCE_MIN_DIRECTION_DELTA_DEGREES)" --hit-min-net-axis-delta-template "$(HIT_MIN_NET_AXIS_DELTA_TEMPLATE)" --bounce-min-image-y-delta-pixels "$(BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS)" --bounce-min-speed-reduction-fraction "$(BOUNCE_MIN_SPEED_REDUCTION_FRACTION)" --hit-player-time-window-ms "$(HIT_PLAYER_TIME_WINDOW_MS)" --hit-contact-fallback-min-speed-delta-fraction "$(HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION)" --hit-contact-fallback-min-direction-delta-degrees "$(HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES)" $(if $(filter false,$(BOUNCE_FALLBACK_ENABLED)),--no-bounce-fallback-enabled,--bounce-fallback-enabled) --bounce-fallback-min-speed-reduction-fraction "$(BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION)" $(if $(filter false,$(PLAYER_ANCHORED_HIT_ENABLED)),--no-player-anchored-hit-enabled,--player-anchored-hit-enabled) --player-anchored-hit-lookback-ms "$(PLAYER_ANCHORED_HIT_LOOKBACK_MS)" --player-anchored-hit-lookahead-ms "$(PLAYER_ANCHORED_HIT_LOOKAHEAD_MS)" --player-anchored-hit-distance-max-template "$(PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE)" --player-anchored-hit-min-net-axis-delta-template "$(PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE)" --player-anchored-hit-min-pre-post-gap-ms "$(PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS)" --event-overlap-distance-template "$(EVENT_OVERLAP_DISTANCE_TEMPLATE)" $(if $(filter false,$(NET_AXIS_REVERSAL_HIT_ENABLED)),--no-net-axis-reversal-hit-enabled,--net-axis-reversal-hit-enabled) --net-axis-reversal-lookback-ms "$(NET_AXIS_REVERSAL_LOOKBACK_MS)" --net-axis-reversal-lookahead-ms "$(NET_AXIS_REVERSAL_LOOKAHEAD_MS)" --net-axis-reversal-min-delta-template "$(NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE)" --net-axis-reversal-min-pre-post-gap-ms "$(NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS)" --net-axis-reversal-dedupe-distance-template "$(NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE)" $(if $(filter false,$(IMAGE_SPACE_NET_AXIS_HIT_ENABLED)),--no-image-space-net-axis-hit-enabled,--image-space-net-axis-hit-enabled) --image-space-net-axis-lookback-ms "$(IMAGE_SPACE_NET_AXIS_LOOKBACK_MS)" --image-space-net-axis-lookahead-ms "$(IMAGE_SPACE_NET_AXIS_LOOKAHEAD_MS)" --image-space-net-axis-min-delta-pixels "$(IMAGE_SPACE_NET_AXIS_MIN_DELTA_PIXELS)" --image-space-net-axis-min-pre-post-gap-ms "$(IMAGE_SPACE_NET_AXIS_MIN_PRE_POST_GAP_MS)" --image-space-net-axis-dedupe-distance-pixels "$(IMAGE_SPACE_NET_AXIS_DEDUPE_DISTANCE_PIXELS)" $(if $(filter false,$(IMAGE_SPACE_DIRECTION_CHANGE_HIT_ENABLED)),--no-image-space-direction-change-hit-enabled,--image-space-direction-change-hit-enabled) --image-space-direction-change-lookback-ms "$(IMAGE_SPACE_DIRECTION_CHANGE_LOOKBACK_MS)" --image-space-direction-change-lookahead-ms "$(IMAGE_SPACE_DIRECTION_CHANGE_LOOKAHEAD_MS)" --image-space-direction-change-min-vector-pixels "$(IMAGE_SPACE_DIRECTION_CHANGE_MIN_VECTOR_PIXELS)" --image-space-direction-change-min-delta-degrees "$(IMAGE_SPACE_DIRECTION_CHANGE_MIN_DELTA_DEGREES)" --image-space-direction-change-min-pre-post-gap-ms "$(IMAGE_SPACE_DIRECTION_CHANGE_MIN_PRE_POST_GAP_MS)" --image-space-direction-change-dedupe-distance-pixels "$(IMAGE_SPACE_DIRECTION_CHANGE_DEDUPE_DISTANCE_PIXELS)" --candidate-dedupe-ms "$(CANDIDATE_DEDUPE_MS)" --viewer-base-url "$(VIEWER_BASE_URL)" --diagnostic-summary "$(DIAGNOSTIC_SUMMARY)" $(if $(filter true 1,$(HIT_BOUNCE_VERBOSE) $(VERBOSE)),--verbose,) $(if $(filter true 1,$(INCLUDE_OBSERVATION_IDS)),--include-observation-ids,) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-hit-bounce-candidates-verbose:
	$(MAKE) tom-v1-hit-bounce-candidates HIT_BOUNCE_VERBOSE=true INCLUDE_OBSERVATION_IDS=true DIAGNOSTIC_SUMMARY=full

tom-v1-point-evidence-snapshot:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-point-evidence-snapshot MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-point-evidence-snapshot EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-point-evidence-snapshot --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(POINT_SNAPSHOT_FORMAT)" $(if $(POINT_SNAPSHOT_OUTPUT),--output "$(POINT_SNAPSHOT_OUTPUT)",)

tom-v1-build-point-manifest:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-build-point-manifest MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-point-manifest --media-id "$(MEDIA_ID)" $(if $(EVENT_CANDIDATE_RUN_ID),--event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)",) $(if $(TRAJECTORY_3D_RUN_ID),--trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)",) $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(POINT_MANIFEST_OUTPUT),--output "$(POINT_MANIFEST_OUTPUT)",)

tom-v1-build-multi-point-replay-index:
	$(PYTHON) -m apps.worker.cli build-multi-point-replay-index --manifest-root "$(POINT_MANIFEST_ROOT)" --viewer-base-url "$(VIEWER_BASE_URL)" --output "$(MULTI_POINT_REPLAY_INDEX_OUTPUT)" --skip-create-db

tom-v1-build-multi-point-regression-matrix:
	$(PYTHON) -m apps.worker.cli build-multi-point-regression-matrix --index "$(MULTI_POINT_REPLAY_INDEX_OUTPUT)" --output "$(MULTI_POINT_REGRESSION_MATRIX_OUTPUT)" --skip-create-db

tom-v1-compare-multi-point-regression-matrix:
	@if [ -z "$(BASELINE)" ]; then echo "BASELINE is required: make tom-v1-compare-multi-point-regression-matrix BASELINE=<baseline_matrix.json>"; exit 1; fi
	@if [ -z "$(CURRENT)" ]; then echo "CURRENT is required: make tom-v1-compare-multi-point-regression-matrix CURRENT=<current_matrix.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli compare-multi-point-regression-matrix --baseline "$(BASELINE)" --current "$(CURRENT)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",) $(if $(filter true,$(STRICT)),--strict,--no-strict) --skip-create-db

tom-v1-verify-multi-point-regression-matrix:
	$(PYTHON) -m apps.worker.cli verify-multi-point-regression-matrix --index "$(MULTI_POINT_REPLAY_INDEX_OUTPUT)" --baseline "$(MULTI_POINT_REGRESSION_MATRIX_BASELINE)" --current-output "$(MULTI_POINT_REGRESSION_MATRIX_CURRENT)" --regression-output "$(MULTI_POINT_REGRESSION_MATRIX_REGRESSION)" --regression-markdown-output "$(MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN)" $(if $(filter true,$(STRICT)),--strict,--no-strict) --skip-create-db

tom-v1-export-observation-quality-taxonomy:
	$(PYTHON) -m apps.worker.cli export-observation-quality-taxonomy --output "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --skip-create-db

tom-v1-build-observation-quality-profile:
	$(PYTHON) -m apps.worker.cli build-observation-quality-profile --index "$(OBSERVATION_QUALITY_PROFILE_SOURCE_INDEX)" --output "$(OBSERVATION_QUALITY_PROFILE_OUTPUT)" --skip-create-db

tom-v1-export-review-label-schema:
	$(PYTHON) -m apps.worker.cli export-review-label-schema --output "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --skip-create-db

tom-v1-build-review-label-template:
	$(PYTHON) -m apps.worker.cli build-review-label-template $(if $(POINT_MANIFEST_ID),--point-manifest-id "$(POINT_MANIFEST_ID)",) $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(REPLAY_URL),--replay-url "$(REPLAY_URL)",) $(if $(EVENT_CANDIDATE_RUN_ID),--event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)",) $(if $(TRAJECTORY_3D_RUN_ID),--trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)",) $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) --output "$(REVIEW_LABEL_TEMPLATE_OUTPUT)" --skip-create-db

tom-v1-validate-review-label-bundle:
	@if [ -z "$(REVIEW_LABEL_BUNDLE)" ]; then echo "REVIEW_LABEL_BUNDLE is required: make tom-v1-validate-review-label-bundle REVIEW_LABEL_BUNDLE=<bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-review-label-bundle --schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --bundle "$(REVIEW_LABEL_BUNDLE)" --output "$(REVIEW_LABEL_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-export-reviewer-confidence-schema:
	$(PYTHON) -m apps.worker.cli export-reviewer-confidence-schema --output "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --skip-create-db

tom-v1-build-reviewer-confidence-template:
	$(PYTHON) -m apps.worker.cli build-reviewer-confidence-template $(if $(POINT_MANIFEST_ID),--point-manifest-id "$(POINT_MANIFEST_ID)",) $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(REPLAY_URL),--replay-url "$(REPLAY_URL)",) $(if $(EVENT_CANDIDATE_RUN_ID),--event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)",) $(if $(TRAJECTORY_3D_RUN_ID),--trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)",) $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) --output "$(REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT)" --skip-create-db

tom-v1-validate-reviewer-confidence-bundle:
	@if [ -z "$(REVIEWER_CONFIDENCE_BUNDLE)" ]; then echo "REVIEWER_CONFIDENCE_BUNDLE is required: make tom-v1-validate-reviewer-confidence-bundle REVIEWER_CONFIDENCE_BUNDLE=<bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-reviewer-confidence-bundle --schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --bundle "$(REVIEWER_CONFIDENCE_BUNDLE)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --output "$(REVIEWER_CONFIDENCE_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-export-multi-reviewer-disagreement-schema:
	$(PYTHON) -m apps.worker.cli export-multi-reviewer-disagreement-schema --output "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --skip-create-db

tom-v1-build-multi-reviewer-review-set-template:
	$(PYTHON) -m apps.worker.cli build-multi-reviewer-review-set-template $(if $(POINT_MANIFEST_ID),--point-manifest-id "$(POINT_MANIFEST_ID)",) $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(REPLAY_URL),--replay-url "$(REPLAY_URL)",) $(if $(EVENT_CANDIDATE_RUN_ID),--event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)",) $(if $(TRAJECTORY_3D_RUN_ID),--trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)",) $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) --reviewer-count "$(REVIEWER_COUNT)" --output "$(MULTI_REVIEWER_REVIEW_SET_OUTPUT)" --skip-create-db

tom-v1-validate-multi-reviewer-review-set:
	@if [ -z "$(MULTI_REVIEWER_REVIEW_SET)" ]; then echo "MULTI_REVIEWER_REVIEW_SET is required: make tom-v1-validate-multi-reviewer-review-set MULTI_REVIEWER_REVIEW_SET=<review-set.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-multi-reviewer-review-set --schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --review-set "$(MULTI_REVIEWER_REVIEW_SET)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --output "$(MULTI_REVIEWER_REVIEW_SET_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-reviewer-disagreement-report:
	@if [ -z "$(MULTI_REVIEWER_REVIEW_SET)" ]; then echo "MULTI_REVIEWER_REVIEW_SET is required: make tom-v1-build-reviewer-disagreement-report MULTI_REVIEWER_REVIEW_SET=<review-set.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-reviewer-disagreement-report --schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --review-set "$(MULTI_REVIEWER_REVIEW_SET)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --output "$(REVIEWER_DISAGREEMENT_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-intennse-label-alignment-contract:
	$(PYTHON) -m apps.worker.cli export-intennse-label-alignment-contract --output "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-intennse-alignment-template:
	$(PYTHON) -m apps.worker.cli build-intennse-alignment-template $(if $(POINT_MANIFEST_ID),--point-manifest-id "$(POINT_MANIFEST_ID)",) $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(REPLAY_URL),--replay-url "$(REPLAY_URL)",) $(if $(EVENT_CANDIDATE_RUN_ID),--event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)",) $(if $(TRAJECTORY_3D_RUN_ID),--trajectory-3d-run-id "$(TRAJECTORY_3D_RUN_ID)",) $(if $(CAMERA_GEOMETRY_ID),--camera-geometry-id "$(CAMERA_GEOMETRY_ID)",) $(if $(REVIEW_LABEL_BUNDLE),--tom-review-label-bundle-ref "$(REVIEW_LABEL_BUNDLE)",) $(if $(REVIEWER_CONFIDENCE_BUNDLE),--tom-reviewer-confidence-bundle-ref "$(REVIEWER_CONFIDENCE_BUNDLE)",) $(if $(MULTI_REVIEWER_REVIEW_SET),--tom-multi-reviewer-review-set-ref "$(MULTI_REVIEWER_REVIEW_SET)",) $(if $(TOM_DISAGREEMENT_REPORT_REF),--tom-disagreement-report-ref "$(TOM_DISAGREEMENT_REPORT_REF)",) $(if $(INTENNSE_LABEL_BUNDLE_REF),--intennse-label-bundle-ref "$(INTENNSE_LABEL_BUNDLE_REF)",) $(if $(INTENNSE_SCHEMA_VERSION),--intennse-schema-version "$(INTENNSE_SCHEMA_VERSION)",) --output "$(INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT)" --skip-create-db

tom-v1-validate-intennse-alignment-bundle:
	@if [ -z "$(INTENNSE_ALIGNMENT_BUNDLE)" ]; then echo "INTENNSE_ALIGNMENT_BUNDLE is required: make tom-v1-validate-intennse-alignment-bundle INTENNSE_ALIGNMENT_BUNDLE=<bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-intennse-alignment-bundle --contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --bundle "$(INTENNSE_ALIGNMENT_BUNDLE)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --output "$(INTENNSE_ALIGNMENT_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-intennse-alignment-report:
	@if [ -z "$(INTENNSE_ALIGNMENT_BUNDLE)" ]; then echo "INTENNSE_ALIGNMENT_BUNDLE is required: make tom-v1-build-intennse-alignment-report INTENNSE_ALIGNMENT_BUNDLE=<bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-intennse-alignment-report --contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --bundle "$(INTENNSE_ALIGNMENT_BUNDLE)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --output "$(INTENNSE_ALIGNMENT_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-versioned-dataset-corpus-contract:
	$(PYTHON) -m apps.worker.cli export-versioned-dataset-corpus-contract --output "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-versioned-dataset-corpus-manifest:
	$(PYTHON) -m apps.worker.cli build-versioned-dataset-corpus-manifest --index "$(DATASET_CORPUS_SOURCE_INDEX)" --matrix "$(DATASET_CORPUS_SOURCE_MATRIX)" --corpus-version "$(DATASET_CORPUS_VERSION)" --output "$(DATASET_CORPUS_MANIFEST_OUTPUT)" $(if $(DATASET_CORPUS_ID),--corpus-id "$(DATASET_CORPUS_ID)",) --skip-create-db

tom-v1-validate-versioned-dataset-corpus-manifest:
	@if [ -z "$(DATASET_CORPUS_MANIFEST)" ]; then echo "DATASET_CORPUS_MANIFEST is required: make tom-v1-validate-versioned-dataset-corpus-manifest DATASET_CORPUS_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-versioned-dataset-corpus-manifest --contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --manifest "$(DATASET_CORPUS_MANIFEST)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --output "$(DATASET_CORPUS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-versioned-dataset-corpus-report:
	@if [ -z "$(DATASET_CORPUS_MANIFEST)" ]; then echo "DATASET_CORPUS_MANIFEST is required: make tom-v1-build-versioned-dataset-corpus-report DATASET_CORPUS_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-versioned-dataset-corpus-report --contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --manifest "$(DATASET_CORPUS_MANIFEST)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --output "$(DATASET_CORPUS_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-coverage-sampling-strategy-contract:
	$(PYTHON) -m apps.worker.cli export-coverage-sampling-strategy-contract --output "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-coverage-sampling-profile:
	$(PYTHON) -m apps.worker.cli build-coverage-sampling-profile --corpus-manifest "$(COVERAGE_SAMPLING_SOURCE_CORPUS_MANIFEST)" --index "$(COVERAGE_SAMPLING_SOURCE_INDEX)" --matrix "$(COVERAGE_SAMPLING_SOURCE_MATRIX)" --output "$(COVERAGE_SAMPLING_PROFILE_OUTPUT)" --skip-create-db

tom-v1-validate-coverage-sampling-profile:
	@if [ -z "$(COVERAGE_SAMPLING_PROFILE)" ]; then echo "COVERAGE_SAMPLING_PROFILE is required: make tom-v1-validate-coverage-sampling-profile COVERAGE_SAMPLING_PROFILE=<profile.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-coverage-sampling-profile --contract "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --profile "$(COVERAGE_SAMPLING_PROFILE)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --dataset-corpus-contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --output "$(COVERAGE_SAMPLING_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-coverage-sampling-report:
	@if [ -z "$(COVERAGE_SAMPLING_PROFILE)" ]; then echo "COVERAGE_SAMPLING_PROFILE is required: make tom-v1-build-coverage-sampling-report COVERAGE_SAMPLING_PROFILE=<profile.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-coverage-sampling-report --contract "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --profile "$(COVERAGE_SAMPLING_PROFILE)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --dataset-corpus-contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --output "$(COVERAGE_SAMPLING_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-many-point-ingestion-gate-contract:
	$(PYTHON) -m apps.worker.cli export-many-point-ingestion-gate-contract --output "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-many-point-ingestion-manifest-template:
	$(PYTHON) -m apps.worker.cli build-many-point-ingestion-manifest-template --local-media-path "$(MANY_POINT_INGESTION_MEDIA_PATH)" --source-label "$(MANY_POINT_INGESTION_SOURCE_LABEL)" --output "$(MANY_POINT_INGESTION_MANIFEST_OUTPUT)" --skip-create-db

tom-v1-validate-many-point-ingestion-manifest:
	@if [ -z "$(MANY_POINT_INGESTION_MANIFEST)" ]; then echo "MANY_POINT_INGESTION_MANIFEST is required: make tom-v1-validate-many-point-ingestion-manifest MANY_POINT_INGESTION_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-many-point-ingestion-manifest --contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --manifest "$(MANY_POINT_INGESTION_MANIFEST)" --output "$(MANY_POINT_INGESTION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-many-point-ingestion-plan:
	@if [ -z "$(MANY_POINT_INGESTION_MANIFEST)" ]; then echo "MANY_POINT_INGESTION_MANIFEST is required: make tom-v1-build-many-point-ingestion-plan MANY_POINT_INGESTION_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-many-point-ingestion-plan --contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --manifest "$(MANY_POINT_INGESTION_MANIFEST)" --mode "$(MANY_POINT_INGESTION_MODE)" --viewer-base-url "$(VIEWER_BASE_URL)" --output "$(MANY_POINT_INGESTION_PLAN_OUTPUT)" --skip-create-db

tom-v1-run-many-point-ingestion-gate:
	@if [ -z "$(MANY_POINT_INGESTION_MANIFEST)" ]; then echo "MANY_POINT_INGESTION_MANIFEST is required: make tom-v1-run-many-point-ingestion-gate MANY_POINT_INGESTION_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-many-point-ingestion-gate --contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --manifest "$(MANY_POINT_INGESTION_MANIFEST)" --mode "$(MANY_POINT_INGESTION_MODE)" --viewer-base-url "$(VIEWER_BASE_URL)" --storage-root "$(MANY_POINT_INGESTION_STORAGE_ROOT)" --manifest-output-dir "$(MANY_POINT_INGESTION_MANIFEST_OUTPUT_DIR)" --multi-point-index-output "$(MANY_POINT_INGESTION_MULTI_POINT_INDEX_OUTPUT)" --dataset-corpus-manifest-output "$(MANY_POINT_INGESTION_DATASET_CORPUS_MANIFEST_OUTPUT)" --multi-point-matrix "$(MANY_POINT_INGESTION_MULTI_POINT_MATRIX)" --output "$(MANY_POINT_INGESTION_GATE_OUTPUT)" $(if $(filter dry_run validate_only,$(MANY_POINT_INGESTION_MODE)),--skip-create-db,)

tom-v1-export-review-ops-metrics-contract:
	$(PYTHON) -m apps.worker.cli export-review-ops-metrics-contract --output "$(REVIEW_OPS_METRICS_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-review-ops-metrics-report:
	$(PYTHON) -m apps.worker.cli build-review-ops-metrics-report --contract "$(REVIEW_OPS_METRICS_CONTRACT_OUTPUT)" --corpus-manifest "$(REVIEW_OPS_SOURCE_CORPUS_MANIFEST)" --coverage-sampling-profile "$(REVIEW_OPS_SOURCE_COVERAGE_PROFILE)" --coverage-sampling-report "$(REVIEW_OPS_SOURCE_COVERAGE_REPORT)" --many-point-ingestion-gate "$(REVIEW_OPS_SOURCE_INGESTION_GATE)" --output "$(REVIEW_OPS_METRICS_REPORT_OUTPUT)" --skip-create-db

tom-v1-validate-review-ops-metrics-report:
	@if [ -z "$(REVIEW_OPS_METRICS_REPORT)" ]; then echo "REVIEW_OPS_METRICS_REPORT is required: make tom-v1-validate-review-ops-metrics-report REVIEW_OPS_METRICS_REPORT=<report.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-review-ops-metrics-report --contract "$(REVIEW_OPS_METRICS_CONTRACT_OUTPUT)" --report "$(REVIEW_OPS_METRICS_REPORT)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --dataset-corpus-contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --coverage-sampling-contract "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --many-point-ingestion-contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --output "$(REVIEW_OPS_METRICS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-review-ops-dashboard-data:
	@if [ -z "$(REVIEW_OPS_METRICS_REPORT)" ]; then echo "REVIEW_OPS_METRICS_REPORT is required: make tom-v1-build-review-ops-dashboard-data REVIEW_OPS_METRICS_REPORT=<report.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-review-ops-dashboard-data --report "$(REVIEW_OPS_METRICS_REPORT)" --output "$(REVIEW_OPS_DASHBOARD_DATA_OUTPUT)" --skip-create-db

tom-v1-export-label-feedback-evaluation-contract:
	$(PYTHON) -m apps.worker.cli export-label-feedback-evaluation-contract --output "$(LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-label-feedback-evaluation-inputs:
	$(PYTHON) -m apps.worker.cli build-label-feedback-evaluation-inputs --contract "$(LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT)" --corpus-manifest "$(LABEL_FEEDBACK_SOURCE_CORPUS_MANIFEST)" --review-ops-metrics-report "$(LABEL_FEEDBACK_SOURCE_REVIEW_OPS_REPORT)" --review-ops-dashboard-data "$(LABEL_FEEDBACK_SOURCE_REVIEW_OPS_DASHBOARD)" --coverage-sampling-profile "$(LABEL_FEEDBACK_SOURCE_COVERAGE_PROFILE)" --coverage-sampling-report "$(LABEL_FEEDBACK_SOURCE_COVERAGE_REPORT)" --multi-point-regression-matrix "$(LABEL_FEEDBACK_SOURCE_REGRESSION_MATRIX)" --output "$(LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT)" --skip-create-db

tom-v1-validate-label-feedback-evaluation-inputs:
	@if [ -z "$(LABEL_FEEDBACK_EVALUATION_INPUTS)" ]; then echo "LABEL_FEEDBACK_EVALUATION_INPUTS is required: make tom-v1-validate-label-feedback-evaluation-inputs LABEL_FEEDBACK_EVALUATION_INPUTS=<inputs.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-label-feedback-evaluation-inputs --contract "$(LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT)" --feedback-inputs "$(LABEL_FEEDBACK_EVALUATION_INPUTS)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --dataset-corpus-contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --coverage-sampling-contract "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --many-point-ingestion-contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --review-ops-metrics-contract "$(REVIEW_OPS_METRICS_CONTRACT_OUTPUT)" --output "$(LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-label-feedback-evaluation-report:
	@if [ -z "$(LABEL_FEEDBACK_EVALUATION_INPUTS)" ]; then echo "LABEL_FEEDBACK_EVALUATION_INPUTS is required: make tom-v1-build-label-feedback-evaluation-report LABEL_FEEDBACK_EVALUATION_INPUTS=<inputs.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-label-feedback-evaluation-report --contract "$(LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT)" --feedback-inputs "$(LABEL_FEEDBACK_EVALUATION_INPUTS)" --output "$(LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-camera-geometry-calibration-provenance-contract:
	$(PYTHON) -m apps.worker.cli export-camera-geometry-calibration-provenance-contract --output "$(CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-camera-geometry-calibration-profile:
	$(PYTHON) -m apps.worker.cli build-camera-geometry-calibration-profile --contract "$(CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT)" --replay-index "$(CAMERA_GEOMETRY_CALIBRATION_SOURCE_REPLAY_INDEX)" --regression-matrix "$(CAMERA_GEOMETRY_CALIBRATION_SOURCE_REGRESSION_MATRIX)" --corpus-manifest "$(CAMERA_GEOMETRY_CALIBRATION_SOURCE_CORPUS_MANIFEST)" --label-feedback-inputs "$(CAMERA_GEOMETRY_CALIBRATION_SOURCE_LABEL_FEEDBACK_INPUTS)" --output "$(CAMERA_GEOMETRY_CALIBRATION_PROFILE_OUTPUT)" --skip-create-db

tom-v1-validate-camera-geometry-calibration-profile:
	@if [ -z "$(CAMERA_GEOMETRY_CALIBRATION_PROFILE)" ]; then echo "CAMERA_GEOMETRY_CALIBRATION_PROFILE is required: make tom-v1-validate-camera-geometry-calibration-profile CAMERA_GEOMETRY_CALIBRATION_PROFILE=<profile.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-camera-geometry-calibration-profile --contract "$(CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT)" --profile "$(CAMERA_GEOMETRY_CALIBRATION_PROFILE)" --observation-quality-taxonomy "$(OBSERVATION_QUALITY_TAXONOMY_OUTPUT)" --review-label-schema "$(REVIEW_LABEL_SCHEMA_OUTPUT)" --reviewer-confidence-schema "$(REVIEWER_CONFIDENCE_SCHEMA_OUTPUT)" --multi-reviewer-schema "$(MULTI_REVIEWER_SCHEMA_OUTPUT)" --intennse-alignment-contract "$(INTENNSE_ALIGNMENT_CONTRACT_OUTPUT)" --dataset-corpus-contract "$(DATASET_CORPUS_CONTRACT_OUTPUT)" --coverage-sampling-contract "$(COVERAGE_SAMPLING_CONTRACT_OUTPUT)" --many-point-ingestion-contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --review-ops-metrics-contract "$(REVIEW_OPS_METRICS_CONTRACT_OUTPUT)" --label-feedback-contract "$(LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT)" --output "$(CAMERA_GEOMETRY_CALIBRATION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-camera-geometry-calibration-report:
	@if [ -z "$(CAMERA_GEOMETRY_CALIBRATION_PROFILE)" ]; then echo "CAMERA_GEOMETRY_CALIBRATION_PROFILE is required: make tom-v1-build-camera-geometry-calibration-report CAMERA_GEOMETRY_CALIBRATION_PROFILE=<profile.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-camera-geometry-calibration-report --contract "$(CAMERA_GEOMETRY_CALIBRATION_CONTRACT_OUTPUT)" --profile "$(CAMERA_GEOMETRY_CALIBRATION_PROFILE)" --output "$(CAMERA_GEOMETRY_CALIBRATION_REPORT_OUTPUT)" --skip-create-db

tom-v1-build-tom-v3-expansion-completion-freeze:
	$(PYTHON) -m apps.worker.cli build-tom-v3-expansion-completion-freeze --output "$(TOM_V3_EXPANSION_COMPLETION_FREEZE_OUTPUT)" --skip-create-db

tom-v1-validate-tom-v3-expansion-completion-freeze:
	@if [ -z "$(TOM_V3_EXPANSION_COMPLETION_FREEZE)" ]; then echo "TOM_V3_EXPANSION_COMPLETION_FREEZE is required: make tom-v1-validate-tom-v3-expansion-completion-freeze TOM_V3_EXPANSION_COMPLETION_FREEZE=<freeze.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-tom-v3-expansion-completion-freeze --freeze "$(TOM_V3_EXPANSION_COMPLETION_FREEZE)" --output "$(TOM_V3_EXPANSION_COMPLETION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-tom-v3-next-phase-readiness-report:
	@if [ -z "$(TOM_V3_EXPANSION_COMPLETION_FREEZE)" ]; then echo "TOM_V3_EXPANSION_COMPLETION_FREEZE is required: make tom-v1-build-tom-v3-next-phase-readiness-report TOM_V3_EXPANSION_COMPLETION_FREEZE=<freeze.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-tom-v3-next-phase-readiness-report --freeze "$(TOM_V3_EXPANSION_COMPLETION_FREEZE)" --output "$(TOM_V3_NEXT_PHASE_READINESS_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-segment-gate-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-segment-gate-contract --output "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-inspect-gameplay-classifier-asset:
	$(PYTHON) -m apps.worker.cli inspect-gameplay-classifier-asset --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(GAMEPLAY_CLASSIFIER_INSPECTION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-segment-candidates:
	@if [ -z "$(GAMEPLAY_SEGMENT_MEDIA_PATH)" ]; then echo "GAMEPLAY_SEGMENT_MEDIA_PATH is required: make tom-v1-build-gameplay-segment-candidates GAMEPLAY_SEGMENT_MEDIA_PATH=<media.mp4>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-segment-candidates --local-media-path "$(GAMEPLAY_SEGMENT_MEDIA_PATH)" $(if $(GAMEPLAY_SEGMENT_MEDIA_ID),--media-id "$(GAMEPLAY_SEGMENT_MEDIA_ID)",) --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(GAMEPLAY_SEGMENT_CANDIDATES_OUTPUT)" --threshold "$(GAMEPLAY_SEGMENT_THRESHOLD)" --smoothing-window "$(GAMEPLAY_SEGMENT_SMOOTHING_WINDOW)" --hysteresis-enter "$(GAMEPLAY_SEGMENT_HYSTERESIS_ENTER)" --hysteresis-exit "$(GAMEPLAY_SEGMENT_HYSTERESIS_EXIT)" --frame-sample-rate "$(GAMEPLAY_SEGMENT_FRAME_SAMPLE_RATE)" --max-frames "$(GAMEPLAY_SEGMENT_MAX_FRAMES)" --min-segment-duration-ms "$(GAMEPLAY_SEGMENT_MIN_DURATION_MS)" --inference-mode "$(GAMEPLAY_SEGMENT_INFERENCE_MODE)" --viewer-base-url "$(VIEWER_BASE_URL)" --skip-create-db

tom-v1-validate-gameplay-segment-candidates:
	@if [ -z "$(GAMEPLAY_SEGMENT_CANDIDATES)" ]; then echo "GAMEPLAY_SEGMENT_CANDIDATES is required: make tom-v1-validate-gameplay-segment-candidates GAMEPLAY_SEGMENT_CANDIDATES=<candidates.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-segment-candidates --contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --candidates "$(GAMEPLAY_SEGMENT_CANDIDATES)" --output "$(GAMEPLAY_SEGMENT_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-segment-report:
	@if [ -z "$(GAMEPLAY_SEGMENT_CANDIDATES)" ]; then echo "GAMEPLAY_SEGMENT_CANDIDATES is required: make tom-v1-build-gameplay-segment-report GAMEPLAY_SEGMENT_CANDIDATES=<candidates.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-segment-report --contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --candidates "$(GAMEPLAY_SEGMENT_CANDIDATES)" --output "$(GAMEPLAY_SEGMENT_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-gated-routing-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-gated-routing-contract --output "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gated-routing-plan:
	@if [ -z "$(GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS)" ]; then echo "GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS is required: make tom-v1-build-gameplay-gated-routing-plan GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS=<gameplay_segments.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-routing-plan --gameplay-segments "$(GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS)" --gameplay-segment-contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --output "$(GAMEPLAY_GATED_ROUTING_PLAN_OUTPUT)" --routing-mode "$(GAMEPLAY_GATED_ROUTING_MODE)" $(if $(GAMEPLAY_GATED_ROUTING_DOWNSTREAM_STAGES),--downstream-stages "$(GAMEPLAY_GATED_ROUTING_DOWNSTREAM_STAGES)",) --skip-create-db

tom-v1-validate-gameplay-gated-routing-plan:
	@if [ -z "$(GAMEPLAY_GATED_ROUTING_PLAN)" ]; then echo "GAMEPLAY_GATED_ROUTING_PLAN is required: make tom-v1-validate-gameplay-gated-routing-plan GAMEPLAY_GATED_ROUTING_PLAN=<routing_plan.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-gated-routing-plan --contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --plan "$(GAMEPLAY_GATED_ROUTING_PLAN)" --gameplay-segment-contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --output "$(GAMEPLAY_GATED_ROUTING_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gated-routing-report:
	@if [ -z "$(GAMEPLAY_GATED_ROUTING_PLAN)" ]; then echo "GAMEPLAY_GATED_ROUTING_PLAN is required: make tom-v1-build-gameplay-gated-routing-report GAMEPLAY_GATED_ROUTING_PLAN=<routing_plan.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-routing-report --contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --plan "$(GAMEPLAY_GATED_ROUTING_PLAN)" --gameplay-segment-contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --output "$(GAMEPLAY_GATED_ROUTING_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-gated-perception-execution-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-gated-perception-execution-contract --output "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gated-perception-execution-plan:
	@if [ -z "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN)" ]; then echo "GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN is required: make tom-v1-build-gameplay-gated-perception-execution-plan GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN=<routing_plan.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-perception-execution-plan --routing-plan "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN)" --routing-contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --output "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN_OUTPUT)" --execution-mode "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_MODE)" $(if $(GAMEPLAY_GATED_PERCEPTION_EXECUTION_STAGES),--perception-stages "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_STAGES)",) --skip-create-db

tom-v1-validate-gameplay-gated-perception-execution-plan:
	@if [ -z "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN)" ]; then echo "GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN is required: make tom-v1-validate-gameplay-gated-perception-execution-plan GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN=<execution_plan.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-gated-perception-execution-plan --contract "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT)" --plan "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN)" --routing-contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" $(if $(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN),--routing-plan "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN)",) --output "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gated-perception-execution-report:
	@if [ -z "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN)" ]; then echo "GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN is required: make tom-v1-build-gameplay-gated-perception-execution-report GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN=<execution_plan.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-perception-execution-report --contract "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT)" --plan "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN)" --routing-contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" $(if $(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN),--routing-plan "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN)",) --output "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-segment-replay-review-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-segment-replay-review-contract --output "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-segment-replay-timeline:
	@if [ -z "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS)" ]; then echo "GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS is required: make tom-v1-build-gameplay-segment-replay-timeline GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS=<gameplay_segments.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-segment-replay-timeline --gameplay-segments "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS)" $(if $(GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN),--routing-plan "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN)",) $(if $(GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN),--execution-plan "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN)",) --viewer-base-url "$(VIEWER_BASE_URL)" --output "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE_OUTPUT)" --skip-create-db

tom-v1-validate-gameplay-segment-replay-timeline:
	@if [ -z "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" ]; then echo "GAMEPLAY_SEGMENT_REPLAY_TIMELINE is required: make tom-v1-validate-gameplay-segment-replay-timeline GAMEPLAY_SEGMENT_REPLAY_TIMELINE=<timeline.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-segment-replay-timeline --contract "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --timeline "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" $(if $(GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS),--gameplay-segments "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS)",) $(if $(GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN),--routing-plan "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN)",) $(if $(GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN),--execution-plan "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN)",) --output "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-segment-review-template:
	@if [ -z "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" ]; then echo "GAMEPLAY_SEGMENT_REPLAY_TIMELINE is required: make tom-v1-build-gameplay-segment-review-template GAMEPLAY_SEGMENT_REPLAY_TIMELINE=<timeline.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-segment-review-template --timeline "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" $(if $(GAMEPLAY_SEGMENT_REVIEWER_ID),--reviewer-id "$(GAMEPLAY_SEGMENT_REVIEWER_ID)",) --output "$(GAMEPLAY_SEGMENT_REVIEW_TEMPLATE_OUTPUT)" --skip-create-db

tom-v1-validate-gameplay-segment-review-bundle:
	@if [ -z "$(GAMEPLAY_SEGMENT_REVIEW_BUNDLE)" ]; then echo "GAMEPLAY_SEGMENT_REVIEW_BUNDLE is required: make tom-v1-validate-gameplay-segment-review-bundle GAMEPLAY_SEGMENT_REVIEW_BUNDLE=<review_bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-segment-review-bundle --contract "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --bundle "$(GAMEPLAY_SEGMENT_REVIEW_BUNDLE)" $(if $(GAMEPLAY_SEGMENT_REPLAY_TIMELINE),--timeline "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)",) --output "$(GAMEPLAY_SEGMENT_REVIEW_BUNDLE_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-segment-review-report:
	@if [ -z "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" ]; then echo "GAMEPLAY_SEGMENT_REPLAY_TIMELINE is required: make tom-v1-build-gameplay-segment-review-report GAMEPLAY_SEGMENT_REPLAY_TIMELINE=<timeline.json>"; exit 1; fi
	@if [ -z "$(GAMEPLAY_SEGMENT_REVIEW_BUNDLE)" ]; then echo "GAMEPLAY_SEGMENT_REVIEW_BUNDLE is required: make tom-v1-build-gameplay-segment-review-report GAMEPLAY_SEGMENT_REVIEW_BUNDLE=<review_bundle.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-segment-review-report --contract "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --timeline "$(GAMEPLAY_SEGMENT_REPLAY_TIMELINE)" --bundle "$(GAMEPLAY_SEGMENT_REVIEW_BUNDLE)" --output "$(GAMEPLAY_SEGMENT_REVIEW_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-gated-many-point-smoke-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-gated-many-point-smoke-contract --output "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gated-many-point-smoke-manifest-template:
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-many-point-smoke-manifest-template --local-media-path "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MEDIA_PATH)" --source-label "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_SOURCE_LABEL)" $(if $(GAMEPLAY_GATED_MANY_POINT_SMOKE_REQUESTED_STEP),--requested-smoke-step "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_REQUESTED_STEP)",) --output "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST_OUTPUT)" --skip-create-db

tom-v1-validate-gameplay-gated-many-point-smoke-manifest:
	@if [ -z "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST)" ]; then echo "GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST is required: make tom-v1-validate-gameplay-gated-many-point-smoke-manifest GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-gameplay-gated-many-point-smoke-manifest --contract "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT)" --manifest "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST)" --output "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-run-gameplay-gated-many-point-smoke:
	@if [ -z "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST)" ]; then echo "GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST is required: make tom-v1-run-gameplay-gated-many-point-smoke GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-gameplay-gated-many-point-smoke --contract "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT)" --manifest "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST)" --smoke-mode "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_MODE)" --output-dir "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT_DIR)" --output "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_OUTPUT)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --many-point-contract "$(MANY_POINT_INGESTION_CONTRACT_OUTPUT)" --gameplay-segment-contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --routing-contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --execution-contract "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT)" --replay-review-contract "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --viewer-base-url "$(VIEWER_BASE_URL)" --skip-create-db

tom-v1-build-gameplay-gated-many-point-smoke-report:
	@if [ -z "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT)" ]; then echo "GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT is required: make tom-v1-build-gameplay-gated-many-point-smoke-report GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT=<smoke_report.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-gameplay-gated-many-point-smoke-report --contract "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_CONTRACT_OUTPUT)" --smoke-report "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT)" --output "$(GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-gate-regression-baseline-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-gate-regression-baseline-contract --output "$(GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-regression-baseline:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-regression-baseline --contract "$(GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT)" $(if $(GAMEPLAY_GATE_REGRESSION_SMOKE_MANIFEST),--smoke-manifest "$(GAMEPLAY_GATE_REGRESSION_SMOKE_MANIFEST)",) --work-dir "$(GAMEPLAY_GATE_REGRESSION_WORK_DIR)" --fixture-media-path "$(GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT)" --skip-create-db

tom-v1-verify-gameplay-gate-regression-baseline:
	$(PYTHON) -m apps.worker.cli verify-gameplay-gate-regression-baseline --contract "$(GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT)" --baseline "$(GAMEPLAY_GATE_REGRESSION_BASELINE)" $(if $(GAMEPLAY_GATE_REGRESSION_SMOKE_MANIFEST),--smoke-manifest "$(GAMEPLAY_GATE_REGRESSION_SMOKE_MANIFEST)",) --work-dir "$(GAMEPLAY_GATE_REGRESSION_WORK_DIR)" --fixture-media-path "$(GAMEPLAY_GATE_REGRESSION_FIXTURE_MEDIA_PATH)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-regression-report:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-regression-report --contract "$(GAMEPLAY_GATE_REGRESSION_CONTRACT_OUTPUT)" --baseline "$(GAMEPLAY_GATE_REGRESSION_BASELINE)" --verification "$(GAMEPLAY_GATE_REGRESSION_VERIFICATION_OUTPUT)" --output "$(GAMEPLAY_GATE_REGRESSION_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-gameplay-gate-review-dataset-contract:
	$(PYTHON) -m apps.worker.cli export-gameplay-gate-review-dataset-contract --output "$(GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-review-dataset:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-review-dataset --contract "$(GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT)" $(if $(GAMEPLAY_GATE_REVIEW_DATASET_GAMEPLAY_SEGMENTS),--gameplay-segments "$(GAMEPLAY_GATE_REVIEW_DATASET_GAMEPLAY_SEGMENTS)",) $(if $(GAMEPLAY_GATE_REVIEW_DATASET_ROUTING_PLAN),--routing-plan "$(GAMEPLAY_GATE_REVIEW_DATASET_ROUTING_PLAN)",) $(if $(GAMEPLAY_GATE_REVIEW_DATASET_EXECUTION_PLAN),--execution-plan "$(GAMEPLAY_GATE_REVIEW_DATASET_EXECUTION_PLAN)",) $(if $(GAMEPLAY_GATE_REVIEW_DATASET_REPLAY_TIMELINE),--replay-timeline "$(GAMEPLAY_GATE_REVIEW_DATASET_REPLAY_TIMELINE)",) --regression-baseline "$(GAMEPLAY_GATE_REVIEW_DATASET_REGRESSION_BASELINE)" --regression-verification "$(GAMEPLAY_GATE_REVIEW_DATASET_REGRESSION_VERIFICATION)" --work-dir "$(GAMEPLAY_GATE_REVIEW_DATASET_WORK_DIR)" --fixture-media-path "$(GAMEPLAY_GATE_REVIEW_DATASET_FIXTURE_MEDIA_PATH)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --viewer-base-url "$(VIEWER_BASE_URL)" --output "$(GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT)" --skip-create-db

tom-v1-validate-gameplay-gate-review-dataset:
	$(PYTHON) -m apps.worker.cli validate-gameplay-gate-review-dataset --contract "$(GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT)" --dataset "$(GAMEPLAY_GATE_REVIEW_DATASET)" --output "$(GAMEPLAY_GATE_REVIEW_DATASET_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-review-dataset-report:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-review-dataset-report --contract "$(GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT)" --dataset "$(GAMEPLAY_GATE_REVIEW_DATASET)" --output "$(GAMEPLAY_GATE_REVIEW_DATASET_REPORT_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-pathway-completion-freeze:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-pathway-completion-freeze --output "$(GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_OUTPUT)" --skip-create-db

tom-v1-validate-gameplay-gate-pathway-completion-freeze:
	$(PYTHON) -m apps.worker.cli validate-gameplay-gate-pathway-completion-freeze --freeze "$(GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE)" --output "$(GAMEPLAY_GATE_PATHWAY_COMPLETION_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-gameplay-gate-next-phase-readiness-report:
	$(PYTHON) -m apps.worker.cli build-gameplay-gate-next-phase-readiness-report --freeze "$(GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE)" --output "$(GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-real-broadcast-gameplay-corpus-run-contract:
	$(PYTHON) -m apps.worker.cli export-real-broadcast-gameplay-corpus-run-contract --output "$(REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-corpus-manifest-template:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-corpus-manifest-template $(if $(REAL_BROADCAST_GAMEPLAY_CORPUS_MEDIA_PATH),--local-media-path "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MEDIA_PATH)",) --source-label "$(REAL_BROADCAST_GAMEPLAY_CORPUS_SOURCE_LABEL)" --expected-broadcast-content-tag "$(REAL_BROADCAST_GAMEPLAY_CORPUS_CONTENT_TAG)" $(if $(REAL_BROADCAST_GAMEPLAY_CORPUS_REQUESTED_STEP),--requested-step "$(REAL_BROADCAST_GAMEPLAY_CORPUS_REQUESTED_STEP)",) $(if $(filter true,$(REAL_BROADCAST_GAMEPLAY_CORPUS_ALLOW_FIXTURE_MODE)),--allow-fixture-mode,) --output "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_OUTPUT)" --skip-create-db

tom-v1-validate-real-broadcast-gameplay-corpus-manifest:
	@if [ -z "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST)" ]; then echo "REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST is required: make tom-v1-validate-real-broadcast-gameplay-corpus-manifest REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli validate-real-broadcast-gameplay-corpus-manifest --contract "$(REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT)" --manifest "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST)" --run-mode "$(REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE)" --output "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-run-real-broadcast-gameplay-corpus:
	@if [ -z "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST)" ]; then echo "REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST is required: make tom-v1-run-real-broadcast-gameplay-corpus REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST=<manifest.json>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-broadcast-gameplay-corpus --contract "$(REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT)" --manifest "$(REAL_BROADCAST_GAMEPLAY_CORPUS_MANIFEST)" --run-mode "$(REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE)" --output-dir "$(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT_DIR)" --output "$(REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --gameplay-segment-contract "$(GAMEPLAY_SEGMENT_GATE_CONTRACT_OUTPUT)" --routing-contract "$(GAMEPLAY_GATED_ROUTING_CONTRACT_OUTPUT)" --execution-contract "$(GAMEPLAY_GATED_PERCEPTION_EXECUTION_CONTRACT_OUTPUT)" --replay-review-contract "$(GAMEPLAY_SEGMENT_REPLAY_REVIEW_CONTRACT_OUTPUT)" --review-dataset-contract "$(GAMEPLAY_GATE_REVIEW_DATASET_CONTRACT_OUTPUT)" --viewer-base-url "$(VIEWER_BASE_URL)" --frame-sample-rate "$(GAMEPLAY_SEGMENT_FRAME_SAMPLE_RATE)" --max-frames "$(GAMEPLAY_SEGMENT_MAX_FRAMES)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-corpus-report:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-corpus-report --contract "$(REAL_BROADCAST_GAMEPLAY_CORPUS_CONTRACT_OUTPUT)" --corpus-run "$(REAL_BROADCAST_GAMEPLAY_CORPUS_RUN)" --output "$(REAL_BROADCAST_GAMEPLAY_CORPUS_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-real-broadcast-gameplay-review-loop-contract:
	$(PYTHON) -m apps.worker.cli export-real-broadcast-gameplay-review-loop-contract --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-review-bundle-template:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-review-bundle-template --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT)" --source-corpus-run "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_CORPUS_RUN)" $(if $(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REVIEW_DATASET),--source-review-dataset "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REVIEW_DATASET)",) $(if $(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REPLAY_TIMELINE),--source-replay-timeline "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REPLAY_TIMELINE)",) $(if $(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_ROUTING_PLAN),--source-routing-plan "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_ROUTING_PLAN)",) $(if $(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_EXECUTION_PLAN),--source-execution-plan "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_EXECUTION_PLAN)",) --source-regression-baseline "$(REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_REGRESSION_BASELINE)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_OUTPUT)" --skip-create-db

tom-v1-validate-real-broadcast-gameplay-review-bundle:
	$(PYTHON) -m apps.worker.cli validate-real-broadcast-gameplay-review-bundle --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT)" --bundle "$(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-review-loop-report:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-review-loop-report --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT)" --bundle "$(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-human-review-readiness-report:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-human-review-readiness-report --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_OUTPUT)" --bundle "$(REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE)" --output "$(REAL_BROADCAST_GAMEPLAY_HUMAN_REVIEW_READINESS_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-real-broadcast-gameplay-review-metrics-contract:
	$(PYTHON) -m apps.worker.cli export-real-broadcast-gameplay-review-metrics-contract --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-review-metrics-report:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-review-metrics-report --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT)" --source-review-loop-report "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_LOOP_REPORT)" --source-review-bundle "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_BUNDLE)" --source-corpus-run "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_CORPUS_RUN)" $(if $(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_DATASET),--source-review-dataset "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REVIEW_DATASET)",) --source-regression-baseline "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_SOURCE_REGRESSION_BASELINE)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT)" --skip-create-db

tom-v1-validate-real-broadcast-gameplay-review-metrics-report:
	$(PYTHON) -m apps.worker.cli validate-real-broadcast-gameplay-review-metrics-report --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT)" --metrics-report "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-review-qa-dashboard:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-review-qa-dashboard --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT)" --metrics-report "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_OUTPUT)" --skip-create-db

tom-v1-build-real-broadcast-gameplay-review-next-actions-report:
	$(PYTHON) -m apps.worker.cli build-real-broadcast-gameplay-review-next-actions-report --contract "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT)" --metrics-report "$(REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT)" --output "$(REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_OUTPUT)" --skip-create-db

tom-v1-export-review-guided-gameplay-calibration-proposal-contract:
	$(PYTHON) -m apps.worker.cli export-review-guided-gameplay-calibration-proposal-contract --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-inputs:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-inputs --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --source-metrics-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_METRICS_REPORT)" --source-review-loop-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_LOOP_REPORT)" --source-review-bundle "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_BUNDLE)" --source-review-dataset "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REVIEW_DATASET)" --source-corpus-run "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_CORPUS_RUN)" --source-regression-baseline "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SOURCE_REGRESSION_BASELINE)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --current-threshold "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_CURRENT_THRESHOLD)" --current-smoothing-window "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_CURRENT_SMOOTHING_WINDOW)" --hysteresis-enter "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_HYSTERESIS_ENTER)" --hysteresis-exit "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_HYSTERESIS_EXIT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT)" --skip-create-db

tom-v1-validate-review-guided-gameplay-calibration-inputs:
	$(PYTHON) -m apps.worker.cli validate-review-guided-gameplay-calibration-inputs --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --calibration-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-proposal:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-proposal --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --calibration-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT)" --skip-create-db

tom-v1-validate-review-guided-gameplay-calibration-proposal:
	$(PYTHON) -m apps.worker.cli validate-review-guided-gameplay-calibration-proposal --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --calibration-proposal "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-proposal-report:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-proposal-report --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT)" --calibration-proposal "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-review-guided-gameplay-calibration-evaluation-sandbox-contract:
	$(PYTHON) -m apps.worker.cli export-review-guided-gameplay-calibration-evaluation-sandbox-contract --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-evaluation-inputs:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-evaluation-inputs --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --source-calibration-proposal "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_CALIBRATION_PROPOSAL)" --source-metrics-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_METRICS_REPORT)" --source-review-loop-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REVIEW_LOOP_REPORT)" --source-review-bundle "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REVIEW_BUNDLE)" --source-corpus-run "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_CORPUS_RUN)" --source-regression-baseline "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SOURCE_REGRESSION_BASELINE)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --current-threshold "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_CURRENT_THRESHOLD)" --current-smoothing-window "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_CURRENT_SMOOTHING_WINDOW)" --hysteresis-enter "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_HYSTERESIS_ENTER)" --hysteresis-exit "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_HYSTERESIS_EXIT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT)" --skip-create-db

tom-v1-validate-review-guided-gameplay-calibration-evaluation-inputs:
	$(PYTHON) -m apps.worker.cli validate-review-guided-gameplay-calibration-evaluation-inputs --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --evaluation-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-run-review-guided-gameplay-calibration-evaluation-sandbox:
	$(PYTHON) -m apps.worker.cli run-review-guided-gameplay-calibration-evaluation-sandbox --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --evaluation-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS)" --evaluation-mode "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_MODE)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT)" --skip-create-db

tom-v1-validate-review-guided-gameplay-calibration-evaluation-report:
	$(PYTHON) -m apps.worker.cli validate-review-guided-gameplay-calibration-evaluation-report --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --evaluation-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-evaluation-summary:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-evaluation-summary --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT)" --evaluation-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_OUTPUT)" --skip-create-db

tom-v1-export-review-guided-gameplay-calibration-sandbox-regression-contract:
	$(PYTHON) -m apps.worker.cli export-review-guided-gameplay-calibration-sandbox-regression-contract --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-baseline:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-sandbox-regression-baseline --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT)" --source-evaluation-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_INPUTS)" --source-evaluation-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_REPORT)" --source-evaluation-contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_CONTRACT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT)" --skip-create-db

tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline:
	$(PYTHON) -m apps.worker.cli verify-review-guided-gameplay-calibration-sandbox-regression-baseline --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT)" --baseline "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE)" --source-evaluation-inputs "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_INPUTS)" --source-evaluation-report "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_REPORT)" --source-evaluation-contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_SOURCE_EVALUATION_CONTRACT)" --current-output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_OUTPUT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT)" --skip-create-db

tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-report:
	$(PYTHON) -m apps.worker.cli build-review-guided-gameplay-calibration-sandbox-regression-report --contract "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT)" --baseline "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE)" --verification "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT)" --output "$(REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_OUTPUT)" --skip-create-db

tom-v1-export-calibration-candidate-decision-packet-contract:
	$(PYTHON) -m apps.worker.cli export-calibration-candidate-decision-packet-contract --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --skip-create-db

tom-v1-build-calibration-candidate-decision-packet-inputs:
	$(PYTHON) -m apps.worker.cli build-calibration-candidate-decision-packet-inputs --contract "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --source-calibration-proposal "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CALIBRATION_PROPOSAL)" --source-sandbox-evaluation-report "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_SANDBOX_EVALUATION_REPORT)" --source-sandbox-regression-verification "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_SANDBOX_REGRESSION_VERIFICATION)" --source-review-metrics-report "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_REVIEW_METRICS_REPORT)" --source-review-loop-report "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_REVIEW_LOOP_REPORT)" --source-corpus-run "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CORPUS_RUN)" --source-gameplay-gate-regression-baseline "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_GAMEPLAY_GATE_REGRESSION_BASELINE)" --source-calibration-sandbox-baseline "$(CALIBRATION_CANDIDATE_DECISION_PACKET_SOURCE_CALIBRATION_SANDBOX_BASELINE)" --model-asset-path "$(GAMEPLAY_CLASSIFIER_ASSET_PATH)" --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT)" --skip-create-db

tom-v1-validate-calibration-candidate-decision-packet-inputs:
	$(PYTHON) -m apps.worker.cli validate-calibration-candidate-decision-packet-inputs --contract "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --packet-inputs "$(CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS)" --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-calibration-candidate-decision-packet:
	$(PYTHON) -m apps.worker.cli build-calibration-candidate-decision-packet --contract "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --packet-inputs "$(CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS)" --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT)" --skip-create-db

tom-v1-validate-calibration-candidate-decision-packet:
	$(PYTHON) -m apps.worker.cli validate-calibration-candidate-decision-packet --contract "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --decision-packet "$(CALIBRATION_CANDIDATE_DECISION_PACKET)" --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_VALIDATION_OUTPUT)" --skip-create-db

tom-v1-build-calibration-candidate-decision-packet-report:
	$(PYTHON) -m apps.worker.cli build-calibration-candidate-decision-packet-report --contract "$(CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)" --decision-packet "$(CALIBRATION_CANDIDATE_DECISION_PACKET)" --output "$(CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_OUTPUT)" --skip-create-db

tom-v1-post-codex-validate:
	scripts/post_codex_validate.sh $(if $(EXPECTED_BRANCH),--branch "$(EXPECTED_BRANCH)",) $(if $(EXPECTED_TAG),--expected-tag "$(EXPECTED_TAG)",) --python "$(PYTHON)"

tom-v1-evaluate-point-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-evaluate-point-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(EVENT_CANDIDATE_RUN_ID)" ]; then echo "EVENT_CANDIDATE_RUN_ID is required: make tom-v1-evaluate-point-candidates EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli evaluate-point-candidates --media-id "$(MEDIA_ID)" --event-candidate-run-id "$(EVENT_CANDIDATE_RUN_ID)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",)

tom-v1-declare-camera-geometry:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-declare-camera-geometry MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(COURT_PROJECTION_RUN_ID)" ]; then echo "COURT_PROJECTION_RUN_ID is required: make tom-v1-declare-camera-geometry COURT_PROJECTION_RUN_ID=<court_projection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli declare-camera-geometry --media-id "$(MEDIA_ID)" $(if $(COURT_RUN_ID),--court-run-id "$(COURT_RUN_ID)",) --court-projection-run-id "$(COURT_PROJECTION_RUN_ID)" $(if $(HOMOGRAPHY_RUN_ID),--homography-run-id "$(HOMOGRAPHY_RUN_ID)",) --court-model "$(COURT_MODEL)" --camera-model "$(CAMERA_MODEL)" --geometry-status "$(GEOMETRY_STATUS)" --viewer-base-url "$(VIEWER_BASE_URL)" --format "$(FORMAT)" $(if $(OUTPUT),--output "$(OUTPUT)",)

tom-v1-court-keypoints-probe:
	$(PYTHON) -m apps.worker.cli tom-v1-court-keypoints-probe --weights "$(TOM_V1_MODEL_ROOT)/keypoints_model.pth" --allowed-root "$(TOM_V1_MODEL_ROOT)"

tom-v1-court-keypoints:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-court-keypoints MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-court-keypoints --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/keypoints_model.pth" --model-name tom-v1-court-keypoints --model-version v1-local --device "$(YOLO_DEVICE)" --img-size "$(if $(IMG_SIZE),$(IMG_SIZE),$(TOM_V1_COURT_KEYPOINT_IMG_SIZE))" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" --preprocessing-mode "$(COURT_KEYPOINT_PREPROCESSING_MODE)" --coordinate-interpretation "$(COURT_KEYPOINT_COORDINATE_INTERPRETATION)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter false,$(DERIVE_LINES)),--no-derive-lines,--derive-lines) $(if $(filter true,$(EMIT_DEBUG_ARTIFACTS)),--emit-debug-artifacts,) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-court-keypoint-audit:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-court-keypoint-audit MEDIA_ID=<media_id>"; exit 1; fi
	$(MAKE) tom-v1-court-keypoints MEDIA_ID="$(MEDIA_ID)" PYTHON="$(PYTHON)" YOLO_DEVICE="$(YOLO_DEVICE)" IMG_SIZE="$(if $(IMG_SIZE),$(IMG_SIZE),224)" EVERY_N_FRAMES="$(EVERY_N_FRAMES)" MAX_FRAMES="$(MAX_FRAMES)" VIEWER_BASE_URL="$(VIEWER_BASE_URL)" COURT_KEYPOINT_PREPROCESSING_MODE="$(COURT_KEYPOINT_PREPROCESSING_MODE)" COURT_KEYPOINT_COORDINATE_INTERPRETATION="$(COURT_KEYPOINT_COORDINATE_INTERPRETATION)" EMIT_DEBUG_ARTIFACTS=true DERIVE_LINES="$(DERIVE_LINES)" PLAN_ONLY="$(PLAN_ONLY)"

court-fixture:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make court-fixture MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-fixture-court --media-id "$(MEDIA_ID)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --run-name "$(COURT_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

homography-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make homography-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(COURT_RUN_ID)" ]; then echo "COURT_RUN_ID is required: make homography-candidates COURT_RUN_ID=<court_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-homography-candidates --media-id "$(MEDIA_ID)" --court-run-id "$(COURT_RUN_ID)" --run-name "$(HOMOGRAPHY_RUN_NAME)" --min-keypoint-confidence "$(MIN_KEYPOINT_CONFIDENCE)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

projection-diagnostics:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make projection-diagnostics MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(HOMOGRAPHY_RUN_ID)" ]; then echo "HOMOGRAPHY_RUN_ID is required: make projection-diagnostics HOMOGRAPHY_RUN_ID=<homography_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-projection-diagnostics --media-id "$(MEDIA_ID)" --homography-run-id "$(HOMOGRAPHY_RUN_ID)" --run-name "$(PROJECTION_DIAGNOSTIC_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

court-review-export:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make court-review-export MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli export-court-review-dataset --media-id "$(MEDIA_ID)" $(if $(COURT_RUN_ID),--court-run-id "$(COURT_RUN_ID)",) $(if $(HOMOGRAPHY_RUN_ID),--homography-run-id "$(HOMOGRAPHY_RUN_ID)",) $(if $(PROJECTION_DIAGNOSTIC_RUN_ID),--projection-diagnostic-run-id "$(PROJECTION_DIAGNOSTIC_RUN_ID)",) --output-root "$(EXPORT_ROOT)"

web:
	cd $(WEB_DIR) && npm run dev

web-build:
	cd $(WEB_DIR) && npm run build

web-lint:
	cd $(WEB_DIR) && npm run lint

smoke:
	$(PYTHON) scripts/smoke_synthetic_viewer_data.py

all-checks:
	$(PYTHON) -m pytest -q
	ruff check .
	cd $(WEB_DIR) && npm run lint
	cd $(WEB_DIR) && npm run build
