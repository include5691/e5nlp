import os
import time
import logging
import httpx
from openai import OpenAI, RateLimitError

RATE_LIMIT_PAUSE_SEC = 3600

client: OpenAI | None = None
rate_limit_error_timestamp: int | None = None

def _get_client() -> OpenAI:
    global client
    if not client:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is not set in .env file")
        proxy = os.getenv("HTTP_PROXY")
        if not proxy:
            raise ValueError("HTTP_PROXY is not set in .env file")
        client = OpenAI(api_key=key, http_client=httpx.Client(proxy=proxy))
    return client

def make_gpt_request(text: str, prompt: str, model_name: str) -> str | None:
    """Make request using OpenAI API"""
    client = _get_client()
    if not client:
        logging.error("OpenAI client is not initialized")
        return None
    global rate_limit_error_timestamp
    if rate_limit_error_timestamp and time.time() - RATE_LIMIT_PAUSE_SEC < rate_limit_error_timestamp:
        logging.error("Holding pause for limit error")
        return None
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "assistant", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        return completion.choices[0].message.content
    except RateLimitError as e:
        logging.error(f"Rate limit error: {e}")
        rate_limit_error_timestamp = time.time()
        return None
    except Exception as e:
        logging.error(f"Error in openai request: {e}")
        return None