"""
parser.py — Static analysis and extraction for CodeLens.

Uses Python's ast module for structural extraction (functions, classes, imports)
and pyan3 for function-level call graph construction.

Dependencies: ast (stdlib), pyan3
"""

import ast
import os

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
        "imports": [],  # Will be implemented in Issue #23
        "docstring": ast.get_docstring(tree),
        "lines": len(source.splitlines())
    }
    
    for node in ast.iter_child_nodes(tree):
        # Extract Functions
        if isinstance(node, ast.FunctionDef):
            data["functions"].append({
                "name": node.name,
                "lineno": node.lineno,
                "args": [arg.arg for arg in node.args.args]
            })
            
        # Extract Classes
        elif isinstance(node, ast.ClassDef):
            data["classes"].append({
                "name": node.name,
                "bases": [ast.unparse(b) if hasattr(ast, 'unparse') else str(b) for b in node.bases]
            })
            
    return data
