import { NextResponse } from "next/server";

import { getApiBaseUrl } from "../../../../lib/api";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const response = await fetch(`${getApiBaseUrl()}/replay/overlays?${url.searchParams}`, {
    cache: "no-store"
  });
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
