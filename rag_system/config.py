"""
Configuration file for the Physical AI & Humanoid Robotics RAG System
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RAGConfig:
    """Configuration class for RAG system parameters"""

    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Vector database settings
    vector_db_persist_dir: str = "./chroma_db"
    search_k: int = 4  # Number of documents to retrieve

    # LLM settings
    llm_model_name: str = "microsoft/DialoGPT-small"
    max_new_tokens: int = 100
    temperature: float = 0.7

    # API settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Textbook content paths
    textbook_paths: list = None

    def __post_init__(self):
        if self.textbook_paths is None:
            self.textbook_paths = [
                "docs/intro.md",
                "docs/module-1-ros2/nodes-topics-services.md",
                "docs/module-1-ros2/ai-ros-integration.md",
                "docs/module-1-ros2/urdf-structure.md",
                "docs/module-2-simulation/index.md",
                "docs/module-2-simulation/digital-twin-concept.md",
                "docs/module-3-ai-robot-brain/index.md",
                "docs/module-3-ai-robot-brain/isaac-sim.md",
                "docs/module-3-ai-robot-brain/synthetic-data.md",
                "docs/module-3-ai-robot-brain/isaac-ros.md",
                "docs/module-3-ai-robot-brain/vslam-navigation.md",
                "docs/module-4-vla/index.md",
                "docs/module-4-vla/vla-concept.md",
                "docs/module-4-vla/voice-to-action.md",
                "docs/module-4-vla/llm-planning.md",
                "docs/module-4-vla/command-translation.md",
                "docs/module-4-vla/capstone-project.md"
            ]

# Create default configuration
config = RAGConfig()

def get_config() -> RAGConfig:
    """Get the current configuration"""
    return config

# Environment-specific configurations
def get_env_config() -> RAGConfig:
    """Get configuration based on environment variables"""
    env_config = RAGConfig()

    # Override defaults with environment variables if present
    env_config.host = os.getenv("RAG_HOST", env_config.host)
    env_config.port = int(os.getenv("RAG_PORT", env_config.port))
    env_config.debug = os.getenv("RAG_DEBUG", str(env_config.debug)).lower() == "true"
    env_config.chunk_size = int(os.getenv("RAG_CHUNK_SIZE", env_config.chunk_size))
    env_config.search_k = int(os.getenv("RAG_SEARCH_K", env_config.search_k))

    return env_config