import json

def find_relevant_faq(question):
    """Find the most relevant FAQ entry for a given question"""
    # Load the FAQ data
    with open('mf_faq_data.json', 'r') as f:
        faq_data = json.load(f)
    
    question_lower = question.lower()
    
    # First try exact match
    for entry in faq_data:
        if entry["question"].lower() == question_lower:
            return entry
    
    # Then try partial matching with boosting for ICICI Prudential funds
    best_match = None
    best_score = 0
    
    icici_schemes = [
        "icici prudential elss tax saver fund",
        "icici prudential large cap fund",
        "icici prudential multi-asset fund",
        "icici prudential bluechip fund",
        "icici prudential focused equity fund"
    ]
    
    for entry in faq_data:
        entry_question_lower = entry["question"].lower()
        score = 0
        
        # Check for exact word matches
        question_words = set(question_lower.split())
        entry_words = set(entry_question_lower.split())
        common_words = question_words.intersection(entry_words)
        score += len(common_words)
        
        # Boost score for ICICI Prudential scheme matches
        for scheme in icici_schemes:
            if scheme in question_lower and scheme in entry_question_lower:
                score += 10  # High boost for scheme matching
        
        if score > best_score:
            best_score = score
            best_match = entry
    
    return best_match if best_score > 0 else None

def test_faq_matching():
    """Test the FAQ matching function with fund-specific queries"""
    
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
    
    print("Testing FAQ matching function with fund-specific queries...")
    print("=" * 60)
    
    found_matches = 0
    for query in test_queries:
        result = find_relevant_faq(query)
        if result:
            found_matches += 1
            print(f"✓ Query: {query}")
            print(f"  Matched: {result['question']}")
            print(f"  Answer: {result['answer'][:100]}...")
            print(f"  Source: {result['source']}")
            print()
        else:
            print(f"✗ Query: {query}")
            print(f"  No match found")
            print()
    
    print(f"Found matches for {found_matches} out of {len(test_queries)} test queries")
    print(f"Success rate: {found_matches/len(test_queries)*100:.1f}%")

if __name__ == "__main__":
    test_faq_matching()