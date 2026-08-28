import math
import re
from collections import Counter
from dataclasses import dataclass

import tiktoken


TARGET_TOKENS = 650
MAX_TOKENS = 800
OVERLAP_TOKENS = 100

ENCODER = tiktoken.get_encoding("cl100k_base")


@dataclass
class TextSegment:
    text: str
    page_number: int


@dataclass
class Chunk:
    text: str
    page_numbers: list[int]


def token_count(text: str) -> int:
    return len(ENCODER.encode(text))


def count_tokens(text: str) -> int:
    """
    Public helper used by the ingestion pipeline.
    """
    return token_count(text)


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def remove_repeated_boilerplate(pages: list[dict]) -> list[dict]:
    """
    Remove lines that repeatedly appear at the top or bottom
    of multiple pages.

    We intentionally only inspect page boundaries so that
    repeated terminology inside actual content is preserved.
    """
    if len(pages) < 2:
        return pages

    candidates: list[str] = []

    for page in pages:
        lines = [
            normalize_line(line)
            for line in page["text"].splitlines()
        ]

        lines = [line for line in lines if line]

        boundary_lines = lines[:3] + lines[-3:]

        for line in boundary_lines:
            if len(line) >= 8:
                candidates.append(line)

    counts = Counter(candidates)

    minimum_occurrences = max(
        2,
        math.ceil(len(pages) * 0.5),
    )

    boilerplate = {
        line
        for line, count in counts.items()
        if count >= minimum_occurrences
    }

    cleaned_pages = []

    for page in pages:
        lines = page["text"].splitlines()
        cleaned_lines = []

        for line in lines:
            normalized = normalize_line(line)

            if normalized in boilerplate:
                continue

            if normalized:
                cleaned_lines.append(normalized)

        cleaned_pages.append(
            {
                "page_number": page["page_number"],
                "text": "\n".join(cleaned_lines),
            }
        )

    return cleaned_pages


def split_into_segments(
    pages: list[dict],
) -> list[TextSegment]:
    """
    Convert page text into logical segments.

    Blank lines are treated as natural boundaries.
    """
    segments = []

    for page in pages:
        raw_segments = re.split(
            r"\n\s*\n",
            page["text"],
        )

        for raw_segment in raw_segments:
            text = raw_segment.strip()

            if not text:
                continue

            segments.append(
                TextSegment(
                    text=text,
                    page_number=page["page_number"],
                )
            )

    return segments


def split_long_segment(
    segment: TextSegment,
) -> list[TextSegment]:
    """
    Split an oversized segment while trying to preserve
    meaningful line and sentence boundaries.
    """
    if token_count(segment.text) <= MAX_TOKENS:
        return [segment]

    lines = [
        line.strip()
        for line in segment.text.splitlines()
        if line.strip()
    ]

    # Prefer line-based splitting for algorithm steps,
    # pseudocode, lists, and code-like PDF content.
    if len(lines) > 1:
        pieces: list[TextSegment] = []
        current_lines: list[str] = []
        current_tokens = 0

        for line in lines:
            line_tokens = token_count(line)

            if (
                current_lines
                and current_tokens + line_tokens > MAX_TOKENS
            ):
                pieces.append(
                    TextSegment(
                        text="\n".join(current_lines),
                        page_number=segment.page_number,
                    )
                )

                current_lines = []
                current_tokens = 0

            current_lines.append(line)
            current_tokens += line_tokens

        if current_lines:
            pieces.append(
                TextSegment(
                    text="\n".join(current_lines),
                    page_number=segment.page_number,
                )
            )

        return pieces

    # For normal prose, prefer sentence boundaries.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        segment.text,
    )

    pieces: list[TextSegment] = []
    current: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_tokens = token_count(sentence)

        if (
            current
            and current_tokens + sentence_tokens > MAX_TOKENS
        ):
            pieces.append(
                TextSegment(
                    text=" ".join(current),
                    page_number=segment.page_number,
                )
            )

            current = []
            current_tokens = 0

        current.append(sentence)
        current_tokens += sentence_tokens

    if current:
        pieces.append(
            TextSegment(
                text=" ".join(current),
                page_number=segment.page_number,
            )
        )

    # A single sentence can itself exceed MAX_TOKENS.
    final_pieces: list[TextSegment] = []

    for piece in pieces:
        if token_count(piece.text) <= MAX_TOKENS:
            final_pieces.append(piece)
            continue

        tokens = ENCODER.encode(piece.text)

        for start in range(
            0,
            len(tokens),
            MAX_TOKENS,
        ):
            token_slice = tokens[
                start:start + MAX_TOKENS
            ]

            text = ENCODER.decode(
                token_slice
            ).strip()

            if text:
                final_pieces.append(
                    TextSegment(
                        text=text,
                        page_number=piece.page_number,
                    )
                )

    return final_pieces


def build_overlap(
    segments: list[TextSegment],
) -> list[TextSegment]:
    """
    Build an overlap from the end of the previous chunk.

    Whole segments are preferred so we don't create awkward
    partial sentences or broken algorithm steps.
    """
    overlap: list[TextSegment] = []
    overlap_tokens = 0

    for segment in reversed(segments):
        segment_tokens = token_count(segment.text)

        if overlap_tokens + segment_tokens > OVERLAP_TOKENS:
            break

        overlap.insert(0, segment)
        overlap_tokens += segment_tokens

    return overlap


def build_chunks(
    segments: list[TextSegment],
) -> list[Chunk]:
    """
    Build retrieval chunks.

    TARGET_TOKENS is the preferred size.
    MAX_TOKENS is the hard ceiling.

    We only split when adding the next segment would exceed
    MAX_TOKENS. This avoids unnecessary tiny chunks.
    """
    expanded_segments: list[TextSegment] = []

    for segment in segments:
        expanded_segments.extend(
            split_long_segment(segment)
        )

    chunks: list[Chunk] = []

    current_segments: list[TextSegment] = []
    current_tokens = 0

    for segment in expanded_segments:
        segment_tokens = token_count(segment.text)

        if (
            current_segments
            and current_tokens + segment_tokens > MAX_TOKENS
        ):
            chunks.append(
                Chunk(
                    text="\n\n".join(
                        item.text
                        for item in current_segments
                    ),
                    page_numbers=sorted(
                        {
                            item.page_number
                            for item in current_segments
                        }
                    ),
                )
            )

            current_segments = build_overlap(
                current_segments
            )

            current_tokens = sum(
                token_count(item.text)
                for item in current_segments
            )

        current_segments.append(segment)
        current_tokens += segment_tokens

    if current_segments:
        chunks.append(
            Chunk(
                text="\n\n".join(
                    item.text
                    for item in current_segments
                ),
                page_numbers=sorted(
                    {
                        item.page_number
                        for item in current_segments
                    }
                ),
            )
        )

    return chunks


def chunk_document(
    pages: list[dict],
) -> list[Chunk]:
    cleaned_pages = remove_repeated_boilerplate(
        pages
    )

    segments = split_into_segments(
        cleaned_pages
    )

    return build_chunks(segments)