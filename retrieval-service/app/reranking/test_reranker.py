from app.reranking.reranker import (
    CrossEncoderReranker,
)

from app.retrieval.hybrid import HybridRetriever


def main() -> None:

    query = (
        "Explain Euclid's algorithm "
        "for finding GCD."
    )

    print("\n" + "=" * 80)
    print("CROSS-ENCODER RERANKING TEST")
    print("=" * 80)

    print(f"\nQuery: {query}")

    print("\nRetrieving candidates...")

    hybrid_retriever = HybridRetriever()

    candidates = hybrid_retriever.search(
        query=query,
        top_k=10,
        candidate_k=10,
    )

    print(
        f"Retrieved {len(candidates)} candidates."
    )

    print("\nLoading reranker...")

    reranker = CrossEncoderReranker()

    results = reranker.rerank(
        query=query,
        candidates=candidates,
        top_k=5,
    )

    print(
        f"\nReturning top {len(results)} results."
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print("\n" + "=" * 80)
        print(f"Result #{rank}")
        print("=" * 80)

        print(
            f"\nSource: "
            f"{result['metadata']['source']}"
        )

        print(
            f"Pages: "
            f"{result['metadata']['page_start']}"
            f"-{result['metadata']['page_end']}"
        )

        print(
            f"\nRRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"Rerank Score: "
            f"{result['rerank_score']:.4f}"
        )

        print(
            "\nRetrieved by: "
            + ", ".join(
                result["retrieval_methods"]
            )
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()