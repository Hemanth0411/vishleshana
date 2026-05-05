"""
visualizer.py — Graph visualization for CodeLens.

Uses Pyvis to turn NetworkX graphs into interactive HTML/JS visualizations.
Handles node styling (colors, sizes) based on analysis results.

Dependencies: pyvis, networkx
"""

import networkx as nx
import os
from pyvis.network import Network

def render_graph(file_graph: nx.DiGraph) -> str:
    """
    Converts a networkx graph into an interactive Pyvis HTML visualization.
    
    Returns:
        A string containing the full HTML/JS for the visualization.
    """
    # Initialize Pyvis Network
    # notebook=False because we want a standalone HTML string
    # directed=True for our dependency arrows
    nt = Network(height="600px", width="100%", directed=True, bgcolor="#ffffff", font_color="#2c3e50")
    
    # Assign colors
    colors = _assign_node_colors(file_graph)
    
    # Add Nodes
    for node, data in file_graph.nodes(data=True):
        label = data.get("label", os.path.basename(node))
        
        # Build tooltip (title)
        functions = [f["name"] for f in data.get("functions", [])]
        title = f"File: {label}\n"
        title += f"Docstring: {data.get('docstring', 'N/A')}\n"
        title += f"Functions: {', '.join(functions[:5])}{'...' if len(functions)>5 else ''}"
        
        nt.add_node(
            node, 
            label=label, 
            color=colors.get(node), 
            title=title,
            borderWidth=2
        )
        
    # Add Edges
    for source, target in file_graph.edges():
        nt.add_edge(source, target, color="#bdc3c7")
        
    # Disable physics for large graphs to prevent "jumping"
    nt.toggle_physics(True)
    
    # Generate the HTML string
    return nt.generate_html()
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
