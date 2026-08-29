from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_PATH = PROJECT_ROOT / "storage" / "chroma"

COLLECTION_NAME = "knowledge_chunks"


class ChromaStore:
    """
    Persistent vector store for document chunks.
    """

    def __init__(self) -> None:
        CHROMA_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,
            )
        )

    def upsert(
        self,
        *,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Insert new chunks or update existing chunks.

        Deterministic chunk IDs make re-indexing safe.
        """
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def count(self) -> int:
        """
        Return the number of chunks currently stored.
        """
        return self.collection.count()

    def query(
        self,
        *,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict:
        """
        Search for the most similar document chunks.
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
        ],
    )