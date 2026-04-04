from unittest import result

import streamlit as st
from backend.graph import run_analysis_stream, run_analysis
from backend.utils import init_memory, add_memory, get_memory

st.set_page_config(page_title="AI Market Intelligence Swarm", layout="wide")

st.title("📊 AI Market Intelligence Swarm")
st.caption("Multi-Agent AI with Streaming + Memory + Stock Insights")

# ----------------------
# Memory Init
# ----------------------
init_memory()

# ----------------------
# Sidebar Memory
# ----------------------
st.sidebar.title("🧠 Session History")

for item in get_memory()[::-1]:
    st.sidebar.write(f"🔹 {item['query']}")

# ----------------------
# Input
# ----------------------
query = st.text_input("Enter Company / Industry")
ticker = st.text_input("Enter Stock Ticker (Optional, e.g., AAPL, TSLA)")

# ----------------------
# Stock Chart
# ----------------------
if ticker:
    st.subheader("📈 Live Stock Chart")

    import yfinance as yf
    import pandas as pd

    data = yf.download(ticker, period="6mo")

    if not data.empty:
        st.line_chart(data["Close"])
    else:
        st.error("Invalid ticker or no data found")
# ----------------------
# Streaming Output
# ----------------------
if st.button("🚀 Analyze"):

    research_box = st.empty()
    bull_box = st.empty()
    bear_box = st.empty()
    final_box = st.empty()

    final_output = ""

    for step in run_analysis_stream(query):
        for node, value in step.items():
            if isinstance(value, dict):
                for k, v in value.items():

                    if k == "research":
                        research_box.markdown(f"## 🔍 Research\n{v}")

                    elif k == "bull":
                        bull_box.markdown(f"## 🐂 Bull View\n{v}")

                    elif k == "bear":
                        bear_box.markdown(f"## 🐻 Bear View\n{v}")

                    elif k == "final":
                        final_output = v
                        final_box.markdown(f"## 🧠 Final Report\n{v}")

    st.success("✅ Analysis Complete")

    st.download_button(
        "📥 Download Report",
        final_output,
        file_name=f"{query}_report.txt"
    )
    
    final_box.markdown(
    f"""
    <div style="padding:20px; border-radius:10px; background-color:#111;">
    {v}
    </div>
    """,
    unsafe_allow_html=True
)