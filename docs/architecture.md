# Explanation of model architecture 
# Model Architecture

## Overview
The QA Bot uses a Retrieval-Augmented Generation (RAG) architecture, combining:
1. **Vector-based retrieval**: To find relevant document sections using Pinecone.
2. **Generative model**: To generate answers based on retrieved sections using the Cohere API.

### Components
1. **Document Processing**:
   - PDF/Text files are uploaded and converted into text.
   - Text is split into chunks, and embeddings are created for each chunk using a transformer model.
   - Embeddings are stored in Pinecone for fast retrieval.

2. **Query Processing**:
   - User submits a question.
   - The question is converted into an embedding, and the most relevant chunks are retrieved.
   - Retrieved chunks are passed to the generative model to generate an answer.

### Technology Stack
- **Pinecone**: Vector-based document storage and retrieval.
- **Cohere API**: Used to generate natural language responses.
- **FastAPI**: Backend service for document processing and querying.
- **Streamlit/Gradio**: Frontend interface for user interaction.
