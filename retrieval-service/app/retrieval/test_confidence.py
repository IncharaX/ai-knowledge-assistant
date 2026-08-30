from app.reranking.reranker import CrossEncoderReranker
from app.retrieval.confidence import RetrievalConfidence
from app.retrieval.hybrid import HybridRetriever


def main() -> None:
    retriever = HybridRetriever()
    reranker = CrossEncoderReranker()
    confidence = RetrievalConfidence()

    questions = [
        "Explain Euclid's algorithm for finding GCD.",
        "What is Big O notation?",
        "Explain graph traversal.",
        "What is quantum entanglement?",
        "How does photosynthesis work?",
        "What is sequential search?",
    ]

    for question in questions:

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        candidates = retriever.search(
            query=question,
            top_k=10,
            candidate_k=10,
        )

        chunks = reranker.rerank(
            query=question,
            candidates=candidates,
            top_k=5,
        )

        result = confidence.evaluate(
            chunks=chunks,
        )

        print("\nTOP RERANK SCORE:")
        print(result["top_score"])
        
        print("\nSUFFICIENT EVIDENCE:")
        print(result["is_sufficient"])

        print("\nTOP RESULT:")

        if chunks:
            metadata = chunks[0]["metadata"]

            print(
                f"Source: {metadata['source']}"
            )

            print(
                "Pages: "
                f"{metadata['page_start']}"
                "-"
                f"{metadata['page_end']}"
            )

            print("\nText preview:")

            print(
                chunks[0]["text"][:300]
            )


if __name__ == "__main__":
    main()