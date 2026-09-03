from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.embeddings.model import EmbeddingModel
from app.ingestion.upload import process_uploaded_pdf
from app.pipeline.rag_pipeline import RAGPipeline
from app.pipeline.uploaded_pipeline import UploadedDocumentPipeline


app = FastAPI(
    title="AI Knowledge Assistant",
    description=(
        "A Retrieval-Augmented Generation (RAG) API "
        "for answering questions from a knowledge base."
    ),
    version="1.1.0",
)


UPLOADS_DIR = Path("/tmp/uploads")
UPLOADS_DIR.mkdir(
    parents=True,
    exist_ok=True,
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


class UploadResponse(BaseModel):
    document_id: str
    source: str
    chunk_count: int
    message: str


pipeline = RAGPipeline()

embedding_model = EmbeddingModel()

uploaded_pipeline: UploadedDocumentPipeline | None = None


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
    summary="Ask the knowledge base",
)
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    try:
        return pipeline.answer(question=question)

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@app.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload a PDF",
)
async def upload_pdf(
    file: UploadFile = File(...),
):
    global uploaded_pipeline

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a PDF file.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    upload_id = uuid4().hex

    file_path = (
        UPLOADS_DIR
        / f"{upload_id}.pdf"
    )

    try:
        contents = await file.read()

        file_path.write_bytes(contents)

        result = process_uploaded_pdf(
            pdf_path=file_path,
            original_filename=file.filename,
            embedding_model=embedding_model,
        )

        uploaded_pipeline = UploadedDocumentPipeline(
            collection_name=result["collection_name"],
            bm25_chunks=result["bm25_chunks"],
            embedding_model=embedding_model,
        )

        return {
            "document_id": result["document_id"],
            "source": file.filename,
            "chunk_count": result["chunk_count"],
            "message": (
                "PDF uploaded and processed successfully."
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    finally:
        await file.close()


@app.post(
    "/ask-uploaded",
    response_model=AnswerResponse,
    summary="Ask the uploaded PDF",
)
def ask_uploaded_question(
    request: QuestionRequest,
):
    if uploaded_pipeline is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Please upload a PDF before asking questions "
                "about an uploaded document."
            ),
        )

    question = request.question.strip()

    try:
        return uploaded_pipeline.answer(
            question=question
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@app.post(
    "/summarize-uploaded",
    response_model=AnswerResponse,
    summary="Summarize the uploaded PDF",
)

def summarize_uploaded_document():
    if uploaded_pipeline is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Please upload a PDF before requesting "
                "a document summary."
            ),
        )

    try:
        return uploaded_pipeline.summarize()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

@app.post(
    "/main-topic-uploaded",
    response_model=AnswerResponse,
    summary="Get the main topic of the uploaded PDF",
)
def get_uploaded_main_topic():
    if uploaded_pipeline is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Please upload a PDF before requesting "
                "its main topic."
            ),
        )

    try:
        return uploaded_pipeline.get_main_topic()

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )    