---
id: 2
title: update-constitution-again
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
  # Project Constitution: Physical AI & Humanoid Robotics RAG Chatbot

  ## Purpose
  This AI assistant answers questions strictly based on the textbook
  "Physical AI & Humanoid Robotics".

  ## Scope
  - ROS 2
  - Gazebo & Unity
  - NVIDIA Isaac Sim & Isaac ROS
  - Vision-Language-Action (VLA)
  - Humanoid robot simulation and control

  ## Audience
  - Beginner to intermediate students
  - Undergraduate CS and AI learners
  - No advanced mathematics

  ## Rules
  - Only answer using the provided book content
  - If information is missing, say: "This topic is not covered in the book"
  - Use simple English
  - Explain step-by-step
  - Prefer examples related to humanoid robots

  ## Style
  - Educational
  - Clear
  - Concise
  - Beginner-friendly
responseText: |
  Successfully updated the project constitution to v1.2.0 with the following changes:

  - Updated Robotics Tool Compliance principle to specifically include NVIDIA Isaac Sim & Isaac ROS and Vision-Language-Action (VLA) systems
  - Added "Humanoid robot simulation and control" to the technical stack
  - Updated Module 3 to specifically reference "NVIDIA Isaac Sim & Isaac ROS – AI Robot Brain"
  - Updated Module 4 to specifically reference "Vision-Language-Action (VLA) – LLMs + Robotics"
  - Updated the RAG behavior rule to use the exact phrase "This topic is not covered in the book" as specified
  - Updated Technical Standards to emphasize using examples related to humanoid robots
  - Updated Governance section to use the exact response phrase as specified

  The constitution now more accurately reflects the specific technologies and scope outlined in the user's requirements.
outcome: |
  The project constitution has been successfully updated to v1.2.0, incorporating the specific technologies (Isaac Sim & Isaac ROS, VLA) and exact response patterns requested. The version was incremented to reflect the addition of specific technology details and refinement of the RAG behavior rules.
evaluation: |
  The constitution update successfully incorporates the specific technology stack mentioned in the user input, including NVIDIA Isaac Sim & Isaac ROS, Vision-Language-Action (VLA), and humanoid robot simulation and control. The response pattern has been updated to match exactly what was specified in the requirements. All changes align with the project's educational focus on humanoid robotics.
---
