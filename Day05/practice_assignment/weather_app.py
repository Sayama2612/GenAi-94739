import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from streamlit_lottie import st_lottie

# ----------------------------------
# Load environment variables
# ----------------------------------
load_dotenv()

WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(page_title="Animated Weather App", page_icon="🌦️")
st.title("🌦️ Weather App with Animated Icons & LLM")

# ----------------------------------
# Initialize LLM (Groq)
# ----------------------------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------------
# Load Lottie from URL
# ----------------------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ----------------------------------
# Weather → Lottie Mapping
# ----------------------------------
def get_weather_animation(condition):
    condition = condition.lower()

    if "clear" in condition:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jmBauI.json")
    elif "cloud" in condition:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_Stdaec.json")
    elif "rain" in condition:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_rpC1Rd.json")
    elif "thunder" in condition:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_xRmNN8.json")
    elif "snow" in condition:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_HflU56.json")
    else:
        return load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_2ks3pj.json")

# ----------------------------------
# User Input
# ----------------------------------
city = st.text_input("🌍 Enter City Name")

# ----------------------------------
# Fetch Weather
# ----------------------------------
if st.button("Get Weather") and city:
    with st.spinner("Fetching weather..."):
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url)

        if response.status_code != 200:
            st.error("❌ Could not fetch weather data. Check city name.")
        else:
            data = response.json()

            # Extract weather info
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            condition = data["weather"][0]["description"]

            animation = get_weather_animation(condition)

            # ----------------------------------
            # UI Layout
            # ----------------------------------
            col1, col2 = st.columns([1, 3])

            with col1:
                st_lottie(animation, height=180, speed=1)

            with col2:
                st.subheader(f"📍 {city.title()}")
                st.write(f"🌡 **Temperature:** {temp} °C")
                st.write(f"💧 **Humidity:** {humidity}%")
                st.write(f"🌬 **Wind Speed:** {wind_speed} m/s")
                st.write(f"☁ **Condition:** {condition}")

            # ----------------------------------
            # LLM Explanation
            # ----------------------------------
            prompt = f"""
                You are a friendly assistant.

                Explain the following weather conditions in very simple English
                so that even a kid can understand it.

                City: {city}
                Temperature: {temp} °C
                Humidity: {humidity}%
                Wind Speed: {wind_speed} m/s
                Condition: {condition}
            """

            explanation = llm.invoke(prompt)

            st.subheader("🗣️ Simple Explanation")
            st.write(explanation.content)
