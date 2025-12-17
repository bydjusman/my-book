---
id: 1
title: create-project-constitution
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,spec-driven,rag-chatbot,documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: AI/Spec-Driven Book with Integrated RAG Chatbot

Purpose:
Write and publish a technical book using a spec-driven workflow. The book will be built with Docusaurus, deployed on GitHub Pages, and include an embedded RAG chatbot that answers questions strictly from the book content.

Audience:
- Undergraduate CS students
- Beginner AI developers
- Learners new to spec-driven development and RAG

Core Principles:
- Spec-first workflow (constitution → spec → plan → build)
- Clear and beginner-friendly explanations
- Practical, implementation-focused learning
- No hallucinations or unsupported claims

Book Standards:
- Markdown only
- Built with Docusaurus
- Deployed to GitHub Pages
- Modular chapters with clear learning goals
- Simple English, no advanced math

Technical Stack:
- Spec-Kit Plus + Claude Code
- FastAPI backend
- OpenAI Agents / ChatKit SDKs
- Qdrant Cloud (Free Tier)
- Neon Serverless Postgres

RAG Chatbot Rules:
- Answers must come only from book content
- Supports full-book, chapter, and selected-text Q&A
- If answer is missing, say "Not found in book"
- Clear retrieval → generation separation

Constraints:
- 1500–2000 words per chapter
- Free-tier tools only
- Reproducible code examples

Success Criteria:
- Book builds and deploys successfully
- Embedded chatbot works correctly
- Answers are grounded in book text
```

## Response snapshot

Created the project constitution file (.specify/memory/constitution.md) with the following sections:
- Core Principles (Spec-First Workflow, Beginner-Friendly Accessibility, Grounded Content, Modular Design, Free-Tier Tool Compliance, Markdown-Only Standard)
- Technical Standards (Docusaurus, GitHub Pages, RAG chatbot requirements)
- Development Workflow (Spec-Kit Plus methodology)
- Governance (Amendment procedures, compliance requirements)

The constitution establishes the foundational principles for the AI/Spec-Driven Book with Integrated RAG Chatbot project, emphasizing spec-first development, accessibility for beginners, grounded content without hallucinations, and free-tier tool compliance.

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Create feature specifications following the constitution
- 🧠 Reflection: Constitution provides strong foundation for spec-driven development approach

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification process