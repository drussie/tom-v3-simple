"use client";

import type {
  ReplayBallCourtProjectionOverlay,
  ReplayMainPlayerCourtProjectionOverlay
} from "../lib/types";
import {
  activeReplayBallCourtProjection,
  activeReplayMainPlayerCourtProjection
} from "../lib/replayOverlays";

interface ReplayCourtProjectionMiniMapProps {
  ballProjections: ReplayBallCourtProjectionOverlay[];
  mainPlayerProjections: ReplayMainPlayerCourtProjectionOverlay[];
  currentTimestampMs: number;
  currentFrame: number;
  showBall: boolean;
  showPlayers: boolean;
  selectedObservationId?: string | null;
  onSelectBallProjection: (item: ReplayBallCourtProjectionOverlay) => void;
  onSelectMainPlayerProjection: (item: ReplayMainPlayerCourtProjectionOverlay) => void;
}

const COURT_WIDTH = 320;
const COURT_HEIGHT = 180;

export function ReplayCourtProjectionMiniMap({
  ballProjections,
  mainPlayerProjections,
  currentTimestampMs,
  currentFrame,
  showBall,
  showPlayers,
  selectedObservationId = null,
  onSelectBallProjection,
  onSelectMainPlayerProjection
}: ReplayCourtProjectionMiniMapProps) {
  const activeBall = showBall
    ? activeReplayBallCourtProjection(ballProjections, currentTimestampMs, currentFrame)
    : [];
  const activePlayers = showPlayers
    ? activeReplayMainPlayerCourtProjection(
        mainPlayerProjections,
        currentTimestampMs,
        currentFrame
      )
    : [];

  if (activeBall.length === 0 && activePlayers.length === 0) {
    return (
      <section className="replay-court-projection-panel">
        <div>
          <p className="eyebrow">Court projection candidates</p>
          <h3>No current court projection candidate</h3>
        </div>
        <p className="subtle">
          Projection candidates appear here when a courtProjectionRunId is selected.
        </p>
      </section>
    );
  }

  return (
    <section className="replay-court-projection-panel">
      <div className="replay-court-projection-header">
        <div>
          <p className="eyebrow">Court projection candidates</p>
          <h3>Normalized court-template view</h3>
        </div>
        <span className="evidence-badge">not court truth</span>
      </div>
      <svg
        className="replay-court-projection-map"
        viewBox={`0 0 ${COURT_WIDTH} ${COURT_HEIGHT}`}
        role="img"
        aria-label="Court projection candidate mini map"
      >
        <rect className="court-map-surface" x="8" y="8" width="304" height="164" rx="3" />
        <line className="court-map-line" x1="160" y1="8" x2="160" y2="172" />
        <line className="court-map-line" x1="8" y1="90" x2="312" y2="90" />
        <line className="court-map-line muted" x1="84" y1="8" x2="84" y2="172" />
        <line className="court-map-line muted" x1="236" y1="8" x2="236" y2="172" />
        <line className="court-map-line muted" x1="8" y1="48" x2="312" y2="48" />
        <line className="court-map-line muted" x1="8" y1="132" x2="312" y2="132" />
        {activePlayers.map((item) => {
          const point = templatePointToSvg(item.court_point.x, item.court_point.y);
          const role = item.track_role_candidate?.includes("near")
            ? "near"
            : item.track_role_candidate?.includes("far")
            ? "far"
            : "player";
          const label = role === "near" ? "NEAR PLAYER CANDIDATE" : role === "far" ? "FAR PLAYER CANDIDATE" : "PLAYER CANDIDATE";
          return (
            <g
              key={item.observation_id}
              className={`court-projection-point-group player ${role} ${
                selectedObservationId === item.observation_id ? "selected" : ""
              }`}
              onClick={() => onSelectMainPlayerProjection(item)}
            >
              <circle cx={point.x} cy={point.y} r="5" />
              <text x={point.x + 8} y={point.y - 7}>
                {label}
              </text>
            </g>
          );
        })}
        {activeBall.map((item) => {
          const point = templatePointToSvg(item.court_point.x, item.court_point.y);
          return (
            <g
              key={item.observation_id}
              className={`court-projection-point-group ball ${
                selectedObservationId === item.observation_id ? "selected" : ""
              }`}
              onClick={() => onSelectBallProjection(item)}
            >
              <circle cx={point.x} cy={point.y} r="4" />
              <text x={point.x + 7} y={point.y + 4}>
                BALL CANDIDATE
              </text>
            </g>
          );
        })}
      </svg>
      <p className="subtle">
        Derived projection evidence only. These points do not imply bounce, hit, in/out, or
        player position truth.
      </p>
    </section>
  );
}

function templatePointToSvg(x: number, y: number): { x: number; y: number } {
  return {
    x: 8 + clamp01(x) * 304,
    y: 8 + clamp01(y) * 164
  };
}

function clamp01(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.min(1, Math.max(0, value));
}
