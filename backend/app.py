import os
import pinecone
import cohere
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from utils import process_document, retrieve_answer
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load API keys from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize Pinecone and Cohere clients
pinecone.init(api_key=PINECONE_API_KEY)
co = cohere.Client(api_key=COHERE_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model for query requests
class Query(BaseModel):
    question: str

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload and process a document (PDF or text).
    The document is processed into chunks, and embeddings are stored in Pinecone.
    """
    try:
        # Read and process the document
        contents = await file.read()
        logger.info(f"Processing document: {file.filename}")
        
        response = process_document(contents, PINECONE_API_KEY)
        return JSONResponse(status_code=200, content={"status": "success", "response": response})
    
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail="Failed to process document.")

@app.post("/answer/")
async def get_answer(query: Query):
    """
    Endpoint to retrieve an answer for a given question.
    Uses Pinecone to retrieve relevant document sections and Cohere to generate an answer.
    """
    try:
        logger.info(f"Received question: {query.question}")
        
        # Retrieve answer using Pinecone and Cohere
        answer = retrieve_answer(query.question, PINECONE_API_KEY, COHERE_API_KEY)
        logger.info(f"Generated answer: {answer}")
        
        return JSONResponse(status_code=200, content={"answer": answer})
    
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate answer.")

@app.get("/")
def health_check():
    """
    Simple health check endpoint to ensure the API is running.
    """
    return {"status": "API is running successfully"}

# Error handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )
