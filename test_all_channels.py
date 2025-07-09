import requests
import json

def test_all_channels():
    """Test all channels to identify any issues"""
    
    print("🧪 Testing All Channels")
    print("=" * 50)
    
    # Test cases for each channel
    test_cases = {
        'email': {
            'safe': {
                'content': 'Hello, this is a normal business email about our quarterly meeting.',
                'sender': 'john.doe@company.com',
                'subject': 'Quarterly Meeting Schedule'
            },
            'scam': {
                'content': 'URGENT: Your bank account has been suspended. Click here immediately: http://bit.ly/verify-now',
                'sender': 'security@bank-verify.com',
                'subject': 'ACCOUNT SUSPENDED - IMMEDIATE ACTION REQUIRED'
            }
        },
        'webpage': {
            'safe': {
                'url': 'https://www.google.com',
                'content': 'Welcome to Google. Search the web.'
            },
            'scam': {
                'url': 'http://bit.ly/fake-bank-login',
                'content': 'Please enter your bank account details and password to verify your account.'
            }
        },
        'social_media': {
            'safe': {
                'content': 'Great meeting everyone at the conference today! #networking',
                'profile': {'followers': 500, 'verified': True, 'account_age_days': 365},
                'links': []
            },
            'scam': {
                'content': 'URGENT: You have won a prize! Click here to claim: http://tinyurl.com/prize',
                'profile': {'followers': 5, 'verified': False, 'account_age_days': 2},
                'links': ['http://tinyurl.com/prize']
            }
        },
        'transaction': {
            'safe': {
                'amount': 50.00,
                'location': {'country': 'US', 'distance_from_home': 5},
                'timestamp': '2024-01-15T14:30:00Z',
                'user_id': 'user123'
            },
            'scam': {
                'amount': 15000.00,
                'location': {'country': 'XX', 'distance_from_home': 5000},
                'timestamp': '2024-01-15T03:00:00Z',
                'user_id': 'user123'
            }
        }
    }
    
    results = {}
    
    for channel, cases in test_cases.items():
        print(f"\n📊 Testing {channel.upper()} channel:")
        print("-" * 30)
        
        channel_results = {}
        
        for case_type, data in cases.items():
            print(f"\n  Testing {case_type} {channel}...")
            
            try:
                response = requests.post(
                    f"http://localhost:5000/analyze/{channel}",
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    risk_score = result.get('risk_score', 0)
                    threat_level = result.get('threat_level', 'UNKNOWN')
                    
                    print(f"    ✅ Risk Score: {risk_score:.1%}")
                    print(f"    ✅ Threat Level: {threat_level}")
                    
                    # Check for potential issues
                    issues = []
                    if case_type == 'safe' and risk_score > 0.5:
                        issues.append("Safe case showing high risk")
                    elif case_type == 'scam' and risk_score < 0.3:
                        issues.append("Scam case showing low risk")
                    
                    if issues:
                        print(f"    ⚠️  Issues: {', '.join(issues)}")
                    
                    channel_results[case_type] = {
                        'risk_score': risk_score,
                        'threat_level': threat_level,
                        'issues': issues
                    }
                    
                else:
                    print(f"    ❌ Error: {response.status_code}")
                    channel_results[case_type] = {'error': f"HTTP {response.status_code}"}
                    
            except Exception as e:
                print(f"    ❌ Request failed: {e}")
                channel_results[case_type] = {'error': str(e)}
        
        results[channel] = channel_results
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    for channel, channel_results in results.items():
        print(f"\n{channel.upper()}:")
        for case_type, result in channel_results.items():
            if 'error' in result:
                print(f"  {case_type}: ❌ {result['error']}")
            else:
                risk_score = result['risk_score']
                threat_level = result['threat_level']
                issues = result.get('issues', [])
                
                status = "✅" if not issues else "⚠️"
                print(f"  {case_type}: {status} {risk_score:.1%} ({threat_level})")
                if issues:
                    for issue in issues:
                        print(f"    - {issue}")
    
    return results

def test_ai_status():
    """Test AI system status"""
    print("\n🤖 Testing AI System Status")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:5000/api/ai/status", timeout=10)
        
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Advanced AI Available: {status.get('advanced_ai_available', False)}")
            print(f"✅ Active AI System: {status.get('active_ai_system', 'unknown')}")
            print(f"✅ Trained Models: {status.get('trained_models', [])}")
            
            performance = status.get('performance', {})
            if performance:
                print("✅ Model Performance:")
                for model, perf in performance.items():
                    accuracy = perf.get('accuracy', 0)
                    samples = perf.get('samples', 0)
                    print(f"  - {model}: {accuracy:.1%} accuracy ({samples} samples)")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_nlp_analysis():
    """Test NLP analysis endpoint"""
    print("\n📝 Testing NLP Analysis")
    print("-" * 30)
    
    test_texts = [
        "Hello, this is a normal message.",
        "URGENT: Your account has been suspended. Click here immediately!"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n  Testing text {i}: {text[:50]}...")
        
        try:
            response = requests.post(
                "http://localhost:5000/api/nlp/analyze",
                json={'text': text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get('analysis', {})
                risk_assessment = analysis.get('risk_assessment', {})
                overall_risk = risk_assessment.get('overall_nlp_risk', 0)
                
                print(f"    ✅ Overall NLP Risk: {overall_risk:.1f}%")
                
                # Check fraud indicators
                fraud_indicators = analysis.get('fraud_indicators', {})
                total_indicators = fraud_indicators.get('total_fraud_indicators', 0)
                print(f"    ✅ Fraud Indicators: {total_indicators}")
                
            else:
                print(f"    ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Request failed: {e}")

if __name__ == "__main__":
    test_all_channels()
    test_ai_status()
    test_nlp_analysis() 