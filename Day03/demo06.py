import streamlit as st
import pandas as pd

name = st.text_input("Enter your name: ")
message = st.text_area("Enter your message :", height=100)
uploaded_file = st.file_uploader("Choose a file", type= ["txt","pdf","csv"])
model = st.selectbox("Choose AI model :", ["GPT-4", "Llama 3", "Gemini", "Claude"])

if name:
    st.write(f"Hello : {name} !!")
    
st.markdown("**This is bold text** and *this is italic*")

df = pd.DataFrame({'A': [1,2,3], "B": [4,5,6]})
st.dataframe(df)

config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500}
st.json(config)