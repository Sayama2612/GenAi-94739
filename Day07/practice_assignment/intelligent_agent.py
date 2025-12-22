'''Q1:
Design and implement a Streamlit-based application consisting of two intelligent agents:
(1) a CSV Question Answering Agent that allows users to upload a CSV file, display its schema, and answer questions by converting them into SQL queries using pandasql; and
(2) a Web Scraping Agent that retrieves sunbeam internship and batch information from the Sunbeam website and answers user queries.
The application should maintain complete chat history.
All responses must be explained in simple English.'''

import streamlit as st
import os
import pandas as pd
from pandasql import sqldf
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent #type: ignore
from langchain.tools import tool

# Selenium 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()

st.set_page_config(page_title="Multi-Agent App", page_icon="🤖")
st.title("🤖 Intelligent Agent Application")
st.write(
    "This application uses two intelligent agents:\n"
    
)

#csv
st.sidebar.header("📂 CSV Agent")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("CSV uploaded successfully!")

    st.sidebar.subheader("📊 CSV Schema")
    schema_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })
    st.sidebar.dataframe(schema_df)


@tool
def csv_sql_agent(sql_query: str):
    """
    Executes SQL queries on uploaded CSV using pandasql.
    The table name is 'df'.
    """
    if df is None:
        return "No CSV file uploaded. Please upload a CSV first."

    try:
        result = sqldf(sql_query, {"df": df})
        return result.to_string(index=False)
    except Exception:
        return "ERROR. Please ask a simple question."


@tool
def get_sunbeam_internship_info():
    """
    Scrapes Sunbeam internship batch information using Selenium.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    info = []

    try:
        driver.get("https://sunbeaminfo.in/internship")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))

        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 7:
                info.append(
                    f"Batch {cols[1].text} starts on {cols[3].text}, "
                    f"ends on {cols[4].text}, Fees: {cols[6].text}"
                )
    except:
        driver.quit()
        return "Error fetching Sunbeam internship data."

    driver.quit()
    return "\n".join(info)


llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = create_agent(
    model=llm,
    tools=[csv_sql_agent, get_sunbeam_internship_info],
    system_prompt=(
        "You are a helpful assistant."
        "If the user asks about CSV data, convert the question into a SQL query on table df."
        "If the user asks about Sunbeam internships, use the web scraping tool."
        "Always explain the final answer in simple English."
    )
)

#chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#input
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    result = agent.invoke({
        "messages": st.session_state.messages
    })

    response = result["messages"][-1].content

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)