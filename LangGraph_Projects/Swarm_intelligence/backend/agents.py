import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

load_dotenv(override=True)  # Load .env file and override existing environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def research_agent(state):
    query = state["query"] + " AI revenue growth financial results"

    results = tavily.search(query=query, max_results=5)

    contents = list(set([
        r["content"] for r in results["results"]
        if "content" in r
    ]))

    return {"research": "\n".join(contents)}

def bull_agent(state):
    prompt = f"""
    You are a BULLISH financial analyst.

    DATA:
    {state['research']}

    Give strong positive insights.
    """
    return {"bull": llm.invoke(prompt).content}


def bear_agent(state):
    prompt = f"""
    You are a BEARISH financial analyst.

    DATA:
    {state['research']}

    Highlight risks and weaknesses.
    """
    return {"bear": llm.invoke(prompt).content}

def judge_agent(state):
    prompt = f"""
    You are a senior investment strategist.

    Create a PROFESSIONAL INVESTMENT REPORT in this format:

    ## 📌 Executive Summary
    (Short 3-4 lines summary)

    ## 🚀 Opportunities
    (Bullet points)

    ## ⚠️ Risks
    (Bullet points)

    ## 📊 Key Insights
    (Add any metrics, trends, or observations)
   ## 🧠 Final Recommendation
   Give ONE clear decision:
  - BUY (strong growth)
  - HOLD (balanced)
  - CAUTIOUS (high risk)

Also justify in 2 lines.
    BULL:
    {state['bull']}

    BEAR:
    {state['bear']}
    """

    return {"final": llm.invoke(prompt).content}