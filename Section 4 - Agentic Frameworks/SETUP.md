# Section 4 Setup Guide

## Quick Fix for Missing Dependencies

If you see `ModuleNotFoundError: No module named 'langchain_community'`, run:

```bash
# Navigate to project root
cd "/Users/robbarto/Dropbox/Programming Projects/Pearson Live Training Repos/Oreilly-AI-Systems-In-Production"

# Install all dependencies
pip install -r requirements.txt
```

## Recommended: Use Virtual Environment

### Option 1: Using venv (built-in)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using uv (faster)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Verify Installation

```bash
# Test imports
python3 -c "
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langgraph.graph import StateGraph
print('✅ All dependencies installed correctly!')
"
```

## Required Ollama Models

Make sure Ollama is running and has the required models:

```bash
# Check Ollama is running
ollama list

# Pull required models
ollama pull llama3
ollama pull mxbai-embed-large

# Verify
ollama list | grep -E "llama3|mxbai"
```

## Run the Demo

⚠️ **CRITICAL:** The demo must be run from within the `Section 4 - Agentic Frameworks/` directory!

Once dependencies are installed:

```bash
# Make sure you're in the right directory
cd "Section 4 - Agentic Frameworks"

# Verify you're in the right place (should show climate.txt)
ls climate.txt

# Run the demo
python agent_production_demo.py
```

**Common mistake:** Running from the project root will fail with `FileNotFoundError: climate.txt`

## Troubleshooting

### Issue: `command not found: ollama`
**Solution:** Install Ollama from https://ollama.ai

### Issue: Still getting import errors after pip install
**Solution:** Make sure you're in the correct Python environment
```bash
# Check which Python
which python3
python3 --version

# Should be in your venv if activated
# If not, activate: source .venv/bin/activate
```

### Issue: Chroma DB errors
**Solution:** Clear the vector store
```bash
rm -rf demo_chroma
# Demo will recreate it
```

### Issue: "Connection refused" from Ollama
**Solution:** Start Ollama
```bash
# On macOS (if installed via brew)
brew services start ollama

# Or manually
ollama serve
```

## Minimal Install (Just for Section 4)

If you only want to run Section 4:

```bash
pip install langchain>=0.3.0 \
            langchain-community>=0.3.0 \
            langchain-core>=0.3.0 \
            langgraph>=0.2.0 \
            chromadb>=0.4.22 \
            wikipedia>=1.4.0
```
