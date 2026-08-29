from typing import Any


def build_sources(
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Build a clean, deduplicated list of sources
    from retrieved chunks.
    """

    sources = []
    seen_sources = set()

    for chunk in chunks:
        metadata = chunk["metadata"]

        source = metadata["source"]
        page_start = metadata["page_start"]
        page_end = metadata["page_end"]

        source_key = (
            source,
            page_start,
            page_end,
        )

        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)

        sources.append(
            {
                "source": source,
                "page_start": page_start,
                "page_end": page_end,
            }
        )

    return sources