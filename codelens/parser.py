"""
parser.py — Static analysis and extraction for CodeLens.

Uses Python's ast module for structural extraction (functions, classes, imports)
and pyan3 for function-level call graph construction.

Dependencies: ast (stdlib), pyan3
"""

import ast
import pyan


def parse_files(file_paths: list[str]) -> dict:
    """
    Parses multiple .py files and extracts structural metadata and call edges.

    Args:
        file_paths: List of absolute .py file paths.
    Returns:
        Dictionary containing file metadata and inter-file call edges.
    """
    results = {"files": {}, "call_edges": _build_call_edges(file_paths)}

    for path in file_paths:
        try:
            results["files"][path] = _parse_single_file(path)
        except Exception as e:
            print(f"Warning: Failed to parse {path}: {e}")

    return results


def _build_call_edges(file_paths: list[str]) -> list[tuple[str, str]]:
    """
    Uses pyan3 to find function-level call edges across multiple files.

    Args:
        file_paths: List of absolute paths to .py files.
    Returns:
        List of (caller_name, callee_name) tuples.
    """
    try:
        # pyan3 uses its own internal visitor to build the call graph
        # draw_defines=False prevents it from adding 'definition' edges
        # draw_uses=True ensures it captures 'call' edges
        visitor = pyan.create_callgraph(
            filenames=file_paths, draw_defines=False, draw_uses=True
        )

        edges = []
        # Extract edges from the pyan visitor object
        # Pyan edges are objects with 'source' and 'dest' attributes
        for edge in visitor.edges:
            edges.append((str(edge.source), str(edge.dest)))

        return edges
    except Exception as e:
        print(f"Warning: pyan3 failed to build call edges: {e}")
        return []


def _parse_single_file(path: str) -> dict:
    """
    Parses a single .py file and extracts functions, classes, and docstrings.

    Args:
        path: Absolute path to the .py file.
    Returns:
        Dictionary containing extracted metadata.
    """
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    data = {
        "functions": [],
        "classes": [],
        "imports": _extract_imports(tree),
        "docstring": ast.get_docstring(tree),
        "lines": len(source.splitlines()),
    }

    for node in ast.iter_child_nodes(tree):
        # Extract Functions
        if isinstance(node, ast.FunctionDef):
            data["functions"].append(
                {
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                }
            )

        # Extract Classes
        elif isinstance(node, ast.ClassDef):
            data["classes"].append(
                {
                    "name": node.name,
                    "bases": [
                        ast.unparse(b) if hasattr(ast, "unparse") else str(b)
                        for b in node.bases
                    ],
                }
            )

    return data


def _extract_imports(tree: ast.AST) -> list[dict]:
    """
    Extracts all imports from an AST tree.
    Handles 'import x' and 'from x import y'.
    """
    imports = []
    for node in ast.walk(tree):
        # Handle 'import os'
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append({"module": n.name, "alias": n.asname})

        # Handle 'from os import path'
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            # Handle relative imports (from . import x)
            if node.level > 0:
                module = "." * node.level + module

            for n in node.names:
                imports.append({"module": module, "name": n.name, "alias": n.asname})
    return imports
