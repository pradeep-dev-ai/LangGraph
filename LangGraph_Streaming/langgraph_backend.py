from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

# Define state
class ChatState(TypedDict):
    input: str
    output: str

# LLM with streaming enabled
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    streaming=True
)

# Node function
def chatbot_node(state: ChatState):
    response = llm.invoke(state["input"])
    return {"output": response.content}

# Build graph
builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

# Streaming function (important)
def chatbot(user_input):
    for event in graph.stream({"input": user_input}, stream_mode="values"):
        if "output" in event:
            yield event["output"]