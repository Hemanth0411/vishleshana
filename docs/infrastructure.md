# 🏗️ Infrastructure & Quality Assurance

## 1. Automated Testing (Pytest)
- **Philosophy**: We use the "Arrange-Act-Assert" pattern.
- **Fixtures**: We heavily use the `tmp_path` fixture from `pytest`. This creates a temporary, isolated file system for every test, ensuring that testing the "Ingestion" or "Parsing" modules doesn't leave real files behind.
- **Mocking**: We use mocking for the `GitPython` calls to ensure our tests don't require an internet connection and are "Lightning Fast."
- **How to run**: `pytest tests/`

## 2. Dockerization
- **Purpose**: "It works on my machine" protection.
- **Dockerfile**: Uses a `python:3.11-slim` base to keep the image size small. It installs `git` at the system level, which is a required dependency for `GitPython`.
- **Docker Compose**: Orchestrates the environment, mounting the local folder as a volume so you can see code changes in real-time inside the container.

## 3. CI/CD (GitHub Actions)
- **Workflow**: `.github/workflows/ci.yml`
- **Steps**:
    1. **Linting**: Uses `ruff` and `black` to ensure every developer follows the same "clean code" style.
    2. **Testing**: Runs the entire `pytest` suite on every Push or Pull Request.
    3. **Attribution Check**: Automatically verifies that `ATTRIBUTION.md` exists and contains all required licenses for third-party libraries.
- **Protection**: The `main` branch is configured to block merges if any of these checks fail.

## 4. Development Standards
- **300-Line Rule**: No single file should exceed 300 lines. This ensures modules stay focused and easy to document.
- **Statelessness**: Modules pass data (dictionaries/graphs) to each other but do not share "Global State." This makes the system incredibly easy to debug.
