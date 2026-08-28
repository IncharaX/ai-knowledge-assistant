import math
import re
from collections import Counter
from dataclasses import dataclass

import tiktoken


TARGET_TOKENS = 650
MAX_TOKENS = 800
OVERLAP_TOKENS = 100

# cl100k_base is a good general-purpose tokenizer for measuring
# the size of text that will eventually be sent to an LLM.
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


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def remove_repeated_boilerplate(pages: list[dict]) -> list[dict]:
    """
    Remove lines that repeatedly appear at the top or bottom
    of multiple pages.

    We only inspect the first and last few lines so that
    legitimate repeated terminology inside the actual content
    isn't accidentally removed.
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

    minimum_occurrences = max(2, math.ceil(len(pages) * 0.5))

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


def split_into_segments(pages: list[dict]) -> list[TextSegment]:
    """
    Convert page text into small logical segments.

    Blank lines are treated as natural boundaries. When a PDF
    doesn't preserve paragraph boundaries, individual lines
    remain separate segments and can still be grouped later.
    """
    segments = []

    for page in pages:
        raw_segments = re.split(r"\n\s*\n", page["text"])

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


def split_oversized_segment(segment: TextSegment) -> list[TextSegment]:
    """
    Split a segment that exceeds MAX_TOKENS.

    Sentences are preferred as boundaries. If an individual
    sentence is still too large, it is split by tokens.
    """
    if token_count(segment.text) <= MAX_TOKENS:
        return [segment]

    sentences = re.split(
        r"(?<=[.!?])\s+",
        segment.text,
    )

    pieces: list[TextSegment] = []
    current: list[str] = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        candidate = " ".join(current + [sentence])

        if current and token_count(candidate) > MAX_TOKENS:
            pieces.append(
                TextSegment(
                    text=" ".join(current),
                    page_number=segment.page_number,
                )
            )
            current = [sentence]
        else:
            current.append(sentence)

    if current:
        pieces.append(
            TextSegment(
                text=" ".join(current),
                page_number=segment.page_number,
            )
        )

    # A single sentence can itself be too large.
    final_pieces: list[TextSegment] = []

    for piece in pieces:
        if token_count(piece.text) <= MAX_TOKENS:
            final_pieces.append(piece)
            continue

        tokens = ENCODER.encode(piece.text)

        for start in range(0, len(tokens), MAX_TOKENS):
            token_slice = tokens[start:start + MAX_TOKENS]
            text = ENCODER.decode(token_slice).strip()

            if text:
                final_pieces.append(
                    TextSegment(
                        text=text,
                        page_number=piece.page_number,
                    )
                )

    return final_pieces


def build_chunks(segments: list[TextSegment]) -> list[Chunk]:
    """
    Group segments into chunks around TARGET_TOKENS without
    exceeding MAX_TOKENS.

    Overlap is created from the end of the previous chunk.
    """
    expanded_segments: list[TextSegment] = []

    for segment in segments:
        expanded_segments.extend(
            split_oversized_segment(segment)
        )

    chunks: list[Chunk] = []

    current_segments: list[TextSegment] = []
    current_tokens = 0

    for segment in expanded_segments:
        segment_tokens = token_count(segment.text)

        if (
            current_segments
            and current_tokens + segment_tokens > TARGET_TOKENS
        ):
            chunks.append(
                Chunk(
                    text="\n\n".join(
                        item.text for item in current_segments
                    ),
                    page_numbers=sorted(
                        {item.page_number for item in current_segments}
                    ),
                )
            )

            overlap_segments: list[TextSegment] = []
            overlap_tokens = 0

            for previous in reversed(current_segments):
                previous_tokens = token_count(previous.text)

                if overlap_tokens + previous_tokens > OVERLAP_TOKENS:
                    break

                overlap_segments.insert(0, previous)
                overlap_tokens += previous_tokens

            current_segments = overlap_segments
            current_tokens = overlap_tokens

        current_segments.append(segment)
        current_tokens += segment_tokens

    if current_segments:
        chunks.append(
            Chunk(
                text="\n\n".join(
                    item.text for item in current_segments
                ),
                page_numbers=sorted(
                    {item.page_number for item in current_segments}
                ),
            )
        )

    return chunks


def chunk_document(pages: list[dict]) -> list[Chunk]:
    cleaned_pages = remove_repeated_boilerplate(pages)
    segments = split_into_segments(cleaned_pages)

    return build_chunks(segments)


def count_tokens(text: str) -> int:
    return token_count(text)