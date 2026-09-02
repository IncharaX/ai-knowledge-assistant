from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.generation.llm import OpenRouterLLM


def create_llm() -> OpenRouterLLM:
    with patch.dict(
        "os.environ",
        {
            "OPENROUTER_API_KEY": "test-api-key",
            "OPENROUTER_MODEL": "test-model",
        },
    ):
        return OpenRouterLLM()


def test_generate_returns_answer():
    llm = create_llm()

    mock_response = MagicMock()

    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Euclid's algorithm finds the GCD."
                }
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "app.generation.llm.httpx.post",
        return_value=mock_response,
    ):
        result = llm.generate(
            "Explain Euclid's algorithm."
        )

    assert result == (
        "Euclid's algorithm finds the GCD."
    )