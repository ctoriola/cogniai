#!/usr/bin/env python3
"""
Comprehensive training script for all AI models
"""

import requests
import json
import time
from datetime import datetime

def train_email_model():
    """Train email model with comprehensive data"""
    print("📧 Training Email Model with Comprehensive Data")
    print("=" * 50)
    
    training_data = [
        # High Risk - Phishing Emails
        {
            "data": {
                "content": "URGENT: Your account has been suspended! Click here to verify: http://bit.ly/fake-bank",
                "sender": "security@fake-bank.com",
                "subject": "Account Verification Required"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Your password will expire in 24 hours. Verify now: http://tinyurl.com/fake-login",
                "sender": "noreply@secure-bank.net",
                "subject": "Password Expiration Notice"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "You have won $10,000! Claim your prize: http://bit.ly/fake-prize",
                "sender": "prize@lottery-winner.com",
                "subject": "Congratulations! You've Won!"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Your account has been compromised. Immediate action required: http://goo.gl/fake-security",
                "sender": "security@account-protection.org",
                "subject": "Security Alert - Account Compromised"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Your payment has been declined. Update your information: http://is.gd/fake-payment",
                "sender": "billing@payment-service.com",
                "subject": "Payment Declined - Action Required"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Your account will be terminated unless you verify: http://bit.ly/fake-verify",
                "sender": "support@account-service.net",
                "subject": "Account Termination Notice"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "FREE iPhone! Click here to claim: http://tinyurl.com/fake-iphone",
                "sender": "promotions@free-gifts.com",
                "subject": "Claim Your Free iPhone"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Your credit card has been charged $999. Dispute here: http://goo.gl/fake-dispute",
                "sender": "billing@credit-service.org",
                "subject": "Unauthorized Charge Alert"
            },
            "is_fraud": True
        },
        
        # Medium Risk - Suspicious Emails
        {
            "data": {
                "content": "Click here to claim your free gift: http://goo.gl/fake-gift",
                "sender": "newsletter@suspicious-site.com",
                "subject": "Your Free Gift Awaits"
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Make money fast! Join our program: http://bit.ly/fake-money",
                "sender": "opportunity@money-making.com",
                "subject": "Earn $5000 Weekly"
            },
            "is_fraud": True
        },
        
        # Low Risk - Legitimate Emails
        {
            "data": {
                "content": "Hello, here is your monthly newsletter with the latest updates.",
                "sender": "newsletter@company.com",
                "subject": "Monthly Newsletter - July 2024"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Thank you for your recent purchase. Your order #12345 has been confirmed.",
                "sender": "orders@legitimate-store.com",
                "subject": "Order Confirmation - #12345"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Your meeting reminder: Team standup tomorrow at 9 AM.",
                "sender": "calendar@company.com",
                "subject": "Meeting Reminder - Team Standup"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Your password was successfully changed. If this wasn't you, contact support.",
                "sender": "security@legitimate-bank.com",
                "subject": "Password Changed Successfully"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Welcome to our service! Here's how to get started with your account.",
                "sender": "welcome@service.com",
                "subject": "Welcome to Our Service"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Your subscription has been renewed. Thank you for your business.",
                "sender": "billing@legitimate-service.com",
                "subject": "Subscription Renewed"
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Your account has been successfully created. Welcome aboard!",
                "sender": "welcome@new-service.com",
                "subject": "Account Created Successfully"
            },
            "is_fraud": False
        }
    ]
    
    try:
        response = requests.post('http://localhost:5000/api/ai/train', json={
            'channel': 'email',
            'training_data': training_data
        })
        
        print(f"✅ Email model trained with {len(training_data)} samples")
        print(f"📊 Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Error training email model: {e}")

def train_transaction_model():
    """Train transaction model with comprehensive data"""
    print("\n💳 Training Transaction Model with Comprehensive Data")
    print("=" * 50)
    
    training_data = [
        # High Risk - Fraudulent Transactions
        {
            "data": {
                "amount": 15000,
                "location": {"city": "Unknown", "distance_from_home": 1000},
                "timestamp": "2024-07-09T02:30:00Z",
                "user_id": "user123"
            },
            "is_fraud": True
        },
        {
            "data": {
                "amount": -5000,
                "location": {"city": "Local", "distance_from_home": 5},
                "timestamp": "2024-07-09T12:30:00Z",
                "user_id": "user123"
            },
            "is_fraud": True
        },
        {
            "data": {
                "amount": 25000,
                "location": {"city": "Unknown", "distance_from_home": 2000},
                "timestamp": "2024-07-09T04:00:00Z",
                "user_id": "user456"
            },
            "is_fraud": True
        },
        {
            "data": {
                "amount": 50000,
                "location": {"city": "Foreign", "distance_from_home": 5000},
                "timestamp": "2024-07-09T03:15:00Z",
                "user_id": "user789"
            },
            "is_fraud": True
        },
        {
            "data": {
                "amount": -15000,
                "location": {"city": "Unknown", "distance_from_home": 1500},
                "timestamp": "2024-07-09T01:45:00Z",
                "user_id": "user123"
            },
            "is_fraud": True
        },
        
        # Medium Risk - Suspicious Transactions
        {
            "data": {
                "amount": 5000,
                "location": {"city": "Local", "distance_from_home": 50},
                "timestamp": "2024-07-09T03:30:00Z",
                "user_id": "user123"
            },
            "is_fraud": True
        },
        {
            "data": {
                "amount": 3000,
                "location": {"city": "Local", "distance_from_home": 100},
                "timestamp": "2024-07-09T02:00:00Z",
                "user_id": "user456"
            },
            "is_fraud": True
        },
        
        # Low Risk - Legitimate Transactions
        {
            "data": {
                "amount": 150,
                "location": {"city": "Local", "distance_from_home": 5},
                "timestamp": "2024-07-09T12:30:00Z",
                "user_id": "user123"
            },
            "is_fraud": False
        },
        {
            "data": {
                "amount": 75,
                "location": {"city": "Local", "distance_from_home": 10},
                "timestamp": "2024-07-09T14:15:00Z",
                "user_id": "user123"
            },
            "is_fraud": False
        },
        {
            "data": {
                "amount": 200,
                "location": {"city": "Local", "distance_from_home": 15},
                "timestamp": "2024-07-09T16:45:00Z",
                "user_id": "user456"
            },
            "is_fraud": False
        },
        {
            "data": {
                "amount": 50,
                "location": {"city": "Local", "distance_from_home": 2},
                "timestamp": "2024-07-09T18:20:00Z",
                "user_id": "user789"
            },
            "is_fraud": False
        },
        {
            "data": {
                "amount": 300,
                "location": {"city": "Local", "distance_from_home": 20},
                "timestamp": "2024-07-09T19:30:00Z",
                "user_id": "user123"
            },
            "is_fraud": False
        }
    ]
    
    try:
        response = requests.post('http://localhost:5000/api/ai/train', json={
            'channel': 'transaction',
            'training_data': training_data
        })
        
        print(f"✅ Transaction model trained with {len(training_data)} samples")
        print(f"📊 Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Error training transaction model: {e}")

def train_social_media_model():
    """Train social media model with comprehensive data"""
    print("\n📱 Training Social Media Model with Comprehensive Data")
    print("=" * 50)
    
    training_data = [
        # High Risk - Fraudulent Social Media Posts
        {
            "data": {
                "content": "FREE MONEY! Click here to claim your prize: http://bit.ly/fake-prize",
                "profile": {"followers": 5, "verified": False, "account_age_days": 2},
                "links": ["http://bit.ly/fake-prize"]
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Make $1000/day working from home! DM me for details #money #workfromhome",
                "profile": {"followers": 50, "verified": False, "account_age_days": 5},
                "links": []
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "FREE iPhone! Click here: http://tinyurl.com/fake-iphone",
                "profile": {"followers": 10, "verified": False, "account_age_days": 1},
                "links": ["http://tinyurl.com/fake-iphone"]
            },
            "is_fraud": True
        },
        {
            "data": {
                "content": "Earn $5000 weekly! Join our program: http://bit.ly/fake-earn",
                "profile": {"followers": 25, "verified": False, "account_age_days": 3},
                "links": ["http://bit.ly/fake-earn"]
            },
            "is_fraud": True
        },
        
        # Low Risk - Legitimate Social Media Posts
        {
            "data": {
                "content": "Great meeting with the team today! #work #collaboration",
                "profile": {"followers": 500, "verified": True, "account_age_days": 365},
                "links": []
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Check out our new product launch: https://legitimate-company.com",
                "profile": {"followers": 1000, "verified": True, "account_age_days": 730},
                "links": ["https://legitimate-company.com"]
            },
            "is_fraud": False
        },
        {
            "data": {
                "content": "Happy to announce our latest achievement! #success #milestone",
                "profile": {"followers": 250, "verified": True, "account_age_days": 180},
                "links": []
            },
            "is_fraud": False
        }
    ]
    
    try:
        response = requests.post('http://localhost:5000/api/ai/train', json={
            'channel': 'social_media',
            'training_data': training_data
        })
        
        print(f"✅ Social media model trained with {len(training_data)} samples")
        print(f"📊 Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Error training social media model: {e}")

def save_and_verify_models():
    """Save models and verify training results"""
    print("\n💾 Saving and Verifying Models")
    print("=" * 50)
    
    try:
        # Save models
        save_response = requests.post('http://localhost:5000/api/ai/save')
        print(f"💾 Save Response: {save_response.json()}")
        
        # Load models
        load_response = requests.post('http://localhost:5000/api/ai/load')
        print(f"📂 Load Response: {load_response.json()}")
        
        # Check final status
        status_response = requests.get('http://localhost:5000/api/ai/status')
        final_status = status_response.json()
        print(f"🔍 Final Status: {json.dumps(final_status, indent=2)}")
        
        return final_status
        
    except Exception as e:
        print(f"❌ Error in save/verify: {e}")
        return None

def test_improved_models():
    """Test the improved models"""
    print("\n🧪 Testing Improved Models")
    print("=" * 50)
    
    # Test high-risk email
    test_email = {
        "content": "URGENT: Your account has been suspended! Click here to verify: http://bit.ly/fake-bank",
        "sender": "security@fake-bank.com",
        "subject": "Account Verification Required"
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze/email', json=test_email)
        result = response.json()
        print(f"📧 High-risk email test:")
        print(f"   Risk Score: {result.get('risk_score', 0):.3f}")
        print(f"   Threat Level: {result.get('threat_level', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing email: {e}")
    
    # Test high-risk transaction
    test_transaction = {
        "amount": 15000,
        "location": {"city": "Unknown", "distance_from_home": 1000},
        "timestamp": "2024-07-09T02:30:00Z",
        "user_id": "user123"
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze/transaction', json=test_transaction)
        result = response.json()
        print(f"\n💳 High-risk transaction test:")
        print(f"   Risk Score: {result.get('risk_score', 0):.3f}")
        print(f"   Threat Level: {result.get('threat_level', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing transaction: {e}")

def main():
    """Main training function"""
    print("🚨 Omni-Channel AI Scam & Fraud Detection Platform")
    print("🎯 Comprehensive Model Training")
    print("=" * 60)
    
    # Train all models
    train_email_model()
    train_transaction_model()
    train_social_media_model()
    
    # Save and verify
    final_status = save_and_verify_models()
    
    # Test improved models
    test_improved_models()
    
    print("\n🎉 Training completed!")
    print("📈 Models should now show improved performance")
    print("🌐 Visit http://localhost:5000/dashboard to see the results")

if __name__ == "__main__":
    main() 