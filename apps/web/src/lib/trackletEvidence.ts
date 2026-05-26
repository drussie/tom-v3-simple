import type {
  JsonRecord,
  Tracklet,
  TrackletEvidenceBundle,
  TrackletEvidencePoint
} from "./types";

export interface TrackletEvidenceModel {
  status: string;
  identityStatus: string;
  frameRange: string;
  sourceRunId: string | null;
  selectedPoint: TrackletEvidencePoint | null;
  warning: string;
}

export function resolveTrackletIdForObservation(
  tracklets: Tracklet[],
  observationId: string | null
): string | null {
  if (observationId === null) {
    return tracklets[0]?.id ?? null;
  }

  const directTracklet = tracklets.find((tracklet) => tracklet.observation_id === observationId);
  if (directTracklet) {
    return directTracklet.id;
  }

  const pointTracklet = tracklets.find((tracklet) =>
    tracklet.points.some((point) => point.observation_id === observationId)
  );
  return pointTracklet?.id ?? tracklets[0]?.id ?? null;
}

export function buildTrackletEvidenceModel(
  bundle: TrackletEvidenceBundle | null,
  selectedObservationId: string | null
): TrackletEvidenceModel | null {
  if (bundle === null) {
    return null;
  }

  const selectedPoint =
    bundle.track_points.find((point) => point.observation?.id === selectedObservationId) ??
    bundle.track_points[0] ??
    null;
  return {
    status: bundle.summary.track_status ?? "candidate",
    identityStatus: bundle.summary.identity_status ?? "unverified",
    frameRange: `${bundle.summary.frame_start ?? "n/a"}-${bundle.summary.frame_end ?? "n/a"}`,
    sourceRunId: bundle.runs.source_detection_run?.id ?? null,
    selectedPoint,
    warning: bundle.summary.warning
  };
}

export function stringValue(value: unknown, fallback = "n/a"): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

export function jsonRecordValue(value: unknown): JsonRecord {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? (value as JsonRecord)
    : {};
}
