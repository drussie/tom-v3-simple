import { NextResponse } from "next/server";

import { getApiBaseUrl } from "../../../../../lib/api";

interface RouteContext {
  params: Promise<{
    mediaId: string;
  }>;
}

export async function GET(request: Request, context: RouteContext) {
  const { mediaId } = await context.params;
  const url = new URL(request.url);
  const response = await fetch(
    `${getApiBaseUrl()}/replay/${encodeURIComponent(mediaId)}/trajectory-3d-debug-reviews?${url.searchParams}`,
    { cache: "no-store" }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}

export async function POST(request: Request, context: RouteContext) {
  const { mediaId } = await context.params;
  const payload = await request.json();
  const response = await fetch(
    `${getApiBaseUrl()}/replay/${encodeURIComponent(mediaId)}/trajectory-3d-debug-reviews`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
