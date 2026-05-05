"""
main.py — Streamlit Entry Point for Vishleshana (CodeLens).
Orchestrates the entire pipeline.
"""

import streamlit as st
from codelens import ingestion, parser, graph_builder, metrics, analyzer, ui_tabs

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vishleshana | Code Analysis",
    page_icon="🔍",
    layout="wide",
)

# --- AESTHETICS ---
st.markdown("<style>.main {background-color: #0e1117;}</style>", unsafe_allow_html=True)

# --- SESSION STATE ---
for key in ["graph_data", "analysis_results", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "chat_history" else None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔍 Vishleshana")
    repo_source = st.text_input(
        "GitHub URL or Local Path", placeholder="https://github.com/..."
    )

    if (
        st.button("Analyze Codebase", type="primary", use_container_width=True)
        and repo_source
    ):
        try:
            with st.status("Analyzing codebase...", expanded=True) as status:
                st.write("📥 Ingesting...")
                file_paths = ingestion.ingest(repo_source)
                st.write("🔍 Parsing...")
                parsed_data = parser.parse_files(file_paths)
                st.write("🕸️ Graphing...")
                g = graph_builder.build_graphs(parsed_data)
                st.write("📊 Metrics...")
                g["file_graph"] = metrics.compute_metrics(file_paths, g["file_graph"])
                st.write("🧠 Analyzing...")
                st.session_state.analysis_results = analyzer.analyze(g["file_graph"])
                st.session_state.graph_data = g
                if "reading_order_explanation" in st.session_state:
                    del st.session_state.reading_order_explanation
                status.update(label="Complete!", state="complete", expanded=False)
                st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")

    if st.button("Clear Cache", use_container_width=True):
        for key in [
            "graph_data",
            "analysis_results",
            "chat_history",
            "reading_order_explanation",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- MAIN UI ---
st.title("Code Lens")
tabs = st.tabs(
    [
        "📊 Overview",
        "🕸️ Graph",
        "📈 Complexity",
        "📚 Reading Order",
        "🤖 AI Chat",
        "🔍 Query",
    ]
)

with tabs[0]:
    ui_tabs.render_overview()
with tabs[1]:
    ui_tabs.render_graph()
with tabs[2]:
    ui_tabs.render_complexity()
with tabs[3]:
    ui_tabs.render_reading_order()
with tabs[4]:
    ui_tabs.render_chat()
with tabs[5]:
    ui_tabs.render_query()
