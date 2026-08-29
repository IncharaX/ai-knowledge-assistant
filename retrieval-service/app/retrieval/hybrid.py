from app.keyword_search.bm25 import BM25Retriever
from app.retrieval.retriever import SemanticRetriever


class HybridRetriever:
    """
    Combines semantic retrieval and BM25 keyword retrieval
    using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self) -> None:
        self.semantic_retriever = SemanticRetriever()
        self.bm25_retriever = BM25Retriever()

    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 10,
        rrf_k: int = 60,
    ) -> list[dict]:
        """
        Retrieve candidates from semantic and keyword search,
        then combine their rankings using RRF.
        """

        semantic_results = self.semantic_retriever.search(
            query=query,
            top_k=candidate_k,
        )

        bm25_results = self.bm25_retriever.search(
            query=query,
            top_k=candidate_k,
        )

        fused_results: dict[str, dict] = {}

        self._add_results(
            fused_results=fused_results,
            results=semantic_results,
            rrf_k=rrf_k,
            retrieval_method="semantic",
        )

        self._add_results(
            fused_results=fused_results,
            results=bm25_results,
            rrf_k=rrf_k,
            retrieval_method="bm25",
        )

        ranked_results = sorted(
            fused_results.values(),
            key=lambda result: result["rrf_score"],
            reverse=True,
        )

        return ranked_results[:top_k]

    def _add_results(
        self,
        fused_results: dict[str, dict],
        results: list[dict],
        rrf_k: int,
        retrieval_method: str,
    ) -> None:
        """
        Add ranked retrieval results to the fused result set.
        """

        for rank, result in enumerate(
            results,
            start=1,
        ):
            chunk_id = result["chunk_id"]

            rrf_score = 1 / (
                rrf_k + rank
            )

            if chunk_id not in fused_results:

                fused_results[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "rrf_score": 0.0,
                    "retrieval_methods": [],
                }

            fused_results[chunk_id]["rrf_score"] += rrf_score

            fused_results[chunk_id][
                "retrieval_methods"
            ].append(retrieval_method)