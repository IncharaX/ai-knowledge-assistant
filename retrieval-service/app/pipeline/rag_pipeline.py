from app.generation.generator import RAGGenerator
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.confidence import RetrievalConfidence


class RAGPipeline:
    """
    Complete RAG pipeline.

    Hybrid Retrieval
        ↓
    Cross-Encoder Reranking
        ↓
    Confidence Check
        ↓
    Answer Generation
    """

    def __init__(self) -> None:
        self.retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()
        self.confidence = RetrievalConfidence()
        self.generator = RAGGenerator()

    def answer(
        self,
        question: str,
        candidate_k: int = 18,
        top_k: int = 5,
    ) -> dict:

        candidate_k: int = 18

        # Step 1: Hybrid retrieval
        candidates = self.retriever.search(
            query=question,
            top_k=candidate_k,
            candidate_k=candidate_k,
        )

        # Step 2: Reranking
        reranked_chunks = self.reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=top_k,
        )

        # Step 3: Confidence check
        confidence_result = self.confidence.evaluate(
            reranked_chunks
        )

        # Step 4: Refuse if evidence is insufficient
        if not confidence_result["is_sufficient"]:
            return {
                "answer": (
                    "I don't have enough information in the "
                    "provided knowledge base to answer that reliably."
                ),
                "sources": [],
                "answered": False,
                "retrieval_score": confidence_result[
                    "top_score"
                ],
            }

        # Step 5: Generate grounded answer
        result = self.generator.answer(
            question=question,
            chunks=reranked_chunks,
        )

        return result