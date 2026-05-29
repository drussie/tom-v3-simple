"use client";

import type { CSSProperties } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayEventCandidates,
  imagePixelPointToOverlayPoint
} from "../lib/replayOverlays";
import type {
  ReplayEventCandidateOverlay,
  ReplayInfo
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayEventCandidateVideoOverlayProps {
  replayInfo: ReplayInfo;
  eventCandidates: ReplayEventCandidateOverlay[];
  currentTimestampMs: number;
  currentFrame: number;
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  onSelectEventCandidate: (item: ReplayEventCandidateOverlay) => void;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

export function ReplayEventCandidateVideoOverlay({
  replayInfo,
  eventCandidates,
  currentTimestampMs,
  currentFrame,
  enabled,
  isLoading,
  error,
  selectedObservationId,
  onSelectEventCandidate,
  holdMs = 500
}: ReplayEventCandidateVideoOverlayProps) {
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

  const activeCandidates = useMemo(
    () => activeReplayEventCandidates(eventCandidates, currentTimestampMs, currentFrame, holdMs),
    [currentFrame, currentTimestampMs, eventCandidates, holdMs]
  );
  const drawableCandidates = useMemo(
    () =>
      activeCandidates
        .map((item) => {
          if (item.image_point === null) {
            return null;
          }
          const point = imagePixelPointToOverlayPoint(
            item.image_point.x,
            item.image_point.y,
            replayInfo.width,
            replayInfo.height,
            overlaySize.width,
            overlaySize.height
          );
          if (point === null) {
            return null;
          }
          return { item, point };
        })
        .filter(
          (entry): entry is {
            item: ReplayEventCandidateOverlay;
            point: { x: number; y: number };
          } => entry !== null
        ),
    [activeCandidates, overlaySize.height, overlaySize.width, replayInfo.height, replayInfo.width]
  );
  const status = overlayStatus({
    enabled,
    isLoading,
    error,
    activeCount: drawableCandidates.length,
    activeCandidateCount: activeCandidates.length,
    totalCount: eventCandidates.length
  });

  return (
    <div className="replay-overlay-layer event-candidate-video" ref={overlayRef}>
      {enabled
        ? drawableCandidates.map(({ item, point }) => {
            const isHit = item.candidate_type === "hit_candidate";
            const label = isHit ? "HIT CANDIDATE" : "BOUNCE CANDIDATE";
            const selected = selectedObservationId === item.observation_id;
            return (
              <button
                aria-label={`${label} ${formatConfidence(item.confidence)} frame ${
                  item.frame_number
                }`}
                className={`replay-event-candidate-video-marker ${
                  isHit ? "hit" : "bounce"
                }${selected ? " selected" : ""}`}
                key={item.observation_id}
                onClick={(event) => {
                  event.stopPropagation();
                  onSelectEventCandidate(item);
                }}
                style={eventCandidateMarkerStyle(point)}
                type="button"
              >
                <span className="event-marker-shape" />
                <span className="event-marker-cross horizontal" />
                <span className="event-marker-cross vertical" />
                <span className="event-marker-label">{label}</span>
              </button>
            );
          })
        : null}
      {status !== null ? <div className="replay-overlay-status event-candidate">{status}</div> : null}
    </div>
  );
}

function eventCandidateMarkerStyle(point: { x: number; y: number }): CSSProperties {
  return {
    left: `${point.x}px`,
    top: `${point.y}px`
  };
}

function overlayStatus({
  enabled,
  isLoading,
  error,
  activeCount,
  activeCandidateCount,
  totalCount
}: {
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  activeCount: number;
  activeCandidateCount: number;
  totalCount: number;
}): string | null {
  if (!enabled) {
    return null;
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading event candidate markers...";
  }
  if (totalCount === 0) {
    return null;
  }
  if (activeCandidateCount > 0 && activeCount === 0) {
    return "Event candidate image marker unavailable.";
  }
  return null;
}
