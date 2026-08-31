import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.question || !body.question.trim()) {
      return NextResponse.json(
        {
          error: "Question is required.",
        },
        {
          status: 400,
        }
      );
    }

    const response = await fetch(
      `${process.env.RETRIEVAL_SERVICE_URL}/ask`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: body.question.trim(),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        {
          error:
            data.error ||
            "The AI Knowledge Assistant could not process your question.",
        },
        {
          status: response.status,
        }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("API Error:", error);

    return NextResponse.json(
      {
        error:
          "Unable to connect to the AI Knowledge Assistant. Please try again later.",
      },
      {
        status: 500,
      }
    );
  }
}