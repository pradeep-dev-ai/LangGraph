# 🚀 LangGraph Tools Chatbot

A powerful AI chatbot built using **LangGraph**, **LangChain**, and **Streamlit** with support for:

* 🧠 LLM-based conversations
* 🛠️ Tool usage (Calculator, Web Search, Stock Price)
* 💾 Persistent memory using SQLite
* 🔄 Multi-turn conversation support

---

## 📌 Features

* 🔍 **Web Search Tool** (DuckDuckGo)
* 🧮 **Calculator Tool** (basic arithmetic)
* 📈 **Stock Price Tool** (Alpha Vantage API)
* 💬 **Conversational AI** using OpenAI models
* 💾 **SQLite memory** for chat persistence
* 🔄 **LangGraph workflow orchestration**

---

## 🏗️ Tech Stack

* **LangGraph**
* **LangChain**
* **OpenAI (gpt-4o-mini)**
* **Streamlit**
* **SQLite**
* **Python**

---

## 📂 Project Structure

```
LangGraph_Tools/
│── frontend.py          # Streamlit UI
│── tool_backend.py      # LangGraph + Tools logic
│── chatbot.db           # SQLite database (ignored)
│── .env                 # API keys (ignored)
│── .gitignore
│── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/pradeep-dev-ai/LangGraph.git
cd LangGraph/LangGraph_Tools
```

---

### 2. Create virtual environment

```bash
python -m venv env
env\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install langgraph langchain langchain-core langchain-openai langchain-community streamlit python-dotenv requests ddgs langgraph-checkpoint-sqlite
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run frontend.py
```

---

## 🧠 How It Works

1. User sends a message
2. LangGraph processes it
3. LLM decides:

   * Direct answer OR
   * Call a tool
4. Tool executes
5. Result is returned to LLM
6. Final response shown in UI

---

## 🔧 Available Tools

### 🧮 Calculator

* add, sub, mul, div

### 🔍 Web Search

* Uses DuckDuckGo

### 📈 Stock Price

* Uses Alpha Vantage API

---

## ⚠️ Notes

* `.env` and `chatbot.db` are ignored via `.gitignore`
* Do not expose API keys publicly
* SQLite is used for local persistence

---

## 🚀 Future Improvements

* ✅ Add chat history per thread
* ✅ Add authentication system
* ✅ Integrate RAG (PDF chatbot)
* ✅ Deploy on cloud (Streamlit Cloud / AWS)

---

