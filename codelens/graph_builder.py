"""
graph_builder.py — Graph construction for CodeLens.

Builds two directed graphs from parsed code data:
  1. File dependency graph (nodes = files, edges = imports)
  2. Function call graph (nodes = functions, edges = calls)

Dependencies: networkx
"""

import networkx as nx
import os

def _build_file_graph(parsed_data: dict) -> nx.DiGraph:
    """
    Creates a directed graph where nodes are files and edges are imports.
    
    Args:
        parsed_data: Output of parser.parse_files()
    Returns:
        A networkx DiGraph with file metadata on each node.
    """
    G = nx.DiGraph()
    
    # 1. Add all files as nodes first
    for path, meta in parsed_data["files"].items():
        G.add_node(
            path,
            label=os.path.basename(path),
            functions=meta["functions"],
            classes=meta["classes"],
            lines=meta["lines"],
            docstring=meta["docstring"] or ""
        )
        
    return G
