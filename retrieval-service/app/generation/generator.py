from typing import Any

from app.generation.citations import build_sources
from app.generation.llm import OpenRouterLLM
from app.generation.prompt import build_rag_prompt
from app.retrieval.retriever import SemanticRetriever


class RAGGenerator:
    """
    Coordinates retrieval, grounded generation,
    and source construction.
    """

    def __init__(self) -> None:
        self.retriever = SemanticRetriever()
        self.llm = OpenRouterLLM()

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Retrieve context, generate an answer,
        and return deterministic source metadata.
        """

        chunks = self.retriever.search(
            query=question,
            top_k=top_k,
        )

        prompt = build_rag_prompt(
            question=question,
            chunks=chunks,
        )

        answer = self.llm.generate(
            prompt=prompt,
        )

        sources = build_sources(chunks)

        return {
            "answer": answer,
            "sources": sources,
        }