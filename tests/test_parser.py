import pytest
import os
from codelens import parser


def test_parse_single_file(tmp_path):
    """
    Test that we can extract functions, classes, and docstrings correctly.
    """
    code = '''
"""Module docstring."""
import os

class MyClass(Base):
    pass

def my_function(a, b):
    pass
'''
    p = tmp_path / "sample.py"
    p.write_text(code)

    data = parser._parse_single_file(str(p))

    assert data["docstring"] == "Module docstring."
    assert data["lines"] == 9

    # Check classes
    class_names = [c["name"] for c in data["classes"]]
    assert "MyClass" in class_names
    assert data["classes"][0]["bases"] == ["Base"]

    # Check functions
    func_names = [f["name"] for f in data["functions"]]
    assert "my_function" in func_names
    assert data["functions"][0]["args"] == ["a", "b"]


def test_extract_imports(tmp_path):
    """
    Test that imports are extracted correctly including aliases and from-imports.
    """
    code = """
import os
import pandas as pd
from math import sqrt
from . import local_mod
"""
    import ast

    tree = ast.parse(code)
    imports = parser._extract_imports(tree)

    # Standard import
    assert any(i["module"] == "os" and i["alias"] is None for i in imports)

    # Alias import
    assert any(i["module"] == "pandas" and i["alias"] == "pd" for i in imports)

    # From import
    assert any(i["module"] == "math" and i["name"] == "sqrt" for i in imports)

    # Relative import
    assert any(i["module"] == "." and i["name"] == "local_mod" for i in imports)


def test_parse_files_integration(tmp_path):
    """
    Test the public parse_files API with multiple files.
    """
    f1 = tmp_path / "one.py"
    f1.write_text("def first(): pass")

    f2 = tmp_path / "two.py"
    f2.write_text("def second(): pass")

    results = parser.parse_files([str(f1), str(f2)])

    assert str(f1) in results["files"]
    assert str(f2) in results["files"]
    assert "first" in [f["name"] for f in results["files"][str(f1)]["functions"]]
    assert "second" in [f["name"] for f in results["files"][str(f2)]["functions"]]
    assert isinstance(results["call_edges"], list)
