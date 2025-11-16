import requests
import json

def test_api_endpoints():
    """Test all API endpoints"""
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Health check: {response.json()}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test topics endpoint
    print("Testing topics endpoint...")
    try:
        response = requests.get('http://localhost:5000/topics')
        topics = response.json()
        print(f"Available topics: {len(topics.get('topics', []))}")
        print(f"First 5 topics: {topics.get('topics', [])[:5]}")
    except Exception as e:
        print(f"Error testing topics endpoint: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test FAQ endpoint with various questions
    test_questions = [
        "What is exit load in mutual funds?",
        "What is expense ratio?",
        "What is the minimum SIP amount?",
        "What is lock-in period for ELSS funds?",
        "How are capital gains taxed in mutual funds?",
        "What is Net Asset Value (NAV)?",
        "SIP vs lump sum investment",
        "Types of mutual funds"
    ]
    
    print("Testing FAQ endpoint with sample questions...")
    for question in test_questions:
        try:
            response = requests.get(f'http://localhost:5000/faq?question={question}')
            data = response.json()
            print(f"Q: {question}")
            print(f"A: {data.get('answer', 'No answer')[:100]}...")
            print(f"Source: {data.get('source', 'No source')}")
            print("-" * 30)
        except Exception as e:
            print(f"Error testing question '{question}': {e}")

if __name__ == "__main__":
    test_api_endpoints()