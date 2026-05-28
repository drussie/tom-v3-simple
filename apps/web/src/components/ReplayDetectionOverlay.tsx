"use client";

import type { CSSProperties } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayDetections,
  imagePixelRectToOverlayRect
} from "../lib/replayOverlays";
import type {
  ReplayDetectionOverlay as ReplayDetectionOverlayItem,
  ReplayInfo,
  ReplayOverlayDisplayMode
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayDetectionOverlayProps {
  replayInfo: ReplayInfo;
  detections: ReplayDetectionOverlayItem[];
  currentTimestampMs: number;
  currentFrame: number;
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  onSelectObservation: (detection: ReplayDetectionOverlayItem) => void;
  displayMode?: ReplayOverlayDisplayMode;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

export function ReplayDetectionOverlay({
  replayInfo,
  detections,
  currentTimestampMs,
  currentFrame,
  enabled,
  isLoading,
  error,
  selectedObservationId,
  onSelectObservation,
  displayMode = "current_only",
  holdMs = 250
}: ReplayDetectionOverlayProps) {
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

  const activeDetections = useMemo(
    () => activeReplayDetections(detections, currentTimestampMs, currentFrame, holdMs, displayMode),
    [currentFrame, currentTimestampMs, detections, displayMode, holdMs]
  );

  const status = overlayStatus({
    enabled,
    isLoading,
    error,
    activeCount: activeDetections.length,
    totalCount: detections.length
  });

  return (
    <div className="replay-overlay-layer" ref={overlayRef}>
      {enabled
        ? activeDetections.map((detection) => {
            const style = overlayBoxStyle(detection, replayInfo, overlaySize);
            if (style === null) {
              return null;
            }
            const selected = detection.observation_id === selectedObservationId;
            return (
              <button
                aria-label={`${detection.label} detection observation ${formatConfidence(
                  detection.confidence
                )} frame ${detection.frame_number}`}
                className={`replay-detection-box ${
                  detection.observation_type === "ball_detection" ? "ball" : "player"
                }${selected ? " selected" : ""}`}
                key={detection.observation_id}
                onClick={(event) => {
                  event.stopPropagation();
                  onSelectObservation(detection);
                }}
                style={style}
                type="button"
              >
                <span>
                  {detection.label}
                  <em>{formatConfidence(detection.confidence)}</em>
                </span>
              </button>
            );
          })
        : null}
      {status !== null ? <div className="replay-overlay-status">{status}</div> : null}
    </div>
  );
}

function overlayBoxStyle(
  detection: ReplayDetectionOverlayItem,
  replayInfo: ReplayInfo,
  overlaySize: OverlaySize
): CSSProperties | null {
  const rect = imagePixelRectToOverlayRect(
    detection.bbox,
    replayInfo.width,
    replayInfo.height,
    overlaySize.width,
    overlaySize.height
  );
  if (rect === null) {
    return null;
  }
  return {
    left: `${rect.x}px`,
    top: `${rect.y}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`
  };
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
    return "Detection layer hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading detection observations...";
  }
  if (totalCount === 0) {
    return "No detection overlays in this time window.";
  }
  if (activeCount === 0) {
    return "No detection observations at the current timestamp.";
  }
  return null;
}
