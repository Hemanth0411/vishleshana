"""
config.py — Central configuration for CodeLens.

Values are resolved in this order:
  1. Environment variables / .env  (local development, Docker)
  2. st.secrets                    (Streamlit Community Cloud deployment)
  3. The default supplied below

Import this module wherever configuration is needed.
Do not hardcode values in other modules.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


def _get(key: str, default: str | None = None):
    """
    Reads a setting from the environment, falling back to Streamlit secrets.

    Streamlit Community Cloud exposes secrets through st.secrets rather than
    as OS environment variables, so both sources must be checked.
    """
    value = os.getenv(key)
    if value:
        return value

    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # No Streamlit runtime / no secrets file — fall through to the default.
        pass

    return default


# NVIDIA NIM
NIM_API_KEY = _get("NIM_API_KEY")
NIM_BASE_URL = _get("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_MODEL = _get("NIM_MODEL", "meta/llama-3.1-8b-instruct")
NIM_MAX_TOKENS = int(_get("NIM_MAX_TOKENS", "1024"))

# Analysis Settings
MAX_FILES = int(_get("MAX_FILES", "150"))
COMPLEXITY_THRESHOLD = int(_get("COMPLEXITY_THRESHOLD", "10"))  # radon rank C cutoff

# Temp directory for cloned repos
# Default is Linux-friendly (/tmp) so it works unchanged on Streamlit Cloud.
TEMP_DIR = _get("TEMP_DIR", "/tmp/codelens_repos")

# Ignored paths during ingestion
IGNORED_DIRS = {
    "__pycache__",
    ".git",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "dist",
    "build",
}
IGNORED_FILES = {"setup.py", "conftest.py"}
IGNORED_PREFIXES = {"test_"}
