import type {
  EventCandidateReviewAnnotation,
  EventCandidateReviewList,
  EventCandidateReviewLabel,
  EventCandidateReviewKind,
  HumanAnnotation,
  JsonRecord,
  ReplayInfo,
  ReplayOverlayChunk,
  ReplayTimeline,
  Trajectory3DDebugReviewAnnotation,
  Trajectory3DDebugReviewKind,
  Trajectory3DDebugReviewLabel,
  Trajectory3DDebugReviewList,
  TrackletEvidenceBundle,
  ViewerRun
} from "./types";

const defaultApiBaseUrl = "http://127.0.0.1:8000";

export function getApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_TOM_V3_API_BASE_URL ?? defaultApiBaseUrl;
}

export async function fetchViewerRun(runId: string): Promise<ViewerRun> {
  const response = await fetch(`${getApiBaseUrl()}/viewer/runs/${runId}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load run ${runId}: ${response.status}`);
  }

  return (await response.json()) as ViewerRun;
}

export async function fetchReplayInfo(mediaId: string): Promise<ReplayInfo> {
  const response = await fetch(`${getApiBaseUrl()}/media/${mediaId}/replay-info`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load replay info for media ${mediaId}: ${response.status}`);
  }

  return (await response.json()) as ReplayInfo;
}

export interface FetchReplayOverlayChunkInput {
  mediaId: string;
  startMs: number;
  endMs: number;
  layers?: string;
  detectionRunId?: string | null;
  trackletRunId?: string | null;
  poseRunId?: string | null;
  mainPlayerTrackRunId?: string | null;
  motionSmoothingRunId?: string | null;
  courtRunId?: string | null;
  homographyRunId?: string | null;
  projectionDiagnosticRunId?: string | null;
  courtProjectionRunId?: string | null;
  ballTrajectoryRunId?: string | null;
  eventCandidateRunId?: string | null;
  trajectory3dRunId?: string | null;
  courtTemporalPersistence?: string | null;
  courtPersistenceMaxGapMs?: number | null;
  minConfidence?: number | null;
  minPoseConfidence?: number | null;
}

export async function fetchReplayOverlayChunk({
  mediaId,
  startMs,
  endMs,
  layers = "detections",
  detectionRunId = null,
  trackletRunId = null,
  poseRunId = null,
  mainPlayerTrackRunId = null,
  motionSmoothingRunId = null,
  courtRunId = null,
  homographyRunId = null,
  projectionDiagnosticRunId = null,
  courtProjectionRunId = null,
  ballTrajectoryRunId = null,
  eventCandidateRunId = null,
  trajectory3dRunId = null,
  courtTemporalPersistence = null,
  courtPersistenceMaxGapMs = null,
  minConfidence = null,
  minPoseConfidence = null
}: FetchReplayOverlayChunkInput): Promise<ReplayOverlayChunk> {
  const params = new URLSearchParams({
    media_id: mediaId,
    start_ms: startMs.toString(),
    end_ms: endMs.toString(),
    layers
  });
  if (detectionRunId !== null) {
    params.set("detection_run_id", detectionRunId);
  }
  if (trackletRunId !== null) {
    params.set("tracklet_run_id", trackletRunId);
  }
  if (poseRunId !== null) {
    params.set("pose_run_id", poseRunId);
  }
  if (mainPlayerTrackRunId !== null) {
    params.set("main_player_track_run_id", mainPlayerTrackRunId);
  }
  if (motionSmoothingRunId !== null) {
    params.set("motion_smoothing_run_id", motionSmoothingRunId);
  }
  if (courtRunId !== null) {
    params.set("court_run_id", courtRunId);
  }
  if (homographyRunId !== null) {
    params.set("homography_run_id", homographyRunId);
  }
  if (projectionDiagnosticRunId !== null) {
    params.set("projection_diagnostic_run_id", projectionDiagnosticRunId);
  }
  if (courtProjectionRunId !== null) {
    params.set("court_projection_run_id", courtProjectionRunId);
  }
  if (ballTrajectoryRunId !== null) {
    params.set("ball_trajectory_run_id", ballTrajectoryRunId);
  }
  if (eventCandidateRunId !== null) {
    params.set("event_candidate_run_id", eventCandidateRunId);
  }
  if (trajectory3dRunId !== null) {
    params.set("trajectory_3d_run_id", trajectory3dRunId);
  }
  if (courtTemporalPersistence !== null) {
    params.set("court_temporal_persistence", courtTemporalPersistence);
  }
  if (courtPersistenceMaxGapMs !== null) {
    params.set("court_persistence_max_gap_ms", courtPersistenceMaxGapMs.toString());
  }
  if (minConfidence !== null) {
    params.set("min_confidence", minConfidence.toString());
  }
  if (minPoseConfidence !== null) {
    params.set("min_pose_confidence", minPoseConfidence.toString());
  }

  const response = await fetch(`/api/replay/overlays?${params.toString()}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load replay overlay chunk: ${response.status}`);
  }

  return (await response.json()) as ReplayOverlayChunk;
}

export interface FetchReplayTimelineInput {
  mediaId: string;
  detectionRunId?: string | null;
  trackletRunId?: string | null;
  poseRunId?: string | null;
  mainPlayerTrackRunId?: string | null;
  motionSmoothingRunId?: string | null;
  courtRunId?: string | null;
  homographyRunId?: string | null;
  projectionDiagnosticRunId?: string | null;
  courtProjectionRunId?: string | null;
  ballTrajectoryRunId?: string | null;
  eventCandidateRunId?: string | null;
  includeAnnotations?: boolean;
}

export async function fetchReplayTimeline({
  mediaId,
  detectionRunId = null,
  trackletRunId = null,
  poseRunId = null,
  mainPlayerTrackRunId = null,
  motionSmoothingRunId = null,
  courtRunId = null,
  homographyRunId = null,
  projectionDiagnosticRunId = null,
  courtProjectionRunId = null,
  ballTrajectoryRunId = null,
  eventCandidateRunId = null,
  includeAnnotations = true
}: FetchReplayTimelineInput): Promise<ReplayTimeline> {
  const params = new URLSearchParams({
    media_id: mediaId,
    include_annotations: includeAnnotations ? "true" : "false"
  });
  if (detectionRunId !== null) {
    params.set("detection_run_id", detectionRunId);
  }
  if (trackletRunId !== null) {
    params.set("tracklet_run_id", trackletRunId);
  }
  if (poseRunId !== null) {
    params.set("pose_run_id", poseRunId);
  }
  if (mainPlayerTrackRunId !== null) {
    params.set("main_player_track_run_id", mainPlayerTrackRunId);
  }
  if (motionSmoothingRunId !== null) {
    params.set("motion_smoothing_run_id", motionSmoothingRunId);
  }
  if (courtRunId !== null) {
    params.set("court_run_id", courtRunId);
  }
  if (homographyRunId !== null) {
    params.set("homography_run_id", homographyRunId);
  }
  if (projectionDiagnosticRunId !== null) {
    params.set("projection_diagnostic_run_id", projectionDiagnosticRunId);
  }
  if (courtProjectionRunId !== null) {
    params.set("court_projection_run_id", courtProjectionRunId);
  }
  if (ballTrajectoryRunId !== null) {
    params.set("ball_trajectory_run_id", ballTrajectoryRunId);
  }
  if (eventCandidateRunId !== null) {
    params.set("event_candidate_run_id", eventCandidateRunId);
  }

  const response = await fetch(`/api/replay/timeline?${params.toString()}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load replay timeline: ${response.status}`);
  }

  return (await response.json()) as ReplayTimeline;
}

export async function fetchTrackletEvidenceBundle(
  trackletId: string
): Promise<TrackletEvidenceBundle> {
  const response = await fetch(`/api/tracklets/${trackletId}/evidence-bundle`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load tracklet evidence bundle ${trackletId}: ${response.status}`);
  }

  return (await response.json()) as TrackletEvidenceBundle;
}

export async function fetchEventCandidateReviews(
  mediaId: string,
  eventCandidateRunId: string
): Promise<EventCandidateReviewList> {
  const params = new URLSearchParams({ event_candidate_run_id: eventCandidateRunId });
  const response = await fetch(
    `/api/replay/${mediaId}/event-candidate-reviews?${params.toString()}`,
    { cache: "no-store" }
  );

  if (!response.ok) {
    throw new Error(`Unable to load event candidate reviews: ${response.status}`);
  }

  return (await response.json()) as EventCandidateReviewList;
}

export interface CreateEventCandidateReviewInput {
  event_candidate_run_id: string;
  observation_id?: string | null;
  annotation_kind: EventCandidateReviewKind;
  review_label: EventCandidateReviewLabel;
  candidate_type?: string | null;
  frame?: number | null;
  timestamp_ms?: number | null;
  image_x?: number | null;
  image_y?: number | null;
  court_x?: number | null;
  court_y?: number | null;
  note?: string | null;
  reviewer?: string | null;
  payload_jsonb?: JsonRecord;
}

export async function createEventCandidateReview(
  mediaId: string,
  input: CreateEventCandidateReviewInput
): Promise<EventCandidateReviewAnnotation> {
  const response = await fetch(`/api/replay/${mediaId}/event-candidate-reviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error(`Unable to create event candidate review: ${response.status}`);
  }

  return (await response.json()) as EventCandidateReviewAnnotation;
}

export async function updateEventCandidateReview(
  mediaId: string,
  reviewId: string,
  input: {
    review_label?: EventCandidateReviewLabel;
    note?: string | null;
    reviewer?: string | null;
    payload_jsonb?: JsonRecord;
  }
): Promise<EventCandidateReviewAnnotation> {
  const response = await fetch(`/api/replay/${mediaId}/event-candidate-reviews/${reviewId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error(`Unable to update event candidate review: ${response.status}`);
  }

  return (await response.json()) as EventCandidateReviewAnnotation;
}

export async function deleteEventCandidateReview(mediaId: string, reviewId: string): Promise<void> {
  const response = await fetch(`/api/replay/${mediaId}/event-candidate-reviews/${reviewId}`, {
    method: "DELETE"
  });

  if (!response.ok) {
    throw new Error(`Unable to delete event candidate review: ${response.status}`);
  }
}

export async function fetchTrajectory3DDebugReviews(
  mediaId: string,
  input: {
    trajectory3dRunId?: string | null;
    eventCandidateRunId?: string | null;
  }
): Promise<Trajectory3DDebugReviewList> {
  const params = new URLSearchParams();
  if (input.trajectory3dRunId !== undefined && input.trajectory3dRunId !== null) {
    params.set("trajectory3dRunId", input.trajectory3dRunId);
  }
  if (input.eventCandidateRunId !== undefined && input.eventCandidateRunId !== null) {
    params.set("eventCandidateRunId", input.eventCandidateRunId);
  }
  const response = await fetch(
    `/api/replay/${mediaId}/trajectory-3d-debug-reviews?${params.toString()}`,
    { cache: "no-store" }
  );

  if (!response.ok) {
    throw new Error(`Unable to load 3D debug reviews: ${response.status}`);
  }

  return (await response.json()) as Trajectory3DDebugReviewList;
}

export interface CreateTrajectory3DDebugReviewInput {
  trajectory_3d_run_id?: string | null;
  camera_geometry_id?: string | null;
  event_candidate_run_id?: string | null;
  event_observation_id?: string | null;
  trajectory_3d_candidate_id?: string | null;
  event_candidate_3d_diagnostic_id?: string | null;
  annotation_kind: Trajectory3DDebugReviewKind;
  review_label: Trajectory3DDebugReviewLabel;
  frame?: number | null;
  timestamp_ms?: number | null;
  image_x?: number | null;
  image_y?: number | null;
  court_x_m?: number | null;
  court_y_m?: number | null;
  court_z_m?: number | null;
  note?: string | null;
  reviewer?: string | null;
  payload_jsonb?: JsonRecord;
}

export async function createTrajectory3DDebugReview(
  mediaId: string,
  input: CreateTrajectory3DDebugReviewInput
): Promise<Trajectory3DDebugReviewAnnotation> {
  const response = await fetch(`/api/replay/${mediaId}/trajectory-3d-debug-reviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error(`Unable to create 3D debug review: ${response.status}`);
  }

  return (await response.json()) as Trajectory3DDebugReviewAnnotation;
}

export async function updateTrajectory3DDebugReview(
  mediaId: string,
  reviewId: string,
  input: {
    review_label?: Trajectory3DDebugReviewLabel;
    note?: string | null;
    reviewer?: string | null;
    payload_jsonb?: JsonRecord;
  }
): Promise<Trajectory3DDebugReviewAnnotation> {
  const response = await fetch(
    `/api/replay/${mediaId}/trajectory-3d-debug-reviews/${reviewId}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input)
    }
  );

  if (!response.ok) {
    throw new Error(`Unable to update 3D debug review: ${response.status}`);
  }

  return (await response.json()) as Trajectory3DDebugReviewAnnotation;
}

export interface CreateAnnotationInput {
  media_id?: string | null;
  observation_id?: string | null;
  evidence_artifact_id?: string | null;
  frame_start?: number | null;
  frame_end?: number | null;
  timestamp_start_ms?: number | null;
  timestamp_end_ms?: number | null;
  annotation_type: string;
  payload_jsonb?: JsonRecord;
  created_by?: string | null;
}

export async function createAnnotation(
  input: CreateAnnotationInput
): Promise<HumanAnnotation> {
  const response = await fetch("/api/annotations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error(`Unable to create annotation: ${response.status}`);
  }

  return (await response.json()) as HumanAnnotation;
}
