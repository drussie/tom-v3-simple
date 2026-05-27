import type {
  ReplayDetectionBBox,
  ReplayDetectionOverlay,
  ReplayPoseOverlay,
  ReplayRunSummary,
  ReplayTrackletOverlay,
  ReplayTrackPointOverlay
} from "./types";

export interface ContainedMediaRect {
  x: number;
  y: number;
  width: number;
  height: number;
  scaleX: number;
  scaleY: number;
}

export interface OverlayRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface OverlayPoint {
  x: number;
  y: number;
}

export function computeContainedMediaRect(
  containerWidth: number,
  containerHeight: number,
  mediaWidth: number | null,
  mediaHeight: number | null
): ContainedMediaRect | null {
  if (
    containerWidth <= 0 ||
    containerHeight <= 0 ||
    mediaWidth === null ||
    mediaHeight === null ||
    mediaWidth <= 0 ||
    mediaHeight <= 0
  ) {
    return null;
  }

  const scale = Math.min(containerWidth / mediaWidth, containerHeight / mediaHeight);
  const width = mediaWidth * scale;
  const height = mediaHeight * scale;
  return {
    x: (containerWidth - width) / 2,
    y: (containerHeight - height) / 2,
    width,
    height,
    scaleX: scale,
    scaleY: scale
  };
}

export function imagePixelRectToOverlayRect(
  bbox: ReplayDetectionBBox,
  mediaWidth: number | null,
  mediaHeight: number | null,
  overlayWidth: number,
  overlayHeight: number
): OverlayRect | null {
  const contained = computeContainedMediaRect(overlayWidth, overlayHeight, mediaWidth, mediaHeight);
  if (contained === null) {
    return null;
  }
  return {
    x: contained.x + bbox.x * contained.scaleX,
    y: contained.y + bbox.y * contained.scaleY,
    width: bbox.w * contained.scaleX,
    height: bbox.h * contained.scaleY
  };
}

export function imagePixelPointToOverlayPoint(
  x: number,
  y: number,
  mediaWidth: number | null,
  mediaHeight: number | null,
  overlayWidth: number,
  overlayHeight: number
): OverlayPoint | null {
  const contained = computeContainedMediaRect(overlayWidth, overlayHeight, mediaWidth, mediaHeight);
  if (contained === null) {
    return null;
  }
  return {
    x: contained.x + x * contained.scaleX,
    y: contained.y + y * contained.scaleY
  };
}

export function activeReplayDetections(
  detections: ReplayDetectionOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayDetectionOverlay[] {
  return detections.filter((detection) => {
    const timestampDelta = Math.abs(detection.timestamp_ms - currentTimestampMs);
    if (timestampDelta <= holdMs) {
      return true;
    }
    return detection.frame_number === currentFrame && timestampDelta <= Math.max(holdMs, 34);
  });
}

export function activeReplayTracklets(
  tracklets: ReplayTrackletOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayTrackletOverlay[] {
  return tracklets.filter((tracklet) => {
    if (
      currentTimestampMs >= tracklet.timestamp_start_ms - holdMs &&
      currentTimestampMs <= tracklet.timestamp_end_ms + holdMs
    ) {
      return true;
    }
    return tracklet.points.some((point) =>
      isActiveReplayPoint(point.timestamp_ms, point.frame_number, currentTimestampMs, currentFrame, holdMs)
    );
  });
}

export function activeReplayTrackPoints(
  points: ReplayTrackPointOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayTrackPointOverlay[] {
  return points.filter((point) =>
    isActiveReplayPoint(point.timestamp_ms, point.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

export function activeReplayPoses(
  poses: ReplayPoseOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayPoseOverlay[] {
  return poses.filter((pose) =>
    isActiveReplayPoint(pose.timestamp_ms, pose.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

export function selectInitialDetectionRun(
  runs: ReplayRunSummary[],
  requestedRunId?: string
): string | null {
  return selectInitialReplayRun(runs, requestedRunId);
}

export function selectInitialReplayRun(
  runs: ReplayRunSummary[],
  requestedRunId?: string
): string | null {
  if (requestedRunId !== undefined && runs.some((run) => run.run_id === requestedRunId)) {
    return requestedRunId;
  }
  return runs.length === 1 ? runs[0].run_id : null;
}

function isActiveReplayPoint(
  timestampMs: number,
  frameNumber: number,
  currentTimestampMs: number,
  currentFrame: number,
  holdMs: number
): boolean {
  const timestampDelta = Math.abs(timestampMs - currentTimestampMs);
  if (timestampDelta <= holdMs) {
    return true;
  }
  return frameNumber === currentFrame && timestampDelta <= Math.max(holdMs, 34);
}
