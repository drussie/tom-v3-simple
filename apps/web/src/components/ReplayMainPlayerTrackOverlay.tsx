"use client";

import type { CSSProperties } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayMainPlayerTracks,
  imagePixelRectToOverlayRect
} from "../lib/replayOverlays";
import type {
  ReplayInfo,
  ReplayMainPlayerTrackOverlay as ReplayMainPlayerTrackOverlayItem
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayMainPlayerTrackOverlayProps {
  replayInfo: ReplayInfo;
  tracks: ReplayMainPlayerTrackOverlayItem[];
  currentTimestampMs: number;
  currentFrame: number;
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  onSelectTrackAssignment: (track: ReplayMainPlayerTrackOverlayItem) => void;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

export function ReplayMainPlayerTrackOverlay({
  replayInfo,
  tracks,
  currentTimestampMs,
  currentFrame,
  enabled,
  isLoading,
  error,
  selectedObservationId,
  onSelectTrackAssignment,
  holdMs = 250
}: ReplayMainPlayerTrackOverlayProps) {
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

  const activeTracks = useMemo(
    () => activeReplayMainPlayerTracks(tracks, currentTimestampMs, currentFrame, holdMs),
    [currentFrame, currentTimestampMs, holdMs, tracks]
  );
  const status = overlayStatus({
    enabled,
    isLoading,
    error,
    activeCount: activeTracks.length,
    totalCount: tracks.length
  });

  return (
    <div className="replay-overlay-layer" ref={overlayRef}>
      {enabled
        ? activeTracks.map((track) => {
            const style = overlayBoxStyle(track, replayInfo, overlaySize);
            if (style === null) {
              return null;
            }
            const selected = track.observation_id === selectedObservationId;
            const roleClass =
              track.track_role_candidate === "near_player_track_candidate" ? "near" : "far";
            return (
              <button
                aria-label={`${track.label} main player track candidate ${formatConfidence(
                  track.assignment_score
                )} frame ${track.frame_number}`}
                className={`replay-main-player-track-box ${roleClass}${
                  selected ? " selected" : ""
                }`}
                key={track.observation_id}
                onClick={(event) => {
                  event.stopPropagation();
                  onSelectTrackAssignment(track);
                }}
                style={style}
                type="button"
              >
                <span>
                  {track.label}
                  <em>{formatConfidence(track.assignment_score)}</em>
                </span>
              </button>
            );
          })
        : null}
      {status !== null ? <div className="replay-overlay-status main-player-track">{status}</div> : null}
    </div>
  );
}

function overlayBoxStyle(
  track: ReplayMainPlayerTrackOverlayItem,
  replayInfo: ReplayInfo,
  overlaySize: OverlaySize
): CSSProperties | null {
  const rect = imagePixelRectToOverlayRect(
    track.bbox,
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
    return "Main player track layer hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading main player track assignments...";
  }
  if (totalCount === 0) {
    return "No main player track assignments in this time window.";
  }
  if (activeCount === 0) {
    return "No main player track assignments at the current timestamp.";
  }
  return null;
}
