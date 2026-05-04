# 🔍 Parsing Module Logic

The Parsing module turns raw text into structural data using Abstract Syntax Trees (AST).

## 1. `_parse_single_file(path: str)`
- **Purpose**: Extracts functions, classes, and docstrings from a file.
- **How it works**: Uses the built-in `ast.parse()` to build a tree. It then iterates through the top-level nodes of that tree.
- **Why this way?**:
    - **Pros**: 100% accurate structural info without running the code (Static Analysis).
    - **Cons**: It cannot see "dynamic" attributes (e.g., functions added via decorators or `setattr`).
- **Logic Details**: It specifically looks for `ast.FunctionDef` and `ast.ClassDef` nodes.

## 2. `_extract_imports(tree: ast.AST)`
- **Purpose**: Finds all dependencies of a file.
- **How it works**: Uses `ast.walk()` to visit every node in the file (even those nested in functions).
- **Why this way?**:
    - **Pros**: Finds imports even if they are "hidden" inside an `if` block or a function.
    - **Cons**: Can't resolve imports that are strings or calculated at runtime.
- **Logic Details**: Handles both `import x` (`ast.Import`) and `from x import y` (`ast.ImportFrom`).

## 3. `_build_call_edges(file_paths: list)`
- **Purpose**: Tracks how functions talk to each other across files.
- **How it works**: Utilizes the `pyan3` library, which performs its own AST walk to find function calls.
- **Why this way?**:
    - **Pros**: Cross-file visibility. It knows that `A()` in `main.py` calls `B()` in `utils.py`.
    - **Cons**: `pyan3` is sensitive to complex Python syntax and can sometimes miss edges in highly dynamic code.

## 4. `parse_files(file_paths: list)`
- **Purpose**: Orchestrates the parsing of a whole project.
- **Logic Details**: It builds a dictionary where each file path is a key, containing the metadata extracted by the functions above.
