#!/usr/bin/env node

// Script to index Module 1 content into the RAG system

require('dotenv').config();

const ContentIndexingService = require('../src/services/content-indexing');

async function indexModule1Content() {
  console.log('Starting Module 1 content indexing...');

  try {
    const indexingService = new ContentIndexingService();

    // Index only Module 1 content
    await indexingService.indexAllContent('./docs/module-1-ros2');

    console.log('Module 1 content indexing completed successfully!');
  } catch (error) {
    console.error('Error during Module 1 content indexing:', error);
    process.exit(1);
  }
}

// Run indexing if this script is executed directly
if (require.main === module) {
  indexModule1Content();
}

module.exports = indexModule1Content;