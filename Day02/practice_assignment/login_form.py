import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Weather App", page_icon="🌦️")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "show_login_success" not in st.session_state:
    st.session_state.show_login_success = False

if "show_logout_msg" not in st.session_state:
    st.session_state.show_logout_msg = False


# Login Page
def login_page():
    st.title("🔐 Login")

    if st.session_state.show_logout_msg:
        st.success("Thanks for using the Weather App 😊")
        st.session_state.show_logout_msg = False

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")

    if submit:
        if username == password and username != "":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_login_success = True
            st.rerun()
        else:
            st.error("Invalid credentials (Username must match Password)")


# Weather Page
def weather_page():
    if st.session_state.show_login_success:
        st.success("Login successful!")
        st.session_state.show_login_success = False

    st.title("🌦️ Weather Information")
    st.write(f"Welcome, **{st.session_state.username}** 👋")

    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        st.error("❌ API key not found. Please check your .env file.")
        return

    with st.form("weather_form"):
        city = st.text_input("Enter City Name")
        get_weather = st.form_submit_button("Get Weather")

    if get_weather:
        if city:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
                response = requests.get(url, timeout=5)
                weather = response.json()

                st.subheader(f"Weather in {city}")
                st.write(" Temperature:", weather["main"]["temp"], "°C")
                st.write(" Condition:", weather["weather"][0]["description"].title())
                st.write(" Wind Speed:", weather["wind"]["speed"], "km/h")
                st.write(" Humidity:", weather["main"]["humidity"], "%")

            except :
                st.error("❌ Unable to fetch weather. Check internet or city name.")
        else:
            st.warning("Please enter a city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.show_logout_msg = True
        st.rerun()


# App Flow Control
if st.session_state.logged_in:
    weather_page()
else:
    login_page()
