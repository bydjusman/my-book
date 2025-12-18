# Physical AI & Humanoid Robotics RAG Chatbot System

This directory contains the RAG (Retrieval-Augmented Generation) chatbot system that answers questions from the "Physical AI & Humanoid Robotics" textbook.

## System Architecture

The system consists of:
- **Ingestion Pipeline**: Processes textbook content from `/docs` and `/content` directories
- **Vector Database**: Stores embeddings for efficient retrieval
- **Query System**: Retrieves relevant content and generates answers
- **API Layer**: FastAPI endpoints for web interface
- **Web Chat Interface**: React component integrated into Docusaurus

## Setup Instructions

### 1. Install Dependencies

```bash
cd rag_system
pip install -r requirements.txt
```

### 2. Process Textbook Content

Run the ingestion pipeline to process all markdown files from `/docs` and `/content`:

```bash
python ingest.py
```

This will:
- Find all `.md` files in `/docs` and `/content` directories
- Split content into chunks (~500 tokens with 50-token overlap)
- Generate embeddings using Sentence Transformers
- Store vectors in ChromaDB at `./vector_db`

### 3. Start the API Server

```bash
uvicorn api.chat:app --host 0.0.0.0 --port 8000
```

Or run directly:
```bash
python api/chat.py
```

The API will be available at `http://localhost:8000`

### 4. Start the Docusaurus Website

In a new terminal, from the project root:

```bash
npm install
npm start
```

The website will be available at `http://localhost:3000`

## Using the Chatbot

1. Navigate to any page on the Docusaurus website
2. Look for the floating "🤖 Ask the Book" button at the bottom-right
3. Click the button to open the chat interface
4. Type your question about the textbook content
5. The chatbot will respond based only on information from the textbook

## API Endpoints

- `POST /chat`: Send a message and receive a response
- `GET /`: API information
- `GET /health`: Health check

Example API request:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain ROS 2 concepts"}'
```

## Constitution Compliance

The chatbot strictly follows these rules:
- Answers only from textbook content
- Responds with "This topic is not covered in the book" when information is missing
- Uses simple, beginner-friendly English
- Provides step-by-step explanations
- Includes humanoid robotics examples when relevant
- No hallucinations or external information