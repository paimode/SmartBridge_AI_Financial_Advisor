# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# def get_gemini_api_key() -> str:
#     """Retrieve Gemini API key from environment variables."""
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError(
#             "GEMINI_API_KEY not found. "
#             "Please set it in your .env file or environment variables."
#         )
#     return api_key

# # App-level config constants
# APP_TITLE = "AI Financial Advisor"
# GEMINI_MODEL = "gemini-2.5-flash"
import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key() -> str:
    """Retrieve Gemini API key from environment variables. Never hardcoded."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found.\n"
            "  Local dev  : add it to your .env file\n"
            "  Production : set it as an environment variable on your server\n"
            "  Streamlit  : add it under Settings -> Secrets"
        )
    return api_key

# App Constants
APP_TITLE    = "AI Financial Advisor"
GEMINI_MODEL = "gemini-2.5-flash"