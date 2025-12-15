import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Weather App", page_icon="🌦️")

# ---------------------------
# Session State Initialization
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False


# ---------------------------
# Login Page
# ---------------------------
def login_page():
    st.title("🔐 Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if username == password and username != "":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.logged_out = False
            st.session_state.show_login_success = True
            st.rerun()
        else:
            st.error("Invalid credentials (Username must match Password)")


# ---------------------------
# Weather Page
# ---------------------------
def weather_page():
    if st.session_state.get("show_login_success"):
        st.success("Login successful!")
        st.session_state.show_login_success = False
        
    st.title("🌦️ Weather Information")
    st.write(f"Welcome, **{st.session_state.username}** 👋")

    load_dotenv() 
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
            response = requests.get(url)
            weather = response.json()
            
            st.subheader(f"Weather in {city}")
            st.write("🌡️ Temperature: ",weather["main"]["temp"],"°C")
            st.write("☁️ Condition: ", weather["weather"][0]["description"].title())
            st.write("💨 Wind Speed: ",weather["wind"]["speed"] ,"km/h")
            st.write("💧 Humidity: ",weather["main"]["humidity"],"%")
        else:
            st.warning("Please enter a city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logged_out = True


# ---------------------------
# Thank You Page
# ---------------------------
def logout_page():
    st.title("🙏 Thank You")
    st.write("You have successfully logged out.")
    st.write("Have a great day! 😊")


# ---------------------------
# App Flow Control
# ---------------------------
if st.session_state.logged_out:
    logout_page()
elif st.session_state.logged_in:
    weather_page()
else:
    login_page()
