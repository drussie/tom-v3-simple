import type { CSSProperties } from "react";

import type { DetectionOverlayItem } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface DetectionOverlayCanvasProps {
  items: DetectionOverlayItem[];
  mediaWidth: number;
  mediaHeight: number;
  selectedFrame: number;
  onSelectObservation: (observationId: string) => void;
}

export function DetectionOverlayCanvas({
  items,
  mediaWidth,
  mediaHeight,
  selectedFrame,
  onSelectObservation
}: DetectionOverlayCanvasProps) {
  return (
    <div
      aria-label={`Detection overlay frame ${selectedFrame}`}
      className="detection-canvas"
      style={{ aspectRatio: `${mediaWidth} / ${mediaHeight}` }}
    >
      <div className="detection-canvas-grid" />
      <div className="frame-space-label">
        <strong>image_pixels</strong>
        <span>
          {mediaWidth} x {mediaHeight}
        </span>
      </div>
      {items.map((item) => (
        <button
          aria-label={`${item.label} ${formatConfidence(item.confidence)} frame ${item.frameNumber}`}
          className={`detection-box ${item.observationType === "ball_detection" ? "ball" : "player"}${
            item.isSelected ? " selected" : ""
          }`}
          key={item.id}
          onClick={() => onSelectObservation(item.observationId)}
          style={bboxStyle(item, mediaWidth, mediaHeight)}
          type="button"
        >
          <span>
            {item.label}
            <em>{formatConfidence(item.confidence)}</em>
          </span>
        </button>
      ))}
    </div>
  );
}

function bboxStyle(
  item: DetectionOverlayItem,
  mediaWidth: number,
  mediaHeight: number
): CSSProperties {
  const left = percentage(item.bbox.x, mediaWidth);
  const top = percentage(item.bbox.y, mediaHeight);
  const width = percentage(item.bbox.width, mediaWidth);
  const height = percentage(item.bbox.height, mediaHeight);
  return {
    left: `${left}%`,
    top: `${top}%`,
    width: `${width}%`,
    height: `${height}%`
  };
}

function percentage(value: number, dimension: number): number {
  return Math.max(0, Math.min(100, (value / dimension) * 100));
}
