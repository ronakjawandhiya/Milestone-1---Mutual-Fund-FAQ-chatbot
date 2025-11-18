import requests
import json

def test_streamlit_app():
    """Test the Streamlit app with fund-specific queries"""
    
    # Test URL (assuming the app is running on localhost:8505)
    base_url = "http://localhost:8505"
    
    # Test queries for specific funds
    test_queries = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the expense ratio of ICICI Prudential Large Cap Fund?",
        "What is the expense ratio of ICICI Prudential Multi-Asset Fund?",
        "What is the expense ratio of ICICI Prudential Bluechip Fund?",
        "What is the expense ratio of ICICI Prudential Focused Equity Fund?"
    ]
    
    print("Testing Streamlit app with fund-specific queries...")
    print("=" * 50)
    
    for query in test_queries:
        try:
            # Make a request to the app
            response = requests.get(f"{base_url}/faq", params={"question": query})
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Query: {query}")
                print(f"  Answer: {data['answer'][:100]}...")
                print(f"  Source: {data['source']}")
                print()
            else:
                print(f"✗ Query: {query}")
                print(f"  Error: HTTP {response.status_code}")
                print()
        except Exception as e:
            print(f"✗ Query: {query}")
            print(f"  Error: {str(e)}")
            print()
    
    print("Test completed.")

if __name__ == "__main__":
    test_streamlit_app()