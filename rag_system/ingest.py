"""
Ingestion module for RAG chatbot.
Recursively reads all .md files from /docs and /content,
splits text into chunks, generates embeddings, and stores in vector database.
"""
import os
import glob
from typing import List
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain_community.vectorstores import Chroma
except ImportError:
    logger.error("Required packages not found. Install with: pip install -r requirements.txt")
    raise


def get_all_md_files(base_path: str = ".") -> List[str]:
    """
    Recursively find all .md files in /docs and /content directories.

    Args:
        base_path: Base path to search from (default: current directory)

    Returns:
        List of paths to .md files
    """
    md_files = []

    # Look for .md files in docs directory
    docs_pattern = os.path.join(base_path, "docs", "**", "*.md")
    docs_files = glob.glob(docs_pattern, recursive=True)
    md_files.extend(docs_files)

    # Look for .md files in content directory
    content_pattern = os.path.join(base_path, "content", "**", "*.md")
    content_files = glob.glob(content_pattern, recursive=True)
    md_files.extend(content_files)

    logger.info(f"Found {len(md_files)} markdown files")
    for file in md_files:
        logger.info(f"  - {file}")

    return md_files


def read_md_files(file_paths: List[str]) -> List[dict]:
    """
    Read content from all markdown files.

    Args:
        file_paths: List of paths to markdown files

    Returns:
        List of dictionaries with 'content' and 'source' keys
    """
    documents = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Remove frontmatter if present (YAML metadata at the beginning)
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2]  # Take content after the second ---

                # Create document with metadata
                document = {
                    "content": content.strip(),
                    "source": file_path
                }
                documents.append(document)

                logger.info(f"Successfully read {file_path}")

        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")

    return documents


def split_documents(documents: List[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> List[dict]:
    """
    Split documents into chunks of specified size.

    Args:
        documents: List of document dictionaries with 'content' and 'source'
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of chunk dictionaries with 'content', 'source', and 'chunk_id'
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for doc_idx, doc in enumerate(documents):
        content = doc["content"]
        source = doc["source"]

        # Split the content
        split_texts = text_splitter.split_text(content)

        # Create chunks with metadata
        for chunk_idx, chunk_text in enumerate(split_texts):
            chunk = {
                "content": chunk_text,
                "source": source,
                "chunk_id": f"{os.path.basename(source)}_{doc_idx}_{chunk_idx}"
            }
            chunks.append(chunk)

    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
    return chunks


def create_vector_store(chunks: List[dict], persist_directory: str = "./vector_db"):
    """
    Create and persist a vector store from document chunks.

    Args:
        chunks: List of chunk dictionaries
        persist_directory: Directory to persist the vector store
    """
    # Initialize embeddings model
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Prepare texts and metadata for the vector store
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [{"source": chunk["source"], "chunk_id": chunk["chunk_id"]} for chunk in chunks]

    # Create and persist the vector store
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_directory
    )

    logger.info(f"Vector store created and persisted to {persist_directory}")
    logger.info(f"Stored {len(chunks)} chunks in the vector database")

    return vector_store


def main():
    """Main ingestion function."""
    logger.info("Starting ingestion process...")

    # Step 1: Find all .md files in /docs and /content
    md_files = get_all_md_files()

    if not md_files:
        logger.warning("No markdown files found in /docs or /content directories")
        return

    # Step 2: Read content from all markdown files
    documents = read_md_files(md_files)

    if not documents:
        logger.warning("No documents were successfully read")
        return

    # Step 3: Split documents into chunks (300-500 tokens ≈ 300-500 characters)
    chunks = split_documents(documents, chunk_size=500, chunk_overlap=50)

    if not chunks:
        logger.warning("No chunks were created from the documents")
        return

    # Step 4: Create and persist vector store
    vector_store = create_vector_store(chunks)

    logger.info("Ingestion process completed successfully!")


if __name__ == "__main__":
    main()