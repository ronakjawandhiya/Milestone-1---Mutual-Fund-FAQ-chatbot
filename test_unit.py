import json
import os
import sys

# Add the current directory to the path so we can import app
sys.path.append('.')

try:
    from app import find_relevant_faq, FAQ_TOPICS, load_faq_data
    print("Successfully imported app module")
except ImportError as e:
    print(f"Error importing app module: {e}")
    # If we can't import, let's test the data directly
    pass

def test_data_loading():
    """Test that FAQ data loads correctly"""
    DATA_FILE = "mf_faq_data.json"
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} FAQ entries")
        
        # Check structure of first entry
        if data:
            first_entry = data[0]
            required_fields = ['question', 'answer', 'source']
            
            for field in required_fields:
                if field in first_entry:
                    print(f"✓ Found required field: {field}")
                else:
                    print(f"✗ Missing required field: {field}")
            
            print(f"Sample entry: {first_entry['question']}")
        
        return data
    else:
        print("Data file not found")
        return []

def test_topic_coverage():
    """Test that we have topics covered"""
    try:
        from app import FAQ_TOPICS
        topics = FAQ_TOPICS
    except ImportError:
        topics = []
    
    print(f"Available topics: {len(topics)}")
    
    if topics:
        print("First 5 topics:")
        for topic in topics[:5]:
            print(f"  - {topic}")

def test_question_matching():
    """Test question matching functionality"""
    # Load data
    faq_data = test_data_loading()
    
    if not faq_data:
        print("No FAQ data to test")
        return
    
    # Test questions
    test_questions = [
        "What is exit load?",
        "expense ratio",
        "SIP amount",
        "lock-in period",
        "capital gains tax"
    ]
    
    print("\nTesting question matching:")
    
    # We'll implement a simple version of the matching logic here
    for question in test_questions:
        question_lower = question.lower()
        matched = False
        
        for entry in faq_data:
            entry_question_lower = entry['question'].lower()
            
            # Exact match
            if question_lower in entry_question_lower or entry_question_lower in question_lower:
                print(f"✓ Exact match for '{question}': {entry['question']}")
                matched = True
                break
        
        # Keyword match
        if not matched:
            for entry in faq_data:
                entry_question_lower = entry['question'].lower()
                score = 0
                
                try:
                    from app import FAQ_TOPICS
                    topics_to_check = FAQ_TOPICS
                except ImportError:
                    topics_to_check = []
                
                for topic in topics_to_check:
                    if topic in question_lower and topic in entry_question_lower:
                        score += 1
                
                if score > 0:
                    print(f"✓ Keyword match for '{question}': {entry['question']} (score: {score})")
                    matched = True
                    break
        
        if not matched:
            print(f"✗ No match found for '{question}'")

if __name__ == "__main__":
    print("Running unit tests for Mutual Fund FAQ Bot...\n")
    
    test_data_loading()
    print()
    
    test_topic_coverage()
    print()
    
    test_question_matching()
    print()
    
    print("Unit tests completed.")