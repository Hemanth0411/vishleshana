# 🕸️ Visualization & UI Logic

This layer handles how the user interacts with the analysis results. It focuses on making complex data intuitive and interactive.

## 1. `visualizer.py` (Milestone 8)
- **`_assign_node_colors`**:
    - **Logic**: It maps code roles to a visual hierarchy.
    - **Entry Points (Blue)**: Shows where to start.
    - **Danger Zones (Red)**: Highlights files with high Cyclomatic Complexity.
    - **Critical Hubs (Purple)**: Highlights the most important "bridge" files.
- **`render_graph`**:
    - **How it works**: Uses `Pyvis` to generate a standalone HTML/JS block. It includes a physics engine for auto-layout and rich tooltips that appear on hover.

## 2. `main.py` & `ui_tabs.py` (Milestone 9)
- **Modular Architecture**:
    - `main.py` acts as the **Orchestrator**. It handles the sidebar, progress bars, and the high-level tab structure.
    - `ui_tabs.py` handles the **Rendering**. Each tab has its own dedicated function, keeping the codebase under the 200-line modular limit.
- **Session State Management**:
    - **Purpose**: To keep the dashboard fast and responsive.
    - **Logic**: Analysis results and AI explanations are cached in `st.session_state`. This means if you switch from the "Graph" tab to the "AI Chat" tab, the system doesn't have to re-analyze the whole project.
- **Progress Tracking**: Uses `st.status` to provide real-time feedback during the 5-stage analysis pipeline (Ingest → Parse → Graph → Metrics → Analyze).

## 3. The Query System
- **Context Attribution**:
    - **Purpose**: Transparency.
    - **Logic**: In the Query tab, we use a dedicated expander to show the user exactly which files the system cited. This allows developers to verify the AI's answer by looking at the source code.
