from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

from app.extractor import extract_once, extract_retry
from app.validator import validate
from app.schemas import InvoiceFields, AgentResult


class AgentState(TypedDict, total=False):
    text: str
    data: Optional[InvoiceFields]
    issues: List[str]
    attempts: int


def extract_node(state: AgentState):
    data = extract_once(state["text"])
    return {
        "data": data,
        "attempts": 1,
    }


def validate_node(state: AgentState):
    issues = validate(state["data"], state["text"])
    return {
        "issues": issues,
    }


def retry_node(state: AgentState):
    data = extract_retry(state["text"])
    return {
        "data": data,
        "attempts": state.get("attempts", 1) + 1,
    }


def decide_next(state: AgentState):
    issues = state.get("issues", [])
    attempts = state.get("attempts", 0)

    if not issues:
        return "success"

    if attempts >= 2:
        return "human_review"

    return "retry"


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("extract", extract_node)
    builder.add_node("validate", validate_node)
    builder.add_node("retry", retry_node)

    builder.set_entry_point("extract")

    builder.add_edge("extract", "validate")

    builder.add_conditional_edges(
        "validate",
        decide_next,
        {
            "success": END,
            "retry": "retry",
            "human_review": END,
        },
    )

    builder.add_edge("retry", "validate")

    return builder.compile()


graph = build_graph()


def run_agent(text: str) -> AgentResult:
    result = graph.invoke(
        {
            "text": text,
            "attempts": 0,
            "issues": [],
        }
    )

    issues = result.get("issues", [])
    status = "success" if not issues else "human_review"

    return AgentResult(
        status=status,
        extracted_data=result.get("data"),
        issues=issues,
        attempts=result.get("attempts", 0),
    )