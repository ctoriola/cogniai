#!/usr/bin/env python3
"""
Test script to evaluate the efficacy of pre-trained models
"""

import requests
import json
from datetime import datetime

def test_email_model_efficacy():
    """Test email model efficacy with various scenarios"""
    print("📧 Testing Email Model Efficacy")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "High Risk - Urgent Account Suspension",
            "data": {
                "content": "URGENT: Your account has been suspended! Click here to verify: http://bit.ly/fake-bank",
                "sender": "security@fake-bank.com",
                "subject": "Account Verification Required"
            },
            "expected_risk": "High"
        },
        {
            "name": "High Risk - Password Expiration",
            "data": {
                "content": "Your password will expire in 24 hours. Verify now: http://tinyurl.com/fake-login",
                "sender": "noreply@secure-bank.net",
                "subject": "Password Expiration Notice"
            },
            "expected_risk": "High"
        },
        {
            "name": "High Risk - Prize Scam",
            "data": {
                "content": "You have won $10,000! Claim your prize: http://bit.ly/fake-prize",
                "sender": "prize@lottery-winner.com",
                "subject": "Congratulations! You've Won!"
            },
            "expected_risk": "High"
        },
        {
            "name": "Medium Risk - Suspicious Newsletter",
            "data": {
                "content": "Click here to claim your free gift: http://goo.gl/fake-gift",
                "sender": "newsletter@suspicious-site.com",
                "subject": "Your Free Gift Awaits"
            },
            "expected_risk": "Medium"
        },
        {
            "name": "Low Risk - Legitimate Newsletter",
            "data": {
                "content": "Hello, here is your monthly newsletter with the latest updates.",
                "sender": "newsletter@company.com",
                "subject": "Monthly Newsletter - July 2024"
            },
            "expected_risk": "Low"
        },
        {
            "name": "Low Risk - Order Confirmation",
            "data": {
                "content": "Thank you for your recent purchase. Your order #12345 has been confirmed.",
                "sender": "orders@legitimate-store.com",
                "subject": "Order Confirmation - #12345"
            },
            "expected_risk": "Low"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        
        try:
            response = requests.post('http://localhost:5000/analyze/email', json=test_case['data'])
            result = response.json()
            
            risk_score = result.get('risk_score', 0)
            threat_level = result.get('threat_level', 'Unknown')
            
            print(f"   Risk Score: {risk_score:.3f}")
            print(f"   Threat Level: {threat_level}")
            print(f"   Expected: {test_case['expected_risk']}")
            
            # Evaluate efficacy
            if test_case['expected_risk'] == 'High' and risk_score > 0.7:
                efficacy = "✅ GOOD"
            elif test_case['expected_risk'] == 'Medium' and 0.3 < risk_score < 0.8:
                efficacy = "✅ GOOD"
            elif test_case['expected_risk'] == 'Low' and risk_score < 0.4:
                efficacy = "✅ GOOD"
            else:
                efficacy = "❌ POOR"
            
            print(f"   Efficacy: {efficacy}")
            
            results.append({
                'test': test_case['name'],
                'risk_score': risk_score,
                'threat_level': threat_level,
                'expected': test_case['expected_risk'],
                'efficacy': efficacy
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'test': test_case['name'],
                'error': str(e)
            })
    
    return results

def test_transaction_model_efficacy():
    """Test transaction model efficacy"""
    print("\n💳 Testing Transaction Model Efficacy")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "High Risk - Large Foreign Transaction",
            "data": {
                "amount": 15000,
                "location": {"city": "Unknown", "distance_from_home": 1000},
                "timestamp": "2024-07-09T02:30:00Z",
                "user_id": "user123"
            },
            "expected_risk": "High"
        },
        {
            "name": "High Risk - Negative Amount",
            "data": {
                "amount": -5000,
                "location": {"city": "Local", "distance_from_home": 5},
                "timestamp": "2024-07-09T12:30:00Z",
                "user_id": "user123"
            },
            "expected_risk": "High"
        },
        {
            "name": "Medium Risk - Unusual Time",
            "data": {
                "amount": 500,
                "location": {"city": "Local", "distance_from_home": 10},
                "timestamp": "2024-07-09T03:15:00Z",
                "user_id": "user123"
            },
            "expected_risk": "Medium"
        },
        {
            "name": "Low Risk - Normal Transaction",
            "data": {
                "amount": 150,
                "location": {"city": "Local", "distance_from_home": 5},
                "timestamp": "2024-07-09T14:30:00Z",
                "user_id": "user123"
            },
            "expected_risk": "Low"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        
        try:
            response = requests.post('http://localhost:5000/analyze/transaction', json=test_case['data'])
            result = response.json()
            
            risk_score = result.get('risk_score', 0)
            threat_level = result.get('threat_level', 'Unknown')
            
            print(f"   Risk Score: {risk_score:.3f}")
            print(f"   Threat Level: {threat_level}")
            print(f"   Expected: {test_case['expected_risk']}")
            
            # Evaluate efficacy
            if test_case['expected_risk'] == 'High' and risk_score > 0.6:
                efficacy = "✅ GOOD"
            elif test_case['expected_risk'] == 'Medium' and 0.3 < risk_score < 0.7:
                efficacy = "✅ GOOD"
            elif test_case['expected_risk'] == 'Low' and risk_score < 0.4:
                efficacy = "✅ GOOD"
            else:
                efficacy = "❌ POOR"
            
            print(f"   Efficacy: {efficacy}")
            
            results.append({
                'test': test_case['name'],
                'risk_score': risk_score,
                'threat_level': threat_level,
                'expected': test_case['expected_risk'],
                'efficacy': efficacy
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'test': test_case['name'],
                'error': str(e)
            })
    
    return results

def test_multi_modal_efficacy():
    """Test multi-modal model efficacy"""
    print("\n🔄 Testing Multi-Modal Model Efficacy")
    print("=" * 50)
    
    test_case = {
        "name": "Multi-Channel Attack Simulation",
        "data": {
            "email": {
                "content": "URGENT: Your account has been suspended!",
                "sender": "security@fake-bank.com",
                "subject": "Account Verification Required"
            },
            "transaction": {
                "amount": 15000,
                "location": {"city": "Unknown", "distance_from_home": 1000},
                "timestamp": "2024-07-09T02:30:00Z",
                "user_id": "user123"
            },
            "social_media": {
                "content": "FREE MONEY! Click here: http://bit.ly/fake-prize",
                "profile": {"followers": 5, "verified": False, "account_age_days": 2},
                "links": ["http://bit.ly/fake-prize"]
            }
        },
        "channels": ["email", "transaction", "social_media"],
        "expected_risk": "High"
    }
    
    print(f"\n🧪 Test: {test_case['name']}")
    
    try:
        response = requests.post('http://localhost:5000/analyze/multi_modal', json=test_case)
        result = response.json()
        
        fused_score = result.get('fused_risk_score', 0)
        threat_level = result.get('overall_threat_level', 'Unknown')
        
        print(f"   Fused Risk Score: {fused_score:.3f}")
        print(f"   Overall Threat Level: {threat_level}")
        print(f"   Expected: {test_case['expected_risk']}")
        
        # Evaluate efficacy
        if test_case['expected_risk'] == 'High' and fused_score > 0.7:
            efficacy = "✅ GOOD"
        else:
            efficacy = "❌ POOR"
        
        print(f"   Efficacy: {efficacy}")
        
        return [{
            'test': test_case['name'],
            'fused_risk_score': fused_score,
            'overall_threat_level': threat_level,
            'expected': test_case['expected_risk'],
            'efficacy': efficacy
        }]
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return [{
            'test': test_case['name'],
            'error': str(e)
        }]

def generate_efficacy_report(email_results, transaction_results, multi_modal_results):
    """Generate comprehensive efficacy report"""
    print("\n📊 MODEL EFFICACY REPORT")
    print("=" * 60)
    
    # Calculate success rates
    total_tests = len(email_results) + len(transaction_results) + len(multi_modal_results)
    successful_tests = 0
    
    for result in email_results + transaction_results + multi_modal_results:
        if 'efficacy' in result and '✅ GOOD' in result['efficacy']:
            successful_tests += 1
    
    success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Overall Success Rate: {success_rate:.1f}%")
    print(f"Successful Tests: {successful_tests}/{total_tests}")
    
    # Model-specific analysis
    print(f"\n📧 Email Model:")
    email_success = sum(1 for r in email_results if 'efficacy' in r and '✅ GOOD' in r['efficacy'])
    print(f"   Success Rate: {email_success}/{len(email_results)} ({email_success/len(email_results)*100:.1f}%)")
    
    print(f"\n💳 Transaction Model:")
    transaction_success = sum(1 for r in transaction_results if 'efficacy' in r and '✅ GOOD' in r['efficacy'])
    print(f"   Success Rate: {transaction_success}/{len(transaction_results)} ({transaction_success/len(transaction_results)*100:.1f}%)")
    
    print(f"\n🔄 Multi-Modal Model:")
    multi_modal_success = sum(1 for r in multi_modal_results if 'efficacy' in r and '✅ GOOD' in r['efficacy'])
    print(f"   Success Rate: {multi_modal_success}/{len(multi_modal_results)} ({multi_modal_success/len(multi_modal_results)*100:.1f}%)")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if success_rate < 70:
        print("   ⚠️  Model performance is below optimal levels")
        print("   🔧 Consider training with more diverse data")
        print("   📈 Fine-tune feature weights and thresholds")
    elif success_rate < 85:
        print("   ✅ Model performance is acceptable")
        print("   🔧 Minor improvements possible with training")
    else:
        print("   🎉 Excellent model performance!")
        print("   ✅ Models are ready for production use")
    
    return {
        'overall_success_rate': success_rate,
        'email_success_rate': email_success/len(email_results)*100 if email_results else 0,
        'transaction_success_rate': transaction_success/len(transaction_results)*100 if transaction_results else 0,
        'multi_modal_success_rate': multi_modal_success/len(multi_modal_results)*100 if multi_modal_results else 0
    }

def main():
    """Main testing function"""
    print("🚨 Omni-Channel AI Scam & Fraud Detection Platform")
    print("🧪 Pre-trained Model Efficacy Testing")
    print("=" * 60)
    
    # Test each model type
    email_results = test_email_model_efficacy()
    transaction_results = test_transaction_model_efficacy()
    multi_modal_results = test_multi_modal_efficacy()
    
    # Generate comprehensive report
    report = generate_efficacy_report(email_results, transaction_results, multi_modal_results)
    
    print(f"\n📋 SUMMARY:")
    print(f"   Email Model: {report['email_success_rate']:.1f}% efficacy")
    print(f"   Transaction Model: {report['transaction_success_rate']:.1f}% efficacy")
    print(f"   Multi-Modal Model: {report['multi_modal_success_rate']:.1f}% efficacy")
    print(f"   Overall: {report['overall_success_rate']:.1f}% efficacy")
    
    print(f"\n🎯 CONCLUSION:")
    if report['overall_success_rate'] >= 80:
        print("   ✅ Pre-trained models show good efficacy")
        print("   🚀 Ready for production use with monitoring")
    elif report['overall_success_rate'] >= 60:
        print("   ⚠️  Pre-trained models show acceptable efficacy")
        print("   🔧 Consider training with domain-specific data")
    else:
        print("   ❌ Pre-trained models need improvement")
        print("   🔧 Training with custom data recommended")

if __name__ == "__main__":
    main() 