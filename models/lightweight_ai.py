"""
Lightweight AI system using minimal Hugging Face models
Optimized for Railway deployment with small footprint
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class LightweightAI:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False
        
    def extract_features(self, text):
        """Extract basic text features without heavy ML models"""
        if not text:
            return {}
        
        features = {}
        
        # Basic text statistics
        features['length'] = len(text)
        features['word_count'] = len(text.split())
        features['char_count'] = len(text.replace(' ', ''))
        
        # Suspicious patterns
        suspicious_patterns = [
            r'urgent|emergency|immediate|asap',
            r'bank|account|password|login|verify',
            r'lottery|winner|prize|claim|money',
            r'bitcoin|crypto|wallet|investment',
            r'click|link|website|url',
            r'limited|offer|expire|soon',
            r'free|gift|bonus|reward',
            r'personal|information|social|security',
            r'payment|credit|card|banking',
            r'verify|confirm|update|secure'
        ]
        
        text_lower = text.lower()
        for pattern in suspicious_patterns:
            matches = len(re.findall(pattern, text_lower))
            features[f'pattern_{pattern.split("|")[0]}'] = matches
        
        # Email-specific features
        if '@' in text:
            features['has_email'] = 1
            features['email_count'] = len(re.findall(r'\S+@\S+', text))
        else:
            features['has_email'] = 0
            features['email_count'] = 0
        
        # URL features
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        features['url_count'] = len(re.findall(url_pattern, text))
        
        # Sentiment indicators
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disaster', 'problem']
        
        features['positive_words'] = sum(1 for word in positive_words if word in text_lower)
        features['negative_words'] = sum(1 for word in negative_words if word in text_lower)
        
        return features
    
    def calculate_risk_score(self, features):
        """Calculate risk score based on extracted features"""
        risk_score = 0
        
        # Length-based risk
        if features.get('length', 0) > 1000:
            risk_score += 10
        elif features.get('length', 0) < 50:
            risk_score += 15
        
        # Pattern-based risk
        pattern_weights = {
            'pattern_urgent': 20,
            'pattern_bank': 25,
            'pattern_lottery': 30,
            'pattern_bitcoin': 25,
            'pattern_click': 15,
            'pattern_limited': 10,
            'pattern_free': 15,
            'pattern_personal': 20,
            'pattern_payment': 25,
            'pattern_verify': 20
        }
        
        for pattern, weight in pattern_weights.items():
            if features.get(pattern, 0) > 0:
                risk_score += weight * features[pattern]
        
        # Email and URL risk
        if features.get('email_count', 0) > 2:
            risk_score += 20
        if features.get('url_count', 0) > 3:
            risk_score += 25
        
        # Sentiment risk
        if features.get('negative_words', 0) > features.get('positive_words', 0):
            risk_score += 10
        
        # Normalize to 0-100 scale
        risk_score = min(100, max(0, risk_score))
        
        return risk_score
    
    def analyze_email(self, email_content):
        """Analyze email for fraud indicators"""
        features = self.extract_features(email_content)
        risk_score = self.calculate_risk_score(features)
        # Ensure risk_score is always a float and not NaN
        try:
            risk_score = float(risk_score)
            if not np.isfinite(risk_score):
                risk_score = 0.0
        except Exception:
            risk_score = 0.0
        print(f"[DEBUG] Email risk_score: {risk_score}")
        # Determine risk level
        if risk_score >= 70:
            risk_level = "HIGH"
            recommendation = "Block immediately - multiple fraud indicators detected"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
            recommendation = "Review carefully - suspicious patterns detected"
        else:
            risk_level = "LOW"
            recommendation = "Appears safe - minimal risk indicators"
        # Generate detailed analysis
        analysis = {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'features': features,
            'indicators': []
        }
        # Add specific indicators
        if features.get('pattern_urgent', 0) > 0:
            analysis['indicators'].append("Urgency indicators detected")
        if features.get('pattern_bank', 0) > 0:
            analysis['indicators'].append("Banking-related keywords found")
        if features.get('pattern_lottery', 0) > 0:
            analysis['indicators'].append("Lottery/prize scam indicators")
        if features.get('email_count', 0) > 2:
            analysis['indicators'].append("Multiple email addresses detected")
        if features.get('url_count', 0) > 3:
            analysis['indicators'].append("Suspicious number of URLs")
        print(f"[DEBUG] Email analysis result: {analysis}")
        return analysis
    
    def analyze_transaction(self, transaction_data):
        """Analyze transaction for fraud indicators"""
        # Extract transaction features
        amount = transaction_data.get('amount', 0)
        location = transaction_data.get('location', '')
        merchant = transaction_data.get('merchant', '')
        time = transaction_data.get('time', '')
        
        risk_score = 0
        indicators = []
        
        # Amount-based analysis
        if amount > 1000:
            risk_score += 20
            indicators.append("High transaction amount")
        elif amount < 1:
            risk_score += 10
            indicators.append("Suspiciously low amount")
        
        # Location analysis
        if location and len(location) < 3:
            risk_score += 15
            indicators.append("Vague location information")
        
        # Merchant analysis
        if merchant and len(merchant) < 5:
            risk_score += 15
            indicators.append("Suspicious merchant name")
        
        # Time analysis (if provided)
        if time:
            # Simple time-based logic could be added here
            pass
        
        # Normalize risk score
        risk_score = min(100, max(0, risk_score))
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "HIGH"
            recommendation = "Review transaction - multiple risk factors"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            recommendation = "Monitor transaction - some risk factors"
        else:
            risk_level = "LOW"
            recommendation = "Transaction appears normal"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'indicators': indicators,
            'amount': amount,
            'location': location,
            'merchant': merchant
        }
    
    def analyze_social_media(self, post_content):
        """Analyze social media post for fraud indicators"""
        features = self.extract_features(post_content)
        risk_score = self.calculate_risk_score(features)
        
        # Social media specific adjustments
        if features.get('url_count', 0) > 2:
            risk_score += 10
        
        if features.get('pattern_free', 0) > 0:
            risk_score += 15
        
        # Normalize risk score
        risk_score = min(100, max(0, risk_score))
        
        # Determine risk level
        if risk_score >= 65:
            risk_level = "HIGH"
            recommendation = "Flag for review - suspicious social media activity"
        elif risk_score >= 35:
            risk_level = "MEDIUM"
            recommendation = "Monitor account - some suspicious indicators"
        else:
            risk_level = "LOW"
            recommendation = "Normal social media activity"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'features': features,
            'indicators': []
        } 