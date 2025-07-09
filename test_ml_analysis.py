import requests
import json

def test_email_analysis():
    """Test email analysis with high-risk phishing email"""
    print("🧪 Testing Email Analysis with ML Models")
    print("=" * 50)
    
    # High-risk phishing email
    test_email = {
        "content": "URGENT: Your account has been suspended! Click here to verify: http://bit.ly/fake-bank",
        "sender": "security@fake-bank.com",
        "subject": "Account Verification Required"
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze/email', json=test_email)
        result = response.json()
        
        print(f"📧 Email Analysis Result:")
        print(f"   Risk Score: {result.get('risk_score', 0):.3f}")
        print(f"   Threat Level: {result.get('threat_level', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.3f}")
        print(f"   Analysis Time: {result.get('analysis_time', 0):.3f}s")
        
        # Check if ML model was used
        if result.get('risk_score', 0) > 0.5:
            print("✅ ML model detected high risk - GOOD!")
        elif result.get('risk_score', 0) > 0.1:
            print("⚠️ ML model detected some risk - ACCEPTABLE")
        else:
            print("❌ ML model detected no risk - NEEDS IMPROVEMENT")
            
    except Exception as e:
        print(f"❌ Error testing email analysis: {e}")

def test_transaction_analysis():
    """Test transaction analysis with high-risk transaction"""
    print("\n💳 Testing Transaction Analysis with ML Models")
    print("=" * 50)
    
    # High-risk transaction
    test_transaction = {
        "amount": 15000,
        "location": {"city": "Unknown", "distance_from_home": 1000},
        "timestamp": "2024-07-09T02:30:00Z",
        "user_id": "user123"
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze/transaction', json=test_transaction)
        result = response.json()
        
        print(f"💳 Transaction Analysis Result:")
        print(f"   Risk Score: {result.get('risk_score', 0):.3f}")
        print(f"   Threat Level: {result.get('threat_level', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.3f}")
        print(f"   Analysis Time: {result.get('analysis_time', 0):.3f}s")
        
        # Check if ML model was used
        if result.get('risk_score', 0) > 0.5:
            print("✅ ML model detected high risk - GOOD!")
        elif result.get('risk_score', 0) > 0.1:
            print("⚠️ ML model detected some risk - ACCEPTABLE")
        else:
            print("❌ ML model detected no risk - NEEDS IMPROVEMENT")
            
    except Exception as e:
        print(f"❌ Error testing transaction analysis: {e}")

def test_ai_status():
    """Test AI system status"""
    print("\n🤖 Testing AI System Status")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5000/api/ai/status')
        status = response.json()
        
        print(f"🤖 AI System Status:")
        print(f"   Active System: {status.get('active_ai_system', 'Unknown')}")
        print(f"   Advanced AI Available: {status.get('advanced_ai_available', False)}")
        print(f"   Models Loaded: {status.get('models_loaded', 0)}")
        
        performance = status.get('performance', {})
        if performance:
            print(f"   Performance Metrics:")
            for model, metrics in performance.items():
                accuracy = metrics.get('accuracy', 0)
                samples = metrics.get('samples', 0)
                print(f"     {model}: {accuracy:.3f} accuracy ({samples} samples)")
        else:
            print(f"   Performance Metrics: None (models not trained)")
            
    except Exception as e:
        print(f"❌ Error testing AI status: {e}")

def main():
    """Main test function"""
    print("🚨 Omni-Channel AI Scam & Fraud Detection Platform")
    print("🧪 ML Model Analysis Testing")
    print("=" * 60)
    
    # Test AI status first
    test_ai_status()
    
    # Test email analysis
    test_email_analysis()
    
    # Test transaction analysis
    test_transaction_analysis()
    
    print("\n🎯 SUMMARY:")
    print("   If risk scores are > 0.5: ML models are working well")
    print("   If risk scores are 0.1-0.5: ML models need improvement")
    print("   If risk scores are < 0.1: ML models are not learning properly")

if __name__ == "__main__":
    main() 