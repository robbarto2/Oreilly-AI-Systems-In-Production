# Section 4: Agent Frameworks in Production - Demo Script

**Duration:** 25 minutes
**Format:** Live coding with explanation
**Instructor:** Rob Barton

---

## 🎯 Learning Objectives

By the end of this section, students will understand:
1. The difference between prototyping and production-ready agents
2. Why LangChain is great for prototyping but limited for production
3. How LangGraph provides explicit control, observability, and testability
4. Key production concerns: error handling, cost tracking, and graceful degradation

---

## 📋 Pre-Demo Checklist

### Before the session starts:
- [ ] Ollama is running (`ollama list` should show models)
- [ ] Required models are pulled:
  - `ollama pull llama3`
  - `ollama pull mxbai-embed-large`
- [ ] Terminal window is ready with proper font size for screen sharing
- [ ] Navigate to: `Section 4 - Agentic Frameworks/`
- [ ] Test run: `python agent_production_demo.py` (verify it works)
- [ ] Have code editor open with `agent_production_demo.py`
- [ ] Optional: Have the Jupyter notebook open in another tab

### Environment Setup:
```bash
cd "Section 4 - Agentic Frameworks"
source ../.venv/bin/activate  # or your venv path
```

---

## 🎬 Demo Script (25 minutes)

### **Part 1: Introduction & Context (3 minutes)**

#### What to say:
> "In Section 2, we looked at local model serving with Ollama. Now we're going to talk about something that changes dramatically when you move from development to production: **agent-based systems**.
>
> When you're prototyping an agent, you want speed. You want to quickly wire up tools, test ideas, and iterate. But in production, you need:
> - **Observability**: What is the agent doing and why?
> - **Error handling**: What happens when a tool fails?
> - **Cost control**: Can we avoid expensive API calls?
> - **Testability**: Can we unit test individual components?
>
> Today, we'll compare two approaches: **LangChain** for prototyping and **LangGraph** for production."

#### Show on screen:
```bash
ls -la
# Point out the files:
# - agent_production_demo.py (what we'll run)
# - climate.txt (our local knowledge base)
# - agent_production_demo.ipynb (for students to experiment later)
```

---

### **Part 2: The Scenario (2 minutes)**

#### What to say:
> "Here's our scenario: We're building a research agent that answers questions about climate change.
>
> **The smart production approach:**
> 1. First, check our local documents (fast, cheap, private)
> 2. If nothing is found, fall back to web search (slower, costs money)
> 3. Handle failures gracefully
>
> This is a common pattern in production: **optimize for cost and latency** by trying cheaper sources first."

#### Show the architecture:
Draw or show on screen:
```
User Question
      ↓
  [Router]
      ↓
 Try Local RAG (fast, cheap)
      ↓
   Success? → Answer
      ↓ No
 Try Web Search (slow, costs $)
      ↓
   Success? → Answer
      ↓ No
  Error Handler (graceful degradation)
```

---

### **Part 3: LangChain Agent Demo (6 minutes)**

#### What to say:
> "Let's start with LangChain. This is what most people use when prototyping. It's quick to set up, but has limitations for production."

#### Open code editor and show:
```python
# Scroll to demo_langchain_agent function (line ~150)
```

#### Key points to highlight:
1. **Quick setup** - Just define tools and initialize agent
2. **Black box** - Agent decides which tool to use (we don't control it)
3. **Limited error handling** - What if the web API is down?

#### Run the demo:
```bash
python agent_production_demo.py 2>&1 | grep -A 50 "PART 1: LangChain"
```

#### Point out:
- ✅ "Notice it worked... eventually"
- ⚠️ "But look at the metrics: 2-3 tool calls"
- ⚠️ "We don't know exactly which tools were called or why"
- ⚠️ "The agent hit its iteration limit - not ideal for production"

#### What to say:
> "This is fine for prototyping, but imagine debugging this in production at 2 AM. You have no visibility into **why** the agent made certain decisions."

---

### **Part 4: LangGraph Agent Demo (10 minutes)**

#### What to say:
> "Now let's look at LangGraph. Yes, it's more verbose. But in production, **explicit is better than implicit**."

#### Open code editor and show the structure:

**1. State Definition (30 seconds)**
```python
# Show class AgentState (line ~200)
```
> "We explicitly define what data flows through our system. This makes it testable and debuggable."

**2. Node Functions (2 minutes)**
```python
# Show route_question, local_search_node, web_search_node (lines ~210-280)
```

#### Key points:
- **route_question**: "We decide the routing logic - always try local first"
- **local_search_node**: "See the error handling? If local fails, we explicitly route to web"
- **web_search_node**: "And if web fails, we route to error handler"
- **synthesize_answer**: "We control how results are combined"

> "Each node has **one job**. This is testable. You can unit test each node independently."

**3. Graph Construction (2 minutes)**
```python
# Show the graph building (lines ~350-420)
```

#### What to say:
> "Here's where LangGraph shines. We explicitly build the flow:
> - Router → Local
> - Local → (success? Synthesize : Web)
> - Web → (success? Synthesize : Error Handler)
>
> This isn't black magic. This is a **state machine** you can reason about, test, and debug."

**4. Run the LangGraph version (2 minutes)**
```bash
# Already ran - show the output
```

#### Point out in the output:
- ✅ "See the decision log? 'Router → Local → Synthesize'"
- ✅ "Only **1 tool call** vs 2-3 with LangChain"
- ✅ "Faster: 0.86s vs 6.16s"
- ✅ "Clear visibility into what happened"

#### What to say:
> "In production, this observability is **critical**. When something goes wrong, you need to know:
> - Which node failed?
> - What was the state at that time?
> - What decision was made and why?"

**5. Show error handling (3 minutes)**

#### What to say:
> "Now let's see what happens when things go wrong. I'm going to simulate a web API failure."

#### Show the code:
```python
# Show simulate_failure parameter in demo
# Show the failure simulation section (line ~475)
```

#### Point out in the output:
- ⚠️ LangChain: "Notice how opaque the error handling is"
- ✅ LangGraph: "But LangGraph shows exactly what failed and why"

> "LangGraph didn't even try the web because local search succeeded. But if it had tried and failed, we'd see:
> - Clear error message
> - Fallback to error handler
> - Graceful degradation with user-friendly message"

---

### **Part 5: Production Implications (3 minutes)**

#### What to say:
> "Let me summarize the key production differences:"

#### Show comparison table (prepare slide or screen):

| Aspect | LangChain | LangGraph |
|--------|-----------|-----------|
| **Setup Time** | ⚡ Fast | 📝 More verbose |
| **Control** | ❌ Limited | ✅ Explicit |
| **Debugging** | 😕 Hard | ✅ Easy |
| **Error Handling** | ❌ Opaque | ✅ Explicit |
| **Testability** | ❌ E2E only | ✅ Unit + Integration |
| **Observability** | ❌ Limited | ✅ Full visibility |
| **Cost Optimization** | ❌ Hard | ✅ Easy |
| **Production Ready** | ⚠️ Risky | ✅ Yes |

#### Key takeaways to emphasize:

**1. Cost Control**
> "LangGraph lets you optimize routing. We try local (free) before web (costs money). With LangChain, you're at the mercy of the agent's decisions."

**2. Observability**
> "In production, you need logs, metrics, and traces. LangGraph gives you clear decision paths. LangChain is a black box."

**3. Error Handling**
> "When your RAG system goes down at 3 AM, you need graceful degradation and clear error messages, not mysterious agent failures."

**4. Testability**
> "Each LangGraph node is a pure function you can unit test. With LangChain agents, you're mostly limited to end-to-end tests."

---

### **Part 6: When to Use What (1 minute)**

#### What to say:
> "So when should you use each?
>
> **Use LangChain when:**
> - Rapid prototyping
> - POCs and demos
> - Simple, non-critical applications
> - You're exploring ideas quickly
>
> **Use LangGraph when:**
> - Production deployments
> - Critical business logic
> - You need observability and debugging
> - Cost control matters
> - You need to test components independently
>
> **For multi-agent systems:**
> - Consider frameworks like **CrewAI** (which we'll touch on later)"

---

## 🤔 Common Questions & Answers

### Q: "Isn't LangGraph just more complicated?"
**A:** "Yes, it's more verbose. But in production, **explicit beats implicit**. The extra lines of code pay dividends when you're debugging a production incident. Would you rather have 50 lines of clear, testable code, or 20 lines of magic that breaks mysteriously?"

### Q: "Can I use LangChain in production?"
**A:** "You can, but you'll need to add custom logging, error handling, and monitoring around it. LangGraph gives you these patterns out of the box. Many teams start with LangChain and migrate to LangGraph when they hit production issues."

### Q: "What about other frameworks like CrewAI or AutoGen?"
**A:** "Great question. CrewAI is excellent for **multi-agent** systems where you have specialized agents collaborating. AutoGen is similar. But for single-agent production deployments with multiple tools, LangGraph's explicit graph model is hard to beat."

### Q: "How do I add monitoring to LangGraph?"
**A:** "Each node is a function. You can add decorators for timing, logging, metrics. The decision log we showed is the foundation for observability. In Section 7, we'll show how to integrate with **LangSmith** for full agent monitoring."

### Q: "What about LangChain's newer features like LCEL?"
**A:** "LangChain Expression Language (LCEL) is better than the old agents, but LangGraph is specifically designed for production agent workflows. It's what LangChain recommends for production use cases."

### Q: "Can LangGraph handle streaming?"
**A:** "Yes! Each node can stream responses. You have full control over streaming behavior at each step."

---

## 🛠️ Troubleshooting

### Issue: Ollama not responding
**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve &

# Verify models
ollama pull llama3
ollama pull mxbai-embed-large
```

### Issue: "Module not found" errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r ../requirements.txt

# Or specific packages
pip install langchain langchain-community langgraph chromadb wikipedia
```

### Issue: Demo runs too slow
**Solution:**
- Use smaller model: Change `llama3` to `llama3:8b`
- Reduce chunk size in RAG setup
- Skip the failure simulation demo if time is short

### Issue: Chroma DB errors
**Solution:**
```bash
# Clear the vector store
rm -rf demo_chroma lc_chroma

# Demo will recreate it on next run
```

---

## 📝 Post-Demo Activities

### For students to try:
1. Run the Jupyter notebook interactively
2. Modify the routing logic (e.g., try web first for certain question types)
3. Add a third tool (e.g., database search)
4. Add retry logic with exponential backoff
5. Implement cost tracking (count tokens used)

### Code to share:
```bash
# Students can clone and run
cd "Section 4 - Agentic Frameworks"
python agent_production_demo.py

# Or explore interactively
jupyter notebook agent_production_demo.ipynb
```

---

## 🔗 Connection to Other Sections

**Link back to Section 2:**
> "Remember how we set up Ollama for local serving? That's what powers our local RAG system here."

**Link forward to Section 5:**
> "Next, we'll look at cloud deployment with AWS Bedrock. The same production principles apply - you need observability, error handling, and cost control."

**Link forward to Section 6:**
> "And in Section 6, we'll talk about security - because agents that call external tools are a security risk if not properly controlled."

**Link forward to Section 7:**
> "In Section 7, we'll show you LangSmith for monitoring these agents in production. You'll see how to track every decision, measure performance, and debug failures."

---

## 📊 Timing Breakdown

- **0:00 - 0:03** - Introduction & Context
- **0:03 - 0:05** - Scenario Overview
- **0:05 - 0:11** - LangChain Demo
- **0:11 - 0:21** - LangGraph Demo (main content)
- **0:21 - 0:24** - Production Implications
- **0:24 - 0:25** - When to Use What
- **Buffer:** 5 minutes for questions

---

## 🎯 Key Messages to Drive Home

1. **"Explicit is better than implicit in production"**
2. **"Observability is not optional for production agents"**
3. **"Cost optimization starts with controlling tool usage"**
4. **"Test individual components, not just end-to-end"**
5. **"Error handling should be explicit, not hope-based"**

---

## 📚 Additional Resources for Students

- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- Migration Guide: https://python.langchain.com/docs/how_to/migrate_agent/
- Our GitHub Repo: https://github.com/robbarto2/Oreilly-AI-Systems-In-Production

---

**Good luck with the demo! Remember: Show, don't just tell. The live comparison is powerful.**
