#!/usr/bin/env python3
"""
Test script to verify email analysis fix
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_email_analysis():
    """Test email analysis with different inputs"""
    
    print("🧪 Testing Email Analysis Fix")
    
    # Test cases
    test_cases = [
        {
            "name": "Safe Email",
            "data": {
                "content": "Hello, this is a normal business email.",
                "sender": "john.doe@company.com",
                "subject": "Meeting Schedule"
            }
        },
        {
            "name": "Suspicious Email", 
            "data": {
                "content": "URGENT: Your account suspended. Click here: http://bit.ly/verify",
                "sender": "security@bank-verify.com",
                "subject": "ACCOUNT SUSPENDED"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📧 Test: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/analyze/email",
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                risk_score = result.get('risk_score', 0)
                print(f"✅ Risk Score: {risk_score:.1%}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_email_analysis() 