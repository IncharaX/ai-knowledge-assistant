from .chroma import ChromaStore


def main() -> None:
    store = ChromaStore()

    print("ChromaDB initialized successfully.")

    print(
        f"Current chunk count: {store.count()}"
    )


if __name__ == "__main__":
    main()