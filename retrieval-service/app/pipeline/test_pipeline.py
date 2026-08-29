from app.pipeline.rag_pipeline import RAGPipeline


def main() -> None:
    pipeline = RAGPipeline()

    questions = [
        "Explain Euclid's algorithm for finding GCD.",
        "What is quantum entanglement?",
    ]

    for question in questions:

        print("\n" + "=" * 80)
        print("QUESTION")
        print("=" * 80)

        print(question)

        print("\n" + "=" * 80)
        print("PROCESSING...")
        print("=" * 80)

        result = pipeline.answer(
            question=question
        )

        print("\nANSWER:\n")
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
                metadata = source["metadata"]

                print(
                    f"\n[{index}] "
                    f"{metadata['source']} "
                    f"(Pages "
                    f"{metadata['page_start']}-"
                    f"{metadata['page_end']})"
                )


if __name__ == "__main__":
    main()