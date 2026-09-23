"""
Dutch4You - core logic
Takes pasted Dutch text and returns:
  - an English translation
  - a plain-language explanation
  - key info (deadlines, amounts, required actions)
  - a warning if the text is unclear or doesn't look like Dutch
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# Load .env from the SAME FOLDER as this script, regardless of the
# terminal's current working directory.
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

MODEL = "gemini-3.6-flash"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5  # doubles each retry: 5s, 10s, 20s


def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No API key found. Create a .env file next to this script "
            "containing: GEMINI_API_KEY=your-key-here"
        )
    return genai.Client(api_key=api_key)


PROMPT_TEMPLATE = """You are helping a non-Dutch speaker understand a Dutch letter or text
(university, housing, healthcare, public services, or official notices).

Translate the text into English, explain it in simple plain language a non-expert
would understand, and pull out the key practical info.

Respond ONLY with valid JSON in exactly this shape, no other text:
{{
  "translation": "...",
  "explanation": "...",
  "key_info": {{
    "deadlines": ["..."],
    "amounts": ["..."],
    "required_actions": ["..."]
  }},
  "confidence": "high" | "medium" | "low",
  "warning": "any concern about ambiguous or unclear parts of the source text, or empty string"
}}

If the text does not look like Dutch, or is empty/unreadable, set "confidence" to "low"
and explain the problem in "warning" instead of guessing.

Text to process:
---
{text}
---
"""


def _generate_with_retry(client: genai.Client, **kwargs):
    """Calls generate_content, auto-retrying on temporary server overload (503)."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return client.models.generate_content(**kwargs)
        except ServerError as e:
            last_error = e
            if getattr(e, "code", None) == 503 and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
                continue
            raise
    raise last_error


def process_text(dutch_text: str) -> dict:
    """Takes pasted Dutch text, returns translation + explanation + key info."""
    if not dutch_text or not dutch_text.strip():
        return _error_result("No text was provided.")

    client = get_client()
    prompt = PROMPT_TEMPLATE.format(text=dutch_text)

    try:
        response = _generate_with_retry(client, model=MODEL, contents=prompt)
    except Exception as e:
        return _error_result(f"API call failed: {e}")

    return _parse_response(response)


def _parse_response(response) -> dict:
    raw = (response.text or "").strip()
    # Gemini sometimes wraps JSON in ```json fences even when told not to - strip them.
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return _error_result("The AI's response wasn't valid JSON. Try again.")

    # Defensive defaults so the UI never crashes on a missing field.
    data.setdefault("translation", "")
    data.setdefault("explanation", "")
    data.setdefault("key_info", {"deadlines": [], "amounts": [], "required_actions": []})
    data.setdefault("confidence", "low")
    data.setdefault("warning", "")
    return data


def _error_result(message: str) -> dict:
    return {
        "translation": "",
        "explanation": "",
        "key_info": {"deadlines": [], "amounts": [], "required_actions": []},
        "confidence": "low",
        "warning": message,
    }


if __name__ == "__main__":
    sample = "U dient uiterlijk 30 september uw documenten in te leveren."
    result = process_text(sample)
    print(json.dumps(result, indent=2, ensure_ascii=False))
