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


def _detect_critical_modules(file_graph: nx.DiGraph, top_n: int = 3) -> list[str]:
    """
    Identifies 'critical' modules using betweenness centrality.
    A critical module is a 'hub' that connects many other parts of the graph.

    Args:
        file_graph: networkx DiGraph of file dependencies.
        top_n: Number of top modules to return.
    Returns:
        List of file paths for the most central modules.
    """
    if not file_graph.nodes:
        return []

    # Compute centrality (how often a node is on the shortest path between others)
    centrality = nx.betweenness_centrality(file_graph)

    # Sort by score descending and take the top N
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

    return [node for node, score in sorted_centrality[:top_n] if score > 0]
