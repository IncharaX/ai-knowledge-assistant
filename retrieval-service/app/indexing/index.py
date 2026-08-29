import json
from pathlib import Path

from app.embeddings.model import EmbeddingModel
from app.vector_store.chroma import ChromaStore
from app.indexing.quality import should_index


RETRIEVAL_SERVICE_ROOT = Path(__file__).resolve().parents[2]

PROJECT_ROOT = RETRIEVAL_SERVICE_ROOT.parent

CHUNKS_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chunks"
)

def load_chunk_files() -> list[dict]:
    """
    Load all processed chunk JSON files.
    """
    documents = []

    for file_path in sorted(CHUNKS_DIR.glob("*.json")):
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            documents.append(json.load(file))

    return documents


def prepare_records(
    documents: list[dict],
) -> tuple[
    list[str],
    list[str],
    list[dict],
]:
    """
    Convert useful processed chunks into records
    suitable for embedding and storage.
    """

    ids: list[str] = []
    texts: list[str] = []
    metadatas: list[dict] = []

    skipped_chunks = 0

    for document in documents:
        document_id = document["document_id"]
        source = document["source"]

        for chunk in document["chunks"]:
            text = chunk["text"]

            if not should_index(text):
                skipped_chunks += 1
                continue

            page_numbers = chunk["page_numbers"]

            ids.append(chunk["chunk_id"])
            texts.append(text)

            metadatas.append(
                {
                    "document_id": document_id,
                    "source": source,
                    "page_start": min(page_numbers),
                    "page_end": max(page_numbers),
                }
            )

    print(
        f"Skipped {skipped_chunks} low-quality chunks."
    )

    return ids, texts, metadatas


def main() -> None:
    print("Loading processed chunks...")

    documents = load_chunk_files()

    ids, texts, metadatas = prepare_records(
        documents
    )

    print(
        f"Loaded {len(ids)} chunks "
        f"from {len(documents)} documents."
    )

    if not ids:
        raise RuntimeError(
        f"No chunks found in: {CHUNKS_DIR}"
    )

    print("\nLoading embedding model...")

    embedding_model = EmbeddingModel()

    print("Generating embeddings...")

    embeddings = embedding_model.embed_documents(
        texts
    )

    print(
        f"Generated {len(embeddings)} embeddings."
    )

    print("\nConnecting to ChromaDB...")

    store = ChromaStore()

    print("Resetting existing index...")

    store.reset()

    store.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Successfully indexed "
        f"{len(ids)} chunks."
    )

    print(
        f"Current ChromaDB chunk count: "
        f"{store.count()}"
    )


if __name__ == "__main__":
    main()