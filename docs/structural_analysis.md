# 🧠 Structural Analysis Logic

This is the "Brain" of the project. It uses Graph Theory to extract insights from the network.

## 1. `_detect_entry_points(file_graph)`
- **Purpose**: Finds the "Front Doors" of the project.
- **Logic**: It identifies nodes with **In-Degree 0**. If no other file in the project imports a module, it is statistically likely to be a script, a CLI entry, or a main orchestrator.

## 2. `_detect_critical_modules(file_graph)`
- **Purpose**: Finds the "Heart" of the project.
- **Logic**: Uses **Betweenness Centrality**. This algorithm finds nodes that act as "bridges" between other parts of the graph.
- **Why this way?**:
    - **Pros**: It finds "Implicit" importance. A small utility file that everyone imports might be more critical than a large feature file.
    - **Cons**: Can be slow on massive graphs (though not an issue for our size).

## 3. `_compute_reading_order(file_graph)`
- **Purpose**: Recommends the best sequence to learn the project.
- **Logic**: Performs a **Topological Sort**.
    - We reverse the sort so that **Dependencies** (Base classes, Utils) appear at the top.
    - **Fallbacks**: If there is a "Circular Import" (A -> B -> A), a standard sort fails. We fall back to **In-Degree Sorting** (files with fewer incoming dependencies first).
- **Pros**: It prevents a developer from starting with "Complex Feature X" before they've read "Base Config A."
