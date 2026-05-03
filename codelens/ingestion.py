"""
ingestion.py — Repository ingestion for CodeLens.

Accepts a GitHub URL or local directory path.
Clones (if remote) and returns filtered list of .py file paths.

Dependencies: gitpython
"""

import os
import time
from git import Repo
from codelens import config


def ingest(source: str) -> list[str]:
    """
    Accepts a GitHub URL or local directory path.
    Clones (if remote) and returns a filtered list of .py file paths.

    Args:
        source: GitHub URL (https://github.com/...) or absolute local path.
    Returns:
        List of absolute paths to .py files, filtered per config.
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

    Args:
        url: The GitHub repository URL.
    Returns:
        The absolute path to the locally cloned repository.
    Raises:
        RuntimeError: If cloning fails.
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


def _discover_files(root: str) -> list[str]:
    """
    Walks the directory and returns absolute paths to all .py files,
    excluding those in IGNORED_DIRS or matching IGNORED_FILES/PREFIXES.

    Args:
        root: The root directory to scan.
    Returns:
        List of absolute paths to filtered .py files.
    """
    py_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        # 1. Filter out ignored directories in-place to prevent os.walk from entering them
        dirnames[:] = [d for d in dirnames if d not in config.IGNORED_DIRS]

        for filename in filenames:
            # 2. Check if it's a .py file
            if not filename.endswith(".py"):
                continue

            # 3. Check if file is in IGNORED_FILES
            if filename in config.IGNORED_FILES:
                continue

            # 4. Check if file matches IGNORED_PREFIXES
            if any(filename.startswith(prefix) for prefix in config.IGNORED_PREFIXES):
                continue

            # 5. Add valid file to list
            full_path = os.path.join(dirpath, filename)
            py_files.append(os.path.abspath(full_path))

    return py_files
