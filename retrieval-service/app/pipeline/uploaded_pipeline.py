
from unittest import result

from app.embeddings.model import EmbeddingModel
from app.generation.generator import RAGGenerator
from app.keyword_search.bm25 import BM25Retriever
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.confidence import RetrievalConfidence
from app.retrieval.retriever import SemanticRetriever


class UploadedDocumentPipeline:
    """
    RAG pipeline for a dynamically uploaded PDF.

    Semantic Retrieval
        +
    BM25 Retrieval
        ↓
    Reciprocal Rank Fusion
        ↓
    Reranking
        ↓
    Confidence Check
        ↓
    Answer Generation
    """

    def __init__(
        self,
        collection_name: str,
        bm25_chunks: list[dict],
        embedding_model: EmbeddingModel,
    ) -> None:
        self.document_chunks = bm25_chunks

        self.semantic_retriever = SemanticRetriever(
        collection_name=collection_name,
        embedding_model=embedding_model,
        )

        self.bm25_retriever = BM25Retriever(
        chunks=bm25_chunks
        )

        self.reranker = CrossEncoderReranker()
        self.confidence = RetrievalConfidence()
        self.generator = RAGGenerator()

    def answer(
        self,
        question: str,
        candidate_k: int = 18,
        top_k: int = 5,
        rrf_k: int = 60,
    ) -> dict:
        """
        Answer a question using only the uploaded PDF.
        """

        # Semantic retrieval
        semantic_results = self.semantic_retriever.search(
            query=question,
            top_k=candidate_k,
        )

        # BM25 retrieval
        bm25_results = self.bm25_retriever.search(
            query=question,
            top_k=candidate_k,
        )

        # Reciprocal Rank Fusion
        fused_results: dict[str, dict] = {}

        self._add_results(
            fused_results=fused_results,
            results=semantic_results,
            rrf_k=rrf_k,
            retrieval_method="semantic",
        )

        self._add_results(
            fused_results=fused_results,
            results=bm25_results,
            rrf_k=rrf_k,
            retrieval_method="bm25",
        )

        candidates = sorted(
            fused_results.values(),
            key=lambda result: result["rrf_score"],
            reverse=True,
        )[:candidate_k]

        # Reranking
        reranked_chunks = self.reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=top_k,
        )

        # Confidence check
        confidence_result = self.confidence.evaluate(
            reranked_chunks
        )

        if not confidence_result["is_sufficient"]:
            return {
                "answer": (
                    "I don't have enough information in the "
                    "uploaded document to answer that reliably."
                ),
                "sources": [],
                "answered": False,
                "retrieval_score": confidence_result[
                    "top_score"
                ],
            }

        # Generate grounded answer
        result = self.generator.answer(
            question=question,
            chunks=reranked_chunks,
        )

        result["retrieval_score"] = confidence_result["top_score"]

        return result

    def summarize(self) -> dict:
        """
        Generate a summary using the uploaded document.
        """

        document_chunks = self.document_chunks[:10]

        result = self.generator.answer(
            question=(
                "Provide a clear and concise summary of the "
                "uploaded document. Cover the main topics, "
                "important points, and key conclusions."
            ),
            chunks=document_chunks,
        )

        result["answered"] = True

        return result

    def get_main_topic(self) -> dict:
        """
        Identify the main topic of the uploaded document.
        """

        document_chunks = self.document_chunks[:10]

        result = self.generator.answer(
            question=(
                "What is the main topic of this uploaded document? "
                "Answer briefly and clearly. Focus on the central "
                "subject or purpose of the document."
            ),
            chunks=document_chunks,
        )

        result["answered"] = True

        return result

    def _add_results(
        self,
        fused_results: dict[str, dict],
        results: list[dict],
        rrf_k: int,
        retrieval_method: str,
    ) -> None:
        """
        Add retrieval results using Reciprocal Rank Fusion.
        """

        for rank, result in enumerate(
            results,
            start=1,
        ):
            chunk_id = result["chunk_id"]

            rrf_score = 1 / (rrf_k + rank)

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "rrf_score": 0.0,
                    "retrieval_methods": [],
                }

            fused_results[chunk_id]["rrf_score"] += rrf_score

            fused_results[chunk_id][
                "retrieval_methods"
            ].append(retrieval_method)