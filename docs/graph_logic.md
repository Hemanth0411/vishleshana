# 🕸️ Graph Construction Logic

This module turns flat metadata into a living network using the `networkx` library.

## 1. `_build_file_graph(parsed_data: dict)`
- **Purpose**: Creates the high-level architecture view.
- **How it works**:
    1. Every file becomes a **Node** in a `nx.DiGraph` (Directed Graph).
    2. We attach metadata (lines, functions, classes) to each node.
    3. Every import becomes an **Edge** (Arrow).
- **Pros**: Allows for mathematical analysis like "find the most important file."
- **Cons**: Can become cluttered ("Spaghetti Graph") in very large projects.

## 2. `_resolve_import(module_name: str, all_files: list)`
- **Purpose**: Connects the string `import app.utils` to the file `/path/to/app/utils.py`.
- **How it works**: Converts the dots in the module name to the system's path separator (`/` or `\`) and checks if any project file ends with that path.
- **Why this way?**:
    - **Pros**: Robust across different OS (Windows vs Linux).
    - **Cons**: Might fail if multiple files have the same suffix (though rare in Python).

## 3. `_build_call_graph(parsed_data: dict)`
- **Purpose**: Creates a low-level view of function interactions.
- **How it works**: Simply maps the caller/callee pairs from the parsing step into a new `networkx` graph.
- **Pros**: Perfect for finding "Dead Code" (functions that are never called).
