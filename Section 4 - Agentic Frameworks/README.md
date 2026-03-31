# Section 4: Agent Frameworks in Production Environments

This section demonstrates the operational differences between LangChain and LangGraph for production agent deployments.

## 🎯 Learning Objectives

- Understand what changes when agents move from development to production
- Compare LangChain (prototyping) vs LangGraph (production)
- Learn production patterns: error handling, observability, cost optimization
- See explicit control flow vs black-box agent behavior

## 📁 Files in This Section

### Demo Files
- **`agent_production_demo.py`** - Complete Python demo script (runs standalone)
- **`agent_production_demo.ipynb`** - Interactive Jupyter notebook version
- **`DEMO_SCRIPT.md`** - Instructor guide with timing, talking points, and Q&A

### Data Files
- **`climate.txt`** - Sample knowledge base for RAG system
- **`Noclimate.txt`** - Alternative test document

## 🚀 Quick Start

### Prerequisites
Make sure Ollama is running with required models:
```bash
ollama pull llama3
ollama pull mxbai-embed-large
```

### Run the Demo

**Option 1: Python Script (Recommended for instructors)**
```bash
cd "Section 4 - Agentic Frameworks"
python agent_production_demo.py
```

**Option 2: Jupyter Notebook (For students)**
```bash
jupyter notebook agent_production_demo.ipynb
```

## 📊 What the Demo Shows

### Part 1: LangChain Agent
- ✅ Quick setup with minimal code
- ❌ Limited control over tool selection
- ❌ Opaque decision-making
- ❌ Hard to debug
- ⚠️ May hit iteration limits

**Result:** Works for prototyping, risky for production

### Part 2: LangGraph Agent
- ✅ Explicit control flow (state machine)
- ✅ Observable decision paths
- ✅ Graceful error handling
- ✅ Cost-optimized routing (local before web)
- ✅ Unit testable components
- ✅ Clear logs and metrics

**Result:** Production-ready with full observability

## 🔍 Key Concepts Demonstrated

### 1. Observability
```
LangChain: Black box agent behavior
LangGraph: Clear decision log showing which nodes were executed
```

### 2. Error Handling
```
LangChain: Opaque failures, limited control
LangGraph: Explicit error handling with graceful degradation
```

### 3. Cost Optimization
```
LangChain: Agent decides tool order
LangGraph: You control routing (try cheap tools first)
```

### 4. Testability
```
LangChain: End-to-end tests only
LangGraph: Unit test each node independently
```

## 📈 Performance Comparison

From actual test run:

| Metric | LangChain | LangGraph |
|--------|-----------|-----------|
| Tool Calls | 2-3 | 1 |
| Time | ~6 seconds | ~0.9 seconds |
| Errors | Opaque | Explicit logging |
| Predictability | Low | High |

## 🎓 For Instructors

See **`DEMO_SCRIPT.md`** for:
- Complete 25-minute demo script with timing
- Key talking points
- Common questions and answers
- Troubleshooting tips
- Connection to other sections

## 💡 For Students

### Try These Extensions:
1. Add a third tool (e.g., database search)
2. Implement retry logic with exponential backoff
3. Add token counting for cost tracking
4. Create a health check endpoint
5. Add circuit breaker pattern for failing tools

### Key Takeaways:
- **Explicit is better than implicit** in production
- **Observability is not optional** for agents
- **Test components individually**, not just end-to-end
- **Cost optimization** starts with controlling tool routing
- Use LangChain for prototyping, LangGraph for production

## 🔗 Related Sections

- **Section 2:** Local Model Serving (powers the RAG system)
- **Section 5:** Cloud Deployment (same principles apply)
- **Section 6:** Security (agents need security controls)
- **Section 7:** Monitoring with LangSmith (observability in depth)

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Migration Guide: LangChain → LangGraph](https://python.langchain.com/docs/how_to/migrate_agent/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)

---

**Duration:** 25 minutes | **Format:** Live demo with code walkthrough
