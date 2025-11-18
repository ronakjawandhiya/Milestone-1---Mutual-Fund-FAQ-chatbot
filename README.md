# Mutual Fund FAQ Assistant

This is a comprehensive FAQ assistant that provides factual information about mutual funds, with a special focus on ICICI Prudential schemes.

## Features

- Provides factual information about mutual funds with source citations
- Specialized knowledge about ICICI Prudential mutual fund schemes:
  - ELSS Tax Saver Fund
  - Large Cap Fund
  - Multi-Asset Fund
  - Bluechip Fund
  - Focused Equity Fund
- Refuses to answer opinionated/portfolio questions with polite redirects to educational resources
- Clean, user-friendly interface built with Streamlit
- Comprehensive database with 42+ FAQ entries

## Database Structure

The knowledge base ([mf_faq_data.json](mf_faq_data.json)) contains detailed information about:

1. **Expense Ratios** - For all 5 ICICI Prudential schemes
2. **Exit Loads** - For all 5 ICICI Prudential schemes
3. **Minimum Investment Amounts** - For all 5 ICICI Prudential schemes
4. **Benchmarks** - For all 5 ICICI Prudential schemes
5. **Riskometer Ratings** - For all 5 ICICI Prudential schemes
6. **Lock-in Periods** - For ELSS Tax Saver Fund
7. **Dividend Yields** - For various schemes
8. **Portfolio Turnover Ratios** - For equity schemes
9. **Asset Allocation** - For Multi-Asset Fund
10. **General Mutual Fund Concepts** - Exit loads, expense ratios, SIP amounts, lock-in periods, capital gains

## How It Works

1. **Data Collection**: The system scrapes official sources (ICICI Prudential AMC, AMFI) to build a comprehensive knowledge base
2. **Question Matching**: Uses keyword matching with boosting for ICICI Prudential schemes to find the most relevant answers
3. **Response Generation**: Returns factual answers with source citations
4. **Opinion Filtering**: Politely refuses opinionated questions and redirects to educational resources

## Files

- [streamlit_app.py](streamlit_app.py) - Main application interface
- [mf_faq_data.json](mf_faq_data.json) - Knowledge base with 42+ FAQ entries
- [update_knowledge.py](update_knowledge.py) - Script to update the knowledge base by scraping official sources
- [test_enhanced_db.py](test_enhanced_db.py) - Test script for the enhanced database
- [test_faq_matching.py](test_faq_matching.py) - Test script for the FAQ matching function

## Running the Application

1. Install required packages:
   ```
   pip install streamlit requests beautifulsoup4
   ```

2. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

3. Access the application in your browser at `http://localhost:8501` (or the URL provided in the terminal)

## Updating the Knowledge Base

To update the knowledge base with the latest information from official sources:

```
python update_knowledge.py
```

## Testing

To test the enhanced database:
```
python test_enhanced_db.py
```

To test the FAQ matching function:
```
python test_faq_matching.py
```