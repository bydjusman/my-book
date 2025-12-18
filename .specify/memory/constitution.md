<!-- SYNC IMPACT REPORT
Version change: v1.1.0 → v1.2.0
Modified principles: V. Robotics Tool Compliance → V. Robotics Tool Compliance (expanded to include Isaac Sim & Isaac ROS, VLA), VII. Technical Standards → VII. Technical Standards (updated scope and rules)
Added sections: None
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
- README.md ⚠ pending
Follow-up TODOs: Update all templates to reflect new project scope
-->

# Physical AI & Humanoid Robotics RAG Chatbot Constitution

## Core Principles

### I. Spec-First Workflow
All development begins with comprehensive specifications before any implementation. The workflow follows constitution → spec → plan → build in strict sequence. Every feature, requirement, and constraint must be documented in spec files before coding begins. This applies specifically to the four modules of Physical AI & Humanoid Robotics.

### II. Beginner-Friendly Accessibility
Content and code must be accessible to undergraduate CS students, AI learners new to robotics, and beginners in ROS 2, simulation, and humanoid robots. Use simple English, avoid advanced mathematics, provide clear explanations, and ensure all concepts build progressively from fundamentals.

### III. Strict Book Content Adherence (NON-NEGOTIABLE)
All chatbot responses must be strictly grounded in the official course textbook: "Physical AI & Humanoid Robotics". No hallucinations or unsupported claims are permitted. The RAG chatbot must only answer from book content, stating "This topic is not covered in the book" when information is missing.

### IV. Module-Based Learning Structure
The system must support the four official modules of the book with clear learning goals. Each module should build upon previous concepts while maintaining independence. Content must be structured to support progressive learning from ROS 2 (Robotic Nervous System) through Vision-Language-Action (LLMs + Robotics).

### V. Robotics Tool Compliance
Only the specified robotics tools and frameworks may be used to ensure proper learning progression. Technical stack includes ROS 2, Gazebo & Unity (Digital Twin), NVIDIA Isaac Sim & Isaac ROS (AI Robot Brain), Vision-Language-Action (VLA) systems, and Humanoid robot simulation and control. All implementations must align with these core technologies.

### VI. Educational Content Standards
All content must be authored in Markdown format and focus on embodied intelligence concepts. Emphasize the connection between AI brain and physical robot body, encouraging practical understanding over memorization.

## Technical Standards

The RAG chatbot must answer questions strictly based on the textbook "Physical AI & Humanoid Robotics". The system should help students understand concepts, modules, tools, and workflows described in the book. The chatbot must support simple English, beginner-friendly explanations, clear step-by-step guidance, short paragraphs, and use examples related to humanoid robots when possible while avoiding unnecessary theory.

## Development Workflow

All work follows the Spec-Kit Plus methodology using the constitution → spec → plan → tasks → build sequence. Each phase must be completed before proceeding to the next. Code changes require corresponding updates to specifications and plans. All development must align with the core principles and technical stack requirements. Special attention must be paid to the four modules:
- Module 1: ROS 2 – Robotic Nervous System
- Module 2: Gazebo & Unity – Digital Twin
- Module 3: NVIDIA Isaac Sim & Isaac ROS – AI Robot Brain
- Module 4: Vision-Language-Action (VLA) – LLMs + Robotics

## Governance

This constitution supersedes all other development practices and guidelines. All team members must comply with these principles. Amendments to this constitution require formal documentation and approval. All pull requests and code reviews must verify compliance with constitutional principles. Complexity must be justified with clear benefits to the target audience. The RAG behavior rules must be strictly enforced: always retrieve context from the book before answering, and if the answer is not found in the book, reply: "This topic is not covered in the book".

**Version**: v1.2.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-18