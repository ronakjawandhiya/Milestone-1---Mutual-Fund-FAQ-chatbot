import streamlit as st
import json
import re

# Load FAQ data
with open('mf_faq_data.json', 'r') as f:
    faq_data = json.load(f)

def find_relevant_faq(question):
    """Find the most relevant FAQ entry for a given question"""
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
    
    # First try exact matching
    for entry in faq_data:
        if question_lower in entry['question'].lower() or \
           entry['question'].lower() in question_lower:
            return entry
    
    # Try keyword matching with ICICI Prudential focus
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

# Streamlit app
st.set_page_config(
    page_title="Mutual Fund FAQ Assistant",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        max-width: 80%;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background-color: #f5f7fa;
        margin-right: auto;
    }
    .answer-text {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .source-link {
        color: #1e3c72;
        text-decoration: none;
        font-weight: bold;
    }
    .source-link:hover {
        text-decoration: underline;
    }
    .example-questions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .example-card {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .example-card:hover {
        background-color: #bbdefb;
        transform: translateY(-2px);
    }
    .disclaimer {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-top: 2rem;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
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
    # Chat container
    st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)
    
    # Display chat history
    for role, content in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"<div class='message user-message'><strong>You:</strong><br>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message assistant-message'><strong>Assistant:</strong><br><div class='answer-text'>{content['answer']}</div><br><a href='{content['source']}' class='source-link' target='_blank'>🔗 Source: {content['source']}</a></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Example questions
    st.markdown("### 💡 Example Questions")
    example_questions = [
        "What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?",
        "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
        "What is the minimum SIP amount for ICICI Prudential schemes?",
        "What is the exit load for ICICI Prudential Large Cap Fund?",
        "What is the riskometer rating for ICICI Prudential Multi-Asset Fund?",
        "How to download capital gains statement from ICICI Prudential?",
        "What is the benchmark for ICICI Prudential Bluechip Fund?",
        "What is the minimum investment amount for ICICI Prudential Focused Equity Fund?"
    ]
    
    # Display example questions in a grid
    st.markdown("<div class='example-questions'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, question in enumerate(example_questions):
        with cols[i % 4]:
            if st.button(question, key=f"example_{i}", use_container_width=True):
                # Find relevant FAQ
                result = find_relevant_faq(question)
                
                # Add to chat history
                st.session_state.chat_history.append(("user", question))
                st.session_state.chat_history.append(("assistant", result))
                
                # Rerun to update the UI
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Sidebar content
    st.header("About this Assistant")
    st.markdown("""
    This FAQ assistant provides factual information about:
    - ICICI Prudential mutual funds
    - General mutual fund concepts
    - Exit loads, expense ratios, SIP amounts
    - Lock-in periods, capital gains, etc.
    
    Every answer includes a verified source link.
    """)
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Important Note")
    st.markdown("""
    - Facts-only. No investment advice.
    - For personalized advice, consult a certified financial advisor.
    """)
    
    # Health check info
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success(f"FAQ Database: {len(faq_data)} entries loaded")

# Input container at the bottom
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    # Create a form for the input
    with st.form(key='question_form', clear_on_submit=True):
        user_question = st.text_input("Ask a question about mutual funds:", placeholder="e.g., What is the expense ratio of ICICI Prudential ELSS Tax Saver Fund?", label_visibility="collapsed")
        submit_button = st.form_submit_button(label='Send', use_container_width=True)
        
        # Process the question if submitted
        if submit_button and user_question:
            # Find relevant FAQ
            result = find_relevant_faq(user_question)
            
            # Add to chat history
            st.session_state.chat_history.append(("user", user_question))
            st.session_state.chat_history.append(("assistant", result))
            
            # Rerun to update the UI
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Disclaimer
st.markdown("<div class='disclaimer'><h4>⚠️ Disclaimer</h4><p>This assistant provides factual information about mutual funds based on official sources. It does not provide investment advice. For personalized investment recommendations, please consult a certified financial advisor.</p></div>", unsafe_allow_html=True)