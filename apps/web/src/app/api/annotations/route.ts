import { NextResponse } from "next/server";

import { getApiBaseUrl } from "../../../lib/api";

export async function POST(request: Request) {
  const payload = await request.json();
  const response = await fetch(`${getApiBaseUrl()}/annotations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const body = await response.json();
  return NextResponse.json(body, { status: response.status });
}
