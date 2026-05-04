"""
analyzer.py — Structural analysis for CodeLens.

Derives insights from the file dependency graph:
  - Entry points (zero in-degree nodes)
  - Critical modules (betweenness centrality)
  - Topological reading order (nx.topological_sort)

Dependencies: networkx
"""

import networkx as nx


def _detect_entry_points(file_graph: nx.DiGraph) -> list[str]:
    """
    Identifies entry points in the codebase.
    An entry point is a node with an in-degree of 0 (no other file imports it).

    Args:
        file_graph: networkx DiGraph of file dependencies.
    Returns:
        List of file paths that are entry points.
    """
    # Find nodes with 0 incoming edges
    entry_points = [node for node, degree in file_graph.in_degree() if degree == 0]

    # Sort for consistency
    return sorted(entry_points)
