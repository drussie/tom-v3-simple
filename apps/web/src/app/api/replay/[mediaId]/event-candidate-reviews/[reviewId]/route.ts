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
    `${getApiBaseUrl()}/replay/${encodeURIComponent(mediaId)}/event-candidate-reviews/${encodeURIComponent(reviewId)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}

export async function DELETE(_request: Request, context: RouteContext) {
  const { mediaId, reviewId } = await context.params;
  const response = await fetch(
    `${getApiBaseUrl()}/replay/${encodeURIComponent(mediaId)}/event-candidate-reviews/${encodeURIComponent(reviewId)}`,
    { method: "DELETE" }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
