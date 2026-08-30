from typing import Any


class RetrievalConfidence:
    """
    Evaluates whether reranked retrieval results
    provide sufficient evidence to answer a query.

    The cross-encoder score is treated as a relevance
    signal, not as a probability.
    """

    CONFIDENCE_THRESHOLD = -5.0

    def evaluate(
        self,
        chunks: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not chunks:
            return {
                "top_score": None,
                "is_sufficient": False,
            }

        top_score = chunks[0].get(
            "rerank_score"
        )

        if top_score is None:
            raise ValueError(
                "Chunks must contain rerank_score "
                "before confidence can be evaluated."
            )

        top_score = float(top_score)

        return {
            "top_score": top_score,
            "is_sufficient": (
                top_score > self.CONFIDENCE_THRESHOLD
            ),
        }