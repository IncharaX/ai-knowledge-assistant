from app.generation.generator import Generator
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.confidence import RetrievalConfidence
from app.retrieval.hybrid import HybridRetriever


REFUSAL_MESSAGE = (
    "I don't have enough information in the provided "
    "knowledge base to answer that reliably."
)


class RAGPipeline:
    """
    Orchestrates the complete RAG pipeline:

    Hybrid Retrieval
        ↓
    Cross-Encoder Reranking
        ↓
    Retrieval Confidence Check
        ↓
    Generate Answer or Refuse
    """

    def __init__(self) -> None:
        self.retriever = HybridRetriever()

        self.reranker = CrossEncoderReranker()

        self.confidence = RetrievalConfidence()

        self.generator = Generator()

    def answer(
        self,
        question: str,
        candidate_k: int = 10,
        top_k: int = 5,
    ) -> dict:
        """
        Run the complete RAG pipeline.

        Generate an answer only when sufficient
        retrieval evidence exists.
        """

        # Step 1: Hybrid retrieval
        candidates = self.retriever.search(
            query=question,
            top_k=candidate_k,
            candidate_k=candidate_k,
        )

        # Step 2: Cross-encoder reranking
        reranked_chunks = self.reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=top_k,
        )

        # Step 3: Evaluate retrieval confidence
        confidence_result = self.confidence.evaluate(
            reranked_chunks
        )

        # Step 4: Refuse when evidence is insufficient
        if not confidence_result["is_sufficient"]:
            return {
                "answer": REFUSAL_MESSAGE,
                "sources": [],
                "answered": False,
                "retrieval_score": confidence_result[
                    "top_score"
                ],
            }

        # Step 5: Generate grounded answer
        answer = self.generator.answer(
            question=question,
            chunks=reranked_chunks,
        )

        # Step 6: Return complete pipeline result
        return {
            "answer": answer,
            "sources": reranked_chunks,
            "answered": True,
            "retrieval_score": confidence_result[
                "top_score"
            ],
        }