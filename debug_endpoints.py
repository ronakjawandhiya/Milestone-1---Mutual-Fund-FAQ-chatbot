import requests
import json

# Test the health endpoint
try:
    response = requests.get('http://localhost:5000/health')
    print("Health Check Status Code:", response.status_code)
    print("Health Check Response Text:", response.text)
    if response.text:
        try:
            print("Health Check JSON:", response.json())
        except:
            print("Health Check Response is not JSON")
except Exception as e:
    print(f"Error testing health endpoint: {e}")

print("\n" + "="*50 + "\n")

# Test the FAQ endpoint
try:
    response = requests.get('http://localhost:5000/faq?question=What is exit load')
    print("FAQ Status Code:", response.status_code)
    print("FAQ Response Text:", response.text)
    if response.text:
        try:
            print("FAQ JSON:", response.json())
        except:
            print("FAQ Response is not JSON")
except Exception as e:
    print(f"Error testing FAQ endpoint: {e}")

print("\n" + "="*50 + "\n")

# Test the topics endpoint
try:
    response = requests.get('http://localhost:5000/topics')
    print("Topics Status Code:", response.status_code)
    print("Topics Response Text:", response.text)
    if response.text:
        try:
            print("Topics JSON:", response.json())
        except:
            print("Topics Response is not JSON")
except Exception as e:
    print(f"Error testing topics endpoint: {e}")