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

export interface DetectionOverlayModel {
  items: DetectionOverlayItem[];
  frameItems: DetectionOverlayItem[];
  selectedFrame: number | null;
  missingBboxObservationIds: string[];
  unavailableReason: string | null;
  mediaWidth: number | null;
  mediaHeight: number | null;
}
