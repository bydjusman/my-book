"""
Data loader module for the Physical AI & Humanoid Robotics RAG System
Handles loading and preprocessing of textbook content
"""

import os
from typing import List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TextbookDataLoader:
    """Class to handle loading and preprocessing of textbook content"""

    def __init__(self, base_path: str = "D:\\my-book"):
        """
        Initialize the data loader

        Args:
            base_path: Base path of the textbook repository
        """
        self.base_path = Path(base_path)
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

    def load_textbook_content(self) -> str:
        """
        Load content from all textbook markdown files

        Returns:
            Combined content from all textbook files
        """
        content_parts = []

        for file_path in self.textbook_paths:
            full_path = self.base_path / file_path

            if full_path.exists():
                try:
                    content = self._load_single_file(full_path)
                    if content:
                        # Add file identifier to help with source tracking
                        file_content = f"\n\n--- CONTENT FROM: {file_path} ---\n{content}\n--- END OF {file_path} ---\n"
                        content_parts.append(file_content)
                        logger.info(f"Loaded content from {file_path}")
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {str(e)}")
            else:
                logger.warning(f"File not found: {file_path}")

        return "".join(content_parts)

    def _load_single_file(self, file_path: Path) -> Optional[str]:
        """
        Load content from a single markdown file

        Args:
            file_path: Path to the markdown file

        Returns:
            Content of the file or None if error occurs
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove frontmatter if present (the YAML metadata at the beginning)
            if content.startswith("---"):
                # Find the end of frontmatter
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2]  # Take content after the second ---

            return content.strip()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return None

    def get_file_list(self) -> List[str]:
        """
        Get the list of textbook files that will be loaded

        Returns:
            List of file paths
        """
        return self.textbook_paths.copy()

    def validate_content(self, content: str) -> bool:
        """
        Basic validation of loaded content

        Args:
            content: Content to validate

        Returns:
            True if content appears valid, False otherwise
        """
        if not content:
            return False

        # Check if content has reasonable length
        if len(content) < 100:
            logger.warning("Loaded content appears to be very short")
            return False

        # Check for basic markdown elements that should be present in textbook
        required_elements = ["#", "##", "- ", "* "]  # Basic markdown indicators
        has_markdown = any(element in content for element in required_elements)

        if not has_markdown:
            logger.warning("Content doesn't appear to have expected markdown elements")

        return True

    def load_and_validate(self) -> Optional[str]:
        """
        Load and validate textbook content

        Returns:
            Validated content or None if validation fails
        """
        content = self.load_textbook_content()

        if self.validate_content(content):
            return content
        else:
            logger.error("Content validation failed")
            return None

# Convenience function for direct use
def load_textbook_content(base_path: str = "D:\\my-book") -> str:
    """
    Convenience function to load textbook content directly

    Args:
        base_path: Base path of the textbook repository

    Returns:
        Combined content from all textbook files
    """
    loader = TextbookDataLoader(base_path)
    return loader.load_textbook_content()