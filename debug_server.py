import http.server
import socketserver
import json
import urllib.parse

class DebugHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request for: {self.path}")
        
        if self.path == '/health':
            print("Handling health endpoint")
            response_data = {"status": "healthy"}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            print("Serving static file")
            super().do_GET()

# Start server
PORT = 8000

with socketserver.TCPServer(("", PORT), DebugHandler) as httpd:
    print(f"Debug server running at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")