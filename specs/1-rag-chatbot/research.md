# Research: Physical AI & Humanoid Robotics RAG Chatbot

**Created**: 2025-12-18
**Feature**: RAG Chatbot for Physical AI & Humanoid Robotics textbook
**Status**: Complete

## Decision: Embedding Model Selection
**Rationale**: For educational content with technical terminology, we need an embedding model that can effectively capture the semantic meaning of robotics and AI concepts while maintaining good performance on specialized vocabulary.
**Decision**: Use all-MiniLM-L6-v2 model from Sentence Transformers
**Alternatives considered**:
- all-mpnet-base-v2 (higher quality but slower)
- BGE-small-en (good for technical content but less tested)
- Custom trained model (too complex for this project)
**Chosen because**: Good balance of speed, quality, and effectiveness for technical content

## Decision: LLM Selection
**Rationale**: Need to balance cost, performance, and educational appropriateness while ensuring responses follow constitutional constraints.
**Decision**: Start with OpenAI GPT-3.5 Turbo, with option to switch to local model (Llama 2/3 via Ollama) if needed
**Alternatives considered**:
- GPT-4 (more capable but higher cost)
- Anthropic Claude (good for educational content but requires API access)
- Local models (Ollama with Llama 2/3, better for privacy but requires more resources)
- Mistral or other open models (emerging options but less proven)
**Chosen because**: Proven track record for educational applications and good prompt engineering capabilities

## Decision: Vector Database
**Rationale**: Need efficient similarity search for textbook content retrieval with good performance and easy integration.
**Decision**: FAISS with IndexFlatIP (Inner Product) for cosine similarity
**Alternatives considered**:
- ChromaDB (easier setup but potentially slower for this use case)
- Pinecone (managed service but adds complexity)
- Weaviate (feature-rich but overkill for this project)
- Annoy (good performance but less flexible)
**Chosen because**: Excellent performance for semantic search with good Python integration

## Decision: Text Chunking Strategy
**Rationale**: Need to balance context preservation with retrieval precision for textbook content that includes both conceptual explanations and technical details.
**Decision**: RecursiveCharacterTextSplitter with chunk_size=512, chunk_overlap=64
**Alternatives considered**:
- Sentence-based splitting (might break up related concepts)
- Fixed-size character splitting (might split in the middle of important concepts)
- Markdown-aware splitting (preserves section structure)
- Custom splitting by textbook sections (too rigid)
**Chosen because**: Preserves context while maintaining semantic coherence for technical content

## Decision: Retrieval Strategy
**Rationale**: Need to ensure relevant textbook sections are retrieved while maintaining accuracy and avoiding irrelevant results.
**Decision**: Hybrid retrieval combining semantic search (FAISS) with keyword-based filtering
**Alternatives considered**:
- Pure semantic search (might return less relevant results)
- Pure keyword search (might miss semantically related content)
- Multi-query retrieval (more complex but potentially better results)
- Re-ranking with cross-encoder (improves results but adds latency)
**Chosen because**: Balances precision and recall while maintaining reasonable response times

## Decision: Frontend Integration Approach
**Rationale**: Need to integrate seamlessly with existing Docusaurus documentation site while providing a good user experience.
**Decision**: React-based chat component integrated as Docusaurus theme component
**Alternatives considered**:
- Standalone web application (separates from documentation context)
- Iframe embedding (adds complexity and potential security issues)
- Third-party chat widget (less customizable)
- Custom HTML/CSS/JS (more work, less maintainable)
**Chosen because**: Maintains consistency with existing documentation site and allows for customization

## Decision: Safety and Constitution Enforcement
**Rationale**: Critical to ensure the chatbot never violates the constitutional requirement to only use textbook content.
**Decision**: Multi-layer validation system with content filtering and response verification
**Alternatives considered**:
- Simple keyword filtering (too basic for this use case)
- LLM-based verification (circular logic, LLM might also hallucinate)
- Rule-based verification with textbook citation requirement (more robust)
- Human-in-the-loop for edge cases (not scalable)
**Chosen because**: Rule-based verification with citation requirement provides reliable enforcement of constitutional constraints