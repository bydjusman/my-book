// Vector embedding service for textbook content

const { openai, EMBEDDING_MODEL } = require('./openai-config');

class VectorEmbeddingService {
  constructor() {
    this.model = EMBEDDING_MODEL;
  }

  // Generate embeddings for a single text
  async generateEmbedding(text) {
    try {
      if (!text || typeof text !== 'string' || text.trim().length === 0) {
        throw new Error('Text must be a non-empty string');
      }

      const response = await openai.createEmbedding({
        model: this.model,
        input: text,
      });

      const embedding = response.data.data[0].embedding;

      return {
        vector: embedding,
        length: embedding.length,
        text: text.substring(0, 100) + (text.length > 100 ? '...' : '') // Preview of text
      };
    } catch (error) {
      console.error('Error generating embedding:', error);
      throw error;
    }
  }

  // Generate embeddings for multiple texts in batch
  async generateEmbeddingsBatch(texts) {
    try {
      if (!Array.isArray(texts) || texts.length === 0) {
        throw new Error('Texts must be a non-empty array');
      }

      // Validate each text
      for (let i = 0; i < texts.length; i++) {
        if (!texts[i] || typeof texts[i] !== 'string' || texts[i].trim().length === 0) {
          throw new Error(`Text at index ${i} must be a non-empty string`);
        }
      }

      // OpenAI has a limit on the number of inputs per request
      // We'll process in batches of up to 2048 texts
      const BATCH_SIZE = 2048;
      const allEmbeddings = [];

      for (let i = 0; i < texts.length; i += BATCH_SIZE) {
        const batch = texts.slice(i, i + BATCH_SIZE);

        const response = await openai.createEmbedding({
          model: this.model,
          input: batch,
        });

        const batchEmbeddings = response.data.data.map((item, idx) => ({
          vector: item.embedding,
          index: i + idx,
          length: item.embedding.length,
          text: batch[idx].substring(0, 100) + (batch[idx].length > 100 ? '...' : '') // Preview of text
        }));

        allEmbeddings.push(...batchEmbeddings);
      }

      return allEmbeddings;
    } catch (error) {
      console.error('Error generating embeddings batch:', error);
      throw error;
    }
  }

  // Calculate cosine similarity between two vectors
  cosineSimilarity(vecA, vecB) {
    if (vecA.length !== vecB.length) {
      throw new Error('Vectors must have the same length for similarity calculation');
    }

    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < vecA.length; i++) {
      dotProduct += vecA[i] * vecB[i];
      normA += vecA[i] * vecA[i];
      normB += vecB[i] * vecB[i];
    }

    const similarity = dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));

    // Ensure the result is between -1 and 1 (floating point precision issues can cause slight deviations)
    return Math.max(-1, Math.min(1, similarity));
  }

  // Calculate similarity between text and a vector
  async similarityToVector(text, vector) {
    const textEmbedding = await this.generateEmbedding(text);
    return this.cosineSimilarity(textEmbedding.vector, vector);
  }

  // Calculate similarity between two texts
  async similarityBetweenTexts(textA, textB) {
    const embeddingA = await this.generateEmbedding(textA);
    const embeddingB = await this.generateEmbedding(textB);
    return this.cosineSimilarity(embeddingA.vector, embeddingB.vector);
  }

  // Find the most similar text from a list of texts
  async findMostSimilar(text, texts) {
    if (!Array.isArray(texts) || texts.length === 0) {
      throw new Error('Texts must be a non-empty array');
    }

    const textEmbedding = await this.generateEmbedding(text);
    const textEmbeddings = await this.generateEmbeddingsBatch(texts);

    let maxSimilarity = -2; // Cosine similarity ranges from -1 to 1
    let mostSimilarIndex = -1;

    for (let i = 0; i < textEmbeddings.length; i++) {
      const similarity = this.cosineSimilarity(textEmbedding.vector, textEmbeddings[i].vector);

      if (similarity > maxSimilarity) {
        maxSimilarity = similarity;
        mostSimilarIndex = i;
      }
    }

    return {
      index: mostSimilarIndex,
      similarity: maxSimilarity,
      text: texts[mostSimilarIndex]
    };
  }

  // Validate that a vector is a proper embedding vector
  validateVector(vector) {
    if (!Array.isArray(vector)) {
      return { valid: false, error: 'Vector must be an array' };
    }

    if (vector.length === 0) {
      return { valid: false, error: 'Vector must not be empty' };
    }

    for (let i = 0; i < vector.length; i++) {
      if (typeof vector[i] !== 'number' || isNaN(vector[i]) || !isFinite(vector[i])) {
        return { valid: false, error: `Vector element at index ${i} is not a valid number` };
      }
    }

    return { valid: true, error: null };
  }

  // Normalize a vector to unit length
  normalizeVector(vector) {
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));

    if (magnitude === 0) {
      return vector; // Return as-is if zero vector
    }

    return vector.map(val => val / magnitude);
  }

  // Get embedding model info
  getModelInfo() {
    return {
      model: this.model,
      dimensions: 1536, // text-embedding-ada-002 has 1536 dimensions
      provider: 'OpenAI',
      description: 'Text embedding model for generating vector representations of textbook content'
    };
  }
}

module.exports = VectorEmbeddingService;