"use client";

import type {
  ReplayTimeline,
  ReplayTimelineItem,
  ReplayTimelineLane
} from "../lib/types";
import {
  timelineLaneItemsAvailableAt,
  timelineItemKey,
  timelineItemTimestampMs,
  timelinePointPercent,
  timelineSpanPosition
} from "../lib/replayTimeline";

interface ReplayEvidenceTimelineProps {
  availableUntilMs?: number | null;
  currentTimestampMs: number;
  durationMs: number | null;
  error: string | null;
  isLoading: boolean;
  layerVisibility: {
    detections: boolean;
    tracklets: boolean;
    pose: boolean;
    main_player_tracks: boolean;
    smoothed_motion: boolean;
    court_keypoints: boolean;
    court_lines: boolean;
    camera_view: boolean;
    homography_candidates: boolean;
    projection_diagnostics: boolean;
    court_projection: boolean;
    ball_trajectory: boolean;
    annotations: boolean;
  };
  onSelectItem: (item: ReplayTimelineItem) => void;
  selectedItemKey: string | null;
  timeline: ReplayTimeline | null;
}

export function ReplayEvidenceTimeline({
  availableUntilMs = null,
  currentTimestampMs,
  durationMs,
  error,
  isLoading,
  layerVisibility,
  onSelectItem,
  selectedItemKey,
  timeline
}: ReplayEvidenceTimelineProps) {
  const playheadPercent = timelinePointPercent(currentTimestampMs, durationMs);
  const lanes = timeline?.lanes ?? [];

  return (
    <section className="panel replay-evidence-timeline">
      <div className="panel-header">
        <h2>Evidence Timeline</h2>
        <span className="mini-pill">click to seek</span>
      </div>
      <div className="panel-body">
        <p className="evidence-note">
          Timeline lanes are navigation aids over persisted evidence. They do not classify tennis
          actions or confirm object identity.
        </p>
        {availableUntilMs !== null ? (
          <p className="evidence-note">
            Stream Proxy Mode hides future evidence until the live-like edge reaches it. Hidden
            future items are still persisted records, not operator-available evidence yet.
          </p>
        ) : null}
        {error !== null ? <p className="empty-state">{error}</p> : null}
        {isLoading && timeline === null ? (
          <p className="empty-state">Loading timeline evidence lanes...</p>
        ) : null}
        {timeline === null && !isLoading && error === null ? (
          <p className="empty-state">No timeline payload loaded for this replay media.</p>
        ) : null}
        {timeline !== null ? (
          <div className="timeline-lane-stack">
            <div className="timeline-ruler" aria-hidden="true">
              <span>0 ms</span>
              <span>{durationMs ?? 0} ms</span>
            </div>
            <div className="timeline-lanes">
              <div
                className="timeline-playhead"
                style={{ left: `${playheadPercent}%` }}
                title={`${currentTimestampMs} ms`}
              />
              {lanes.map((lane) => (
                <TimelineLane
                  durationMs={durationMs}
                  availableUntilMs={availableUntilMs}
                  isVisible={layerVisibility[lane.lane_type]}
                  key={lane.lane_type}
                  lane={lane}
                  onSelectItem={onSelectItem}
                  selectedItemKey={selectedItemKey}
                />
              ))}
            </div>
            {timeline.annotations_without_time_count > 0 ? (
              <p className="empty-state compact">
                {timeline.annotations_without_time_count} review annotations have no media time and
                are omitted from the lane.
              </p>
            ) : null}
          </div>
        ) : null}
      </div>
    </section>
  );
}

function TimelineLane({
  availableUntilMs,
  durationMs,
  isVisible,
  lane,
  onSelectItem,
  selectedItemKey
}: {
  availableUntilMs: number | null;
  durationMs: number | null;
  isVisible: boolean;
  lane: ReplayTimelineLane;
  onSelectItem: (item: ReplayTimelineItem) => void;
  selectedItemKey: string | null;
}) {
  const availableItems = timelineLaneItemsAvailableAt(lane, availableUntilMs);
  const hiddenFutureCount = lane.items.length - availableItems.length;

  return (
    <div className={`timeline-lane-row${isVisible ? "" : " muted"}`}>
      <div className="timeline-lane-label">
        <strong>{lane.label}</strong>
        <span>
          {isVisible
            ? availableUntilMs === null
              ? `${lane.items.length} items`
              : `${availableItems.length} available · ${hiddenFutureCount} future hidden`
            : "layer hidden"}
        </span>
      </div>
      <div className="timeline-lane-track">
        {availableItems.length === 0 ? (
          <span className="timeline-lane-empty">
            {availableUntilMs === null
              ? emptyLaneText(lane.lane_type)
              : proxyEmptyLaneText(lane.lane_type)}
          </span>
        ) : (
          availableItems.map((item) => (
            <TimelineItemButton
              durationMs={durationMs}
              isSelected={timelineItemKey(item) === selectedItemKey}
              item={item}
              key={timelineItemKey(item)}
              onSelectItem={onSelectItem}
            />
          ))
        )}
      </div>
    </div>
  );
}

function TimelineItemButton({
  durationMs,
  isSelected,
  item,
  onSelectItem
}: {
  durationMs: number | null;
  isSelected: boolean;
  item: ReplayTimelineItem;
  onSelectItem: (item: ReplayTimelineItem) => void;
}) {
  if (
    item.item_type === "tracklet" ||
    item.item_type === "ball_trajectory_court_candidate"
  ) {
    const position = timelineSpanPosition(item, durationMs);
    const label =
      item.item_type === "tracklet"
        ? `${item.display_label}: ${item.timestamp_start_ms}-${item.timestamp_end_ms} ms`
        : `${item.display_label}: ${item.timestamp_start_ms}-${item.timestamp_end_ms} ms`;
    return (
      <button
        className={`timeline-lane-item span ${item.item_type}${isSelected ? " selected" : ""}`}
        onClick={() => onSelectItem(item)}
        style={{ left: `${position.left}%`, width: `${position.width}%` }}
        title={label}
        type="button"
      >
        <span>{item.display_label}</span>
      </button>
    );
  }

  const left = timelinePointPercent(timelineItemTimestampMs(item), durationMs);
  return (
    <button
      className={`timeline-lane-item tick ${item.item_type}${isSelected ? " selected" : ""}`}
      onClick={() => onSelectItem(item)}
      style={{ left: `${left}%` }}
      title={`${item.display_label}: ${timelineItemTimestampMs(item)} ms`}
      type="button"
    >
      <span>{item.display_label}</span>
    </button>
  );
}

function emptyLaneText(laneType: ReplayTimelineLane["lane_type"]): string {
  if (laneType === "detections") {
    return "No detection observations in the selected run.";
  }
  if (laneType === "tracklets") {
    return "No tracklet candidates in the selected run.";
  }
  if (laneType === "pose") {
    return "No pose observations in the selected run.";
  }
  if (laneType === "main_player_tracks") {
    return "No main player track assignments in the selected run.";
  }
  if (laneType === "smoothed_motion") {
    return "No smoothed motion candidates in the selected run.";
  }
  if (laneType === "court_keypoints") {
    return "No court keypoint evidence in the selected run.";
  }
  if (laneType === "court_lines") {
    return "No court line evidence in the selected run.";
  }
  if (laneType === "camera_view") {
    return "No camera/view evidence in the selected run.";
  }
  if (laneType === "homography_candidates") {
    return "No homography candidates in the selected run.";
  }
  if (laneType === "projection_diagnostics") {
    return "No projection diagnostics in the selected run.";
  }
  if (laneType === "court_projection") {
    return "No court projection candidates in the selected run.";
  }
  if (laneType === "ball_trajectory") {
    return "No ball trajectory court candidates in the selected run.";
  }
  return "No review annotations for this media/run context.";
}

function proxyEmptyLaneText(laneType: ReplayTimelineLane["lane_type"]): string {
  if (laneType === "detections") {
    return "No detection observations available at the current live-like edge.";
  }
  if (laneType === "tracklets") {
    return "No tracklet candidates available at the current live-like edge.";
  }
  if (laneType === "pose") {
    return "No pose observations available at the current live-like edge.";
  }
  if (laneType === "main_player_tracks") {
    return "No main player track assignments available at the current live-like edge.";
  }
  if (laneType === "smoothed_motion") {
    return "No smoothed motion candidates available at the current live-like edge.";
  }
  if (laneType === "court_keypoints") {
    return "No court keypoint evidence available at the current live-like edge.";
  }
  if (laneType === "court_lines") {
    return "No court line evidence available at the current live-like edge.";
  }
  if (laneType === "camera_view") {
    return "No camera/view evidence available at the current live-like edge.";
  }
  if (laneType === "homography_candidates") {
    return "No homography candidates available at the current live-like edge.";
  }
  if (laneType === "projection_diagnostics") {
    return "No projection diagnostics available at the current live-like edge.";
  }
  if (laneType === "court_projection") {
    return "No court projection candidates available at the current live-like edge.";
  }
  if (laneType === "ball_trajectory") {
    return "No ball trajectory court candidates available at the current live-like edge.";
  }
  return "No review annotations available at the current live-like edge.";
}
