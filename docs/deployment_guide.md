# Instructions for deploying the app 
# Deployment Guide

## Prerequisites
- Python 3.8+
- Docker
- Pinecone API key
- Cohere API key (or alternative)
- PDF/text files to upload

## Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/QA_Bot_Project.git
   cd QA_Bot_Project

2. Set up environment variables:
    Create a .env file in the root directory:
    
    PINECONE_API_KEY=your_pinecone_api_key
    COHERE_API_KEY=your_cohere_api_key


3. Install dependencies:
    pip install -r requirements.txt


4. Run the backend:
    uvicorn backend.app:app --reload


5. Run the frontend:
    cd frontend
    streamlit run app.py 


6. Run using Docker: Build and run the Docker container:
    docker build -t qa-bot .
    docker run -p 8000:8000 qa-bot


7. Access the frontend:
    Open http://localhost:8501 in your browser for the Streamlit app.


