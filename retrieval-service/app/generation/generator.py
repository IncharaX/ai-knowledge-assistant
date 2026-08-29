from app.generation.llm import OpenRouterLLM
from app.generation.prompt import build_rag_prompt


class Generator:
    """
    Generates grounded answers using
    trusted retrieved chunks.
    """

    def __init__(self) -> None:
        self.llm = OpenRouterLLM()

    def answer(
        self,
        question: str,
        chunks: list[dict],
    ) -> str:
        """
        Generate an answer using only
        the provided retrieved context.
        """

        prompt = build_rag_prompt(
            question=question,
            chunks=chunks,
        )

        return self.llm.generate(
            prompt=prompt,
        )