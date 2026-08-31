import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class OpenRouterLLM:
    """
    Client for communicating with the
    OpenRouter Chat Completions API.
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
        Generate an answer using OpenRouter.
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

        try:
            response = httpx.post(
                self.BASE_URL,
                headers=headers,
                json=payload,
                timeout=60.0,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except httpx.TimeoutException:
            raise RuntimeError(
                "The AI service took too long to respond."
            )

        except httpx.HTTPStatusError as error:
            status_code = error.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "The AI service authentication failed."
                )

            if status_code == 429:
                raise RuntimeError(
                    "The AI service rate limit was reached. "
                    "Please try again later."
                )

            raise RuntimeError(
                f"The AI service returned an error "
                f"(status {status_code})."
            )

        except httpx.RequestError:
            raise RuntimeError(
                "Unable to connect to the AI service."
            )

        except (KeyError, IndexError, TypeError):
            raise RuntimeError(
                "The AI service returned an unexpected response."
            )