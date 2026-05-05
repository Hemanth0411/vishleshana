# 🧠 AI Reasoning Logic (NVIDIA NIM)

This module acts as the "Brain" of Vishleshana, translating raw graph data into human-readable insights using the `openai` SDK connected to NVIDIA's optimized NIM infrastructure.

## 1. `_get_client()`
- **Purpose**: Establishes a secure connection to the NIM endpoint.
- **Logic**: It initializes a standard OpenAI client but points the `base_url` to NVIDIA's hosted models. This allows us to use state-of-the-art LLMs (like Llama-3) while keeping the code compatible with standard AI tools.

## 2. `generate_summary(graph_data)`
- **Purpose**: Provides a high-level architectural overview.
- **How it works**: It takes the metadata from every node (filename, docstring, functions) and compresses it into a structured text prompt.
- **Prompt Engineering**: It instructs the AI to act as a "Software Architect," focusing on the project's purpose rather than line-by-line details.

## 3. `explain_reading_order(reading_order)`
- **Purpose**: Provides a mentorship-style guide for new developers.
- **Logic**: It takes the mathematical topological sort and asks the AI to create a "narrative" explaining why you should read the foundation files (utils, config) before the feature files (main, api).

## 4. `answer_query(query, graph_data)`
- **Purpose**: Targeted Q&A about specific features.
- **How it works**:
    1. **Keyword Search**: It scans the graph for files that contain keywords from the user's query.
    2. **Context Retrieval**: It selects the top 5 most relevant file summaries.
    3. **Grounding**: It sends only that specific context to the AI to prevent "hallucinations" (the AI making things up).
- **Pros**: Extremely fast and token-efficient. It doesn't need to read the whole project to answer a question about one specific function.
