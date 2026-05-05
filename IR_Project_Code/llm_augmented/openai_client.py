from openai import OpenAI
from llm_augmented.config import OPENAI_API_KEY, OPENAI_MODEL


def get_openai_client():
    if not OPENAI_API_KEY:
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to your .env file.")

    return OpenAI(api_key=OPENAI_API_KEY)


def call_llm(prompt: str, model: str = OPENAI_MODEL) -> str:
    client = get_openai_client()

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text.strip()