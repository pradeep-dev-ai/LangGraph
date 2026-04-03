# backend.py

from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv

import sqlite3
import requests
import os

load_dotenv()

# -------------------
# 1. LLM
# -------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------
# 2. Tools
# -------------------

# 🔍 Search Tool
search_tool = DuckDuckGoSearchRun(region="us-en")


# 🧮 Calculator Tool
@tool
def calculator(first_num: float, second_num: float, operation: str) -> str:
    """
    Perform arithmetic: add, sub, mul, div.
    Example:
    - add: 5 + 3
    - mul: 5 * 3
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return "Error: Division by zero"
            result = first_num / second_num
        else:
            return "Error: Unsupported operation"

        return f"Result: {result}"

    except Exception as e:
        return f"Error: {str(e)}"


# 📈 Stock Tool
@tool
def get_stock_price(symbol: str) -> str:
    """
    Get latest stock price.
    Example: AAPL, TSLA, MSFT
    """
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
        r = requests.get(url, timeout=5)
        data = r.json()

        price = data.get("Global Quote", {}).get("05. price")

        if not price:
            return f"Could not fetch price for {symbol}"

        return f"{symbol} stock price is ${price}"

    except Exception as e:
        return f"Error fetching stock data: {str(e)}"


# Tool list
tools = [search_tool, get_stock_price, calculator]

# Bind tools
llm_with_tools = llm.bind_tools(tools)

# -------------------
# 3. State
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------
# 4. Nodes
# -------------------
def chat_node(state: ChatState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# -------------------
# 5. SQLite Memory
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "chatbot.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
checkpointer = SqliteSaver(conn)

# -------------------
# 6. Graph
# -------------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")

graph.add_conditional_edges(
    "chat_node",
    tools_condition
)

graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

# -------------------
# 7. Thread Helper
# -------------------
def retrieve_all_threads():
    try:
        threads = set()
        for checkpoint in checkpointer.list(None):
            thread_id = checkpoint.config.get("configurable", {}).get("thread_id")
            if thread_id:
                threads.add(thread_id)
        return list(threads)
    except:
        return []