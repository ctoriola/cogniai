import requests
import json

def test_simple_training():
    """Test simple training with more data"""
    print("🧪 Testing simple AI training...")
    
    # More comprehensive training data
    training_data = [
        # Fraudulent emails
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
        
        # Legitimate emails
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
        }
    ]
    
    try:
        # Train email model
        print("📧 Training email model...")
        response = requests.post('http://localhost:5000/api/ai/train', json={
            'channel': 'email',
            'training_data': training_data
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check status after training
        print("\n🔍 Checking AI status after training...")
        status_response = requests.get('http://localhost:5000/api/ai/status')
        status = status_response.json()
        print(f"Status: {json.dumps(status, indent=2)}")
        
        # Save models
        print("\n💾 Saving models...")
        save_response = requests.post('http://localhost:5000/api/ai/save')
        print(f"Save Response: {save_response.json()}")
        
        # Load models
        print("\n📂 Loading models...")
        load_response = requests.post('http://localhost:5000/api/ai/load')
        print(f"Load Response: {load_response.json()}")
        
        # Check final status
        print("\n🔍 Final AI status...")
        final_status = requests.get('http://localhost:5000/api/ai/status').json()
        print(f"Final Status: {json.dumps(final_status, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple_training() 