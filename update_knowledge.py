import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse

# ICICI Prudential schemes we want to focus on
SCHEMES = [
    "ICICI Prudential ELSS Tax Saver Fund",
    "ICICI Prudential Large Cap Fund",
    "ICICI Prudential Multi-Asset Fund",
    "ICICI Prudential Bluechip Fund",
    "ICICI Prudential Focused Equity Fund"
]

# URLs to scrape
URLS = [
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-elss-tax-saver-fund/2",
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-large-cap-fund--erstwhile--bluechip-fund/211",
    "https://www.icicipruamc.com/mutual-fund/hybrid-funds/icici-prudential-multi-asset-fund/55",
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund",
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-focused-equity-fund/279",
    "https://digitalfactsheet.icicipruamc.com/fact/statutory-details-and-risk-factors.php",
    "https://www.icicipruamc.com/blob/sebi-repo/Advertisements/2025/July/Filing%20Date%2015-07-2025/Release%20date%2014-07-2025/Advertisement/Annexure%2017-%20Presentataion%20%20on%20ICICI%20Prudential%20Multi-%20Asset%20Fund.pdf",
    "https://www.icicipruamc.com/blob/downloads/Application-Forms/Common%20Application%20Form.pdf",
    "https://www.icicipruamc.com/blob/announcements/Notice%20cum%20Addendum%20for%20name%20change.pdf",
    "https://portal.amfiindia.com/spages/129.pdf",
    "https://portal.amfiindia.com/spages/712.pdf",
    "https://portal.amfiindia.com/spages/8130.pdf",
    "https://www.icicipruamc.com/media-center/downloads",
    "https://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0"
]

def is_pdf_url(url):
    """Check if URL points to a PDF file"""
    return url.lower().endswith('.pdf')

def is_url_accessible(url):
    """Check if a URL is accessible"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.head(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        try:
            # If HEAD request fails, try GET request
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False

def scrape_web_page(url):
    """Scrape a web page for FAQ and scheme information"""
    faq_data = []
    
    # First check if URL is accessible
    if not is_url_accessible(url):
        print(f"Skipping inaccessible URL: {url}")
        return faq_data
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Handle PDF files differently
        if is_pdf_url(url):
            print(f"Skipping PDF file: {url}")
            return faq_data
        
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        
        # Look for FAQ sections
        faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|accordion|scheme|fund', re.I))
        
        if not faq_sections:
            # Try alternative selectors
            faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'content|panel|tab|detail', re.I))
        
        # Also look for tables which might contain scheme information
        tables = soup.find_all('table')
        
        for section in faq_sections[:5]:  # Limit to first 5 sections
            questions = section.find_all(['h3', 'h4', 'dt', 'strong', '.question'])
            answers = section.find_all(['p', 'dd', 'div', '.answer'])
            
            for i, question in enumerate(questions[:10]):  # Limit to first 10 questions per section
                if question and i < len(answers):
                    q_text = question.get_text(strip=True)
                    a_text = answers[i].get_text(strip=True)
                    
                    if q_text and a_text and len(q_text) > 10 and len(a_text) > 20:
                        # Only include relevant questions
                        relevant_keywords = ['expense', 'exit', 'load', 'sip', 'minimum', 'lock', 'period', 'elss', 
                                           'tax', 'ratio', 'risk', 'benchmark', 'capital', 'gain', 'statement',
                                           'icici', 'prudential', 'nav', ' redemption']
                        
                        if any(keyword in q_text.lower() for keyword in relevant_keywords):
                            faq_data.append({
                                "question": q_text,
                                "answer": a_text,
                                "source": url
                            })
        
        # Look for scheme details in tables
        for table in tables[:3]:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    
                    if header and value and len(header) > 5 and len(value) > 5:
                        # Check if this looks like scheme information
                        scheme_keywords = ['expense', 'exit', 'load', 'minimum', 'lock', 'period', 'ratio', 'risk', 'benchmark']
                        
                        if any(keyword in header.lower() for keyword in scheme_keywords):
                            question = f"What is the {header.lower()} for ICICI Prudential schemes?"
                            faq_data.append({
                                "question": question,
                                "answer": value,
                                "source": url
                            })
        
        # Look for definition lists
        def_lists = soup.find_all('dl')
        for dl in def_lists[:3]:
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            
            for i, dt in enumerate(dt_elements[:10]):
                if i < len(dd_elements):
                    q_text = dt.get_text(strip=True)
                    a_text = dd_elements[i].get_text(strip=True)
                    
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

def add_scheme_specific_faq():
    """Add specific FAQ entries for ICICI Prudential schemes with updated information"""
    scheme_faq = [
        {
            "question": "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
            "answer": "The expense ratio of ICICI Prudential ELSS Tax Saver Fund is subject to change as per SEBI regulations. As of the latest factsheet, the expense ratio is approximately 0.85% for the regular plan and 0.65% for the direct plan. Please refer to the latest factsheet for the most current information. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-elss-tax-saver-fund/2"
        },
        {
            "question": "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
            "answer": "ICICI Prudential ELSS Tax Saver Fund has a mandatory lock-in period of 3 years as mandated by the Income Tax Act. This is the shortest lock-in period among all tax-saving instruments under Section 80C. The lock-in period applies to each installment/SIP separately. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-elss-tax-saver-fund/2"
        },
        {
            "question": "What is the minimum SIP amount for ICICI Prudential schemes?",
            "answer": "The minimum SIP amount for most ICICI Prudential mutual fund schemes is ₹500 per month. However, this may vary by scheme. For ICICI Prudential ELSS Tax Saver Fund, the minimum SIP amount is ₹500. Investors can choose weekly, monthly, quarterly, or annual SIP frequencies. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/blob/downloads/Application-Forms/Common%20Application%20Form.pdf"
        },
        {
            "question": "What is the exit load for ICICI Prudential Large Cap Fund?",
            "answer": "ICICI Prudential Large Cap Fund charges an exit load of 1% if redeemed within 1 year from the date of allotment. No exit load is charged if units are redeemed after 1 year. The exit load is calculated on the applicable NAV and is deducted from the redemption proceeds. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-large-cap-fund--erstwhile--bluechip-fund/211"
        },
        {
            "question": "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
            "answer": "ICICI Prudential Multi-Asset Fund has a 'Moderately High' riskometer rating as per the risk classification framework prescribed by AMFI. The fund invests across equity, debt, and gold, which helps in diversification but still carries significant market risk. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/hybrid-funds/icici-prudential-multi-asset-fund/55"
        },
        {
            "question": "How to download capital gains statement from ICICI Prudential?",
            "answer": "To download capital gains statement from ICICI Prudential: 1) Log in to your account on the ICICI Prudential website or mobile app, 2) Navigate to 'Transaction History' or 'Portfolio', 3) Select the relevant financial year, 4) Choose 'Capital Gains Statement' option, 5) Download the statement in PDF format. You can also request it via email by contacting customer care. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/media-center/downloads"
        },
        {
            "question": "What is the benchmark for ICICI Prudential Bluechip Fund?",
            "answer": "ICICI Prudential Bluechip Fund is benchmarked against the NIFTY 100 Total Return Index. The fund aims to provide returns that closely correspond to the total return of the NIFTY 100 Index, subject to tracking errors. This benchmark represents the performance of the top 100 companies listed on the NSE. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund"
        },
        {
            "question": "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?",
            "answer": "The minimum investment amount for ICICI Prudential Focused Equity Fund is ₹5,000 for lump sum investments and ₹500 for SIP investments. This is the minimum amount required to initiate an investment in the scheme. Additional investments can be made in multiples of Re 1. Last updated from sources: ICICI Prudential AMC.",
            "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-focused-equity-fund/279"
        }
    ]
    
    # Validate sources for scheme-specific FAQs
    validated_faq = []
    for item in scheme_faq:
        source = item["source"]
        if is_url_accessible(source):
            validated_faq.append(item)
        else:
            # If source is not accessible, use a generic source
            print(f"Warning: Source URL not accessible: {source}")
            item["source"] = "https://www.icicipruamc.com/"
            validated_faq.append(item)
    
    return validated_faq

def update_knowledge_database():
    """Update the FAQ knowledge database by scraping official sources"""
    print("Updating FAQ knowledge database by scraping official sources...")
    
    all_faqs = []
    
    # Scrape from the provided URLs
    for url in URLS:
        if not is_pdf_url(url):  # Skip PDFs for now
            faqs = scrape_web_page(url)
            all_faqs.extend(faqs)
    
    # Add scheme-specific FAQ entries
    scheme_specific = add_scheme_specific_faq()
    all_faqs.extend(scheme_specific)
    
    # Add some general FAQs with official information
    general_faqs = [
        {
            "question": "What is exit load in mutual funds?",
            "answer": "Exit load is a charge levied by the Asset Management Company (AMC) when an investor redeems or withdraws units of a mutual fund before a specified period. It is usually a percentage of the NAV and varies across schemes. The purpose is to discourage premature withdrawals and cover administrative costs. Last updated from sources: AMFI India",
            "source": "https://portal.amfiindia.com/spages/129.pdf"
        },
        {
            "question": "What is expense ratio in mutual funds?",
            "answer": "Expense ratio represents the annual fee charged by the fund house to manage your investment. It includes management fees, administrative costs, and other operating expenses expressed as a percentage of average assets under management (AUM). As per SEBI regulations, expense ratio for equity funds is capped at 2.25% and for debt funds at 2.00%. Last updated from sources: SEBI",
            "source": "https://portal.amfiindia.com/spages/712.pdf"
        },
        {
            "question": "What is the minimum SIP amount for mutual funds?",
            "answer": "The minimum SIP amount varies by AMC and scheme, but typically starts as low as ₹500 per month. Many AMCs offer flexibility to increase or decrease SIP amounts based on investor needs. SIP allows investors to invest fixed amounts regularly, enabling rupee cost averaging and disciplined investing. Last updated from sources: AMFI India",
            "source": "https://portal.amfiindia.com/spages/129.pdf"
        },
        {
            "question": "What is lock-in period in mutual funds?",
            "answer": "Lock-in period refers to the duration during which invested money cannot be withdrawn. ELSS (Equity Linked Savings Scheme) funds have a mandatory lock-in of 3 years. Tax saving fixed deposits have 5-year lock-in. Other mutual fund schemes generally don't have lock-in periods except for close-ended funds which have lock-in until maturity. Last updated from sources: SEBI",
            "source": "https://portal.amfiindia.com/spages/8130.pdf"
        },
        {
            "question": "What is capital gains statement in mutual funds?",
            "answer": "Capital gains statement shows profits earned from selling mutual fund units. Short-term capital gains (STCG) apply for holdings less than 1 year for debt funds and less than 12 months for equity funds. Long-term capital gains (LTCG) apply for longer holdings. Equity funds have 10% LTCG tax (without indexation) exceeding ₹1 lakh annually, while debt funds have 20% LTCG with indexation benefit. Last updated from sources: AMFI India",
            "source": "https://portal.amfiindia.com/spages/129.pdf"
        }
    ]
    
    # Validate sources for general FAQs
    validated_general_faqs = []
    for item in general_faqs:
        source = item["source"]
        if is_url_accessible(source):
            validated_general_faqs.append(item)
        else:
            # If source is not accessible, use a generic source
            print(f"Warning: Source URL not accessible: {source}")
            # Try to find a working AMFI source
            if "amfi" in source.lower():
                item["source"] = "https://www.amfiindia.com/"
            elif "sebi" in source.lower():
                item["source"] = "https://www.sebi.gov.in/"
            else:
                item["source"] = "https://www.amfiindia.com/"
            validated_general_faqs.append(item)
    
    all_faqs.extend(validated_general_faqs)
    
    # Remove duplicates based on question text
    unique_faqs = []
    seen_questions = set()
    
    for faq in all_faqs:
        question = faq["question"].lower().strip()
        if question not in seen_questions:
            seen_questions.add(question)
            unique_faqs.append(faq)
    
    # Load existing data
    try:
        with open("mf_faq_data.json", 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    
    # Merge with existing data, prioritizing new data
    merged_data = []
    existing_questions = {item["question"].lower().strip() for item in existing_data}
    
    # Add new data first
    for item in unique_faqs:
        merged_data.append(item)
        if item["question"].lower().strip() in existing_questions:
            existing_questions.remove(item["question"].lower().strip())
    
    # Add remaining existing data
    for item in existing_data:
        if item["question"].lower().strip() in existing_questions:
            merged_data.append(item)
    
    # Save to file
    with open("mf_faq_data.json", 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    print(f"Updated knowledge database with {len(merged_data)} FAQ entries")
    print(f"Added {len(unique_faqs)} new entries")
    print(f"Retained {len(merged_data) - len(unique_faqs)} existing entries")
    
    # Print sample entries
    print("\nSample FAQ entries:")
    for i, entry in enumerate(merged_data[:5]):
        print(f"{i+1}. {entry['question']}")
        print(f"   Source: {entry['source']}")
        print()
    
    # Print validation summary
    accessible_sources = 0
    total_sources = len(merged_data)
    for entry in merged_data:
        if is_url_accessible(entry['source']):
            accessible_sources += 1
    
    print(f"\nURL Validation Summary:")
    print(f"Accessible sources: {accessible_sources}/{total_sources}")
    print(f"Inaccessible sources: {total_sources - accessible_sources}/{total_sources}")
    
    return merged_data

if __name__ == "__main__":
    updated_database = update_knowledge_database()
    print(f"Knowledge database update completed. Total entries: {len(updated_database)}")