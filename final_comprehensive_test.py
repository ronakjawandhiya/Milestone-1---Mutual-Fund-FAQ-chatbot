"""
Final comprehensive test script to verify that the Mutual Fund FAQ Assistant is working correctly
"""

import json
import sys

def test_database_comprehensiveness():
    """Test that the database is comprehensive and has fund-specific information"""
    
    # Load the database
    with open('mf_faq_data.json', 'r') as f:
        faq_data = json.load(f)
    
    print("=== Mutual Fund FAQ Assistant - Final Comprehensive Test ===")
    print(f"Total FAQ entries in database: {len(faq_data)}")
    
    # Check that we have enough entries
    if len(faq_data) < 40:
        print("❌ Database is not comprehensive enough")
        return False
    else:
        print("✅ Database has sufficient entries")
    
    # Check for fund-specific entries
    icici_schemes = [
        "ICICI Prudential ELSS Tax Saver Fund",
        "ICICI Prudential Large Cap Fund", 
        "ICICI Prudential Multi-Asset Fund",
        "ICICI Prudential Bluechip Fund",
        "ICICI Prudential Focused Equity Fund"
    ]
    
    fund_metrics = ["expense ratio", "exit load", "minimum investment", "benchmark", "riskometer", "dividend yield", "portfolio turnover"]
    
    fund_specific_entries = 0
    for scheme in icici_schemes:
        for metric in fund_metrics:
            for entry in faq_data:
                if scheme.lower() in entry["question"].lower() and metric in entry["question"].lower():
                    fund_specific_entries += 1
                    break
    
    print(f"Fund-specific entries found: {fund_specific_entries}")
    
    if fund_specific_entries < 30:
        print("❌ Not enough fund-specific entries")
        return False
    else:
        print("✅ Sufficient fund-specific entries")
    
    # Check for source URLs
    entries_with_sources = 0
    for entry in faq_data:
        if "source" in entry and entry["source"] and entry["source"].startswith("http"):
            entries_with_sources += 1
    
    print(f"Entries with valid sources: {entries_with_sources}/{len(faq_data)}")
    
    if entries_with_sources < len(faq_data) * 0.8:
        print("❌ Too many entries without valid sources")
        return False
    else:
        print("✅ Most entries have valid sources")
    
    # Check for opinion filtering
    from streamlit_app import find_relevant_faq
    
    opinionated_question = "Should I buy ICICI Prudential ELSS Tax Saver Fund?"
    result = find_relevant_faq(opinionated_question)
    
    if "I can only provide factual information" in result["answer"]:
        print("✅ Opinion filtering working correctly")
    else:
        print("❌ Opinion filtering not working correctly")
        return False
    
    # Test fund-specific queries
    test_queries = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the expense ratio of ICICI Prudential Large Cap Fund?",
        "What is the exit load for ICICI Prudential Multi-Asset Fund?",
        "What is the minimum investment amount for ICICI Prudential Bluechip Fund?",
        "What is the benchmark for ICICI Prudential Focused Equity Fund?",
        "What is the riskometer rating for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the dividend yield of ICICI Prudential Large Cap Fund?",
        "What is the portfolio turnover ratio for ICICI Prudential Focused Equity Fund?"
    ]
    
    correct_matches = 0
    for query in test_queries:
        result = find_relevant_faq(query)
        if result and query.lower() == result["question"].lower():
            correct_matches += 1
    
    print(f"Correct fund-specific matches: {correct_matches}/{len(test_queries)}")
    
    if correct_matches < len(test_queries) * 0.8:
        print("❌ Fund-specific matching not working correctly")
        return False
    else:
        print("✅ Fund-specific matching working correctly")
    
    # Test general mutual fund concepts
    general_queries = [
        "What is expense ratio in mutual funds?",
        "What is exit load in mutual funds?",
        "What is lock-in period in mutual funds?",
        "What is capital gains statement in mutual funds?"
    ]
    
    general_matches = 0
    for query in general_queries:
        result = find_relevant_faq(query)
        if result:
            general_matches += 1
    
    print(f"General mutual fund concept matches: {general_matches}/{len(general_queries)}")
    
    if general_matches < len(general_queries) * 0.8:
        print("❌ General concept matching not working correctly")
        return False
    else:
        print("✅ General concept matching working correctly")
    
    print("\n=== All tests passed! ===")
    print("The Mutual Fund FAQ Assistant is working correctly.")
    print(f"Database contains {len(faq_data)} comprehensive entries covering all 5 ICICI Prudential schemes.")
    print("You can now run 'streamlit run streamlit_app.py' to start the application.")
    
    return True

if __name__ == "__main__":
    success = test_database_comprehensiveness()
    sys.exit(0 if success else 1)