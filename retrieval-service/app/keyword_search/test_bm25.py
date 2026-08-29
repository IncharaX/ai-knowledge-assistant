from app.keyword_search.bm25 import BM25Retriever


def main() -> None:
    retriever = BM25Retriever()

    query = "What is Euclid's algorithm?"

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retriever.search(
        query=query,
        top_k=5,
    )

    print(
        f"\nFound {len(results)} results."
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
            f"\nBM25 Score: "
            f"{result['score']:.4f}"
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()