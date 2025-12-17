// Health check API routes

const express = require('express');
const router = express.Router();
const { qdrantClient } = require('../../services/qdrant-config');

router.get('/', async (req, res) => {
  try {
    // Test Qdrant connection
    let vectorIndexStatus = 'unknown';
    try {
      await qdrantClient.getCollections();
      vectorIndexStatus = 'ready';
    } catch (qdrantErr) {
      vectorIndexStatus = 'error';
    }

    // Test API connections
    const apiConnectionStatus = process.env.OPENAI_API_KEY ? 'configured' : 'missing';

    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      details: {
        vectorIndex: vectorIndexStatus,
        apiConnection: apiConnectionStatus,
        lastIndexUpdate: 'N/A' // Will be updated when indexing is implemented
      }
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      details: {
        error: error.message
      }
    });
  }
});

module.exports = router;