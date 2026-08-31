from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.pipeline.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Knowledge Assistant",
    description="RAG-powered knowledge assistant API",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


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
    try:
        result = pipeline.answer(
            question=request.question
        )

        return result

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        )