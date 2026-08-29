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

    answer = generator.answer(
        question=question,
        top_k=5,
    )

    print(answer)


if __name__ == "__main__":
    main()