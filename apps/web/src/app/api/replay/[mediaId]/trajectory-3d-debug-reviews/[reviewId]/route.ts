import { NextResponse } from "next/server";

import { getApiBaseUrl } from "../../../../../../lib/api";

interface RouteContext {
  params: Promise<{
    mediaId: string;
    reviewId: string;
  }>;
}

export async function PATCH(request: Request, context: RouteContext) {
  const { mediaId, reviewId } = await context.params;
  const payload = await request.json();
  const response = await fetch(
    `${getApiBaseUrl()}/replay/${encodeURIComponent(mediaId)}/trajectory-3d-debug-reviews/${encodeURIComponent(reviewId)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
