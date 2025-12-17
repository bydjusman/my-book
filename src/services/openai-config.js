// OpenAI configuration for the RAG system

require('dotenv').config();
const OpenAI = require('openai');

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Default model for embeddings
const EMBEDDING_MODEL = 'text-embedding-ada-002';

// Default model for chat completions
const CHAT_MODEL = process.env.OPENAI_MODEL || 'gpt-3.5-turbo';

module.exports = {
  openai,
  EMBEDDING_MODEL,
  CHAT_MODEL
};