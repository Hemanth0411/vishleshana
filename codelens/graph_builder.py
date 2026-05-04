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
            docstring=meta["docstring"] or "",
        )

    # 2. Resolve imports and add edges
    all_file_paths = list(parsed_data["files"].keys())
    for path, meta in parsed_data["files"].items():
        for imp in meta["imports"]:
            target_path = _resolve_import(imp["module"], all_file_paths)
            if target_path and target_path != path:
                G.add_edge(path, target_path)

    return G


def _resolve_import(module_name: str, all_file_paths: list[str]) -> str | None:
    """
    Attempts to map a module name (e.g., 'codelens.config')
    to an actual file path in the project.
    """
    if not module_name:
        return None

    # Convert dots to path separators
    module_path_part = module_name.replace(".", os.sep)

    for path in all_file_paths:
        # Check if the file path ends with the module name + .py
        # e.g., if path is '.../codelens/config.py' and module is 'codelens.config'
        if path.endswith(module_path_part + ".py") or path.endswith(
            module_path_part + os.sep + "__init__.py"
        ):
            return path

    return None


def _build_call_graph(parsed_data: dict) -> nx.DiGraph:
    """
    Creates a directed graph where nodes are functions and edges are calls.

    Args:
        parsed_data: Output of parser.parse_files()
    Returns:
        A networkx DiGraph of function calls.
    """
    G = nx.DiGraph()

    # Add edges from pyan3 data
    # Edges are (caller_name, callee_name)
    for caller, callee in parsed_data["call_edges"]:
        G.add_edge(caller, callee)

    return G
