from app.generation.generator import RAGGenerator


def main() -> None:

    generator = RAGGenerator()

    question = (
        "Explain Euclid's algorithm "
        "for finding GCD."
    )

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(f"\n{question}")

    print("\n" + "=" * 80)
    print("GENERATING ANSWER...")
    print("=" * 80)

    result = generator.answer(
        question=question,
        candidate_k=10,
        top_k=5,
    )

    print("\nANSWER:\n")
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
            f"{source['page_start']}"
            f"-{source['page_end']})"
        )


if __name__ == "__main__":
    main()