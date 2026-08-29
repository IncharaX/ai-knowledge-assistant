from app.retrieval.hybrid import HybridRetriever


def main() -> None:
    retriever = HybridRetriever()

    query = "Explain Euclid's algorithm for finding GCD."

    print("\n" + "=" * 80)
    print("HYBRID RETRIEVAL TEST")
    print("=" * 80)

    print(f"\nQuery: {query}")

    results = retriever.search(
        query=query,
        top_k=5,
        candidate_k=10,
    )

    print(
        f"\nFound {len(results)} fused results."
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
            "\nRetrieved by: "
            + ", ".join(
                result["retrieval_methods"]
            )
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()