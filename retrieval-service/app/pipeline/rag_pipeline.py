from app.generation.generator import Generator
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.hybrid import HybridRetriever


class RAGPipeline:
    """
    Orchestrates the complete RAG pipeline:

    Hybrid Retrieval
        ↓
    Cross-Encoder Reranking
        ↓
    Answer Generation
    """

    def __init__(self) -> None:
        self.retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()
        self.generator = Generator()

    def answer(
        self,
        question: str,
        candidate_k: int = 10,
        top_k: int = 5,
    ) -> dict:
        """
        Run the complete RAG pipeline and return
        the generated answer with its sources.
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

        # Step 3: Generate answer
        answer = self.generator.answer(
            question=question,
            chunks=reranked_chunks,
        )

        # Step 4: Return the complete pipeline result
        return {
            "answer": answer,
            "sources": reranked_chunks,
        }