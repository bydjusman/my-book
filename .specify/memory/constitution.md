<!-- SYNC IMPACT REPORT
Version change: N/A (initial creation) → v1.0.0
Modified principles: N/A (initial creation)
Added sections: All sections (initial creation)
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
- README.md ⚠ pending
Follow-up TODOs: None
-->

# AI/Spec-Driven Book with Integrated RAG Chatbot Constitution

## Core Principles

### I. Spec-First Workflow
All development begins with comprehensive specifications before any implementation. The workflow follows constitution → spec → plan → build in strict sequence. Every feature, requirement, and constraint must be documented in spec files before coding begins.

### II. Beginner-Friendly Accessibility
Content and code must be accessible to undergraduate CS students and beginner AI developers. Use simple English, avoid advanced mathematics, provide clear explanations, and ensure all concepts build progressively from fundamentals.

### III. Grounded Content (NON-NEGOTIABLE)
All book content and chatbot responses must be strictly grounded in the book text. No hallucinations or unsupported claims are permitted. The RAG chatbot must only answer from book content, stating "Not found in book" when information is missing.

### IV. Modular and Testable Design
The book and supporting systems must be built in modular components with clear learning goals. Each chapter should be 1500-2000 words, code examples must be reproducible, and all functionality should be independently testable.

### V. Free-Tier Tool Compliance
Only free-tier tools and services may be used to ensure accessibility and reproducibility. Technical stack includes Docusaurus, FastAPI, OpenAI Agents/ChatKit SDKs, Qdrant Cloud (Free Tier), and Neon Serverless Postgres.

### VI. Markdown-Only Content Standard
All book content must be authored in Markdown format only. No other document formats are permitted to maintain simplicity and version control compatibility.

## Technical Standards

The book will be built with Docusaurus and deployed on GitHub Pages. The RAG chatbot must support full-book, chapter, and selected-text Q&A with clear separation between retrieval and generation phases. The embedded chatbot must work correctly and answers must be grounded in book text.

## Development Workflow

All work follows the Spec-Kit Plus methodology using the constitution → spec → plan → tasks → build sequence. Each phase must be completed before proceeding to the next. Code changes require corresponding updates to specifications and plans. All development must align with the core principles and technical stack requirements.

## Governance

This constitution supersedes all other development practices and guidelines. All team members must comply with these principles. Amendments to this constitution require formal documentation and approval. All pull requests and code reviews must verify compliance with constitutional principles. Complexity must be justified with clear benefits to the target audience.

**Version**: v1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16