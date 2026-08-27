import json
from pathlib import Path

from .pdf import extract_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


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

    output_path = PROCESSED_DIR / f"{pdf_path.stem}.json"

    output_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        f"Processed {pdf_path.name}: "
        f"{len(pages)} pages → {output_path.name}"
    )


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

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