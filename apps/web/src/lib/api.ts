import type { HumanAnnotation, JsonRecord, TrackletEvidenceBundle, ViewerRun } from "./types";

const defaultApiBaseUrl = "http://127.0.0.1:8000";

export function getApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_TOM_V3_API_BASE_URL ?? defaultApiBaseUrl;
}

export async function fetchViewerRun(runId: string): Promise<ViewerRun> {
  const response = await fetch(`${getApiBaseUrl()}/viewer/runs/${runId}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load run ${runId}: ${response.status}`);
  }

  return (await response.json()) as ViewerRun;
}

export async function fetchTrackletEvidenceBundle(
  trackletId: string
): Promise<TrackletEvidenceBundle> {
  const response = await fetch(`/api/tracklets/${trackletId}/evidence-bundle`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Unable to load tracklet evidence bundle ${trackletId}: ${response.status}`);
  }

  return (await response.json()) as TrackletEvidenceBundle;
}

export interface CreateAnnotationInput {
  media_id?: string | null;
  observation_id?: string | null;
  evidence_artifact_id?: string | null;
  frame_start?: number | null;
  frame_end?: number | null;
  timestamp_start_ms?: number | null;
  timestamp_end_ms?: number | null;
  annotation_type: string;
  payload_jsonb?: JsonRecord;
  created_by?: string | null;
}

export async function createAnnotation(
  input: CreateAnnotationInput
): Promise<HumanAnnotation> {
  const response = await fetch("/api/annotations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error(`Unable to create annotation: ${response.status}`);
  }

  return (await response.json()) as HumanAnnotation;
}
