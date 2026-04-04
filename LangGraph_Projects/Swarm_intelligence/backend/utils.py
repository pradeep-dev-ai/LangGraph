import streamlit as st


def init_memory():
    if "history" not in st.session_state:
        st.session_state.history = []


def add_memory(query, result):
    st.session_state.history.append({
        "query": query,
        "result": result
    })


def get_memory():
    return st.session_state.history