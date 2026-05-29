"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplaySmoothedBall,
  activeReplaySmoothedPlayerBoxes,
  activeReplaySmoothedPoses,
  imagePixelPointToOverlayPoint,
  imagePixelRectToOverlayRect,
  poseEdgeSideClass
} from "../lib/replayOverlays";
import type {
  ReplayInfo,
  ReplayOverlayDisplayMode,
  ReplayPoseKeypoint,
  ReplayPoseVisualStyle,
  ReplaySmoothedBallOverlay,
  ReplaySmoothedPlayerBoxOverlay,
  ReplaySmoothedPoseOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplaySmoothedMotionOverlayProps {
  replayInfo: ReplayInfo;
  smoothedBall: ReplaySmoothedBallOverlay[];
  smoothedPlayerBoxes: ReplaySmoothedPlayerBoxOverlay[];
  smoothedPoses: ReplaySmoothedPoseOverlay[];
  currentTimestampMs: number;
  currentFrame: number;
  enabledBall: boolean;
  enabledPlayerBoxes: boolean;
  enabledPoses: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  displayMode?: ReplayOverlayDisplayMode;
  poseVisualStyle?: ReplayPoseVisualStyle;
  onSelectSmoothedBall: (item: ReplaySmoothedBallOverlay) => void;
  onSelectSmoothedPlayerBox: (item: ReplaySmoothedPlayerBoxOverlay) => void;
  onSelectSmoothedPose: (item: ReplaySmoothedPoseOverlay) => void;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

interface ScaledKeypoint {
  keypoint: ReplayPoseKeypoint;
  x: number;
  y: number;
}

export function ReplaySmoothedMotionOverlay({
  replayInfo,
  smoothedBall,
  smoothedPlayerBoxes,
  smoothedPoses,
  currentTimestampMs,
  currentFrame,
  enabledBall,
  enabledPlayerBoxes,
  enabledPoses,
  isLoading,
  error,
  selectedObservationId,
  displayMode = "current_only",
  poseVisualStyle = "limbs_only",
  onSelectSmoothedBall,
  onSelectSmoothedPlayerBox,
  onSelectSmoothedPose,
  holdMs = 125
}: ReplaySmoothedMotionOverlayProps) {
  const overlayRef = useRef<HTMLDivElement | null>(null);
  const [overlaySize, setOverlaySize] = useState<OverlaySize>({ width: 0, height: 0 });

  useEffect(() => {
    const overlay = overlayRef.current;
    if (overlay === null) {
      return;
    }
    const updateSize = () => {
      const rect = overlay.getBoundingClientRect();
      setOverlaySize({ width: rect.width, height: rect.height });
    };
    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(overlay);
    return () => observer.disconnect();
  }, []);

  const activeBall = useMemo(
    () =>
      activeReplaySmoothedBall(
        smoothedBall,
        currentTimestampMs,
        currentFrame,
        holdMs,
        displayMode
      ),
    [currentFrame, currentTimestampMs, displayMode, holdMs, smoothedBall]
  );
  const activeBoxes = useMemo(
    () =>
      activeReplaySmoothedPlayerBoxes(
        smoothedPlayerBoxes,
        currentTimestampMs,
        currentFrame,
        holdMs,
        displayMode
      ),
    [currentFrame, currentTimestampMs, displayMode, holdMs, smoothedPlayerBoxes]
  );
  const activePoses = useMemo(
    () =>
      activeReplaySmoothedPoses(
        smoothedPoses,
        currentTimestampMs,
        currentFrame,
        holdMs,
        displayMode
      ),
    [currentFrame, currentTimestampMs, displayMode, holdMs, smoothedPoses]
  );
  const labelBallIds = useMemo(
    () =>
      new Set(
        activeReplaySmoothedBall(
          smoothedBall,
          currentTimestampMs,
          currentFrame,
          holdMs,
          "current_only"
        ).map((item) => item.observation_id)
      ),
    [currentFrame, currentTimestampMs, holdMs, smoothedBall]
  );
  const labelBoxIds = useMemo(
    () =>
      new Set(
        activeReplaySmoothedPlayerBoxes(
          smoothedPlayerBoxes,
          currentTimestampMs,
          currentFrame,
          holdMs,
          "current_only"
        ).map((item) => item.observation_id)
      ),
    [currentFrame, currentTimestampMs, holdMs, smoothedPlayerBoxes]
  );
  const enabled = enabledBall || enabledPlayerBoxes || enabledPoses;
  const totalCount = smoothedBall.length + smoothedPlayerBoxes.length + smoothedPoses.length;
  const activeCount = activeBall.length + activeBoxes.length + activePoses.length;
  const status = overlayStatus({ enabled, isLoading, error, activeCount, totalCount });

  return (
    <div className="replay-overlay-layer" ref={overlayRef}>
      {enabled ? (
        <svg className="replay-vector-layer" role="presentation">
          {enabledPlayerBoxes
            ? activeBoxes.map((item) => {
                const rect = imagePixelRectToOverlayRect(
                  item.bbox,
                  replayInfo.width,
                  replayInfo.height,
                  overlaySize.width,
                  overlaySize.height
                );
                if (rect === null) {
                  return null;
                }
                const selected = selectedObservationId === item.observation_id;
                const roleClass =
                  item.track_role_candidate === "near_player_track_candidate" ? "near" : "far";
                return (
                  <g
                    className={`replay-smoothed-box ${roleClass}${selected ? " selected" : ""}`}
                    key={item.observation_id}
                    onClick={(event) => {
                      event.stopPropagation();
                      onSelectSmoothedPlayerBox(item);
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onSelectSmoothedPlayerBox(item);
                      }
                    }}
                    role="button"
                    tabIndex={0}
                  >
                    <rect height={rect.height} width={rect.width} x={rect.x} y={rect.y} />
                    {displayMode === "current_only" || labelBoxIds.has(item.observation_id) ? (
                      <text x={rect.x} y={Math.max(14, rect.y - 8)}>
                        {item.track_role_candidate === "near_player_track_candidate"
                          ? "SMOOTH NEAR"
                          : "SMOOTH FAR"}
                      </text>
                    ) : null}
                  </g>
                );
              })
            : null}
          {enabledPoses
            ? activePoses.map((pose) => {
                const scaledKeypoints = scalePoseKeypoints(pose, replayInfo, overlaySize);
                const byName = new Map(
                  scaledKeypoints.map((keypoint) => [keypoint.keypoint.name, keypoint])
                );
                const selected = selectedObservationId === pose.observation_id;
                const showLimbs = poseVisualStyle !== "joints_only";
                const showJoints = poseVisualStyle !== "limbs_only";
                return (
                  <g
                    aria-label={`smoothed pose candidate ${formatConfidence(
                      pose.pose_confidence
                    )} frame ${pose.frame_number}`}
                    className={`replay-smoothed-pose${selected ? " selected" : ""}`}
                    key={pose.observation_id}
                    onClick={(event) => {
                      event.stopPropagation();
                      onSelectSmoothedPose(pose);
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onSelectSmoothedPose(pose);
                      }
                    }}
                    role="button"
                    tabIndex={0}
                  >
                    {showLimbs
                      ? pose.edges.map(([start, end]) => {
                          const startPoint = byName.get(start);
                          const endPoint = byName.get(end);
                          if (startPoint === undefined || endPoint === undefined) {
                            return null;
                          }
                          return (
                            <line
                              className={`replay-smoothed-pose-edge pose-limb-${poseEdgeSideClass(start, end)}`}
                              key={`${pose.observation_id}:${start}:${end}`}
                              x1={startPoint.x}
                              x2={endPoint.x}
                              y1={startPoint.y}
                              y2={endPoint.y}
                            />
                          );
                        })
                      : null}
                    {showJoints
                      ? scaledKeypoints.map((keypoint) => (
                          <circle
                            cx={keypoint.x}
                            cy={keypoint.y}
                            key={`${pose.observation_id}:${keypoint.keypoint.index}`}
                            r={selected ? 5 : 4}
                          />
                        ))
                      : null}
                  </g>
                );
              })
            : null}
          {enabledBall
            ? activeBall.map((item) => {
                const point = imagePixelPointToOverlayPoint(
                  item.x,
                  item.y,
                  replayInfo.width,
                  replayInfo.height,
                  overlaySize.width,
                  overlaySize.height
                );
                if (point === null) {
                  return null;
                }
                const selected = selectedObservationId === item.observation_id;
                return (
                  <g
                    aria-label={`smoothed ball position candidate ${formatConfidence(
                      item.confidence
                    )} frame ${item.frame_number}`}
                    className={`replay-smoothed-ball${selected ? " selected" : ""}`}
                    key={item.observation_id}
                    onClick={(event) => {
                      event.stopPropagation();
                      onSelectSmoothedBall(item);
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onSelectSmoothedBall(item);
                      }
                    }}
                    role="button"
                    tabIndex={0}
                  >
                    <circle cx={point.x} cy={point.y} r={selected ? 9 : 7} />
                    {displayMode === "current_only" || labelBallIds.has(item.observation_id) ? (
                      <text x={point.x + 10} y={point.y - 8}>
                        SMOOTH BALL
                      </text>
                    ) : null}
                  </g>
                );
              })
            : null}
        </svg>
      ) : null}
      {status !== null ? <div className="replay-overlay-status smoothed-motion">{status}</div> : null}
    </div>
  );
}

function scalePoseKeypoints(
  pose: ReplaySmoothedPoseOverlay,
  replayInfo: ReplayInfo,
  overlaySize: OverlaySize
): ScaledKeypoint[] {
  return pose.keypoints
    .filter(
      (keypoint) =>
        keypoint.present &&
        typeof keypoint.x === "number" &&
        typeof keypoint.y === "number"
    )
    .map((keypoint) => {
      const scaled = imagePixelPointToOverlayPoint(
        keypoint.x as number,
        keypoint.y as number,
        replayInfo.width,
        replayInfo.height,
        overlaySize.width,
        overlaySize.height
      );
      return scaled === null ? null : { keypoint, ...scaled };
    })
    .filter((keypoint): keypoint is ScaledKeypoint => keypoint !== null);
}

function overlayStatus({
  enabled,
  isLoading,
  error,
  activeCount,
  totalCount
}: {
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  activeCount: number;
  totalCount: number;
}): string | null {
  if (!enabled) {
    return "Smoothed motion layer hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading smoothed motion candidates...";
  }
  if (totalCount === 0) {
    return "No smoothed motion candidates in this time window.";
  }
  if (activeCount === 0) {
    return "No smoothed motion candidates at the current timestamp.";
  }
  return null;
}
