
import os
import time
import logging

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


def generate_response(prompt, max_retries=3):

    if not prompt or not prompt.strip():
        return None

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as error:

            error_message = str(error).upper()

            temporary_error = any(
                term in error_message
                for term in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "INTERNAL"
                ]
            )

            if temporary_error and attempt < max_retries - 1:

                wait_time = 2 ** attempt

                logger.warning(
                    "Gemini temporary failure. Retry %s in %s seconds.",
                    attempt + 1,
                    wait_time
                )

                time.sleep(wait_time)

            else:

                logger.exception(
                    "Gemini API request failed."
                )

                return None

    return None
