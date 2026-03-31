#!/bin/bash
# Wrapper script to run the demo with warnings filtered out

# Run the demo and filter out LangChain deprecation warnings from stderr
/Users/robbarto/.pyenv/versions/3.10.13/bin/python agent_production_demo.py 2>&1 | \
    grep -v "LangChainDeprecationWarning" | \
    grep -v "deprecated" | \
    grep -v "langchain-ollama" | \
    grep -v "langchain_ollama" | \
    grep -v "embeddings = OllamaEmbeddings" | \
    grep -v "llm = Ollama" | \
    grep -v "agent = initialize_agent" | \
    grep -v "\.py:[0-9]*:"
