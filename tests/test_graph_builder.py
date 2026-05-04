import pytest
import networkx as nx
from codelens import graph_builder

def test_resolve_import():
    """
    Test that module names are correctly mapped to file paths.
    """
    all_files = [
        "/app/main.py",
        "/app/utils/helper.py",
        "/app/models/__init__.py"
    ]
    
    # Direct match
    assert graph_builder._resolve_import("main", all_files) == "/app/main.py"
    
    # Nested match
    assert graph_builder._resolve_import("utils.helper", all_files) == "/app/utils/helper.py"
    
    # Init match
    assert graph_builder._resolve_import("models", all_files) == "/app/models/__init__.py"
    
    # No match
    assert graph_builder._resolve_import("os", all_files) is None

def test_build_file_graph():
    """
    Test that nodes and edges are created correctly in the file graph.
    """
    parsed_data = {
        "files": {
            "main.py": {
                "functions": [], "classes": [], "lines": 10, "docstring": "",
                "imports": [{"module": "utils"}]
            },
            "utils.py": {
                "functions": [], "classes": [], "lines": 5, "docstring": "",
                "imports": []
            }
        },
        "call_edges": []
    }
    
    graphs = graph_builder.build_graphs(parsed_data)
    fg = graphs["file_graph"]
    
    assert "main.py" in fg.nodes
    assert "utils.py" in fg.nodes
    assert fg.has_edge("main.py", "utils.py")
    assert fg.nodes["main.py"]["lines"] == 10

def test_build_call_graph():
    """
    Test that function call edges are added correctly.
    """
    parsed_data = {
        "files": {},
        "call_edges": [("main", "helper"), ("helper", "db_save")]
    }
    
    graphs = graph_builder.build_graphs(parsed_data)
    cg = graphs["call_graph"]
    
    assert cg.has_edge("main", "helper")
    assert cg.has_edge("helper", "db_save")
    assert len(cg.nodes) == 3
