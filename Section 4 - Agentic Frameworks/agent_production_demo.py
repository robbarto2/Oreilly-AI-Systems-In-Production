#!/usr/bin/env python3
"""
Production-Ready Agent Demo: LangChain vs LangGraph

Shows the difference in observability and debuggability.
Both agents use the LLM to decide which tools to call.

Usage:
    python agent_production_demo.py
"""

import os
import time
import warnings
from pathlib import Path
from typing import TypedDict, Annotated
from datetime import datetime

warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

_SCRIPT_DIR = Path(__file__).resolve().parent

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️  Wikipedia not installed. Install with: pip install wikipedia")


# ==================== SHARED SETUP ====================

def setup_local_search():
    print("📚 Setting up local RAG system...")

    loader = TextLoader(str(_SCRIPT_DIR / "climate.txt"))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    chroma_dir = str(_SCRIPT_DIR / "demo_chroma")
    if (_SCRIPT_DIR / "demo_chroma" / "chroma.sqlite3").exists():
        print("   (loading existing vector store...)")
        vectorstore = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)
    else:
        print("   (building vector store — takes ~30s the first time...)")
        vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=chroma_dir)

    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    llm = Ollama(model="llama3")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True
    )

    print("✅ RAG system ready\n")
    return qa_chain


def run_local_search(query: str, qa_chain) -> str:
    try:
        result = qa_chain.invoke({"query": query})
        return result["result"]
    except Exception as e:
        return f"❌ Local search failed: {str(e)}"


def run_web_search(query: str) -> str:
    if not WIKIPEDIA_AVAILABLE:
        return "❌ Wikipedia module not installed"
    try:
        results = wikipedia.search(query)
        if results:
            summary = wikipedia.summary(results[0], sentences=3)
            return f"📰 From Wikipedia ({results[0]}): {summary}"
        return "❌ No Wikipedia results found"
    except Exception as e:
        return f"❌ Web search failed: {str(e)}"


# ==================== PART 1: LANGCHAIN AGENT ====================

def demo_langchain_agent(qa_chain):
    print("=" * 60)
    print("PART 1: LangChain Agent")
    print("=" * 60)
    print("""
The LangChain agent uses a ReAct loop: the LLM decides which tool
to call, reads the result, and decides what to do next. It works —
but you're watching a stream of text, not structured state.

Notice:
  - You can't easily tell WHEN a decision was made
  - No way to pause and inspect mid-run
  - No way to redirect or interrupt the agent
  - If something goes wrong, good luck debugging it
""")

    # Counter to track agentic loops — each tool call is one loop iteration
    loop_counter = {"count": 0}

    def local_search_with_count(q):
        loop_counter["count"] += 1
        print(f"   🔧 [Loop #{loop_counter['count']}] LocalSearch")
        return run_local_search(q, qa_chain)

    def web_search_with_count(q):
        loop_counter["count"] += 1
        print(f"   🔧 [Loop #{loop_counter['count']}] WebSearch")
        return run_web_search(q)

    tools = [
        Tool(
            name="LocalSearch",
            func=local_search_with_count,
            description="Search local climate documents. Use for climate-related questions."
        ),
        Tool(
            name="WebSearch",
            func=web_search_with_count,
            description="Search Wikipedia for general information."
        )
    ]

    llm = Ollama(model="llama3")
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    question = "What are the main causes of climate change and what countries are the biggest emitters?"
    print(f"❓ Question: {question}")
    print("⏱️  Running...\n")

    start = time.time()
    try:
        result = agent.invoke({"input": question})
        elapsed = time.time() - start
        print(f"\n💬 Answer: {result['output']}\n")
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n❌ Failed after {elapsed:.2f}s: {e}\n")

    return {"loops": loop_counter["count"], "elapsed": elapsed}


# ==================== PART 2: LANGGRAPH AGENT ====================

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls_log: list[dict]
    loop_count: int


def make_langgraph_agent(qa_chain):
    llm = Ollama(model="llama3")

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        content = last.content if hasattr(last, "content") else ""
        if "Action:" in content and "Action Input:" in content:
            return "tools"
        return "end"

    def call_model(state: AgentState) -> AgentState:
        loop_num = state.get("loop_count", 0) + 1
        print(f"\n🧠 [LangGraph Loop #{loop_num}] LLM thinking...")

        system = """You are a research assistant. Use tools to answer the question.

Available tools:
- LocalSearch: Search local climate documents
- WebSearch: Search Wikipedia

Use this format:
Thought: <your reasoning>
Action: <LocalSearch or WebSearch>
Action Input: <the query>

When you have enough information, respond with:
Thought: I have enough information
Final Answer: <your answer>"""

        messages = state["messages"]
        conversation = "\n".join(
            f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
            for m in messages
        )

        response = llm.invoke(f"{system}\n\n{conversation}\nAssistant:")
        ai_msg = AIMessage(content=response)

        print(f"\n📋 [LangGraph] LLM decision:\n{response[:300]}{'...' if len(response) > 300 else ''}")

        return {
            "messages": [ai_msg],
            "tool_calls_log": state.get("tool_calls_log", []),
            "loop_count": loop_num
        }

    def call_tools(state: AgentState) -> AgentState:
        last = state["messages"][-1]
        content = last.content

        tool_name = None
        tool_input = None
        for line in content.split("\n"):
            if line.startswith("Action:"):
                tool_name = line.replace("Action:", "").strip()
            elif line.startswith("Action Input:"):
                tool_input = line.replace("Action Input:", "").strip()

        if not tool_name or not tool_input:
            return state

        print(f"\n🔧 [LangGraph] Executing: {tool_name}({tool_input[:60]})")

        if tool_name == "LocalSearch":
            result = run_local_search(tool_input, qa_chain)
        elif tool_name == "WebSearch":
            result = run_web_search(tool_input)
        else:
            result = f"❌ Unknown tool: {tool_name}"

        log_entry = {
            "tool": tool_name,
            "input": tool_input,
            "result_preview": result[:100],
            "timestamp": datetime.now().isoformat()
        }
        print(f"📄 [LangGraph] Result: {result[:150]}...")

        tool_msg = ToolMessage(content=f"Observation: {result}", tool_call_id="1")
        log = state.get("tool_calls_log", []) + [log_entry]

        return {
            "messages": [tool_msg],
            "tool_calls_log": log,
            "loop_count": state.get("loop_count", 0)
        }

    graph = StateGraph(AgentState)
    graph.add_node("model", call_model)
    graph.add_node("tools", call_tools)
    graph.set_entry_point("model")
    graph.add_conditional_edges("model", should_continue, {"tools": "tools", "end": END})
    graph.add_edge("tools", "model")

    return graph.compile()


def demo_langgraph_agent(qa_chain):
    print("=" * 60)
    print("PART 2: LangGraph Agent (Observable)")
    print("=" * 60)
    print("""
Same LLM, same tools, same question.

Key differences you'll see:
  ✅ Each loop is numbered — you can see exactly how many iterations ran
  ✅ LLM decision is printed as structured state before execution
  ✅ Full decision log at the end — every step, timestamped
  ✅ State is checkpointed — you could pause, resume, or branch
""")

    app = make_langgraph_agent(qa_chain)
    question = "What are the main causes of climate change and what countries are the biggest emitters?"
    print(f"❓ Question: {question}\n")

    start = time.time()
    final_state = app.invoke({
        "messages": [HumanMessage(content=question)],
        "tool_calls_log": [],
        "loop_count": 0
    })
    elapsed = time.time() - start

    # Extract final answer
    final_answer = ""
    for msg in reversed(final_state["messages"]):
        if isinstance(msg, AIMessage) and "Final Answer:" in msg.content:
            final_answer = msg.content.split("Final Answer:")[-1].strip()
            break

    print(f"\n💬 Final Answer:\n{final_answer}\n")

    print("📋 Full Decision Log:")
    for i, entry in enumerate(final_state.get("tool_calls_log", []), 1):
        print(f"   {i}. {entry['tool']}({entry['input'][:50]})")
        print(f"      → {entry['result_preview'][:80]}...")
        print(f"      @ {entry['timestamp']}")

    return {"loops": final_state.get("loop_count", 0), "elapsed": elapsed}


# ==================== MAIN ====================

def main():
    print("\n" + "=" * 60)
    print("Production Agent Demo: LangChain vs LangGraph")
    print("=" * 60 + "\n")

    qa_chain = setup_local_search()

    lc_stats = demo_langchain_agent(qa_chain)

    input("\nPress Enter to run LangGraph...\n")

    lg_stats = demo_langgraph_agent(qa_chain)

    # Side-by-side comparison
    print("\n" + "=" * 60)
    print("COMPARISON")
    print("=" * 60)
    print(f"{'':20} {'LangChain':>15} {'LangGraph':>15}")
    print(f"{'─'*50}")
    print(f"{'Agentic loops':20} {lc_stats['loops']:>15} {lg_stats['loops']:>15}")
    print(f"{'Total time (s)':20} {lc_stats['elapsed']:>15.2f} {lg_stats['elapsed']:>15.2f}")

    print("""
KEY TAKEAWAYS
─────────────
Both agents use the same LLM and same tools.

LangChain:
  ✅ Less code to write
  ❌ Decisions are invisible until after the fact
  ❌ Can't pause, inspect, or redirect mid-run
  ❌ Hard to test individual steps

LangGraph:
  ✅ Every LLM decision is visible as structured state
  ✅ Numbered loops — instantly see how many iterations ran
  ✅ Full audit trail of what happened and why
  ✅ Checkpointing: pause, resume, branch at any point
  ❌ More code to set up

When to use each:
  Prototyping / simple pipelines  → LangChain
  Production / auditability       → LangGraph
""")


if __name__ == "__main__":
    main()
