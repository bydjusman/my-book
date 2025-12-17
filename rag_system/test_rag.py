"""
Simple test script for the Physical AI & Humanoid Robotics RAG System
"""

import requests
import json
import time

def test_rag_system():
    """Test the RAG system endpoints"""

    base_url = "http://localhost:8000"

    print("Testing Physical AI & Humanoid Robotics RAG System")
    print("=" * 50)

    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Status: {health_data['status']}")
            print(f"   Vectorstore: {health_data['vectorstore']}")
            print(f"   QA Chain: {health_data['qa_chain']}")
        else:
            print(f"   Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   Error during health check: {e}")

    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            root_data = response.json()
            print(f"   Message: {root_data['message']}")
            print(f"   Status: {root_data['status']}")
        else:
            print(f"   Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   Error during root endpoint test: {e}")

    # Test 3: Ask a question (this might take a moment to process)
    print("\n3. Testing question answering...")
    try:
        question = "What is ROS 2?"
        print(f"   Asking: '{question}'")

        # Using GET parameters for simplicity in this test
        params = {
            "question": question,
            "max_tokens": 150,
            "temperature": 0.7
        }

        response = requests.post(f"{base_url}/ask", params=params)

        if response.status_code == 200:
            result = response.json()
            print(f"   Question: {result['question']}")
            print(f"   Answer: {result['answer'][:200]}...")  # Truncate for readability

            if result['sources']:
                print(f"   Sources: Found {len(result['sources'])} source documents")
        else:
            print(f"   Question answering failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error during question answering test: {e}")

    # Test 4: Another question about the textbook
    print("\n4. Testing another question...")
    try:
        question = "Explain digital twins in robotics"
        print(f"   Asking: '{question}'")

        params = {
            "question": question,
            "max_tokens": 200,
            "temperature": 0.7
        }

        response = requests.post(f"{base_url}/ask", params=params)

        if response.status_code == 200:
            result = response.json()
            print(f"   Question: {result['question']}")
            print(f"   Answer: {result['answer'][:300]}...")  # Truncate for readability
        else:
            print(f"   Question answering failed with status {response.status_code}")
    except Exception as e:
        print(f"   Error during second question test: {e}")

    print("\n" + "=" * 50)
    print("Test completed. Note: The RAG system needs to be running at", base_url)

if __name__ == "__main__":
    test_rag_system()