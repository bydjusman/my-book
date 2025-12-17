// Document chunking logic for content processing

class DocumentChunkingService {
  constructor(maxChunkSize = 1000, overlap = 200) {
    this.maxChunkSize = maxChunkSize; // Maximum number of words per chunk
    this.overlap = overlap; // Number of words to overlap between chunks
  }

  // Split content into chunks of specified size with overlap
  chunkContent(content, moduleId, chapterId = null) {
    if (!content || typeof content !== 'string') {
      throw new Error('Content must be a non-empty string');
    }

    // Split content into sentences to maintain context
    const sentences = this.splitIntoSentences(content);
    const chunks = [];
    let currentChunk = '';
    let currentWordCount = 0;
    let position = 0;

    for (let i = 0; i < sentences.length; i++) {
      const sentence = sentences[i];
      const sentenceWords = this.countWords(sentence);

      // If adding this sentence would exceed the max chunk size
      if (currentWordCount + sentenceWords > this.maxChunkSize && currentChunk !== '') {
        // Save the current chunk
        chunks.push({
          chunkId: `${moduleId}-${chapterId || 'unknown'}-${position}`,
          content: currentChunk.trim(),
          position: position,
          wordCount: currentWordCount
        });

        position++;

        // Start a new chunk with overlap from the previous chunk
        const overlapWords = this.getOverlapWords(currentChunk, this.overlap);
        currentChunk = overlapWords + ' ' + sentence;
        currentWordCount = this.countWords(currentChunk);
      } else {
        // Add sentence to current chunk
        currentChunk += ' ' + sentence;
        currentWordCount += sentenceWords;
      }
    }

    // Add the final chunk if it has content
    if (currentChunk.trim() !== '') {
      chunks.push({
        chunkId: `${moduleId}-${chapterId || 'unknown'}-${position}`,
        content: currentChunk.trim(),
        position: position,
        wordCount: currentWordCount
      });
    }

    return chunks;
  }

  // Split text into sentences while preserving context
  splitIntoSentences(text) {
    // Split on sentence boundaries (. ! ?) followed by whitespace and capital letter
    // Also handle common abbreviations to avoid false splits
    const sentences = text
      .replace(/\s+/g, ' ') // Normalize whitespace
      .replace(/\.([A-Z])/g, '. $1') // Add space after periods followed by capital
      .replace(/!([A-Z])/g, '! $1') // Add space after exclamation marks followed by capital
      .replace(/\?([A-Z])/g, '? $1') // Add space after question marks followed by capital
      .split(/[.!?]+\s+/); // Split on sentence endings followed by whitespace

    // Filter out empty sentences and trim whitespace
    return sentences
      .map(s => s.trim())
      .filter(s => s.length > 0);
  }

  // Get the last N words from a text string for overlap
  getOverlapWords(text, wordCount) {
    const words = text.split(/\s+/);
    if (words.length <= wordCount) {
      return text;
    }

    // Take the last 'wordCount' words
    const overlapWords = words.slice(-wordCount);
    return overlapWords.join(' ');
  }

  // Count words in a text string
  countWords(text) {
    if (!text || typeof text !== 'string') {
      return 0;
    }

    return text.trim()
      .split(/\s+/)
      .filter(word => word.length > 0).length;
  }

  // Validate that chunks meet requirements
  validateChunks(chunks) {
    const validation = {
      valid: true,
      errors: [],
      totalChunks: chunks.length,
      totalWords: 0
    };

    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const wordCount = this.countWords(chunk.content);

      // Check if chunk exceeds maximum size
      if (wordCount > this.maxChunkSize) {
        validation.valid = false;
        validation.errors.push(`Chunk ${i} exceeds maximum size: ${wordCount} words (max: ${this.maxChunkSize})`);
      }

      validation.totalWords += wordCount;
    }

    return validation;
  }

  // Process content with different chunking strategies
  chunkWithStrategy(content, moduleId, chapterId = null, strategy = 'sentence') {
    switch (strategy) {
      case 'sentence':
        return this.chunkContent(content, moduleId, chapterId);
      case 'paragraph':
        return this.chunkByParagraphs(content, moduleId, chapterId);
      case 'word':
        return this.chunkByWords(content, moduleId, chapterId);
      default:
        throw new Error(`Unknown chunking strategy: ${strategy}`);
    }
  }

  // Alternative: Chunk by paragraphs
  chunkByParagraphs(content, moduleId, chapterId = null) {
    const paragraphs = content.split(/\n\s*\n/); // Split on double newlines (paragraph breaks)
    const chunks = [];
    let currentChunk = '';
    let currentWordCount = 0;
    let position = 0;

    for (const paragraph of paragraphs) {
      const paragraphWords = this.countWords(paragraph);

      if (currentWordCount + paragraphWords > this.maxChunkSize && currentChunk !== '') {
        // Save current chunk
        chunks.push({
          chunkId: `${moduleId}-${chapterId || 'unknown'}-${position}`,
          content: currentChunk.trim(),
          position: position,
          wordCount: currentWordCount
        });

        position++;
        currentChunk = paragraph;
        currentWordCount = paragraphWords;
      } else if (paragraphWords > this.maxChunkSize) {
        // If paragraph is too large, fall back to sentence chunking
        const sentenceChunks = this.chunkContent(paragraph, moduleId, `${chapterId}-p${position}`);
        chunks.push(...sentenceChunks);
        position += sentenceChunks.length;
      } else {
        currentChunk += '\n\n' + paragraph;
        currentWordCount += paragraphWords;
      }
    }

    // Add final chunk
    if (currentChunk.trim() !== '') {
      chunks.push({
        chunkId: `${moduleId}-${chapterId || 'unknown'}-${position}`,
        content: currentChunk.trim(),
        position: position,
        wordCount: currentWordCount
      });
    }

    return chunks;
  }

  // Alternative: Chunk by fixed word count
  chunkByWords(content, moduleId, chapterId = null) {
    const words = content.split(/\s+/);
    const chunks = [];
    let position = 0;

    for (let i = 0; i < words.length; i += (this.maxChunkSize - this.overlap)) {
      const chunkWords = words.slice(i, i + this.maxChunkSize);
      const chunkContent = chunkWords.join(' ');

      chunks.push({
        chunkId: `${moduleId}-${chapterId || 'unknown'}-${position}`,
        content: chunkContent,
        position: position,
        wordCount: chunkWords.length
      });

      position++;
    }

    return chunks;
  }
}

module.exports = DocumentChunkingService;