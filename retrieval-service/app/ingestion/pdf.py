from pathlib import Path

import fitz


def clean_text(text: str) -> str:
    """
    Normalize obvious PDF extraction noise while preserving
    meaningful line breaks and content structure.
    """
    lines = []

    for line in text.splitlines():
        cleaned = " ".join(line.split())

        if cleaned:
            lines.append(cleaned)

    return "\n".join(lines)


def extract_pdf(pdf_path: Path) -> list[dict]:
    """
    Extract text from a PDF page-by-page.

    Each page keeps its source filename and page number
    so that downstream chunks can retain citation metadata.
    """
    pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            raw_text = page.get_text("text")
            text = clean_text(raw_text)

            if not text:
                continue

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    return pages