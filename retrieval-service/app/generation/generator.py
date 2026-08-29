from app.generation.llm import OpenRouterLLM
from app.generation.prompt import build_rag_prompt
from app.retrieval.retriever import SemanticRetriever


class RAGGenerator:
    """
    Coordinates retrieval and answer generation.
    """

    def __init__(self) -> None:
        self.retriever = SemanticRetriever()
        self.llm = OpenRouterLLM()

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve relevant context and generate
        a grounded answer.
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

        return answer