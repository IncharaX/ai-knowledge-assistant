from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.pipeline.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Knowledge Assistant",
    description="RAG-powered knowledge assistant API",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )


pipeline = RAGPipeline()


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Assistant API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
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