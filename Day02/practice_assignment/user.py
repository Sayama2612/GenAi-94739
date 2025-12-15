import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CSV Explorer", page_icon="📊")

USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["username", "filename", "upload_time"]).to_csv(HISTORY_FILE, index=False)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# Helper Funstion
def load_users():
    return pd.read_csv(USERS_FILE)

def save_user(username, password):
    users = load_users()
    users.loc[len(users)] = [username, password]
    users.to_csv(USERS_FILE, index=False)

def authenticate(username, password):
    users = load_users()
    return not users[(users.username == username) & (users.password == password)].empty

def save_history(username, filename):
    history = pd.read_csv(HISTORY_FILE)
    history.loc[len(history)] = [username, filename, datetime.now()]
    history.to_csv(HISTORY_FILE, index=False)

# Sidebar Menu
st.sidebar.title("📌 Menu")

if not st.session_state.authenticated:
    menu = st.sidebar.radio("Navigate", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigate", ["Explore CSV", "See History", "Logout"])

# Home Page
if menu == "Home":
    st.title("🏠 Home")
    st.write("Welcome to the CSV Explorer App")

# Register Page
if menu == "Register":
    st.title("📝 Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        register_btn = st.form_submit_button("Register")
        
    if register_btn:
        users = load_users()
        if username in users.username.values:
            st.error("User already exists")
        else:
            save_user(username, password)
            st.success("Registration successful")


# Login Page
if menu == "Login":
    st.title("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        
    if login_btn:
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# Explore CSV
if menu == "Explore CSV":
    st.title("📂 Upload & Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        save_history(st.session_state.username, uploaded_file.name)
        st.success("File uploaded and history saved")

# See History
if menu == "See History":
    st.title("📜 Upload History")

    history = pd.read_csv(HISTORY_FILE)
    user_history = history[history.username == st.session_state.username]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

# Logout
if menu == "Logout":
    st.session_state.authenticated = False
    st.session_state.username = None
    st.success("Thanks for using the app 😊")
    
