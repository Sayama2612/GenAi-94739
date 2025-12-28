import os
import streamlit as st
from datetime import datetime

# LangChain (NEW imports)
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------
# Configuration
# -----------------------------
RESUME_DIR = "resumes"
CHROMA_DIR = "chroma_db"

os.makedirs(RESUME_DIR, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Vector Store
# -----------------------------
def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

# -----------------------------
# Save uploaded file & return path
# -----------------------------
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(RESUME_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# -----------------------------
# Add / Update Resume (ONE FILE)
# -----------------------------
def add_resume(uploaded_file):
    file_path = save_uploaded_file(uploaded_file)

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    for doc in chunks:
        doc.metadata["resume_name"] = uploaded_file.name
        doc.metadata["uploaded_at"] = str(datetime.now())

    vectordb = get_vectorstore()

    # Delete old resume embeddings (UPDATE case)
    vectordb._collection.delete(
        where={"resume_name": uploaded_file.name}
    )

    vectordb.add_documents(chunks)
    vectordb.persist()

# -----------------------------
# Delete Resume
# -----------------------------
def delete_resume(resume_name):
    vectordb = get_vectorstore()
    vectordb._collection.delete(
        where={"resume_name": resume_name}
    )

    file_path = os.path.join(RESUME_DIR, resume_name)
    if os.path.exists(file_path):
        os.remove(file_path)

# -----------------------------
# List Resumes
# -----------------------------
def list_resumes():
    return os.listdir(RESUME_DIR)

# -----------------------------
# Shortlist Resumes
# -----------------------------
def shortlist_resumes(job_desc, top_k):
    vectordb = get_vectorstore()

    results = vectordb.similarity_search(job_desc, k=top_k)

    shortlisted = []
    seen = set()

    for doc in results:
        name = doc.metadata.get("resume_name")
        if name not in seen:
            shortlisted.append(name)
            seen.add(name)

    return shortlisted

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config("AI Resume Shortlisting", layout="wide")
st.title("📄 AI-Enabled Resume Shortlisting (RAG)")

tab1, tab2, tab3 = st.tabs(
    ["📤 Upload Resumes", "📋 Manage Resumes", "🎯 Shortlist"]
)

# -----------------------------
# Upload Multiple Resumes
# -----------------------------
with tab1:
    st.subheader("Upload Resume PDFs")

    uploaded_files = st.file_uploader(
        "Select PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                add_resume(file)

        st.success(f"{len(uploaded_files)} resume(s) uploaded successfully")

# -----------------------------
# Manage Resumes
# -----------------------------
with tab2:
    st.subheader("Stored Resumes")

    resumes = list_resumes()

    if not resumes:
        st.info("No resumes uploaded yet.")
    else:
        for resume in resumes:
            col1, col2 = st.columns([4, 1])
            col1.write(resume)
            if col2.button("Delete", key=resume):
                delete_resume(resume)
                st.success(f"{resume} deleted")
                st.rerun()

# -----------------------------
# Shortlist Resumes
# -----------------------------
with tab3:
    st.subheader("Shortlist Resumes for Job Description")

    job_desc = st.text_area(
        "Enter Job Description",
        height=200
    )

    top_k = st.number_input(
        "Number of resumes to shortlist",
        min_value=1,
        max_value=10,
        value=3
    )

    if st.button("Shortlist"):
        if not job_desc.strip():
            st.warning("Please enter job description.")
        else:
            results = shortlist_resumes(job_desc, top_k)

            if not results:
                st.info("No matching resumes found.")
            else:
                st.success("Top Matching Resumes:")
                for i, name in enumerate(results, 1):
                    st.write(f"{i}. {name}")
