import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(page_title="Tool Calling Chatbot", page_icon="🤖")
st.title("🤖 Tool Calling Chatbot")

# --------------------------------------------------
# Tools
# --------------------------------------------------

@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"

@tool
def get_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'    
    """
    try:
        api_key = OPEN_WEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"

@tool
def read_file(filepath):
    """
    This read_file() function gets path of the given file.
    It reads the content of the file and returns it as a string
    
    :param filepath
    :returns result as str
    """
    
    with open(filepath, 'r') as file:
        text = file.read()
        return text

@tool
def knowledge_lookup(topic):
    """
    Returns basic knowledge about a topic.
    (Simple internal lookup)
    """
    knowledge_base = {
        "python": "Python is a high-level programming language known for simplicity.",
        "java": "Java is a class-based, object-oriented programming language.",
        "ai": "Artificial Intelligence enables machines to mimic human intelligence.",
        "ml": "Machine Learning is a subset of AI focused on learning from data."
    }

    return knowledge_base.get(
        topic.lower(),
        f"No knowledge found for topic: {topic}"
    )
    
# --------------------------------------------------
# Initialize LLM (Groq)
# --------------------------------------------------

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = GROQ_API_KEY
)

# --------------------------------------------------
# Create Agent
# --------------------------------------------------

agent = create_agent(
    model = llm,
    tools = [calculator, get_weather, read_file, knowledge_lookup],
    system_prompt = "You are a helpful assistant. Answer in short."
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------------------------------
# User Input
# --------------------------------------------------

user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call agent
    result = agent.invoke({
        "messages": st.session_state.messages
    })

    ai_message = result["messages"][-1].content

    # Save AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_message}
    )

    with st.chat_message("assistant"):
        st.markdown(ai_message)
