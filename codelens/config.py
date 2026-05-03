"""
config.py — Central configuration for CodeLens.

All environment variables and constants are defined here.
Import this module wherever configuration is needed.
Do not hardcode values in other modules.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# NVIDIA NIM
NIM_API_KEY = os.getenv("NIM_API_KEY")
NIM_BASE_URL = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_MODEL = os.getenv("NIM_MODEL", "meta/llama-3.1-8b-instruct")
NIM_MAX_TOKENS = int(os.getenv("NIM_MAX_TOKENS", "1024"))

# Analysis Settings
MAX_FILES = int(os.getenv("MAX_FILES", "150"))
COMPLEXITY_THRESHOLD = int(
    os.getenv("COMPLEXITY_THRESHOLD", "10")
)  # radon rank C cutoff

# Temp directory for cloned repos
# Default to /tmp/codelens_repos (Linux) or a suitable Windows path if set in .env
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/codelens_repos")

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
