# 🚀 AI Systems in Production

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Course Duration](https://img.shields.io/badge/duration-3%20hours-orange)
![Status](https://img.shields.io/badge/status-active-success)

*A comprehensive 3-hour live training session developed in partnership with Pearson O'Reilly*

</div>


## 👋 Welcome

Welcome to the official repository for "AI Systems in Production" — your guide to deploying, securing, and operating LLM and agent-based systems in production environments. This course teaches you the practical skills needed to move AI systems from prototype to production, covering infrastructure, deployment patterns, security, and observability.

## 🎯 What You'll Learn

This hands-on course teaches you how to deploy, secure, and operate LLM and agent-based systems in production. You'll understand where deployment and operations fit in the LLM lifecycle and be equipped to handle common challenges when moving from prototype to production.

### 📚 Course Curriculum

#### Section 1: Welcome and Overview (10 min)
- **Topics:**
  - Course objectives and learning outcomes
  - Where deployment and operations fit in the LLM and agent lifecycle
  - Common challenges when moving from prototype to production
  - What you will be able to deploy, secure, and operate by the end of the course

#### Section 2: Local Model Management and Inference Serving (45 min)
- **Instructor:** Rob Barton
- **Code:** [`Section 2 - Local Model Serving/`](./Section%202%20-%20Local%20Model%20Serving/)
- **Topics:**
  - Why run models locally: cost, latency, control, and privacy considerations
  - Managing models with Ollama: setup, versioning, and lifecycle management
  - Exposing local models as inference endpoints
  - Comparing Ollama and vLLM: operational trade-offs and use cases
  - When local, hybrid, or cloud-first deployments make sense
- **Files:**
  - [`Ollama-API.py`](./Section%202%20-%20Local%20Model%20Serving/Ollama-API.py) - REST API integration with Ollama
  - [`Ollama-python-library.py`](./Section%202%20-%20Local%20Model%20Serving/Ollama-python-library.py) - Python library usage examples

#### Section 3: Deploying Production RAG Systems (55 min)
- **Instructor:** Jerome Henry
- **Topics:**
  - RAG as a production architecture pattern
  - Data ingestion, chunking, and embedding pipelines at scale
  - Vector store selection and deployment considerations
  - Hybrid retrieval approaches: dense, sparse, and reranking
  - Query orchestration and response synthesis
  - Evaluating RAG quality, relevance, and cost
  - Scaling RAG systems under real-world load

#### Section 4: Agent Frameworks in Production Environments (25 min)
- **Instructor:** Rob Barton
- **Code:** [`Section 4 - Agentic Frameworks/`](./Section%204%20-%20Agentic%20Frameworks/)
- **Topics:**
  - What changes when agents move from development to production
  - Understanding CrewAI, LangChain, and others
  - Operational implications of agent-based architectures
  - Scaling and operating agent-based systems reliably
- **Files:**
  - [`LangChain_Agent.ipynb`](./Section%204%20-%20Agentic%20Frameworks/LangChain_Agent.ipynb) - LangChain agent implementations with RAG and tool usage
  - [`Agent_demo.ipynb`](./Section%204%20-%20Agentic%20Frameworks/Agent_demo.ipynb) - Agent demonstration examples

#### Section 5: Cloud-Based Deployment of LLMs with AWS Bedrock (30 min)
- **Instructor:** Rob Barton
- **Code:** [`Section 5 - AI Models in the Cloud/`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/)
- **Topics:**
  - Cloud deployment models for LLM systems
  - Overview of managed LLM platforms and when to use them
  - AWS Bedrock architecture, model offerings, and configuration
  - Integrating Bedrock into existing application stacks
  - Cost, latency, and governance considerations for cloud-based LLMs
- **Files:**
  - [`list bedrock models.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/list%20bedrock%20models.py) - List available Bedrock models
  - [`Invoke bedrock model.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Invoke%20bedrock%20model.py) - Basic model invocation
  - [`Bedrock Chatbot.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Bedrock%20Chatbot.py) - Streamlit chatbot using Mistral 7B
  - [`Anthropic Chatbot Guardrails.py`](./Section%205%20-%20AI%20Models%20in%20the%20Cloud/Anthropic%20Chatbot%20Guardrails.py) - Claude Haiku chatbot with guardrails

#### Section 6: Securing Agentic AI Systems (30 min)
- **Instructor:** Jerome Henry
- **Topics:**
  - Threat models specific to LLM and agent-based systems
  - Prompt injection, tool misuse, and indirect prompt attacks
  - Guardrails, policy enforcement, and runtime controls
  - Data privacy, access control, and secrets management
  - Audit logging, governance, and compliance considerations

#### Section 7: Monitoring and Observability of AI Systems in Production (25 min)
- **Instructor:** Jerome Henry
- **Topics:**
  - Why traditional monitoring is insufficient for LLMs and agents
  - Core operational metrics: latency, cost, throughput, and reliability
  - Observing model behavior and agent decision paths
  - Using LangSmith to monitor the Agentic AI system (with a live demo)

## 📁 Repository Structure

```
├── Section 2 - Local Model Serving/          # Ollama API and Python library examples
├── Section 4 - Agentic Frameworks/           # LangChain and LangGraph agent implementations
├── Section 5 - AI Models in the Cloud/       # AWS Bedrock examples with Streamlit UIs
├── .gitignore                                # Git ignore patterns
├── pyproject.toml                            # uv/pip project configuration
├── requirements.txt                          # Python dependencies
└── README.md                                 # This file
```

Each section includes:
- 📓 Jupyter Notebooks (`.ipynb`) or Python scripts (`.py`)
- 📊 Sample data files and knowledge sources (where applicable)
- 💻 Runnable examples for local testing and deployment

## ⚙️ Prerequisites

Before you begin, ensure you have:

- 🐍 Python 3.10 or higher
- 🦙 Ollama installed (for local model examples)
- ☁️ AWS credentials configured with Bedrock access
- 📚 Basic understanding of LLMs and Python
- 🔧 Git installed

## 🚀 Getting Started

### Option 1: Using uv (recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/robbarto2/Oreilly-AI-Systems-In-Production.git
   cd Oreilly-AI-Systems-In-Production
   ```

2. **Install uv if you haven't already:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create virtual environment and install dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

### Option 2: Using pip

1. **Clone the repository:**
   ```bash
   git clone https://github.com/robbarto2/Oreilly-AI-Systems-In-Production.git
   cd Oreilly-AI-Systems-In-Production
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start learning!** Run the Jupyter notebooks, Streamlit apps, or Python scripts for each section.

## 💡 Usage Examples

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

## 🛠️ Key Technologies

- **Local Serving**: Ollama, vLLM
- **Agent Frameworks**: LangChain, LangGraph, CrewAI
- **Cloud Platforms**: AWS Bedrock
- **Vector Stores**: ChromaDB
- **UI Framework**: Streamlit
- **Monitoring**: LangSmith

## 👥 Meet the Instructors

<div align="center">

### Rob Barton
**Distinguished Engineer, AI & Networking**

### Jerome Henry
**Distinguished Engineer, Wireless & AI**

</div>

---

<div align="center">

Made with ❤️ by Rob Barton and Jerome Henry

</div>
