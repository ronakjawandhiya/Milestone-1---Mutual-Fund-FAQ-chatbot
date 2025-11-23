import streamlit as st
import json
import re
from vector_db import search_similar_questions, initialize_vector_db

# Load FAQ data
with open('mf_faq_data.json', 'r') as f:
    faq_data = json.load(f)

# Initialize vector database
initialize_vector_db()

def find_relevant_faq(question):
    """Find the most relevant FAQ entry for a given question using RAG"""
    question_lower = question.lower()
    
    # Check for opinionated/portfolio questions and refuse politely
    opinionated_keywords = [
        'should i buy', 'should i sell', 'is it good', 'recommend', 
        'best fund', 'which fund', 'portfolio', 'investment advice',
        'where to invest', 'good time to invest', 'risk level', 'best mutual fund',
        'good for long term', 'recommend a portfolio', 'invest in'
    ]
    
    for keyword in opinionated_keywords:
        if keyword in question_lower:
            return {
                "question": question,
                "answer": "I can only provide factual information about mutual funds. For personalized investment advice, please consult a certified financial advisor. You can learn more about making informed investment decisions at the official AMFI investor education resources.",
                "source": "https://www.amfiindia.com/investor-corner/investor-education"
            }
    
    # Use vector database to find similar questions
    try:
        similar_questions = search_similar_questions(question, k=1)
        if similar_questions and similar_questions[0]['distance'] < 1.0:  # Threshold for similarity
            return similar_questions[0]
    except Exception as e:
        print(f"Error in vector search: {e}")
    
    # Fallback to keyword matching with ICICI Prudential focus
    keywords = question_lower.split()
    best_match = None
    best_score = 0
    
    for entry in faq_data:
        entry_question_lower = entry['question'].lower()
        score = 0
        
        # Count matching keywords
        for keyword in keywords:
            if keyword in entry_question_lower:
                score += 1
        
        # Boost score for ICICI Prudential related questions
        if 'icici' in question_lower and 'icici' in entry_question_lower:
            score += 2
        
        # Update best match if this entry has a higher score
        if score > best_score:
            best_score = score
            best_match = entry
    
    # Return best match if found, otherwise first entry
    return best_match if best_match else (faq_data[0] if faq_data else {"error": "No data available"})

def format_table_with_colors(table_content):
    """Format table content with color coding for positive and negative numbers"""
    lines = table_content.split('\n')
    formatted_lines = []
    
    for i, line in enumerate(lines):
        if i >= 2 and line.strip():  # Skip headers and process data rows
            # Split by tabs to get individual cells
            cells = line.split('\t')
            if len(cells) >= 5:
                # Color code the last column (Change %)
                change_cell = cells[4]
                # Extract numeric value
                change_value = re.search(r'(-?\d+\.?\d*)', change_cell)
                if change_value:
                    try:
                        value = float(change_value.group(1))
                        if value > 0:
                            # Green for positive values
                            cells[4] = f"<span style='color: green; font-weight: bold;'>{change_cell}</span>"
                        elif value < 0:
                            # Red for negative values
                            cells[4] = f"<span style='color: red; font-weight: bold;'>{change_cell}</span>"
                    except ValueError:
                        # If conversion fails, leave as is
                        pass
                # Rejoin the cells
                line = '\t'.join(cells)
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

# Streamlit app
st.set_page_config(
    page_title="Mutual Fund FAQ Assistant",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Chat container */
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e1e8ed;
    }
    
    /* Message styling */
    .message {
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        max-width: 85%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        margin-left: auto;
        border-bottom-right-radius: 5px;
        border-top-right-radius: 5px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border-top-left-radius: 5px;
        border-left: 4px solid #2a5298;
    }
    
    /* Answer text */
    .answer-text {
        font-size: 1.1rem;
        color: #333;
        margin-bottom: 1rem;
        white-space: pre-wrap; /* Preserve whitespace and line breaks */
    }
    
    /* Source link */
    .source-link {
        color: #1e3c72;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        padding: 0.4rem 0.8rem;
        background-color: rgba(30, 60, 114, 0.1);
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    .source-link:hover {
        background-color: rgba(30, 60, 114, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Example questions grid */
    .example-questions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .example-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .example-card:hover {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        border-color: #bbdefb;
    }
    
    .example-card h4 {
        margin: 0 0 0.5rem 0;
        color: #1e3c72;
        font-size: 1rem;
    }
    
    .example-card p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ffc107;
        margin-top: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    
    .disclaimer h4 {
        margin-top: 0;
        color: #e65100;
    }
    
    /* Response container */
    .response-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-top: 1.5rem;
        border: 1px solid #e1e8ed;
    }
    
    .response-container h3 {
        color: #1e3c72;
        margin-top: 0;
        font-size: 1.4rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        padding: 1rem;
        font-size: 1.1rem;
        border-radius: 12px;
        border: 2px solid #e1e8ed;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2a5298;
        box-shadow: 0 2px 10px rgba(42, 82, 152, 0.2);
    }
    
    /* Sidebar styling */
    [data-testid=stSidebar] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid #e1e8ed;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e1e8ed;
    }
    
    .sidebar-header h3 {
        color: #1e3c72;
        margin: 0;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .status-success {
        background-color: rgba(40, 167, 69, 0.2);
        color: #28a745;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 2rem;
        border-top: 1px solid #e1e8ed;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .example-questions {
            grid-template-columns: 1fr;
        }
        
        .message {
            max-width: 95%;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'><h1>💰 Mutual Fund FAQ Assistant</h1><p>Get factual information about ICICI Prudential mutual funds and general mutual fund concepts</p></div>", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # User input
    user_question = st.text_input("Ask a question about mutual funds:", placeholder="e.g., What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?")
    
    # Example questions
    st.markdown("### 💡 Popular Questions")
    example_questions = [
        {
            "question": "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
            "category": "Expense Ratio"
        },
        {
            "question": "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
            "category": "Lock-in Period"
        },
        {
            "question": "What is the minimum SIP amount for ICICI Prudential schemes?",
            "category": "SIP Investment"
        },
        {
            "question": "What is the exit load for ICICI Prudential Large Cap Fund?",
            "category": "Exit Load"
        },
        {
            "question": "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
            "category": "Risk Rating"
        },
        {
            "question": "How to download capital gains statement from ICICI Prudential?",
            "category": "Account Services"
        },
        {
            "question": "What is the benchmark for ICICI Prudential Bluechip Fund?",
            "category": "Benchmark"
        },
        {
            "question": "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?",
            "category": "Investment Amount"
        }
    ]
    
    # Display example questions in a grid
    st.markdown("<div class='example-questions'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, example in enumerate(example_questions):
        with cols[i % 4]:
            if st.button(example["question"], key=f"example_{i}", use_container_width=True):
                user_question = example["question"]
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process the question if submitted
    if user_question:
        # Find relevant FAQ
        result = find_relevant_faq(user_question)
        
        # Add to chat history
        st.session_state.chat_history.append(("user", user_question))
        st.session_state.chat_history.append(("assistant", result))
    
    # Display current response if there's a question
    if user_question:
        result = find_relevant_faq(user_question)
        st.markdown("### 📤 Response")
        
        # Format the answer text to preserve whitespace and handle code blocks
        answer_text = result['answer']
        if '```' in answer_text:
            # Handle code blocks
            parts = answer_text.split('```')
            formatted_answer = ""
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Regular text
                    formatted_answer += part
                else:
                    # Code block - check if it's a table and format with colors
                    if "Company Name" in part and "As on Date" in part:
                        formatted_table = format_table_with_colors(part)
                        formatted_answer += f"<pre style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; overflow-x: auto; white-space: pre;'>{formatted_table}</pre>"
                    else:
                        formatted_answer += f"<pre style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; overflow-x: auto;'>{part}</pre>"
            st.markdown(f"<div class='response-container'><h3>{result['question']}</h3><div class='answer-text'>{formatted_answer}</div><br><a href='{result['source']}' class='source-link' target='_blank'>🔗 Source: {result['source']}</a></div>", unsafe_allow_html=True)
        else:
            # Regular text
            st.markdown(f"<div class='response-container'><h3>{result['question']}</h3><div class='answer-text'>{answer_text}</div><br><a href='{result['source']}' class='source-link' target='_blank'>🔗 Source: {result['source']}</a></div>", unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for role, content in st.session_state.chat_history[-6:]:  # Show last 3 exchanges
            if role == "user":
                st.markdown(f"<div class='message user-message'><strong>You:</strong><br>{content}</div>", unsafe_allow_html=True)
            else:
                # Format the answer text to preserve whitespace and handle code blocks
                answer_text = content['answer']
                if '```' in answer_text:
                    # Handle code blocks
                    parts = answer_text.split('```')
                    formatted_answer = ""
                    for i, part in enumerate(parts):
                        if i % 2 == 0:
                            # Regular text
                            formatted_answer += part
                        else:
                            # Code block - check if it's a table and format with colors
                            if "Company Name" in part and "As on Date" in part:
                                formatted_table = format_table_with_colors(part)
                                formatted_answer += f"<pre style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; overflow-x: auto; white-space: pre;'>{formatted_table}</pre>"
                            else:
                                formatted_answer += f"<pre style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; overflow-x: auto;'>{part}</pre>"
                    st.markdown(f"<div class='message assistant-message'><strong>Assistant:</strong><br><div class='answer-text'>{formatted_answer}</div><br><a href='{content['source']}' class='source-link' target='_blank'>🔗 Source: {content['source']}</a></div>", unsafe_allow_html=True)
                else:
                    # Regular text
                    st.markdown(f"<div class='message assistant-message'><strong>Assistant:</strong><br><div class='answer-text'>{answer_text}</div><br><a href='{content['source']}' class='source-link' target='_blank'>🔗 Source: {content['source']}</a></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Sidebar content
    st.markdown("<div class='sidebar-header'><h3>ℹ️ About</h3></div>", unsafe_allow_html=True)
    st.markdown("""
    This FAQ assistant provides factual information about:
    - ICICI Prudential mutual funds
    - General mutual fund concepts
    - Exit loads, expense ratios, SIP amounts
    - Lock-in periods, capital gains, etc.
    
    Every answer includes a verified source link.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Key Features")
    st.markdown("""
    - ✅ Fact-based answers only
    - 🔗 Verified sources for all information
    - 💰 Covers all major mutual fund concepts
    - 📱 Mobile responsive design
    - 🛡️ No investment advice (opinion filtering)
    """)
    
    st.markdown("---")
    st.markdown("### 📚 Fund Categories")
    fund_categories = [
        "📈 Equity Funds",
        "📊 Hybrid Funds", 
        "💵 Debt Funds",
        "🛡️ Solution Oriented"
    ]
    
    for category in fund_categories:
        st.markdown(f"- {category}")

# Disclaimer
st.markdown("<div class='disclaimer'><h4>⚠️ Disclaimer</h4><p>This assistant provides factual information about mutual funds based on official sources. It does not provide investment advice. For personalized investment recommendations, please consult a certified financial advisor.</p></div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'><p>Built with ❤️ for mutual fund investors | Data sourced from ICICI Prudential AMC, AMFI & SEBI</p></div>", unsafe_allow_html=True)