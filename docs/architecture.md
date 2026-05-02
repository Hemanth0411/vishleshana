# Architecture — Vishleshana (The Code Lens)

## Overview

Vishleshana follows a strict linear pipeline. Each module has exactly one job. Data flows forward as plain Python dicts and networkx graphs. No shared mutable state between modules.

```
GitHub URL / Local Path
        │
        ▼
  [ingestion.py]   ← clones repo, returns list[str] of .py paths
        │
        ▼
   [parser.py]     ← AST extraction + pyan3 call edges → dict
        │
        ▼
[graph_builder.py] ← builds file_graph + call_graph (networkx DiGraphs)
        │
        ▼
  [metrics.py]     ← radon complexity → attaches scores to file_graph nodes
        │
        ▼
  [analyzer.py]    ← entry points, centrality, topological sort → dict
        │
        ▼
 [ai_client.py]    ← NVIDIA NIM: summary, reading order explanation, Q&A
        │
        ▼
[visualizer.py]    ← pyvis HTML string from networkx graph
        │
        ▼
   [main.py]       ← Streamlit UI: tabs, session state, progress bar
```

## Module Responsibilities

| Module | Input | Output | Key Dependency |
|--------|-------|--------|----------------|
| `config.py` | `.env` file | constants | `python-dotenv` |
| `ingestion.py` | URL or path | `list[str]` file paths | `gitpython` |
| `parser.py` | file paths | parsed dict | `ast`, `pyan3` |
| `graph_builder.py` | parsed dict | 2× `nx.DiGraph` | `networkx` |
| `metrics.py` | file paths + file_graph | annotated `nx.DiGraph` | `radon` |
| `analyzer.py` | file_graph | analysis dict | `networkx` |
| `ai_client.py` | graph + analysis | strings | `openai` (NIM) |
| `visualizer.py` | file_graph + analysis | HTML string | `pyvis` |
| `main.py` | user input | rendered UI | `streamlit` |

## Design Decisions

- **No RAG / no vector database** — the graph IS the retrieval mechanism.
- **No Docker required to run** — Docker support is for reproducibility only.
- **No shared mutable state** — all data is passed explicitly between modules.
- **No module exceeds 300 lines** — enforced by code review.
- **pyan3 failures are non-fatal** — graceful fallback to empty call edges.
- **Cycle detection before topological sort** — circular imports are valid Python.

## Attribution

See [ATTRIBUTION.md](../ATTRIBUTION.md) for full auto-generated dependency attribution.
