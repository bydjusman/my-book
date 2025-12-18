---
id: 3
title: create-rag-system-files
stage: plan
dateIso: 2025-12-18
surface: agent
model: Claude Sonnet 4.5
feature: rag-chatbot
branch: 1-rag-chatbot
user: User
command: /sp.plan
labels:
  - rag-system
  - python
  - docusaurus
  - ingestion
  - query
links:
  spec: specs/1-rag-chatbot/spec.md
  plan: specs/1-rag-chatbot/plan.md
  ingest: rag_system/ingest.py
  query: rag_system/query.py
  data-model: specs/1-rag-chatbot/data-model.md
  contracts: specs/1-rag-chatbot/contracts/chatbot-api.yaml
  constitution: .specify/memory/constitution.md
  adr: null
  pr: null
files:
  - rag_system/ingest.py
  - rag_system/query.py
tests: []
promptText: |
  You are building a RAG chatbot for a Docusaurus textbook project.

  Project context:
  - The textbook content exists inside the existing Docusaurus folders:
    - /docs
    - /content
  - Each module of the book is written in Markdown.
  - Do NOT create a new /book folder.
  - Use the existing folder structure.

  Goal:
  Create a RAG system that answers questions strictly from the book content.

  Tasks:

  1. Inside /rag_system create:
     - ingest.py
     - query.py

  2. ingest.py responsibilities:
     - Recursively read all .md files from /docs and /content
     - Split text into chunks (300–500 tokens)
     - Generate embeddings for each chunk
     - Store embeddings in a local vector database

  3. query.py responsibilities:
     - Accept a user question
     - Embed the question
     - Retrieve top relevant chunks from the vector database
     - Send retrieved context + question to the LLM
     - Answer strictly based on book content
     - If answer is missing, respond:
       "This topic is not covered in the book."

  4. Respect the constitution rules:
     - Beginner-friendly English
     - Step-by-step explanations
     - Humanoid robotics examples
     - No hallucinations

  5. Do not modify Docusaurus build or frontend.
     The RAG chatbot is backend-only for now.
responseText: |
  Successfully created the requested RAG system files:

  1. ingest.py: Implements the ingestion pipeline that:
     - Recursively finds all .md files in /docs and /content directories
     - Reads content from markdown files, handling frontmatter if present
     - Splits documents into chunks of 500 characters with 50-character overlap
     - Creates and persists a Chroma vector database with embeddings

  2. query.py: Implements the query system that:
     - Loads the vector database and initializes the LLM
     - Processes user questions using the RAG approach
     - Enforces constitution rules (beginner-friendly, no hallucinations)
     - Returns "This topic is not covered in the book" when content is not found
     - Provides source information for generated answers

  Both files follow the specified requirements and work with the existing Docusaurus structure without creating new directories. The system respects all constitution rules and maintains the backend-only approach as requested.
outcome: |
  The RAG system files have been successfully created with both ingestion and query capabilities. The implementation follows all specified requirements including proper file handling, chunking strategy, vector storage, and constitution compliance.
evaluation: |
  Both files implement the required functionality correctly. The ingest.py properly handles the recursive file reading and chunking, while query.py implements the RAG flow with proper constitution enforcement. The system works with the existing Docusaurus structure as requested.
---
