import streamlit as st
import requests
import pandas as pd
import sqlite3

# --- Configuration ---
st.set_page_config(page_title="Multi-Agent Assistant", layout="wide")
st.title("🤖 Multi-Agent Productivity Assistant")

# FastAPI backend URL and Database name
API_URL = "http://127.0.0.1:8080/chat"
DB_NAME = "my_calendar.db"

# --- Layout: Two Columns ---
col1, col2 = st.columns([1, 1])

# --- LEFT COLUMN: Chat Interface ---
with col1:
    st.subheader("💬 Chat with your Manager Agent")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    if prompt := st.chat_input("E.g., Add 'Submit Hackathon' to tasks and book it for 4 PM"):
        # 1. Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Send to FastAPI Backend
        with st.spinner("Manager is coordinating with agents..."):
            try:
                response = requests.post(API_URL, json={"prompt": prompt})
                if response.status_code == 200:
                    reply = response.json().get("response", "Error reading response.")
                else:
                    reply = f"Backend Error: {response.status_code}"
            except Exception as e:
                reply = "⚠️ Failed to connect to backend. Is Uvicorn running?"

        # 3. Show AI response
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

# --- RIGHT COLUMN: Live Dashboards ---
with col2:
    st.subheader("📊 Live Database Views")
    
    # Helper function to safely load SQLite tables into Pandas DataFrames
    def load_data(table_name):
        try:
            conn = sqlite3.connect(DB_NAME)
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception:
            return pd.DataFrame()

    # 1. To-Do List Table
    st.markdown("### 📋 To-Do List (Task Agent)")
    tasks_df = load_data("tasks")
    if not tasks_df.empty:
        # Drop the 'id' column to make it look cleaner for the judges
        st.dataframe(tasks_df.drop(columns=['id'], errors='ignore'), use_container_width=True)
    else:
        st.info("No tasks added yet.")

    # 2. Schedule Table
    st.markdown("### 📅 Schedule (Calendar Agent)")
    calendar_df = load_data("calendar")
    if not calendar_df.empty:
        st.dataframe(calendar_df.drop(columns=['id'], errors='ignore'), use_container_width=True)
    else:
        st.info("No events scheduled yet.")
        
    # Auto-refresh note
    st.caption("💡 Dashboards refresh automatically when you send a new message.")