"""
ai_client.py — AI reasoning for CodeLens via NVIDIA NIM.

Uses the OpenAI-compatible API to interact with hosted LLMs.
Handles prompt construction and context-aware responses.

Dependencies: openai
"""

from openai import OpenAI
from codelens import config

def _get_client() -> OpenAI:
    """
    Initializes and returns an OpenAI-compatible client for NVIDIA NIM.
    """
    return OpenAI(
        base_url=config.NIM_BASE_URL,
        api_key=config.NIM_API_KEY
    )

def test_connection() -> bool:
    """
    Performs a simple health check to verify the NIM API connection.
    Returns: True if successful, False otherwise.
    """
    try:
        client = _get_client()
        # Simple ping request
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        return True if response.choices else False
    except Exception as e:
        print(f"Error: NIM API connection failed: {e}")
        return False
