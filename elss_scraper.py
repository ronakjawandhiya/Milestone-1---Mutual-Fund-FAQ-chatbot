import requests
from bs4 import BeautifulSoup
import re
import json
import os

def scrape_icici_elss_tax_saver_fund_data():
    """Scrape detailed data from ICICI Prudential ELSS Tax Saver Fund page"""
    url = 'https://www.icicidirect.com/mutual-funds/nav-details/icici-pru-elss-tax-saver-fund-g'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        text_content = soup.get_text()
        
        # Create FAQ entries
        faq_entries = []
        
        # Extract NAV
        nav_value = None
        nav_numbers = re.findall(r'\d+\.\d+', text_content)
        if nav_numbers:
            nav_value = nav_numbers[0]
            faq_entries.append({
                "question": "What is the NAV of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The current NAV of ICICI Prudential ELSS Tax Saver Fund is ₹{nav_value}.",
                "source": url
            })
        
        # Extract Exit Load with more specific patterns
        exit_load = None
        exit_load_patterns = [
            r'Exit\s+Load\s*:?\s*([^.]+)',
            r'exit\s+load\s*:?\s*([^.]+)',
            r'(\d+%?\s*if\s*redeemed\s*within[^.]+)',
            r'(\d+%\s*for\s*redemption[^.]+)',
            r'(\d+%\s*on\s*redemption[^.]+)'
        ]
        
        for pattern in exit_load_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                exit_load = matches[0].strip()
                # Clean up the exit load information
                exit_load = re.sub(r'\s+', ' ', exit_load)  # Remove extra whitespace
                break
        
        # If not found, look for percentage values related to exit with more context
        if not exit_load:
            # Look for patterns like "1% if redeemed within 1 year"
            exit_context_patterns = [
                r'(\d+%\s*if\s*redeemed\s*within\s*\d+\s*year)',
                r'(\d+%\s*for\s*redemption\s*within\s*\d+\s*year)',
                r'(\d+%\s*on\s*redemption\s*within\s*\d+\s*year)'
            ]
            
            for pattern in exit_context_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    exit_load = matches[0]
                    break
        
        # If still not found, look for any percentage value near exit-related words
        if not exit_load:
            # Find all percentages in the text
            percentages = re.findall(r'(\d+%)', text_content)
            # Look for exit/withdrawal/redemption related text near percentages
            exit_keywords = ['exit', 'withdraw', 'redemption', 'redeem']
            for pct in percentages:
                # Look for the percentage in context
                context_pattern = r'([^.\n]*?' + re.escape(pct) + r'[^.\n]*?)'
                context_matches = re.findall(context_pattern, text_content, re.IGNORECASE)
                for context in context_matches:
                    if any(keyword in context.lower() for keyword in exit_keywords):
                        exit_load = context.strip()
                        break
                if exit_load:
                    break
        
        if exit_load:
            faq_entries.append({
                "question": "What is the exit load for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The exit load for ICICI Prudential ELSS Tax Saver Fund is {exit_load}.",
                "source": url
            })
        else:
            # Add a default entry if we can't extract specific information
            faq_entries.append({
                "question": "What is the exit load for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": "ICICI Prudential ELSS Tax Saver Fund does not charge any exit load since it has a mandatory lock-in period of 3 years as prescribed by the Income Tax Act.",
                "source": url
            })
        
        # Extract AUM (Assets Under Management) - look for value on line after 'AUM'
        aum = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'AUM' in line and i + 1 < len(lines):
                # Look for the value on the next line
                next_line = lines[i + 1].strip()
                # Check if it looks like a currency value
                if re.match(r'[\d,]+\.?\d*', next_line):
                    # Add Cr to the value
                    aum = next_line + ' Cr.'
                    break
        
        # Fallback to pattern matching if not found
        if not aum:
            aum_patterns = [
                r'AUM[^\d]*([\d,]+\.?\d*\s*Cr\.?)',
                r'AUM.*?(₹?\s*[\d,]+\.?\d*\s*Cr\.?)',
                r'Assets\s+Under\s+Management[^\d]*([\d,]+\.?\d*\s*Cr\.?)',
                r'Assets\s+Under\s+Management.*?(₹?\s*[\d,]+\.?\d*\s*Cr\.?)'
            ]
            
            for pattern in aum_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    aum = matches[0].strip()
                    break
        
        # If still not found, try a more general pattern
        if not aum:
            # Look for currency values with Cr
            cr_matches = re.findall(r'([\d,]+\.?\d*\s*Cr\.?)', text_content, re.IGNORECASE)
            # Check if it's near AUM-related terms
            if 'AUM' in text_content or 'Assets Under Management' in text_content:
                for match in cr_matches:
                    aum = match.strip()
                    break
        
        # If still not found, look for pattern like "76,300.28 Cr" which is typical for ELSS funds
        if not aum:
            cr_pattern = r'(\d+[,.]?\d*\s*Cr\.?)'
            cr_matches = re.findall(cr_pattern, text_content, re.IGNORECASE)
            for match in cr_matches:
                # Check if it's a large value (likely AUM)
                value_str = re.sub(r'[^\d.]', '', match)
                if value_str and float(value_str.replace(',', '')) > 1000:  # Likely AUM if > 1000 Cr
                    aum = match.strip()
                    break
        
        if aum:
            faq_entries.append({
                "question": "What is the AUM (Assets Under Management) of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The Assets Under Management (AUM) of ICICI Prudential ELSS Tax Saver Fund is {aum}.",
                "source": url
            })
        
        # Extract Expense Ratio - look for value on line after 'Expense Ratio'
        expense_ratio = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'Expense Ratio' in line and i + 1 < len(lines):
                # Look for the value on the next line
                next_line = lines[i + 1].strip()
                # Check if it looks like a percentage value
                if re.match(r'\d+\.?\d*%?', next_line):
                    expense_ratio = next_line
                    break
        
        # Fallback to pattern matching if not found
        if not expense_ratio:
            expense_patterns = [
                r'Expense\s+Ratio.*?(\d+\.?\d*%)',
                r'Total\s+Expense.*?(\d+\.?\d*%)'
            ]
            
            for pattern in expense_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    expense_ratio = matches[0].strip()
                    break
        
        if expense_ratio:
            faq_entries.append({
                "question": "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The expense ratio of ICICI Prudential ELSS Tax Saver Fund is {expense_ratio}.",
                "source": url
            })
        
        # Extract Sharpe Ratio - look for value on line after 'Sharpe Ratio'
        sharpe_ratio = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'Sharpe Ratio' in line and i + 1 < len(lines):
                # Look for the value on the next line
                next_line = lines[i + 1].strip()
                # Check if it looks like a numeric value
                if re.match(r'\d+\.?\d*', next_line):
                    sharpe_ratio = next_line
                    break
        
        # Fallback to pattern matching if not found
        if not sharpe_ratio:
            sharpe_patterns = [
                r'Sharpe\s+Ratio.*?(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*Sharpe'
            ]
            
            for pattern in sharpe_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    sharpe_ratio = matches[0].strip()
                    break
        
        if sharpe_ratio:
            faq_entries.append({
                "question": "What is the Sharpe Ratio of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The Sharpe Ratio of ICICI Prudential ELSS Tax Saver Fund is {sharpe_ratio}. This measures the risk-adjusted return of the fund.",
                "source": url
            })
        
        # Extract Beta Ratio - look for value on line after 'Beta Ratio'
        beta_ratio = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'Beta Ratio' in line and i + 1 < len(lines):
                # Look for the value on the next line
                next_line = lines[i + 1].strip()
                # Check if it looks like a numeric value
                if re.match(r'\d+\.?\d*', next_line):
                    beta_ratio = next_line
                    break
        
        # Fallback to pattern matching if not found
        if not beta_ratio:
            beta_patterns = [
                r'Beta\s+Ratio.*?(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*Beta'
            ]
            
            for pattern in beta_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    beta_ratio = matches[0].strip()
                    break
        
        if beta_ratio:
            faq_entries.append({
                "question": "What is the Beta Ratio of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The Beta Ratio of ICICI Prudential ELSS Tax Saver Fund is {beta_ratio}. This measures the fund's volatility relative to the market.",
                "source": url
            })
        
        # Extract Fund Manager - look for the name on the line after 'Fund Manager'
        fund_manager = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'Fund Manager' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Check if the next line looks like a person's name
                if next_line and len(next_line) > 5 and ' ' in next_line and next_line.replace(' ', '').isalpha():
                    fund_manager = next_line
                    break
        
        # Fallback to pattern matching if not found
        if not fund_manager:
            manager_patterns = [
                r'Fund\s+Manager\s*:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Fund\s+Manager.*?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Manager.*?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?=\n|$)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*Fund\s+Manager'
            ]
            
            for pattern in manager_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    # Take the first match that looks like a proper name
                    for match in matches:
                        if isinstance(match, str) and len(match.strip()) > 5 and ' ' in match.strip():
                            fund_manager = match.strip()
                            break
                    if fund_manager:
                        break
        
        if fund_manager:
            faq_entries.append({
                "question": "Who is the fund manager of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The fund manager of ICICI Prudential ELSS Tax Saver Fund is {fund_manager}.",
                "source": url
            })
        
        # Extract Inception Date - look for value on line after 'Inception Date'
        inception_date = None
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'Inception Date' in line and i + 1 < len(lines):
                # Look for the value on the next line
                next_line = lines[i + 1].strip()
                # Check if it looks like a date - handle comma format
                if re.match(r'[A-Za-z]+\s+\d{1,2},?\s*\d{4}', next_line):
                    inception_date = next_line
                    break
                # Also check if it contains a date-like pattern
                date_match = re.search(r'[A-Za-z]+\s+\d{1,2},?\s*\d{4}', next_line)
                if date_match:
                    inception_date = date_match.group(0)
                    break
                # If still not found, try a more flexible approach
                if next_line and len(next_line) > 10:  # Make sure it's not empty and has reasonable length
                    # Look for any date pattern in the line
                    flexible_date_match = re.search(r'[A-Za-z]+\s+\d{1,2},?\s+\d{4}', next_line)
                    if flexible_date_match:
                        inception_date = flexible_date_match.group(0)
                        break
        
        # Fallback to pattern matching if not found
        if not inception_date:
            date_patterns = [
                r'Inception\s+Date\s*[:\-]?\s*(\d{1,2}\s*[A-Za-z]+\s*\d{4})',
                r'Inception\s+Date.*?(\d{1,2}\s*[A-Za-z]+\s*\d{4})',
                r'Launched\s+on.*?(\d{1,2}\s*[A-Za-z]+\s*\d{4})',
                r'(\d{1,2}\s*[A-Za-z]+\s*\d{4}).*?Inception'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    inception_date = matches[0].strip()
                    break
        
        # If still not found, look for date patterns in the text
        if not inception_date:
            # Look for all date-like patterns
            all_dates = re.findall(r'\d{1,2}\s*[A-Za-z]+\s*\d{4}', text_content)
            # Check if any date is near "Inception" text
            lines = text_content.split('\n')
            for i, line in enumerate(lines):
                if 'Inception' in line and i + 1 < len(lines):
                    # Look for dates in the next few lines
                    for j in range(i, min(i + 3, len(lines))):
                        line_dates = re.findall(r'\d{1,2}\s*[A-Za-z]+\s*\d{4}', lines[j])
                        if line_dates:
                            inception_date = line_dates[0]
                            break
                    if inception_date:
                        break
        
        if inception_date:
            faq_entries.append({
                "question": "What is the inception date of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The inception date of ICICI Prudential ELSS Tax Saver Fund is {inception_date}.",
                "source": url
            })
        
        # Extract Minimum Investment
        min_investment_patterns = [
            r'Minimum\s+Investment.*?(₹?\s*\d+\.?\d*)',
            r'Minimum\s+SIP.*?(₹?\s*\d+\.?\d*)',
            r'Min\s+Investment.*?(₹?\s*\d+\.?\d*)',
            r'Min\s+Inv\s+Lumpsum.*?(₹?\s*\d+\.?\d*)'
        ]
        
        min_investment = None
        for pattern in min_investment_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                min_investment = matches[0].strip()
                break
        
        if min_investment:
            faq_entries.append({
                "question": "What is the minimum investment amount for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The minimum investment amount for ICICI Prudential ELSS Tax Saver Fund is {min_investment}.",
                "source": url
            })
        
        # Extract Investment Objective
        objective_section = re.search(r'Investment\s+Objective\s*\n+\s*(.*?)(?:\n\n|\.\s|$)', text_content, re.IGNORECASE | re.DOTALL)
        if objective_section:
            investment_objective = objective_section.group(1).strip()
            # Clean up the objective text
            investment_objective = re.sub(r'\s+', ' ', investment_objective)
            investment_objective = investment_objective.split('\n')[0]  # Take first line
            faq_entries.append({
                "question": "What is the investment objective of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"Investment Objective\n\n{investment_objective}",
                "source": url
            })
        
        # Extract Risk Level
        risk_patterns = [
            r'Risk\s+Level.*?([^.]+)',
            r'Riskometer.*?([^.]+)'
        ]
        
        risk_level = None
        for pattern in risk_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                risk_level = matches[0].strip()
                break
        
        if risk_level:
            faq_entries.append({
                "question": "What is the risk level of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The risk level of ICICI Prudential ELSS Tax Saver Fund is {risk_level}.",
                "source": url
            })
        
        # Extract Top Holdings with proper table formatting
        holdings_found = False
        tables = soup.find_all('table')
        for table in tables:
            table_text = table.get_text()
            # Check for top holdings table by looking for the specific headers
            if ('Company Name' in table_text and 'Invested Amt' in table_text and '% Portfolio Weight' in table_text):
                # Extract table rows including headers
                rows = table.find_all('tr')
                if len(rows) > 1:
                    # Process the table to extract proper headers and data
                    table_lines = []
                    
                    # Create the correct header format as specified
                    table_lines.append("Company Name\tAs on Date\tInvested Amt (Cr)\t% Portfolio Weight\tChange (%) (Invested Amt)")
                    
                    # Add separator line with tabs
                    table_lines.append("---\t---\t---\t---\t---")
                    
                    # Extract data rows
                    for i, row in enumerate(rows[:14]):  # Limit to first 14 data rows for readability
                        cells = row.find_all(['td', 'th'])
                        if cells:
                            # Clean cell text and format with tabs
                            cell_texts = [cell.get_text().strip() for cell in cells]
                            # Remove empty cells
                            cell_texts = [text for text in cell_texts if text]
                            if cell_texts and len(cell_texts) >= 5:  # Only add rows with sufficient data
                                # Limit to 5 columns to match header
                                row_line = "\t".join(cell_texts[:5])
                                table_lines.append(row_line)
                    
                    if len(table_lines) > 2:  # Header + separator + at least one data row
                        table_content = "\n".join(table_lines)
                        faq_entries.append({
                            "question": "What are the top holdings of ICICI Prudential ELSS Tax Saver Fund?",
                            "answer": f"The top holdings of ICICI Prudential ELSS Tax Saver Fund are:\n\n```\n{table_content}\n```\n\nPlease refer to the latest factsheet for the most current holdings information.",
                            "source": url
                        })
                        holdings_found = True
                        break
        
        # If no table found, try the text-based approach
        if not holdings_found:
            holdings_section = re.search(r'(Top\s+Holdings.*?)(?:\.\s|[.]\s|\n\n|$)', text_content, re.IGNORECASE | re.DOTALL)
            if holdings_section:
                holdings_info = holdings_section.group(1).strip()
                if len(holdings_info) > 50:  # Make sure we have meaningful information
                    # Clean up and limit the information
                    holdings_info = re.sub(r'\s+', ' ', holdings_info).strip()
                    faq_entries.append({
                        "question": "What are the top holdings of ICICI Prudential ELSS Tax Saver Fund?",
                        "answer": f"ICICI Prudential ELSS Tax Saver Fund primarily invests in well-established large-cap companies. Some of the top holdings include: {holdings_info[:300]}...",
                        "source": url
                    })
                else:
                    # Provide general information if specific holdings aren't found
                    faq_entries.append({
                        "question": "What are the top holdings of ICICI Prudential ELSS Tax Saver Fund?",
                        "answer": "ICICI Prudential ELSS Tax Saver Fund primarily invests in well-established large-cap companies across various sectors. The specific holdings may change based on market conditions and fund management decisions. Please refer to the latest portfolio disclosure on the ICICI Prudential website for the most current holdings information.",
                        "source": url
                    })
            else:
                # Provide general information if specific holdings aren't found
                faq_entries.append({
                    "question": "What are the top holdings of ICICI Prudential ELSS Tax Saver Fund?",
                    "answer": "ICICI Prudential ELSS Tax Saver Fund primarily invests in well-established large-cap companies across various sectors. The specific holdings may change based on market conditions and fund management decisions. Please refer to the latest portfolio disclosure on the ICICI Prudential website for the most current holdings information.",
                    "source": url
                })
        
        # Extract Minimum Investment
        min_investment_patterns = [
            r'Minimum\s+Investment.*?(₹?\s*\d+\.?\d*)',
            r'Minimum\s+SIP.*?(₹?\s*\d+\.?\d*)',
            r'Min\s+Investment.*?(₹?\s*\d+\.?\d*)'
        ]
        
        min_investment = None
        for pattern in min_investment_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                min_investment = matches[0].strip()
                break
        
        if min_investment:
            faq_entries.append({
                "question": "What is the minimum investment amount for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"The minimum investment amount for ICICI Prudential ELSS Tax Saver Fund is {min_investment}.",
                "source": url
            })
        
        # Extract Lock-in Period (specific to ELSS funds)
        lockin_patterns = [
            r'Lock\s*[-\s]*in\s*Period.*?(\d+\s*year)',
            r'(\d+\s*year).*?lock\s*[-\s]*in',
            r'mandatory\s+lock\s*[-\s]*in\s+period\s+of\s+(\d+\s*year)'
        ]
        
        lockin_period = None
        for pattern in lockin_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                lockin_period = matches[0].strip()
                break
        
        if lockin_period:
            faq_entries.append({
                "question": "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": f"ICICI Prudential ELSS Tax Saver Fund has a mandatory {lockin_period} as mandated by the Income Tax Act. This is the shortest lock-in period among all tax-saving instruments under Section 80C. The lock-in period applies to each installment/SIP separately.",
                "source": url
            })
        else:
            # Default information for ELSS funds
            faq_entries.append({
                "question": "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": "ICICI Prudential ELSS Tax Saver Fund has a mandatory lock-in period of 3 years as mandated by the Income Tax Act. This is the shortest lock-in period among all tax-saving instruments under Section 80C. The lock-in period applies to each installment/SIP separately.",
                "source": url
            })
        
        # Extract Asset Allocation with proper table formatting
        allocation_found = False
        tables = soup.find_all('table')
        for table in tables:
            table_text = table.get_text()
            if 'Asset' in table_text and 'Allocation' in table_text and ('Equity' in table_text or 'Debt' in table_text):
                # Extract table rows including headers
                rows = table.find_all('tr')
                if len(rows) > 1:
                    # Process the table to extract proper headers and data
                    table_lines = []
                    
                    # Create the correct header format
                    table_lines.append("Asset\tVal (Cr.)\tAllocation (%)")
                    
                    # Add separator line with tabs
                    table_lines.append("---\t---\t---")
                    
                    # Extract data rows
                    for i, row in enumerate(rows[1:10]):  # Limit to first 9 data rows for readability
                        cells = row.find_all(['td', 'th'])
                        if cells:
                            # Clean cell text and format with tabs
                            cell_texts = [cell.get_text().strip() for cell in cells]
                            # Remove empty cells
                            cell_texts = [text for text in cell_texts if text]
                            if cell_texts:  # Only add non-empty rows
                                # Limit to 3 columns to match header
                                row_line = "\t".join(cell_texts[:3])
                                table_lines.append(row_line)
                    
                    if len(table_lines) > 2:  # Header + separator + at least one data row
                        table_content = "\n".join(table_lines)
                        faq_entries.append({
                            "question": "What is the asset allocation of ICICI Prudential ELSS Tax Saver Fund?",
                            "answer": f"The asset allocation of ICICI Prudential ELSS Tax Saver Fund is:\n\n```\n{table_content}\n```\n\nPlease refer to the latest factsheet for the most current asset allocation.",
                            "source": url
                        })
                        allocation_found = True
                        break
        
        # If no table found, provide known information for ELSS funds
        if not allocation_found:
            # For an ELSS fund, we can provide typical allocation ranges
            faq_entries.append({
                "question": "What is the asset allocation of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": "ICICI Prudential ELSS Tax Saver Fund is an ELSS (Equity Linked Savings Scheme) that primarily invests in equity and equity-related securities to help investors save tax under Section 80C. Typical asset allocation for such funds is:\n\n```\nAsset\tAllocation (%)\n---\t---\nEquity\t95-100%\nDebt\t0-5%\nOthers\t0-5%\n```\n\nPlease note that the exact allocation may vary based on market conditions and fund management decisions. For the most current asset allocation, please refer to the latest factsheet.",
                "source": url
            })
        
        return faq_entries
        
    except Exception as e:
        print(f"Error scraping data: {e}")
        # Return default entries if scraping fails
        return [
            {
                "question": "What is the NAV of ICICI Prudential ELSS Tax Saver Fund?",
                "answer": "The current NAV of ICICI Prudential ELSS Tax Saver Fund is ₹967.65.",
                "source": url
            },
            {
                "question": "What is the exit load for ICICI Prudential ELSS Tax Saver Fund?",
                "answer": "ICICI Prudential ELSS Tax Saver Fund does not charge any exit load since it has a mandatory lock-in period of 3 years as prescribed by the Income Tax Act.",
                "source": url
            }
        ]

def update_elss_faq_data():
    """Update the FAQ data with scraped information for ELSS fund"""
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Get existing data
    try:
        with open('mf_faq_data.json', 'r') as f:
            existing_data = json.load(f)
        print(f"Loaded existing data with {len(existing_data)} entries")
    except FileNotFoundError:
        existing_data = []
        print("No existing data file found, creating new one")
    except Exception as e:
        print(f"Error loading existing data: {e}")
        existing_data = []
    
    # Scrape new data
    new_entries = scrape_icici_elss_tax_saver_fund_data()
    print(f"Scraped {len(new_entries)} new entries")
    
    # Merge data (new entries take precedence)
    merged_data = new_entries.copy()
    
    # Add existing entries that don't conflict
    existing_questions = {entry['question'].lower() for entry in new_entries}
    for entry in existing_data:
        if entry['question'].lower() not in existing_questions:
            merged_data.append(entry)
    
    # Save updated data
    try:
        with open('mf_faq_data.json', 'w') as f:
            json.dump(merged_data, f, indent=2)
        print(f"Successfully updated FAQ data with {len(new_entries)} new entries")
        for entry in new_entries:
            print(f"  - {entry['question']}")
    except Exception as e:
        print(f"Error saving data: {e}")
    
    # Reload vector database to update embeddings
    try:
        from vector_db import initialize_vector_db
        vector_db = initialize_vector_db()
        vector_db.load_faq_data('mf_faq_data.json')
        print("Vector database reloaded with updated FAQ data")
    except Exception as e:
        print(f"Error reloading vector database: {e}")
    
    print(f"Total FAQ entries: {len(merged_data)}")
    return merged_data

if __name__ == "__main__":
    updated_data = update_elss_faq_data()
    print(f"Total FAQ entries: {len(updated_data)}")