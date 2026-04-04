from typing import TypedDict
from langgraph.graph import StateGraph, END
from backend.agents import research_agent, bull_agent, bear_agent, judge_agent


class AgentState(TypedDict):
    query: str
    research: str
    bull: str
    bear: str
    final: str


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("research", research_agent)
    builder.add_node("bull", bull_agent)
    builder.add_node("bear", bear_agent)
    builder.add_node("judge", judge_agent)

    builder.set_entry_point("research")

    # Parallel execution
    builder.add_edge("research", "bull")
    builder.add_edge("research", "bear")

    builder.add_edge("bull", "judge")
    builder.add_edge("bear", "judge")

    builder.add_edge("judge", END)

    return builder.compile()


graph = build_graph()


# 🔴 Streaming function
def run_analysis_stream(query):
    for step in graph.stream({"query": query}):
        yield step


# Normal run
def run_analysis(query):
    return graph.invoke({"query": query})