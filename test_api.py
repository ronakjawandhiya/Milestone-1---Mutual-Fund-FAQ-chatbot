import requests
import json

# Test the health endpoint
try:
    response = requests.get('http://localhost:5000/health')
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error testing health endpoint: {e}")

print("\n" + "="*50 + "\n")

# Test the FAQ endpoint
try:
    response = requests.get('http://localhost:5000/faq?question=What is exit load')
    print("FAQ Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error testing FAQ endpoint: {e}")