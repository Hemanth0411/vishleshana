# 📊 Metrics Logic

This module measures the "health" and "danger" of the codebase using the `radon` library.

## 1. `_analyze_file(path: str)`
- **Purpose**: Calculates Cyclomatic Complexity (CC).
- **How it works**: Uses `radon.complexity.cc_visit()`. This counts the number of independent paths through a function's code (if-statements, loops, etc.).
- **Scoring**:
    - **1-5 (Rank A)**: Simple, clean code.
    - **6-10 (Rank B)**: Moderate complexity.
    - **11+ (Rank C-F)**: "Danger Zone". Hard to maintain and test.
- **Why this way?**:
    - **Pros**: Objective. It's not a "guess" about complexity; it's a mathematical count of logic branches.
    - **Cons**: High CC doesn't *always* mean bad code (some algorithms are inherently complex).

## 2. `compute_metrics(file_paths, file_graph)`
- **Purpose**: Aggregates data and "flags" offenders.
- **Logic Details**: It calculates the **Average** and **Max** complexity for each file. If any function exceeds the threshold set in `.env`, its name is added to the `flagged_functions` list for that node.
- **Pros**: The AI can now prioritize explaining the "Complex" parts of the project first.
