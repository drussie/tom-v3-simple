export function currentTimeSecondsToTimestampMs(currentTimeSeconds: number): number {
  if (!Number.isFinite(currentTimeSeconds) || currentTimeSeconds <= 0) {
    return 0;
  }
  return Math.round(currentTimeSeconds * 1000);
}

export function currentTimeSecondsToFrame(
  currentTimeSeconds: number,
  fps: number | null,
  frameCount: number | null
): number {
  if (!Number.isFinite(currentTimeSeconds) || currentTimeSeconds <= 0 || fps === null || fps <= 0) {
    return 0;
  }
  const frame = Math.round(currentTimeSeconds * fps);
  if (frameCount === null || frameCount <= 0) {
    return Math.max(0, frame);
  }
  return Math.max(0, Math.min(frame, frameCount - 1));
}

export function formatReplayTime(seconds: number): string {
  const timestampMs = currentTimeSecondsToTimestampMs(seconds);
  const minutes = Math.floor(timestampMs / 60000);
  const remainingMs = timestampMs - minutes * 60000;
  const wholeSeconds = Math.floor(remainingMs / 1000);
  const milliseconds = remainingMs % 1000;
  return `${minutes.toString().padStart(2, "0")}:${wholeSeconds
    .toString()
    .padStart(2, "0")}.${milliseconds.toString().padStart(3, "0")}`;
}
