import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Animated Weather App", page_icon="🌦️")
st.title("🌦️ Weather App with Animation & LLM")

# -------------------------------
# CSS Animations
# -------------------------------
st.markdown("""
<style>
.weather-box {
    font-size: 100px;
    text-align: center;
    animation: float 2s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

.sun { color: gold; }
.cloud { color: lightgray; }
.rain { color: deepskyblue; }
.snow { color: aliceblue; }
.thunder { color: orange; }
.fog { color: silver; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LLM Init
# -------------------------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# -------------------------------
# Input
# -------------------------------
city = st.text_input("🌍 Enter city name")

# -------------------------------
# Button
# -------------------------------
if st.button("Get Weather") and city:

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("❌ Invalid city name")
    else:
        data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["main"].lower()

        # -------------------------------
        # Animation Selection
        # -------------------------------
        if "clear" in condition:
            icon, cls = "☀️", "sun"
        elif "cloud" in condition:
            icon, cls = "☁️", "cloud"
        elif "rain" in condition:
            icon, cls = "🌧️", "rain"
        elif "snow" in condition:
            icon, cls = "❄️", "snow"
        elif "thunder" in condition:
            icon, cls = "⚡", "thunder"
        else:
            icon, cls = "🌫️", "fog"

        # -------------------------------
        # Layout: LEFT animation | RIGHT data
        # -------------------------------
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(
                f'<div class="weather-box {cls}">{icon}</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.subheader(f"📍 {city.title()}")
            st.write(f"🌡 **Temperature:** {temp} °C")
            st.write(f"💧 **Humidity:** {humidity}%")
            st.write(f"🌬 **Wind Speed:** {wind} m/s")
            st.write(f"☁ **Condition:** {condition}")

        # -------------------------------
        # LLM Explanation
        # -------------------------------
        prompt = f"""
            You are a helpful assistant.
            Explain the following weather conditions in very simple English
            so that even a child can understand. Use emojis and simple analogies.

            City: {city}
            Temperature: {temp} °C
            Humidity: {humidity}%
            Wind Speed: {wind} m/s
            Condition: {condition}
        """
        explanation = llm.invoke(prompt)

        st.subheader("🗣️ Simple Weather Explanation")
        st.write(explanation.content)
