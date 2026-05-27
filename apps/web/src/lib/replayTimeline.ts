import type {
  ReplayTimelineItem,
  ReplayTimelineLane,
  ReplayTrackletTimelineItem
} from "./types";

export function timelinePointPercent(
  timestampMs: number,
  durationMs: number | null
): number {
  if (durationMs === null || durationMs <= 0) {
    return 0;
  }
  return clampPercent((timestampMs / durationMs) * 100);
}

export function timelineSpanPosition(
  item: ReplayTrackletTimelineItem,
  durationMs: number | null
): { left: number; width: number } {
  if (durationMs === null || durationMs <= 0) {
    return { left: 0, width: 0 };
  }
  const start = Math.min(item.timestamp_start_ms, item.timestamp_end_ms);
  const end = Math.max(item.timestamp_start_ms, item.timestamp_end_ms);
  const left = timelinePointPercent(start, durationMs);
  const right = timelinePointPercent(end, durationMs);
  return {
    left,
    width: Math.max(0.6, right - left)
  };
}

export function timelineItemTimestampMs(item: ReplayTimelineItem): number {
  if (item.item_type === "tracklet") {
    return item.timestamp_start_ms;
  }
  return item.timestamp_ms;
}

export function timelineItemKey(item: ReplayTimelineItem): string {
  if (item.item_type === "detection") {
    return `detection:${item.observation_id}`;
  }
  if (item.item_type === "tracklet") {
    return `tracklet:${item.tracklet_id}`;
  }
  if (item.item_type === "pose") {
    return `pose:${item.observation_id}`;
  }
  if (item.item_type === "court_keypoint") {
    return `court_keypoint:${item.observation_id}`;
  }
  if (item.item_type === "court_line") {
    return `court_line:${item.observation_id}`;
  }
  if (item.item_type === "camera_view") {
    return `camera_view:${item.observation_id}`;
  }
  if (item.item_type === "homography_candidate") {
    return `homography_candidate:${item.observation_id}`;
  }
  return `annotation:${item.annotation_id}`;
}

export function timelineItemAvailableAt(
  item: ReplayTimelineItem,
  availableUntilMs: number | null
): boolean {
  if (availableUntilMs === null) {
    return true;
  }
  if (item.item_type === "tracklet") {
    return item.timestamp_start_ms <= availableUntilMs;
  }
  return item.timestamp_ms <= availableUntilMs;
}

export function timelineLaneItemsAvailableAt(
  lane: ReplayTimelineLane,
  availableUntilMs: number | null
): ReplayTimelineItem[] {
  if (availableUntilMs === null) {
    return lane.items;
  }
  return lane.items
    .filter((item) => timelineItemAvailableAt(item, availableUntilMs))
    .map((item) => {
      if (item.item_type !== "tracklet") {
        return item;
      }
      return {
        ...item,
        timestamp_end_ms: Math.min(item.timestamp_end_ms, Math.max(item.timestamp_start_ms, availableUntilMs))
      };
    });
}

export function timelineAvailableItemCount(
  lanes: ReplayTimelineLane[],
  availableUntilMs: number | null
): number {
  return lanes.reduce(
    (count, lane) => count + timelineLaneItemsAvailableAt(lane, availableUntilMs).length,
    0
  );
}

function clampPercent(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.max(0, Math.min(value, 100));
}
