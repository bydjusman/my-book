// Content indexing service for the RAG system

const fs = require('fs');
const path = require('path');
const { qdrantClient, COLLECTION_NAME, VECTOR_DIMENSION } = require('./qdrant-config');
const { openai, EMBEDDING_MODEL } = require('./openai-config');

class ContentIndexingService {
  constructor() {
    this.collectionName = COLLECTION_NAME;
  }

  // Initialize the Qdrant collection for storing textbook content
  async initializeCollection() {
    try {
      // Check if collection already exists
      const collections = await qdrantClient.getCollections();
      const collectionExists = collections.collections.some(
        collection => collection.name === this.collectionName
      );

      if (!collectionExists) {
        // Create new collection with specified vector size
        await qdrantClient.createCollection(this.collectionName, {
          vectors: {
            size: VECTOR_DIMENSION,
            distance: 'Cosine'
          }
        });
        console.log(`Created Qdrant collection: ${this.collectionName}`);
      } else {
        console.log(`Qdrant collection already exists: ${this.collectionName}`);
      }
    } catch (error) {
      console.error('Error initializing Qdrant collection:', error);
      throw error;
    }
  }

  // Generate embeddings for text content using OpenAI
  async generateEmbeddings(text) {
    try {
      const response = await openai.embeddings.create({
        model: EMBEDDING_MODEL,
        input: text,
      });

      return response.data[0].embedding;
    } catch (error) {
      console.error('Error generating embeddings:', error);
      throw error;
    }
  }

  // Index a single document chunk
  async indexDocumentChunk(chunk, moduleId, chapterId = null) {
    try {
      const embedding = await this.generateEmbeddings(chunk.content);

      const point = {
        id: chunk.chunkId,
        vector: embedding,
        payload: {
          content: chunk.content,
          moduleId: moduleId,
          chapterId: chapterId,
          position: chunk.position,
          wordCount: chunk.content.split(/\s+/).length
        }
      };

      await qdrantClient.upsert(this.collectionName, {
        points: [point]
      });

      return true;
    } catch (error) {
      console.error('Error indexing document chunk:', error);
      throw error;
    }
  }

  // Index entire module content
  async indexModuleContent(moduleId, content) {
    try {
      // This would typically involve chunking the content first
      // For now, we'll create a single chunk for the entire module
      const chunk = {
        chunkId: `${moduleId}-${Date.now()}`,
        content: content,
        position: 0
      };

      await this.indexDocumentChunk(chunk, moduleId);
      console.log(`Indexed module: ${moduleId}`);
    } catch (error) {
      console.error(`Error indexing module ${moduleId}:`, error);
      throw error;
    }
  }

  // Index all content from the docs directory
  async indexAllContent(docsPath = './docs') {
    try {
      console.log('Starting content indexing process...');

      // Initialize collection if needed
      await this.initializeCollection();

      // Read all markdown files from docs directory
      const files = this.getAllMarkdownFiles(docsPath);

      // Import DocumentChunkingService to properly chunk content
      const DocumentChunkingService = require('./document-chunking');
      const chunker = new DocumentChunkingService(1000, 200); // 1000 words max, 200 overlap

      for (const file of files) {
        const relativePath = path.relative(docsPath, file);
        const content = fs.readFileSync(file, 'utf8');

        // Extract module ID from path
        const pathParts = relativePath.split('/');
        if (pathParts.length >= 2 && pathParts[0].startsWith('module-')) {
          const moduleId = pathParts[0];
          const chapterId = path.basename(file, '.md');

          console.log(`Indexing: ${moduleId}/${chapterId}`);

          // Chunk the content properly using the document chunking service
          const chunks = chunker.chunkContent(content, moduleId, chapterId);

          // Index each chunk
          for (const chunk of chunks) {
            await this.indexDocumentChunk(chunk, moduleId, chapterId);
          }
        }
      }

      console.log('Content indexing completed.');
    } catch (error) {
      console.error('Error during content indexing:', error);
      throw error;
    }
  }

  // Helper to get all markdown files recursively
  getAllMarkdownFiles(dirPath, arrayOfFiles = []) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
      const filePath = path.join(dirPath, file);

      if (fs.statSync(filePath).isDirectory()) {
        this.getAllMarkdownFiles(filePath, arrayOfFiles);
      } else if (path.extname(filePath) === '.md') {
        arrayOfFiles.push(filePath);
      }
    });

    return arrayOfFiles;
  }

  // Delete a specific module's content from the index
  async deleteModuleContent(moduleId) {
    try {
      // Find all points with this module ID
      const searchResult = await qdrantClient.scroll(this.collectionName, {
        filter: {
          must: [{
            key: 'moduleId',
            match: { value: moduleId }
          }]
        },
        limit: 10000 // Adjust as needed
      });

      if (searchResult.points.length > 0) {
        const pointIds = searchResult.points.map(point => point.id);

        await qdrantClient.delete(this.collectionName, {
          points: pointIds
        });

        console.log(`Deleted ${pointIds.length} chunks for module: ${moduleId}`);
      }
    } catch (error) {
      console.error(`Error deleting module ${moduleId} from index:`, error);
      throw error;
    }
  }
}

module.exports = ContentIndexingService;