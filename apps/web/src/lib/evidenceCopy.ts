import type { EvidenceArtifact, HumanAnnotation, JsonRecord, Observation } from "./types";

export function observationDisplayName(observation: Observation): string {
  switch (observation.observation_type) {
    case "ball_detection":
      return "Ball detection observation";
    case "player_detection":
      return "Player detection observation";
    case "ball_tracklet_candidate":
      return "Ball tracklet candidate";
    case "player_tracklet_candidate":
      return "Player tracklet candidate";
    case "track_point_candidate":
      return "Track point candidate";
    case "player_pose_observation":
      return "Pose observation";
    case "view_state":
      return "Gameplay view-state observation";
    default:
      return observation.observation_type.replaceAll("_", " ");
  }
}

export function observationEvidenceNote(observation: Observation): string {
  if (observation.observation_type === "ball_detection") {
    return "Detection observations are model or fixture outputs. They are evidence, not final ball state.";
  }
  if (observation.observation_type === "player_detection") {
    return "Player detection observations are model or fixture outputs. They do not establish identity.";
  }
  if (observation.observation_type.endsWith("_tracklet_candidate")) {
    return "Tracklet candidates are temporal groupings of source observations. They do not decide object identity or path correctness.";
  }
  if (observation.observation_type === "track_point_candidate") {
    return "Track point candidates keep source detection context inside a candidate grouping.";
  }
  if (observation.observation_type === "player_pose_observation") {
    return "Pose observations are keypoint evidence only. They do not classify strokes, movement, or biomechanics.";
  }
  return "This row is persisted observation evidence. Review annotations and exports do not mutate it.";
}

export function relationshipDescription(relationshipType: string): string {
  switch (relationshipType) {
    case "tracked_from":
      return "Source detection grouped into track point candidate.";
    case "grouped_from":
      return "Track point candidate grouped into tracklet candidate.";
    case "pose_from_subject_detection_candidate":
      return "Pose observation generated from source player detection candidate.";
    case "subject_context_candidate":
      return "Pose observation has candidate subject context from tracklet.";
    case "pose_from_track_point_candidate":
      return "Pose observation has candidate subject context from track point.";
    default:
      return "Observation lineage relationship.";
  }
}

export function annotationDisplayLabel(annotation: HumanAnnotation): string {
  return stringValue(annotation.payload_jsonb.annotation_label) ?? annotation.annotation_type;
}

export function annotationNotes(annotation: HumanAnnotation): string | null {
  return stringValue(annotation.payload_jsonb.notes);
}

export function keypointAnnotationText(annotation: HumanAnnotation): string | null {
  const name = stringValue(annotation.payload_jsonb.keypoint_name);
  const index = scalarValue(annotation.payload_jsonb.keypoint_index);
  if (name === null && index === null) {
    return null;
  }
  return `Keypoint ${name ?? "n/a"}${index !== null ? ` (#${index})` : ""}`;
}

export function booleanFlagText(
  annotation: HumanAnnotation,
  key: string,
  label: string
): string | null {
  return annotation.payload_jsonb[key] === true ? label : null;
}

export function sourceRuntime(observation: Observation): string | null {
  return (
    stringValue(observation.payload_jsonb.source_runtime) ??
    stringValue(observation.payload_jsonb.adapter) ??
    stringValue(observation.pose?.metadata_jsonb.source_runtime)
  );
}

export function frameTimeOwner(observation: Observation): string | null {
  return (
    stringValue(observation.payload_jsonb.frame_time_owner) ??
    stringValue(observation.pose?.frame_time_owner)
  );
}

export function isReviewExportArtifact(artifact: EvidenceArtifact): boolean {
  return artifact.artifact_type.endsWith("_review_dataset_export");
}

export function exportRecordCount(artifact: EvidenceArtifact): string {
  const poseCount = scalarValue(artifact.metadata_jsonb.pose_count);
  if (poseCount !== null) {
    return `${poseCount} pose records`;
  }
  const trackletCount = scalarValue(artifact.metadata_jsonb.tracklet_count);
  if (trackletCount !== null) {
    return `${trackletCount} tracklet records`;
  }
  const recordCount = scalarValue(artifact.metadata_jsonb.record_count);
  if (recordCount !== null) {
    return `${recordCount} records`;
  }
  return "record count n/a";
}

export function stringValue(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

export function scalarValue(value: unknown): string | number | null {
  if (typeof value === "string" && value.length > 0) {
    return value;
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  return null;
}

export function compactJson(value: JsonRecord): string {
  return Object.keys(value).length === 0 ? "{}" : JSON.stringify(value, null, 2);
}
