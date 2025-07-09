import requests
import json

# Test training the email model
print("Testing email model training...")

training_data = [
    {
        "data": {
            "content": "URGENT: Your account has been suspended!",
            "sender": "security@fake-bank.com",
            "subject": "Account Verification Required"
        },
        "is_fraud": True
    },
    {
        "data": {
            "content": "Hello, here is your monthly newsletter.",
            "sender": "newsletter@company.com",
            "subject": "Monthly Newsletter"
        },
        "is_fraud": False
    }
]

try:
    response = requests.post('http://localhost:5000/api/ai/train', json={
        'channel': 'email',
        'training_data': training_data
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except Exception as e:
    print(f"Error: {e}")

# Check status after training
print("\nChecking AI status...")
try:
    status_response = requests.get('http://localhost:5000/api/ai/status')
    print(f"Status: {status_response.json()}")
except Exception as e:
    print(f"Error checking status: {e}") 