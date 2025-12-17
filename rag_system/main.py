from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
import tempfile
import shutil
from typing import List, Optional
import logging

# Import our custom modules
from config import get_env_config
from data_loader import TextbookDataLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG System",
    description="A Retrieval-Augmented Generation system for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for the RAG system
vectorstore = None
qa_chain = None
documents = []

# Initialize the RAG system
def initialize_rag_system():
    global vectorstore, qa_chain

    try:
        logger.info("Initializing RAG system...")

        # Get configuration
        config = get_env_config()

        # Initialize embeddings model
        embeddings = SentenceTransformerEmbeddings(
            model_name=config.embedding_model
        )

        # Load documents from the textbook using our data loader
        loader = TextbookDataLoader()
        textbook_content = loader.load_and_validate()

        if textbook_content:
            # Split documents using config parameters
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                length_function=len,
            )
            docs = text_splitter.split_text(textbook_content)

            # Create vector store
            vectorstore = Chroma.from_texts(
                texts=docs,
                embedding=embeddings,
                persist_directory=config.vector_db_persist_dir
            )

            # Initialize a lightweight model for question answering
            # Using a smaller model for faster responses
            tokenizer = AutoTokenizer.from_pretrained(config.llm_model_name)
            model = AutoModelForCausalLM.from_pretrained(config.llm_model_name)

            # Create Hugging Face pipeline
            hf_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                pad_token_id=tokenizer.eos_token_id
            )

            llm = HuggingFacePipeline(pipeline=hf_pipeline)

            # Create QA chain with config parameters
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(
                    search_kwargs={"k": config.search_k}  # Retrieve top k relevant chunks
                ),
                return_source_documents=True
            )

            logger.info("RAG system initialized successfully")
        else:
            logger.warning("No textbook content found to initialize RAG system")

    except Exception as e:
        logger.error(f"Error initializing RAG system: {str(e)}")
        raise


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system when the application starts"""
    initialize_rag_system()

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {
        "message": "Physical AI & Humanoid Robotics RAG System",
        "status": "running",
        "endpoints": {
            "/ask": "Ask a question about the textbook",
            "/health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "vectorstore": "initialized" if vectorstore is not None else "not initialized",
        "qa_chain": "initialized" if qa_chain is not None else "not initialized"
    }

@app.post("/ask")
async def ask_question(
    question: str = Query(..., description="The question to ask about the textbook"),
    max_tokens: int = Query(200, description="Maximum number of tokens in the response"),
    temperature: float = Query(0.7, description="Temperature for response generation")
):
    """
    Ask a question about the Physical AI & Humanoid Robotics textbook
    """
    global qa_chain

    if qa_chain is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")

    try:
        logger.info(f"Processing question: {question}")

        # Use the QA chain to get an answer
        result = qa_chain({"query": question})

        # Extract the answer and source documents
        answer = result.get("result", "I couldn't find a specific answer to your question.")
        source_docs = result.get("source_documents", [])

        # Extract relevant source information
        sources = []
        for doc in source_docs[:2]:  # Limit to first 2 sources for brevity
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            sources.append({
                "preview": content_preview,
                "metadata": doc.metadata
            })

        response = {
            "question": question,
            "answer": answer,
            "sources": sources,
            "status": "success"
        }

        logger.info("Question processed successfully")
        return response

    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload additional documents to enhance the knowledge base
    """
    global vectorstore, qa_chain

    if vectorstore is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")

    try:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        # Process the uploaded file based on its type
        content = ""
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext == ".txt":
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        elif file_ext in [".md", ".markdown"]:
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # For other file types, we would need additional processing
            # This is a simplified implementation
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")

        # Split the content and add to vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        docs = text_splitter.split_text(content)

        # Add new documents to the existing vector store
        vectorstore.add_texts(docs)

        # Reinitialize the QA chain with the updated vector store
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        # For simplicity, we're using a basic LLM here
        # In a real implementation, you might want to maintain the original LLM
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=100,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        llm = HuggingFacePipeline(pipeline=hf_pipeline)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return {
            "status": "success",
            "message": f"Document '{file.filename}' uploaded and integrated successfully",
            "chunks_added": len(docs)
        }

    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        # Clean up the temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)