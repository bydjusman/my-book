// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/index',
        'module-1-ros2/concepts',
        'module-1-ros2/nodes-topics-services',
        'module-1-ros2/ai-ros-integration',
        'module-1-ros2/urdf-structure'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-simulation/index',
        'module-2-simulation/digital-twin-concept',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-ai-robot-brain/index',
        'module-3-ai-robot-brain/isaac-sim',
        'module-3-ai-robot-brain/isaac-ros',
        'module-3-ai-robot-brain/synthetic-data',
        'module-3-ai-robot-brain/vslam-navigation',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vla/index',
        'module-4-vla/vla-concept',
        'module-4-vla/voice-to-action',
        'module-4-vla/llm-planning',
        'module-4-vla/command-translation',
        'module-4-vla/capstone-project',
      ],
    },
  ],
};

module.exports = sidebars;