import requests
import time

# Test the frontend functionality by simulating user interactions
def test_frontend():
    print("Testing frontend functionality...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get('http://localhost:8000/health')
        data = response.json()
        print(f"   Status: {data['status']}")
        print(f"   FAQ Count: {data['faq_count']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Topics endpoint
    print("\n2. Testing topics endpoint...")
    try:
        response = requests.get('http://localhost:8000/topics')
        data = response.json()
        print(f"   Available topics: {len(data['topics'])}")
        print(f"   First 3 topics: {data['topics'][:3]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: FAQ queries
    print("\n3. Testing FAQ queries...")
    test_questions = [
        "What is exit load in mutual funds?",
        "What is expense ratio?",
        "What is the minimum SIP amount?",
        "What is lock-in period for ELSS funds?",
        "How are capital gains taxed in mutual funds?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        try:
            response = requests.get(f'http://localhost:8000/faq?question={question}')
            data = response.json()
            print(f"   {i}. Question: {question}")
            print(f"      Answer: {data['answer'][:100]}...")
            print(f"      Source: {data['source']}")
            print()
        except Exception as e:
            print(f"   {i}. Error with question '{question}': {e}")
    
    # Test 4: Edge cases
    print("4. Testing edge cases...")
    
    # Empty question
    try:
        response = requests.get('http://localhost:8000/faq?question=')
        data = response.json()
        print(f"   Empty question response: {data.get('question', 'N/A')}")
    except Exception as e:
        print(f"   Error with empty question: {e}")
    
    # Non-existent topic
    try:
        response = requests.get('http://localhost:8000/faq?question=What is cryptocurrency')
        data = response.json()
        print(f"   Non-existent topic response: {data.get('question', 'N/A')}")
    except Exception as e:
        print(f"   Error with non-existent topic: {e}")

if __name__ == "__main__":
    test_frontend()
    print("\nFrontend testing completed!")