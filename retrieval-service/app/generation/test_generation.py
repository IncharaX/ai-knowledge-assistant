from app.generation.generator import RAGGenerator
from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.hybrid import HybridRetriever


def main() -> None:
    retriever = HybridRetriever()
    reranker = CrossEncoderReranker()
    generator = RAGGenerator()

    question = (
        "Explain Euclid's algorithm "
        "for finding GCD."
    )

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)

    print("\nRetrieving candidates...")

    candidates = retriever.search(
        query=question,
        top_k=10,
        candidate_k=10,
    )

    print(
        f"Retrieved {len(candidates)} candidates."
    )

    print("\nReranking candidates...")

    chunks = reranker.rerank(
        query=question,
        candidates=candidates,
        top_k=5,
    )

    print(
        f"Using {len(chunks)} chunks for generation."
    )

    print("\nGenerating answer...")

    result = generator.answer(
        question=question,
        chunks=chunks,
    )

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):
        print(
            f"\n[{index}] "
            f"{source['source']} "
            f"(Pages "
            f"{source['page_start']}-"
            f"{source['page_end']})"
        )


if __name__ == "__main__":
    main()