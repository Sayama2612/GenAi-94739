import streamlit as st
import pandas as pd
from pandasql import sqldf

if "page" not in st.session_state:
    st.session_state.page = "Upload"

if 'result' not in st.session_state:
    st.session_state.result = None
    
if st.session_state.page == "Upload":

    st.title("Upload CSV & Run SQL Query")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("CSV Preview")
        st.dataframe(df)

        st.markdown("Write SQL Query")
        st.info("Table name is **data**")

        query = st.text_area(
            "Example: SELECT * FROM df WHERE column_name > 100"
        )

        if st.button("Execute Query"):
            try:
                st.session_state.result = sqldf(query, {"data": df})
                st.session_state.page = "Result"
                
            except Exception as e:
                st.error(f"Error: {e}")


elif st.session_state.page == "Result":

    st.title("Query Result")

    st.dataframe(st.session_state.result)

    if st.button("Back"):
        st.session_state.page = "Upload"
        
