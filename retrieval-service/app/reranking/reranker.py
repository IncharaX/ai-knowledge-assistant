from sentence_transformers import CrossEncoder


MODEL_NAME = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


class CrossEncoderReranker:
    """
    Re-ranks retrieved chunks based on their
    relevance to the user's query.
    """

    def __init__(self) -> None:
        self.model = CrossEncoder(
            MODEL_NAME
        )

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Score query-document pairs and return
        the most relevant candidates.
        """

        if not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        scores = self.model.predict(
            pairs
        )

        reranked_results = []

        for candidate, score in zip(
            candidates,
            scores,
        ):
            result = candidate.copy()

            result["rerank_score"] = float(score)

            reranked_results.append(result)

        reranked_results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return reranked_results[:top_k]