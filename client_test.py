import urllib.request
import json

# Test the endpoints directly
def test_endpoint(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data.decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

# Test health endpoint
print("Testing health endpoint:")
result = test_endpoint("http://localhost:5000/health")
print(result)
print()

# Test FAQ endpoint
print("Testing FAQ endpoint:")
result = test_endpoint("http://localhost:5000/faq?question=What%20is%20exit%20load")
print(result)
print()

# Test topics endpoint
print("Testing topics endpoint:")
result = test_endpoint("http://localhost:5000/topics")
print(result)
print()

# Test static file serving
print("Testing static file serving:")
result = test_endpoint("http://localhost:5000/index.html")
print(f"Received {len(result)} characters" if not result.startswith("Error") else result)