import requests
import json
import urllib.parse

def test_enhanced_functionality():
    """Test all enhanced functionality of the ICICI Prudential FAQ bot"""
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        data = response.json()
        print(f"✓ Health check: {data}")
    except Exception as e:
        print(f"✗ Error testing health endpoint: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test topics endpoint
    print("Testing topics endpoint...")
    try:
        response = requests.get(f"{base_url}/topics")
        data = response.json()
        print(f"✓ Available topics: {len(data.get('topics', []))}")
        print(f"✓ Sample topics: {data.get('topics', [])[:5]}")
    except Exception as e:
        print(f"✗ Error testing topics endpoint: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test ICICI Prudential specific queries
    print("Testing ICICI Prudential specific queries...")
    icici_questions = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the minimum SIP amount for ICICI Prudential schemes?",
        "What is the exit load for ICICI Prudential Large Cap Fund?",
        "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
        "How to download capital gains statement from ICICI Prudential?",
        "What is the benchmark for ICICI Prudential Bluechip Fund?",
        "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?"
    ]
    
    for question in icici_questions:
        try:
            response = requests.get(f"{base_url}/faq?question={urllib.parse.quote(question)}")
            data = response.json()
            if "ICICI" in data.get("answer", "") or "icici" in data.get("source", ""):
                print(f"✓ {question}")
                print(f"  Answer: {data.get('answer', '')[:100]}...")
                print(f"  Source: {data.get('source', '')}")
            else:
                print(f"? {question} (may not be ICICI-specific)")
            print()
        except Exception as e:
            print(f"✗ Error testing question '{question}': {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test general mutual fund queries
    print("Testing general mutual fund queries...")
    general_questions = [
        "What is exit load in mutual funds?",
        "What is expense ratio?",
        "What is the minimum SIP amount?",
        "What is lock-in period for ELSS funds?",
        "How are capital gains taxed in mutual funds?"
    ]
    
    for question in general_questions:
        try:
            response = requests.get(f"{base_url}/faq?question={urllib.parse.quote(question)}")
            data = response.json()
            print(f"✓ {question}")
            print(f"  Answer: {data.get('answer', '')[:100]}...")
            print(f"  Source: {data.get('source', '')}")
            print()
        except Exception as e:
            print(f"✗ Error testing question '{question}': {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test opinionated question handling
    print("Testing opinionated question handling...")
    opinionated_questions = [
        "Should I buy ICICI Prudential ELSS Tax Saver Fund?",
        "Which is the best mutual fund to invest in?",
        "Is ICICI Prudential a good fund house?",
        "Can you recommend a portfolio for me?"
    ]
    
    for question in opinionated_questions:
        try:
            response = requests.get(f"{base_url}/faq?question={urllib.parse.quote(question)}")
            data = response.json()
            if "only provide factual information" in data.get("answer", ""):
                print(f"✓ Correctly refused: {question}")
                print(f"  Polite response: {data.get('answer', '')}")
                print(f"  Educational source: {data.get('source', '')}")
            else:
                print(f"? Unexpected response for: {question}")
            print()
        except Exception as e:
            print(f"✗ Error testing question '{question}': {e}")

if __name__ == "__main__":
    test_enhanced_functionality()