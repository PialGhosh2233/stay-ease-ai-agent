from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agent.nodes import (
    classify_request_node,
    compose_response_node,
    execute_tool_node,
    extract_entities_node,
    human_escalation_node,
    route_after_classification,
)
from agent.state import AgentState


def build_graph():
    """StayEase LangGraph workflow."""
    graph = StateGraph(AgentState)

    graph.add_node("classify_request", classify_request_node)
    graph.add_node("extract_entities", extract_entities_node)
    graph.add_node("execute_tool", execute_tool_node)
    graph.add_node("compose_response", compose_response_node)
    graph.add_node("human_escalation", human_escalation_node)

    graph.add_edge(START, "classify_request")
    graph.add_conditional_edges(
        "classify_request",
        route_after_classification,
        {
            "extract_entities": "extract_entities",
            "human_escalation": "human_escalation",
        },
    )
    graph.add_edge("extract_entities", "execute_tool")
    graph.add_edge("execute_tool", "compose_response")
    graph.add_edge("compose_response", END)
    graph.add_edge("human_escalation", END)

    return graph.compile()


stayease_graph = build_graph()
