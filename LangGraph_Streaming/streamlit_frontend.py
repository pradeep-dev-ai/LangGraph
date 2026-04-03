import streamlit as st
from langgraph_backend import chatbot

st.title("LangGraph Streaming Chatbot 🤖")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Assistant response (streaming)
    response_container = st.chat_message("assistant")
    full_response = ""

    with response_container:
        response_placeholder = st.empty()

        for chunk in chatbot(user_input):
            full_response += chunk
            response_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )