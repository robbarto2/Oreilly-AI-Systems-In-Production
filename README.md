# O'Reilly AI Systems in Production

Training materials for O'Reilly's AI Systems in Production course, covering local model serving, agentic frameworks, cloud-based AI models, security, and production operations.

## Course Overview

This course teaches you how to deploy, secure, and operate LLM and agent-based systems in production environments. By the end, you'll understand where deployment and operations fit in the LLM lifecycle and be equipped to handle common challenges when moving from prototype to production.

## Course Outline

### Segment 1: Welcome and Overview (10 min)
- Course objectives and learning outcomes
- Where deployment and operations fit in the LLM and agent lifecycle
- Common challenges when moving from prototype to production
- What you will be able to deploy, secure, and operate by the end of the course

### Segment 2: Local Model Management and Inference Serving (45 min)
**Code:** [`Section 2 - Local Model Serving/`](./Section%202%20-%20Local%20Model%20Serving/)
- Why run models locally: cost, latency, control, and privacy considerations
- Managing models with Ollama: setup, versioning, and lifecycle management
- Exposing local models as inference endpoints
- Comparing Ollama and vLLM: operational trade-offs and use cases
- When local, hybrid, or cloud-first deployments make sense

**Files:**
- [`Ollama-API.py`](./Section%202%20-%20Local%20Model%20Serving/Ollama-API.py) - REST API integration with Ollama
- [`Ollama-python-library.py`](./Section%202%20-%20Local%20Model%20Serving/Ollama-python-library.py) - Python library usage examples

### Segment 3: Deploying Production RAG Systems (55 min)
- RAG as a production architecture pattern
- Data ingestion, chunking, and embedding pipelines at scale
- Vector store selection and deployment considerations
- Hybrid retrieval approaches: dense, sparse, and reranking
- Query orchestration and response synthesis
- Evaluating RAG quality, relevance, and cost
- Scaling RAG systems under real-world load

### Segment 4: Agent Frameworks in Production Environments (25 min)
**Code:** [`Section 4 - Agentic Frameworks/`](./Section%204%20-%20Agentic%20Frameworks/)
- What changes when agents move from development to production
- Understanding CrewAI, LangChain, and others
- Operational implications of agent-based architectures
- Scaling and operating agent-based systems reliably

**Files:**
- [`LangChain_Agent.ipynb`](./Section%204%20-%20Agentic%20Frameworks/LangChain_Agent.ipynb) - LangChain agent implementations with RAG and tool usage
- [`Agent_demo.ipynb`](./Section%204%20-%20Agentic%20Frameworks/Agent_demo.ipynb) - Agent demonstration examples

### Segment 5: Cloud-Based Deployment of LLMs with AWS Bedrock (30 min)
**Code:** [`Section 5 - AI Models in the Cloud/`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/)
- Cloud deployment models for LLM systems
- Overview of managed LLM platforms and when to use them
- AWS Bedrock architecture, model offerings, and configuration
- Integrating Bedrock into existing application stacks
- Cost, latency, and governance considerations for cloud-based LLMs

**Files:**
- [`list bedrock models.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/list%20bedrock%20models.py) - List available Bedrock models
- [`Invoke bedrock model.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Invoke%20bedrock%20model.py) - Basic model invocation
- [`Bedrock Chatbot.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Bedrock%20Chatbot.py) - Streamlit chatbot using Mistral 7B
- [`Anthropic Chatbot Guardrails.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Anthropic%20Chatbot%20Guardrails.py) - Claude Haiku chatbot with guardrails

### Segment 6: Securing Agentic AI Systems (30 min)
- Threat models specific to LLM and agent-based systems
- Prompt injection, tool misuse, and indirect prompt attacks
- Guardrails, policy enforcement, and runtime controls
- Data privacy, access control, and secrets management
- Audit logging, governance, and compliance considerations

### Segment 7: Monitoring and Observability of AI Systems in Production (25 min)
- Why traditional monitoring is insufficient for LLMs and agents
- Core operational metrics: latency, cost, throughput, and reliability
- Observing model behavior and agent decision paths
- Using LangSmith to monitor the Agentic AI system (with a live demo)

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

## Prerequisites

- Python 3.10+
- Ollama (for local model examples in Segment 2 & 4)
- AWS credentials configured with Bedrock access (for Segment 5)
- Optional: LangSmith account for monitoring (Segment 7)

## Usage

### Running Jupyter Notebooks

```bash
jupyter notebook
# Navigate to Section 4 - Agentic Frameworks/
```

### Running Streamlit Apps

```bash
# Bedrock Chatbot (Mistral 7B)
streamlit run "Section 5 - AI Models in the Cloud/Bedrock Chatbot.py"

# Claude Haiku Chatbot with Guardrails
streamlit run "Section 5 - AI Models in the Cloud/Anthropic Chatbot Guardrails.py"
```

### Running Python Scripts

```bash
# Ollama examples
python "Section 2 - Local Model Serving/Ollama-API.py"
python "Section 2 - Local Model Serving/Ollama-python-library.py"

# AWS Bedrock examples
python "Section 5 - AI Models in the Cloud/list bedrock models.py"
python "Section 5 - AI Models in the Cloud/Invoke bedrock model.py"
```

## Key Technologies

- **Local Serving**: Ollama, vLLM
- **Agent Frameworks**: LangChain, LangGraph, CrewAI
- **Cloud Platforms**: AWS Bedrock
- **Vector Stores**: ChromaDB
- **UI Framework**: Streamlit
- **Monitoring**: LangSmith

## Course Structure

- **Total Duration**: ~3 hours
- **Format**: Hands-on with live demos
- **Instructors**: Rob & Jerome
