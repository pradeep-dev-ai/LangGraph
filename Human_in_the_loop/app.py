import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

# -----------------------------
# 1. Define State
# -----------------------------
class ContractState(TypedDict):
    contract_text: str
    issues: list
    status: str


# -----------------------------
# 2. Nodes
# -----------------------------
def review_contract(state: ContractState):
    text = state.get("contract_text", "").lower()
    issues = []

    if "penalty" in text:
        issues.append("Penalty clause detected")

    if "terminate anytime" in text:
        issues.append("Unfair termination clause")

    return {"issues": issues, "status": "reviewed"}

def human_review(state: ContractState):
    issues = state.get("issues", [])

    decision = interrupt({
        "message": "Approve or Reject?",
        "issues": issues
    })

    if decision == "approve":
        return {"status": "approved"}
    else:
        return {"status": "rejected"}

def finalize(state: ContractState):
    return state


# -----------------------------
# 3. Routing Logic (IMPORTANT)
# -----------------------------
def route_after_review(state: ContractState):
    if len(state["issues"]) == 0:
        return "finalize"
    else:
        return "human_review"


# -----------------------------
# 4. Build Graph
# -----------------------------
builder = StateGraph(ContractState)

builder.add_node("review_contract", review_contract)
builder.add_node("human_review", human_review)
builder.add_node("finalize", finalize)

builder.set_entry_point("review_contract")

builder.add_conditional_edges(
    "review_contract",
    route_after_review,
    {
        "human_review": "human_review",
        "finalize": "finalize"
    }
)

builder.add_edge("human_review", "finalize")
builder.add_edge("finalize", END)

# Checkpoint (to pause & resume)
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)


# -----------------------------
# 5. Streamlit UI
# -----------------------------
st.title("📄 HITL Contract Reviewer")

# Session state setup
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "thread_1"

if "paused" not in st.session_state:
    st.session_state.paused = False

if "issues" not in st.session_state:
    st.session_state.issues = []

config = {"configurable": {"thread_id": st.session_state.thread_id}}

contract_text = st.text_area("Enter Contract Text")

# -----------------------------
# Step 1: Analyze Contract
# -----------------------------
if st.button("Analyze Contract"):
    result = graph.invoke(
        {
            "contract_text": contract_text,
            "issues": [],
            "status": "pending"
        },
        config=config
    )

    # If issues exist → pause for human
    if len(result.get("issues", [])) > 0:
        st.session_state.paused = True
        st.session_state.issues = result["issues"]
    else:
        st.success("✅ Contract Auto Approved")
        st.write(result)


# -----------------------------
# Step 2: Human Approval UI
# -----------------------------
if st.session_state.paused:
    st.warning("⚠️ Human Approval Required")

    st.write("### Issues Found:")
    for issue in st.session_state.issues:
        st.write("-", issue)

    col1, col2 = st.columns(2)

    # Approve
    with col1:
        if st.button("✅ Approve"):
            result = graph.invoke(
                Command(resume="approve"),
                config=config
            )
            st.success("Approved ✅")
            st.write(result)
            st.session_state.paused = False

    # Reject
    with col2:
        if st.button("❌ Reject"):
            result = graph.invoke(
                Command(resume="reject"),
                config=config
            )
            st.error("Rejected ❌")
            st.write(result)
            st.session_state.paused = False