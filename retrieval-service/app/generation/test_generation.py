from app.generation.generator import RAGGenerator


def main() -> None:
    generator = RAGGenerator()

    question = (
        "Explain Euclid's algorithm for finding GCD."
    )

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)

    print("\n" + "=" * 80)
    print("GENERATING ANSWER...")
    print("=" * 80 + "\n")

    response = generator.answer(
        question=question,
        top_k=5,
    )

    print("ANSWER:\n")

    print(response["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for index, source in enumerate(
        response["sources"],
        start=1,
    ):
        print(
            f"\n[{index}] "
            f"{source['source']} "
            f"(Pages {source['page_start']}"
            f"-{source['page_end']})"
        )


if __name__ == "__main__":
    main()