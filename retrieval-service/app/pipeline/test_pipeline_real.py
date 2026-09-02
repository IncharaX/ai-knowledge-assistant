from app.pipeline.rag_pipeline import RAGPipeline


def main() -> None:
    pipeline = RAGPipeline()

    questions = [
        "Explain Euclid's algorithm for finding GCD.",
        "What is Big O notation?",
        "What is quantum entanglement?",
        "How does photosynthesis work?",
        "What is sequential search?",
    ]

    for question in questions:

        print("\n" + "=" * 80)
        print("QUESTION")
        print("=" * 80)

        print(question)

        print("\nProcessing...")

        result = pipeline.answer(
            question=question
        )

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)

        print(result["answer"])

        print("\nANSWERED:")
        print(result["answered"])

        print("\nRETRIEVAL SCORE:")
        print(result["retrieval_score"])

        print("\n" + "=" * 80)
        print("SOURCES")
        print("=" * 80)

        if not result["sources"]:
            print("No sources returned.")

        else:
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