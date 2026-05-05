"""
ai_client.py — AI reasoning for CodeLens via NVIDIA NIM.

Uses the OpenAI-compatible API to interact with hosted LLMs.
Handles prompt construction and context-aware responses.

Dependencies: openai
"""

import os
from openai import OpenAI
from codelens import config


def _get_client() -> OpenAI:
    """
    Initializes and returns an OpenAI-compatible client for NVIDIA NIM.
    """
    return OpenAI(base_url=config.NIM_BASE_URL, api_key=config.NIM_API_KEY)


def test_connection() -> bool:
    """
    Performs a simple health check to verify the NIM API connection.
    Returns: True if successful, False otherwise.
    """
    try:
        client = _get_client()
        # Simple ping request
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5,
        )
        return True if response.choices else False
    except Exception as e:
        print(f"Error: NIM API connection failed: {e}")
        return False


def generate_summary(graph_data: dict) -> str:
    """
    Constructs a prompt from graph metadata and asks NIM to summarize the project.

    Args:
        graph_data: Dictionary containing 'file_graph' and 'call_graph'.
    Returns:
        A text summary of the codebase.
    """
    file_graph = graph_data["file_graph"]

    # 1. Build context string from graph nodes
    context_lines = []
    for node, data in file_graph.nodes(data=True):
        line = f"- File: {data.get('label')}\n"
        line += f"  Summary: {data.get('docstring') or 'No docstring'}\n"
        line += f"  Functions: {', '.join([f['name'] for f in data.get('functions', [])])}\n"
        line += f"  Complexity Rank: {data.get('complexity_rank', 'N/A')}\n"
        context_lines.append(line)

    context_str = "\n".join(context_lines)

    # 2. Construct the prompt
    prompt = f"""
You are an expert software architect. Below is a summary of a Python codebase extracted via static analysis.
Please provide a high-level summary of the project's purpose, architecture, and core features based on this data.

CODEBASE CONTEXT:
{context_str}

SUMMARY:
"""

    # 3. Call NIM
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=config.NIM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful software architect."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=config.NIM_MAX_TOKENS,
            temperature=0.2,  # Lower temperature for factual summary
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"


def explain_reading_order(reading_order: list[str]) -> str:
    """
    Asks NIM to explain why the given reading order is logical.

    Args:
        reading_order: List of file paths in topological order.
    Returns:
        A text explanation of the reading path.
    """
    if not reading_order:
        return "No files to explain."

    order_str = "\n".join(
        [f"{i+1}. {os.path.basename(f)}" for i, f in enumerate(reading_order)]
    )

    prompt = f"""
You are a technical mentor. I have calculated a topological reading order for a Python codebase.
The order is designed so that dependencies are read before the modules that use them.

Please explain to a new developer why this sequence is a good path to follow. 
Highlight the "Building Blocks" vs the "Features."

READING ORDER:
{order_str}

EXPLANATION:
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

    Args:
        query: User's question about the code.
        graph_data: Dictionary containing 'file_graph' and 'call_graph'.
    Returns:
        AI-generated answer based on local context.
    """
    file_graph = graph_data["file_graph"]
    keywords = query.lower().split()

    # 1. Search graph for relevant nodes
    relevant_context = []
    for node, data in file_graph.nodes(data=True):
        # Match against filename, docstring, or function names
        search_text = (
            f"{data.get('label', '')} {data.get('docstring', '')} "
            f"{' '.join([f['name'] for f in data.get('functions', [])])}"
        ).lower()

        if any(word in search_text for word in keywords if len(word) > 3):
            ctx = f"--- File: {data.get('label')} ---\n"
            ctx += f"Path: {node}\n"
            ctx += f"Docstring: {data.get('docstring') or 'N/A'}\n"
            ctx += f"Functions: {', '.join([f['name'] for f in data.get('functions', [])])}\n"
            relevant_context.append(ctx)

    # Limit context to top 5 matches to stay within token limits
    context_str = "\n".join(relevant_context[:5])

    if not context_str:
        context_str = "No specific files matched the keywords in your query."

    # 2. Construct the prompt
    prompt = f"""
You are a helpful assistant analyzing a Python codebase.
The user has a specific question. Use the provided file metadata to answer it.
If the answer isn't in the context, say you don't know based on the current analysis.

USER QUERY: {query}

RELEVANT CODE CONTEXT:
{context_str}

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
