"""
analyzer.py — Structural analysis for CodeLens.

Derives insights from the file dependency graph:
  - Entry points (zero in-degree nodes)
  - Critical modules (betweenness centrality)
  - Topological reading order (nx.topological_sort)

Dependencies: networkx
"""

import networkx as nx


def analyze(file_graph: nx.DiGraph) -> dict:
    """
    Performs structural analysis on the file graph.

    Args:
        file_graph: networkx DiGraph of file dependencies.
    Returns:
        Dictionary containing entry points, critical modules, and reading order.
    """
    has_cycles = not nx.is_directed_acyclic_graph(file_graph)
    cycle_nodes = []
    if has_cycles:
        try:
            cycle_nodes = list(nx.find_cycle(file_graph))
        except Exception:
            pass

    return {
        "entry_points": _detect_entry_points(file_graph),
        "critical_modules": _detect_critical_modules(file_graph),
        "reading_order": _compute_reading_order(file_graph),
        "has_cycles": has_cycles,
        "cycle_nodes": [str(node) for node in cycle_nodes],
    }


def get_path_from_entry(graph: nx.DiGraph, entry_point: str) -> list[str]:
    """
    Extracts the topological reading order for a specific entry point flow.
    """
    if entry_point not in graph:
        return []

    # Find all nodes reachable from this entry point (downstream dependencies)
    # We use reverse() logic because we want foundational files at the top
    reachable = nx.descendants(graph, entry_point) | {entry_point}
    subgraph = graph.subgraph(reachable)

    try:
        order = list(nx.topological_sort(subgraph))
        order.reverse()
        return order
    except nx.NetworkXUnfeasible:
        # Fallback if subgraph has a cycle
        return list(subgraph.nodes)


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


def _compute_reading_order(file_graph: nx.DiGraph) -> list[str]:
    """
    Computes a recommended reading order for the codebase.
    Uses topological sort (dependencies first).
    Handles circular imports by falling back to in-degree sorting.

    Args:
        file_graph: networkx DiGraph of file dependencies.
    Returns:
        Ordered list of file paths.
    """
    if not file_graph.nodes:
        return []

    try:
        # Check if we can do a standard topological sort (only works on DAGs)
        if nx.is_directed_acyclic_graph(file_graph):
            # Reverse it so dependencies (A) come before users (B)
            order = list(nx.topological_sort(file_graph))
            order.reverse()
            return order
        else:
            # If there are circular imports, fall back to sorting by in-degree
            # Files with fewer things depending on them come first (highest in-degree at the end)
            sorted_nodes = sorted(
                file_graph.in_degree(), key=lambda x: x[1], reverse=True
            )
            return [node for node, degree in sorted_nodes]
    except Exception as e:
        print(f"Warning: Topological sort failed, falling back to alphabetical: {e}")
        return sorted(list(file_graph.nodes))
