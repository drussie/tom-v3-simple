export type JsonRecord = Record<string, unknown>;

export interface MediaAsset {
  id: string;
  source_uri: string;
  media_type: string;
  duration_ms: number | null;
  frame_count: number | null;
  fps: number | null;
  width: number | null;
  height: number | null;
  checksum: string | null;
  metadata_jsonb: JsonRecord;
  created_at: string | null;
}

export interface ProcessingRun {
  id: string;
  media_id: string;
  run_name: string;
  run_status: string;
  started_at: string | null;
  completed_at: string | null;
  runtime_config_id: string | null;
  metadata_jsonb: JsonRecord;
}

export interface ProcessingStep {
  id: string;
  run_id: string;
  step_name: string;
  step_status: string;
  started_at: string | null;
  completed_at: string | null;
  runtime_config_id: string | null;
  metadata_jsonb: JsonRecord;
}

export interface GameplayDetail {
  observation_id: string;
  view_state: string;
  view_state_subtype: string | null;
  payload_jsonb: JsonRecord;
}

export interface AtomicDetail {
  observation_id: string;
  atomic_kind: string;
  payload_jsonb: JsonRecord;
}

export interface DerivedDetail {
  observation_id: string;
  derived_kind: string;
  derivation_payload_jsonb: JsonRecord;
}

export interface PoseKeypoint {
  index: number;
  name: string;
  x: number | null;
  y: number | null;
  x_norm: number | null;
  y_norm: number | null;
  confidence: number | null;
  present: boolean;
  visibility: string | null;
}

export interface PoseDetail {
  observation_id: string;
  media_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  skeleton_format: string;
  skeleton_version: string;
  keypoint_schema_jsonb: JsonRecord;
  keypoints_jsonb: PoseKeypoint[];
  keypoint_count: number;
  keypoints_present_count: number;
  keypoints_missing_count: number;
  mean_keypoint_confidence: number | null;
  min_keypoint_confidence: number | null;
  max_keypoint_confidence: number | null;
  pose_confidence: number | null;
  bbox_x: number | null;
  bbox_y: number | null;
  bbox_w: number | null;
  bbox_h: number | null;
  bbox_confidence: number | null;
  crop_x: number | null;
  crop_y: number | null;
  crop_w: number | null;
  crop_h: number | null;
  crop_source: string | null;
  subject_ref_type: string;
  subject_detection_observation_id: string | null;
  subject_tracklet_id: string | null;
  subject_track_point_id: string | null;
  association_status: string;
  association_method: string | null;
  association_confidence: number | null;
  frame_time_owner: string;
  raw_model_payload_jsonb: JsonRecord;
  metadata_jsonb: JsonRecord;
  created_at: string | null;
}

export interface Observation {
  id: string;
  media_id: string;
  run_id: string;
  observation_family: string;
  observation_type: string;
  granularity: string;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number | null;
  timestamp_end_ms: number | null;
  confidence: number | null;
  model_id: string | null;
  runtime_config_id: string | null;
  coordinate_space: string | null;
  schema_version: number;
  payload_jsonb: JsonRecord;
  idempotency_key: string | null;
  created_at: string | null;
  gameplay: GameplayDetail | null;
  atomic: AtomicDetail | null;
  derived: DerivedDetail | null;
  pose: PoseDetail | null;
}

export interface TrackPoint {
  id: string;
  tracklet_id: string;
  observation_id: string | null;
  frame_number: number;
  timestamp_ms: number | null;
  x: number;
  y: number;
  width: number | null;
  height: number | null;
  confidence: number | null;
  payload_jsonb: JsonRecord;
}

export interface CoverageSegment {
  state: string;
  frame_start: number;
  frame_end: number;
}

export interface Tracklet {
  id: string;
  media_id: string;
  run_id: string;
  track_family: string;
  subject_ref: string | null;
  frame_start: number | null;
  frame_end: number | null;
  confidence: number | null;
  observation_id: string | null;
  metadata_jsonb: JsonRecord & {
    viewer_row?: string;
    coverage_segments?: CoverageSegment[];
  };
  points: TrackPoint[];
}

export interface LineageRow {
  id: string;
  child_observation_id: string;
  parent_observation_id: string;
  relationship_type: string;
  processing_step_id: string | null;
  payload_jsonb: JsonRecord;
  created_at: string | null;
}

export interface EvidenceArtifact {
  id: string;
  media_id: string;
  run_id: string | null;
  target_observation_id: string | null;
  artifact_type: string;
  uri: string;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number | null;
  timestamp_end_ms: number | null;
  checksum: string | null;
  metadata_jsonb: JsonRecord;
  created_at: string | null;
}

export interface HumanAnnotation {
  id: string;
  media_id: string;
  observation_id: string | null;
  evidence_artifact_id: string | null;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number | null;
  timestamp_end_ms: number | null;
  annotation_type: string;
  payload_jsonb: JsonRecord;
  created_by: string | null;
  created_at: string | null;
}

export interface AnnotationSummary {
  count: number;
  labels: Record<string, number>;
  latest_created_at: string | null;
}

export interface ViewerRun {
  run: ProcessingRun;
  media: MediaAsset | null;
  steps: ProcessingStep[];
  observations: Observation[];
  tracklets: Tracklet[];
  lineage: LineageRow[];
  artifacts: EvidenceArtifact[];
  annotations: HumanAnnotation[];
}

export interface ReplayRunSummary {
  run_id: string;
  run_name: string;
  run_status: string;
  created_at: string | null;
  completed_at: string | null;
  observation_count: number;
  evidence_source?: "real_model_output" | "fixture_demo" | "persisted_evidence" | string;
  source_label?: string | null;
  adapter_name?: string | null;
  source_runtime?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  model_registry_id?: string | null;
  runtime_config_id?: string | null;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
  is_real_detection_derived?: boolean;
  source_detection_run_id?: string | null;
  source_tracklet_run_id?: string | null;
  source_main_player_track_run_id?: string | null;
  source_pose_run_id?: string | null;
  source_detection_evidence_source?: string | null;
  source_detection_source_label?: string | null;
  source_detection_runtime?: string | null;
  source_subject_run_id?: string | null;
  source_court_run_id?: string | null;
  source_homography_run_id?: string | null;
  track_candidate_count?: number;
  track_assignment_count?: number;
  court_keypoint_count?: number;
  court_line_count?: number;
  camera_view_count?: number;
  candidate_count?: number;
  projection_diagnostic_count?: number;
  candidate_geometry?: boolean;
  diagnostic_geometry?: boolean;
  geometry_evidence_only?: boolean;
  not_ball_player_projection?: boolean;
  candidate_track_only?: boolean;
  candidate_subject_only?: boolean;
  not_identity_truth?: boolean;
  model_output_not_truth?: boolean;
  smoothed_ball_count?: number;
  smoothed_player_box_count?: number;
  smoothed_pose_count?: number;
  smoothed_candidate_only?: boolean;
  not_truth?: boolean;
}

export interface ReplayAvailableRuns {
  detection: ReplayRunSummary[];
  tracklet: ReplayRunSummary[];
  pose: ReplayRunSummary[];
  gameplay: ReplayRunSummary[];
  court: ReplayRunSummary[];
  homography: ReplayRunSummary[];
  projection_diagnostic: ReplayRunSummary[];
  main_player_track: ReplayRunSummary[];
  motion_smoothing: ReplayRunSummary[];
}

export interface ReplayInfo {
  media_id: string;
  video_url: string;
  source_uri: string;
  width: number | null;
  height: number | null;
  duration_ms: number | null;
  fps: number | null;
  frame_count: number | null;
  frame_time_mode: string;
  frame_time_index: JsonRecord | null;
  available_runs: ReplayAvailableRuns;
  observation_only: boolean;
  no_adjudication: boolean;
}

export interface ReplayDetectionBBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

export type ReplayOverlayDisplayMode = "current_only" | "short_trail" | "full_trail";
export type ReplayCourtTemporalPersistence = "off" | "carry_forward";

export interface ReplayDetectionOverlay {
  overlay_type: "detection_bbox";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  observation_type: "ball_detection" | "player_detection";
  label: string;
  confidence: number | null;
  bbox: ReplayDetectionBBox;
  source_language: "detection observation";
  source_runtime: string | null;
  coordinate_space: "image_pixels";
  class_id?: number | null;
  class_label?: string | null;
  frame_time_owner?: string | null;
  evidence_source?: "real_model_output" | "fixture_demo" | "persisted_evidence" | string;
  source_label?: string | null;
  real_model_output?: boolean;
  model_output_not_truth?: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
}

export interface ReplayTrackPointOverlay {
  track_point_id: string;
  observation_id: string | null;
  source_detection_observation_id: string | null;
  source_detection_run_id?: string | null;
  source_detection_evidence_source?: string | null;
  source_detection_source_label?: string | null;
  source_detection_runtime?: string | null;
  source_detection_real_model_output?: boolean;
  frame_number: number;
  timestamp_ms: number;
  x: number;
  y: number;
  bbox: ReplayDetectionBBox | null;
  confidence: number | null;
}

export interface ReplayTrackletOverlay {
  overlay_type: "tracklet_candidate";
  observation_id: string | null;
  tracklet_id: string;
  run_id: string;
  track_type: "ball" | "player" | string;
  label_hint: string | null;
  track_status: "candidate" | string;
  identity_status: "unverified" | string;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number;
  timestamp_end_ms: number;
  points: ReplayTrackPointOverlay[];
  source_language: "tracklet candidate";
  source_detection_run_id?: string | null;
  source_detection_evidence_source?: string | null;
  source_detection_source_label?: string | null;
  source_detection_runtime?: string | null;
  source_detection_real_model_output?: boolean;
  is_real_detection_derived?: boolean;
  candidate_evidence_only?: boolean;
}

export interface ReplayPoseKeypoint {
  index: number;
  name: string;
  x: number | null;
  y: number | null;
  confidence: number | null;
  present: boolean;
}

export interface ReplayPoseSubjectContext {
  subject_ref_type: string;
  subject_detection_observation_id: string | null;
  subject_tracklet_id: string | null;
  subject_track_point_id: string | null;
  association_status: string;
  association_method: string | null;
  association_confidence: number | null;
  source_subject_run_id?: string | null;
  subject_candidate_observation_id?: string | null;
  subject_role_candidate?: string | null;
  source_track_run_id?: string | null;
  track_assignment_observation_id?: string | null;
  track_candidate_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  assignment_method?: string | null;
  assignment_score?: number | null;
  candidate_subject_only?: boolean;
  candidate_track_only?: boolean;
  not_identity_truth?: boolean;
}

export interface ReplayPoseOverlay {
  overlay_type: "pose_skeleton";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  skeleton_format: string;
  skeleton_version: string;
  pose_confidence: number | null;
  bbox: (ReplayDetectionBBox & { confidence: number | null }) | null;
  keypoint_count: number;
  keypoints_present_count: number;
  keypoints_missing_count: number;
  mean_keypoint_confidence: number | null;
  min_keypoint_confidence: number | null;
  max_keypoint_confidence: number | null;
  keypoints: ReplayPoseKeypoint[];
  edges: [string, string][];
  subject_context: ReplayPoseSubjectContext;
  source_track_run_id?: string | null;
  track_assignment_observation_id?: string | null;
  track_candidate_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  candidate_track_only?: boolean;
  source_subject_run_id?: string | null;
  subject_candidate_observation_id?: string | null;
  subject_role_candidate?: string | null;
  candidate_subject_only?: boolean;
  not_identity_truth?: boolean;
  source_language: "pose keypoint evidence";
  evidence_source?: "real_pose_model_output" | "fixture_demo" | "persisted_evidence" | string;
  source_label?: string | null;
  source_runtime?: string | null;
  real_model_output?: boolean;
  model_output_not_truth?: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
}

export interface ReplayMainPlayerTrackOverlay {
  overlay_type: "main_player_track_assignment";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  bbox: ReplayDetectionBBox;
  track_candidate_id: string | null;
  track_role_candidate: string | null;
  label: string;
  assignment_score: number | null;
  assignment_method: string | null;
  track_lock_state?: string | null;
  source_track_candidate_observation_id?: string | null;
  source_subject_candidate_observation_id: string | null;
  source_detection_observation_id: string | null;
  candidate_track_only: boolean;
  candidate_subject_only?: boolean;
  not_identity_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  source_language: "main player track assignment candidate";
  coordinate_space: "image_pixels";
  evidence_source?: string;
  source_label?: string | null;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  model_output_not_truth?: boolean;
}

export interface ReplaySmoothedCandidateSource {
  overlay_type:
    | "smoothed_ball_position_candidate"
    | "smoothed_main_player_box_candidate"
    | "smoothed_pose_candidate";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  smoothing_method: string | null;
  source_observation_ids: string[];
  smoothed_candidate_only: boolean;
  not_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  source_language: "smoothed replay candidate evidence";
  coordinate_space: "image_pixels";
  evidence_source?: string;
  source_label?: string | null;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
}

export interface ReplaySmoothedBallOverlay extends ReplaySmoothedCandidateSource {
  overlay_type: "smoothed_ball_position_candidate";
  x: number;
  y: number;
  bbox: ReplayDetectionBBox;
  confidence: number | null;
  source_detection_run_id?: string | null;
  source_tracklet_run_id?: string | null;
  source_tracklet_id?: string | null;
  source_track_point_id?: string | null;
  not_ball_truth: boolean;
}

export interface ReplaySmoothedPlayerBoxOverlay extends ReplaySmoothedCandidateSource {
  overlay_type: "smoothed_main_player_box_candidate";
  bbox: ReplayDetectionBBox;
  confidence: number | null;
  source_main_player_track_run_id?: string | null;
  source_track_assignment_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  not_identity_truth: boolean;
}

export interface ReplaySmoothedPoseOverlay extends ReplaySmoothedCandidateSource {
  overlay_type: "smoothed_pose_candidate";
  pose_confidence: number | null;
  skeleton_format: string;
  skeleton_version: string;
  keypoints: ReplayPoseKeypoint[];
  edges: [string, string][];
  bbox: ReplayDetectionBBox | null;
  source_pose_run_id?: string | null;
  source_pose_observation_id?: string | null;
  source_track_run_id?: string | null;
  track_assignment_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  not_pose_truth: boolean;
}

export interface ReplayCourtEvidenceSource {
  evidence_source?: string;
  source_label?: string | null;
  source_runtime?: string | null;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  fixture_court_evidence?: boolean;
  fixture_camera_view_evidence?: boolean;
  candidate_geometry?: boolean;
  geometry_evidence_only?: boolean;
  diagnostic_geometry?: boolean;
  not_ball_player_projection?: boolean;
  observation_only?: boolean;
  no_adjudication?: boolean;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
  model_output_not_truth?: boolean;
  calibration_audit_v0?: boolean;
  uncalibrated_tom_v1_keypoint_mapping?: boolean;
  calibration_warning?: string | null;
  frame_time_owner?: string | null;
  temporal_display_mode?: ReplayCourtTemporalPersistence | string;
  carried_forward?: boolean;
  active_from_ms?: number | null;
  active_until_ms?: number | null;
  source_observation_id?: string | null;
  source_frame_number?: number | null;
  source_observation_timestamp_ms?: number | null;
  current_replay_timestamp_ms?: number | null;
  court_persistence_max_gap_ms?: number | null;
  carry_forward_boundary?: string | null;
  camera_view_boundary_available?: boolean;
  temporal_display_candidate?: boolean;
  candidate_geometry_only?: boolean;
  not_court_truth?: boolean;
}

export interface ReplayCourtKeypoint {
  name: string;
  x: number | null;
  y: number | null;
  confidence: number | null;
  present: boolean;
  visibility?: string | null;
  source_index?: number | null;
}

export interface ReplayRawTomV1CourtKeypoint {
  source_index: number;
  label: string;
  raw_name?: string | null;
  raw_x: number | null;
  raw_y: number | null;
  image_x: number | null;
  image_y: number | null;
  confidence: number | null;
  present: boolean;
  visibility?: string | null;
  coordinate_interpretation?: string | null;
}

export interface ReplayCourtKeypointOverlay extends ReplayCourtEvidenceSource {
  overlay_type: "court_keypoint_evidence";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  coordinate_space: "image_pixels";
  court_keypoint_schema: string;
  schema_version: string;
  keypoints: ReplayCourtKeypoint[];
  mapped_keypoints?: ReplayCourtKeypoint[];
  raw_tom_v1_keypoints?: ReplayRawTomV1CourtKeypoint[];
  preprocessing_mode?: string | null;
  coordinate_interpretation?: string | null;
  raw_output_coordinate_assumption?: string | null;
  model_input_size?: number | null;
  output_reference_size?: number | null;
  mapping_version?: string | null;
  inferred_tom_v3_keypoints?: string[];
  keypoint_count: number;
  keypoints_present_count: number;
  keypoints_missing_count: number;
  mean_keypoint_confidence: number | null;
  min_keypoint_confidence: number | null;
  max_keypoint_confidence: number | null;
}

export interface ReplayCourtLineSegment {
  line_class: string;
  x1: number | null;
  y1: number | null;
  x2: number | null;
  y2: number | null;
  confidence: number | null;
  visibility?: string | null;
}

export interface ReplayCourtLineOverlay extends ReplayCourtEvidenceSource {
  overlay_type: "court_line_evidence";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  coordinate_space: "image_pixels";
  line_segments: ReplayCourtLineSegment[];
  line_classes?: string[];
  line_count: number;
  mean_line_confidence: number | null;
}

export interface ReplayCameraViewOverlay extends ReplayCourtEvidenceSource {
  overlay_type: "camera_view_evidence";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number | null;
  timestamp_end_ms: number | null;
  view_label: string;
  view_confidence: number | null;
  camera_motion_hint: string | null;
  stability_score: number | null;
  cut_likelihood: number | null;
}

export interface ReplayCourtTemplateKeypoint {
  name: string;
  x: number;
  y: number;
}

export interface ReplayCourtTemplateLine {
  line_class: string;
  start_keypoint: string;
  end_keypoint: string;
}

export interface ReplayCourtTemplate {
  template_name: string;
  template_version: string;
  target_coordinate_space: string;
  keypoints: ReplayCourtTemplateKeypoint[];
  lines: ReplayCourtTemplateLine[];
}

export type HomographyMatrix3x3 = [
  [number, number, number],
  [number, number, number],
  [number, number, number]
];

export interface ReplayHomographyCandidateOverlay extends ReplayCourtEvidenceSource {
  overlay_type: "homography_candidate";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  source_court_keypoint_observation_id: string | null;
  source_court_line_observation_id: string | null;
  source_camera_view_observation_id: string | null;
  homography_matrix: HomographyMatrix3x3 | null;
  inverse_homography_matrix: HomographyMatrix3x3 | null;
  matrix_direction: string;
  template_name: string;
  template_version: string;
  template: ReplayCourtTemplate | null;
  reprojection_error_mean: number | null;
  reprojection_error_median: number | null;
  reprojection_error_max: number | null;
  inlier_count: number | null;
  outlier_count: number | null;
  source_point_count: number | null;
  source_line_count: number | null;
  confidence: number | null;
  status: string;
}

export interface ReplayProjectedTemplateKeypoint {
  name: string;
  template_x: number;
  template_y: number;
  image_x: number | null;
  image_y: number | null;
  valid: boolean;
}

export interface ReplayProjectedTemplateLine {
  line_class: string;
  start_keypoint: string;
  end_keypoint: string;
  x1: number | null;
  y1: number | null;
  x2: number | null;
  y2: number | null;
  valid: boolean;
}

export interface ReplayProjectionDiagnosticOverlay extends ReplayCourtEvidenceSource {
  overlay_type: "projection_diagnostic";
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  source_homography_candidate_observation_id: string;
  projected_template_keypoints: ReplayProjectedTemplateKeypoint[];
  projected_template_lines: ReplayProjectedTemplateLine[];
  diagnostic_metrics: JsonRecord;
  status: string;
  confidence: number | null;
}

export interface ReplayOverlayChunk {
  media_id: string;
  start_ms: number;
  end_ms: number;
  coordinate_space: "image_pixels";
  video_width: number | null;
  video_height: number | null;
  detections: ReplayDetectionOverlay[];
  tracklets: ReplayTrackletOverlay[];
  poses: ReplayPoseOverlay[];
  main_player_tracks: ReplayMainPlayerTrackOverlay[];
  smoothed_ball: ReplaySmoothedBallOverlay[];
  smoothed_player_boxes: ReplaySmoothedPlayerBoxOverlay[];
  smoothed_pose: ReplaySmoothedPoseOverlay[];
  court_keypoints: ReplayCourtKeypointOverlay[];
  court_lines: ReplayCourtLineOverlay[];
  camera_view: ReplayCameraViewOverlay[];
  homography_candidates: ReplayHomographyCandidateOverlay[];
  projection_diagnostics: ReplayProjectionDiagnosticOverlay[];
  court_temporal_persistence?: ReplayCourtTemporalPersistence | string;
  court_persistence_max_gap_ms?: number;
  observation_only: boolean;
  no_adjudication: boolean;
}

export type ReplayMode = "replay" | "stream_proxy";

export interface ReplayPlaybackState {
  currentTimeSeconds: number;
  timestampMs: number;
  frameNumber: number;
  durationSeconds: number;
  paused: boolean;
}

export interface ReplaySeekRequest {
  timestampMs: number;
  nonce: number;
}

export interface ReplayDetectionTimelineItem {
  item_type: "detection";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  label: string;
  observation_type: "ball_detection" | "player_detection";
  confidence: number | null;
  display_label: string;
  evidence_source?: "real_model_output" | "fixture_demo" | "persisted_evidence" | string;
  source_label?: string | null;
  real_model_output?: boolean;
  model_output_not_truth?: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
  source_track_run_id?: string | null;
  track_assignment_observation_id?: string | null;
  track_candidate_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  candidate_track_only?: boolean;
  source_subject_run_id?: string | null;
  subject_candidate_observation_id?: string | null;
  subject_role_candidate?: string | null;
  candidate_subject_only?: boolean;
  not_identity_truth?: boolean;
}

export interface ReplayTrackletTimelineItem {
  item_type: "tracklet";
  observation_id: string | null;
  tracklet_id: string;
  run_id: string;
  timestamp_start_ms: number;
  timestamp_end_ms: number;
  frame_start: number | null;
  frame_end: number | null;
  label_hint: string | null;
  track_type: "ball" | "player" | string;
  track_status: "candidate" | string;
  identity_status: "unverified" | string;
  track_point_count: number;
  display_label: string;
  source_detection_run_id?: string | null;
  source_detection_evidence_source?: string | null;
  source_detection_source_label?: string | null;
  source_detection_runtime?: string | null;
  source_detection_real_model_output?: boolean;
  is_real_detection_derived?: boolean;
  candidate_evidence_only?: boolean;
}

export interface ReplayPoseTimelineItem {
  item_type: "pose";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  pose_confidence: number | null;
  keypoints_present_count: number;
  keypoints_missing_count: number;
  display_label: string;
  evidence_source?: "real_pose_model_output" | "fixture_demo" | "persisted_evidence" | string;
  source_label?: string | null;
  source_runtime?: string | null;
  real_model_output?: boolean;
  model_output_not_truth?: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  is_fixture?: boolean;
  is_real_model_output?: boolean;
  source_track_run_id?: string | null;
  track_assignment_observation_id?: string | null;
  track_candidate_observation_id?: string | null;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  candidate_track_only?: boolean;
  source_subject_run_id?: string | null;
  subject_candidate_observation_id?: string | null;
  subject_role_candidate?: string | null;
  candidate_subject_only?: boolean;
  not_identity_truth?: boolean;
}

export interface ReplayMainPlayerTrackTimelineItem {
  item_type: "main_player_track_assignment";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  track_candidate_id: string | null;
  track_role_candidate: string | null;
  assignment_score: number | null;
  assignment_method: string | null;
  source_subject_candidate_observation_id: string | null;
  source_detection_observation_id: string | null;
  candidate_track_only: boolean;
  not_identity_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  display_label: string;
}

export interface ReplayAnnotationTimelineItem {
  item_type: "annotation";
  annotation_id: string;
  target_observation_id: string | null;
  target_observation_type: string | null;
  target_run_id: string | null;
  timestamp_ms: number;
  frame_number: number;
  annotation_label: string;
  created_by: string | null;
  display_label: string;
}

export interface ReplayCourtKeypointTimelineItem extends ReplayCourtEvidenceSource {
  item_type: "court_keypoint";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  court_keypoint_schema: string;
  schema_version: string;
  keypoint_count: number;
  keypoints_present_count: number;
  keypoints_missing_count: number;
  mean_keypoint_confidence: number | null;
  display_label: string;
}

export interface ReplayCourtLineTimelineItem extends ReplayCourtEvidenceSource {
  item_type: "court_line";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  line_count: number;
  line_classes?: string[];
  mean_line_confidence: number | null;
  display_label: string;
}

export interface ReplayCameraViewTimelineItem extends ReplayCourtEvidenceSource {
  item_type: "camera_view";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  frame_start: number | null;
  frame_end: number | null;
  timestamp_start_ms: number | null;
  timestamp_end_ms: number | null;
  view_label: string;
  view_confidence: number | null;
  camera_motion_hint: string | null;
  stability_score: number | null;
  cut_likelihood: number | null;
  display_label: string;
}

export interface ReplayHomographyCandidateTimelineItem extends ReplayCourtEvidenceSource {
  item_type: "homography_candidate";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  status: string;
  template_name: string;
  template_version: string;
  matrix_direction: string;
  source_point_count: number | null;
  source_line_count: number | null;
  reprojection_error_mean: number | null;
  confidence: number | null;
  display_label: string;
}

export interface ReplayProjectionDiagnosticTimelineItem extends ReplayCourtEvidenceSource {
  item_type: "projection_diagnostic";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  source_homography_candidate_observation_id: string;
  projected_keypoint_count: number | null;
  projected_line_count: number | null;
  status: string;
  confidence: number | null;
  display_label: string;
}

export interface ReplaySmoothedMotionTimelineItem {
  item_type:
    | "smoothed_ball_position_candidate"
    | "smoothed_main_player_box_candidate"
    | "smoothed_pose_candidate";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  display_label: string;
  smoothing_method: string | null;
  source_observation_ids: string[];
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  smoothed_candidate_only: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
}

export type ReplayTimelineItem =
  | ReplayDetectionTimelineItem
  | ReplayTrackletTimelineItem
  | ReplayPoseTimelineItem
  | ReplayMainPlayerTrackTimelineItem
  | ReplaySmoothedMotionTimelineItem
  | ReplayCourtKeypointTimelineItem
  | ReplayCourtLineTimelineItem
  | ReplayCameraViewTimelineItem
  | ReplayHomographyCandidateTimelineItem
  | ReplayProjectionDiagnosticTimelineItem
  | ReplayAnnotationTimelineItem;

export interface ReplayTimelineLane {
  lane_type:
    | "detections"
    | "tracklets"
    | "pose"
    | "main_player_tracks"
    | "smoothed_motion"
    | "court_keypoints"
    | "court_lines"
    | "camera_view"
    | "homography_candidates"
    | "projection_diagnostics"
    | "annotations";
  label: string;
  items: ReplayTimelineItem[];
}

export interface ReplayTimeline {
  media_id: string;
  duration_ms: number | null;
  frame_count: number | null;
  fps: number | null;
  observation_only: boolean;
  no_adjudication: boolean;
  annotations_without_time_count: number;
  lanes: ReplayTimelineLane[];
}

export interface TimelineRange {
  start: number;
  end: number;
}

export interface TimelineSegment {
  id: string;
  label: string;
  state: string;
  frameStart: number;
  frameEnd: number;
  confidence: number | null;
  observationId?: string;
  trackletId?: string;
}

export interface TimelineRow {
  id: string;
  label: string;
  segments: TimelineSegment[];
}

export interface CandidateMarker {
  id: string;
  type: string;
  label: string;
  frame: number;
  confidence: number | null;
  observationId: string;
}

export interface DetectionBBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface DetectionPoint {
  x: number;
  y: number;
}

export interface DetectionOverlayItem {
  id: string;
  observationId: string;
  observationType: "ball_detection" | "player_detection";
  label: string;
  frameNumber: number;
  timestampMs: number | null;
  confidence: number | null;
  bbox: DetectionBBox;
  center: DetectionPoint | null;
  classLabel: string | null;
  classId: number | string | null;
  metadata: JsonRecord;
  isSelected: boolean;
}

export interface FrameArtifactImage {
  artifact: EvidenceArtifact;
  match: "selected_observation" | "same_frame";
}

export interface DetectionOverlayModel {
  items: DetectionOverlayItem[];
  frameItems: DetectionOverlayItem[];
  selectedFrame: number | null;
  frameArtifact: FrameArtifactImage | null;
  missingBboxObservationIds: string[];
  unavailableReason: string | null;
  mediaWidth: number | null;
  mediaHeight: number | null;
}

export interface PoseBBox {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number | null;
}

export type PoseConfidenceBand = "unknown" | "low" | "normal";

export interface PoseOverlayKeypoint extends PoseKeypoint {
  confidenceBand: PoseConfidenceBand;
}

export interface PoseOverlayEdge {
  id: string;
  start: PoseOverlayKeypoint;
  end: PoseOverlayKeypoint;
}

export interface PoseOverlayItem {
  id: string;
  observationId: string;
  frameNumber: number;
  timestampMs: number | null;
  skeletonFormat: string;
  skeletonVersion: string;
  poseConfidence: number | null;
  bbox: PoseBBox | null;
  keypoints: PoseKeypoint[];
  presentKeypoints: PoseOverlayKeypoint[];
  missingKeypoints: PoseKeypoint[];
  edges: PoseOverlayEdge[];
  keypointCount: number;
  keypointsPresentCount: number;
  keypointsMissingCount: number;
  meanKeypointConfidence: number | null;
  minKeypointConfidence: number | null;
  maxKeypointConfidence: number | null;
  subjectRefType: string;
  subjectDetectionObservationId: string | null;
  subjectTrackletId: string | null;
  subjectTrackPointId: string | null;
  associationStatus: string;
  associationMethod: string | null;
  associationConfidence: number | null;
  frameTimeOwner: string;
  metadata: JsonRecord;
  isSelected: boolean;
}

export interface PoseOverlayModel {
  items: PoseOverlayItem[];
  frameItems: PoseOverlayItem[];
  selectedFrame: number | null;
  selectedPoseItem: PoseOverlayItem | null;
  unavailableReason: string | null;
  mediaWidth: number | null;
  mediaHeight: number | null;
}

export interface RuntimeConfigSummary {
  id: string;
  config_name: string;
  config_version: string;
  payload_jsonb: JsonRecord;
  created_at: string | null;
}

export interface ModelRegistrySummary {
  id: string;
  name: string;
  version: string;
  model_family: string;
  source: string | null;
  metadata_jsonb: JsonRecord;
  created_at: string | null;
}

export interface TrackletEvidenceSourceDetection {
  observation: Observation;
  frame_artifacts: EvidenceArtifact[];
  annotations: HumanAnnotation[];
  annotation_summary: AnnotationSummary;
}

export interface TrackletEvidencePoint {
  typed: TrackPoint;
  observation: Observation | null;
  sequence_index: number | string | null;
  frame_number: number;
  timestamp_ms: number | null;
  bbox: unknown;
  center: unknown;
  source_detection_observation_id: string | null;
  source_detection: Observation | null;
  lineage_to_source: LineageRow | null;
  lineage_to_tracklet: LineageRow | null;
  frame_artifacts: EvidenceArtifact[];
  annotations: HumanAnnotation[];
  annotation_summary: AnnotationSummary;
}

export interface TrackletEvidenceBundle {
  tracklet: {
    typed: Omit<Tracklet, "points">;
    observation: Observation | null;
    annotations: HumanAnnotation[];
    annotation_summary: AnnotationSummary;
  };
  media: MediaAsset | null;
  runs: {
    tracklet_run: ProcessingRun | null;
    source_detection_run: ProcessingRun | null;
  };
  runtime_configs: {
    tracklet_runtime_config: RuntimeConfigSummary | null;
    source_detection_runtime_config: RuntimeConfigSummary | null;
  };
  model_registry: {
    tracklet_builder_model: ModelRegistrySummary | null;
    source_detection_model: ModelRegistrySummary | null;
  };
  track_points: TrackletEvidencePoint[];
  source_detections: TrackletEvidenceSourceDetection[];
  frame_artifacts: EvidenceArtifact[];
  lineage: LineageRow[];
  annotations: HumanAnnotation[];
  annotation_summary: {
    tracklet: AnnotationSummary;
    track_points: AnnotationSummary;
    source_detections: AnnotationSummary;
    all: AnnotationSummary;
  };
  summary: {
    track_status: string | null;
    identity_status: string | null;
    track_point_count: number;
    source_detection_count: number;
    frame_start: number | null;
    frame_end: number | null;
    timestamp_start_ms: number | null;
    timestamp_end_ms: number | null;
    gap_count: number | null;
    confidence: number | null;
    warning: string;
  };
}
