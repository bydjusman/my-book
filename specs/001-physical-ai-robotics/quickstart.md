# Quickstart Guide: Physical AI & Humanoid Robotics Book

**Feature**: 001-physical-ai-robotics
**Date**: 2025-12-16

## Overview

This guide provides a quick setup and development workflow for the Physical AI & Humanoid Robotics textbook project. This project creates a Docusaurus-based documentation site with 4 modules covering ROS 2, simulation, AI perception, and Vision-Language-Action systems, integrated with a RAG chatbot.

## Prerequisites

- Node.js (v18 or higher)
- Git
- Basic command line knowledge
- GitHub account (for deployment)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <your-repository-url>
cd <repository-name>
npm install
```

### 2. Install Docusaurus

```bash
npm install @docusaurus/core@latest @docusaurus/preset-classic@latest
```

### 3. Project Structure

After setup, your project structure should look like:

```
my-book/
├── docs/
│   ├── intro.md
│   ├── module-1-ros2/
│   │   ├── index.md
│   │   └── ...
│   ├── module-2-simulation/
│   │   ├── index.md
│   │   └── ...
│   ├── module-3-perception/
│   │   ├── index.md
│   │   └── ...
│   └── module-4-vla/
│       ├── index.md
│       └── ...
├── src/
│   └── components/
│       └── Chatbot/
├── static/
├── docusaurus.config.js
├── package.json
└── README.md
```

### 4. Local Development

```bash
# Start local development server
npm run start

# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

## Creating Content Modules

### 1. Module 1: The Robotic Nervous System (ROS 2)

Create files in `docs/module-1-ros2/`:
- `index.md` - Main module page
- `concepts.md` - ROS 2 concepts, nodes, topics, services
- `examples.md` - Practical examples connecting AI to ROS

### 2. Module 2: The Digital Twin (Gazebo & Unity)

Create files in `docs/module-2-simulation/`:
- `index.md` - Main module page
- `gazebo.md` - Gazebo physics simulation
- `unity.md` - Unity high-fidelity rendering

### 3. Module 3: The AI-Robot Brain (NVIDIA Isaac™)

Create files in `docs/module-3-perception/`:
- `index.md` - Main module page
- `isaac.md` - NVIDIA Isaac tools and concepts
- `vslam.md` - Visual SLAM and navigation

### 4. Module 4: Vision-Language-Action (VLA)

Create files in `docs/module-4-vla/`:
- `index.md` - Main module page
- `voice-to-action.md` - Voice commands to robot actions
- `capstone.md` - End-to-end autonomous humanoid project

## RAG Chatbot Integration

### 1. Environment Setup

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 2. Chatbot Component

The chatbot component should be created in `src/components/Chatbot/Chatbot.jsx` and include:

- Document indexing functionality for book content
- Vector search against book content
- Response generation that only uses book content
- "Not found in book" response when content is missing

## Content Guidelines

### Writing Standards
- Use simple English, avoid advanced mathematics
- Focus on conceptual understanding over heavy code
- Each module should be 1500-2000 words
- Include diagrams to illustrate concepts
- Maintain beginner-friendly explanations

### Markdown Structure
```markdown
---
sidebar_position: 1
title: Module Title
description: Brief description of the module
---

# Module Title

## Learning Objectives
- Objective 1
- Objective 2

## Introduction
[Content here]

## Main Content
[Detailed content organized in sections]

## Summary
[Key takeaways from the module]
```

## Deployment

### GitHub Pages
1. Configure your `docusaurus.config.js` for GitHub Pages
2. Set up GitHub Actions for automatic deployment
3. Run `npm run deploy` to manually deploy

### Environment Variables
For production deployment, ensure environment variables are set in your hosting environment for the RAG system to function.

## Development Workflow

1. Create or edit Markdown files in the `docs/` directory
2. Run `npm run start` to preview changes locally
3. Test the RAG chatbot functionality
4. Commit changes to version control
5. Deploy to production when ready