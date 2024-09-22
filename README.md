# Project overview and setup instructions 
# QA Bot Project

## Overview
This is a QA bot project that allows users to upload documents and ask questions based on the content of those documents. It utilizes a Retrieval-Augmented Generation (RAG) architecture with Pinecone for document retrieval and Cohere for generating answers.

## Features
- Upload PDF/Text files.
- Ask questions and get answers in real-time.
- Modular, scalable, and containerized using Docker.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/QA_Bot_Project.git
   cd QA_Bot_Project

2. Install dependencies:
    pip install -r requirements.txt

3. Set up environment variables:
    cp .env.example .env

4. Run the backend:
    uvicorn backend.app:app --reload

5. Run the frontend:
    cd frontend
    streamlit run app.py

6. Run using Docker:
    docker build -t qa-bot .
    docker run -p 8000:8000 qa-bot

# Usage
Upload a document through the frontend.
Ask questions based on the uploaded document.
Refer 'docs' folder for project documentation.
