import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API base URL (backend server)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Streamlit app configuration
st.set_page_config(page_title="QA Bot", page_icon="🤖", layout="wide")

# Title and description
st.title("Document-Based Question Answering Bot")
st.write("Upload a document and ask questions based on its content.")

# Sidebar for uploading documents
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt"])

if uploaded_file:
    # Show filename and initiate document processing
    st.sidebar.write(f"Processing file: {uploaded_file.name}")

    # Send file to backend for processing
    try:
        with st.spinner('Uploading and processing document...'):
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(f"{API_URL}/upload/", files=files)
            if response.status_code == 200:
                st.sidebar.success("Document uploaded and processed successfully.")
            else:
                st.sidebar.error(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.sidebar.error(f"An error occurred while uploading: {e}")

# Section for question input
st.header("Ask Questions")
question = st.text_input("Type your question here:")

if st.button("Get Answer") and question:
    try:
        with st.spinner('Retrieving answer...'):
            # Send question to backend for answer retrieval
            data = {"question": question}
            response = requests.post(f"{API_URL}/answer/", json=data)
            if response.status_code == 200:
                answer = response.json().get("answer")
                st.success(f"Answer: {answer}")
            else:
                st.error(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Optional: Display uploaded document (PDF preview for PDF files)
if uploaded_file and uploaded_file.name.endswith(".pdf"):
    st.sidebar.subheader("Document Preview")
    st.sidebar.write("This is a preview of the uploaded PDF.")
    st.sidebar.download_button(
        label="Download PDF",
        data=uploaded_file,
        file_name=uploaded_file.name,
    )

# Footer
st.markdown("""
    ---
    **Note:** The bot may take a few seconds to retrieve answers, especially for large documents.
    """)
