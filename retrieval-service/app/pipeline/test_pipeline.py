from unittest.mock import MagicMock

from app.pipeline.rag_pipeline import RAGPipeline


def create_pipeline():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    pipeline.retriever = MagicMock()
    pipeline.reranker = MagicMock()
    pipeline.confidence = MagicMock()
    pipeline.generator = MagicMock()

    return pipeline


def test_pipeline_generates_answer_when_confident():
    pipeline = create_pipeline()

    candidates = [
        {
            "chunk_id": "chunk-1",
            "text": "Sequential search checks elements one by one.",
            "metadata": {
                "source": "DAA_Unit_2.pdf",
                "page_start": 7,
                "page_end": 7,
            },
        }
    ]

    reranked_chunks = [
        {
            **candidates[0],
            "rerank_score": 5.0,
        }
    ]

    expected_result = {
        "answer": "Sequential search checks elements one by one.",
        "sources": [],
        "answered": True,
    }

    pipeline.retriever.search.return_value = candidates

    pipeline.reranker.rerank.return_value = reranked_chunks

    pipeline.confidence.evaluate.return_value = {
        "top_score": 5.0,
        "is_sufficient": True,
    }

    pipeline.generator.answer.return_value = expected_result

    result = pipeline.answer(
        question="What is sequential search?"
    )

    assert result == expected_result

    pipeline.retriever.search.assert_called_once()

    pipeline.reranker.rerank.assert_called_once()

    pipeline.confidence.evaluate.assert_called_once_with(
        reranked_chunks
    )

    pipeline.generator.answer.assert_called_once_with(
        question="What is sequential search?",
        chunks=reranked_chunks,
    )


def test_pipeline_refuses_when_evidence_is_insufficient():
    pipeline = create_pipeline()

    candidates = [
        {
            "chunk_id": "chunk-1",
            "text": "Some unrelated information.",
            "metadata": {},
        }
    ]

    reranked_chunks = [
        {
            **candidates[0],
            "rerank_score": -10.0,
        }
    ]

    pipeline.retriever.search.return_value = candidates

    pipeline.reranker.rerank.return_value = reranked_chunks

    pipeline.confidence.evaluate.return_value = {
        "top_score": -10.0,
        "is_sufficient": False,
    }

    result = pipeline.answer(
        question="What is quantum entanglement?"
    )

    assert result["answered"] is False

    assert result["sources"] == []

    assert result["retrieval_score"] == -10.0

    assert (
        "don't have enough information"
        in result["answer"]
    )

    pipeline.generator.answer.assert_not_called()