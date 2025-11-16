import http.server
import socketserver
import json
import urllib.parse

# Load FAQ data
with open('mf_faq_data.json', 'r') as f:
    faq_data = json.load(f)

class FAQHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/faq'):
            # Parse query parameters
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            question = query_params.get('question', [''])[0]
            
            # Find relevant FAQ
            response_data = self.find_relevant_faq(question)
            
            # Send JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/health':
            # Health check endpoint
            response_data = {
                "status": "healthy",
                "faq_count": len(faq_data)
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/topics':
            # Topics endpoint
            response_data = {
                "topics": [
                    "exit load", "expense ratio", "minimum sip", "lock in period", "capital gains",
                    "icici prudential elss", "icici prudential large cap", "icici prudential multi asset",
                    "icici prudential bluechip", "icici prudential focused equity", "riskometer",
                    "benchmark", "capital gains statement", "sip amount", "elss lock-in"
                ]
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # Serve static files
            super().do_GET()
    
    def find_relevant_faq(self, question):
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

# Start server
PORT = 8000
Handler = FAQHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")