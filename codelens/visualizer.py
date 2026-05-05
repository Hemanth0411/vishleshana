"""
visualizer.py — Graph visualization for CodeLens.

Uses Pyvis to turn NetworkX graphs into interactive HTML/JS visualizations.
Handles node styling (colors, sizes) based on analysis results.

Dependencies: pyvis, networkx
"""

import networkx as nx

def _assign_node_colors(file_graph: nx.DiGraph) -> dict[str, str]:
    """
    Assigns hex colors to nodes based on their role and complexity.
    
    Colors:
        - Blue (#3498db): Entry Point
        - Red (#e74c3c): High Complexity (Rank C, D, E, F)
        - Purple (#9b59b6): Critical Module
        - Emerald (#2ecc71): Default / Healthy
    """
    color_map = {}
    
    # Get critical modules (pre-calculated in metadata or re-calculate)
    # For now, we'll check the 'flagged_functions' and 'complexity_rank'
    
    for node, data in file_graph.nodes(data=True):
        # Default color
        color = "#2ecc71" # Emerald
        
        # 1. Check if High Complexity (Danger)
        rank = data.get("complexity_rank", "A")
        if rank in ["C", "D", "E", "F"]:
            color = "#e74c3c" # Red
            
        # 2. Check if Entry Point (No incoming edges)
        elif file_graph.in_degree(node) == 0:
            color = "#3498db" # Blue
            
        # 3. Check if Critical (This is a simplified check for now)
        # In a real run, we might have a 'is_critical' flag from analyzer
        elif data.get("is_critical"):
            color = "#9b59b6" # Purple
            
        color_map[node] = color
        
    return color_map
