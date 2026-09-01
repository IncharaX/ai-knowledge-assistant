from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.pipeline.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Knowledge Assistant",
    description=(
        "A Retrieval-Augmented Generation (RAG) API "
        "for answering questions from a knowledge base."
    ),
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The question to ask the knowledge assistant.",
        examples=["What is sequential search?"],
    )


class Source(BaseModel):
    source: str
    page_start: int
    page_end: int


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Source]
    answered: bool
    retrieval_score: float | None = None


class HealthResponse(BaseModel):
    status: str


class RootResponse(BaseModel):
    message: str


pipeline = RAGPipeline()


@app.get(
    "/",
    response_model=RootResponse,
    summary="API status",
)
def root():
    return {
        "message": "AI Knowledge Assistant API is running"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/ask",
    response_model=AnswerResponse,
    summary="Ask a question",
    description=(
        "Answers a question using the configured knowledge base "
        "and returns supporting document sources."
    ),
)
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        result = pipeline.answer(
            question=question
        )

        return result

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )