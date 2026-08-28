from pathlib import Path

import fitz
import re


def clean_text(text: str) -> str:
    """
    Normalize obvious PDF extraction noise while preserving
    paragraph boundaries.
    """
    blocks = re.split(r"\n\s*\n", text)

    cleaned_blocks = []

    for block in blocks:
        lines = []

        for line in block.splitlines():
            cleaned = " ".join(line.split())

            if cleaned:
                lines.append(cleaned)

        if lines:
            cleaned_blocks.append("\n".join(lines))

    return "\n\n".join(cleaned_blocks)


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