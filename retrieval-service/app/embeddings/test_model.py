from .model import EmbeddingModel


def main() -> None:
    embedding_model = EmbeddingModel()

    text = "An algorithm is a finite sequence of instructions."

    embedding = embedding_model.embed_query(text)

    print("Text:")
    print(text)

    print("\nEmbedding dimensions:")
    print(len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])


if __name__ == "__main__":
    main()