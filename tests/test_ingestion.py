import os
import pytest
from codelens import ingestion, config

def test_discover_files(tmp_path):
    """
    Test that _discover_files finds .py files and respects ignore rules.
    """
    # 1. Create a dummy structure in a temp directory
    # root/
    #   main.py
    #   utils.py
    #   test_logic.py (should be ignored by prefix)
    #   venv/ (should be ignored)
    #     lib.py
    #   data.txt (should be ignored by extension)
    
    d = tmp_path / "repo"
    d.mkdir()
    (d / "main.py").write_text("print('hello')")
    (d / "utils.py").write_text("def run(): pass")
    (d / "test_logic.py").write_text("def test(): pass")
    (d / "data.txt").write_text("some data")
    
    venv_dir = d / "venv"
    venv_dir.mkdir()
    (venv_dir / "lib.py").write_text("secret")
    
    # 2. Run discovery
    found_files = ingestion._discover_files(str(d))
    
    # 3. Assertions
    basenames = [os.path.basename(f) for f in found_files]
    
    assert "main.py" in basenames
    assert "utils.py" in basenames
    assert "test_logic.py" not in basenames  # Ignored by prefix
    assert "lib.py" not in basenames         # Ignored because it's in venv/
    assert "data.txt" not in basenames       # Ignored by extension
    assert len(found_files) == 2

def test_ingest_local_invalid_path():
    """
    Test that ingest() raises ValueError for a non-existent local path.
    """
    with pytest.raises(ValueError, match="Source path does not exist"):
        ingestion.ingest("/non/existent/path/at/all")

def test_ingest_local_valid_path(tmp_path):
    """
    Test that ingest() works correctly for a valid local path.
    """
    d = tmp_path / "valid_repo"
    d.mkdir()
    (d / "app.py").write_text("pass")
    
    files = ingestion.ingest(str(d))
    assert len(files) == 1
    assert files[0].endswith("app.py")
