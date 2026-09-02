import { NextResponse } from "next/server";

const RETRIEVAL_SERVICE_URL =
  process.env.RETRIEVAL_SERVICE_URL ||
  "http://127.0.0.1:8000";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const response = await fetch(
      `${RETRIEVAL_SERVICE_URL}/ask-uploaded`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        data,
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      {
        detail:
          "Unable to connect to the retrieval service.",
      },
      { status: 503 }
    );
  }
}