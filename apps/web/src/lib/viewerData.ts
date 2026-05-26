import type {
  CandidateMarker,
  EvidenceArtifact,
  HumanAnnotation,
  LineageRow,
  Observation,
  TimelineRange,
  TimelineRow,
  TimelineSegment,
  Tracklet,
  ViewerRun
} from "./types";
import { extractDetectionOverlayItems } from "./detections";
import { extractPoseOverlayItems } from "./poses";

export interface ViewerModel {
  range: TimelineRange;
  rows: TimelineRow[];
  candidates: CandidateMarker[];
  observations: Observation[];
  observationsById: Map<string, Observation>;
  lineageByObservation: Map<string, { parents: LineageRow[]; children: LineageRow[] }>;
  artifactsByObservation: Map<string, EvidenceArtifact[]>;
  annotationsByObservation: Map<string, HumanAnnotation[]>;
  defaultObservationId: string | null;
}

export function buildViewerModel(viewerRun: ViewerRun): ViewerModel {
  const observationsById = new Map(viewerRun.observations.map((row) => [row.id, row]));
  const candidates = buildCandidates(viewerRun.observations);
  const rows = [
    buildGameplayRow(viewerRun.observations),
    ...buildTrackRows(viewerRun.tracklets),
    buildDetectionRow(viewerRun.observations),
    buildPoseRow(viewerRun.observations),
    buildHomographyRow(viewerRun.observations)
  ].filter((row): row is TimelineRow => row !== null);

  const range = buildRange(viewerRun, rows, candidates);
  const lineageByObservation = groupLineage(viewerRun.lineage);
  const artifactsByObservation = groupArtifacts(viewerRun.artifacts);
  const annotationsByObservation = groupAnnotations(viewerRun.annotations);
  const defaultObservationId =
    candidates.find((candidate) => candidate.type === "bounce_candidate")?.observationId ??
    candidates[0]?.observationId ??
    extractDetectionOverlayItems(viewerRun.observations).items[0]?.observationId ??
    extractPoseOverlayItems(viewerRun.observations)[0]?.observationId ??
    viewerRun.observations[0]?.id ??
    null;

  return {
    range,
    rows,
    candidates,
    observations: sortObservations(viewerRun.observations),
    observationsById,
    lineageByObservation,
    artifactsByObservation,
    annotationsByObservation,
    defaultObservationId
  };
}

function buildGameplayRow(observations: Observation[]): TimelineRow | null {
  const segments = observations
    .filter((row) => row.gameplay !== null)
    .map(
      (row): TimelineSegment => ({
        id: row.id,
        label: row.gameplay?.view_state_subtype ?? row.gameplay?.view_state ?? "view_state",
        state: row.gameplay?.view_state ?? "unknown",
        frameStart: row.frame_start ?? 0,
        frameEnd: row.frame_end ?? row.frame_start ?? 0,
        confidence: row.confidence,
        observationId: row.id
      })
    );

  return segments.length > 0 ? { id: "gameplay", label: "Gameplay", segments } : null;
}

function buildTrackRows(tracklets: Tracklet[]): TimelineRow[] {
  const rowOrder = ["Ball track", "Near player", "Far player"];
  const rows = new Map<string, TimelineSegment[]>();

  for (const tracklet of tracklets) {
    const rowLabel = String(tracklet.metadata_jsonb.viewer_row ?? labelTracklet(tracklet));
    const coverage = Array.isArray(tracklet.metadata_jsonb.coverage_segments)
      ? tracklet.metadata_jsonb.coverage_segments
      : [];
    const segments =
      coverage.length > 0
        ? coverage.map(
            (segment, index): TimelineSegment => ({
              id: `${tracklet.id}:${index}`,
              label: segment.state,
              state: segment.state,
              frameStart: segment.frame_start,
              frameEnd: segment.frame_end,
              confidence: tracklet.confidence,
              observationId: tracklet.observation_id ?? undefined,
              trackletId: tracklet.id
            })
          )
        : [
            {
              id: tracklet.id,
              label: "tracked",
              state: "tracked",
              frameStart: tracklet.frame_start ?? 0,
              frameEnd: tracklet.frame_end ?? tracklet.frame_start ?? 0,
              confidence: tracklet.confidence,
              observationId: tracklet.observation_id ?? undefined,
              trackletId: tracklet.id
            }
          ];
    rows.set(rowLabel, [...(rows.get(rowLabel) ?? []), ...segments]);
  }

  return [...rows.entries()]
    .sort(([left], [right]) => {
      const leftIndex = rowOrder.indexOf(left);
      const rightIndex = rowOrder.indexOf(right);
      return (leftIndex === -1 ? 99 : leftIndex) - (rightIndex === -1 ? 99 : rightIndex);
    })
    .map(([label, segments]) => ({
      id: label.toLowerCase().replaceAll(" ", "-"),
      label,
      segments
    }));
}

function buildHomographyRow(observations: Observation[]): TimelineRow | null {
  const segments = observations
    .filter((row) => row.observation_type === "homography_placeholder")
    .map((row): TimelineSegment => {
      const status = String(row.payload_jsonb.homography_status ?? "unknown");
      return {
        id: row.id,
        label: status,
        state: status,
        frameStart: row.frame_start ?? 0,
        frameEnd: row.frame_end ?? row.frame_start ?? 0,
        confidence: row.confidence,
        observationId: row.id
      };
    });

  return segments.length > 0 ? { id: "homography", label: "Homography", segments } : null;
}

function buildDetectionRow(observations: Observation[]): TimelineRow | null {
  const { items } = extractDetectionOverlayItems(observations);
  const segments = items.map(
    (item): TimelineSegment => ({
      id: item.id,
      label: item.label,
      state: item.observationType,
      frameStart: item.frameNumber,
      frameEnd: item.frameNumber,
      confidence: item.confidence,
      observationId: item.observationId
    })
  );

  return segments.length > 0 ? { id: "detections", label: "Detections", segments } : null;
}

function buildPoseRow(observations: Observation[]): TimelineRow | null {
  const items = extractPoseOverlayItems(observations);
  const segments = items.map(
    (item): TimelineSegment => ({
      id: item.id,
      label: "pose observation",
      state: "pose_observation",
      frameStart: item.frameNumber,
      frameEnd: item.frameNumber,
      confidence: item.poseConfidence,
      observationId: item.observationId
    })
  );

  return segments.length > 0 ? { id: "poses", label: "Pose Observations", segments } : null;
}

function buildCandidates(observations: Observation[]): CandidateMarker[] {
  return observations
    .filter((row) => row.observation_family === "derived" && row.observation_type.endsWith("_candidate"))
    .map((row) => ({
      id: row.id,
      type: row.observation_type,
      label: row.observation_type.replaceAll("_", " "),
      frame: row.frame_start ?? row.frame_end ?? 0,
      confidence: row.confidence,
      observationId: row.id
    }))
    .sort((left, right) => left.frame - right.frame);
}

function buildRange(
  viewerRun: ViewerRun,
  rows: TimelineRow[],
  candidates: CandidateMarker[]
): TimelineRange {
  const frames: number[] = [];
  for (const row of rows) {
    for (const segment of row.segments) {
      frames.push(segment.frameStart, segment.frameEnd);
    }
  }
  for (const candidate of candidates) {
    frames.push(candidate.frame);
  }

  if (frames.length === 0) {
    return { start: 0, end: viewerRun.media?.frame_count ?? 1 };
  }

  const mediaEnd = viewerRun.media?.frame_count ?? Math.max(...frames);
  return {
    start: Math.max(0, Math.min(...frames) - 20),
    end: Math.min(mediaEnd, Math.max(...frames) + 20)
  };
}

function groupLineage(
  lineage: LineageRow[]
): Map<string, { parents: LineageRow[]; children: LineageRow[] }> {
  const grouped = new Map<string, { parents: LineageRow[]; children: LineageRow[] }>();
  for (const row of lineage) {
    const childGroup = grouped.get(row.child_observation_id) ?? { parents: [], children: [] };
    childGroup.parents.push(row);
    grouped.set(row.child_observation_id, childGroup);

    const parentGroup = grouped.get(row.parent_observation_id) ?? { parents: [], children: [] };
    parentGroup.children.push(row);
    grouped.set(row.parent_observation_id, parentGroup);
  }
  return grouped;
}

function groupArtifacts(artifacts: EvidenceArtifact[]): Map<string, EvidenceArtifact[]> {
  const grouped = new Map<string, EvidenceArtifact[]>();
  for (const artifact of artifacts) {
    if (artifact.target_observation_id === null) {
      continue;
    }
    grouped.set(artifact.target_observation_id, [
      ...(grouped.get(artifact.target_observation_id) ?? []),
      artifact
    ]);
  }
  return grouped;
}

function groupAnnotations(annotations: HumanAnnotation[]): Map<string, HumanAnnotation[]> {
  const grouped = new Map<string, HumanAnnotation[]>();
  for (const annotation of annotations) {
    if (annotation.observation_id === null) {
      continue;
    }
    grouped.set(annotation.observation_id, [
      ...(grouped.get(annotation.observation_id) ?? []),
      annotation
    ]);
  }
  return grouped;
}

function sortObservations(observations: Observation[]): Observation[] {
  return [...observations].sort((left, right) => {
    const frameDelta = (left.frame_start ?? 0) - (right.frame_start ?? 0);
    if (frameDelta !== 0) {
      return frameDelta;
    }
    return left.observation_type.localeCompare(right.observation_type);
  });
}

function labelTracklet(tracklet: Tracklet): string {
  if (tracklet.track_family === "ball") {
    return "Ball track";
  }
  if (tracklet.subject_ref === "near_player") {
    return "Near player";
  }
  if (tracklet.subject_ref === "far_player") {
    return "Far player";
  }
  return tracklet.subject_ref ?? tracklet.track_family;
}
