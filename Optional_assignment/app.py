import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Initialize Groq LLM (LangChain 1.2.0)
# -----------------------------
llm = init_chat_model(
    model="llama-3.1-8b-instant",
    provider="groq",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

output_parser = StrOutputParser()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="NLQ to MySQL (LangChain 1.2.0)", layout="wide")

st.title("💬 Natural Language to MySQL Query")
st.write("Ask questions in plain English and query your MySQL database.")

# -----------------------------
# Database Connection
# -----------------------------
st.sidebar.header("🔐 Database Connection")

db_host = st.sidebar.text_input("Host", "localhost")
db_user = st.sidebar.text_input("User", "root")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database Name")

connect_btn = st.sidebar.button("Connect")

if "db_connected" not in st.session_state:
    st.session_state.db_connected = False

if connect_btn:
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        st.session_state.conn = conn
        st.session_state.db_connected = True
        st.sidebar.success("Connected successfully!")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")

# -----------------------------
# Main App
# -----------------------------
if st.session_state.db_connected:

    st.subheader("📌 Ask Your Question")
    user_question = st.text_area(
        "Example: Show total sales per product",
        height=100
    )

    ask_btn = st.button("Generate & Run Query")

    if ask_btn and user_question.strip():

        cursor = st.session_state.conn.cursor()

        # Fetch schema
        cursor.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = %s
        """, (db_name,))
        schema_info = cursor.fetchall()

        schema_text = ""
        for table, column in schema_info:
            schema_text += f"Table: {table}, Column: {column}\n"

        # -----------------------------
        # SQL Generation Prompt
        # -----------------------------
        sql_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert MySQL developer. "
             "Generate ONLY a valid SELECT query. "
             "Never use INSERT, UPDATE, DELETE, DROP."),
            ("human",
             "Schema:\n{schema}\n\n"
             "Question:\n{question}")
        ])

        sql_chain = sql_prompt | llm | output_parser

        with st.spinner("Generating SQL using LangChain 1.2.0..."):
            sql_query = sql_chain.invoke({
                "schema": schema_text,
                "question": user_question
            }).strip()

        # Safety check
        if not sql_query.lower().startswith("select"):
            st.error("❌ Only SELECT queries are allowed.")
            st.code(sql_query)
        else:
            st.subheader("🧾 Generated SQL Query")
            st.code(sql_query, language="sql")

            try:
                df = pd.read_sql(sql_query, st.session_state.conn)

                st.subheader("📊 Query Result")
                st.dataframe(df)

                # -----------------------------
                # Explanation Prompt
                # -----------------------------
                explain_prompt = ChatPromptTemplate.from_messages([
                    ("system", "Explain SQL queries in very simple English."),
                    ("human", "{sql}")
                ])

                explain_chain = explain_prompt | llm | output_parser

                explanation = explain_chain.invoke({
                    "sql": sql_query
                })

                st.subheader("📝 Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"❌ Query execution failed: {e}")

else:
    st.info("👈 Please connect to a MySQL database from the sidebar.")
