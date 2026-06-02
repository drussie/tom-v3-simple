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
  source_motion_smoothing_run_id?: string | null;
  source_detection_evidence_source?: string | null;
  source_detection_source_label?: string | null;
  source_detection_runtime?: string | null;
  source_subject_run_id?: string | null;
  source_court_run_id?: string | null;
  source_homography_run_id?: string | null;
  source_court_projection_run_id?: string | null;
  camera_geometry_id?: string | null;
  trajectory_3d_run_id?: string | null;
  camera_model?: string | null;
  geometry_status?: string | null;
  court_model?: string | null;
  court_plane_geometry_declared?: boolean;
  camera_intrinsics_known?: boolean;
  camera_extrinsics_known?: boolean;
  true_3d_reconstruction_available?: boolean;
  "3d_ball_trajectory_available"?: boolean;
  "3d_ball_trajectory_truth_available"?: boolean;
  trajectory_3d_candidate_count?: number;
  known_height_count?: number;
  unknown_height_count?: number;
  height_model?: string | null;
  track_candidate_count?: number;
  track_assignment_count?: number;
  court_keypoint_count?: number;
  court_line_count?: number;
  camera_view_count?: number;
  candidate_count?: number;
  projection_diagnostic_count?: number;
  ball_court_projection_count?: number;
  main_player_court_projection_count?: number;
  ball_trajectory_court_candidate_count?: number;
  hit_candidate_count?: number;
  bounce_candidate_count?: number;
  evaluated_trajectory_points?: number | null;
  source_point_count?: number;
  candidate_geometry?: boolean;
  diagnostic_geometry?: boolean;
  projection_candidate_only?: boolean;
  trajectory_candidate_only?: boolean;
  event_candidate_only?: boolean;
  candidate_only?: boolean;
  not_ball_truth?: boolean;
  not_player_truth?: boolean;
  not_bounce_truth?: boolean;
  not_hit_truth?: boolean;
  not_in_out_truth?: boolean;
  not_court_truth?: boolean;
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
  court_projection: ReplayRunSummary[];
  ball_trajectory: ReplayRunSummary[];
  event_candidate: ReplayRunSummary[];
  camera_geometry: ReplayRunSummary[];
  trajectory_3d: ReplayRunSummary[];
  event_candidate_3d_diagnostic?: ReplayRunSummary[];
  main_player_track: ReplayRunSummary[];
  motion_smoothing: ReplayRunSummary[];
}

export interface ReplayCameraGeometrySummary {
  available: boolean;
  camera_geometry_id?: string | null;
  media_id?: string | null;
  court_run_id?: string | null;
  court_projection_run_id?: string | null;
  homography_run_id?: string | null;
  geometry_run_id?: string | null;
  camera_model?: string | null;
  geometry_status?: string | null;
  court_model?: string | null;
  court_plane_geometry_declared?: boolean;
  camera_intrinsics_known?: boolean;
  camera_extrinsics_known?: boolean;
  true_3d_reconstruction_available?: boolean;
  "3d_ball_trajectory_available"?: boolean;
  geometry_evidence_only?: boolean;
  no_adjudication?: boolean;
}

export interface ReplayTrajectory3DSummary {
  available: boolean;
  trajectory_3d_run_id?: string | null;
  media_id?: string | null;
  ball_trajectory_run_id?: string | null;
  court_projection_run_id?: string | null;
  camera_geometry_id?: string | null;
  candidate_count?: number;
  height_model?: string | null;
  known_height_count?: number;
  unknown_height_count?: number;
  true_3d_reconstruction_available?: boolean;
  "3d_ball_trajectory_truth_available"?: boolean;
  geometry_evidence_only?: boolean;
  no_adjudication?: boolean;
}

export interface ReplayTrajectory3DDebugCourtDimensions {
  units: string;
  court_length: number;
  court_width: number;
  net_height_center: number;
  net_height_posts: number;
}

export interface ReplayTrajectory3DDebugPoint {
  id: string;
  frame: number;
  frame_number: number;
  timestamp_ms: number;
  court_x_m: number | null;
  court_y_m: number | null;
  court_z_m: number | null;
  court_z_status: string;
  height_model: string;
  velocity_available: boolean;
  speed_mps?: number | null;
  trajectory_3d_candidate_only: boolean;
  not_3d_truth: boolean;
  height_not_verified: boolean;
  no_adjudication: boolean;
}

export interface ReplayTrajectory3DDebugPayload {
  available: boolean;
  status?: string;
  trajectory_3d_run_id?: string | null;
  camera_geometry_id?: string | null;
  media_id?: string | null;
  height_model?: string | null;
  known_height_count?: number;
  unknown_height_count?: number;
  true_3d_reconstruction_available?: boolean;
  court_dimensions?: ReplayTrajectory3DDebugCourtDimensions;
  points?: ReplayTrajectory3DDebugPoint[];
  trajectory_3d_debug_review_summary?: ReplayTrajectory3DDebugReviewSummary;
  warnings?: {
    display_only?: boolean;
    trajectory_3d_candidate_only?: boolean;
    not_3d_truth?: boolean;
    height_not_verified?: boolean;
    no_adjudication?: boolean;
  };
  display_only?: boolean;
  trajectory_3d_candidate_only?: boolean;
  not_3d_truth?: boolean;
  height_not_verified?: boolean;
  no_adjudication?: boolean;
}

export type Trajectory3DDebugReviewKind =
  | "trajectory_3d_sample_review"
  | "event_candidate_3d_diagnostic_review"
  | "missing_3d_sample_note"
  | "debug_view_note";

export type Trajectory3DDebugReviewLabel =
  | "useful"
  | "wrong"
  | "unclear"
  | "needs_review"
  | "missing_3d_sample"
  | "bad_3d_position"
  | "bad_diagnostic_link";

export interface Trajectory3DDebugReviewAnnotation {
  id: string;
  media_id: string;
  trajectory_3d_run_id: string | null;
  camera_geometry_id: string | null;
  event_candidate_run_id: string | null;
  event_observation_id: string | null;
  trajectory_3d_candidate_id: string | null;
  event_candidate_3d_diagnostic_id: string | null;
  annotation_kind: Trajectory3DDebugReviewKind | string;
  review_label: Trajectory3DDebugReviewLabel | string;
  frame: number | null;
  timestamp_ms: number | null;
  image_x: number | null;
  image_y: number | null;
  court_x_m: number | null;
  court_y_m: number | null;
  court_z_m: number | null;
  note: string | null;
  reviewer: string | null;
  created_at: string;
  updated_at: string;
  payload_jsonb: JsonRecord;
}

export interface ReplayTrajectory3DDebugReviewSummary {
  available: boolean;
  total_reviews: number;
  sample_reviews?: number;
  diagnostic_reviews?: number;
  missing_3d_sample_notes?: number;
  debug_view_notes?: number;
  useful?: number;
  wrong?: number;
  unclear?: number;
  needs_review?: number;
  missing_3d_sample?: number;
  bad_3d_position?: number;
  bad_diagnostic_link?: number;
  review_metadata_only?: boolean;
  not_truth?: boolean;
  not_3d_truth?: boolean;
  does_not_change_event_candidates?: boolean;
  does_not_change_3d_candidates?: boolean;
  does_not_create_in_out?: boolean;
  does_not_create_score?: boolean;
  no_adjudication?: boolean;
}

export interface Trajectory3DDebugReviewList {
  reviews: Trajectory3DDebugReviewAnnotation[];
  reviews_by_trajectory_3d_candidate_id: Record<string, Trajectory3DDebugReviewAnnotation[]>;
  reviews_by_event_candidate_3d_diagnostic_id: Record<
    string,
    Trajectory3DDebugReviewAnnotation[]
  >;
  review_summary: ReplayTrajectory3DDebugReviewSummary;
  warnings: Record<string, boolean>;
}

export interface ReplayEventCandidate3DDiagnostic {
  id: string;
  event_observation_id: string;
  candidate_type: string;
  frame: number;
  timestamp_ms: number;
  trajectory_3d_run_id?: string | null;
  camera_geometry_id?: string | null;
  nearest_3d_candidate_id?: string | null;
  nearest_3d_frame?: number | null;
  nearest_3d_timestamp_ms?: number | null;
  nearest_time_delta_ms?: number | null;
  nearest_court_x_m?: number | null;
  nearest_court_y_m?: number | null;
  nearest_court_z_m?: number | null;
  height_status: string;
  diagnostic_status: string;
  diagnostic_label: string;
  diagnostic_confidence?: number | null;
  pre_window_sample_count: number;
  post_window_sample_count: number;
  local_window_sample_count: number;
  local_velocity_available: boolean;
  local_speed_mps?: number | null;
  local_direction_delta_degrees?: number | null;
  diagnostic_only: boolean;
  not_truth: boolean;
  not_3d_truth: boolean;
  height_not_verified: boolean;
  no_adjudication: boolean;
}

export interface ReplayEventCandidate3DDiagnosticSummary {
  available: boolean;
  event_candidate_run_id?: string | null;
  trajectory_3d_run_id?: string | null;
  camera_geometry_id?: string | null;
  diagnostic_count?: number;
  height_unknown_count?: number;
  supports_candidate_context_count?: number;
  weakens_candidate_context_count?: number;
  neutral_context_count?: number;
  diagnostic_only?: boolean;
  not_truth?: boolean;
  not_3d_truth?: boolean;
  no_adjudication?: boolean;
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
  camera_geometry_summary: ReplayCameraGeometrySummary;
  trajectory_3d_summary: ReplayTrajectory3DSummary;
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
export type ReplayPoseVisualStyle = "limbs_only" | "limbs_and_joints" | "joints_only";
export type ReplayEventCandidateMarkerState = "inactive" | "active" | "selected";

export type ReplayLayerPreset = "operator" | "debug";
export type ReplayPoseLimbSide = "left" | "right" | "neutral";
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

export interface ReplayCourtProjectionPoint {
  x: number;
  y: number;
}

export interface ReplayCourtProjectionImageAnchor extends ReplayCourtProjectionPoint {
  anchor_type: string;
  bbox?: ReplayDetectionBBox;
}

export interface ReplayCourtProjectionBase {
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  court_point: ReplayCourtProjectionPoint;
  court_coordinate_space: "court_template_2d" | string;
  template_name: string | null;
  template_version: string | null;
  projection_method: string | null;
  source_motion_smoothing_run_id: string | null;
  source_homography_run_id: string | null;
  source_homography_observation_id: string | null;
  source_homography_status: string | null;
  source_homography_confidence: number | null;
  homography_match_policy: string | null;
  homography_time_delta_ms: number | null;
  homography_carried_forward: boolean;
  homography_source_frame_number: number | null;
  projection_frame_number: number | null;
  source_observation_ids: string[];
  confidence: number | null;
  projection_candidate_only: boolean;
  not_court_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  coordinate_space: "court_template_2d" | string;
  evidence_source?: string;
  source_label?: string | null;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
}

export interface ReplayBallCourtProjectionOverlay extends ReplayCourtProjectionBase {
  overlay_type: "ball_court_projection_candidate";
  source_ball_observation_id: string | null;
  image_point: ReplayCourtProjectionPoint | null;
  not_ball_truth: boolean;
}

export interface ReplayMainPlayerCourtProjectionOverlay extends ReplayCourtProjectionBase {
  overlay_type: "main_player_court_projection_candidate";
  source_player_box_observation_id: string | null;
  source_main_player_track_run_id: string | null;
  track_candidate_id: string | null;
  track_role_candidate: string | null;
  image_anchor: ReplayCourtProjectionImageAnchor | null;
  not_player_truth: boolean;
  not_identity_truth: boolean;
}

export interface ReplayBallTrajectoryPoint {
  frame_number: number;
  timestamp_ms: number;
  court_x: number;
  court_y: number;
  source_observation_id: string | null;
  source_homography_observation_id: string | null;
  homography_time_delta_ms: number | null;
  homography_carried_forward: boolean;
  inside_template_bounds: boolean;
}

export interface ReplayBallTrajectoryKinematicStep {
  from_frame: number;
  to_frame: number;
  dt_ms: number;
  dx: number;
  dy: number;
  speed_template_units_per_second: number;
  direction_angle_degrees: number;
}

export interface ReplayBallCourtTrajectoryOverlay {
  overlay_type: "ball_trajectory_court_candidate";
  observation_id: string;
  run_id: string;
  source_court_projection_run_id: string | null;
  source_ball_court_projection_observation_ids: string[];
  trajectory_segment_index: number;
  frame_start: number;
  frame_end: number;
  timestamp_start_ms: number;
  timestamp_end_ms: number;
  point_count: number;
  points: ReplayBallTrajectoryPoint[];
  kinematics: ReplayBallTrajectoryKinematicStep[];
  diagnostics: JsonRecord;
  trajectory_method: string | null;
  coordinate_space: "court_template_2d" | string;
  template_name: string | null;
  template_version: string | null;
  confidence: number | null;
  trajectory_candidate_only: boolean;
  not_ball_truth: boolean;
  not_bounce_truth: boolean;
  not_hit_truth: boolean;
  not_in_out_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  evidence_source?: string;
  source_label?: string | null;
}

export interface ReplayEventCandidateNearestPlayer {
  track_role_candidate: string | null;
  track_candidate_id: string | null;
  source_player_court_projection_observation_id: string | null;
  court_x: number;
  court_y: number;
  distance_template_units: number;
  time_delta_ms: number;
}

export interface ReplayEventCandidateTrajectoryContext {
  previous_frame?: number;
  next_frame?: number;
  previous_timestamp_ms?: number;
  next_timestamp_ms?: number;
  direction_before_degrees?: number;
  direction_after_degrees?: number;
  direction_delta_degrees?: number;
  speed_before?: number;
  speed_after?: number;
  speed_delta_fraction?: number;
}

export interface ReplayEventCandidatePlayerProximityGate {
  nearest_player_found: boolean;
  distance_template_units: number | null;
  time_delta_ms: number | null;
  threshold: number;
  away_from_player?: boolean;
}

export interface ReplayEventCandidateDecision {
  selected_candidate_type: string;
  suppressed_candidate_types: string[];
  reason: string;
  classification_priority?: string;
}

export interface ReplayEventCandidateNetAxisReversal {
  axis: string;
  vy_before: number | null;
  vy_after: number | null;
  reversal: boolean;
  min_axis_delta: number;
  previous_frame?: number | null;
  current_frame?: number;
  next_frame?: number | null;
  previous_timestamp_ms?: number | null;
  current_timestamp_ms?: number;
  next_timestamp_ms?: number | null;
}

export interface ReplayEventCandidateVerticalMotionProxy {
  proxy_type: string;
  status?: string;
  image_y_before: number | null;
  image_y_current: number | null;
  image_y_after: number | null;
  image_vy_before: number | null;
  image_vy_after: number | null;
  descending_to_ascending: boolean;
  min_image_y_delta_pixels: number;
  previous_frame?: number | null;
  current_frame?: number;
  next_frame?: number | null;
  previous_timestamp_ms?: number | null;
  current_timestamp_ms?: number;
  next_timestamp_ms?: number | null;
  proxy_warning?: string;
}

export interface ReplayEventCandidateSpeedReduction {
  speed_before: number;
  speed_after: number;
  speed_reduction_fraction: number | null;
  speed_reduced: boolean;
  min_speed_reduction_fraction: number;
}

export interface ReplayEventCandidateOverlay {
  overlay_type: "hit_candidate" | "bounce_candidate";
  candidate_type: "hit_candidate" | "bounce_candidate" | string;
  observation_id: string;
  run_id: string;
  frame_number: number;
  timestamp_ms: number;
  court_point: ReplayCourtProjectionPoint;
  image_point: ReplayCourtProjectionPoint | null;
  image_marker_source:
    | "source_ball_court_projection_image_point"
    | "event_candidate_payload_image_point"
    | "unavailable"
    | string;
  confidence: number | null;
  reason_codes: string[];
  candidate_method: string | null;
  original_candidate_type?: string | null;
  original_candidate_method?: string | null;
  classification_priority: string | null;
  player_proximity_gate: ReplayEventCandidatePlayerProximityGate | null;
  candidate_decision: ReplayEventCandidateDecision | null;
  net_axis_reversal: ReplayEventCandidateNetAxisReversal | null;
  vertical_motion_proxy: ReplayEventCandidateVerticalMotionProxy | null;
  speed_reduction: ReplayEventCandidateSpeedReduction | null;
  court_side_zone?: Record<string, unknown> | null;
  player_contact_zone?: Record<string, unknown> | null;
  court_landing_zone?: Record<string, unknown> | null;
  candidate_reclassification?: Record<string, unknown> | null;
  candidate_sequence?: Record<string, unknown> | null;
  player_anchored_hit_recall?: Record<string, unknown> | null;
  player_anchor_contact_zone?: Record<string, unknown> | null;
  net_axis_reversal_recall?: Record<string, unknown> | null;
  image_space_net_axis_reversal_recall?: Record<string, unknown> | null;
  image_space_direction_change_recall?: Record<string, unknown> | null;
  local_evidence_event_type?: Record<string, unknown> | null;
  universal_hit_validity_guard?: Record<string, unknown> | null;
  marker_level_arbitration?: Record<string, unknown> | null;
  overlap_suppression?: Record<string, unknown> | null;
  source_ball_trajectory_run_id: string | null;
  source_ball_trajectory_observation_id: string | null;
  source_court_projection_run_id: string | null;
  source_ball_court_projection_observation_id: string | null;
  source_player_court_projection_observation_id: string | null;
  nearest_player: ReplayEventCandidateNearestPlayer | null;
  trajectory_context: ReplayEventCandidateTrajectoryContext;
  coordinate_space: "court_template_2d" | string;
  template_name: string | null;
  template_version: string | null;
  candidate_only: boolean;
  not_ball_truth: boolean;
  not_hit_truth: boolean;
  not_bounce_truth: boolean;
  not_in_out_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
  model_registry_id?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  runtime_config_id?: string | null;
  evidence_source?: string;
  source_label?: string | null;
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
  ball_court_projection: ReplayBallCourtProjectionOverlay[];
  main_player_court_projection: ReplayMainPlayerCourtProjectionOverlay[];
  ball_court_trajectory: ReplayBallCourtTrajectoryOverlay[];
  hit_candidates: ReplayEventCandidateOverlay[];
  bounce_candidates: ReplayEventCandidateOverlay[];
  marker_summary: ReplayMarkerSummary[];
  event_candidate_3d_diagnostics?: ReplayEventCandidate3DDiagnostic[];
  event_candidate_3d_diagnostic_summary?: ReplayEventCandidate3DDiagnosticSummary;
  trajectory_3d_debug?: ReplayTrajectory3DDebugPayload;
  trajectory_3d_debug_review_summary?: ReplayTrajectory3DDebugReviewSummary;
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

export interface ReplayCourtProjectionTimelineItem {
  item_type: "ball_court_projection_candidate" | "main_player_court_projection_candidate";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  display_label: string;
  court_point: ReplayCourtProjectionPoint;
  court_coordinate_space: string;
  projection_method: string | null;
  source_homography_observation_id: string | null;
  homography_time_delta_ms: number | null;
  homography_carried_forward: boolean;
  track_candidate_id?: string | null;
  track_role_candidate?: string | null;
  projection_candidate_only: boolean;
  not_ball_truth?: boolean | null;
  not_player_truth?: boolean | null;
  not_court_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
}

export interface ReplayBallTrajectoryTimelineItem {
  item_type: "ball_trajectory_court_candidate";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  timestamp_start_ms: number;
  timestamp_end_ms: number;
  frame_start: number;
  frame_end: number;
  display_label: string;
  point_count: number;
  trajectory_method: string | null;
  coordinate_space: string;
  source_court_projection_run_id: string | null;
  trajectory_candidate_only: boolean;
  not_ball_truth: boolean;
  not_bounce_truth: boolean;
  not_hit_truth: boolean;
  not_in_out_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
}

export interface ReplayEventCandidateTimelineItem {
  item_type: "hit_candidate" | "bounce_candidate";
  observation_id: string;
  run_id: string;
  timestamp_ms: number;
  frame_number: number;
  display_label: string;
  candidate_type: "hit_candidate" | "bounce_candidate" | string;
  court_point: ReplayCourtProjectionPoint;
  image_point: ReplayCourtProjectionPoint | null;
  image_marker_source:
    | "source_ball_court_projection_image_point"
    | "event_candidate_payload_image_point"
    | "unavailable"
    | string;
  confidence: number | null;
  reason_codes: string[];
  candidate_method: string | null;
  original_candidate_type?: string | null;
  original_candidate_method?: string | null;
  classification_priority: string | null;
  player_proximity_gate: ReplayEventCandidatePlayerProximityGate | null;
  candidate_decision: ReplayEventCandidateDecision | null;
  net_axis_reversal: ReplayEventCandidateNetAxisReversal | null;
  vertical_motion_proxy: ReplayEventCandidateVerticalMotionProxy | null;
  speed_reduction: ReplayEventCandidateSpeedReduction | null;
  court_side_zone?: Record<string, unknown> | null;
  player_contact_zone?: Record<string, unknown> | null;
  court_landing_zone?: Record<string, unknown> | null;
  candidate_reclassification?: Record<string, unknown> | null;
  candidate_sequence?: Record<string, unknown> | null;
  player_anchored_hit_recall?: Record<string, unknown> | null;
  player_anchor_contact_zone?: Record<string, unknown> | null;
  net_axis_reversal_recall?: Record<string, unknown> | null;
  image_space_net_axis_reversal_recall?: Record<string, unknown> | null;
  image_space_direction_change_recall?: Record<string, unknown> | null;
  local_evidence_event_type?: Record<string, unknown> | null;
  universal_hit_validity_guard?: Record<string, unknown> | null;
  marker_level_arbitration?: Record<string, unknown> | null;
  overlap_suppression?: Record<string, unknown> | null;
  source_ball_trajectory_observation_id: string | null;
  source_ball_court_projection_observation_id: string | null;
  source_player_court_projection_observation_id: string | null;
  candidate_only: boolean;
  not_hit_truth: boolean;
  not_bounce_truth: boolean;
  not_in_out_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
}

export interface ReplayMarkerSummary {
  index: number;
  observation_id: string;
  candidate_type: "hit_candidate" | "bounce_candidate" | string;
  frame: number;
  timestamp_ms: number;
  source_method?: string | null;
  candidate_method?: string | null;
  original_candidate_type?: string | null;
  original_candidate_method?: string | null;
  arbitration_decision?: string | null;
  arbitration_reason?: string | null;
  confidence?: number | null;
  court_x?: number | null;
  court_y?: number | null;
  image_x?: number | null;
  image_y?: number | null;
  event_candidate_3d_diagnostic?: ReplayEventCandidate3DDiagnostic;
  candidate_only: boolean;
  not_hit_truth: boolean;
  not_bounce_truth: boolean;
  not_in_out_truth: boolean;
  observation_only: boolean;
  no_adjudication: boolean;
}

export type EventCandidateReviewKind =
  | "candidate_marker_review"
  | "point_moment_review"
  | "missing_candidate_note";

export type EventCandidateReviewLabel =
  | "useful"
  | "wrong"
  | "unclear"
  | "needs_review"
  | "missing_hit_candidate"
  | "missing_bounce_candidate"
  | "missing_event_candidate";

export interface EventCandidateReviewAnnotation {
  id: string;
  media_id: string;
  event_candidate_run_id: string;
  observation_id: string | null;
  annotation_kind: EventCandidateReviewKind | string;
  review_label: EventCandidateReviewLabel | string;
  candidate_type: string | null;
  frame: number | null;
  timestamp_ms: number | null;
  image_x: number | null;
  image_y: number | null;
  court_x: number | null;
  court_y: number | null;
  note: string | null;
  reviewer: string | null;
  created_at: string;
  updated_at: string;
  payload_jsonb: JsonRecord;
}

export interface EventCandidateReviewList {
  reviews: EventCandidateReviewAnnotation[];
  reviews_by_observation_id: Record<string, EventCandidateReviewAnnotation[]>;
  review_summary: Record<string, number>;
  warnings: Record<string, boolean>;
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
  | ReplayCourtProjectionTimelineItem
  | ReplayBallTrajectoryTimelineItem
  | ReplayEventCandidateTimelineItem
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
    | "court_projection"
    | "ball_trajectory"
    | "event_candidates"
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
  marker_summary: ReplayMarkerSummary[];
  event_candidate_3d_diagnostics?: ReplayEventCandidate3DDiagnostic[];
  event_candidate_3d_diagnostic_summary?: ReplayEventCandidate3DDiagnosticSummary;
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
