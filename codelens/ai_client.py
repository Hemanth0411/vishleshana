"""
ai_client.py — AI reasoning for CodeLens via NVIDIA NIM.

Uses the OpenAI-compatible API to interact with hosted LLMs.
Handles prompt construction and context-aware responses.

Dependencies: openai
"""

from openai import OpenAI
from codelens import config

def _get_client() -> OpenAI:
    """
    Initializes and returns an OpenAI-compatible client for NVIDIA NIM.
    """
    return OpenAI(
        base_url=config.NIM_BASE_URL,
        api_key=config.NIM_API_KEY
    )

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
            max_tokens=5
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
            messages=[{"role": "system", "content": "You are a helpful software architect."},
                      {"role": "user", "content": prompt}],
            max_tokens=config.NIM_MAX_TOKENS,
            temperature=0.2 # Lower temperature for factual summary
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"
