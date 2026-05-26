import type {
  DetectionBBox,
  DetectionOverlayItem,
  DetectionOverlayModel,
  DetectionPoint,
  JsonRecord,
  MediaAsset,
  Observation
} from "./types";

const detectionTypes = new Set(["ball_detection", "player_detection"]);

export function buildDetectionOverlayModel(
  media: MediaAsset | null,
  observations: Observation[],
  selectedObservationId: string | null
): DetectionOverlayModel {
  const { items, missingBboxObservationIds } = extractDetectionOverlayItems(observations);
  const selectedFrame = selectDetectionFrame(items, observations, selectedObservationId);
  const selectedItems =
    selectedFrame === null ? [] : items.filter((item) => item.frameNumber === selectedFrame);

  const mediaWidth = validDimension(media?.width) ? media?.width ?? null : null;
  const mediaHeight = validDimension(media?.height) ? media?.height ?? null : null;

  return {
    items: markSelected(items, selectedObservationId),
    frameItems: markSelected(selectedItems, selectedObservationId),
    selectedFrame,
    missingBboxObservationIds,
    unavailableReason: unavailableReason(mediaWidth, mediaHeight, items),
    mediaWidth,
    mediaHeight
  };
}

export function extractDetectionOverlayItems(observations: Observation[]): {
  items: DetectionOverlayItem[];
  missingBboxObservationIds: string[];
} {
  const items: DetectionOverlayItem[] = [];
  const missingBboxObservationIds: string[] = [];

  for (const observation of observations) {
    if (!isDetectionObservation(observation)) {
      continue;
    }

    const bbox = extractBBox(observation);
    if (bbox === null) {
      missingBboxObservationIds.push(observation.id);
      continue;
    }

    const payload = mergedPayload(observation);
    const frameNumber = observation.frame_start ?? observation.frame_end;
    if (frameNumber === null) {
      missingBboxObservationIds.push(observation.id);
      continue;
    }

    items.push({
      id: observation.id,
      observationId: observation.id,
      observationType: observation.observation_type as "ball_detection" | "player_detection",
      label: detectionLabel(observation, payload),
      frameNumber,
      timestampMs: observation.timestamp_start_ms ?? observation.timestamp_end_ms,
      confidence: observation.confidence,
      bbox,
      center: extractCenter(payload),
      classLabel: stringOrNull(payload.class_label),
      classId: scalarOrNull(payload.class_id),
      metadata: recordOrEmpty(payload.metadata),
      isSelected: false
    });
  }

  return {
    items: items.sort((left, right) => {
      const frameDelta = left.frameNumber - right.frameNumber;
      if (frameDelta !== 0) {
        return frameDelta;
      }
      return left.label.localeCompare(right.label);
    }),
    missingBboxObservationIds
  };
}

export function isDetectionObservation(observation: Observation): boolean {
  return (
    observation.observation_family === "atomic" &&
    detectionTypes.has(observation.observation_type)
  );
}

function selectDetectionFrame(
  items: DetectionOverlayItem[],
  observations: Observation[],
  selectedObservationId: string | null
): number | null {
  if (selectedObservationId !== null) {
    const selectedObservation = observations.find((observation) => observation.id === selectedObservationId);
    if (selectedObservation !== undefined && isDetectionObservation(selectedObservation)) {
      return selectedObservation.frame_start ?? selectedObservation.frame_end ?? null;
    }
  }

  return items[0]?.frameNumber ?? null;
}

function markSelected(
  items: DetectionOverlayItem[],
  selectedObservationId: string | null
): DetectionOverlayItem[] {
  return items.map((item) => ({
    ...item,
    isSelected: item.observationId === selectedObservationId
  }));
}

function unavailableReason(
  mediaWidth: number | null,
  mediaHeight: number | null,
  items: DetectionOverlayItem[]
): string | null {
  if (mediaWidth === null || mediaHeight === null) {
    return "Media dimensions are unavailable, so image-pixel bboxes cannot be scaled.";
  }
  if (items.length === 0) {
    return "No persisted detection observations with bbox payloads are available for this run.";
  }
  return null;
}

function isDetectionType(value: string): value is "ball_detection" | "player_detection" {
  return value === "ball_detection" || value === "player_detection";
}

function extractBBox(observation: Observation): DetectionBBox | null {
  const payload = mergedPayload(observation);
  const bbox = asRecord(payload.bbox);
  if (bbox === null) {
    return null;
  }

  const x = numeric(bbox.x);
  const y = numeric(bbox.y);
  const width = numeric(bbox.width);
  const height = numeric(bbox.height);
  if (x === null || y === null || width === null || height === null) {
    return null;
  }

  return { x, y, width, height };
}

function extractCenter(payload: JsonRecord): DetectionPoint | null {
  const center = asRecord(payload.center);
  if (center === null) {
    return null;
  }
  const x = numeric(center.x);
  const y = numeric(center.y);
  return x === null || y === null ? null : { x, y };
}

function mergedPayload(observation: Observation): JsonRecord {
  return {
    ...observation.payload_jsonb,
    ...(observation.atomic?.payload_jsonb ?? {})
  };
}

function detectionLabel(observation: Observation, payload: JsonRecord): string {
  const directLabel = stringOrNull(payload.label);
  if (directLabel !== null) {
    return directLabel;
  }

  const detector = asRecord(payload.detector);
  const detectorLabel = detector === null ? null : stringOrNull(detector.label);
  if (detectorLabel !== null) {
    return detectorLabel;
  }

  const classLabel = stringOrNull(payload.class_label);
  if (classLabel !== null) {
    return classLabel;
  }

  return isDetectionType(observation.observation_type)
    ? observation.observation_type.replace("_detection", "")
    : "detection";
}

function validDimension(value: unknown): boolean {
  return typeof value === "number" && Number.isFinite(value) && value > 0;
}

function numeric(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  return null;
}

function scalarOrNull(value: unknown): number | string | null {
  if (typeof value === "number" || typeof value === "string") {
    return value;
  }
  return null;
}

function stringOrNull(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function recordOrEmpty(value: unknown): JsonRecord {
  return asRecord(value) ?? {};
}

function asRecord(value: unknown): JsonRecord | null {
  if (value !== null && typeof value === "object" && !Array.isArray(value)) {
    return value as JsonRecord;
  }
  return null;
}
