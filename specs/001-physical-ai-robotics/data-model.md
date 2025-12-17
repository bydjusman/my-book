# Data Model: Physical AI & Humanoid Robotics Book

**Feature**: 001-physical-ai-robotics
**Date**: 2025-12-16

## Overview

This document defines the data models and structures for the Physical AI & Humanoid Robotics textbook project, focusing on content organization and RAG system requirements.

## Content Entities

### Module
- **Description**: A major section of the textbook covering a specific aspect of humanoid robotics
- **Attributes**:
  - moduleId: Unique identifier for the module
  - title: Display title of the module
  - slug: URL-friendly identifier
  - wordCount: Number of words in the module (1500-2000)
  - learningObjectives: List of key learning goals
  - prerequisites: List of required knowledge before reading
  - content: Markdown content of the module
  - createdAt: Creation timestamp
  - updatedAt: Last update timestamp

### Chapter
- **Description**: A subsection within a module
- **Attributes**:
  - chapterId: Unique identifier for the chapter
  - moduleId: Reference to the parent module
  - title: Display title of the chapter
  - slug: URL-friendly identifier
  - order: Position within the module
  - content: Markdown content of the chapter
  - createdAt: Creation timestamp
  - updatedAt: Last update timestamp

### Concept
- **Description**: A key robotics or AI concept explained in the textbook
- **Attributes**:
  - conceptId: Unique identifier for the concept
  - name: Name of the concept
  - definition: Clear definition of the concept
  - relatedModules: List of modules where the concept appears
  - relatedConcepts: List of related concepts
  - examples: Practical examples of the concept
  - createdAt: Creation timestamp
  - updatedAt: Last update timestamp

### Tool/Technology
- **Description**: A specific technology or framework covered in the textbook
- **Attributes**:
  - toolId: Unique identifier for the tool
  - name: Name of the tool/technology
  - purpose: What the tool is used for
  - modules: List of modules where the tool is discussed
  - keyFeatures: List of important features
  - useCases: Common applications of the tool
  - createdAt: Creation timestamp
  - updatedAt: Last update timestamp

## RAG System Entities

### DocumentChunk
- **Description**: A segment of content used for vector search in the RAG system
- **Attributes**:
  - chunkId: Unique identifier for the chunk
  - moduleId: Reference to the module this chunk belongs to
  - chapterId: Reference to the chapter this chunk belongs to (optional)
  - content: Text content of the chunk
  - embedding: Vector embedding of the content
  - position: Position of the chunk within the document
  - createdAt: Creation timestamp

### VectorIndex
- **Description**: Index structure for efficient similarity search
- **Attributes**:
  - indexId: Unique identifier for the index
  - name: Name of the index
  - dimensions: Number of dimensions in the vector space
  - chunks: List of document chunks in the index
  - createdAt: Creation timestamp
  - updatedAt: Last update timestamp

### SearchResult
- **Description**: Result of a similarity search in the RAG system
- **Attributes**:
  - resultId: Unique identifier for the result
  - query: Original search query
  - chunks: List of matching document chunks with similarity scores
  - confidence: Confidence score for the result
  - timestamp: When the search was performed

## Content Relationships

### Module Relationships
- A Module contains multiple Chapters
- A Module covers multiple Concepts
- A Module discusses multiple Tools/Technologies

### Content Navigation
- Modules are organized in a specific learning sequence
- Chapters within a module follow a logical progression
- Concepts may span multiple modules/chapters

## Validation Rules

### Content Requirements
- Each Module must have 1500-2000 words
- Each Module must have a clear learning objective
- All content must be in Markdown format
- Content must be accessible to undergraduate CS students

### RAG System Requirements
- Document chunks must be of appropriate size for vector search
- Embeddings must be generated from the book content only
- Search results must be grounded in book text
- System must return "Not found in book" when content is missing