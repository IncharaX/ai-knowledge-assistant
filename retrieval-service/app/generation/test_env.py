import os

from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")

print(
    "API key loaded:",
    bool(api_key),
)

if api_key:
    print(
        "Key starts with:",
        api_key[:10],
    )

print(
    "Model:",
    os.getenv("OPENROUTER_MODEL"),
)
