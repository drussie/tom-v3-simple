import type {
  HomographyMatrix3x3,
  ReplayCameraViewOverlay,
  ReplayCourtKeypointOverlay,
  ReplayCourtLineOverlay,
  ReplayDetectionBBox,
  ReplayDetectionOverlay,
  ReplayHomographyCandidateOverlay,
  ReplayMainPlayerTrackOverlay,
  ReplayPoseOverlay,
  ReplayProjectionDiagnosticOverlay,
  ReplayOverlayDisplayMode,
  ReplayRunSummary,
  ReplaySmoothedBallOverlay,
  ReplaySmoothedPlayerBoxOverlay,
  ReplaySmoothedPoseOverlay,
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

export interface TemplateProjectionPoint extends OverlayPoint {
  valid: boolean;
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
  holdMs = 250,
  displayMode: ReplayOverlayDisplayMode = "short_trail"
): ReplayDetectionOverlay[] {
  if (displayMode === "full_trail") {
    return detections;
  }
  if (displayMode === "current_only") {
    const currentFrameDetections = detections.filter(
      (detection) => detection.frame_number === currentFrame
    );
    if (currentFrameDetections.length > 0) {
      return currentFrameDetections;
    }
    return detections.filter(
      (detection) => Math.abs(detection.timestamp_ms - currentTimestampMs) <= 34
    );
  }
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
  holdMs = 250,
  displayMode: ReplayOverlayDisplayMode = "short_trail"
): ReplayTrackletOverlay[] {
  if (displayMode === "full_trail") {
    return tracklets;
  }
  return tracklets.filter((tracklet) => {
    return tracklet.points.some((point) =>
      isActiveReplayPointForDisplay(
        point.timestamp_ms,
        point.frame_number,
        currentTimestampMs,
        currentFrame,
        holdMs,
        displayMode
      )
    );
  });
}

export function activeReplayTrackPoints(
  points: ReplayTrackPointOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250,
  displayMode: ReplayOverlayDisplayMode = "short_trail"
): ReplayTrackPointOverlay[] {
  if (displayMode === "full_trail") {
    return points;
  }
  return points.filter((point) =>
    isActiveReplayPointForDisplay(
      point.timestamp_ms,
      point.frame_number,
      currentTimestampMs,
      currentFrame,
      holdMs,
      displayMode
    )
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

export function activeReplayMainPlayerTracks(
  tracks: ReplayMainPlayerTrackOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayMainPlayerTrackOverlay[] {
  return tracks.filter((track) =>
    isActiveReplayPoint(track.timestamp_ms, track.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

export function activeReplayCourtKeypoints(
  keypoints: ReplayCourtKeypointOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayCourtKeypointOverlay[] {
  return activeReplayCourtEvidence(keypoints, currentTimestampMs, currentFrame, holdMs);
}

export function activeReplayCourtLines(
  lines: ReplayCourtLineOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayCourtLineOverlay[] {
  return activeReplayCourtEvidence(lines, currentTimestampMs, currentFrame, holdMs);
}

export function activeReplayCameraViews(
  cameraViews: ReplayCameraViewOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayCameraViewOverlay[] {
  return cameraViews.filter((item) => {
    const startMs = item.timestamp_start_ms ?? item.timestamp_ms;
    const endMs = item.timestamp_end_ms ?? item.timestamp_ms;
    if (currentTimestampMs >= startMs - holdMs && currentTimestampMs <= endMs + holdMs) {
      return true;
    }
    return isActiveReplayPoint(item.timestamp_ms, item.frame_number, currentTimestampMs, currentFrame, holdMs);
  });
}

export function activeReplayHomographyCandidates(
  homographies: ReplayHomographyCandidateOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayHomographyCandidateOverlay[] {
  return activeReplayCourtEvidence(homographies, currentTimestampMs, currentFrame, holdMs);
}

export function activeReplayProjectionDiagnostics(
  diagnostics: ReplayProjectionDiagnosticOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 250
): ReplayProjectionDiagnosticOverlay[] {
  return activeReplayCourtEvidence(diagnostics, currentTimestampMs, currentFrame, holdMs);
}

export function activeReplaySmoothedBall(
  items: ReplaySmoothedBallOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 125
): ReplaySmoothedBallOverlay[] {
  return items.filter((item) =>
    isActiveReplayPoint(item.timestamp_ms, item.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

export function activeReplaySmoothedPlayerBoxes(
  items: ReplaySmoothedPlayerBoxOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 125
): ReplaySmoothedPlayerBoxOverlay[] {
  return items.filter((item) =>
    isActiveReplayPoint(item.timestamp_ms, item.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

export function activeReplaySmoothedPoses(
  items: ReplaySmoothedPoseOverlay[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs = 125
): ReplaySmoothedPoseOverlay[] {
  return items.filter((item) =>
    isActiveReplayPoint(item.timestamp_ms, item.frame_number, currentTimestampMs, currentFrame, holdMs)
  );
}

function activeReplayCourtEvidence<
  T extends {
    timestamp_ms: number;
    frame_number: number;
    temporal_display_mode?: string;
    active_from_ms?: number | null;
    active_until_ms?: number | null;
    carried_forward?: boolean;
    current_replay_timestamp_ms?: number | null;
  }
>(
  items: T[],
  currentTimestampMs: number,
  currentFrame: number,
  holdMs: number
): T[] {
  return items
    .filter((item) => {
      if (
        item.temporal_display_mode === "carry_forward" &&
        typeof item.active_from_ms === "number" &&
        typeof item.active_until_ms === "number"
      ) {
        return (
          currentTimestampMs >= item.active_from_ms &&
          currentTimestampMs <= item.active_until_ms
        );
      }
      return isActiveReplayPoint(
        item.timestamp_ms,
        item.frame_number,
        currentTimestampMs,
        currentFrame,
        holdMs
      );
    })
    .map((item) => {
      if (
        item.temporal_display_mode !== "carry_forward" ||
        typeof item.active_from_ms !== "number" ||
        typeof item.active_until_ms !== "number"
      ) {
        return item;
      }
      const isAtSourceTime =
        item.frame_number === currentFrame ||
        Math.abs(item.timestamp_ms - currentTimestampMs) <= Math.max(holdMs, 34);
      return {
        ...item,
        carried_forward: !isAtSourceTime,
        current_replay_timestamp_ms: currentTimestampMs
      };
    });
}

export function isActiveReplayPointForDisplay(
  timestampMs: number,
  frameNumber: number,
  currentTimestampMs: number,
  currentFrame: number,
  holdMs: number,
  displayMode: ReplayOverlayDisplayMode
): boolean {
  if (displayMode === "full_trail") {
    return true;
  }
  if (displayMode === "current_only") {
    return frameNumber === currentFrame || Math.abs(timestampMs - currentTimestampMs) <= 34;
  }
  return isActiveReplayPoint(timestampMs, frameNumber, currentTimestampMs, currentFrame, holdMs);
}

export function filterDetectionsAvailableAt(
  detections: ReplayDetectionOverlay[],
  availableUntilMs: number | null
): ReplayDetectionOverlay[] {
  if (availableUntilMs === null) {
    return detections;
  }
  return detections.filter((detection) => detection.timestamp_ms <= availableUntilMs);
}

export function filterTrackletsAvailableAt(
  tracklets: ReplayTrackletOverlay[],
  availableUntilMs: number | null
): ReplayTrackletOverlay[] {
  if (availableUntilMs === null) {
    return tracklets;
  }
  return tracklets
    .map((tracklet) => {
      const points = tracklet.points.filter((point) => point.timestamp_ms <= availableUntilMs);
      if (points.length === 0) {
        return null;
      }
      const timestampEndMs = Math.min(tracklet.timestamp_end_ms, availableUntilMs);
      return {
        ...tracklet,
        timestamp_end_ms: Math.max(tracklet.timestamp_start_ms, timestampEndMs),
        points
      };
    })
    .filter((tracklet): tracklet is ReplayTrackletOverlay => tracklet !== null);
}

export function filterPosesAvailableAt(
  poses: ReplayPoseOverlay[],
  availableUntilMs: number | null
): ReplayPoseOverlay[] {
  if (availableUntilMs === null) {
    return poses;
  }
  return poses.filter((pose) => pose.timestamp_ms <= availableUntilMs);
}

export function filterMainPlayerTracksAvailableAt(
  tracks: ReplayMainPlayerTrackOverlay[],
  availableUntilMs: number | null
): ReplayMainPlayerTrackOverlay[] {
  if (availableUntilMs === null) {
    return tracks;
  }
  return tracks.filter((track) => track.timestamp_ms <= availableUntilMs);
}

export function filterCourtKeypointsAvailableAt(
  keypoints: ReplayCourtKeypointOverlay[],
  availableUntilMs: number | null
): ReplayCourtKeypointOverlay[] {
  if (availableUntilMs === null) {
    return keypoints;
  }
  return keypoints.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterCourtLinesAvailableAt(
  lines: ReplayCourtLineOverlay[],
  availableUntilMs: number | null
): ReplayCourtLineOverlay[] {
  if (availableUntilMs === null) {
    return lines;
  }
  return lines.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterCameraViewsAvailableAt(
  cameraViews: ReplayCameraViewOverlay[],
  availableUntilMs: number | null
): ReplayCameraViewOverlay[] {
  if (availableUntilMs === null) {
    return cameraViews;
  }
  return cameraViews.filter((item) => (item.timestamp_start_ms ?? item.timestamp_ms) <= availableUntilMs);
}

export function filterHomographyCandidatesAvailableAt(
  homographies: ReplayHomographyCandidateOverlay[],
  availableUntilMs: number | null
): ReplayHomographyCandidateOverlay[] {
  if (availableUntilMs === null) {
    return homographies;
  }
  return homographies.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterProjectionDiagnosticsAvailableAt(
  diagnostics: ReplayProjectionDiagnosticOverlay[],
  availableUntilMs: number | null
): ReplayProjectionDiagnosticOverlay[] {
  if (availableUntilMs === null) {
    return diagnostics;
  }
  return diagnostics.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterSmoothedBallAvailableAt(
  items: ReplaySmoothedBallOverlay[],
  availableUntilMs: number | null
): ReplaySmoothedBallOverlay[] {
  if (availableUntilMs === null) {
    return items;
  }
  return items.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterSmoothedPlayerBoxesAvailableAt(
  items: ReplaySmoothedPlayerBoxOverlay[],
  availableUntilMs: number | null
): ReplaySmoothedPlayerBoxOverlay[] {
  if (availableUntilMs === null) {
    return items;
  }
  return items.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function filterSmoothedPosesAvailableAt(
  items: ReplaySmoothedPoseOverlay[],
  availableUntilMs: number | null
): ReplaySmoothedPoseOverlay[] {
  if (availableUntilMs === null) {
    return items;
  }
  return items.filter((item) => item.timestamp_ms <= availableUntilMs);
}

export function projectTemplatePointWithMatrix(
  matrix: HomographyMatrix3x3 | null,
  x: number,
  y: number
): TemplateProjectionPoint | null {
  if (matrix === null) {
    return null;
  }
  const w = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2];
  if (!Number.isFinite(w) || Math.abs(w) < 1e-9) {
    return null;
  }
  const projectedX = (matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]) / w;
  const projectedY = (matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]) / w;
  if (!Number.isFinite(projectedX) || !Number.isFinite(projectedY)) {
    return null;
  }
  return { x: projectedX, y: projectedY, valid: true };
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
  if (requestedRunId !== undefined && requestedRunId.trim() !== "") {
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
