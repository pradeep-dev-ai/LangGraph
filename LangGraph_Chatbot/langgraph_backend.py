from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

# ================== ENV ==================
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ================== LLM ==================
llm = ChatOpenAI()

# ================== STATE ==================
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ================== NODE ==================
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# ================== CHECKPOINTER ==================
checkpointer = InMemorySaver()

# ================== GRAPH ==================
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# ================== THREAD RETRIEVAL ==================
def retrieve_all_threads():
    try:
        # InMemorySaver stores threads here
        return list(checkpointer.storage.keys())
    except Exception:
        return []