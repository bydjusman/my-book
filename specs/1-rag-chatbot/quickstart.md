# Quickstart Guide: Physical AI & Humanoid Robotics RAG Chatbot

**Created**: 2025-12-18
**Feature**: RAG Chatbot for Physical AI & Humanoid Robotics textbook

## Overview

This guide provides a quick introduction to setting up and using the RAG chatbot for the "Physical AI & Humanoid Robotics" textbook. The chatbot is designed to answer student questions using only content from the textbook.

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Access to OpenAI API key or local LLM (Ollama)
- Textbook content in Markdown format

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
TEXTBOOK_PATH=path/to/textbook/markdown/files
VECTOR_DB_PATH=path/to/vector/database
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo  # or local model identifier
```

### 4. Process Textbook Content

Run the document processing pipeline to convert textbook markdown files into searchable chunks:

```bash
python scripts/process_textbook.py
```

This will:
- Parse all textbook markdown files
- Split content into semantic chunks
- Generate embeddings for each chunk
- Store embeddings in the vector database

## Usage

### 1. Start the Backend API

```bash
uvicorn main:app --reload --port 8000
```

### 2. Test the API

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain ROS 2 node communication"
  }'
```

### 3. Integrate with Docusaurus

Add the chatbot component to your Docusaurus site by including the React component in your layout.

## API Endpoints

### Chat Endpoint
- **URL**: `POST /api/chat`
- **Description**: Process a student question and return a textbook-based answer
- **Request**: `{"question": "string", "session_id": "optional uuid"}`
- **Response**: `{"answer": "string", "sources": [...], "question_id": "uuid", "confidence": "float"}`

### Validation Endpoint
- **URL**: `POST /api/validate`
- **Description**: Check if a question is within textbook scope
- **Request**: `{"question": "string"}`
- **Response**: `{"is_valid": "boolean", "message": "string", "suggested_topics": ["string"]}`

### Health Check
- **URL**: `GET /api/health`
- **Description**: Check service health status
- **Response**: `{"status": "healthy", "version": "string", "timestamp": "datetime"}`

## Example Usage

### Asking a Question
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"question": "How does Gazebo simulate physics for humanoid robots?"}
)

print(response.json()["answer"])
```

### Validating a Question
```python
import requests

response = requests.post(
    "http://localhost:8000/api/validate",
    json={"question": "What is quantum computing?"}
)

if not response.json()["is_valid"]:
    print(response.json()["message"])  # "This topic is not covered in the book"
```

## Configuration

### Adjusting Chunk Size
Modify the chunk size in the processing script:
```python
CHUNK_SIZE = 512  # Number of characters per chunk
CHUNK_OVERLAP = 64  # Overlap between chunks
```

### Changing Embedding Model
Update the model in the `.env` file:
```env
EMBEDDING_MODEL=all-mpnet-base-v2  # Alternative model
```

### Using Local LLM
To use a local model with Ollama:
```env
LLM_MODEL=ollama/llama3  # Use local Ollama model
```

## Troubleshooting

### Common Issues

1. **Slow Response Times**
   - Check if the vector database is properly indexed
   - Verify embedding model is cached locally
   - Ensure sufficient system resources

2. **"This topic is not covered in the book" for Valid Questions**
   - Verify the question matches textbook terminology
   - Check if the textbook content was properly processed
   - Adjust similarity threshold in the retrieval configuration

3. **API Connection Errors**
   - Verify the backend service is running
   - Check firewall and network settings
   - Confirm the correct API endpoint URL

## Next Steps

1. Customize the chatbot UI to match your documentation site
2. Fine-tune the retrieval parameters for optimal results
3. Add analytics to track common questions and improve content
4. Implement user feedback mechanisms to improve responses