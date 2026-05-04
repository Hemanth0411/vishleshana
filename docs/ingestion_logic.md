# 📥 Ingestion Module Logic

The Ingestion module is the entry point for data. Its goal is to move code from a source (GitHub or Local) into a controlled environment for analysis.

## 1. `_clone_repo(url: str)`
- **Purpose**: Downloads remote code for analysis.
- **How it works**: Uses `GitPython` to perform a non-blocking clone into a timestamped subdirectory inside the `TEMP_DIR`.
- **Why this way?**:
    - **Pros**: Isolation. Every analysis gets its own clean folder, preventing "leakage" between different project versions.
    - **Cons**: High disk usage if many large repos are analyzed.
- **Logic Details**: It uses `os.path.join(config.TEMP_DIR, timestamp)` to ensure uniqueness.

## 2. `_discover_files(root_dir: str)`
- **Purpose**: Scans a directory for Python files while ignoring "noise" (venv, node_modules).
- **How it works**: Uses `os.walk()` with a specific optimization: it modifies `dirnames[:]` in-place to prune ignored directories before the walker even enters them.
- **Why this way?**:
    - **Pros**: Extremely fast. It doesn't waste time looking at 10,000 files in a `node_modules` folder.
    - **Cons**: Only finds `.py` files. It currently ignores `.pyi` or `.pyx` files.
- **Logic Details**: It checks against `config.IGNORED_DIRS` and `config.IGNORED_FILES`.

## 3. `ingest(source: str)`
- **Purpose**: Unified interface for the rest of the app.
- **How it works**: Checks if `source` starts with `http`. If yes, it calls `_clone_repo`. If no, it verifies the local path exists and proceeds.
- **Pros**: The UI doesn't need to know if the code is local or remote; it just calls `ingest()`.
