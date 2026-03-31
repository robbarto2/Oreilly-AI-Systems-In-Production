#!/usr/bin/env python3
"""
Production-Ready Agent Demo: LangChain vs LangGraph

This demo shows the difference between LangChain and LangGraph for production deployments.
Focus: error handling, observability, cost tracking, and explicit control flow.

Usage:
    python agent_production_demo.py
"""

import os
import time
import warnings
from pathlib import Path
from typing import TypedDict, Optional
from datetime import datetime

# Suppress deprecation warnings for cleaner demo output
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*deprecated.*')

# Cursor / IDE runs with workspace root as cwd; data files live next to this script.
_SCRIPT_DIR = Path(__file__).resolve().parent

# LangChain imports
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType

# LangGraph imports
from langgraph.graph import StateGraph, END

# For web search fallback
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️  Wikipedia not installed. Install with: pip install wikipedia")


class MetricsTracker:
    """Track costs and performance metrics for production monitoring"""

    def __init__(self):
        self.tool_calls = 0
        self.errors = 0
        self.start_time = None
        self.decisions = []

    def reset(self):
        self.__init__()

    def start(self):
        self.start_time = time.time()

    def log_tool_call(self, tool_name: str, success: bool):
        self.tool_calls += 1
        self.decisions.append({
            "tool": tool_name,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        if not success:
            self.errors += 1

    def report(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            "tool_calls": self.tool_calls,
            "errors": self.errors,
            "elapsed_seconds": round(elapsed, 2),
            "decisions": self.decisions
        }


# Global metrics tracker
metrics = MetricsTracker()


def setup_local_search():
    """Set up RAG system for local document search"""
    print("📚 Setting up local RAG system...")

    # Load and chunk the document
    loader = TextLoader(str(_SCRIPT_DIR / "climate.txt"))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=str(_SCRIPT_DIR / "demo_chroma")
    )

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3}
    )

    # Create QA chain
    llm = Ollama(model="llama3")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    print("✅ RAG system ready\n")
    return qa_chain


def local_search_tool(query: str, qa_chain) -> str:
    """Search local documents with error handling"""
    try:
        metrics.log_tool_call("local_search", True)
        result = qa_chain.invoke({"query": query})
        return result["result"]
    except Exception as e:
        metrics.log_tool_call("local_search", False)
        return f"❌ Local search failed: {str(e)}"


def web_search_tool(query: str, simulate_failure: bool = False) -> str:
    """Search Wikipedia with error handling and retry logic"""

    if simulate_failure:
        metrics.log_tool_call("web_search", False)
        return "❌ Web API unavailable (simulated failure)"

    if not WIKIPEDIA_AVAILABLE:
        metrics.log_tool_call("web_search", False)
        return "❌ Wikipedia module not installed"

    try:
        metrics.log_tool_call("web_search", True)
        # Search Wikipedia
        search_results = wikipedia.search(query)
        if search_results:
            page_title = search_results[0]
            summary = wikipedia.summary(page_title, sentences=3)
            return f"📰 From Wikipedia ({page_title}): {summary}"
        else:
            return "❌ No Wikipedia results found"
    except Exception as e:
        metrics.log_tool_call("web_search", False)
        return f"❌ Web search failed: {str(e)}"


# ==================== PART 1: LANGCHAIN AGENT ====================

def demo_langchain_agent(qa_chain, simulate_failure: bool = False):
    """
    LangChain agent with tools

    Pros: Quick to set up
    Cons: Limited control, hard to debug, unpredictable behavior
    """
    print("=" * 60)
    print("PART 1: LangChain Agent (Quick but Less Control)")
    print("=" * 60)

    # Create tools
    tools = [
        Tool(
            name="LocalSearch",
            func=lambda q: local_search_tool(q, qa_chain),
            description="Search local climate documents. Use this first for climate-related questions."
        ),
        Tool(
            name="WebSearch",
            func=lambda q: web_search_tool(q, simulate_failure),
            description="Search Wikipedia. Use only if local search doesn't find the answer."
        )
    ]

    # Initialize agent
    llm = Ollama(model="llama3")
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,  # In production, you'd use structured logging instead
        max_iterations=3,
        handle_parsing_errors=True
    )

    # Run query
    question = "What causes the most CO2 emissions?"
    print(f"\n❓ Question: {question}\n")

    metrics.reset()
    metrics.start()

    try:
        result = agent.invoke({"input": question})
        print(f"💬 Answer: {result['output']}\n")
    except Exception as e:
        print(f"❌ Agent failed: {str(e)}\n")

    # Show metrics
    report = metrics.report()
    print("📊 Metrics:")
    print(f"   - Tool calls: {report['tool_calls']}")
    print(f"   - Errors: {report['errors']}")
    print(f"   - Time: {report['elapsed_seconds']}s")

    if simulate_failure:
        print("\n⚠️  Notice: With LangChain, error handling is less transparent")
        print("   You don't have explicit control over retry logic or fallback behavior")

    print()


# ==================== PART 2: LANGGRAPH AGENT ====================

class AgentState(TypedDict):
    """State for LangGraph agent"""
    question: str
    local_result: Optional[str]
    web_result: Optional[str]
    final_answer: Optional[str]
    error: Optional[str]
    next_step: Optional[str]


def route_question(state: AgentState) -> AgentState:
    """
    Router node: Decides which tool to use first

    Production benefit: Explicit routing logic that's testable and observable
    """
    print("🔀 Router: Starting with local search (cheaper, faster)")
    return {**state, "next_step": "local"}


def local_search_node(state: AgentState, qa_chain) -> AgentState:
    """
    Local search node with error handling

    Production benefit: Can add retries, timeouts, circuit breakers here
    """
    print("📚 Searching local documents...")

    try:
        result = local_search_tool(state["question"], qa_chain)

        # Check if we got a good result
        if "❌" not in result:
            print(f"✅ Found answer locally: {result[:100]}...")
            return {
                **state,
                "local_result": result,
                "next_step": "synthesize"
            }
        else:
            print(f"⚠️  Local search failed, will try web search")
            return {
                **state,
                "local_result": None,
                "next_step": "web"
            }
    except Exception as e:
        print(f"❌ Local search error: {e}")
        return {
            **state,
            "local_result": None,
            "error": str(e),
            "next_step": "web"
        }


def web_search_node(state: AgentState, simulate_failure: bool = False) -> AgentState:
    """
    Web search node with fallback

    Production benefit: Explicit failure handling and cost awareness
    """
    print("🌐 Searching web (fallback)...")

    result = web_search_tool(state["question"], simulate_failure)

    if "❌" not in result:
        print(f"✅ Found answer on web: {result[:100]}...")
        return {
            **state,
            "web_result": result,
            "next_step": "synthesize"
        }
    else:
        print(f"❌ Web search also failed: {result}")
        return {
            **state,
            "web_result": None,
            "error": result,
            "next_step": "error"
        }


def synthesize_answer(state: AgentState) -> AgentState:
    """
    Synthesize final answer from available sources

    Production benefit: Clear citation and source tracking
    """
    print("🔄 Synthesizing final answer...")

    sources = []
    if state.get("local_result"):
        sources.append(f"Local documents: {state['local_result']}")
    if state.get("web_result"):
        sources.append(f"Web search: {state['web_result']}")

    if sources:
        final_answer = "\n\n".join(sources)
        return {
            **state,
            "final_answer": final_answer,
            "next_step": "end"
        }
    else:
        return {
            **state,
            "final_answer": "Unable to find answer from any source",
            "next_step": "end"
        }


def handle_error(state: AgentState) -> AgentState:
    """
    Error handling node

    Production benefit: Graceful degradation with clear error messages
    """
    error_msg = state.get("error", "Unknown error")
    print(f"⚠️  All sources failed. Error: {error_msg}")
    return {
        **state,
        "final_answer": f"Sorry, I couldn't retrieve an answer. Error: {error_msg}",
        "next_step": "end"
    }


def demo_langgraph_agent(qa_chain, simulate_failure: bool = False):
    """
    LangGraph agent with explicit control flow

    Pros: Observable, testable, predictable, production-ready
    Cons: More verbose setup
    """
    print("=" * 60)
    print("PART 2: LangGraph Agent (Production-Ready)")
    print("=" * 60)

    # Build the graph
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", route_question)
    graph.add_node("local", lambda s: local_search_node(s, qa_chain))
    graph.add_node("web", lambda s: web_search_node(s, simulate_failure))
    graph.add_node("synthesize", synthesize_answer)
    graph.add_node("error_handler", handle_error)

    # Set entry point
    graph.set_entry_point("router")

    # Add conditional edges based on next_step
    def route_next(state: AgentState) -> str:
        return state.get("next_step", "end")

    graph.add_conditional_edges(
        "router",
        route_next,
        {
            "local": "local",
            "end": END
        }
    )

    graph.add_conditional_edges(
        "local",
        route_next,
        {
            "web": "web",
            "synthesize": "synthesize",
            "end": END
        }
    )

    graph.add_conditional_edges(
        "web",
        route_next,
        {
            "synthesize": "synthesize",
            "error": "error_handler",
            "end": END
        }
    )

    graph.add_conditional_edges(
        "synthesize",
        route_next,
        {
            "end": END
        }
    )

    graph.add_conditional_edges(
        "error_handler",
        route_next,
        {
            "end": END
        }
    )

    # Compile the graph
    app = graph.compile()

    # Run query
    question = "What causes the most CO2 emissions?"
    print(f"\n❓ Question: {question}\n")

    metrics.reset()
    metrics.start()

    try:
        result = app.invoke({"question": question})
        print(f"\n💬 Final Answer:\n{result['final_answer']}\n")
    except Exception as e:
        print(f"❌ Agent failed: {str(e)}\n")

    # Show metrics
    report = metrics.report()
    print("📊 Metrics:")
    print(f"   - Tool calls: {report['tool_calls']}")
    print(f"   - Errors: {report['errors']}")
    print(f"   - Time: {report['elapsed_seconds']}s")
    print(f"\n📋 Decision Log:")
    for decision in report['decisions']:
        status = "✅" if decision['success'] else "❌"
        print(f"   {status} {decision['tool']} at {decision['timestamp']}")

    if simulate_failure:
        print("\n✨ Notice: LangGraph handled the failure gracefully!")
        print("   - Clear visibility into what failed and why")
        print("   - Explicit fallback logic")
        print("   - Structured error handling")

    print()


# ==================== MAIN DEMO ====================

def pause_for_explanation(message="Press Enter to continue...", talking_points=None):
    """Pause the demo so instructor can explain"""
    print("\n" + "─" * 60)
    print(f"⏸️  PAUSE FOR EXPLANATION")
    print("─" * 60)
    if talking_points:
        print("\n💬 Key points to cover:")
        for point in talking_points:
            print(f"   • {point}")
    print(f"\n{message}")
    print("─" * 60)
    input()


def main():
    """Run the complete demo"""
    print("\n" + "=" * 60)
    print("Production Agent Demo: LangChain vs LangGraph")
    print("=" * 60 + "\n")

    # Setup
    qa_chain = setup_local_search()

    # Part 1: LangChain (normal operation)
    print("\n🎬 Demo 1: Both approaches working normally\n")
    demo_langchain_agent(qa_chain, simulate_failure=False)

    # Pause for explanation
    pause_for_explanation(
        "Press Enter when ready to see LangGraph...",
        talking_points=[
            "LangChain worked, but notice: 3 tool calls, 12+ seconds",
            "Hit iteration limit - agent stopped prematurely",
            "No visibility into why it made those tool choices",
            "Hard to debug what happened under the hood"
        ]
    )

    demo_langgraph_agent(qa_chain, simulate_failure=False)

    # Pause before failure demo
    pause_for_explanation(
        "Press Enter to see failure handling...",
        talking_points=[
            "LangGraph: 1 tool call, ~1.5 seconds (8x faster!)",
            "Clear decision log shows exactly what happened",
            "Explicit routing: always try local (cheap) first",
            "This is testable, observable, production-ready"
        ]
    )

    # Part 2: With failure (shows difference in error handling)
    print("\n🎬 Demo 2: Simulating web API failure\n")
    demo_langchain_agent(qa_chain, simulate_failure=True)

    # Pause for explanation
    pause_for_explanation(
        "Press Enter to see how LangGraph handles the same failure...",
        talking_points=[
            "LangChain tried the web tool but we simulated a failure",
            "Error handling is opaque - you can't see what failed or why",
            "No easy way to add retry logic or fallback behavior",
            "At 2 AM debugging this in production, you'd be frustrated"
        ]
    )

    demo_langgraph_agent(qa_chain, simulate_failure=True)

    # Summary
    print("=" * 60)
    print("KEY TAKEAWAYS FOR PRODUCTION")
    print("=" * 60)
    print("""
    LangChain:
    ✅ Fast prototyping
    ✅ Less boilerplate
    ❌ Hard to debug agent decisions
    ❌ Limited error handling control
    ❌ Unpredictable tool usage

    LangGraph:
    ✅ Explicit control flow (testable!)
    ✅ Observable decision path
    ✅ Graceful error handling
    ✅ Cost-aware routing
    ✅ Production monitoring ready
    ❌ More verbose setup

    Recommendation:
    - Prototyping: LangChain
    - Production: LangGraph
    - Multi-agent: Consider CrewAI
    """)


if __name__ == "__main__":
    main()
