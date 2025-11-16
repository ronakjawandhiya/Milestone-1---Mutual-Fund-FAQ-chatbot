from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Simple data loading
DATA_FILE = "mf_faq_data.json"

def load_faq_data():
    """Load FAQ data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Load FAQ data on startup
faq_database = load_faq_data()

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "faq_count": len(faq_database)
    })

@app.route('/faq')
def get_faq():
    """API endpoint to get FAQ answer for a question"""
    return jsonify(faq_database[0] if faq_database else {"error": "No data available"})

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)