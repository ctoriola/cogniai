#!/usr/bin/env python3
"""
Enhanced ML Model Training Script
Trains all fraud detection models with more diverse and realistic data
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def create_enhanced_training_data():
    """Create comprehensive training data with more diverse examples"""
    
    training_data = {
        'email': {
            'fraudulent': [
                {
                    'data': {
                        'content': 'URGENT: Your account has been suspended due to suspicious activity. Click here to verify your identity immediately: http://bit.ly/fake-bank-verify',
                        'sender': 'security@bank-verify.net',
                        'subject': 'URGENT: Account Suspended - Immediate Action Required'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Congratulations! You have won $50,000 in our lottery. To claim your prize, send your bank details and social security number to: claim@lottery-winner.com',
                        'sender': 'lottery@winner-notification.org',
                        'subject': 'CONGRATULATIONS! You Won $50,000!'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Your PayPal account will be limited unless you verify your identity. Click here to update your information: http://paypal-secure-verify.com',
                        'sender': 'paypal-security@paypal-verify.net',
                        'subject': 'PayPal Account Limited - Action Required'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Your Netflix subscription has been cancelled due to payment issues. Click here to update your payment method: http://netflix-billing-verify.com',
                        'sender': 'netflix@billing-update.net',
                        'subject': 'Netflix Payment Failed - Account Suspended'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Your Apple ID has been locked for security reasons. Verify your identity here: http://apple-id-verify.com',
                        'sender': 'apple@id-security.net',
                        'subject': 'Apple ID Locked - Security Alert'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'FREE iPhone 15! Just click here to claim: http://free-iphone-scam.com',
                        'sender': 'giveaway@free-iphone.net',
                        'subject': 'FREE iPhone 15 - Limited Time Offer!'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Your bank account has been compromised. Transfer your money immediately to this secure account: 1234-5678-9012',
                        'sender': 'bank-security@secure-transfer.net',
                        'subject': 'URGENT: Bank Account Compromised'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'You have inherited $1,000,000 from a distant relative. Contact us immediately: inheritance@million-dollar.net',
                        'sender': 'inheritance@million-dollar.net',
                        'subject': 'URGENT: Million Dollar Inheritance'
                    },
                    'is_fraud': True
                }
            ],
            'legitimate': [
                {
                    'data': {
                        'content': 'Thank you for your recent purchase. Your order #12345 has been confirmed and will be shipped within 2-3 business days.',
                        'sender': 'orders@amazon.com',
                        'subject': 'Order Confirmation - Amazon'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Your monthly statement is now available. Please log in to your account to view your transactions.',
                        'sender': 'statements@chase.com',
                        'subject': 'Monthly Statement Available'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Welcome to our newsletter! Here are this week\'s updates on cybersecurity best practices.',
                        'sender': 'newsletter@security-company.com',
                        'subject': 'Weekly Security Newsletter'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Your password was changed successfully. If this wasn\'t you, please contact support immediately.',
                        'sender': 'security@google.com',
                        'subject': 'Password Changed Successfully'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Your subscription to Premium Plan has been renewed. Thank you for your continued support.',
                        'sender': 'billing@legitimate-service.com',
                        'subject': 'Subscription Renewed'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Hi John, just checking in to see how the project is going. Let me know if you need anything.',
                        'sender': 'colleague@company.com',
                        'subject': 'Project Update'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Your flight has been confirmed for tomorrow. Please arrive 2 hours before departure.',
                        'sender': 'bookings@airline.com',
                        'subject': 'Flight Confirmation'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Thank you for your donation. Your receipt is attached.',
                        'sender': 'donations@charity.org',
                        'subject': 'Donation Receipt'
                    },
                    'is_fraud': False
                }
            ]
        },
        'transaction': {
            'fraudulent': [
                {
                    'data': {
                        'amount': 25000,
                        'location': {'city': 'Moscow', 'country': 'Russia'},
                        'timestamp': '2024-01-15T03:30:00Z',
                        'user_id': 'user123'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': -5000,
                        'location': {'city': 'Lagos', 'country': 'Nigeria'},
                        'timestamp': '2024-01-15T02:15:00Z',
                        'user_id': 'user456'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': 15000,
                        'location': {'city': 'Beijing', 'country': 'China'},
                        'timestamp': '2024-01-15T01:45:00Z',
                        'user_id': 'user789'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': 8000,
                        'location': {'city': 'Istanbul', 'country': 'Turkey'},
                        'timestamp': '2024-01-15T00:30:00Z',
                        'user_id': 'user101'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': 12000,
                        'location': {'city': 'Dubai', 'country': 'UAE'},
                        'timestamp': '2024-01-15T04:20:00Z',
                        'user_id': 'user202'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': -15000,
                        'location': {'city': 'Mumbai', 'country': 'India'},
                        'timestamp': '2024-01-15T05:45:00Z',
                        'user_id': 'user303'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': 30000,
                        'location': {'city': 'Bangkok', 'country': 'Thailand'},
                        'timestamp': '2024-01-15T06:30:00Z',
                        'user_id': 'user404'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'amount': -8000,
                        'location': {'city': 'Jakarta', 'country': 'Indonesia'},
                        'timestamp': '2024-01-15T07:15:00Z',
                        'user_id': 'user505'
                    },
                    'is_fraud': True
                }
            ],
            'legitimate': [
                {
                    'data': {
                        'amount': 150,
                        'location': {'city': 'New York', 'country': 'USA'},
                        'timestamp': '2024-01-15T12:30:00Z',
                        'user_id': 'user123'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 75,
                        'location': {'city': 'San Francisco', 'country': 'USA'},
                        'timestamp': '2024-01-15T18:45:00Z',
                        'user_id': 'user456'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 200,
                        'location': {'city': 'Chicago', 'country': 'USA'},
                        'timestamp': '2024-01-15T14:20:00Z',
                        'user_id': 'user789'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 50,
                        'location': {'city': 'Boston', 'country': 'USA'},
                        'timestamp': '2024-01-15T16:15:00Z',
                        'user_id': 'user101'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 300,
                        'location': {'city': 'Los Angeles', 'country': 'USA'},
                        'timestamp': '2024-01-15T19:30:00Z',
                        'user_id': 'user202'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 25,
                        'location': {'city': 'Seattle', 'country': 'USA'},
                        'timestamp': '2024-01-15T10:45:00Z',
                        'user_id': 'user303'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 100,
                        'location': {'city': 'Austin', 'country': 'USA'},
                        'timestamp': '2024-01-15T11:20:00Z',
                        'user_id': 'user404'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'amount': 80,
                        'location': {'city': 'Denver', 'country': 'USA'},
                        'timestamp': '2024-01-15T13:10:00Z',
                        'user_id': 'user505'
                    },
                    'is_fraud': False
                }
            ]
        },
        'social_media': {
            'fraudulent': [
                {
                    'data': {
                        'content': 'Earn $5000 daily! Join our crypto investment program. DM for details! 💰💰💰',
                        'profile': {'followers': 5, 'verified': False, 'account_age_days': 2},
                        'links': ['http://crypto-scam.com']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'FREE iPhone 15! Just share this post and follow us! Limited time offer! 📱',
                        'profile': {'followers': 12, 'verified': False, 'account_age_days': 1},
                        'links': ['http://fake-giveaway.com']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Make money fast! Join our pyramid scheme. Guaranteed returns! 💸',
                        'profile': {'followers': 8, 'verified': False, 'account_age_days': 3},
                        'links': ['http://pyramid-scheme.net']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Hot singles in your area! Click here to meet them now! 🔥',
                        'profile': {'followers': 15, 'verified': False, 'account_age_days': 1},
                        'links': ['http://dating-scam.com']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Your account has been hacked! Click here to secure it immediately! 🔒',
                        'profile': {'followers': 7, 'verified': False, 'account_age_days': 2},
                        'links': ['http://fake-security.com']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'WIN $10,000! Just retweet and follow! 🎉💰',
                        'profile': {'followers': 3, 'verified': False, 'account_age_days': 1},
                        'links': ['http://fake-contest.com']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'Get rich quick! Bitcoin investment opportunity! 🚀',
                        'profile': {'followers': 6, 'verified': False, 'account_age_days': 2},
                        'links': ['http://bitcoin-scam.net']
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'content': 'FREE gift cards! Click here to claim! 🎁',
                        'profile': {'followers': 4, 'verified': False, 'account_age_days': 1},
                        'links': ['http://gift-card-scam.com']
                    },
                    'is_fraud': True
                }
            ],
            'legitimate': [
                {
                    'data': {
                        'content': 'Great article about cybersecurity best practices. Worth reading! 🔒',
                        'profile': {'followers': 1500, 'verified': True, 'account_age_days': 730},
                        'links': ['https://legitimate-article.com']
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Happy to announce our new product launch! Check it out! 🚀',
                        'profile': {'followers': 5000, 'verified': True, 'account_age_days': 1095},
                        'links': ['https://company-website.com']
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Beautiful sunset at the beach today! 🌅 #photography #nature',
                        'profile': {'followers': 800, 'verified': False, 'account_age_days': 365},
                        'links': []
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Excited to share our latest research findings on AI safety! 🤖',
                        'profile': {'followers': 2500, 'verified': True, 'account_age_days': 1460},
                        'links': ['https://research-paper.com']
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Thanks everyone for the birthday wishes! 🎉',
                        'profile': {'followers': 1200, 'verified': False, 'account_age_days': 1825},
                        'links': []
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Just finished a great workout! 💪 #fitness #motivation',
                        'profile': {'followers': 600, 'verified': False, 'account_age_days': 548},
                        'links': []
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'Amazing coffee at the local cafe! ☕ #coffee #local',
                        'profile': {'followers': 900, 'verified': False, 'account_age_days': 730},
                        'links': []
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'content': 'New blog post about machine learning trends! 📊',
                        'profile': {'followers': 3000, 'verified': True, 'account_age_days': 1095},
                        'links': ['https://tech-blog.com']
                    },
                    'is_fraud': False
                }
            ]
        },
        'webpage': {
            'fraudulent': [
                {
                    'data': {
                        'url': 'http://bit.ly/fake-bank-login',
                        'content': '<form action="/login">Enter your credentials</form>'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'url': 'http://secure-login.tk',
                        'content': '<form action="/login">Sign in to your account</form>'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'url': 'http://paypal-verify.ga',
                        'content': '<form action="/verify">Verify your PayPal account</form>'
                    },
                    'is_fraud': True
                },
                {
                    'data': {
                        'url': 'http://update-account.cf',
                        'content': '<form action="/update">Update your account info</form>'
                    },
                    'is_fraud': True
                }
            ],
            'legitimate': [
                {
                    'data': {
                        'url': 'https://www.amazon.com',
                        'content': '<form action="/search">Search for products</form>'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'url': 'https://www.bankofamerica.com',
                        'content': '<form action="/login">Login to your bank account</form>'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'url': 'https://www.wikipedia.org',
                        'content': '<form action="/search">Search Wikipedia</form>'
                    },
                    'is_fraud': False
                },
                {
                    'data': {
                        'url': 'https://www.google.com',
                        'content': '<form action="/search">Google Search</form>'
                    },
                    'is_fraud': False
                }
            ]
        }
    }
    
    return training_data

def train_enhanced_models():
    """Train all models with enhanced comprehensive data"""
    
    print("🚀 Starting Enhanced ML Model Training")
    print("=" * 60)
    
    # Get training data
    training_data = create_enhanced_training_data()
    
    # Train each channel
    for channel, data in training_data.items():
        print(f"\n📊 Training {channel.upper()} model...")
        print("-" * 40)
        
        # Combine fraudulent and legitimate data
        all_training_data = data['fraudulent'] + data['legitimate']
        
        print(f"📈 Training samples: {len(all_training_data)}")
        print(f"   - Fraudulent: {len(data['fraudulent'])}")
        print(f"   - Legitimate: {len(data['legitimate'])}")
        
        # Train the model
        try:
            response = requests.post(
                f"{BASE_URL}/api/ai/train",
                json={
                    'channel': channel,
                    'training_data': all_training_data
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {channel} model trained successfully!")
                print(f"   Performance: {result.get('performance', {})}")
            else:
                print(f"❌ Failed to train {channel} model: {response.text}")
                
        except Exception as e:
            print(f"❌ Error training {channel} model: {e}")
        
        time.sleep(1)  # Brief pause between training
    
    print("\n" + "=" * 60)
    print("💾 Saving trained models...")
    
    # Save all trained models
    try:
        response = requests.post(f"{BASE_URL}/api/ai/save")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Models saved successfully!")
            print(f"   Filepath: {result.get('filepath', 'Unknown')}")
        else:
            print(f"❌ Failed to save models: {response.text}")
            
    except Exception as e:
        print(f"❌ Error saving models: {e}")
    
    print("\n" + "=" * 60)
    print("📊 Final AI System Status:")
    
    # Check final status
    try:
        response = requests.get(f"{BASE_URL}/api/ai/status")
        
        if response.status_code == 200:
            status = response.json()
            print(f"   Active System: {status.get('active_ai_system', 'Unknown')}")
            print(f"   Trained Models: {status.get('trained_models', [])}")
            print(f"   Performance: {status.get('performance', {})}")
        else:
            print(f"❌ Failed to get status: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")
    
    print("\n🎉 Enhanced Training Complete!")
    print("The ML models are now trained with more diverse data and should provide better predictions.")

if __name__ == "__main__":
    train_enhanced_models() 