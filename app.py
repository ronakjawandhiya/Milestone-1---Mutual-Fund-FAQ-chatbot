import requests
from bs4 import BeautifulSoup
import json
import os
from flask import Flask, jsonify, request
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Data storage file
DATA_FILE = "mf_faq_data.json"

# Official sources for mutual fund information
OFFICIAL_SOURCES = [
    "https://www.amfiindia.com/investor-corner/knowledge-center/faqs",
    "https://www.amfiindia.com/investor-corner/investor-faqs",
    "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
]

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
    "sip vs lumpsum",
    "net asset value",
    "fund manager",
    "portfolio",
    "aum",
    "benchmark",
    "diversification",
    "risk profile",
    "return expectation",
    "fund category",
    "fund house"
]

def scrape_amfi_faqs():
    """Scrape FAQs from AMFI website"""
    faq_data = []
    
    # Scrape from AMFI investor corner
    try:
        url = "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        
        # Look for FAQ sections
        faq_sections = soup.find_all(['div', 'section'], class_=['faq', 'accordion'])
        if not faq_sections:
            # Try alternative selectors
            faq_sections = soup.find_all('div', class_=['content', 'panel'])
            
        for section in faq_sections[:5]:  # Limit to first 5 sections
            questions = section.find_all(['h3', 'h4', 'dt', 'strong'])
            answers = section.find_all(['p', 'dd', 'div'], class_=['answer', 'content'])
            
            for i, question in enumerate(questions[:3]):  # Limit to first 3 questions per section
                if question and i < len(answers):
                    q_text = question.get_text(strip=True)
                    a_text = answers[i].get_text(strip=True)
                    
                    if q_text and a_text:
                        faq_data.append({
                            "question": q_text,
                            "answer": a_text,
                            "source": url
                        })
                        
    except Exception as e:
        print(f"Error scraping AMFI: {e}")
    
    return faq_data

def scrape_sebi_faqs():
    """Scrape FAQs from SEBI website"""
    faq_data = []
    
    try:
        url = "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        
        # Look for FAQ items
        faq_items = soup.find_all('div', class_=['faq-item', 'question-answer'])
        if not faq_items:
            # Try alternative selectors
            faq_items = soup.find_all('li')
            
        for item in faq_items[:10]:  # Limit to first 10 items
            question_elem = item.find(['h3', 'h4', 'strong', 'dt'])
            answer_elem = item.find(['p', 'dd', 'div'])
            
            if question_elem and answer_elem:
                q_text = question_elem.get_text(strip=True)
                a_text = answer_elem.get_text(strip=True)
                
                if q_text and a_text:
                    faq_data.append({
                        "question": q_text,
                        "answer": a_text,
                        "source": url
                    })
                    
    except Exception as e:
        print(f"Error scraping SEBI: {e}")
    
    return faq_data

def initialize_data():
    """Initialize FAQ data by scraping official sources"""
    print("Initializing FAQ data by scraping official sources...")
    
    all_faqs = []
    
    # Scrape from different sources
    amfi_faqs = scrape_amfi_faqs()
    sebi_faqs = scrape_sebi_faqs()
    
    all_faqs.extend(amfi_faqs)
    all_faqs.extend(sebi_faqs)
    
    # Add some predefined FAQs with official information
    predefined_faqs = [
        {
            "question": "What is exit load in mutual funds?",
            "answer": "Exit load is a charge levied by the Asset Management Company (AMC) when an investor redeems or withdraws units of a mutual fund before a specified period. It is usually a percentage of the NAV and varies across schemes. The purpose is to discourage premature withdrawals and cover administrative costs.",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        },
        {
            "question": "What is expense ratio in mutual funds?",
            "answer": "Expense ratio represents the annual fee charged by the fund house to manage your investment. It includes management fees, administrative costs, and other operating expenses expressed as a percentage of average assets under management (AUM). As per SEBI regulations, expense ratio for equity funds is capped at 2.25% and for debt funds at 2.00%.",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        },
        {
            "question": "What is the minimum SIP amount for mutual funds?",
            "answer": "The minimum SIP amount varies by AMC and scheme, but typically starts as low as ₹500 per month. Many AMCs offer flexibility to increase or decrease SIP amounts based on investor needs. SIP allows investors to invest fixed amounts regularly, enabling rupee cost averaging and disciplined investing.",
            "source": "https://www.amfiindia.com/investor-corner/investor-faqs"
        },
        {
            "question": "What is lock-in period in mutual funds?",
            "answer": "Lock-in period refers to the duration during which invested money cannot be withdrawn. ELSS (Equity Linked Savings Scheme) funds have a mandatory lock-in of 3 years. Tax saving fixed deposits have 5-year lock-in. Other mutual fund schemes generally don't have lock-in periods except for close-ended funds which have lock-in until maturity.",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        },
        {
            "question": "What is capital gains statement in mutual funds?",
            "answer": "Capital gains statement shows profits earned from selling mutual fund units. Short-term capital gains (STCG) apply for holdings less than 1 year for debt funds and less than 12 months for equity funds. Long-term capital gains (LTCG) apply for longer holdings. Equity funds have 10% LTCG tax (without indexation) exceeding ₹1 lakh annually, while debt funds have 20% LTCG with indexation benefit.",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        },
        {
            "question": "What is Net Asset Value (NAV) in mutual funds?",
            "answer": "Net Asset Value (NAV) represents the per unit market value of a mutual fund scheme. It is calculated by dividing the difference between the firm's total assets and liabilities by the number of outstanding units in the fund. NAV changes daily based on the market value of the securities held by the scheme.",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        },
        {
            "question": "What is the difference between SIP and lump sum investment in mutual funds?",
            "answer": "Systematic Investment Plan (SIP) allows investors to invest a fixed amount regularly (monthly/quarterly) regardless of market conditions, enabling rupee cost averaging. Lump sum investment involves investing the entire amount at one go. SIP reduces the impact of market volatility and instills discipline, while lump sum investment requires market timing skills.",
            "source": "https://www.amfiindia.com/investor-corner/investor-faqs"
        },
        {
            "question": "What are the different types of mutual funds?",
            "answer": "Mutual funds are broadly classified into: 1) Equity Funds (invest primarily in stocks), 2) Debt Funds (invest in fixed income securities), 3) Hybrid Funds (invest in both equity and debt), 4) Solution-oriented Funds (like retirement or children's funds with lock-in), and 5) Other Funds (like Fund of Funds, Index Funds). Each type has different risk-return profiles.",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        },
        {
            "question": "What is ELSS and what are its benefits?",
            "answer": "ELSS (Equity Linked Savings Scheme) is a type of equity mutual fund that offers tax benefits under Section 80C of the Income Tax Act. It has a mandatory lock-in period of 3 years, which is the shortest among all tax-saving instruments. ELSS offers dual benefits of tax savings and wealth creation through equity investment.",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        },
        {
            "question": "How are mutual funds taxed?",
            "answer": "Mutual fund gains are taxed as capital gains. For equity funds: Short-term gains (holding < 12 months) are taxed at 15%; Long-term gains (> 12 months) exceeding ₹1 lakh per year are taxed at 10%. For debt funds: Short-term gains (holding < 36 months) are added to income and taxed at slab rates; Long-term gains (> 36 months) are taxed at 20% with indexation benefit.",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        }
    ]
    
    all_faqs.extend(predefined_faqs)
    
    # Save to file
    with open(DATA_FILE, 'w') as f:
        json.dump(all_faqs, f, indent=2)
    
    print(f"Saved {len(all_faqs)} FAQ entries to {DATA_FILE}")
    return all_faqs

def load_faq_data():
    """Load FAQ data from file or initialize if not present"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return initialize_data()

# Load FAQ data on startup
faq_database = load_faq_data()

def find_relevant_faq(question):
    """Find the most relevant FAQ entry for a given question"""
    question_lower = question.lower()
    
    # First try exact matching
    for entry in faq_database:
        if question_lower in entry['question'].lower() or \
           entry['question'].lower() in question_lower:
            return entry
    
    # Then try keyword matching with scoring
    best_match = None
    best_score = 0
    
    for entry in faq_database:
        # Count matching keywords
        score = 0
        entry_question_lower = entry['question'].lower()
        
        for topic in FAQ_TOPICS:
            if topic in question_lower and topic in entry_question_lower:
                score += 1
        
        # Update best match if this entry has a higher score
        if score > best_score:
            best_score = score
            best_match = entry
    
    # Return best match if found, otherwise first entry
    return best_match if best_match else (faq_database[0] if faq_database else None)


@app.route('/faq', methods=['GET'])
def get_faq():
    """API endpoint to get FAQ answer for a question"""
    question = request.args.get('question', '')
    logging.debug(f"Received question: {question}")
    
    if not question:
        logging.debug("No question provided")
        return jsonify({"error": "Please provide a question parameter"}), 400
    
    relevant_faq = find_relevant_faq(question)
    logging.debug(f"Found FAQ: {relevant_faq}")
    
    if relevant_faq:
        return jsonify(relevant_faq)
    else:
        return jsonify({
            "question": question,
            "answer": "Sorry, I couldn't find information about that. Please check official sources like AMFI or SEBI websites.",
            "source": "https://www.amfiindia.com/"
        })

@app.route('/topics', methods=['GET'])
def get_topics():
    """API endpoint to get available topics"""
    return jsonify({
        "topics": FAQ_TOPICS
    })

@app.route('/refresh-data', methods=['POST'])
def refresh_data():
    """API endpoint to refresh FAQ data from official sources"""
    global faq_database
    faq_database = initialize_data()
    return jsonify({"message": f"Refreshed FAQ data with {len(faq_database)} entries"})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logging.debug("Health check called")
    response = {
        "status": "healthy",
        "faq_count": len(faq_database),
        "sources": OFFICIAL_SOURCES
    }
    logging.debug(f"Health check response: {response}")
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)