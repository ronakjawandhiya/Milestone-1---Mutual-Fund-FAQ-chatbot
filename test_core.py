import json
import os

# Load the FAQ data
DATA_FILE = "mf_faq_data.json"

def load_faq_data():
    """Load FAQ data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Pre-defined FAQ topics we want to cover
FAQ_TOPICS = [
    "exit load",
    "expense ratio", 
    "minimum sip",
    "lock in period",
    "capital gains",
    "elss funds",
    "debt funds",
    "equity funds",
    "hybrid funds",
    "mutual fund taxation",
    "redemption",
    "switching",
    "dividend payout",
    "growth option",
    "sip vs lumpsum"
]

def find_relevant_faq(question, faq_database):
    """Find the most relevant FAQ entry for a given question"""
    question_lower = question.lower()
    
    # First try exact matching
    for entry in faq_database:
        if question_lower in entry['question'].lower() or \
           entry['question'].lower() in question_lower:
            return entry
    
    # Then try keyword matching
    for topic in FAQ_TOPICS:
        if topic in question_lower:
            # Find entries related to this topic
            for entry in faq_database:
                if topic in entry['question'].lower():
                    return entry
    
    # Return a general entry if no specific match found
    return faq_database[0] if faq_database else None

# Load FAQ data
faq_database = load_faq_data()
print(f"Loaded {len(faq_database)} FAQ entries")

# Test with some sample questions
test_questions = [
    "What is exit load in mutual funds?",
    "What is expense ratio?",
    "What is the minimum SIP amount?",
    "What is lock-in period for ELSS funds?",
    "How are capital gains taxed in mutual funds?"
]

for question in test_questions:
    result = find_relevant_faq(question, faq_database)
    print(f"\nQuestion: {question}")
    if result:
        print(f"Answer: {result['answer']}")
        print(f"Source: {result['source']}")
    else:
        print("No matching FAQ found")