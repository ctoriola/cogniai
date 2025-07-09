from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import re
import random
import os
import json
import hashlib
import math
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

# Import advanced AI system
try:
    from models.advanced_ai import AdvancedAISystem
    ADVANCED_AI_AVAILABLE = True
    print("🤖 Advanced AI system loaded successfully")
except ImportError as e:
    ADVANCED_AI_AVAILABLE = False
    print(f"⚠️ Advanced AI not available: {e}")
    raise RuntimeError("Advanced AI system is required but not available.")

app = Flask(__name__)
CORS(app)

# ============================================================================
# MULTI-MODAL DATA INGESTION LAYER
# ============================================================================

class MultiModalDataIngestion:
    """Handles diverse input channels and data sources"""
    
    def __init__(self):
        self.channels = {
            'email': self._process_email,
            'webpage': self._process_webpage,
            'social_media': self._process_social_media,
            'transaction': self._process_transaction
        }
        
        # Threat patterns for different channels
        self.threat_patterns = {
            'email': {
                'urgent_language': r'\b(urgent|immediate|now|quick|fast|hurry)\b',
                'financial_terms': r'\b(account|password|verify|confirm|secure|bank|credit)\b',
                'threats': r'\b(suspended|blocked|terminated|legal|police|court)\b',
                'rewards': r'\b(prize|winner|selected|exclusive|limited|offer)\b',
                'suspicious_domains': r'\b(bit\.ly|tinyurl|goo\.gl|is\.gd|t\.co)\b'
            },
            'webpage': {
                'phishing_indicators': r'\b(login|signin|verify|secure|banking|account)\b',
                'fake_ssl': r'http://(?!localhost)',
                'suspicious_forms': r'<form[^>]*action=["\'](?!https?://)'
            },
            'social_media': {
                'fake_profiles': r'\b(follow|like|share|win|free|prize)\b',
                'suspicious_links': r'https?://[^\s<>"]+',
                'spam_patterns': r'\b(buy|sell|investment|crypto|bitcoin|earn)\b'
            },
            'messaging': {
                'urgent_requests': r'\b(help|urgent|emergency|money|transfer)\b',
                'suspicious_links': r'https?://[^\s<>"]+',
                'unknown_sender': r'unknown|unverified|new'
            },
            'voice_call': {
                'suspicious_requests': r'\b(verify|confirm|account|password|urgent)\b',
                'emotional_manipulation': r'\b(family|emergency|help|money|transfer)\b'
            }
        }
    
    def _process_email(self, data):
        """Process email data for phishing detection"""
        content = data.get('content', '').lower()
        sender = data.get('sender', '')
        subject = data.get('subject', '')
        
        # Extract features
        features = {
            'content_length': len(content),
            'sender_suspicious': self._check_suspicious_sender(sender),
            'subject_suspicious': self._check_suspicious_subject(subject),
            'pattern_matches': self._count_pattern_matches(content, 'email'),
            'url_count': len(re.findall(r'https?://[^\s<>"]+', content)),
            'suspicious_urls': self._analyze_urls(content),
            'sentiment_score': self._analyze_sentiment(content)
        }
        
        return {
            'channel': 'email',
            'features': features,
            'raw_data': data
        }
    
    def _process_webpage(self, data):
        """Process webpage data for phishing detection"""
        url = data.get('url', '')
        content = data.get('content', '')
        
        features = {
            'domain_suspicious': self._check_suspicious_domain(url),
            'ssl_secure': url.startswith('https://'),
            'phishing_indicators': self._count_pattern_matches(content, 'webpage'),
            'form_count': len(re.findall(r'<form', content)),
            'external_links': len(re.findall(r'href=["\'](?!https?://[^/]*' + re.escape(url.split('/')[2]) + ')', content)) if url else 0
        }
        
        return {
            'channel': 'webpage',
            'features': features,
            'raw_data': data
        }
    
    def _process_social_media(self, data):
        """Process social media data for scam detection"""
        content = data.get('content', '')
        profile = data.get('profile', {})
        links = data.get('links', [])
        
        features = {
            'profile_suspicious': self._check_suspicious_profile(profile),
            'spam_patterns': self._count_pattern_matches(content, 'social_media'),
            'suspicious_links': len([l for l in links if self._is_suspicious_link(l)]),
            'engagement_suspicious': self._check_suspicious_engagement(data.get('engagement', {})),
            'content_length': len(content)
        }
        
        return {
            'channel': 'social_media',
            'features': features,
            'raw_data': data
        }
    

    
    def _process_transaction(self, data):
        """Process transactional data for fraud detection"""
        amount = float(data.get('amount', 0))
        location = data.get('location', {})
        timestamp = data.get('timestamp', '')
        user_id = data.get('user_id', '')
        
        features = {
            'amount_suspicious': amount > 10000 or amount < 0,
            'location_suspicious': self._check_suspicious_location(location),
            'time_suspicious': self._is_suspicious_time(timestamp),
            'user_behavior_anomaly': self._check_user_behavior_anomaly(user_id, data),
            'transaction_frequency': self._get_transaction_frequency(user_id),
            'amount_deviation': self._get_amount_deviation(user_id, amount)
        }
        
        return {
            'channel': 'transaction',
            'features': features,
            'raw_data': data
        }
    

    
    # Helper methods for feature extraction
    def _check_suspicious_sender(self, sender):
        return any(pattern in sender.lower() for pattern in ['noreply', 'support', 'security', 'verify'])
    
    def _check_suspicious_subject(self, subject):
        return any(pattern in subject.lower() for pattern in ['urgent', 'verify', 'suspended', 'account'])
    
    def _count_pattern_matches(self, content, channel):
        patterns = self.threat_patterns.get(channel, {})
        total_matches = 0
        for pattern_name, pattern in patterns.items():
            total_matches += len(re.findall(pattern, content, re.IGNORECASE))
        return total_matches
    
    def _analyze_urls(self, content):
        urls = re.findall(r'https?://[^\s<>"]+', content)
        suspicious_urls = []
        for url in urls:
            if any(suspicious in url.lower() for suspicious in ['bit.ly', 'tinyurl', 'goo.gl']):
                suspicious_urls.append(url)
        return suspicious_urls
    
    def _analyze_sentiment(self, content):
        negative_words = ['urgent', 'suspended', 'blocked', 'terminated', 'legal', 'police']
        negative_count = sum(1 for word in negative_words if word in content.lower())
        return negative_count / len(negative_words) if negative_words else 0
    
    def _check_suspicious_domain(self, url):
        suspicious_domains = ['free', 'win', 'prize', 'claim', 'verify']
        return any(domain in url.lower() for domain in suspicious_domains)
    
    def _is_suspicious_script(self, script):
        return any(suspicious in script.lower() for suspicious in ['eval', 'document.write', 'innerHTML'])
    
    def _check_suspicious_profile(self, profile):
        return profile.get('followers', 0) < 10 or profile.get('verified', False) == False
    
    def _is_suspicious_link(self, link):
        return any(suspicious in link.lower() for suspicious in ['bit.ly', 'tinyurl', 'goo.gl'])
    
    def _check_suspicious_engagement(self, engagement):
        return engagement.get('likes', 0) > 1000 and engagement.get('comments', 0) < 5
    
    def _is_unknown_sender(self, sender):
        return sender.get('verified', False) == False or sender.get('mutual_contacts', 0) == 0
    
    def _is_suspicious_time(self, timestamp):
        if not timestamp:
            return False
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.hour < 6 or dt.hour > 23
        except Exception:
            return False
    
    def _check_suspicious_content(self, content):
        return len(content) < 10 or len(content) > 1000
    
    def _check_suspicious_caller(self, caller_id):
        return caller_id.startswith('+1') and len(caller_id) > 15
    
    def _detect_emotional_manipulation(self, transcript):
        emotional_words = ['family', 'emergency', 'help', 'urgent', 'crisis']
        return sum(1 for word in emotional_words if word in transcript.lower())
    
    def _count_urgent_requests(self, transcript):
        urgent_words = ['now', 'immediate', 'urgent', 'quick', 'fast']
        return sum(1 for word in urgent_words if word in transcript.lower())
    
    def _check_suspicious_location(self, location):
        return location.get('distance_from_home', 0) > 1000
    
    def _check_user_behavior_anomaly(self, user_id, data):
        # Simulate user behavior analysis
        return random.random() > 0.8
    
    def _get_transaction_frequency(self, user_id):
        # Simulate transaction frequency analysis
        return random.randint(1, 20)
    
    def _get_amount_deviation(self, user_id, amount):
        # Simulate amount deviation analysis
        return abs(amount - 1000) / 1000
    
    def _detect_login_anomaly(self, login_patterns):
        return login_patterns.get('unusual_time', False) or login_patterns.get('new_device', False)
    
    def _check_suspicious_activity(self, account_activity):
        return account_activity.get('suspicious_actions', 0) > 5
    
    def _detect_interaction_anomaly(self, interaction_patterns):
        return interaction_patterns.get('unusual_pattern', False)
    
    def _check_suspicious_session(self, session):
        return session.get('duration', 0) > 3600 or session.get('ip_changed', False)

# ============================================================================
# AI/ML CORE WITH ADVANCED MODELS
# ============================================================================

class AICore:
    """Advanced AI/ML core with multi-modal learning and deep learning capabilities"""
    
    def __init__(self):
        if ADVANCED_AI_AVAILABLE:
            self.advanced_ai = AdvancedAISystem()
            print("🧠 Advanced AI/ML system initialized (ML/DL/NLP)")
        else:
            raise RuntimeError("Advanced AI system is required.")
        
        self.models = {
            'email_classifier': self._email_fraud_classifier,
            'web_phishing_detector': self._web_phishing_detector,
            'social_media_scam_detector': self._social_media_scam_detector,
            'messaging_fraud_detector': self._messaging_fraud_detector,
            'voice_call_scam_detector': self._voice_call_scam_detector,
            'transaction_anomaly_detector': self._transaction_anomaly_detector,
            'user_behavior_analyzer': self._user_behavior_analyzer
        }
        
        # Threat intelligence database (simulated)
        self.threat_intelligence = {
            'known_phishing_domains': ['fake-bank.com', 'verify-account.net', 'secure-login.org'],
            'suspicious_patterns': ['urgent', 'verify', 'suspended', 'account', 'password'],
            'fraud_indicators': ['high_value', 'unusual_time', 'unknown_sender', 'suspicious_location']
        }
    
    def _email_fraud_classifier(self, features):
        """Advanced email fraud classification using ML/DL/NLP"""
        if self.advanced_ai:
            # Use advanced AI system
            try:
                # Extract advanced features
                advanced_features = self.advanced_ai.extract_features({
                    'content': features.get('content', ''),
                    'sender': features.get('sender', ''),
                    'subject': features.get('subject', '')
                }, 'email')
                
                # Predict using ML model
                risk_score = self.advanced_ai.predict_risk(advanced_features, 'email')
                return min(max(risk_score, 0.0), 1.0)
            except Exception as e:
                print(f"Advanced AI error: {e}, falling back to rule-based")
        
        # Fallback to rule-based system
        risk_score = 0
        
        # Ensure all features exist with defaults
        pattern_matches = features.get('pattern_matches', 0)
        suspicious_urls = features.get('suspicious_urls', [])
        sentiment_score = features.get('sentiment_score', 0.0)
        sender_suspicious = features.get('sender_suspicious', False)
        subject_suspicious = features.get('subject_suspicious', False)
        
        # Pattern-based scoring
        risk_score += pattern_matches * 0.15
        risk_score += len(suspicious_urls) * 0.2
        risk_score += sentiment_score * 0.1
        
        # Sender analysis
        if sender_suspicious:
            risk_score += 0.3
        
        # Subject analysis
        if subject_suspicious:
            risk_score += 0.2
        
        return min(max(risk_score, 0.0), 1.0)
    
    def _web_phishing_detector(self, features):
        """Web page phishing detection"""
        risk_score = 0
        
        if not features['ssl_secure']:
            risk_score += 0.4
        
        risk_score += features['phishing_indicators'] * 0.15
        risk_score += features['suspicious_scripts'] * 0.2
        risk_score += features['external_links'] * 0.1
        
        if features['domain_suspicious']:
            risk_score += 0.3
        
        return min(risk_score, 1.0)
    
    def _social_media_scam_detector(self, features):
        """Social media scam detection"""
        risk_score = 0
        
        if features['profile_suspicious']:
            risk_score += 0.3
        
        risk_score += features['spam_patterns'] * 0.15
        risk_score += features['suspicious_links'] * 0.2
        
        if features['engagement_suspicious']:
            risk_score += 0.25
        
        return min(risk_score, 1.0)
    
    def _messaging_fraud_detector(self, features):
        """Messaging fraud detection"""
        risk_score = 0
        
        if features['sender_unknown']:
            risk_score += 0.3
        
        risk_score += features['urgent_patterns'] * 0.15
        risk_score += features['suspicious_links'] * 0.2
        
        if features['time_suspicious']:
            risk_score += 0.2
        
        if features['content_suspicious']:
            risk_score += 0.15
        
        return min(risk_score, 1.0)
    
    def _voice_call_scam_detector(self, features):
        """Voice call scam detection"""
        risk_score = 0
        
        if features['caller_suspicious']:
            risk_score += 0.3
        
        risk_score += features['suspicious_patterns'] * 0.15
        risk_score += features['emotional_manipulation'] * 0.1
        risk_score += features['urgent_requests'] * 0.15
        
        if features['call_duration_suspicious']:
            risk_score += 0.2
        
        return min(risk_score, 1.0)
    
    def _transaction_anomaly_detector(self, features):
        """Transaction anomaly detection using ML"""
        if self.advanced_ai:
            # Use advanced AI system
            try:
                # Extract advanced features
                advanced_features = self.advanced_ai.extract_features({
                    'amount': features.get('amount', 0),
                    'location': features.get('location', {}),
                    'timestamp': features.get('timestamp', ''),
                    'user_id': features.get('user_id', '')
                }, 'transaction')
                
                # Predict using ML model
                risk_score = self.advanced_ai.predict_risk(advanced_features, 'transaction')
                return min(max(risk_score, 0.0), 1.0)
            except Exception as e:
                print(f"Advanced AI error: {e}, falling back to rule-based")
        
        # Fallback to rule-based system
        risk_score = 0
        
        if features['amount_suspicious']:
            risk_score += 0.4
        
        if features['location_suspicious']:
            risk_score += 0.3
        
        if features['time_suspicious']:
            risk_score += 0.2
        
        if features['user_behavior_anomaly']:
            risk_score += 0.3
        
        # Frequency analysis
        if features['transaction_frequency'] > 10:
            risk_score += 0.2
        
        # Amount deviation
        if features['amount_deviation'] > 2:
            risk_score += 0.25
        
        return min(risk_score, 1.0)
    
    def _user_behavior_analyzer(self, features):
        """User behavior analysis"""
        risk_score = 0
        
        if features['login_anomaly']:
            risk_score += 0.3
        
        if features['activity_suspicious']:
            risk_score += 0.25
        
        if features['interaction_anomaly']:
            risk_score += 0.2
        
        if features['session_suspicious']:
            risk_score += 0.25
        
        return min(risk_score, 1.0)
    
    def _multi_modal_fusion(self, channel_results):
        """Multi-modal fusion for holistic understanding"""
        # Weighted fusion of different channel results
        weights = {
            'email': 0.35,
            'webpage': 0.25,
            'social_media': 0.2,
            'transaction': 0.2
        }
        
        fused_score = 0
        for channel, result in channel_results.items():
            if channel in weights:
                fused_score += result['risk_score'] * weights[channel]
        
        return min(fused_score, 1.0)

# ============================================================================
# REAL-TIME PROCESSING ENGINE
# ============================================================================

class RealTimeProcessingEngine:
    """Real-time processing engine for immediate threat detection"""
    
    def __init__(self):
        self.data_ingestion = MultiModalDataIngestion()
        self.ai_core = AICore()
        self.alerts = []
        self.stats = defaultdict(int)
        self.user_profiles = defaultdict(dict)
    
    def process_data(self, channel, data):
        """Process data from any channel in real-time"""
        try:
            # 1. Data Ingestion
            processed_data = self.data_ingestion.channels[channel](data)
            
            # 2. AI/ML Analysis using Advanced AI System
            if self.ai_core.advanced_ai:
                print(f"[DEBUG] Using advanced AI system for {channel}")
                # Use advanced AI system directly
                try:
                    # Extract features using advanced AI
                    advanced_features = self.ai_core.advanced_ai.extract_features(data, channel)
                    print(f"[DEBUG] Advanced features extracted for {channel}")
                    
                    # Predict risk using ML models
                    risk_score = self.ai_core.advanced_ai.predict_risk(advanced_features, channel)
                    print(f"[DEBUG] Advanced AI risk score for {channel}: {risk_score}")
                    
                    # Ensure risk_score is a valid number
                    if not isinstance(risk_score, (int, float)) or math.isnan(risk_score):
                        risk_score = 0.0
                        print(f"[DEBUG] Invalid risk score, set to 0.0")
                    
                except Exception as e:
                    print(f"[DEBUG] Advanced AI error for {channel}: {e}")
                    # Fallback to old system
                    model_mapping = {
                        'email': 'email_classifier',
                        'webpage': 'web_phishing_detector',
                        'social_media': 'social_media_scam_detector',
                        'transaction': 'transaction_anomaly_detector'
                    }
                    model_name = model_mapping.get(channel, 'email_classifier')
                    risk_score = self.ai_core.models[model_name](processed_data['features'])
                    print(f"[DEBUG] Fallback risk score for {channel}: {risk_score}")
                    
                    if not isinstance(risk_score, (int, float)) or math.isnan(risk_score):
                        risk_score = 0.0
            else:
                print(f"[DEBUG] No advanced AI, using fallback for {channel}")
                # Fallback to old system
                model_mapping = {
                    'email': 'email_classifier',
                    'webpage': 'web_phishing_detector',
                    'social_media': 'social_media_scam_detector',
                    'transaction': 'transaction_anomaly_detector'
                }
                model_name = model_mapping.get(channel, 'email_classifier')
                risk_score = self.ai_core.models[model_name](processed_data['features'])
                print(f"[DEBUG] Fallback risk score for {channel}: {risk_score}")
                
                if not isinstance(risk_score, (int, float)) or math.isnan(risk_score):
                    risk_score = 0.0
            
            # 3. Threat Assessment
            threat_level = self._assess_threat_level(risk_score, processed_data['features'])
            
            # 4. Alert Generation
            alert = self._generate_alert(channel, processed_data, risk_score, threat_level)
            
            # 5. Update Statistics
            self._update_stats(channel, risk_score, threat_level)
            
            # 6. Update User Profile
            self._update_user_profile(data.get('user_id', 'unknown'), channel, processed_data)
            
            return {
                'channel': channel,
                'risk_score': risk_score,
                'threat_level': threat_level,
                'alert': alert,
                'features': processed_data['features'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'channel': channel,
                'timestamp': datetime.now().isoformat()
            }
    
    def _assess_threat_level(self, risk_score, features):
        """Assess threat level based on risk score and features"""
        if risk_score > 0.8:
            return 'CRITICAL'
        elif risk_score > 0.6:
            return 'HIGH'
        elif risk_score > 0.4:
            return 'MEDIUM'
        elif risk_score > 0.2:
            return 'LOW'
        else:
            return 'SAFE'
    
    def _generate_alert(self, channel, processed_data, risk_score, threat_level):
        """Generate detailed alert with actionable information"""
        alert = {
            'id': hashlib.md5(f"{channel}_{datetime.now()}".encode()).hexdigest()[:8],
            'channel': channel,
            'threat_level': threat_level,
            'risk_score': risk_score,
            'timestamp': datetime.now().isoformat(),
            'description': self._generate_alert_description(channel, processed_data, risk_score),
            'recommendations': self._generate_recommendations(channel, threat_level),
            'features': processed_data['features']
        }
        
        self.alerts.append(alert)
        return alert
    
    def _generate_alert_description(self, channel, processed_data, risk_score):
        """Generate human-readable alert description"""
        descriptions = {
            'email': f"Phishing attempt detected with {risk_score:.1%} confidence",
            'webpage': f"Phishing website detected with {risk_score:.1%} confidence",
            'social_media': f"Social media scam detected with {risk_score:.1%} confidence",
            'transaction': f"Fraudulent transaction detected with {risk_score:.1%} confidence"
        }
        return descriptions.get(channel, f"Suspicious activity detected in {channel}")
    
    def _generate_recommendations(self, channel, threat_level):
        """Generate actionable recommendations"""
        recommendations = {
            'CRITICAL': [
                "Immediate action required",
                "Block the source",
                "Report to authorities",
                "Freeze affected accounts"
            ],
            'HIGH': [
                "Investigate immediately",
                "Monitor closely",
                "Update security settings",
                "Enable additional verification"
            ],
            'MEDIUM': [
                "Review activity",
                "Enable alerts",
                "Monitor for patterns",
                "Update passwords"
            ],
            'LOW': [
                "Monitor for escalation",
                "Review security settings",
                "Stay vigilant"
            ]
        }
        return recommendations.get(threat_level, ["Monitor the situation"])
    
    def _update_stats(self, channel, risk_score, threat_level):
        """Update real-time statistics"""
        self.stats[f'{channel}_alerts'] += 1
        self.stats['total_alerts'] += 1
        
        if threat_level in ['CRITICAL', 'HIGH']:
            self.stats['high_risk_alerts'] += 1
    
    def _update_user_profile(self, user_id, channel, processed_data):
        """Update user behavior profile for anomaly detection"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = defaultdict(list)
        
        self.user_profiles[user_id][channel].append({
            'timestamp': datetime.now().isoformat(),
            'features': processed_data['features']
        })

# ============================================================================
# FLASK ROUTES
# ============================================================================

# Initialize the processing engine
processing_engine = RealTimeProcessingEngine()

# Auto-load trained models on server start
if ADVANCED_AI_AVAILABLE:
    try:
        processing_engine.ai_core.advanced_ai.load_models('models/trained_models.pkl')
        print("✅ Trained models loaded on server start.")
    except Exception as e:
        print(f"⚠️ Could not load trained models on server start: {e}")

@app.route('/')
def home():
    """Home page with system overview"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Omni-Channel AI Scam & Fraud Detection Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
            .btn { background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; margin: 10px; }
            .btn:hover { background: #45a049; }
            h1 { text-align: center; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 Omni-Channel AI Scam & Fraud Detection Platform</h1>
            
            <div class="card">
                <h2>🎯 System Overview</h2>
                <p>Advanced AI-powered platform that analyzes multiple channels for fraud detection:</p>
                <ul>
                    <li>📧 Email Phishing Detection</li>
                    <li>🌐 Web Page Analysis</li>
                    <li>📱 Social Media Monitoring</li>
                    <li>💬 Messaging App Analysis</li>
                    <li>📞 Voice Call Analysis</li>
                    <li>💳 Transaction Monitoring</li>
                    <li>👤 User Behavior Analysis</li>
                </ul>
            </div>
            
            <div class="feature-grid">
                <div class="card">
                    <h3>🔍 Multi-Modal Analysis</h3>
                    <p>Advanced AI models analyze data across multiple channels simultaneously for comprehensive threat detection.</p>
                    <a href="/dashboard" class="btn">📊 Dashboard</a>
                </div>
                
                <div class="card">
                    <h3>⚡ Real-Time Processing</h3>
                    <p>Instant threat detection and alerting with sub-second response times.</p>
                    <a href="/api/dashboard/stats" class="btn">📈 Statistics</a>
                </div>
                
                <div class="card">
                    <h3>🧠 AI/ML Core</h3>
                    <p>Deep learning models with transformer architecture for nuanced fraud detection.</p>
                    <a href="/test" class="btn">🧪 Test API</a>
                </div>
            </div>
            
            <div class="card">
                <h3>📡 API Endpoints</h3>
                <ul>
                    <li><strong>POST /analyze/email</strong> - Email phishing detection</li>
                    <li><strong>POST /analyze/web_page</strong> - Web page analysis</li>
                    <li><strong>POST /analyze/social_media</strong> - Social media monitoring</li>
                    <li><strong>POST /analyze/messaging</strong> - Messaging app analysis</li>
                    <li><strong>POST /analyze/voice_call</strong> - Voice call analysis</li>
                    <li><strong>POST /analyze/transaction</strong> - Transaction monitoring</li>
                    <li><strong>POST /analyze/user_behavior</strong> - User behavior analysis</li>
                    <li><strong>GET /api/dashboard/stats</strong> - Real-time statistics</li>
                    <li><strong>GET /api/dashboard/alerts</strong> - Recent alerts</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard HTML"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Dashboard file not found", 404

# Multi-channel analysis endpoints
@app.route('/analyze/email', methods=['POST'])
def analyze_email():
    """Analyze email for phishing"""
    data = request.json
    result = processing_engine.process_data('email', data)
    return jsonify(result)

@app.route('/analyze/webpage', methods=['POST'])
def analyze_webpage():
    """Analyze webpage for phishing"""
    data = request.json
    result = processing_engine.process_data('webpage', data)
    return jsonify(result)

@app.route('/analyze/social_media', methods=['POST'])
def analyze_social_media():
    """Analyze social media for scams"""
    data = request.json
    result = processing_engine.process_data('social_media', data)
    return jsonify(result)

@app.route('/analyze/transaction', methods=['POST'])
def analyze_transaction():
    """Analyze transaction for fraud"""
    data = request.json
    result = processing_engine.process_data('transaction', data)
    return jsonify(result)

# Multi-modal fusion endpoint
@app.route('/analyze/multi_modal', methods=['POST'])
def analyze_multi_modal():
    """Analyze data from multiple channels simultaneously"""
    data = request.json
    channels = data.get('channels', [])
    channel_data = data.get('data', {})
    
    results = {}
    for channel in channels:
        if channel in channel_data:
            results[channel] = processing_engine.process_data(channel, channel_data[channel])
    
    # Multi-modal fusion
    if results:
        fused_score = processing_engine.ai_core._multi_modal_fusion(results)
        return jsonify({
            'channel_results': results,
            'fused_risk_score': fused_score,
            'overall_threat_level': processing_engine._assess_threat_level(fused_score, {}),
            'timestamp': datetime.now().isoformat()
        })
    
    return jsonify({'error': 'No valid channels provided'})

# Dashboard endpoints
@app.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    """Get real-time statistics"""
    return jsonify(dict(processing_engine.stats))

@app.route('/api/dashboard/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    return jsonify(processing_engine.alerts[-20:])  # Last 20 alerts

@app.route('/api/dashboard/trend', methods=['GET'])
def get_trend():
    """Get risk trend data"""
    trend_data = []
    for i in range(24):
        hour = datetime.now() - timedelta(hours=23-i)
        trend_data.append({
            'time': hour.strftime('%H:00'),
            'email_risk': random.uniform(0.1, 0.8),
            'web_risk': random.uniform(0.2, 0.9),
            'social_risk': random.uniform(0.1, 0.7),
            'transaction_risk': random.uniform(0.2, 0.9),
            'combined_risk': random.uniform(0.3, 0.95)
        })
    return jsonify(trend_data)

@app.route('/api/dashboard/distribution', methods=['GET'])
def get_distribution():
    """Get alert distribution by channel"""
    channel_stats = {}
    for key, value in processing_engine.stats.items():
        if key.endswith('_alerts'):
            channel = key.replace('_alerts', '')
            channel_stats[channel] = value
    
    return jsonify([
        {'name': channel.title(), 'value': count}
        for channel, count in channel_stats.items()
    ])

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'Omni-Channel AI Scam & Fraud Detection Platform is running!',
        'timestamp': datetime.now().isoformat(),
        'channels': list(processing_engine.data_ingestion.channels.keys()),
        'advanced_ai': ADVANCED_AI_AVAILABLE
    })

@app.route('/api/ai/status', methods=['GET'])
def get_ai_status():
    """Get AI system status"""
    # Determine which AI system is active
    ai_system = None
    if processing_engine.ai_core.advanced_ai:
        ai_system = 'advanced'
        performance = processing_engine.ai_core.advanced_ai.model_performance
        
        # Check if models are trained
        trained_models = []
        for channel, perf in performance.items():
            if perf.get('accuracy', 0) > 0:
                trained_models.append(channel)
        
        # Update status to show ML usage
        if trained_models:
            ai_system = 'advanced_ml'
        else:
            ai_system = 'advanced_ml_random'  # Using ML with random predictions
    else:
        ai_system = 'rule-based'
        performance = {}
    
    status = {
        'advanced_ai_available': ADVANCED_AI_AVAILABLE,
        'active_ai_system': ai_system,
        'models_loaded': 1 if processing_engine.ai_core.advanced_ai else 0,
        'trained_models': trained_models if 'trained_models' in locals() else [],
        'performance': performance
    }
    return jsonify(status)

@app.route('/api/ai/train', methods=['POST'])
def train_model():
    """Train AI model with new data"""
    if not ADVANCED_AI_AVAILABLE:
        return jsonify({'error': 'Advanced AI system not available'}), 400
    
    data = request.json
    channel = data.get('channel')
    training_data = data.get('training_data', [])
    
    if not channel or not training_data:
        return jsonify({'error': 'Missing channel or training data'}), 400
    
    try:
        # Use advanced AI
        processing_engine.ai_core.advanced_ai.train_model(channel, training_data)
        performance = processing_engine.ai_core.advanced_ai.model_performance.get(channel, {})
        
        return jsonify({
            'status': 'success',
            'message': f'Model {channel} trained successfully',
            'performance': performance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/save', methods=['POST'])
def save_models():
    """Save trained models"""
    if not ADVANCED_AI_AVAILABLE:
        return jsonify({'error': 'Advanced AI system not available'}), 400

    try:
        filepath = 'models/trained_models.pkl'
        os.makedirs('models', exist_ok=True)

        processing_engine.ai_core.advanced_ai.save_models(filepath)

        return jsonify({
            'status': 'success',
            'message': 'Models saved successfully',
            'filepath': filepath
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/load', methods=['POST'])
def load_models():
    """Load trained models"""
    if not ADVANCED_AI_AVAILABLE:
        return jsonify({'error': 'Advanced AI system not available'}), 400
    
    try:
        filepath = 'models/trained_models.pkl'
        
        processing_engine.ai_core.advanced_ai.load_models(filepath)
        performance = processing_engine.ai_core.advanced_ai.model_performance
        
        return jsonify({
            'status': 'success',
            'message': 'Models loaded successfully',
            'performance': performance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nlp/analyze', methods=['POST'])
def analyze_nlp():
    """Comprehensive NLP analysis endpoint"""
    if not ADVANCED_AI_AVAILABLE:
        return jsonify({'error': 'Advanced AI system not available'}), 400
    
    data = request.json
    text = data.get('text', '')
    analysis_type = data.get('type', 'comprehensive')  # comprehensive, fraud, readability
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Get advanced AI system
        ai_system = processing_engine.ai_core.advanced_ai
        
        # Perform comprehensive NLP analysis
        nlp_features = ai_system._extract_nlp_features(text)
        
        # Categorize features for better presentation
        analysis_result = {
            'text_statistics': {
                'text_length': nlp_features.get('text_length', 0),
                'word_count': nlp_features.get('word_count', 0),
                'sentence_count': nlp_features.get('sentence_count', 0),
                'avg_word_length': round(nlp_features.get('avg_word_length', 0), 2),
                'unique_words_ratio': round(nlp_features.get('unique_words_ratio', 0), 3)
            },
            'fraud_indicators': {
                'urgency_indicators': nlp_features.get('urgency_indicators', 0),
                'authority_indicators': nlp_features.get('authority_indicators', 0),
                'financial_pressure': nlp_features.get('financial_pressure', 0),
                'reward_indicators': nlp_features.get('reward_indicators', 0),
                'personal_info_requests': nlp_features.get('personal_info_requests', 0),
                'emotional_manipulation': nlp_features.get('emotional_manipulation', 0),
                'total_fraud_indicators': nlp_features.get('total_fraud_indicators', 0)
            },
            'linguistic_patterns': {
                'action_verb_count': nlp_features.get('action_verb_count', 0),
                'grammar_errors': nlp_features.get('grammar_errors', 0),
                'caps_ratio': round(nlp_features.get('caps_ratio', 0), 3),
                'exclamation_count': nlp_features.get('exclamation_count', 0),
                'question_count': nlp_features.get('question_count', 0)
            },
            'entity_recognition': {
                'organization_mentions': nlp_features.get('organization_mentions', 0),
                'government_mentions': nlp_features.get('government_mentions', 0),
                'financial_institution_mentions': nlp_features.get('financial_institution_mentions', 0),
                'personal_name_mentions': nlp_features.get('personal_name_mentions', 0),
                'total_entity_mentions': nlp_features.get('total_entity_mentions', 0)
            },
            'readability_metrics': {
                'avg_sentence_length': round(nlp_features.get('avg_sentence_length', 0), 2),
                'readability_score': round(nlp_features.get('readability_score', 0), 2),
                'complexity_score': round(nlp_features.get('complexity_score', 0), 2),
                'long_word_ratio': round(nlp_features.get('long_word_ratio', 0), 3)
            },
            'sentiment_analysis': {
                'compound': round(nlp_features.get('sentiment_compound', 0), 3),
                'positive': round(nlp_features.get('sentiment_positive', 0), 3),
                'negative': round(nlp_features.get('sentiment_negative', 0), 3),
                'neutral': round(nlp_features.get('sentiment_neutral', 0), 3)
            },
            'text_patterns': {
                'url_count': nlp_features.get('url_count', 0),
                'suspicious_url_count': nlp_features.get('suspicious_url_count', 0),
                'phone_patterns': nlp_features.get('phone_patterns', 0),
                'email_patterns': nlp_features.get('email_patterns', 0),
                'currency_patterns': nlp_features.get('currency_patterns', 0),
                'time_pressure_indicators': nlp_features.get('time_pressure_indicators', 0)
            },
            'risk_assessment': {
                'fraud_risk_score': min(100, nlp_features.get('total_fraud_indicators', 0) * 10),
                'urgency_risk': min(100, nlp_features.get('urgency_indicators', 0) * 20),
                'authority_risk': min(100, nlp_features.get('authority_indicators', 0) * 15),
                'emotional_risk': min(100, nlp_features.get('emotional_manipulation', 0) * 12),
                'overall_nlp_risk': min(100, nlp_features.get('total_fraud_indicators', 0) * 8)
            }
        }
        
        # Add risk level assessment
        overall_risk = analysis_result['risk_assessment']['overall_nlp_risk']
        if overall_risk >= 80:
            risk_level = 'CRITICAL'
        elif overall_risk >= 60:
            risk_level = 'HIGH'
        elif overall_risk >= 40:
            risk_level = 'MEDIUM'
        elif overall_risk >= 20:
            risk_level = 'LOW'
        else:
            risk_level = 'SAFE'
        
        analysis_result['risk_level'] = risk_level

        return jsonify({
            'status': 'success',
            'analysis_type': analysis_type,
            'text_preview': text[:200] + '...' if len(text) > 200 else text,
            'analysis': analysis_result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nlp/compare', methods=['POST'])
def compare_nlp():
    """Compare NLP analysis between multiple texts"""
    data = request.json
    texts = data.get('texts', [])
    
    if not texts or len(texts) < 2:
        return jsonify({'error': 'At least 2 texts required for comparison'}), 400
    
    try:
        ai_system = processing_engine.ai_core.advanced_ai
        comparisons = []
        
        for i, text in enumerate(texts):
            nlp_features = ai_system._extract_nlp_features(text)
            
            comparison = {
                'text_id': i + 1,
                'text_preview': text[:100] + '...' if len(text) > 100 else text,
                'fraud_indicators': nlp_features.get('total_fraud_indicators', 0),
                'urgency_score': nlp_features.get('urgency_indicators', 0),
                'sentiment': round(nlp_features.get('sentiment_compound', 0), 3),
                'readability': round(nlp_features.get('readability_score', 0), 2),
                'complexity': round(nlp_features.get('complexity_score', 0), 2),
                'risk_score': min(100, nlp_features.get('total_fraud_indicators', 0) * 10)
            }
            comparisons.append(comparison)
        
        # Sort by risk score (highest first)
        comparisons.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'comparisons': comparisons,
            'total_texts': len(texts),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚨 Starting Omni-Channel AI Scam & Fraud Detection Platform")
    print("📊 API: http://localhost:5000")
    print("🧪 Test: http://localhost:5000/test")
    print("📈 Dashboard: http://localhost:5000/dashboard")
    print("🌐 Home: http://localhost:5000/")
    print("📡 Multi-channel endpoints available")
    app.run(host='0.0.0.0', port=5000, debug=True)