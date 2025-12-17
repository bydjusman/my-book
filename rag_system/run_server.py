"""
Script to run the Physical AI & Humanoid Robotics RAG System
"""

import uvicorn
import sys
import os
from config import get_env_config

def main():
    """Main function to run the RAG system server"""

    # Get configuration
    config = get_env_config()

    print("Starting Physical AI & Humanoid Robotics RAG System...")
    print(f"Server will run on {config.host}:{config.port}")
    print(f"Debug mode: {config.debug}")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Run the server
        uvicorn.run(
            "main:app",
            host=config.host,
            port=config.port,
            reload=config.debug,  # Auto-reload in debug mode
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()