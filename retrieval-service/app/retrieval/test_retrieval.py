from app.retrieval.retriever import SemanticRetriever


def main() -> None:
    retriever = SemanticRetriever()

    query = "What is the difference between Big O and Theta notation?"

    print(f"\nQuery: {query}\n")

    results = retriever.search(
        query=query,
        top_k=5,
    )

    print(f"Found {len(results)} results.\n")

    for index, result in enumerate(results, start=1):
        print("=" * 80)

        print(f"Result #{index}")

        print(
            f"\nSource: "
            f"{result['metadata']['source']}"
        )

        print(
            f"Pages: "
            f"{result['metadata']['page_start']}"
            f"-"
            f"{result['metadata']['page_end']}"
        )

        print(
            f"\nDistance: "
            f"{result['distance']:.4f}"
        )

        print("\nText:")

        print(result["text"][:800])

        print()


if __name__ == "__main__":
    main()