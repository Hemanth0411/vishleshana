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
        complexity_data.append(
            {
                "File": os.path.basename(node),
                "Avg Complexity": data.get("complexity_avg", 0),
                "Max Complexity": data.get("complexity_max", 0),
                "Rank": data.get("complexity_rank", "A"),
                "Flagged Functions": ", ".join(data.get("flagged_functions", []))
                or "None",
            }
        )

    df = pd.DataFrame(complexity_data)
    st.dataframe(
        df.sort_values(by="Max Complexity", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.info("💡 Ranks C, D, E, and F indicate high complexity.")


def render_reading_order():
    st.header("Recommended Reading Order")
    if not st.session_state.analysis_results:
        st.info("Perform an analysis to see the recommended learning path.")
        return

    order = st.session_state.analysis_results["reading_order"]
    entry_points = st.session_state.analysis_results["entry_points"]
    
    st.subheader("🚶 Step-by-Step Path")
    
    # Selection for Multiple Flows
    flow_options = ["Global Project Order"] + [os.path.basename(ep) for ep in entry_points]
    selected_flow = st.selectbox("Select Project Flow", flow_options)
    
    # Calculate the order for the selected flow
    if selected_flow == "Global Project Order":
        display_order = order
    else:
        # Map basename back to full path
        full_path = next(ep for ep in entry_points if os.path.basename(ep) == selected_flow)
        from codelens import analyzer
        display_order = analyzer.get_path_from_entry(st.session_state.graph_data["file_graph"], full_path)

    # Use an interactive flowchart (minimized by default)
    with st.expander("Explore Interactive Flowchart", expanded=False):
        html_str = visualizer.render_reading_path(display_order)
        st.components.v1.html(html_str, height=650, scrolling=True)
    
    st.divider()
    st.subheader("💡 AI Mentor Explanation")

    if "reading_order_explanation" not in st.session_state:
        with st.spinner("Asking AI for explanation..."):
            st.session_state.reading_order_explanation = (
                ai_client.explain_reading_order(order)
            )

    st.markdown(st.session_state.reading_order_explanation)


def render_chat():
    st.header("Chat with your Code")
    if not st.session_state.graph_data:
        st.info("👋 Welcome! Please enter a repository path in the sidebar and click 'Analyze Project' to enable AI Chat.")
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


def render_query():
    st.header("Semantic Query")
    if not st.session_state.graph_data:
        st.info("🔍 Ready to search? Run an analysis in the sidebar to start querying your codebase logic.")
        return

    query = st.text_input(
        "Search for specific logic or features...",
        placeholder="e.g. How does the authentication work?",
    )

    if st.button("Query Codebase", type="primary"):
        with st.spinner("Searching graph and generating answer..."):
            response = ai_client.answer_query(query, st.session_state.graph_data)

            st.markdown("### Answer")
            st.markdown(response)

            # Check if README was found for debugging
            has_readme = any("readme" in os.path.basename(n).lower() for n in st.session_state.graph_data["file_graph"].nodes)
            if has_readme:
                st.success("✅ Analysis grounded in Project README.")
            else:
                st.warning("⚠️ No README found in analysis. AI is using structural inference.")

            st.divider()
            with st.expander("📌 Context Attribution"):
                # --- CONTEXT ATTRIBUTION ENGINE ---
                keywords = query.lower().split()
                file_graph = st.session_state.graph_data["file_graph"]
                matches = []
                
                # Fuzzy match across labels, docstrings, and function names
                for node, data in file_graph.nodes(data=True):
                    functions_str = " ".join([f["name"] for f in data.get("functions", [])])
                    search_blob = f"{data.get('label', '')} {data.get('docstring', '')} {functions_str}".lower()
                    
                    # If any significant keyword (>=3 chars) is in the metadata
                    if any(word in search_blob for word in keywords if len(word) >= 3):
                        matches.append(node)

                # Display attribution
                if matches:
                    st.caption("The AI consulted the following files to generate this answer:")
                    for m in set(matches):
                        st.markdown(f"- `{os.path.basename(m)}`")
                else:
                    st.caption("General knowledge / Global summary used.")
