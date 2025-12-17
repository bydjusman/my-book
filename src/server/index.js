// Basic API server structure for the RAG chatbot

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

// Import service configurations
const { qdrantClient, COLLECTION_NAME } = require('../services/qdrant-config');
const { openai, CHAT_MODEL } = require('../services/openai-config');

// Create Express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 60, // limit each IP to 60 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Import API routes
const chatbotRoutes = require('./routes/chatbot');
const healthRoutes = require('./routes/health');
const modulesRoutes = require('./routes/modules');

// API routes
app.use('/api/chatbot', chatbotRoutes);
app.use('/api/health', healthRoutes);
app.use('/api/modules', modulesRoutes);

// Basic root route
app.get('/', (req, res) => {
  res.json({ message: 'Physical AI & Humanoid Robotics RAG API' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An internal server error occurred'
    }
  });
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down server...');
  process.exit(0);
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API documentation available at /api`);
});

module.exports = app;