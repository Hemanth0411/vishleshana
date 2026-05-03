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
