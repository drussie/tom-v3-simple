import { NextResponse } from "next/server";

import { getApiBaseUrl } from "../../../../../lib/api";

interface RouteContext {
  params: Promise<{
    trackletId: string;
  }>;
}

export async function GET(_request: Request, context: RouteContext) {
  const { trackletId } = await context.params;
  const response = await fetch(
    `${getApiBaseUrl()}/tracklets/${trackletId}/evidence-bundle`,
    { cache: "no-store" }
  );
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
