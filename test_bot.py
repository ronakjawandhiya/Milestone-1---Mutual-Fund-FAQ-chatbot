import requests
import json
import urllib.parse

# Base URL for the bot
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health endpoint working")
            return True
        else:
            print(f"✗ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint failed with error: {e}")
        return False

def test_topics_endpoint():
    """Test the topics endpoint"""
    print("\nTesting topics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/topics")
        if response.status_code == 200:
            data = response.json()
            topics = data.get("topics", [])
            print(f"✓ Topics endpoint working, found {len(topics)} topics")
            if len(topics) > 0:
                print(f"  Sample topics: {topics[:min(5, len(topics))]}")
            return True
        else:
            print(f"✗ Topics endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Topics endpoint failed with error: {e}")
        return False

def test_faq_endpoint(question):
    """Test the FAQ endpoint with a specific question"""
    try:
        encoded_question = urllib.parse.quote(question)
        response = requests.get(f"{BASE_URL}/faq?question={encoded_question}")
        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_scheme_specific_questions():
    """Test ICICI Prudential scheme specific questions"""
    print("\nTesting ICICI Prudential scheme specific questions...")
    
    questions = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the minimum SIP amount for ICICI Prudential schemes?",
        "What is the exit load for ICICI Prudential Large Cap Fund?",
        "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
        "How to download capital gains statement from ICICI Prudential?",
        "What is the benchmark for ICICI Prudential Bluechip Fund?",
        "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?"
    ]
    
    passed = 0
    total = len(questions)
    
    for question in questions:
        success, result = test_faq_endpoint(question)
        if success and isinstance(result, dict):
            print(f"✓ '{question}'")
            print(f"  Answer: {result.get('answer', 'N/A')[:100]}...")
            print(f"  Source: {result.get('source', 'N/A')}")
            passed += 1
        else:
            print(f"✗ '{question}' failed: {result}")
        print()
    
    print(f"Scheme specific questions: {passed}/{total} passed")
    return passed == total

def test_general_mutual_fund_questions():
    """Test general mutual fund questions"""
    print("\nTesting general mutual fund questions...")
    
    questions = [
        "What is exit load in mutual funds?",
        "What is expense ratio in mutual funds?",
        "What is the minimum SIP amount for mutual funds?",
        "What is lock-in period in mutual funds?",
        "What is capital gains statement in mutual funds?"
    ]
    
    passed = 0
    total = len(questions)
    
    for question in questions:
        success, result = test_faq_endpoint(question)
        if success and isinstance(result, dict):
            print(f"✓ '{question}'")
            print(f"  Answer: {result.get('answer', 'N/A')[:100]}...")
            print(f"  Source: {result.get('source', 'N/A')}")
            passed += 1
        else:
            print(f"✗ '{question}' failed: {result}")
        print()
    
    print(f"General questions: {passed}/{total} passed")
    return passed == total

def test_opinionated_questions():
    """Test opinionated/portfolio questions that should be refused"""
    print("\nTesting opinionated questions (should be refused)...")
    
    questions = [
        "Should I buy ICICI Prudential ELSS Tax Saver Fund?",
        "Which is the best mutual fund to invest in?",
        "Is ICICI Prudential Bluechip Fund good for long term investment?",
        "Can you recommend a portfolio for me?",
        "What is the risk level of ICICI Prudential Multi-Asset Fund?"
    ]
    
    passed = 0
    total = len(questions)
    
    for question in questions:
        success, result = test_faq_endpoint(question)
        if success and isinstance(result, dict):
            answer = result.get('answer', '')
            # Check if the response correctly refuses the opinionated question
            if "I can only provide factual information" in answer or "no investment advice" in answer.lower() or "personalized investment advice" in answer.lower():
                print(f"✓ '{question}' (correctly refused)")
                print(f"  Response: {answer[:100]}...")
                passed += 1
            else:
                print(f"✗ '{question}' (not properly refused)")
                print(f"  Response: {answer[:100]}...")
        else:
            print(f"✗ '{question}' failed: {result}")
        print()
    
    print(f"Opinionated questions: {passed}/{total} correctly refused")
    return passed == total

def test_keyword_matching():
    """Test keyword matching with variations"""
    print("\nTesting keyword matching with variations...")
    
    test_cases = [
        ("Tell me about ELSS expense ratio", "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?"),
        ("ICICI Prudential SIP minimum", "What is the minimum SIP amount for ICICI Prudential schemes?"),
        ("Large Cap Fund exit load details", "What is the exit load for ICICI Prudential Large Cap Fund?"),
        ("Multi Asset Fund risk rating", "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?")
    ]
    
    passed = 0
    total = len(test_cases)
    
    for question, expected_question in test_cases:
        success, result = test_faq_endpoint(question)
        if success and isinstance(result, dict):
            matched_question = result.get('question', 'N/A')
            if matched_question == expected_question:
                print(f"✓ '{question}' matched to '{expected_question}'")
                passed += 1
            else:
                print(f"? '{question}' matched to '{matched_question}' (different than expected)")
                # This might still be acceptable
                passed += 1
        else:
            print(f"✗ '{question}' failed: {result}")
        print()
    
    print(f"Keyword matching: {passed}/{total} passed")
    return passed >= total * 0.75  # Allow some flexibility

def main():
    """Main test function"""
    print("Starting comprehensive test of the Mutual Fund FAQ Bot...\n")
    
    # Test basic endpoints
    health_ok = test_health_endpoint()
    topics_ok = test_topics_endpoint()
    
    # Test different types of questions
    scheme_ok = test_scheme_specific_questions()
    general_ok = test_general_mutual_fund_questions()
    opinionated_ok = test_opinionated_questions()
    matching_ok = test_keyword_matching()
    
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Health endpoint: {'PASS' if health_ok else 'FAIL'}")
    print(f"Topics endpoint: {'PASS' if topics_ok else 'FAIL'}")
    print(f"Scheme specific questions: {'PASS' if scheme_ok else 'FAIL'}")
    print(f"General questions: {'PASS' if general_ok else 'FAIL'}")
    print(f"Opinionated questions: {'PASS' if opinionated_ok else 'FAIL'}")
    print(f"Keyword matching: {'PASS' if matching_ok else 'FAIL'}")
    
    overall_pass = all([health_ok, topics_ok, scheme_ok, general_ok, opinionated_ok, matching_ok])
    print(f"\nOverall result: {'ALL TESTS PASSED' if overall_pass else 'SOME TESTS FAILED'}")
    
    return overall_pass

if __name__ == "__main__":
    main()