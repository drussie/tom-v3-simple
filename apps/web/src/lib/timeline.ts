import type { TimelineRange } from "./types";

export function frameToPercent(frame: number, range: TimelineRange): number {
  const span = Math.max(1, range.end - range.start);
  const percent = ((frame - range.start) / span) * 100;
  return Math.min(100, Math.max(0, percent));
}

export function segmentStyle(
  frameStart: number,
  frameEnd: number,
  range: TimelineRange
): { left: string; width: string } {
  const left = frameToPercent(frameStart, range);
  const right = frameToPercent(frameEnd, range);
  return {
    left: `${left}%`,
    width: `${Math.max(0.4, right - left)}%`
  };
}

export function formatFrameRange(frameStart: number | null, frameEnd: number | null): string {
  if (frameStart === null && frameEnd === null) {
    return "frame n/a";
  }
  if (frameStart === frameEnd || frameEnd === null) {
    return `frame ${frameStart ?? "n/a"}`;
  }
  return `frames ${frameStart ?? "n/a"}-${frameEnd}`;
}

export function formatConfidence(confidence: number | null): string {
  if (confidence === null) {
    return "n/a";
  }
  return `${Math.round(confidence * 100)}%`;
}
