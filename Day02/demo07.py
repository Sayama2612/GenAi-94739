import streamlit as st

with st.form(key="reg_form"):
    st.header("Your details")
    
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.slider("Age", min_value=18, max_value=100, value=25)
    submit_button = st.form_submit_button(label="Register")
    
if submit_button:
    st.success(f"Thank you {first_name} {last_name} for registering! You are {age} years old.")    
    