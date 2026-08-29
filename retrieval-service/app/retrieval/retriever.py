from app.embeddings.model import EmbeddingModel
from app.vector_store.chroma import ChromaStore


class SemanticRetriever:
    """
    Retrieves semantically relevant chunks
    from the vector database.
    """

    def __init__(self) -> None:
        self.embedding_model = EmbeddingModel()
        self.vector_store = ChromaStore()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search the knowledge base for chunks
        relevant to the user's query.
        """

        query_embedding = (
            self.embedding_model.embed_query(query)
        )

        results = self.vector_store.query(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        retrieved_chunks = []

        for document, metadata, distance, chunk_id in zip(
            documents,
            metadatas,
            distances,
            ids,
        ):
            retrieved_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_chunks