import streamlit as st
import time

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Ruby")

# ---------------------------
# Session state initialization (MUST BE FIRST)
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Avatar selection
# ---------------------------
choices = ["Male", "Female"]
mode = st.selectbox("Select Gender", choices)

user_icon = "male.png" if mode == "Male" else "female.png"
bot_icon = "bot.png"

# ---------------------------
# Display chat history
# ---------------------------

with st.sidebar:
    st.header("Options")

    show_history = st.button("Show Chat History")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.toast("Chat history cleared!")

    if show_history:
        st.subheader("Chat History")
        for msg in st.session_state.messages:
            avatar = user_icon if msg["role"] == "user" else bot_icon
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

                   

# ---------------------------
# Streaming reply
# ---------------------------
def bot_reply(text):
    response = f"You said: {text}"
    for word in response.split():
        yield word + " "
        time.sleep(0.25)

# ---------------------------
# Chat input
# ---------------------------
user_input = st.chat_input("Say something ... ^_^")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar=user_icon):
        st.write(user_input)

    with st.chat_message("assistant", avatar=bot_icon):
        full_reply = st.write_stream(bot_reply(user_input))

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
