# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-05

### Added
- **AI Mentorship**: Integrated NVIDIA NIM for codebase summarization and learning paths.
- **Interactive Visualization**: Interactive dependency graphs via Pyvis.
- **Streamlit Dashboard**: A full-featured UI for project analysis.
- **Complexity Analysis**: Automated radon-based metrics and risk flagging.
- **Semantic Query**: Natural language search with context attribution.
- **Structural Analysis**: Automatic detection of entry points and critical modules.
- **Graph Architecture**: Two-tier graph system (File level and Call level).
- **Ingestion Pipeline**: Support for local directories and remote GitHub cloning.

### Fixed
- Improved topological sort robustness for circular dependencies.
- Resolved key mismatches in the metrics-to-UI pipeline.
- Fixed bare `except` and unused import linting errors.

### Infrastructure
- Modular UI architecture (under 200 lines per file).
- Automated `ATTRIBUTION.md` generation.
- Pytest suite for core analysis logic.
- GitHub Actions CI/CD pipeline.

---
*Created by Hemanth Reddy Annem*
