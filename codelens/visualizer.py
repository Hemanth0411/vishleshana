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
    Renders a NetworkX file graph into an interactive HTML string using Pyvis.
    """
    nt = Network(height="650px", width="100%", bgcolor="#0e1117", font_color="white", directed=True)
    
    colors = _assign_node_colors(file_graph)
    # Get current workspace to calculate relative paths
    cwd = os.getcwd()

    for node, data in file_graph.nodes(data=True):
        label = data.get("label", os.path.basename(node))
        # Use relative path for tooltip
        rel_path = os.path.relpath(node, cwd) if os.path.isabs(node) else node
        nt.add_node(node, label=label, title=f"/{rel_path}", color=colors.get(node, "#2ecc71"))

    for source, target in file_graph.edges():
        nt.add_edge(source, target, color="#5d6d7e")

    # Force instant centering via aggressive stabilization
    nt.options = {
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 100,
                "springConstant": 0.08
            },
            "solver": "forceAtlas2Based",
            "stabilization": {
                "enabled": True,
                "iterations": 2000,  # Increase iterations for instant fit
                "fit": True          # Auto-fit to screen after stabilization
            }
        },
        "interaction": {
            "navigationButtons": True,
            "hover": True
        }
    }
    
    return nt.generate_html()


def render_reading_path(reading_order: list[str]) -> str:
    """
    Creates an interactive flowchart for the topological reading order.
    """
    from pyvis.network import Network
    
    nt = Network(height="600px", width="100%", bgcolor="#0e1117", font_color="white", directed=True)
    cwd = os.getcwd()

    for i, path in enumerate(reading_order):
        name = os.path.basename(path)
        # Calculate relative path for tooltip
        rel_path = os.path.relpath(path, cwd) if os.path.isabs(path) else path
        nt.add_node(path, label=f"{i+1}. {name}", title=f"/{rel_path}", shape="box", color="#3498db")
        if i > 0:
            nt.add_edge(reading_order[i-1], path, color="#5d6d7e", width=2)

    # Clean hierarchical layout with native tools and instant centering
    nt.options = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "UD",
                "sortMethod": "directed",
                "nodeSpacing": 200,
                "levelSeparation": 150
            }
        },
        "interaction": {
            "navigationButtons": True,
            "hover": True,
            "keyboard": True
        },
        "physics": {
            "enabled": True,  # Temporarily enable for stabilization
            "stabilization": {
                "enabled": True,
                "iterations": 1000,
                "fit": True
            }
        }
    }
    
    return nt.generate_html()


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

    for node, data in file_graph.nodes(data=True):
        # Default color
        color = "#2ecc71"  # Emerald

        # 1. Check if High Complexity (Danger)
        rank = data.get("complexity_rank", "A")
        if rank in ["C", "D", "E", "F"]:
            color = "#e74c3c"  # Red

        # 2. Check if Entry Point (No incoming edges)
        elif file_graph.in_degree(node) == 0:
            color = "#3498db"  # Blue

        # 3. Check if Critical
        elif data.get("is_critical"):
            color = "#9b59b6"  # Purple

        color_map[node] = color

    return color_map
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
        color = "#2ecc71"  # Emerald

        # 1. Check if High Complexity (Danger)
        rank = data.get("complexity_rank", "A")
        if rank in ["C", "D", "E", "F"]:
            color = "#e74c3c"  # Red

        # 2. Check if Entry Point (No incoming edges)
        elif file_graph.in_degree(node) == 0:
            color = "#3498db"  # Blue

        # 3. Check if Critical (This is a simplified check for now)
        # In a real run, we might have a 'is_critical' flag from analyzer
        elif data.get("is_critical"):
            color = "#9b59b6"  # Purple

        color_map[node] = color

    return color_map
