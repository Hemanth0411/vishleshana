"""
metrics.py — Complexity metrics for CodeLens.

Computes cyclomatic complexity (radon) for each function.
Attaches scores to file_graph nodes as metadata.
Flags functions above the configured complexity threshold.

Dependencies: radon
"""

import radon.complexity as cc
from codelens import config

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
            metrics.append({
                "name": item.name,
                "complexity": item.complexity,
                "rank": cc.cc_rank(item.complexity),
                "lineno": item.lineno
            })
        return metrics
    except Exception as e:
        print(f"Warning: Radon failed to analyze {path}: {e}")
        return []
