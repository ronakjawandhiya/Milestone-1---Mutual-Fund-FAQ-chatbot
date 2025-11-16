import requests
import json

# Load the FAQ data
with open('mf_faq_data.json', 'r') as f:
    faq_data = json.load(f)

print("Verifying URLs in the knowledge database...\n")

accessible_count = 0
total_count = len(faq_data)

# Define headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for i, entry in enumerate(faq_data):
    source = entry['source']
    try:
        # Use a more permissive approach for checking URL accessibility
        response = requests.head(source, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✓ Entry {i+1}: {source} - Accessible")
            accessible_count += 1
        else:
            # Try GET request if HEAD fails
            response = requests.get(source, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✓ Entry {i+1}: {source} - Accessible")
                accessible_count += 1
            else:
                print(f"✗ Entry {i+1}: {source} - Status {response.status_code}")
    except Exception as e:
        try:
            # Try GET request if HEAD fails
            response = requests.get(source, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✓ Entry {i+1}: {source} - Accessible")
                accessible_count += 1
            else:
                print(f"✗ Entry {i+1}: {source} - Status {response.status_code}")
        except Exception as e2:
            print(f"✗ Entry {i+1}: {source} - Error: {str(e2)[:50]}...")

print(f"\nSummary: {accessible_count}/{total_count} URLs are accessible")