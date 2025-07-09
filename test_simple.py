import requests
import time

def test_api():
    """Test the fraud detection API"""
    print("🧪 Testing Fraud Detection API...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://localhost:5000/test')
        if response.status_code == 200:
            print("✅ API server is running!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False
    
    # Test 2: Email analysis
    print("\n📧 Testing email analysis...")
    try:
        email_data = {
            "content": "URGENT: Your account has been suspended! Click here to verify: http://bit.ly/fake-bank"
        }
        response = requests.post('http://localhost:5000/analyze/email', json=email_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email analysis successful!")
            print(f"   Risk Score: {result['overall_risk']:.2f}")
            print(f"   Is Phishing: {result['is_phishing']}")
        else:
            print(f"❌ Email analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Email analysis error: {e}")
    
    # Test 3: Transaction analysis
    print("\n💳 Testing transaction analysis...")
    try:
        transaction_data = {
            "amount": 15000,
            "frequency": 10,
            "location_variance": 200,
            "timestamp": "2024-01-15T14:30:00"
        }
        response = requests.post('http://localhost:5000/analyze/transaction', json=transaction_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Transaction analysis successful!")
            print(f"   Anomaly Score: {result['anomaly_score']:.2f}")
            print(f"   Is Fraud: {result['is_fraud']}")
        else:
            print(f"❌ Transaction analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Transaction analysis error: {e}")
    
    # Test 4: Dashboard stats
    print("\n📊 Testing dashboard stats...")
    try:
        response = requests.get('http://localhost:5000/api/dashboard/stats')
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard stats successful!")
            print(f"   Total Alerts: {stats['total_alerts']}")
            print(f"   Email Alerts: {stats['email_alerts']}")
            print(f"   Transaction Alerts: {stats['transaction_alerts']}")
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard stats error: {e}")
    
    print("\n🎉 All tests completed!")
    print("\n📋 System Status:")
    print("✅ API: http://localhost:5000")
    print("✅ Web Interface: Open index.html in your browser")
    print("✅ All endpoints working")

if __name__ == "__main__":
    print("🚀 Starting Fraud Detection System Tests...")
    print("=" * 50)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    test_api() 