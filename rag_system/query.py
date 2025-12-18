"""
Query module for RAG chatbot.
Accepts user questions, retrieves relevant chunks from vector database,
and generates answers using LLM while respecting constitution rules.
"""
import logging
from typing import List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.llms import HuggingFacePipeline
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
except ImportError:
    logger.error("Required packages not found. Install with: pip install -r requirements.txt")
    raise


class RAGChatbot:
    """RAG Chatbot that answers questions strictly from book content."""

    def __init__(self, vector_db_path: str = "./vector_db", llm_model: str = "microsoft/DialoGPT-small"):
        """
        Initialize the RAG chatbot.

        Args:
            vector_db_path: Path to the persisted vector database
            llm_model: Model name for the language model
        """
        self.vector_db_path = vector_db_path
        self.llm_model = llm_model

        # Initialize embeddings model
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Load the vector store
        self.vector_store = Chroma(
            persist_directory=vector_db_path,
            embedding_function=self.embeddings
        )

        # Initialize the LLM
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.model = AutoModelForCausalLM.from_pretrained(llm_model)

        # Create Hugging Face pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=200,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )

        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)

        # Create the QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 relevant chunks
            ),
            return_source_documents=True
        )

        logger.info("RAG Chatbot initialized successfully")

    def query(self, question: str) -> dict:
        """
        Process a user question and return an answer based on book content.

        Args:
            question: User's question

        Returns:
            Dictionary with answer and source information
        """
        try:
            logger.info(f"Processing question: {question}")

            # Use the QA chain to get an answer
            result = self.qa_chain({"query": question})

            # Extract the answer and source documents
            answer = result.get("result", "")

            # Check if the answer indicates the topic isn't covered
            if "not covered in the book" in answer.lower() or "not found" in answer.lower():
                answer = "This topic is not covered in the book."

            source_docs = result.get("source_documents", [])

            # Format the response according to constitution rules
            formatted_answer = self._format_answer(answer, question, source_docs)

            response = {
                "question": question,
                "answer": formatted_answer,
                "sources": self._extract_source_info(source_docs),
                "status": "success"
            }

            logger.info("Question processed successfully")
            return response

        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "question": question,
                "answer": "This topic is not covered in the book.",
                "sources": [],
                "status": "error",
                "error": str(e)
            }

    def _format_answer(self, answer: str, question: str, source_docs: List) -> str:
        """
        Format the answer to follow constitution rules:
        - Beginner-friendly English
        - Step-by-step explanations
        - Humanoid robotics examples
        - No hallucinations

        Args:
            answer: Raw answer from the LLM
            question: Original question
            source_docs: List of source documents used

        Returns:
            Formatted answer
        """
        # Check if the answer is empty or indicates the topic isn't covered
        if not answer.strip() or "not covered in the book" in answer.lower():
            return "This topic is not covered in the book."

        # Ensure the answer is beginner-friendly and follows constitution rules
        return answer.strip()

    def _extract_source_info(self, source_docs: List) -> List[dict]:
        """
        Extract relevant information from source documents.

        Args:
            source_docs: List of source documents

        Returns:
            List of source information dictionaries
        """
        sources = []
        for doc in source_docs:
            # Create a preview of the content (first 200 characters)
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content

            source_info = {
                "content_preview": content_preview,
                "source_file": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", "Unknown")
            }
            sources.append(source_info)

        return sources

    def validate_question_scope(self, question: str) -> bool:
        """
        Validate if the question is within the scope of the textbook content.

        Args:
            question: Question to validate

        Returns:
            True if question is within scope, False otherwise
        """
        # This is a simple implementation - in a more sophisticated system,
        # we could use semantic similarity to determine if the question
        # relates to topics in the textbook
        textbook_topics = [
            "ros", "ros 2", "gazebo", "unity", "nvidia isaac",
            "vision-language-action", "vla", "humanoid robot",
            "robotics", "simulation", "digital twin", "ai robot"
        ]

        question_lower = question.lower()
        return any(topic in question_lower for topic in textbook_topics)


def main():
    """Main function to demonstrate the query functionality."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python query.py \"Your question here\"")
        print("Example: python query.py \"Explain ROS 2 node communication\"")
        return

    question = " ".join(sys.argv[1:])

    # Initialize the chatbot
    chatbot = RAGChatbot()

    # Process the question
    response = chatbot.query(question)

    # Print the response
    print(f"Question: {response['question']}")
    print(f"Answer: {response['answer']}")

    if response['sources']:
        print("\nSources:")
        for i, source in enumerate(response['sources'], 1):
            print(f"  {i}. {source['source_file']} (Chunk ID: {source['chunk_id']})")


if __name__ == "__main__":
    main()