"""
Lightweight AI system using minimal Hugging Face models
Optimized for Railway deployment with small footprint
"""

import re
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Only essential imports
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("❌ Transformers not available")

class LightweightAI:
    """Lightweight AI system using minimal Hugging Face models"""
    
    def __init__(self):
        self.pipelines = {}
        self.training_data = defaultdict(list)
        self.model_performance = {}
        
        # Initialize only essential models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize only essential models"""
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Transformers library is required")
            
        print("🤖 Initializing lightweight AI models...")
        
        try:
            # Only 2 essential models for fraud detection
            # 1. Sentiment analysis for detecting urgency/emotional manipulation
            self.pipelines['sentiment'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            print("✅ Sentiment analysis model loaded")
            
            # 2. Text classification for fraud detection
            self.pipelines['text_classification'] = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium"
            )
            print("✅ Text classification model loaded")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def extract_features(self, data: Dict[str, Any], channel: str) -> Dict[str, Any]:
        """Extract features using lightweight models"""
        features = {}
        
        if channel == 'email':
            features.update(self._extract_email_features(data))
        elif channel == 'transaction':
            features.update(self._extract_transaction_features(data))
        elif channel == 'social_media':
            features.update(self._extract_social_features(data))
        else:
            features.update(self._extract_generic_features(data))
            
        return features
    
    def _extract_email_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract email features using lightweight models"""
        content = data.get('content', '')
        subject = data.get('subject', '')
        sender = data.get('sender', '')
        
        features = {}
        
        # 1. Sentiment Analysis (lightweight)
        if 'sentiment' in self.pipelines and content:
            try:
                sentiment_result = self.pipelines['sentiment'](content[:512])
                features['sentiment_negative'] = 1.0 if sentiment_result[0]['label'] == 'negative' else 0.0
                features['sentiment_score'] = sentiment_result[0]['score']
            except:
                features['sentiment_negative'] = 0.5
                features['sentiment_score'] = 0.5
        
        # 2. Text Classification (lightweight)
        if 'text_classification' in self.pipelines and content:
            try:
                text_result = self.pipelines['text_classification'](content[:512])
                features['text_suspicious'] = text_result[0]['score']
            except:
                features['text_suspicious'] = 0.5
        
        # 3. Traditional features (no ML required)
        features.update({
            'urgency_score': self._calculate_urgency_score(content),
            'financial_terms': self._count_financial_terms(content),
            'threat_indicators': self._count_threat_indicators(content),
            'suspicious_sender': self._check_suspicious_sender(sender),
            'suspicious_subject': self._check_suspicious_subject(subject),
            'suspicious_urls': self._count_suspicious_urls(content),
            'content_length': len(content)
        })
        
        return features
    
    def _extract_transaction_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transaction features (no ML required)"""
        amount = float(data.get('amount', 0))
        location = data.get('location', {})
        timestamp = data.get('timestamp', '')
        description = data.get('description', '')
        
        features = {
            'high_amount': int(amount > 10000),
            'negative_amount': int(amount < 0),
            'foreign_location': int(location.get('distance_from_home', 0) > 1000),
            'unusual_time': self._is_unusual_time(timestamp),
            'large_distance': int(location.get('distance_from_home', 0) > 500),
            'amount_suspicious': amount > 10000 or amount < 0
        }
        
        # Analyze description if available
        if description and 'sentiment' in self.pipelines:
            try:
                desc_result = self.pipelines['sentiment'](description[:512])
                features['description_suspicious'] = 1.0 if desc_result[0]['label'] == 'negative' else 0.0
            except:
                features['description_suspicious'] = 0.5
        
        return features
    
    def _extract_social_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract social media features"""
        content = data.get('content', '')
        profile = data.get('profile', {})
        links = data.get('links', [])
        
        features = {
            'low_followers': int(profile.get('followers', 0) < 10),
            'unverified': int(not profile.get('verified', False)),
            'suspicious_links': len([l for l in links if self._is_suspicious_link(l)]),
            'spam_content': self._count_spam_indicators(content),
            'low_engagement': int(profile.get('engagement_rate', 1) < 0.01)
        }
        
        # Analyze content if available
        if content and 'sentiment' in self.pipelines:
            try:
                sentiment_result = self.pipelines['sentiment'](content[:512])
                features['content_suspicious'] = 1.0 if sentiment_result[0]['label'] == 'negative' else 0.0
            except:
                features['content_suspicious'] = 0.5
        
        return features
    
    def _extract_generic_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract generic features"""
        content = data.get('content', '')
        
        features = {
            'content_length': len(content),
            'suspicious_patterns': self._count_suspicious_patterns(content)
        }
        
        # Generic sentiment analysis
        if content and 'sentiment' in self.pipelines:
            try:
                sentiment_result = self.pipelines['sentiment'](content[:512])
                features['sentiment_score'] = 1.0 if sentiment_result[0]['label'] == 'negative' else 0.0
            except:
                features['sentiment_score'] = 0.5
        
        return features
    
    def predict_risk(self, features: Dict[str, Any], channel: str) -> float:
        """Predict risk using lightweight approach"""
        
        # Base risk from HF models
        hf_risk = 0.0
        hf_weight = 0.3  # Lower weight for HF models
        
        if channel == 'email':
            hf_risk = (
                features.get('sentiment_negative', 0.5) * 0.4 +
                features.get('text_suspicious', 0.5) * 0.6
            )
        elif channel == 'transaction':
            hf_risk = features.get('description_suspicious', 0.5)
        elif channel == 'social_media':
            hf_risk = features.get('content_suspicious', 0.5)
        else:
            hf_risk = features.get('sentiment_score', 0.5)
        
        # Traditional feature risk (higher weight)
        traditional_risk = self._calculate_traditional_risk(features, channel)
        
        # Combine with higher weight on traditional features
        final_risk = (hf_risk * hf_weight) + (traditional_risk * (1 - hf_weight))
        
        # Boost risk for obvious fraud indicators
        if channel == 'email':
            if features.get('suspicious_sender', 0) > 0:
                final_risk += 0.2
            if features.get('suspicious_subject', 0) > 0:
                final_risk += 0.15
            if features.get('suspicious_urls', 0) > 0:
                final_risk += 0.25
            if features.get('urgency_score', 0) > 0.3:
                final_risk += 0.2
                
        elif channel == 'transaction':
            if features.get('high_amount', 0) > 0:
                final_risk += 0.3
            if features.get('foreign_location', 0) > 0:
                final_risk += 0.25
                
        elif channel == 'social_media':
            if features.get('low_followers', 0) > 0:
                final_risk += 0.2
            if features.get('unverified', 0) > 0:
                final_risk += 0.15
            if features.get('suspicious_links', 0) > 0:
                final_risk += 0.3
        
        return min(max(final_risk, 0.0), 1.0)
    
    def _calculate_traditional_risk(self, features: Dict[str, Any], channel: str) -> float:
        """Calculate risk using traditional features"""
        if channel == 'email':
            weights = {
                'urgency_score': 0.2,
                'financial_terms': 0.15,
                'threat_indicators': 0.25,
                'suspicious_sender': 0.3,
                'suspicious_subject': 0.2,
                'suspicious_urls': 0.2
            }
        elif channel == 'transaction':
            weights = {
                'high_amount': 0.4,
                'negative_amount': 0.4,
                'foreign_location': 0.3,
                'unusual_time': 0.2,
                'large_distance': 0.25
            }
        elif channel == 'social_media':
            weights = {
                'low_followers': 0.3,
                'unverified': 0.2,
                'suspicious_links': 0.2,
                'spam_content': 0.25,
                'low_engagement': 0.15
            }
        else:
            weights = {'suspicious_patterns': 1.0}
        
        risk_score = 0.0
        for feature, weight in weights.items():
            if feature in features:
                risk_score += features[feature] * weight
        
        return min(max(risk_score, 0.0), 1.0)
    
    # Traditional feature extraction methods (no ML required)
    def _calculate_urgency_score(self, text: str) -> float:
        """Calculate urgency score"""
        urgency_words = ['urgent', 'immediate', 'now', 'quick', 'fast', 'hurry', 'asap']
        text_lower = text.lower()
        return sum(1 for word in urgency_words if word in text_lower) / len(urgency_words)
    
    def _count_financial_terms(self, text: str) -> int:
        """Count financial terms"""
        financial_words = ['account', 'password', 'verify', 'confirm', 'secure', 'bank', 'credit', 'payment']
        text_lower = text.lower()
        return sum(1 for word in financial_words if word in text_lower)
    
    def _count_threat_indicators(self, text: str) -> int:
        """Count threat indicators"""
        threat_words = ['suspended', 'blocked', 'terminated', 'legal', 'police', 'court', 'action']
        text_lower = text.lower()
        return sum(1 for word in threat_words if word in text_lower)
    
    def _check_suspicious_sender(self, sender: str) -> int:
        """Check if sender is suspicious"""
        suspicious_patterns = ['noreply', 'support', 'security', 'verify', 'fake']
        return int(any(pattern in sender.lower() for pattern in suspicious_patterns))
    
    def _check_suspicious_subject(self, subject: str) -> int:
        """Check if subject is suspicious"""
        suspicious_patterns = ['urgent', 'verify', 'suspended', 'account', 'action']
        return int(any(pattern in subject.lower() for pattern in suspicious_patterns))
    
    def _count_suspicious_urls(self, text: str) -> int:
        """Count suspicious URLs"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co']
        text_lower = text.lower()
        return sum(1 for domain in suspicious_domains if domain in text_lower)
    
    def _is_unusual_time(self, timestamp: str) -> int:
        """Check if timestamp is unusual"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            hour = dt.hour
            return int(hour < 6 or hour > 22)  # Unusual hours
        except:
            return 0
    
    def _is_suspicious_link(self, link: str) -> bool:
        """Check if link is suspicious"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co']
        return any(domain in link.lower() for domain in suspicious_domains)
    
    def _count_spam_indicators(self, text: str) -> int:
        """Count spam indicators"""
        spam_words = ['buy', 'sell', 'investment', 'crypto', 'bitcoin', 'earn', 'money', 'profit']
        text_lower = text.lower()
        return sum(1 for word in spam_words if word in text_lower)
    
    def _count_suspicious_patterns(self, content: str) -> int:
        """Count general suspicious patterns"""
        patterns = [
            r'\b(urgent|immediate|now|quick|fast|hurry)\b',
            r'\b(account|password|verify|confirm|secure)\b',
            r'\b(suspended|blocked|terminated|legal|police)\b'
        ]
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content, re.IGNORECASE))
        return total
    
    def train_model(self, channel: str, training_data: List[Dict[str, Any]]):
        """Store training data for reference"""
        print(f"🔄 Storing training data for {channel} model...")
        self.training_data[channel].extend(training_data)
        
        # Calculate simple performance metrics
        correct_predictions = 0
        total_predictions = len(training_data)
        
        for sample in training_data:
            features = self.extract_features(sample['data'], channel)
            predicted_risk = self.predict_risk(features, channel)
            
            predicted_fraud = predicted_risk > 0.5
            actual_fraud = sample['is_fraud']
            
            if predicted_fraud == actual_fraud:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        self.model_performance[channel] = {
            'accuracy': accuracy,
            'trained_at': datetime.now().isoformat(),
            'samples': total_predictions,
            'correct_predictions': correct_predictions
        }
        
        print(f"✅ {channel} model performance recorded: {accuracy:.3f} accuracy")
    
    def save_models(self, filepath: str):
        """Save training data and performance metrics"""
        model_data = {
            'training_data': dict(self.training_data),
            'model_performance': self.model_performance
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        print(f"💾 Training data saved to {filepath}")
    
    def load_models(self, filepath: str):
        """Load training data and performance metrics"""
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            
            self.training_data = defaultdict(list, model_data.get('training_data', {}))
            self.model_performance = model_data.get('model_performance', {})
            
            print(f"📂 Training data loaded from {filepath}")
        except FileNotFoundError:
            print(f"⚠️ No saved training data found at {filepath}")
        except Exception as e:
            print(f"⚠️ Error loading training data: {e}") 