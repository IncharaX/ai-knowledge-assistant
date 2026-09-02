from pathlib import Path
from uuid import uuid4

from app.embeddings.model import EmbeddingModel
from app.indexing.quality import should_index
from app.ingestion.chunker import chunk_document
from app.ingestion.pdf import extract_pdf
from app.vector_store.chroma import ChromaStore


def process_uploaded_pdf(
    pdf_path: Path,
    original_filename: str,
    embedding_model: EmbeddingModel,
) -> dict:
    """
    Process an uploaded PDF into a separate vector collection.

    The returned chunks can also be used to build
    a BM25 index for hybrid retrieval.
    """

    pages = extract_pdf(pdf_path)

    if not pages:
        raise ValueError(
            "No readable text was found in the uploaded PDF."
        )

    chunks = chunk_document(pages)

    document_id = uuid4().hex
    collection_name = f"upload_{document_id}"

    ids: list[str] = []
    texts: list[str] = []
    metadatas: list[dict] = []
    bm25_chunks: list[dict] = []

    for index, chunk in enumerate(chunks):
        if not should_index(chunk.text):
            continue

        chunk_id = f"{document_id}_{index}"

        metadata = {
            "document_id": document_id,
            "source": original_filename,
            "page_start": min(chunk.page_numbers),
            "page_end": max(chunk.page_numbers),
        }

        ids.append(chunk_id)
        texts.append(chunk.text)
        metadatas.append(metadata)

        bm25_chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk.text,
                "metadata": metadata,
            }
        )

    if not texts:
        raise ValueError(
            "The uploaded PDF did not contain enough useful text."
        )

    embeddings = embedding_model.embed_documents(texts)

    store = ChromaStore(
        collection_name=collection_name
    )

    store.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return {
        "document_id": document_id,
        "collection_name": collection_name,
        "source": original_filename,
        "chunk_count": len(texts),
        "bm25_chunks": bm25_chunks,
    }