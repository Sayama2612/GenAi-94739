import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Ruby")

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "edit_text" not in st.session_state:
    st.session_state.edit_text = ""

if "awaiting_reply" not in st.session_state:
    st.session_state.awaiting_reply = False

# --------------------------------------------------
# GROQ API
# --------------------------------------------------

def call_groq(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"]

# --------------------------------------------------
# GEMINI API
# --------------------------------------------------

def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-2.5-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers={"Content-Type": "application/json"},
                             data=json.dumps(payload), timeout=30)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# --------------------------------------------------
# PHI-4 MINI
# --------------------------------------------------

def call_phi4_mini(prompt):
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={
            "Authorization": "Bearer dummy-key",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "microsoft/phi-4-mini-reasoning",
            "messages": [{"role": "user", "content": prompt}]
        }),
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"]

# --------------------------------------------------
# LLAMA LOCAL
# --------------------------------------------------

def cal_llama_model(prompt):
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={
            "Authorization": "Bearer dummy-key",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "meta-llama-3-4b-mlp-pruned",
            "messages": [{"role": "user", "content": prompt}]
        }),
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"]

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("Options")
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    model = st.radio(
        "Select LLM Model",
        ["GROQ Model", "Gemini Model", "Phi-4 mini model", "meta-llama-3-4b-mlp-pruned model"]
    )

    if st.button("➕ New Chat"):
        name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name

    st.divider()
    for chat in st.session_state.chats:
        if st.button(chat):
            st.session_state.current_chat = chat

# --------------------------------------------------
# Avatars
# --------------------------------------------------

user_icon = "male.png" if gender == "Male" else "female.png"
bot_icon = "bot.png"

messages = st.session_state.chats[st.session_state.current_chat]

# --------------------------------------------------
# Display Messages
# --------------------------------------------------

for i, msg in enumerate(messages):
    avatar = user_icon if msg["role"] == "user" else bot_icon
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"], unsafe_allow_html=False)

        if (
            msg["role"] == "user"
            and i == len(messages) - 2
            and st.session_state.edit_index is None
        ):
            if st.button("✏️ Edit Prompt", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.session_state.edit_text = msg["content"]
                st.rerun()

# --------------------------------------------------
# Edit Prompt
# --------------------------------------------------

if st.session_state.edit_index is not None:
    edited = st.text_area("Modify prompt", st.session_state.edit_text)
    col1, col2 = st.columns(2)

    if col1.button("🔁 Regenerate"):
        idx = st.session_state.edit_index
        messages[idx]["content"] = edited
        messages.pop(idx + 1)
        reply = (
            call_groq(edited) if model == "GROQ Model" else
            call_gemini(edited) if model == "Gemini Model" else
            call_phi4_mini(edited) if model == "Phi-4 mini model" else
            cal_llama_model(edited)
        )
        messages.insert(idx + 1, {"role": "assistant", "content": reply})
        st.session_state.edit_index = None
        st.rerun()

    if col2.button("❌ Cancel"):
        st.session_state.edit_index = None

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

user_input = st.chat_input("Say something... ^_^")

if user_input:
    messages.append({"role": "user", "content": user_input})
    st.session_state.awaiting_reply = True
    st.rerun()

# --------------------------------------------------
# Assistant Reply (ONLY ONCE)
# --------------------------------------------------

if st.session_state.awaiting_reply:
    with st.chat_message("assistant", avatar=bot_icon):
        with st.spinner("Thinking..."):
            prompt = messages[-1]["content"]
            reply = (
                call_groq(prompt) if model == "GROQ Model" else
                call_gemini(prompt) if model == "Gemini Model" else
                call_phi4_mini(prompt) if model == "Phi-4 mini model" else
                cal_llama_model(prompt)
            )
            st.markdown(reply, unsafe_allow_html=False)

    messages.append({"role": "assistant", "content": reply})
    st.session_state.awaiting_reply = False
    st.rerun()
