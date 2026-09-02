from typing import Any

from app.generation.citations import build_sources
from app.generation.llm import OpenRouterLLM
from app.generation.prompt import build_rag_prompt


class RAGGenerator:
    """
    Generates grounded answers from
    already retrieved chunks.
    """

    def __init__(self) -> None:
        self.llm = OpenRouterLLM()

    def answer(
        self,
        question: str,
        chunks: list[dict[str, Any]],
    ) -> dict[str, Any]:

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
            "answered": True,
        }