# Mutual Fund FAQ Assistant

A simple FAQ assistant that provides factual information about Mutual Funds from official sources like AMFI and SEBI. Every answer includes a source link for verification.

## Features

- Answers common questions about mutual funds
- Provides information on exit load, expense ratio, minimum SIP, lock-in period, capital gains, NAV, fund types, etc.
- Every answer includes a verified source link
- No investment advice - only factual information
- Clean, responsive web interface
- Chat history to review previous questions and answers
- Topic-based question matching for better accuracy

## How It Works

1. **Data Collection (Option 1 - Pre-computed)**: 
   - Scrapes official AMFI and SEBI websites for FAQ data
   - Stores structured data locally with source URLs
   - Provides fast responses without real-time scraping

2. **Data Serving**:
   - Flask backend serves FAQ data via REST API
   - Frontend provides a clean interface for asking questions
   - Matches user questions to stored FAQ entries

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```
   cd "Mutual Fund FAQ BOT"
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open `index.html` in your web browser

3. Ask questions about mutual funds!

### API Endpoints

- `GET /faq?question={your_question}` - Get FAQ answer for a question
- `GET /topics` - Get list of available topics
- `POST /refresh-data` - Refresh FAQ data from official sources
- `GET /health` - Health check endpoint

## Example Questions

- What is exit load in mutual funds?
- What is expense ratio?
- What is the minimum SIP amount?
- What is lock-in period for ELSS funds?
- How are capital gains taxed in mutual funds?
- What is Net Asset Value (NAV)?
- What is the difference between SIP and lump sum investment?
- What are the different types of mutual funds?

## Data Sources

- [AMFI India](https://www.amfiindia.com/)
- [SEBI India](https://www.sebi.gov.in/)

## Note

This application is for educational purposes only and does not provide investment advice. All information is sourced from official regulatory websites.