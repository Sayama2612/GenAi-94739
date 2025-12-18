import streamlit as st
import os
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# ----------------------------------
# Load environment variables
# ----------------------------------

load_dotenv()

# ----------------------------------
# Session state
# ----------------------------------

if "show_preview" not in st.session_state:
        st.session_state.show_preview = False
        
# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(page_title="CSV SQL Chatbot", page_icon="📊")
st.title("📊 CSV SQL Chatbot (Groq + LLaMA)")

# ----------------------------------
# Initialize LLM (Same as Code 1)
# ----------------------------------

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------------
# File Upload
# ----------------------------------

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ----------------------------------
    # Data Preview
    # ----------------------------------

    if st.button("📌 Data Preview"):
        st.session_state.show_preview = not st.session_state.show_preview

    if st.session_state.show_preview:
        st.dataframe(df.head())


    # ----------------------------------
    # Schema
    # ----------------------------------
    
    st.subheader("🧬 Schema")
    st.write(df.dtypes)

    # ----------------------------------
    # User Question
    # ----------------------------------
    
    user_question = st.text_input("Ask anything about this CSV")

    if user_question:
        
        # ----------------------------------
        # Prompt (Same style as Code 1)
        # ----------------------------------
        
        llm_input = f"""
            You are a SQLite expert developer with 10 years of experience.
            
            Table Name: data
            Table Schema: {df.dtypes}
            Question: {user_question}
            Instruction:
                Write a SQL query for the above question.
                Generate SQL query only in plain text format and nothing else.
                If you cannot generate the query, then output "Error"
        """

        # ----------------------------------
        # LLM Call
        # ----------------------------------
        
        result = llm.invoke(llm_input)
        sql_query = result.content.strip()

        st.subheader("🧾 Generated SQL")
        st.code(sql_query, language="sql")

        # ----------------------------------
        # Execute SQL
        # ----------------------------------
        
        if sql_query.lower() != "error":
            try:
                result_df = sqldf(sql_query, {"data": df})

                st.subheader("📈 Query Result")
                st.dataframe(result_df)

                # ----------------------------------
                # Explain Result (Simple English)
                # ----------------------------------
                
                explain_prompt = f"""
                    Explain the following result in very simple English.

                    User Question:
                    {user_question}

                    Query Result:
                    {result_df.head(10).to_string(index=False)}
                """

                explanation = llm.invoke(explain_prompt)

                st.subheader("🗣️ Explanation")
                st.write(explanation.content)

            except Exception as e:
                st.error("❌ Error executing SQL")
                st.exception(e)
        else:
            st.error("❌ LLM could not generate SQL")
                