# O'Reilly AI Systems in Production

Training materials for O'Reilly's AI Systems in Production course, covering local model serving, agentic frameworks, and cloud-based AI models.

## Structure

- **Section 2 - Local Model Serving**: Examples using Ollama for local LLM deployment
- **Section 4 - Agentic Frameworks**: LangChain and LangGraph agent implementations
- **Section 5 - AI Models in the Cloud**: AWS Bedrock integrations with Streamlit UIs

## Setup

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Requirements

- Python 3.10+
- Ollama (for local model examples)
- AWS credentials configured (for Bedrock examples)

## Usage

### Running Jupyter Notebooks

```bash
jupyter notebook
```

### Running Streamlit Apps

```bash
streamlit run "Section 5 - AI Models in the Cloud/Bedrock Chatbot.py"
```

### Running Python Scripts

```bash
python "Section 2 - Local Model Serving/Ollama-API.py"
```
