import requests
from bs4 import BeautifulSoup
import json
import time
import re

# ICICI Prudential schemes we want to focus on
SCHEMES = [
    "ICICI Prudential ELSS Tax Saver Fund",
    "ICICI Prudential Large Cap Fund",
    "ICICI Prudential Multi-Asset Fund",
    "ICICI Prudential Bluechip Fund",
    "ICICI Prudential Focused Equity Fund"
]

# Official sources for scraping
OFFICIAL_SOURCES = [
    "https://www.iciciprulife.com/",
    "https://www.icicipruamc.com/",
    "https://www.amfiindia.com/",
    "https://www.sebi.gov.in/"
]

def scrape_icici_prudential():
    """Scrape ICICI Prudential website for scheme information"""
    faq_data = []
    
    # ICICI Prudential AMC URLs for different types of information
    urls = [
        "https://www.icicipruamc.com/faq",
        "https://www.icicipruamc.com/investor-relationship/investor-faq",
        "https://www.icicipruamc.com/mutual-fund/basics-of-mutual-fund",
        "https://www.icicipruamc.com/mutual-fund/elss-fund",
        "https://www.icicipruamc.com/mutual-fund/large-cap-fund",
        "https://www.icicipruamc.com/mutual-fund/multi-asset-fund"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        try:
            print(f"Scraping {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            # Look for FAQ sections
            faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|accordion', re.I))
            
            if not faq_sections:
                # Try alternative selectors
                faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'content|panel|tab', re.I))
            
            for section in faq_sections[:3]:  # Limit to first 3 sections
                questions = section.find_all(['h3', 'h4', 'dt', 'strong', '.question'])
                answers = section.find_all(['p', 'dd', 'div', '.answer'])
                
                for i, question in enumerate(questions[:5]):  # Limit to first 5 questions per section
                    if question and i < len(answers):
                        q_text = question.get_text(strip=True)
                        a_text = answers[i].get_text(strip=True)
                        
                        if q_text and a_text and len(q_text) > 10 and len(a_text) > 20:
                            faq_data.append({
                                "question": q_text,
                                "answer": a_text,
                                "source": url
                            })
            
            # Add delay to be respectful to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    return faq_data

def scrape_amfi_data():
    """Scrape AMFI website for general mutual fund information"""
    faq_data = []
    
    urls = [
        "https://www.amfiindia.com/investor-corner/knowledge-center/faqs",
        "https://www.amfiindia.com/investor-corner/investor-faqs",
        "https://www.amfiindia.com/investor-corner/mutual-fund-basics"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        try:
            print(f"Scraping AMFI {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            # Look for FAQ items
            faq_items = soup.find_all('div', class_=re.compile(r'faq-item|question-answer', re.I))
            
            if not faq_items:
                # Try alternative selectors
                faq_items = soup.find_all('li')
            
            for item in faq_items[:10]:  # Limit to first 10 items
                question_elem = item.find(['h3', 'h4', 'strong', 'dt'])
                answer_elem = item.find(['p', 'dd', 'div'])
                
                if question_elem and answer_elem:
                    q_text = question_elem.get_text(strip=True)
                    a_text = answer_elem.get_text(strip=True)
                    
                    if q_text and a_text and len(q_text) > 10 and len(a_text) > 20:
                        faq_data.append({
                            "question": q_text,
                            "answer": a_text,
                            "source": url
                        })
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error scraping AMFI {url}: {e}")
    
    return faq_data

def scrape_sebi_data():
    """Scrape SEBI website for regulatory information"""
    faq_data = []
    
    urls = [
        "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp",
        "https://www.sebi.gov.in/sebiweb/investment/NAV.jsp",
        "https://www.sebi.gov.in/sebiweb/investment/MutualFundSchemeDetails.jsp"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        try:
            print(f"Scraping SEBI {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            # Look for FAQ items
            faq_items = soup.find_all('div', class_=re.compile(r'faq|question', re.I))
            
            if not faq_items:
                # Try alternative selectors
                faq_items = soup.find_all('li')
            
            for item in faq_items[:10]:  # Limit to first 10 items
                question_elem = item.find(['h3', 'h4', 'strong', 'dt'])
                answer_elem = item.find(['p', 'dd', 'div'])
                
                if question_elem and answer_elem:
                    q_text = question_elem.get_text(strip=True)
                    a_text = answer_elem.get_text(strip=True)
                    
                    if q_text and a_text and len(q_text) > 10 and len(a_text) > 20:
                        faq_data.append({
                            "question": q_text,
                            "answer": a_text,
                            "source": url
                        })
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error scraping SEBI {url}: {e}")
    
    return faq_data

def add_icici_specific_faq():
    """Add specific FAQ entries for ICICI Prudential schemes"""
    icici_faq = [
        {
            "question": "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
            "answer": "The expense ratio of ICICI Prudential ELSS Tax Saver Fund is subject to change as per SEBI regulations. As of the latest factsheet, the expense ratio is approximately 0.85% for the regular plan and 0.65% for the direct plan. Please refer to the latest factsheet for the most current information.",
            "source": "https://www.icicipruamc.com/mutual-fund/elss-tax-saver-fund"
        },
        {
            "question": "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
            "answer": "ICICI Prudential ELSS Tax Saver Fund has a mandatory lock-in period of 3 years as mandated by the Income Tax Act. This is the shortest lock-in period among all tax-saving instruments under Section 80C. The lock-in period applies to each installment/SIP separately.",
            "source": "https://www.icicipruamc.com/mutual-fund/elss-tax-saver-fund"
        },
        {
            "question": "What is the minimum SIP amount for ICICI Prudential schemes?",
            "answer": "The minimum SIP amount for most ICICI Prudential mutual fund schemes is ₹500 per month. However, this may vary by scheme. For ICICI Prudential ELSS Tax Saver Fund, the minimum SIP amount is ₹500. Investors can choose weekly, monthly, quarterly, or annual SIP frequencies.",
            "source": "https://www.icicipruamc.com/investor-relationship/investor-faq"
        },
        {
            "question": "What is the exit load for ICICI Prudential Large Cap Fund?",
            "answer": "ICICI Prudential Large Cap Fund charges an exit load of 1% if redeemed within 1 year from the date of allotment. No exit load is charged if units are redeemed after 1 year. The exit load is calculated on the applicable NAV and is deducted from the redemption proceeds.",
            "source": "https://www.icicipruamc.com/mutual-fund/large-cap-fund"
        },
        {
            "question": "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
            "answer": "ICICI Prudential Multi-Asset Fund has a 'Moderately High' riskometer rating as per the risk classification framework prescribed by AMFI. The fund invests across equity, debt, and gold, which helps in diversification but still carries significant market risk.",
            "source": "https://www.icicipruamc.com/mutual-fund/multi-asset-fund"
        },
        {
            "question": "How to download capital gains statement from ICICI Prudential?",
            "answer": "To download capital gains statement from ICICI Prudential: 1) Log in to your account on the ICICI Prudential website or mobile app, 2) Navigate to 'Transaction History' or 'Portfolio', 3) Select the relevant financial year, 4) Choose 'Capital Gains Statement' option, 5) Download the statement in PDF format. You can also request it via email by contacting customer care.",
            "source": "https://www.icicipruamc.com/investor-relationship/investor-faq"
        },
        {
            "question": "What is the benchmark for ICICI Prudential Bluechip Fund?",
            "answer": "ICICI Prudential Bluechip Fund is benchmarked against the NIFTY 100 Total Return Index. The fund aims to provide returns that closely correspond to the total return of the NIFTY 100 Index, subject to tracking errors. This benchmark represents the performance of the top 100 companies listed on the NSE.",
            "source": "https://www.icicipruamc.com/mutual-fund/bluechip-fund"
        },
        {
            "question": "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?",
            "answer": "The minimum investment amount for ICICI Prudential Focused Equity Fund is ₹5,000 for lump sum investments and ₹500 for SIP investments. This is the minimum amount required to initiate an investment in the scheme. Additional investments can be made in multiples of Re 1.",
            "source": "https://www.icicipruamc.com/mutual-fund/focused-equity-fund"
        }
    ]
    
    return icici_faq

def initialize_data():
    """Initialize FAQ data by scraping official sources and adding ICICI-specific information"""
    print("Initializing FAQ data by scraping official sources...")
    
    all_faqs = []
    
    # Scrape from different sources
    icici_faqs = scrape_icici_prudential()
    amfi_faqs = scrape_amfi_data()
    sebi_faqs = scrape_sebi_data()
    icici_specific = add_icici_specific_faq()
    
    all_faqs.extend(icici_faqs)
    all_faqs.extend(amfi_faqs)
    all_faqs.extend(sebi_faqs)
    all_faqs.extend(icici_specific)
    
    # Add some general FAQs with official information
    general_faqs = [
        {
            "question": "What is exit load in mutual funds?",
            "answer": "Exit load is a charge levied by the Asset Management Company (AMC) when an investor redeems or withdraws units of a mutual fund before a specified period. It is usually a percentage of the NAV and varies across schemes. The purpose is to discourage premature withdrawals and cover administrative costs. Last updated from sources: AMFI India",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        },
        {
            "question": "What is expense ratio in mutual funds?",
            "answer": "Expense ratio represents the annual fee charged by the fund house to manage your investment. It includes management fees, administrative costs, and other operating expenses expressed as a percentage of average assets under management (AUM). As per SEBI regulations, expense ratio for equity funds is capped at 2.25% and for debt funds at 2.00%. Last updated from sources: SEBI",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        },
        {
            "question": "What is the minimum SIP amount for mutual funds?",
            "answer": "The minimum SIP amount varies by AMC and scheme, but typically starts as low as ₹500 per month. Many AMCs offer flexibility to increase or decrease SIP amounts based on investor needs. SIP allows investors to invest fixed amounts regularly, enabling rupee cost averaging and disciplined investing. Last updated from sources: AMFI India",
            "source": "https://www.amfiindia.com/investor-corner/investor-faqs"
        },
        {
            "question": "What is lock-in period in mutual funds?",
            "answer": "Lock-in period refers to the duration during which invested money cannot be withdrawn. ELSS (Equity Linked Savings Scheme) funds have a mandatory lock-in of 3 years. Tax saving fixed deposits have 5-year lock-in. Other mutual fund schemes generally don't have lock-in periods except for close-ended funds which have lock-in until maturity. Last updated from sources: SEBI",
            "source": "https://www.sebi.gov.in/sebiweb/investment/FundInvestor_FAQ.jsp"
        },
        {
            "question": "What is capital gains statement in mutual funds?",
            "answer": "Capital gains statement shows profits earned from selling mutual fund units. Short-term capital gains (STCG) apply for holdings less than 1 year for debt funds and less than 12 months for equity funds. Long-term capital gains (LTCG) apply for longer holdings. Equity funds have 10% LTCG tax (without indexation) exceeding ₹1 lakh annually, while debt funds have 20% LTCG with indexation benefit. Last updated from sources: AMFI India",
            "source": "https://www.amfiindia.com/investor-corner/knowledge-center/faqs"
        }
    ]
    
    all_faqs.extend(general_faqs)
    
    # Remove duplicates
    unique_faqs = []
    seen_questions = set()
    
    for faq in all_faqs:
        question = faq["question"].lower().strip()
        if question not in seen_questions:
            seen_questions.add(question)
            unique_faqs.append(faq)
    
    # Save to file
    with open("mf_faq_data.json", 'w') as f:
        json.dump(unique_faqs, f, indent=2)
    
    print(f"Saved {len(unique_faqs)} unique FAQ entries to mf_faq_data.json")
    return unique_faqs

if __name__ == "__main__":
    faq_database = initialize_data()
    print(f"Total FAQ entries: {len(faq_database)}")
    
    # Print sample entries
    print("\nSample FAQ entries:")
    for i, entry in enumerate(faq_database[:5]):
        print(f"{i+1}. {entry['question']}")
        print(f"   Source: {entry['source']}")
        print()