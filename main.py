"""
main.py — Streamlit Entry Point for Vishleshana (CodeLens).

Orchestrates the entire pipeline from ingestion to AI analysis.
"""

import streamlit as st
import os
from codelens import ingestion, parser, graph_builder

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vishleshana | Code Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS (Aesthetics) ---
st.markdown("""
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
    """, unsafe_allow_html=True)

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
    
    repo_source = st.text_input("GitHub URL or Local Path", placeholder="https://github.com/...")
    analyze_btn = st.button("Analyze Codebase", type="primary", use_container_width=True)
    
    if analyze_btn and repo_source:
        try:
            with st.status("Analyzing codebase...", expanded=True) as status:
                st.write("📥 Ingesting source...")
                file_paths = ingestion.ingest(repo_source)
                
                st.write(f"🔍 Parsing {len(file_paths)} files...")
                parsed_data = parser.parse_files(file_paths)
                
                st.write("🕸️ Building dependency graphs...")
                graph_data = graph_builder.build_graphs(parsed_data)
                
                st.session_state.graph_data = graph_data
                status.update(label="Analysis Complete!", state="complete", expanded=False)
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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "🕸️ Dependency Graph", 
    "📈 Complexity", 
    "📚 Reading Order", 
    "🤖 AI Chat"
])

with tab1:
    st.header("Project Overview")
    if not st.session_state.analysis_results:
        st.info("Enter a repository source in the sidebar to begin analysis.")
    else:
        st.success("Analysis Complete!")

with tab2:
    st.header("System Architecture")
    st.info("Visualization will appear here.")

with tab3:
    st.header("Code Complexity")
    st.info("Complexity metrics will appear here.")

with tab4:
    st.header("Recommended Reading Order")
    st.info("AI mentorship path will appear here.")

with tab5:
    st.header("Chat with your Code")
    st.info("Ask questions about the project structure.")
