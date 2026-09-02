import json
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi

from app.indexing.quality import should_index


RETRIEVAL_SERVICE_ROOT = Path(__file__).resolve().parents[2]

PROJECT_ROOT = RETRIEVAL_SERVICE_ROOT.parent

CHUNKS_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chunks"
)


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase tokens
    for BM25 indexing and querying.
    """

    return re.findall(
        r"\b\w+\b",
        text.lower(),
    )


class BM25Retriever:
    """
    Keyword-based document retriever using BM25.
    """

    def __init__(
        self,
        chunks: list[dict[str, Any]] | None = None,
    ) -> None:
        self.chunks = (
            chunks
            if chunks is not None
            else self._load_chunks()
        )

        if not self.chunks:
            raise ValueError(
                "No processed chunks found. "
                "Run the ingestion pipeline first."
            )

        tokenized_corpus = [
            tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.index = BM25Okapi(
            tokenized_corpus
        )

    def _load_chunks(self) -> list[dict[str, Any]]:
        """
        Load and prepare indexable chunks from
        all processed document JSON files.
        """

        chunks = []

        for file_path in sorted(CHUNKS_DIR.glob("*.json")):

            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                document = json.load(file)

            document_id = document["document_id"]
            source = document["source"]

            for chunk in document["chunks"]:

                text = chunk["text"]

                # Keep BM25 and semantic indexing
                # consistent.
                if not should_index(text):
                    continue

                page_numbers = chunk["page_numbers"]

                chunks.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "text": text,
                        "metadata": {
                            "document_id": document_id,
                            "source": source,
                            "page_start": min(page_numbers),
                            "page_end": max(page_numbers),
                        },
                    }
                )

        return chunks

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search for chunks using BM25 keyword ranking.
        """

        tokenized_query = tokenize(query)

        scores = self.index.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:

            chunk = self.chunks[index]

            results.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "score": float(scores[index]),
                }
            )

        return results