"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayPoses,
  imagePixelPointToOverlayPoint,
  imagePixelRectToOverlayRect,
  poseEdgeSideClass
} from "../lib/replayOverlays";
import type {
  ReplayInfo,
  ReplayPoseKeypoint,
  ReplayPoseOverlay as ReplayPoseOverlayItem,
  ReplayPoseVisualStyle
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayPoseOverlayProps {
  replayInfo: ReplayInfo;
  poses: ReplayPoseOverlayItem[];
  currentTimestampMs: number;
  currentFrame: number;
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  poseVisualStyle?: ReplayPoseVisualStyle;
  onSelectPose: (pose: ReplayPoseOverlayItem) => void;
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

export function ReplayPoseOverlay({
  replayInfo,
  poses,
  currentTimestampMs,
  currentFrame,
  enabled,
  isLoading,
  error,
  selectedObservationId,
  poseVisualStyle = "limbs_only",
  onSelectPose,
  holdMs = 250
}: ReplayPoseOverlayProps) {
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

  const activePoses = useMemo(
    () => activeReplayPoses(poses, currentTimestampMs, currentFrame, holdMs),
    [currentFrame, currentTimestampMs, holdMs, poses]
  );

  const status = overlayStatus({
    enabled,
    isLoading,
    error,
    activeCount: activePoses.length,
    totalCount: poses.length
  });

  return (
    <div className="replay-overlay-layer" ref={overlayRef}>
      {enabled ? (
        <svg className="replay-vector-layer" role="presentation">
          {activePoses.map((pose) => {
            const scaledKeypoints = scalePoseKeypoints(pose, replayInfo, overlaySize);
            const byName = new Map(scaledKeypoints.map((keypoint) => [keypoint.keypoint.name, keypoint]));
            const selected = pose.observation_id === selectedObservationId;
            const showLimbs = poseVisualStyle !== "joints_only";
            const showJoints = poseVisualStyle !== "limbs_only";
            const bbox = pose.bbox
              ? imagePixelRectToOverlayRect(
                  pose.bbox,
                  replayInfo.width,
                  replayInfo.height,
                  overlaySize.width,
                  overlaySize.height
                )
              : null;
            return (
              <g
                aria-label={`pose observation ${formatConfidence(
                  pose.pose_confidence
                )} frame ${pose.frame_number}`}
                className={`replay-pose-group${selected ? " selected" : ""}`}
                key={pose.observation_id}
                onClick={(event) => {
                  event.stopPropagation();
                  onSelectPose(pose);
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    onSelectPose(pose);
                  }
                }}
                role="button"
                tabIndex={0}
              >
                {bbox !== null ? (
                  <rect
                    className="replay-pose-bbox"
                    height={bbox.height}
                    width={bbox.width}
                    x={bbox.x}
                    y={bbox.y}
                  />
                ) : null}
                {showLimbs
                  ? pose.edges.map(([start, end]) => {
                      const startPoint = byName.get(start);
                      const endPoint = byName.get(end);
                      if (startPoint === undefined || endPoint === undefined) {
                        return null;
                      }
                      return (
                        <line
                          className={`replay-pose-edge pose-limb-${poseEdgeSideClass(start, end)}`}
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
                        className={keypointClassName(keypoint.keypoint)}
                        cx={keypoint.x}
                        cy={keypoint.y}
                        key={`${pose.observation_id}:${keypoint.keypoint.index}`}
                        r={selected ? 5 : 4}
                      />
                    ))
                  : null}
                {bbox !== null ? (
                  <text className="replay-pose-label" x={bbox.x} y={Math.max(14, bbox.y - 8)}>
                    pose evidence {formatConfidence(pose.pose_confidence)}
                  </text>
                ) : null}
              </g>
            );
          })}
        </svg>
      ) : null}
      {status !== null ? <div className="replay-overlay-status pose">{status}</div> : null}
    </div>
  );
}

function scalePoseKeypoints(
  pose: ReplayPoseOverlayItem,
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

function keypointClassName(keypoint: ReplayPoseKeypoint): string {
  if (keypoint.confidence === null) {
    return "replay-pose-keypoint unknown";
  }
  if (keypoint.confidence < 0.35) {
    return "replay-pose-keypoint low";
  }
  return "replay-pose-keypoint";
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
    return "Pose observation layer hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading pose observation overlays...";
  }
  if (totalCount === 0) {
    return "No pose observations in this time window.";
  }
  if (activeCount === 0) {
    return "No pose observations active at the current timestamp.";
  }
  return null;
}
