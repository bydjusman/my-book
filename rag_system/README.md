# Physical AI & Humanoid Robotics RAG System

This is a Retrieval-Augmented Generation (RAG) system designed to answer questions about the Physical AI & Humanoid Robotics textbook. The system combines document retrieval with language model generation to provide accurate, context-aware responses based on the textbook content.

## Features

- **Question Answering**: Ask questions about the textbook content and receive relevant answers
- **Document Upload**: Upload additional documents to enhance the knowledge base
- **Source Tracking**: Responses include information about which documents the information came from
- **RESTful API**: Easy-to-use API for integration with other applications
- **Configurable**: Environment variables for customization

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Navigate to the rag_system directory:
```bash
cd rag_system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

The system can be configured using environment variables:

- `RAG_HOST`: Host address for the API server (default: 0.0.0.0)
- `RAG_PORT`: Port for the API server (default: 8000)
- `RAG_DEBUG`: Enable debug mode (default: False)
- `RAG_CHUNK_SIZE`: Size of text chunks for vector storage (default: 1000)
- `RAG_SEARCH_K`: Number of documents to retrieve for each query (default: 4)

## Usage

### Starting the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
- `GET /health` - Check the health status of the RAG system

#### Ask a Question
- `POST /ask` - Ask a question about the textbook
  - Query parameter: `question` (required) - The question to ask
  - Query parameter: `max_tokens` (optional) - Maximum number of tokens in the response (default: 200)
  - Query parameter: `temperature` (optional) - Temperature for response generation (default: 0.7)

  Example:
  ```
  POST /ask?question=What%20is%20ROS%202?
  ```

#### Upload Document
- `POST /upload_document` - Upload additional documents to the knowledge base
  - Form field: `file` - The document to upload (supports .txt, .md, .markdown)

### Example Usage

#### Using curl:

```bash
# Ask a question
curl -X POST "http://localhost:8000/ask?question=Explain%20digital%20twins%20in%20robotics"

# Upload a document
curl -X POST "http://localhost:8000/upload_document" -F "file=@path/to/your/document.md"
```

## System Architecture

The RAG system consists of several components:

1. **Data Loader**: Loads and preprocesses the textbook content
2. **Vector Store**: Stores document embeddings for fast retrieval
3. **Embedding Model**: Converts text to vector representations
4. **Language Model**: Generates responses based on retrieved documents
5. **API Layer**: Provides RESTful endpoints for interaction

## How It Works

1. **Initialization**: During startup, the system loads all textbook content, splits it into chunks, and creates embeddings
2. **Query Processing**: When a question is asked, the system:
   - Converts the question to an embedding
   - Finds the most relevant document chunks using the vector store
   - Combines the question with relevant context
   - Generates a response using the language model
3. **Response**: The system returns the generated answer along with source information

## Customization

To customize the system for your own content:

1. Modify the file paths in `data_loader.py` to point to your documents
2. Adjust the configuration parameters in `config.py` as needed
3. Change the embedding or language models in the configuration

## Troubleshooting

- If you encounter memory issues, try reducing the `max_new_tokens` parameter or using a smaller language model
- If responses are too generic, try adjusting the `temperature` parameter
- If the system can't find relevant information, verify that your documents were loaded correctly

## Performance Considerations

- The initial startup may take some time as the system loads and embeds all documents
- Response time depends on the complexity of the question and the size of the knowledge base
- For large document collections, consider using more powerful embedding or language models

## Security

- In production, ensure proper authentication and rate limiting
- Validate and sanitize all user inputs
- Consider using HTTPS for API communication
- Review the CORS settings in production environments