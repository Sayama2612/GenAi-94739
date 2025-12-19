import streamlit as st
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# ----------------------------------
# Load environment variables
# ----------------------------------

load_dotenv()

# ----------------------------------
# Page config
# ----------------------------------

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot (Context Limited by Turns)")

# ----------------------------------
# Initialize LLM
# ----------------------------------

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------------
# Sidebar: Context control
# ----------------------------------

st.sidebar.header("⚙️ Settings")

context_turns = st.sidebar.slider(
    "Number of last conversation turns",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

st.sidebar.caption(
    "1 turn = 1 user + 1 assistant message"
)

# ----------------------------------
# Session State
# ----------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# ----------------------------------
# Display Chat History
# ----------------------------------

for msg in st.session_state.conversation:
    if msg["role"] == "system":
        continue

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------------
# Chat Input (ONLY ONE)
# ----------------------------------

user_input = st.chat_input(
    "Say something...",
    key="chat_input"
)

# ----------------------------------
# Handle User Input
# ----------------------------------

if user_input:
    # Save user message
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # ----------------------------------
    # CONTEXT LIMITING LOGIC (TURN-BASED)
    # ----------------------------------
    
    system_msg = st.session_state.conversation[0]

    # Each turn = user + assistant = 2 messages
    messages_to_send = context_turns * 2

    recent_msgs = st.session_state.conversation[1:][-messages_to_send:]

    context_to_send = [system_msg] + recent_msgs

    # ----------------------------------
    # Call LLM
    # ----------------------------------
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            llm_output = llm.invoke(context_to_send)
            st.write(llm_output.content)

    # Save assistant response
    st.session_state.conversation.append(
        {"role": "assistant", "content": llm_output.content}
    )

    # ----------------------------------
    # Optional Debug (comment out later)
    # ----------------------------------
    
    st.sidebar.write(
        "Messages sent to LLM:", len(context_to_send)
    )
