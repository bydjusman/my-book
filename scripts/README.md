# Scripts Directory

This directory contains utility scripts for the Physical AI & Humanoid Robotics textbook project.

## Available Scripts

### Content Management
- `validate-content.js` - Validates content against textbook standards (word count, structure, etc.)

### RAG System Scripts
- `index-module1-mock.js` - Mock script to simulate indexing Module 1 content into the RAG system
- `test-module1-rag.js` - Mock script to test RAG system with Module 1 related questions

## Usage

### Content Validation
```bash
node scripts/validate-content.js
```

### RAG System Testing (Mock)
```bash
# Simulate indexing Module 1 content
node scripts/index-module1-mock.js

# Test RAG system with Module 1 questions
node scripts/test-module1-rag.js
```

## Notes

The mock scripts simulate the RAG system functionality since actual API keys are not provided. In a production environment, these would connect to real OpenAI and Qdrant services to index content and answer questions based on the textbook material.