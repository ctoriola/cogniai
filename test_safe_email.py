import requests
import json

def test_safe_email():
    """Test with a safe email to compare results"""
    
    # Safe email
    safe_email = {
        "content": "Hello, this is a normal business email about our quarterly meeting next week. Please let me know if you have any questions.",
        "sender": "john.doe@company.com",
        "subject": "Quarterly Meeting Schedule"
    }
    
    print("🧪 Testing with safe email...")
    print(f"Content: {safe_email['content'][:100]}...")
    print(f"Sender: {safe_email['sender']}")
    print(f"Subject: {safe_email['subject']}")
    print("-" * 50)
    
    try:
        response = requests.post(
            "http://localhost:5000/analyze/email",
            json=safe_email,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            risk_score = result.get('risk_score', 0)
            threat_level = result.get('threat_level', 'UNKNOWN')
            
            print(f"✅ Risk Score: {risk_score:.1%}")
            print(f"✅ Threat Level: {threat_level}")
            print(f"✅ Channel: {result.get('channel', 'unknown')}")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_safe_email() 