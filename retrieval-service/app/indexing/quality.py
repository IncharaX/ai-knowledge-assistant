import re


MIN_WORD_COUNT = 40


def normalize_text(text: str) -> str:
    """
    Normalize text for quality checks.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_table_of_contents(text: str) -> bool:
    """
    Reject table-of-contents chunks.
    """
    normalized = normalize_text(text)

    return "table of contents" in normalized


def is_cover_page(text: str) -> bool:
    """
    Detect chunks that are primarily document metadata.
    """

    normalized = normalize_text(text)

    metadata_signals = [
        "department of",
        "submitted by",
        "under the guidance",
        "course:",
        "module:",
        "reference:",
    ]

    matches = sum(
        signal in normalized
        for signal in metadata_signals
    )

    return matches >= 2


def has_enough_content(text: str) -> bool:
    """
    Reject extremely small fragments.
    """
    return len(text.split()) >= MIN_WORD_COUNT


def should_index(text: str) -> bool:
    """
    Decide whether a chunk should enter the
    retrieval index.
    """

    if not text.strip():
        return False

    if is_table_of_contents(text):
        return False

    if not has_enough_content(text):
        return False

    if is_cover_page(text):
        return False

    return True