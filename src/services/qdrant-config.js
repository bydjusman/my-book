// Qdrant configuration for the RAG system

require('dotenv').config();

const { QdrantClient } = require('@qdrant/js-client-rest');

// Initialize Qdrant client
const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL,
  apiKey: process.env.QDRANT_API_KEY,
});

// Default collection name for textbook content
const COLLECTION_NAME = process.env.QDRANT_COLLECTION_NAME || 'textbook_content';

// Vector dimension for OpenAI embeddings (1536 for text-embedding-ada-002)
const VECTOR_DIMENSION = 1536;

module.exports = {
  qdrantClient,
  COLLECTION_NAME,
  VECTOR_DIMENSION
};