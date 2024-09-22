import os
import pinecone
import cohere
import logging
from PyPDF2 import PdfReader
from typing import List, Tuple

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Pinecone and Cohere clients
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

# Constants
INDEX_NAME = "your-index-name"  # Change to your index name

def process_document(contents: bytes, api_key: str) -> str:
    """
    Process the uploaded document, extract text, and store embeddings in Pinecone.

    Args:
        contents (bytes): The contents of the uploaded file.
        api_key (str): Pinecone API key for initialization.

    Returns:
        str: A message indicating the success of the operation.
    """
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(contents)
        logger.info("Extracted text from document.")

        # Split text into chunks
        chunks = split_text_into_chunks(text)
        logger.info(f"Split text into {len(chunks)} chunks.")

        # Generate embeddings and store in Pinecone
        store_embeddings_in_pinecone(chunks)
        logger.info("Stored embeddings in Pinecone.")

        return "Document processed and embeddings stored successfully."

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return f"Failed to process document: {str(e)}"

def extract_text_from_pdf(contents: bytes) -> str:
    """
    Extract text from a PDF file.

    Args:
        contents (bytes): The contents of the PDF file.

    Returns:
        str: The extracted text.
    """
    pdf_reader = PdfReader(contents)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split the text into manageable chunks.

    Args:
        text (str): The text to split.
        chunk_size (int): The size of each chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def store_embeddings_in_pinecone(chunks: List[str]):
    """
    Store text embeddings in Pinecone.

    Args:
        chunks (List[str]): List of text chunks to embed and store.
    """
    # Ensure the index exists
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME)
    
    index = pinecone.Index(INDEX_NAME)
    
    # Generate embeddings using Cohere
    embeddings = cohere_client.embed(texts=chunks).embeddings
    logger.info("Generated embeddings using Cohere.")

    # Prepare data for Pinecone
    vectors = [(str(i), embeddings[i]) for i in range(len(embeddings))]
    
    # Upsert vectors into Pinecone
    index.upsert(vectors=vectors)
    logger.info(f"Upserted {len(vectors)} vectors into Pinecone.")

def retrieve_answer(question: str, pinecone_api_key: str, cohere_api_key: str) -> str:
    """
    Retrieve the answer to a question based on the stored embeddings in Pinecone.

    Args:
        question (str): The question to answer.

    Returns:
        str: The generated answer.
    """
    # Get embedding for the question
    question_embedding = cohere_client.embed(texts=[question]).embeddings[0]
    logger.info("Generated question embedding.")

    # Query Pinecone for the most relevant documents
    index = pinecone.Index(INDEX_NAME)
    query_response = index.query(queries=[question_embedding], top_k=3)
    logger.info("Retrieved relevant document segments from Pinecone.")

    # Extract the most relevant chunks
    relevant_chunks = [match['id'] for match in query_response['matches']]
    
    # Generate answer using the relevant chunks
    answer = cohere_client.generate(
        prompt=f"Answer the question '{question}' using the following context: {relevant_chunks}",
        max_tokens=100,
        temperature=0.5
    ).generations[0].text.strip()

    return answer

