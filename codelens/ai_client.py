"""
ai_client.py — AI reasoning for Vishleshana via NVIDIA NIM.
Implements summarization, mentorship, and Q&A.
"""

import os
from openai import OpenAI
from codelens import config


def _get_client():
    """Initializes the OpenAI-compatible NIM client."""
    return OpenAI(base_url=config.NIM_BASE_URL, api_key=config.NIM_API_KEY)


def generate_summary(graph_data: dict) -> str:
    """
    Generates a high-level architectural summary of the codebase.
    """
    if not graph_data or "file_graph" not in graph_data:
        return "No files detected to summarize."

    file_graph = graph_data["file_graph"]
    if not file_graph.nodes:
        return "No files detected in the graph."

    # Build a compact manifest from graph nodes
    manifest = []
    for node, data in list(file_graph.nodes(data=True))[:15]: # Limit to first 15 for summary
        manifest.append(f"File: {os.path.basename(node)}\nDocstring: {data.get('docstring', 'N/A')}")

    manifest_str = "\n\n".join(manifest)

    prompt = f"""
    You are an expert Software Architect. Summarize the following Python codebase.
    Focus on the architectural patterns, the main purpose of the project, 
    and how the key modules interact.

    CODEBASE MANIFEST:
    {manifest_str}

    SUMMARY:
    """

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config.NIM_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"


def explain_reading_order(reading_order: list[str]) -> str:
    """
    Provides a mentorship-style explanation of the recommended reading path.
    """
    if not reading_order:
        return "No files to explain."

    order_str = "\n".join(
        [f"{i+1}. {os.path.basename(f)}" for i, f in enumerate(reading_order)]
    )

    prompt = f"""
    You are a Senior Software Architect performing a deep structural review.
    Analyze the following 'Topological Reading Order' (dependency-first) and provide an expert guide:
    
    {order_str}
    
    Analysis Requirements:
    1. Skip the generic introductions. Start immediately with the structural logic.
    2. Group the files into architectural layers (e.g., Data, Logic, Entry Points).
    3. Identify the 'Aha!' moment—the file where the system's core value is realized.
    
    Tone: Precise, professional, and insightful.
    Format: Use clean Markdown with bold headings.
    """

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config.NIM_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error explaining reading order: {e}"


def answer_query(query: str, graph_data: dict) -> str:
    """
    Finds relevant files in the graph based on the query and asks NIM for an answer.
    """
    if not graph_data or "file_graph" not in graph_data:
        return "Please run an analysis from the sidebar to provide the AI with project context."

    file_graph = graph_data["file_graph"]
    
    # 1. Gather global context (README is the highest priority)
    global_context = ""
    for node, data in file_graph.nodes(data=True):
        filename = os.path.basename(node).lower()
        if "readme" in filename and filename.endswith((".md", ".txt", ".markdown")):
            content = data.get('docstring', '')[:4000]
            global_context = f"--- PROJECT VISION (from README) ---\n{content}\n\n"
            break

    # 2. Find specific relevant files (Fuzzy matching)
    keywords = query.lower().split()
    relevant_files = []
    for node, data in file_graph.nodes(data=True):
        search_blob = f"{os.path.basename(node)} {data.get('docstring', '')}".lower()
        if any(word in search_blob for word in keywords if len(word) >= 3):
            content = data.get('docstring', '')[:1500]
            relevant_files.append(f"File: {os.path.basename(node)}\n{content}")

    # 3. Build the grounded prompt
    context_str = global_context + "\n---\n".join(relevant_files[:4])
    
    if not context_str.strip():
        # Fallback: List the project structure
        context_str = "Project Structure: " + ", ".join([os.path.basename(f) for f in file_graph.nodes])

    prompt = f"""
    You are an expert AI Codebase Assistant. 
    Using the CONTEXT provided below, answer the user's QUESTION.
    
    CRITICAL INSTRUCTION:
    - The 'PROJECT VISION' section from the README is the DEFINITIVE source of truth for the project name, purpose, and branding.
    - If the code headers use an old name (like CodeLens) but the README uses a new name (like Vishleshana), use the NEW name.

    SPECIAL INSTRUCTIONS:
    - Classify the project type: TEMPLATE, BOILERPLATE, EXAMPLE, PRODUCTION, LIBRARY/SDK, POC, or UTILITY.
    - If the context explicitly answers the question, summarize the answer.
    - If the context doesn't explicitly answer, use the available metadata to make a professional architectural inference.
    - NEVER say "I don't know" if there is at least some project structure or README provided.

    CONTEXT:
    {context_str}

    QUESTION: {query}
    
    ANSWER:
    """

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config.NIM_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error answering query: {e}"
