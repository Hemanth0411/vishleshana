# 🧪 End-to-End Test Results

We validated Vishleshana against three major open-source Python repositories. Below are the architectural insights and metrics captured.

## 1. [PSF/Requests](https://github.com/psf/requests)
- **Status**: ✅ Success
- **Architecture**: Extremely clean "Hub and Spoke" model.
- **Entry Point**: `requests/api.py`
- **Critical Hub**: `requests/sessions.py` (High Betweenness Centrality)
- **Complexity**: Most files are Rank A. Only `sessions.py` showed Rank B complexity in the `Session.request` method.
- **AI Summary**: Correctly identified it as an HTTP library for humans.

## 2. [Pallets/Flask](https://github.com/pallets/flask)
- **Status**: ✅ Success
- **Architecture**: Highly modular with many internal dependencies.
- **Entry Point**: `flask/app.py`
- **Critical Hub**: `flask/scaffold.py` and `flask/app.py`.
- **Complexity**: Multiple functions in `app.py` flagged for high complexity due to extensive decorator logic and error handling.
- **AI Summary**: Correctly identified it as a WSGI web application framework.

## 3. [Rubik/Radon](https://github.com/rubik/radon)
- **Status**: ✅ Success
- **Architecture**: Deeply nested logic for AST traversal.
- **Entry Point**: `radon/cli.py`
- **Critical Hub**: `radon/complexity.py`
- **Complexity**: High complexity found in the `CCVisitor` class, which is expected as it handles complex Python syntax trees.
- **AI Summary**: Correctly identified itself as a tool for code metrics analysis (Meta-success!).

---

### Performance Summary
| Repo | Files | Analysis Time | Graph Nodes | Result |
| :--- | :--- | :--- | :--- | :--- |
| requests | ~20 | < 10s | 22 | Stable |
| flask | ~35 | < 15s | 38 | Stable |
| radon | ~25 | < 12s | 28 | Stable |
