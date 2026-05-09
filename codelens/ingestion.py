"""
ingestion.py — Codebase scanning and remote repository ingestion.
Supports local directories and GitHub clones.
"""

import os
import time
from git import Repo
from codelens import config


def ingest(source: str) -> list[str]:
    """
    Accepts a GitHub URL or local directory path.
    Clones (if remote) and returns a filtered list of .py and .md file paths.

    Args:
        source: GitHub URL (https://github.com/...) or absolute local path.
    Returns:
        List of absolute paths to valid files, filtered per config.
    Raises:
        ValueError: If source is invalid or path does not exist.
        RuntimeError: If cloning fails.
    """
    if source.startswith("http"):
        # It's a URL, clone it first
        work_dir = _clone_repo(source)
    else:
        # It's a local path, verify it exists
        if not os.path.isabs(source):
            # Try to make it absolute if it's relative to current dir
            source = os.path.abspath(source)

        if not os.path.isdir(source):
            raise ValueError(
                f"Source path does not exist or is not a directory: {source}"
            )
        work_dir = source

    return _discover_files(work_dir)


def _clone_repo(url: str) -> str:
    """
    Clones a remote GitHub repository to a timestamped subdirectory in TEMP_DIR.
    """
    # Create a unique folder name using the current timestamp
    timestamp = int(time.time())
    repo_name = url.split("/")[-1].replace(".git", "")
    target_path = os.path.join(config.TEMP_DIR, f"{repo_name}_{timestamp}")

    # Ensure the TEMP_DIR exists
    os.makedirs(config.TEMP_DIR, exist_ok=True)

    try:
        print(f"Cloning {url} into {target_path}...")
        Repo.clone_from(url, target_path)
        return os.path.abspath(target_path)
    except Exception as e:
        raise RuntimeError(f"Failed to clone repository: {str(e)}")


def _discover_files(root_path: str) -> list[str]:
    """
    Walks the directory and returns absolute paths to all .py and .md files,
    excluding those in IGNORED_DIRS or matching IGNORED_FILES.
    """
    valid_files = []

    # 1. Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Exclude ignored directories in-place
        dirnames[:] = [d for d in dirnames if d not in config.IGNORED_DIRS]

        for filename in filenames:
            # 2. Check extension
            ext = os.path.splitext(filename)[1].lower()
            if ext not in [".py", ".md"]:
                continue

            # 3. Check ignored files
            if filename in config.IGNORED_FILES:
                continue

            # 4. Add valid file
            full_path = os.path.join(dirpath, filename)
            valid_files.append(os.path.abspath(full_path))

    return valid_files
