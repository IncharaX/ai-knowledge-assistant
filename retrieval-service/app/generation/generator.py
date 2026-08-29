from typing import Any

from app.generation.citations import build_sources
from app.generation.llm import OpenRouterLLM
from app.generation.prompt import build_rag_prompt
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.hybrid import HybridRetriever


class RAGGenerator:
    """
    Coordinates hybrid retrieval, cross-encoder
    reranking, grounded generation, and sources.
    """

    def __init__(self) -> None:
        self.retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()
        self.llm = OpenRouterLLM()

    def answer(
        self,
        question: str,
        candidate_k: int = 10,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Retrieve candidates using hybrid search,
        rerank them, generate a grounded answer,
        and return source metadata.
        """

        # Step 1: Hybrid retrieval
        candidates = self.retriever.search(
            query=question,
            top_k=candidate_k,
            candidate_k=candidate_k,
        )

        # Step 2: Cross-encoder reranking
        chunks = self.reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=top_k,
        )

        # Step 3: Build grounded prompt
        prompt = build_rag_prompt(
            question=question,
            chunks=chunks,
        )

        # Step 4: Generate answer
        generated_answer = self.llm.generate(
            prompt=prompt,
        )

        # Step 5: Build deterministic sources
        sources = build_sources(chunks)

        return {
            "answer": generated_answer,
            "sources": sources,
        }