# Development Environment Setup

This document provides instructions for setting up the development environment for the Physical AI & Humanoid Robotics textbook project.

## Prerequisites

- Node.js (version 18 or higher)
- npm (comes with Node.js)
- Git
- A text editor or IDE (VS Code recommended)

## Initial Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd my-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development Workflow

### Starting the Development Server

To start the Docusaurus development server:

```bash
npm start
```

This will start the server at `http://localhost:3000/my-book/` and automatically open your browser to the site.

### Building the Site

To build the static site for production:

```bash
npm run build
```

The built site will be available in the `build/` directory.

### Deploying to GitHub Pages

To deploy to GitHub Pages:

```bash
npm run deploy
```

## Project Structure

```
my-book/
├── docs/                 # Documentation content (textbook modules)
│   ├── intro.md          # Introduction page
│   ├── module-1-ros2/    # Module 1 content
│   ├── module-2-simulation/ # Module 2 content
│   ├── module-3-perception/ # Module 3 content
│   └── module-4-vla/     # Module 4 content
├── src/                  # Custom React components and CSS
│   ├── components/       # React components (e.g., Chatbot)
│   └── css/              # Custom CSS styles
├── static/               # Static assets (images, files)
├── docusaurus.config.js  # Docusaurus configuration
├── sidebars.js           # Navigation sidebar configuration
├── package.json          # Project dependencies and scripts
├── README.md             # Project overview
└── DEVELOPMENT.md        # This file
```

## Content Creation Guidelines

### Writing Modules

Each module should:
- Be between 1500-2000 words
- Use simple English without advanced mathematics
- Focus on conceptual understanding over heavy code
- Include diagrams and examples where helpful
- Have clear learning objectives

### File Structure

Module content should be organized as follows:
```
docs/module-1-ros2/
├── index.md              # Module introduction and overview
├── concepts.md           # Core concepts for this module
├── advanced-topics.md    # Advanced topics (if needed)
└── examples.md           # Practical examples
```

## Working with Docusaurus

### Adding New Pages

To add a new page to the documentation:
1. Create a new `.md` file in the appropriate directory
2. Add it to the sidebar in `sidebars.js`
3. Ensure it has proper frontmatter (at minimum: `---`)

### Frontmatter Example

```markdown
---
sidebar_position: 2
title: My Page Title
description: Brief description of the page content
---

# My Page Title

Content goes here...
```

## Environment Variables

For the RAG chatbot functionality, you may need to set up environment variables in a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

## Troubleshooting

### Common Issues

1. **Module not found errors**: Run `npm install` to ensure all dependencies are installed
2. **Port already in use**: The development server uses port 3000 by default. Use `npm start -- --port <new_port>` to use a different port
3. **Build fails**: Clear the cache with `npm run clear` and try building again

### Clearing Cache

To clear Docusaurus cache:
```bash
npm run clear
```

## Contributing

1. Create a feature branch for your changes
2. Make your changes following the content guidelines
3. Test your changes locally with `npm start`
4. Commit your changes with clear commit messages
5. Submit a pull request