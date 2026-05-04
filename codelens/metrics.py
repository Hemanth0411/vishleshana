"""
metrics.py — Complexity metrics for CodeLens.

Computes cyclomatic complexity (radon) for each function.
Attaches scores to file_graph nodes as metadata.
Flags functions above the configured complexity threshold.

Dependencies: radon
"""

import radon.complexity as cc
import networkx as nx
from codelens import config


def compute_metrics(file_paths: list[str], file_graph: nx.DiGraph) -> nx.DiGraph:
    """
    Computes metrics for all files and attaches them to graph nodes.

    Args:
        file_paths: List of .py file paths.
        file_graph: networkx DiGraph from graph_builder.
    Returns:
        The graph with added complexity attributes on each node.
    """
    for path in file_paths:
        if path not in file_graph.nodes:
            continue

        metrics = _analyze_file(path)
        if not metrics:
            continue

        # Extract complexity values
        scores = [m["complexity"] for m in metrics]
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)

        # Identify functions above the danger threshold
        flagged = [
            m["name"] for m in metrics if m["complexity"] >= config.COMPLEXITY_THRESHOLD
        ]

        # Attach to graph node
        file_graph.nodes[path].update(
            {
                "complexity_avg": round(avg_score, 2),
                "complexity_max": max_score,
                "complexity_rank": cc.cc_rank(avg_score),
                "flagged_functions": flagged,
            }
        )

    return file_graph


def _analyze_file(path: str) -> list[dict]:
    """
    Computes cyclomatic complexity for all functions in a file.

    Args:
        path: Absolute path to the .py file.
    Returns:
        List of dicts containing function names, complexity, and rank.
    """
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        # cc_visit returns a list of Function or Class objects
        results = cc.cc_visit(source)

        metrics = []
        for item in results:
            # We care about functions (Function) and methods (Class)
            metrics.append(
                {
                    "name": item.name,
                    "complexity": item.complexity,
                    "rank": cc.cc_rank(item.complexity),
                    "lineno": item.lineno,
                }
            )
        return metrics
    except Exception as e:
        print(f"Warning: Radon failed to analyze {path}: {e}")
        return []
