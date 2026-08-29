from typing import Any


def build_rag_prompt(
    question: str,
    chunks: list[dict[str, Any]],
) -> str:
    """
    Build a grounded prompt using retrieved chunks.
    """

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):

        source = chunk["metadata"]["source"]

        context_parts.append(
            f"""
SOURCE {index}: {source}

{chunk["text"]}
""".strip()
        )

    context = "\n\n---\n\n".join(context_parts)

    return f"""
You are a helpful academic knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not supported by the context, clearly say:
  "I don't have enough information in the provided documents to answer that."
- Give a clear and concise explanation.

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
""".strip()