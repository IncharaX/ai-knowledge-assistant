import json
from pathlib import Path

from .chunker import chunk_document, count_tokens
from .pdf import extract_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHUNKS_DIR = PROCESSED_DIR / "chunks"


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def process_document(pdf_path: Path) -> None:
    pages = extract_pdf(pdf_path)

    if not pages:
        raise ValueError(
            f"No readable text found in '{pdf_path.name}'. "
            "The PDF may be image-based or contain unsupported content."
        )

    document = {
        "document_id": pdf_path.stem,
        "source": pdf_path.name,
        "pages": pages,
    }

    document_output = PROCESSED_DIR / f"{pdf_path.stem}.json"
    write_json(document_output, document)

    chunks = chunk_document(pages)

    chunk_output = CHUNKS_DIR / f"{pdf_path.stem}.json"

    chunk_data = {
        "document_id": pdf_path.stem,
        "source": pdf_path.name,
        "chunks": [
            {
                "chunk_id": (
                    f"{pdf_path.stem}"
                    f"-chunk-{index:04d}"
                ),
                "text": chunk.text,
                "page_numbers": chunk.page_numbers,
                "token_count": count_tokens(chunk.text),
            }
            for index, chunk in enumerate(chunks, start=1)
        ],
    }

    write_json(chunk_output, chunk_data)

    print(
        f"Processed {pdf_path.name}: "
        f"{len(pages)} pages → "
        f"{len(chunks)} chunks"
    )


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {DOCUMENTS_DIR}"
        )

    print(f"Found {len(pdf_files)} PDF(s).")

    for pdf_path in pdf_files:
        process_document(pdf_path)


if __name__ == "__main__":
    main()