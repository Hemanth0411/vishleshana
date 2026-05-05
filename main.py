"""
main.py — Streamlit Entry Point for Vishleshana (CodeLens).

Orchestrates the entire pipeline from ingestion to AI analysis.
"""

import streamlit as st
import os
import pandas as pd
from codelens import ingestion, parser, graph_builder, metrics, analyzer, visualizer, ai_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vishleshana | Code Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS (Aesthetics) ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SESSION STATE INITIALIZATION ---
if "graph_data" not in st.session_state:
    st.session_state.graph_data = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.title("🔍 Vishleshana")
    st.caption("Graph-Aware Code Analysis")
    st.divider()

    repo_source = st.text_input(
        "GitHub URL or Local Path", placeholder="https://github.com/..."
    )
    analyze_btn = st.button(
        "Analyze Codebase", type="primary", use_container_width=True
    )

    if analyze_btn and repo_source:
        try:
            with st.status("Analyzing codebase...", expanded=True) as status:
                st.write("📥 Ingesting source...")
                file_paths = ingestion.ingest(repo_source)

                st.write(f"🔍 Parsing {len(file_paths)} files...")
                parsed_data = parser.parse_files(file_paths)

                st.write("🕸️ Building dependency graphs...")
                graph_data = graph_builder.build_graphs(parsed_data)

                st.write("📊 Computing complexity metrics...")
                graph_data["file_graph"] = metrics.compute_metrics(
                    file_paths, graph_data["file_graph"]
                )

                st.write("🧠 Performing structural analysis...")
                analysis_results = analyzer.analyze(graph_data["file_graph"])

                st.session_state.graph_data = graph_data
                st.session_state.analysis_results = analysis_results
                status.update(
                    label="Analysis Complete!", state="complete", expanded=False
                )
                st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")

    st.divider()
    if st.button("Clear Cache", use_container_width=True):
        st.session_state.graph_data = None
        st.session_state.analysis_results = None
        st.session_state.chat_history = []
        st.rerun()

# --- MAIN UI ---
st.title("Code Lens")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🕸️ Dependency Graph",
        "📈 Complexity",
        "📚 Reading Order",
        "🤖 AI Chat",
    ]
)

with tab1:
    st.header("Project Overview")
    if not st.session_state.analysis_results:
        st.info("Enter a repository source in the sidebar to begin analysis.")
    else:
        res = st.session_state.analysis_results

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Files", len(st.session_state.graph_data["file_graph"].nodes)
            )
        with col2:
            st.metric("Entry Points", len(res["entry_points"]))
        with col3:
            st.metric("Detected Cycles", "Yes" if res["has_cycles"] else "None")

        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🚀 Entry Points")
            for ep in res["entry_points"]:
                st.code(os.path.basename(ep))

        with c2:
            st.subheader("💎 Critical Modules")
            for cm in res["critical_modules"]:
                st.code(os.path.basename(cm))

with tab2:
    st.header("System Architecture")
    if not st.session_state.graph_data:
        st.info("Perform an analysis to view the dependency graph.")
    else:
        # Render the interactive Pyvis graph
        html_str = visualizer.render_graph(st.session_state.graph_data["file_graph"])

        # Use a container to handle the height properly
        st.components.v1.html(html_str, height=650, scrolling=True)

        st.caption("Tip: You can zoom, drag nodes, and hover for details.")

with tab3:
    st.header("Code Complexity")
    if not st.session_state.graph_data:
        st.info("Perform an analysis to view complexity metrics.")
    else:
        # Extract data for the table
        complexity_data = []
        for node, data in st.session_state.graph_data["file_graph"].nodes(data=True):
            complexity_data.append({
                "File": os.path.basename(node),
                "Avg Complexity": data.get("complexity_avg", 0),
                "Max Complexity": data.get("complexity_max", 0),
                "Rank": data.get("complexity_rank", "A"),
                "Flagged Functions": ", ".join(data.get("flagged_functions", [])) or "None"
            })
        
        df = pd.DataFrame(complexity_data)
        
        # Display as a sortable table
        st.dataframe(
            df.sort_values(by="Max Complexity", ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        st.info("💡 Ranks C, D, E, and F indicate high complexity that may require refactoring.")

with tab4:
    st.header("Recommended Reading Order")
    if not st.session_state.analysis_results:
        st.info("Perform an analysis to see the recommended learning path.")
    else:
        order = st.session_state.analysis_results["reading_order"]
        
        st.subheader("🚶 Step-by-Step Path")
        # Display the file list with arrows
        path_str = " → ".join([os.path.basename(f) for f in order])
        st.write(path_str)
        
        st.divider()
        
        st.subheader("💡 AI Mentor Explanation")
        with st.spinner("Asking AI for explanation..."):
            # We'll use the cached explanation if we implement that later, 
            # for now, we'll just call it directly.
            explanation = ai_client.explain_reading_order(order)
            st.markdown(explanation)

with tab5:
    st.header("Chat with your Code")
    st.info("Ask questions about the project structure.")
