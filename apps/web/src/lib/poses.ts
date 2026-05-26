import type {
  MediaAsset,
  Observation,
  PoseBBox,
  PoseConfidenceBand,
  PoseKeypoint,
  PoseOverlayEdge,
  PoseOverlayItem,
  PoseOverlayKeypoint,
  PoseOverlayModel
} from "./types";

export const coco17SkeletonEdges: Array<[string, string]> = [
  ["nose", "left_eye"],
  ["nose", "right_eye"],
  ["left_eye", "left_ear"],
  ["right_eye", "right_ear"],
  ["left_shoulder", "right_shoulder"],
  ["left_shoulder", "left_elbow"],
  ["left_elbow", "left_wrist"],
  ["right_shoulder", "right_elbow"],
  ["right_elbow", "right_wrist"],
  ["left_shoulder", "left_hip"],
  ["right_shoulder", "right_hip"],
  ["left_hip", "right_hip"],
  ["left_hip", "left_knee"],
  ["left_knee", "left_ankle"],
  ["right_hip", "right_knee"],
  ["right_knee", "right_ankle"]
];

export function buildPoseOverlayModel(
  media: MediaAsset | null,
  observations: Observation[],
  selectedObservationId: string | null
): PoseOverlayModel {
  const items = extractPoseOverlayItems(observations);
  const selectedFrame = selectPoseFrame(items, observations, selectedObservationId);
  const frameItems =
    selectedFrame === null ? [] : items.filter((item) => item.frameNumber === selectedFrame);
  const markedItems = markSelected(items, selectedObservationId);
  const markedFrameItems = markSelected(frameItems, selectedObservationId);
  const selectedPoseItem =
    markedFrameItems.find((item) => item.isSelected) ?? markedFrameItems[0] ?? null;
  const mediaWidth = validDimension(media?.width) ? media?.width ?? null : null;
  const mediaHeight = validDimension(media?.height) ? media?.height ?? null : null;

  return {
    items: markedItems,
    frameItems: markedFrameItems,
    selectedFrame,
    selectedPoseItem,
    unavailableReason: unavailableReason(mediaWidth, mediaHeight, items),
    mediaWidth,
    mediaHeight
  };
}

export function extractPoseOverlayItems(observations: Observation[]): PoseOverlayItem[] {
  const items: PoseOverlayItem[] = [];

  for (const observation of observations) {
    if (!isPoseObservation(observation) || observation.pose === null) {
      continue;
    }

    const pose = observation.pose;
    const keypoints = pose.keypoints_jsonb;
    const presentKeypoints = presentPoseKeypoints(keypoints);
    const missingKeypoints = keypoints.filter((keypoint) => !isPresentKeypoint(keypoint));
    const frameNumber = pose.frame_number ?? observation.frame_start ?? observation.frame_end;
    if (typeof frameNumber !== "number") {
      continue;
    }

    items.push({
      id: observation.id,
      observationId: observation.id,
      frameNumber,
      timestampMs: pose.timestamp_ms ?? observation.timestamp_start_ms,
      skeletonFormat: pose.skeleton_format,
      skeletonVersion: pose.skeleton_version,
      poseConfidence: pose.pose_confidence ?? observation.confidence,
      bbox: extractPoseBBox(observation),
      keypoints,
      presentKeypoints,
      missingKeypoints,
      edges: poseSkeletonEdges(presentKeypoints),
      keypointCount: pose.keypoint_count,
      keypointsPresentCount: pose.keypoints_present_count,
      keypointsMissingCount: pose.keypoints_missing_count,
      meanKeypointConfidence: pose.mean_keypoint_confidence,
      minKeypointConfidence: pose.min_keypoint_confidence,
      maxKeypointConfidence: pose.max_keypoint_confidence,
      subjectRefType: pose.subject_ref_type,
      subjectDetectionObservationId: pose.subject_detection_observation_id,
      subjectTrackletId: pose.subject_tracklet_id,
      subjectTrackPointId: pose.subject_track_point_id,
      associationStatus: pose.association_status,
      associationMethod: pose.association_method,
      associationConfidence: pose.association_confidence,
      frameTimeOwner: pose.frame_time_owner,
      metadata: pose.metadata_jsonb,
      isSelected: false
    });
  }

  return items.sort((left, right) => {
    const frameDelta = left.frameNumber - right.frameNumber;
    if (frameDelta !== 0) {
      return frameDelta;
    }
    return left.observationId.localeCompare(right.observationId);
  });
}

export function presentPoseKeypoints(keypoints: PoseKeypoint[]): PoseOverlayKeypoint[] {
  return keypoints
    .filter(isPresentKeypoint)
    .map((keypoint) => ({
      ...keypoint,
      confidenceBand: confidenceBand(keypoint.confidence)
    }));
}

export function poseSkeletonEdges(keypoints: PoseOverlayKeypoint[]): PoseOverlayEdge[] {
  const byName = new Map(keypoints.map((keypoint) => [keypoint.name, keypoint]));
  return coco17SkeletonEdges.flatMap(([startName, endName]) => {
    const start = byName.get(startName);
    const end = byName.get(endName);
    if (start === undefined || end === undefined) {
      return [];
    }
    return [
      {
        id: `${startName}:${endName}`,
        start,
        end
      }
    ];
  });
}

export function pointToPercent(value: number, dimension: number): number {
  return Math.max(0, Math.min(100, (value / dimension) * 100));
}

export function confidenceBand(confidence: number | null): PoseConfidenceBand {
  if (confidence === null || !Number.isFinite(confidence)) {
    return "unknown";
  }
  return confidence < 0.35 ? "low" : "normal";
}

function isPoseObservation(observation: Observation): boolean {
  return (
    observation.observation_family === "pose" &&
    observation.observation_type === "player_pose_observation"
  );
}

function isPresentKeypoint(keypoint: PoseKeypoint): keypoint is PoseOverlayKeypoint {
  return (
    keypoint.present === true &&
    typeof keypoint.x === "number" &&
    Number.isFinite(keypoint.x) &&
    typeof keypoint.y === "number" &&
    Number.isFinite(keypoint.y)
  );
}

function extractPoseBBox(observation: Observation): PoseBBox | null {
  const pose = observation.pose;
  if (pose === null) {
    return null;
  }
  const x = pose.bbox_x;
  const y = pose.bbox_y;
  const width = pose.bbox_w;
  const height = pose.bbox_h;
  if (
    typeof x !== "number" ||
    typeof y !== "number" ||
    typeof width !== "number" ||
    typeof height !== "number" ||
    !Number.isFinite(x) ||
    !Number.isFinite(y) ||
    !Number.isFinite(width) ||
    !Number.isFinite(height) ||
    width <= 0 ||
    height <= 0
  ) {
    return null;
  }
  return {
    x,
    y,
    width,
    height,
    confidence: pose.bbox_confidence
  };
}

function selectPoseFrame(
  items: PoseOverlayItem[],
  observations: Observation[],
  selectedObservationId: string | null
): number | null {
  if (selectedObservationId !== null) {
    const selectedObservation = observations.find(
      (observation) => observation.id === selectedObservationId
    );
    if (selectedObservation !== undefined) {
      const selectedFrame = selectedObservation.frame_start ?? selectedObservation.frame_end;
      if (
        typeof selectedFrame === "number" &&
        items.some((item) => item.frameNumber === selectedFrame)
      ) {
        return selectedFrame;
      }
    }
  }

  return items[0]?.frameNumber ?? null;
}

function markSelected(
  items: PoseOverlayItem[],
  selectedObservationId: string | null
): PoseOverlayItem[] {
  return items.map((item) => ({
    ...item,
    isSelected: item.observationId === selectedObservationId
  }));
}

function unavailableReason(
  mediaWidth: number | null,
  mediaHeight: number | null,
  items: PoseOverlayItem[]
): string | null {
  if (mediaWidth === null || mediaHeight === null) {
    return "Media dimensions are unavailable, so image-pixel pose evidence cannot be scaled.";
  }
  if (items.length === 0) {
    return "No persisted pose observations are available for this run.";
  }
  return null;
}

function validDimension(value: unknown): boolean {
  return typeof value === "number" && Number.isFinite(value) && value > 0;
}
