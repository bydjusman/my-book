// Modules API routes

const express = require('express');
const router = express.Router();

// Placeholder route - will return available modules
// In later phases, this will connect to the actual module data
router.get('/', (req, res) => {
  res.json({
    modules: [
      {
        id: 'module-1-ros2',
        title: 'Module 1: The Robotic Nervous System (ROS 2)',
        description: 'Fundamentals of ROS 2 as the middleware connecting AI agents to robot controllers',
        wordCount: 0, // Will be updated when content is indexed
        lastIndexUpdate: 'N/A' // Will be updated when indexing is implemented
      },
      {
        id: 'module-2-simulation',
        title: 'Module 2: The Digital Twin (Gazebo & Unity)',
        description: 'Simulation techniques for safe robot development',
        wordCount: 0, // Will be updated when content is indexed
        lastIndexUpdate: 'N/A' // Will be updated when indexing is implemented
      },
      {
        id: 'module-3-perception',
        title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
        description: 'Advanced perception and navigation systems',
        wordCount: 0, // Will be updated when content is indexed
        lastIndexUpdate: 'N/A' // Will be updated when indexing is implemented
      },
      {
        id: 'module-4-vla',
        title: 'Module 4: Vision-Language-Action (VLA)',
        description: 'Control robots with natural language commands',
        wordCount: 0, // Will be updated when content is indexed
        lastIndexUpdate: 'N/A' // Will be updated when indexing is implemented
      }
    ]
  });
});

module.exports = router;