"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayTracklets,
  activeReplayTrackPoints,
  imagePixelPointToOverlayPoint
} from "../lib/replayOverlays";
import type {
  ReplayInfo,
  ReplayTrackletOverlay as ReplayTrackletOverlayItem,
  ReplayTrackPointOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayTrackletOverlayProps {
  replayInfo: ReplayInfo;
  tracklets: ReplayTrackletOverlayItem[];
  currentTimestampMs: number;
  currentFrame: number;
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  selectedTrackletId: string | null;
  selectedTrackPointId: string | null;
  onSelectTracklet: (tracklet: ReplayTrackletOverlayItem) => void;
  onSelectTrackPoint: (
    tracklet: ReplayTrackletOverlayItem,
    point: ReplayTrackPointOverlay
  ) => void;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

export function ReplayTrackletOverlay({
  replayInfo,
  tracklets,
  currentTimestampMs,
  currentFrame,
  enabled,
  isLoading,
  error,
  selectedTrackletId,
  selectedTrackPointId,
  onSelectTracklet,
  onSelectTrackPoint,
  holdMs = 250
}: ReplayTrackletOverlayProps) {
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

  const activeTracklets = useMemo(
    () => activeReplayTracklets(tracklets, currentTimestampMs, currentFrame, holdMs),
    [currentFrame, currentTimestampMs, holdMs, tracklets]
  );

  const status = overlayStatus({
    enabled,
    isLoading,
    error,
    activeCount: activeTracklets.length,
    totalCount: tracklets.length
  });

  return (
    <div className="replay-overlay-layer" ref={overlayRef}>
      {enabled ? (
        <svg className="replay-vector-layer" role="presentation">
          {activeTracklets.map((tracklet) => {
            const selected = tracklet.tracklet_id === selectedTrackletId;
            const activePoints = activeReplayTrackPoints(
              tracklet.points,
              currentTimestampMs,
              currentFrame,
              holdMs
            );
            const pathPoints = selected ? tracklet.points : activePoints;
            const scaledPath = pathPoints
              .map((point) => scalePoint(point, replayInfo, overlaySize))
              .filter((point): point is { x: number; y: number } => point !== null);
            const pointsAttr = scaledPath.map((point) => `${point.x},${point.y}`).join(" ");
            return (
              <g
                className={`replay-tracklet-group ${
                  tracklet.track_type === "ball" ? "ball" : "player"
                }${selected ? " selected" : ""}`}
                key={tracklet.tracklet_id}
              >
                {selected && scaledPath.length > 1 ? (
                  <polyline
                    className="replay-tracklet-path"
                    onClick={(event) => {
                      event.stopPropagation();
                      onSelectTracklet(tracklet);
                    }}
                    points={pointsAttr}
                  />
                ) : null}
                {activePoints.map((point) => {
                  const scaledPoint = scalePoint(point, replayInfo, overlaySize);
                  if (scaledPoint === null) {
                    return null;
                  }
                  const pointSelected = point.track_point_id === selectedTrackPointId;
                  return (
                    <g
                      aria-label={`${trackletLabel(tracklet)} track point candidate ${formatConfidence(
                        point.confidence
                      )} frame ${point.frame_number}`}
                      className={`replay-tracklet-point${pointSelected ? " selected" : ""}`}
                      key={point.track_point_id}
                      onClick={(event) => {
                        event.stopPropagation();
                        onSelectTrackPoint(tracklet, point);
                      }}
                      onKeyDown={(event) => {
                        if (event.key === "Enter" || event.key === " ") {
                          event.preventDefault();
                          onSelectTrackPoint(tracklet, point);
                        }
                      }}
                      role="button"
                      tabIndex={0}
                    >
                      <circle cx={scaledPoint.x} cy={scaledPoint.y} r={selected ? 7 : 5} />
                      <text x={scaledPoint.x + 8} y={scaledPoint.y - 8}>
                        {trackletLabel(tracklet)}
                      </text>
                    </g>
                  );
                })}
              </g>
            );
          })}
        </svg>
      ) : null}
      {status !== null ? <div className="replay-overlay-status tracklet">{status}</div> : null}
    </div>
  );
}

function scalePoint(
  point: ReplayTrackPointOverlay,
  replayInfo: ReplayInfo,
  overlaySize: OverlaySize
): { x: number; y: number } | null {
  return imagePixelPointToOverlayPoint(
    point.x,
    point.y,
    replayInfo.width,
    replayInfo.height,
    overlaySize.width,
    overlaySize.height
  );
}

function trackletLabel(tracklet: ReplayTrackletOverlayItem): string {
  return tracklet.label_hint ?? tracklet.track_type;
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
    return "Tracklet candidate layer hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading tracklet candidate overlays...";
  }
  if (totalCount === 0) {
    return "No tracklet candidates in this time window.";
  }
  if (activeCount === 0) {
    return "No tracklet candidates active at the current timestamp.";
  }
  return null;
}
