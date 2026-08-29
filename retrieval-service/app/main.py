from fastapi import FastAPI
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


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = pipeline.answer(
        question=request.question
    )

    return result