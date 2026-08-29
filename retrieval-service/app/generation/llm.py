import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class OpenRouterLLM:
    """
    Small client for communicating with
    the OpenRouter Chat Completions API.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "meta-llama/llama-3.3-70b-instruct",
        )

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not set."
            )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an answer from the LLM.
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
        }

        response = httpx.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]