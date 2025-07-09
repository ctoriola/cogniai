"""
Simple AI system that works without heavy ML dependencies
"""

import re
import json
import pickle
import os
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

class SimpleAISystem:
    """Simple AI system that works without heavy dependencies"""
    
    def __init__(self):
        self.models = {}
        self.training_data = defaultdict(list)
        self.model_performance = {}
        self.feature_weights = {
            'email': {
                'urgency_score': 0.2,
                'financial_terms': 0.15,
                'threat_indicators': 0.25,
                'suspicious_sender': 0.3,
                'suspicious_subject': 0.2,
                'suspicious_urls': 0.2,
                'sentiment_negative': 0.15
            },
            'transaction': {
                'high_amount': 0.4,
                'negative_amount': 0.4,
                'foreign_location': 0.3,
                'unusual_time': 0.2,
                'large_distance': 0.25
            },
            'social_media': {
                'low_followers': 0.3,
                'unverified': 0.2,
                'suspicious_links': 0.2,
                'spam_content': 0.25,
                'low_engagement': 0.15
            }
        }
    
    def extract_features(self, data: Dict[str, Any], channel: str) -> Dict[str, Any]:
        """Extract features from data"""
        features = {}
        
        if channel == 'email':
            content = data.get('content', '').lower()
            sender = data.get('sender', '').lower()
            subject = data.get('subject', '').lower()
            
            features.update({
                'urgency_score': self._calculate_urgency_score(content),
                'financial_terms': self._count_financial_terms(content),
                'threat_indicators': self._count_threat_indicators(content),
                'suspicious_sender': self._check_suspicious_sender(sender),
                'suspicious_subject': self._check_suspicious_subject(subject),
                'suspicious_urls': self._count_suspicious_urls(content),
                'sentiment_negative': self._calculate_sentiment(content)
            })
            
        elif channel == 'transaction':
            amount = float(data.get('amount', 0))
            location = data.get('location', {})
            timestamp = data.get('timestamp', '')
            
            features.update({
                'high_amount': int(amount > 10000),
                'negative_amount': int(amount < 0),
                'foreign_location': int(location.get('distance_from_home', 0) > 1000),
                'unusual_time': self._is_unusual_time(timestamp),
                'large_distance': int(location.get('distance_from_home', 0) > 500)
            })
            
        elif channel == 'social_media':
            content = data.get('content', '').lower()
            profile = data.get('profile', {})
            links = data.get('links', [])
            
            features.update({
                'low_followers': int(profile.get('followers', 0) < 10),
                'unverified': int(not profile.get('verified', False)),
                'suspicious_links': len([l for l in links if self._is_suspicious_link(l)]),
                'spam_content': self._count_spam_indicators(content),
                'low_engagement': int(profile.get('engagement_rate', 1) < 0.01)
            })
        
        return features
    
    def predict_risk(self, features: Dict[str, Any], channel: str) -> float:
        """Predict risk using weighted scoring"""
        if channel not in self.feature_weights:
            return 0.5
        
        weights = self.feature_weights[channel]
        risk_score = 0.0
        
        for feature, weight in weights.items():
            if feature in features:
                risk_score += features[feature] * weight
        
        return min(max(risk_score, 0.0), 1.0)
    
    def train_model(self, channel: str, training_data: List[Dict[str, Any]]):
        """Train model with data (simplified)"""
        print(f"🔄 Training {channel} model with {len(training_data)} samples...")
        
        # Store training data
        self.training_data[channel].extend(training_data)
        
        # Calculate simple performance metrics
        correct_predictions = 0
        total_predictions = len(training_data)
        
        for sample in training_data:
            features = self.extract_features(sample['data'], channel)
            predicted_risk = self.predict_risk(features, channel)
            
            # Simple threshold-based classification
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
        
        print(f"✅ {channel} model trained with {accuracy:.3f} accuracy")
    
    def save_models(self, filepath: str):
        """Save models and data"""
        model_data = {
            'training_data': dict(self.training_data),
            'model_performance': self.model_performance,
            'feature_weights': self.feature_weights
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Models saved to {filepath}")
    
    def load_models(self, filepath: str):
        """Load models and data"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.training_data = defaultdict(list, model_data.get('training_data', {}))
            self.model_performance = model_data.get('model_performance', {})
            self.feature_weights = model_data.get('feature_weights', self.feature_weights)
            
            print(f"📂 Models loaded from {filepath}")
        except FileNotFoundError:
            print(f"⚠️ No saved models found at {filepath}")
    
    # Helper methods
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
        return int(any(pattern in sender for pattern in suspicious_patterns))
    
    def _check_suspicious_subject(self, subject: str) -> int:
        """Check if subject is suspicious"""
        suspicious_patterns = ['urgent', 'verify', 'suspended', 'account', 'action']
        return int(any(pattern in subject.lower() for pattern in suspicious_patterns))
    
    def _count_suspicious_urls(self, text: str) -> int:
        """Count suspicious URLs"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co']
        text_lower = text.lower()
        return sum(1 for domain in suspicious_domains if domain in text_lower)
    
    def _calculate_sentiment(self, text: str) -> float:
        """Calculate simple sentiment score"""
        negative_words = ['urgent', 'suspended', 'blocked', 'terminated', 'legal', 'police']
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        return negative_count / len(negative_words) if negative_words else 0
    
    def _is_unusual_time(self, timestamp: str) -> int:
        """Check if timestamp is unusual"""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return int(dt.hour < 6 or dt.hour > 22)
        except:
            return 0
    
    def _is_suspicious_link(self, link: str) -> bool:
        """Check if link is suspicious"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co']
        return any(domain in link.lower() for domain in suspicious_domains)
    
    def _count_spam_indicators(self, text: str) -> int:
        """Count spam indicators"""
        spam_words = ['free', 'money', 'prize', 'winner', 'click', 'earn', 'investment']
        text_lower = text.lower()
        return sum(1 for word in spam_words if word in text_lower) 