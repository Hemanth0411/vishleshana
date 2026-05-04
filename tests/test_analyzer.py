import pytest
import networkx as nx
from codelens import analyzer


def test_detect_entry_points():
    """
    Test that nodes with in-degree 0 are correctly identified.
    """
    G = nx.DiGraph()
    G.add_edge("main.py", "utils.py")
    G.add_edge("utils.py", "db.py")
    G.add_node("standalone.py")

    entry_points = analyzer._detect_entry_points(G)
    assert "main.py" in entry_points
    assert "standalone.py" in entry_points
    assert "utils.py" not in entry_points


def test_detect_critical_modules():
    """
    Test that central nodes are identified.
    """
    G = nx.DiGraph()
    # 'hub.py' is the bridge between two groups
    G.add_edge("a.py", "hub.py")
    G.add_edge("b.py", "hub.py")
    G.add_edge("hub.py", "c.py")
    G.add_edge("hub.py", "d.py")

    critical = analyzer._detect_critical_modules(G, top_n=1)
    assert critical == ["hub.py"]


def test_compute_reading_order_dag():
    """
    Test reading order for a Directed Acyclic Graph (no cycles).
    """
    G = nx.DiGraph()
    G.add_edge("B.py", "A.py")  # B depends on A

    order = analyzer._compute_reading_order(G)
    assert order.index("A.py") < order.index("B.py")


def test_compute_reading_order_cycle():
    """
    Test reading order fallback when a cycle exists.
    """
    G = nx.DiGraph()
    G.add_edge("A.py", "B.py")
    G.add_edge("B.py", "A.py")

    order = analyzer._compute_reading_order(G)
    assert len(order) == 2
    assert "A.py" in order
    assert "B.py" in order


def test_analyze_integration():
    """
    Test the public analyze API.
    """
    G = nx.DiGraph()
    G.add_edge("main.py", "utils.py")

    results = analyzer.analyze(G)
    assert results["entry_points"] == ["main.py"]
    assert "reading_order" in results
    assert results["has_cycles"] is False
