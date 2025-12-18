---
id: 1
title: update-constitution
stage: constitution
dateIso: 2025-12-18
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: User
command: /sp.constitution
labels:
  - constitution
  - robotics
  - education
  - rag-chatbot
links:
  constitution: .specify/memory/constitution.md
  spec: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
promptText: |
  # Project Constitution
  Project Name: Physical AI & Humanoid Robotics – RAG Chatbot

  ## Purpose
  This project creates a Retrieval-Augmented Generation (RAG) chatbot
  that answers questions strictly from the official course textbook:
  "Physical AI & Humanoid Robotics".

  The chatbot must help students understand concepts,
  modules, tools, and workflows described in the book.

  ## Audience
  - Undergraduate Computer Science students
  - AI learners new to Robotics
  - Beginners in ROS 2, Simulation, and Humanoid Robots

  ## Scope (Allowed Knowledge)
  The chatbot may ONLY answer using information from:
  - The four official modules of the book
  - Course descriptions and explanations
  - Concepts related to:
    - ROS 2
    - Gazebo & Unity
    - NVIDIA Isaac
    - Vision-Language-Action (VLA)

  ## Out of Scope (Disallowed)
  - No unrelated AI topics
  - No advanced mathematics
  - No hardware schematics beyond conceptual explanation
  - No guessing beyond the book content

  ## Answering Style
  - Simple English
  - Beginner-friendly
  - Clear step-by-step explanations
  - Short paragraphs
  - Use examples when possible
  - Avoid unnecessary theory

  ## RAG Behavior Rules
  - Always retrieve context from the book before answering
  - If the answer is not found in the book, reply:
    "This topic is not covered in the course material."

  ## Educational Philosophy
  - Focus on Embodied Intelligence
  - Emphasize the connection between AI brain and physical robot body
  - Encourage practical understanding over memorization

  ## Modules Reference
  Module 1: ROS 2 – Robotic Nervous System
  Module 2: Gazebo & Unity – Digital Twin
  Module 3: NVIDIA Isaac – AI Robot Brain
  Module 4: Vision-Language-Action – LLMs + Robotics
responseText: |
  Successfully updated the project constitution to reflect the Physical AI & Humanoid Robotics RAG Chatbot project. The constitution was updated from v1.0.0 to v1.1.0 with the following changes:

  - Updated project name and scope to focus on Physical AI & Humanoid Robotics
  - Modified audience to include undergraduate CS students, AI learners new to robotics, and beginners in ROS 2, simulation, and humanoid robots
  - Updated the Strict Book Content Adherence principle to require responses only from the official course textbook
  - Added Module-Based Learning Structure principle to support the four official modules
  - Changed tool compliance to focus on robotics tools: ROS 2, Gazebo & Unity, NVIDIA Isaac, and Vision-Language-Action systems
  - Updated educational content standards to emphasize embodied intelligence
  - Incorporated the four modules reference into the development workflow
  - Updated RAG behavior rules to enforce the required response pattern

  The constitution now properly governs the development of a RAG chatbot specifically for the Physical AI & Humanoid Robotics textbook.
outcome: |
  The project constitution has been successfully updated to align with the Physical AI & Humanoid Robotics RAG Chatbot project. Version was incremented from v1.0.0 to v1.1.0 to reflect the significant scope change from a general AI/Spec-Driven book to a specific robotics textbook. All core principles were updated to reflect the new project focus while maintaining the spec-first workflow methodology.
evaluation: |
  The constitution update successfully transforms the governance document from a general AI/Spec-Driven book project to the specific Physical AI & Humanoid Robotics RAG Chatbot project. All required elements from the user input have been incorporated, including the four modules, target audience, scope limitations, and RAG behavior rules. The versioning follows semantic versioning with a minor bump for the significant scope expansion.
---
