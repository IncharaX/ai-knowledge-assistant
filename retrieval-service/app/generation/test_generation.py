from app.generation.generator import RAGGenerator


def main() -> None:
    generator = RAGGenerator()

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
        print("GENERATING ANSWER...")
        print("=" * 80)

        result = generator.answer(
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
                print(
                    f"\n[{index}] "
                    f"{source['source']} "
                    f"(Pages "
                    f"{source['page_start']}-"
                    f"{source['page_end']})"
                )


if __name__ == "__main__":
    main()