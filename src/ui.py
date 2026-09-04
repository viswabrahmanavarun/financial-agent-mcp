import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

# Ensure we can import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.agent import FinancialAgent, PERSONAS

load_dotenv()

st.set_page_config(page_title="AI Financial Analyst", layout="wide")

st.title("AI Financial Analyst (Configurable Persona)")

# Sidebar for configuration
st.sidebar.header("Agent Configuration")
selected_persona = st.sidebar.selectbox("Persona", list(PERSONAS.keys()))
selected_sector = st.sidebar.selectbox("Sector Context", ["Tech", "Retail", "Logistics"])

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Persona Lens:**\n\n{PERSONAS[selected_persona]}")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask a question about the companies in this sector...")

if user_query:
    # Display user query
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Execute agent
    with st.chat_message("assistant"):
        with st.spinner(f"Analyzing as {selected_persona}..."):
            try:
                agent = FinancialAgent()
                # Run async agent in sync Streamlit context
                response = asyncio.run(agent.query(user_query, selected_persona, selected_sector))
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
