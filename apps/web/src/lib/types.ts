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
}

export interface ReplayAvailableRuns {
  detection: ReplayRunSummary[];
  tracklet: ReplayRunSummary[];
  pose: ReplayRunSummary[];
  gameplay: ReplayRunSummary[];
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
}

export interface ReplayTrackPointOverlay {
  track_point_id: string;
  observation_id: string | null;
  source_detection_observation_id: string | null;
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
  source_language: "pose keypoint evidence";
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
  observation_only: boolean;
  no_adjudication: boolean;
}

export interface ReplayPlaybackState {
  currentTimeSeconds: number;
  timestampMs: number;
  frameNumber: number;
  durationSeconds: number;
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

export type ReplayTimelineItem =
  | ReplayDetectionTimelineItem
  | ReplayTrackletTimelineItem
  | ReplayPoseTimelineItem
  | ReplayAnnotationTimelineItem;

export interface ReplayTimelineLane {
  lane_type: "detections" | "tracklets" | "pose" | "annotations";
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
