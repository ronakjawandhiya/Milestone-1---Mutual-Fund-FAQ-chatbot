import json

def test_comprehensive_database():
    """Test the comprehensive database with specific fund queries"""
    
    # Load the database
    with open('mf_faq_data.json', 'r') as f:
        faq_data = json.load(f)
    
    print(f"Total FAQ entries in database: {len(faq_data)}")
    
    # Test queries for specific funds
    test_queries = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the expense ratio of ICICI Prudential Large Cap Fund?",
        "What is the expense ratio of ICICI Prudential Multi-Asset Fund?",
        "What is the expense ratio of ICICI Prudential Bluechip Fund?",
        "What is the expense ratio of ICICI Prudential Focused Equity Fund?",
        "What is the exit load for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the exit load for ICICI Prudential Large Cap Fund?",
        "What is the exit load for ICICI Prudential Multi-Asset Fund?",
        "What is the exit load for ICICI Prudential Bluechip Fund?",
        "What is the exit load for ICICI Prudential Focused Equity Fund?",
        "What is the minimum investment amount for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the minimum investment amount for ICICI Prudential Large Cap Fund?",
        "What is the minimum investment amount for ICICI Prudential Multi-Asset Fund?",
        "What is the minimum investment amount for ICICI Prudential Bluechip Fund?",
        "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?",
        "What is the benchmark for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the benchmark for ICICI Prudential Large Cap Fund?",
        "What is the benchmark for ICICI Prudential Multi-Asset Fund?",
        "What is the benchmark for ICICI Prudential Bluechip Fund?",
        "What is the benchmark for ICICI Prudential Focused Equity Fund?",
        "What is the riskometer rating for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the riskometer rating for ICICI Prudential Large Cap Fund?",
        "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
        "What is the riskometer rating for ICICI Prudential Bluechip Fund?",
        "What is the riskometer rating for ICICI Prudential Focused Equity Fund?",
        "What is the dividend yield of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the dividend yield of ICICI Prudential Large Cap Fund?",
        "What is the dividend yield of ICICI Prudential Multi-Asset Fund?",
        "What is the dividend yield of ICICI Prudential Bluechip Fund?",
        "What is the dividend yield of ICICI Prudential Focused Equity Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential Large Cap Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential Multi-Asset Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential Bluechip Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential Focused Equity Fund?",
        "What is the asset allocation of ICICI Prudential Multi-Asset Fund?"
    ]
    
    # Test the database
    found_entries = 0
    for query in test_queries:
        for entry in faq_data:
            if entry["question"].lower() == query.lower():
                found_entries += 1
                print(f"✓ Found: {entry['question']}")
                print(f"  Answer: {entry['answer'][:100]}...")
                print(f"  Source: {entry['source']}")
                print()
                break
        else:
            print(f"✗ Not found: {query}")
            print()
    
    print(f"Found {found_entries} out of {len(test_queries)} test queries")
    
    # Show some sample entries
    print("\nSample database entries:")
    for i, entry in enumerate(faq_data[:10]):
        print(f"{i+1}. {entry['question']}")
        print(f"   Source: {entry['source']}")
        print()

if __name__ == "__main__":
    test_comprehensive_database()