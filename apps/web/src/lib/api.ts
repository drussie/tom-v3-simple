import type { ViewerRun } from "./types";

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
