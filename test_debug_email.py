import requests
import json

def test_scam_email():
    """Test with a clear scam email to see debug output"""
    
    # Clear scam email
    scam_email = {
        "content": "URGENT: Your bank account has been suspended due to suspicious activity. Click here immediately to verify your identity: http://bit.ly/verify-now. If you don't act within 24 hours, your account will be permanently blocked.",
        "sender": "security@bank-verify.com", 
        "subject": "ACCOUNT SUSPENDED - IMMEDIATE ACTION REQUIRED"
    }
    
    print("🧪 Testing with clear scam email...")
    print(f"Content: {scam_email['content'][:100]}...")
    print(f"Sender: {scam_email['sender']}")
    print(f"Subject: {scam_email['subject']}")
    print("-" * 50)
    
    try:
        response = requests.post(
            "http://localhost:5000/analyze/email",
            json=scam_email,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            risk_score = result.get('risk_score', 0)
            threat_level = result.get('threat_level', 'UNKNOWN')
            
            print(f"✅ Risk Score: {risk_score:.1%}")
            print(f"✅ Threat Level: {threat_level}")
            print(f"✅ Channel: {result.get('channel', 'unknown')}")
            
            # Show some features if available
            features = result.get('features', {})
            if features:
                print(f"✅ Features extracted: {len(features)} keys")
                # Show some key features
                key_features = ['urgency_score', 'financial_terms', 'threat_indicators', 'has_links']
                for key in key_features:
                    if key in features:
                        print(f"   - {key}: {features[key]}")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_scam_email() 