import json
from pathlib import Path

from app.indexing.quality import should_index


RETRIEVAL_SERVICE_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = RETRIEVAL_SERVICE_ROOT.parent

CHUNKS_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chunks"
)


def main() -> None:
    for file_path in sorted(CHUNKS_DIR.glob("*.json")):

        print("\n" + "=" * 80)
        print(f"FILE: {file_path.name}")
        print("=" * 80)

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            document = json.load(file)

        for chunk in document["chunks"]:

            chunk_id = chunk["chunk_id"]
            text = chunk["text"]

            indexed = should_index(text)

            status = "INDEXED ✅" if indexed else "SKIPPED ❌"

            print(f"\n{chunk_id} — {status}")
            print("-" * 80)
            print(text[:500])
            print()


if __name__ == "__main__":
    main()