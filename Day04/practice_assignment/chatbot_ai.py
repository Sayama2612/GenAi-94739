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

# --------------------------------------------------
# GROQ API
# --------------------------------------------------
def call_groq(prompt):
    try:
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
    except Exception as e:
        return f"Groq Error: {e}"

# --------------------------------------------------
# GEMINI API
# --------------------------------------------------
def call_gemini(prompt):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-2.5-flash:generateContent?key={api_key}"
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30
        )
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini Error: {e}"

# --------------------------------------------------
# PHI-4 MINI (LM Studio)
# --------------------------------------------------
def call_phi4_mini(prompt):
    try:
        url = "http://127.0.0.1:1234/v1/chat/completions"
        headers = {
            "Authorization": "Bearer dummy-key",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "microsoft/phi-4-mini-reasoning",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            url, headers=headers, data=json.dumps(payload), timeout=30
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Model Error: {e}"

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("Options")

    gender = st.selectbox("Select Gender", ["Male", "Female"])
    model = st.radio(
        "Select LLM Model",
        ["GROQ Model", "Gemini Model", "Phi-4 mini model"]
    )

    if st.button("➕ New Chat"):
        chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[chat_name] = []
        st.session_state.current_chat = chat_name

    st.divider()
    st.subheader("Chat History")

    for chat in st.session_state.chats:
        if st.button(chat):
            st.session_state.current_chat = chat

# --------------------------------------------------
# Avatars
# --------------------------------------------------
user_icon = "male.png" if gender == "Male" else "female.png"
bot_icon = "bot.png"

# --------------------------------------------------
# Display Messages
# --------------------------------------------------
messages = st.session_state.chats[st.session_state.current_chat]
if "last_user_index" not in st.session_state:
    st.session_state.last_user_index = None
# --------------------------------------------------
# Display Messages + Edit Button
# --------------------------------------------------
for i, msg in enumerate(messages):
    avatar = user_icon if msg["role"] == "user" else bot_icon
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

        # ✅ Edit ALWAYS on latest user message
        if (
            msg["role"] == "user"
            and i == st.session_state.last_user_index
            and st.session_state.edit_index is None
        ):
            if st.button("✏️ Edit Prompt", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.session_state.edit_text = msg["content"]
                st.rerun()


# --------------------------------------------------
# Edit Prompt Section
# --------------------------------------------------
if st.session_state.edit_index is not None:
    st.subheader("✏️ Edit your prompt")

    edited_prompt = st.text_area(
        "Modify prompt",
        value=st.session_state.edit_text,
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Regenerate"):
            idx = st.session_state.edit_index

            # Update user message
            messages[idx]["content"] = edited_prompt

            # Remove old assistant response
            messages.pop(idx + 1)

            # Generate new response
            if model == "GROQ Model":
                reply = call_groq(edited_prompt)
            elif model == "Gemini Model":
                reply = call_gemini(edited_prompt)
            else:
                reply = call_phi4_mini(edited_prompt)

            messages.insert(idx + 1, {
                "role": "assistant",
                "content": reply
            })

            st.session_state.edit_index = None
            st.rerun()

    with col2:
        if st.button("❌ Cancel"):
            st.session_state.edit_index = None

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
user_input = st.chat_input("Say something... ^_^")

if user_input:
  
    messages.append({"role": "user", "content": user_input})

    # SAVE index immediately
    st.session_state.last_user_index = len(messages) - 1

  
    st.rerun()

if messages and messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar=bot_icon):
        with st.spinner("Thinking..."):
            if model == "GROQ Model":
                reply = call_groq(messages[-1]["content"])
            elif model == "Gemini Model":
                reply = call_gemini(messages[-1]["content"])
            else:
                reply = call_phi4_mini(messages[-1]["content"])

            st.write(reply)

    messages.append({"role": "assistant", "content": reply})
    st.rerun()