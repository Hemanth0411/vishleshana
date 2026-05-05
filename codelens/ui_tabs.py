"""
ui_tabs.py — UI rendering components for CodeLens tabs.
Keeps main.py lean and modular.
"""

import streamlit as st
import os
import pandas as pd
from codelens import visualizer, ai_client

def render_overview():
    st.header("Project Overview")
    if not st.session_state.analysis_results:
        st.info("Enter a repository source in the sidebar to begin analysis.")
        return

    res = st.session_state.analysis_results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Files", len(st.session_state.graph_data["file_graph"].nodes))
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

def render_graph():
    st.header("System Architecture")
    if not st.session_state.graph_data:
        st.info("Perform an analysis to view the dependency graph.")
    else:
        html_str = visualizer.render_graph(st.session_state.graph_data["file_graph"])
        st.components.v1.html(html_str, height=650, scrolling=True)
        st.caption("Tip: You can zoom, drag nodes, and hover for details.")

def render_complexity():
    st.header("Code Complexity")
    if not st.session_state.graph_data:
        st.info("Perform an analysis to view complexity metrics.")
        return

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
    st.dataframe(
        df.sort_values(by="Max Complexity", ascending=False),
        use_container_width=True,
        hide_index=True
    )
    st.info("💡 Ranks C, D, E, and F indicate high complexity.")

def render_reading_order():
    st.header("Recommended Reading Order")
    if not st.session_state.analysis_results:
        st.info("Perform an analysis to see the recommended learning path.")
        return

    order = st.session_state.analysis_results["reading_order"]
    st.subheader("🚶 Step-by-Step Path")
    st.write(" → ".join([os.path.basename(f) for f in order]))
    st.divider()
    st.subheader("💡 AI Mentor Explanation")
    
    if "reading_order_explanation" not in st.session_state:
        with st.spinner("Asking AI for explanation..."):
            st.session_state.reading_order_explanation = ai_client.explain_reading_order(order)
    
    st.markdown(st.session_state.reading_order_explanation)

def render_chat():
    st.header("Chat with your Code")
    if not st.session_state.graph_data:
        st.info("Analysis required for chat.")
        return

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the codebase..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ai_client.answer_query(prompt, st.session_state.graph_data)
                st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
