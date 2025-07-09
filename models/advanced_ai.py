import numpy as np
import pandas as pd
import re
import json
import pickle
import joblib
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Any

# Machine Learning
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

# Deep Learning
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available, using fallback models")

# Natural Language Processing
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.sentiment import SentimentIntensityAnalyzer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available, using fallback text processing")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("spaCy not available, using fallback NLP")

# Transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available, using fallback models")

class AdvancedAISystem:
    """Advanced AI system with ML, DL, and NLP capabilities"""
    
    def __init__(self):
        self.ml_models = {}
        self.dl_models = {}
        self.nlp_models = {}
        self.vectorizers = {}
        self.scalers = {}
        self.label_encoders = {}
        
        # Initialize models
        self._initialize_ml_models()
        self._initialize_dl_models()
        self._initialize_nlp_models()
        
        # Training data storage
        self.training_data = defaultdict(list)
        self.model_performance = {}
        
    def _initialize_ml_models(self):
        """Initialize Machine Learning models"""
        print("🤖 Initializing Machine Learning models...")
        
        # Email classification model
        self.ml_models['email_classifier'] = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=5000, ngram_range=(1, 3))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Transaction fraud detection
        self.ml_models['transaction_classifier'] = RandomForestClassifier(
            n_estimators=100, random_state=42
        )
        
        # Social media scam detection
        self.ml_models['social_media_classifier'] = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=3000, ngram_range=(1, 2))),
            ('classifier', GradientBoostingClassifier(random_state=42))
        ])
        
        # Webpage scam detection
        self.ml_models['webpage_classifier'] = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=2000, ngram_range=(1, 2))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Feature scalers
        self.scalers['transaction'] = StandardScaler()
        self.scalers['user_behavior'] = StandardScaler()
        
        print("✅ ML models initialized")
    
    def _initialize_dl_models(self):
        """Initialize Deep Learning models"""
        if not TENSORFLOW_AVAILABLE:
            print("⚠️ TensorFlow not available, skipping DL models")
            return
            
        print("🧠 Initializing Deep Learning models...")
        
        # Text classification model
        self.dl_models['text_classifier'] = self._build_text_classifier()
        
        # Multi-modal fusion model
        self.dl_models['multimodal_fusion'] = self._build_multimodal_model()
        
        # Sequence model for time-series data
        self.dl_models['sequence_classifier'] = self._build_sequence_model()
        
        # Tokenizers
        self.dl_models['tokenizer'] = Tokenizer(num_words=10000, oov_token="<OOV>")
        
        print("✅ DL models initialized")
    
    def _initialize_nlp_models(self):
        """Initialize Natural Language Processing models"""
        print("📝 Initializing NLP models...")
        
        # Download NLTK data
        if NLTK_AVAILABLE:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                nltk.download('vader_lexicon', quiet=True)
                
                self.nlp_models['sentiment_analyzer'] = SentimentIntensityAnalyzer()
                self.nlp_models['lemmatizer'] = WordNetLemmatizer()
                self.nlp_models['stop_words'] = set(stopwords.words('english'))
            except:
                print("⚠️ NLTK data download failed")
        
        # spaCy model
        if SPACY_AVAILABLE:
            try:
                self.nlp_models['spacy_nlp'] = spacy.load("en_core_web_sm")
            except:
                print("⚠️ spaCy model not available")
        
        # Transformers models
        if TRANSFORMERS_AVAILABLE:
            try:
                self.nlp_models['sentiment_pipeline'] = pipeline(
                    "sentiment-analysis", 
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
                self.nlp_models['text_classification'] = pipeline(
                    "text-classification",
                    model="microsoft/DialoGPT-medium"
                )
            except:
                print("⚠️ Transformers models not available")
        
        print("✅ NLP models initialized")
    
    def _build_text_classifier(self):
        """Build deep learning text classification model"""
        model = keras.Sequential([
            layers.Embedding(10000, 128, input_length=100),
            layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
            layers.Bidirectional(layers.LSTM(32)),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _build_multimodal_model(self):
        """Build multi-modal fusion model"""
        # Text input
        text_input = layers.Input(shape=(100,), name='text_input')
        text_embedding = layers.Embedding(10000, 128)(text_input)
        text_lstm = layers.LSTM(64)(text_embedding)
        
        # Numerical features input
        numerical_input = layers.Input(shape=(10,), name='numerical_input')
        numerical_dense = layers.Dense(32, activation='relu')(numerical_input)
        
        # Combine features
        combined = layers.Concatenate()([text_lstm, numerical_dense])
        dense1 = layers.Dense(128, activation='relu')(combined)
        dropout1 = layers.Dropout(0.3)(dense1)
        dense2 = layers.Dense(64, activation='relu')(dropout1)
        dropout2 = layers.Dropout(0.2)(dense2)
        output = layers.Dense(1, activation='sigmoid')(dropout2)
        
        model = keras.Model(
            inputs=[text_input, numerical_input],
            outputs=output
        )
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _build_sequence_model(self):
        """Build sequence model for time-series data"""
        model = keras.Sequential([
            layers.LSTM(64, return_sequences=True, input_shape=(None, 10)),
            layers.LSTM(32, return_sequences=False),
            layers.Dense(16, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_text(self, text: str) -> str:
        """Advanced text preprocessing"""
        if not text:
            return ""
        
        # Ensure text is string
        text = str(text)
        
        # Basic cleaning
        text = re.sub(r'[^\w\s]', '', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        
        if NLTK_AVAILABLE:
            # Tokenization
            tokens = word_tokenize(text)
            
            # Remove stopwords and lemmatize
            tokens = [
                self.nlp_models['lemmatizer'].lemmatize(token)
                for token in tokens
                if token not in self.nlp_models['stop_words']
            ]
            
            return ' '.join(tokens)
        
        return text
    
    def extract_features(self, data: Dict[str, Any], channel: str) -> Dict[str, Any]:
        """Extract advanced features using NLP and ML"""
        features = {}
        
        if channel == 'email':
            features.update(self._extract_email_features(data))
        elif channel == 'transaction':
            features.update(self._extract_transaction_features(data))
        elif channel == 'social_media':
            features.update(self._extract_social_features(data))
        elif channel == 'user_behavior':
            features.update(self._extract_behavior_features(data))
        elif channel == 'webpage':
            features.update(self._extract_webpage_features(data))
        
        return features
    
    def _extract_email_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract advanced email features with comprehensive NLP analysis"""
        content = str(data.get('content', ''))
        sender = str(data.get('sender', ''))
        subject = str(data.get('subject', ''))
        
        # Basic email features
        features = {
            'raw_content': content,  # Add raw content for ML model
            'content': content,      # Also add as 'content' for compatibility
            'text_length': len(content),
            'word_count': len(content.split()),
            'avg_word_length': np.mean([len(word) for word in content.split()]) if content.split() else 0,
            'has_links': int('http' in content.lower()),
            'has_attachments': int('attachment' in content.lower()),
            'urgency_score': self._calculate_urgency_score(content),
            'financial_terms': self._count_financial_terms(content),
            'threat_indicators': self._count_threat_indicators(content),
            'sender_domain_suspicious': self._check_sender_domain(sender),
            'subject_suspicious': self._analyze_subject(subject)
        }
        
        # Advanced NLP features
        features.update(self._extract_nlp_features(content))
        
        # Subject line analysis
        if subject:
            subject_features = self._extract_nlp_features(subject)
            features.update({
                'subject_' + key: value for key, value in subject_features.items()
            })
        
        # Sender analysis
        if sender:
            sender_features = self._extract_nlp_features(sender)
            features.update({
                'sender_' + key: value for key, value in sender_features.items()
            })
        
        return features
    
    def _extract_transaction_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transaction features"""
        amount = float(data.get('amount', 0))
        location = data.get('location', {})
        timestamp = data.get('timestamp', '')
        
        features = {
            'amount': amount,
            'amount_log': np.log(amount + 1),
            'is_high_value': int(amount > 10000),
            'is_negative': int(amount < 0),
            'location_distance': location.get('distance_from_home', 0),
            'is_foreign': int(location.get('country', '') != 'US'),
            'hour_of_day': self._extract_hour(timestamp),
            'day_of_week': self._extract_day_of_week(timestamp),
            'is_weekend': int(self._is_weekend(timestamp)),
            'is_holiday': int(self._is_holiday(timestamp))
        }
        
        return features
    
    def _extract_social_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract social media features with comprehensive NLP analysis"""
        content = str(data.get('content', ''))
        profile = data.get('profile', {})
        links = data.get('links', [])
        
        # Basic social media features
        features = {
            'content_length': len(content),
            'hashtag_count': content.count('#'),
            'mention_count': content.count('@'),
            'link_count': len(links),
            'suspicious_link_count': len([l for l in links if self._is_suspicious_link(l)]),
            'follower_count': profile.get('followers', 0),
            'follower_log': np.log(profile.get('followers', 1)),
            'is_verified': int(profile.get('verified', False)),
            'account_age_days': profile.get('account_age_days', 0),
            'engagement_rate': self._calculate_engagement_rate(profile)
        }
        
        # Advanced NLP features for content analysis
        features.update(self._extract_nlp_features(content))
        
        # Profile analysis
        if profile:
            profile_text = f"{profile.get('name', '')} {profile.get('bio', '')} {profile.get('location', '')}"
            if profile_text.strip():
                profile_features = self._extract_nlp_features(profile_text)
                features.update({
                    'profile_' + key: value for key, value in profile_features.items()
                })
        
        return features
    
    def _extract_behavior_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user behavior features"""
        login_patterns = data.get('login_patterns', {})
        account_activity = data.get('account_activity', {})
        interaction_patterns = data.get('interaction_patterns', {})
        
        features = {
            'unusual_time': int(login_patterns.get('unusual_time', False)),
            'new_device': int(login_patterns.get('new_device', False)),
            'new_location': int(login_patterns.get('new_location', False)),
            'suspicious_actions': account_activity.get('suspicious_actions', 0),
            'failed_logins': account_activity.get('failed_logins', 0),
            'unusual_pattern': int(interaction_patterns.get('unusual_pattern', False)),
            'session_duration': account_activity.get('session_duration', 0),
            'page_views': account_activity.get('page_views', 0)
        }
        
        return features
    
    def _extract_webpage_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from a webpage/URL for scam detection"""
        url = data.get('url', '')
        content = data.get('content', '')
        features = {
            'url_length': len(url),
            'has_https': int(url.startswith('https://')),
            'has_ip': int(bool(re.search(r'https?://\d+\.\d+\.\d+\.\d+', url))),
            'num_subdomains': url.count('.') - 1,
            'is_shortened': int(any(short in url for short in ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co', 'shorturl'])),
            'phishing_keywords': int(any(word in url.lower() for word in ['login', 'signin', 'verify', 'secure', 'bank', 'account', 'update', 'confirm'])),
            'suspicious_tld': int(any(url.endswith(tld) for tld in ['.tk', '.ml', '.ga', '.cf', '.gq'])),
            'content_length': len(content),
            'form_count': len(re.findall(r'<form', content)),
            'external_link_count': len(re.findall(r'href=["\"](http|https)://', content)),
            'script_count': len(re.findall(r'<script', content)),
            'suspicious_script_count': len(re.findall(r'<script[^>]*src=["\"](?!https?://trusted)', content)),
        }
        # Add NLP features from visible text
        features.update(self._extract_nlp_features(content))
        return features
    
    def _extract_nlp_features(self, text: str) -> Dict[str, Any]:
        """Extract advanced NLP-based features for fraud detection"""
        features = {}
        
        if not text:
            return features
        
        # Ensure text is string
        text = str(text)
        
        # Basic text statistics
        features.update({
            'text_length': len(text),
            'word_count': len(text.split()),
            'avg_word_length': np.mean([len(word) for word in text.split()]) if text.split() else 0,
            'sentence_count': len(text.split('.')),
            'paragraph_count': len(text.split('\n\n')),
            'unique_words_ratio': len(set(text.lower().split())) / max(len(text.split()), 1)
        })
        
        # Linguistic patterns for fraud detection
        features.update(self._extract_fraud_linguistic_patterns(text))
        
        # Sentiment analysis
        if NLTK_AVAILABLE and 'sentiment_analyzer' in self.nlp_models:
            try:
                sentiment = self.nlp_models['sentiment_analyzer'].polarity_scores(text)
                features.update({
                    'sentiment_compound': sentiment['compound'],
                    'sentiment_positive': sentiment['pos'],
                    'sentiment_negative': sentiment['neg'],
                    'sentiment_neutral': sentiment['neu']
                })
            except Exception as e:
                print(f"NLTK sentiment analysis error: {e}")
        
        # Advanced text analysis
        features.update(self._extract_advanced_text_features(text))
        
        # Entity recognition and analysis
        features.update(self._extract_entity_features(text))
        
        # Readability and complexity metrics
        features.update(self._extract_readability_features(text))
        
        return features
    
    def _extract_fraud_linguistic_patterns(self, text: str) -> Dict[str, Any]:
        """Extract linguistic patterns commonly associated with fraud"""
        text_lower = text.lower()
        
        # Urgency indicators
        urgency_words = ['urgent', 'immediate', 'now', 'quick', 'fast', 'hurry', 'deadline', 'expire', 'limited time']
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        
        # Authority indicators
        authority_words = ['police', 'government', 'court', 'legal', 'official', 'federal', 'irs', 'tax']
        authority_count = sum(1 for word in authority_words if word in text_lower)
        
        # Financial pressure indicators
        financial_pressure = ['owe', 'debt', 'payment', 'overdue', 'penalty', 'fine', 'suspended', 'blocked']
        financial_pressure_count = sum(1 for word in financial_pressure if word in text_lower)
        
        # Reward indicators
        reward_words = ['prize', 'winner', 'selected', 'exclusive', 'limited', 'offer', 'free', 'bonus', 'gift']
        reward_count = sum(1 for word in reward_words if word in text_lower)
        
        # Personal information requests
        personal_info = ['ssn', 'social security', 'credit card', 'bank account', 'password', 'pin', 'dob', 'birth date']
        personal_info_count = sum(1 for phrase in personal_info if phrase in text_lower)
        
        # Suspicious action verbs
        action_verbs = ['verify', 'confirm', 'update', 'validate', 'secure', 'protect', 'restore', 'reactivate']
        action_verb_count = sum(1 for word in action_verbs if word in text_lower)
        
        # Emotional manipulation
        emotional_words = ['family', 'emergency', 'help', 'crisis', 'danger', 'threat', 'consequences']
        emotional_count = sum(1 for word in emotional_words if word in text_lower)
        
        # Grammar and spelling indicators
        grammar_errors = len(re.findall(r'\b(ur|u|r|y|ur|u r|u r)\b', text_lower))
        caps_ratio = sum(1 for char in text if char.isupper()) / max(len(text), 1)
        
        return {
            'urgency_indicators': urgency_count,
            'authority_indicators': authority_count,
            'financial_pressure': financial_pressure_count,
            'reward_indicators': reward_count,
            'personal_info_requests': personal_info_count,
            'action_verb_count': action_verb_count,
            'emotional_manipulation': emotional_count,
            'grammar_errors': grammar_errors,
            'caps_ratio': caps_ratio,
            'total_fraud_indicators': urgency_count + authority_count + financial_pressure_count + 
                                    reward_count + personal_info_count + emotional_count
        }
    
    def _extract_advanced_text_features(self, text: str) -> Dict[str, Any]:
        """Extract advanced text analysis features"""
        text_lower = text.lower()
        
        # URL and link analysis
        urls = re.findall(r'https?://[^\s<>"]+', text)
        suspicious_urls = [url for url in urls if any(domain in url for domain in 
                           ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co', 'shorturl'])]
        
        # Phone number patterns
        phone_patterns = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        
        # Email patterns
        email_patterns = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        # Currency and amount patterns
        currency_patterns = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
        
        # Time pressure indicators
        time_patterns = re.findall(r'\b(within|before|until|by|deadline|expires?)\b', text_lower)
        
        # Exclamation and question marks
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        # Repetition analysis
        words = text_lower.split()
        word_freq = {}
        for word in words:
            if len(word) > 2:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        most_repeated = max(word_freq.values()) if word_freq else 0
        
        return {
            'url_count': len(urls),
            'suspicious_url_count': len(suspicious_urls),
            'phone_patterns': len(phone_patterns),
            'email_patterns': len(email_patterns),
            'currency_patterns': len(currency_patterns),
            'time_pressure_indicators': len(time_patterns),
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'most_repeated_word_count': most_repeated,
            'text_complexity': len(set(words)) / max(len(words), 1)
        }
    
    def _extract_entity_features(self, text: str) -> Dict[str, Any]:
        """Extract named entity recognition features"""
        features = {}
        
        # Basic entity patterns
        # Organizations
        org_patterns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|LLC|Ltd|Company|Bank|Banking|Financial|Insurance)\b', text)
        
        # Government entities
        gov_patterns = re.findall(r'\b(?:IRS|FBI|CIA|NSA|Federal|Government|Department|Agency)\b', text)
        
        # Financial institutions
        financial_patterns = re.findall(r'\b(?:Bank|Credit|Union|Savings|Trust|Investment|Securities|Trading)\b', text)
        
        # Personal names (basic pattern)
        name_patterns = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
        
        features.update({
            'organization_mentions': len(org_patterns),
            'government_mentions': len(gov_patterns),
            'financial_institution_mentions': len(financial_patterns),
            'personal_name_mentions': len(name_patterns),
            'total_entity_mentions': len(org_patterns) + len(gov_patterns) + len(financial_patterns) + len(name_patterns)
        })
        
        return features
    
    def _extract_readability_features(self, text: str) -> Dict[str, Any]:
        """Extract readability and complexity metrics"""
        sentences = text.split('.')
        words = text.split()
        
        if not sentences or not words:
            return {
                'avg_sentence_length': 0,
                'avg_word_length': 0,
                'readability_score': 0,
                'complexity_score': 0
            }
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Average word length
        avg_word_length = np.mean([len(word) for word in words])
        
        # Simple readability score (Flesch Reading Ease approximation)
        syllables = sum(len(re.findall(r'[aeiouy]+', word.lower())) for word in words)
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (syllables / len(words)))
        
        # Complexity score based on word length and sentence structure
        long_words = sum(1 for word in words if len(word) > 6)
        complexity_score = (long_words / len(words)) * 100 + (avg_sentence_length / 20) * 100
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'readability_score': max(0, min(100, readability_score)),
            'complexity_score': min(100, complexity_score),
            'long_word_ratio': long_words / max(len(words), 1)
        }
    
    def predict_risk(self, features: Dict[str, Any], channel: str) -> float:
        """Predict risk using ML/DL models"""
        try:
            if channel == 'email':
                return self._predict_email_risk(features)
            elif channel == 'transaction':
                return self._predict_transaction_risk(features)
            elif channel == 'social_media':
                return self._predict_social_risk(features)
            elif channel == 'webpage':
                return self._predict_webpage_risk(features)
            else:
                return self._predict_generic_risk(features)
        except Exception as e:
            print(f"Error in risk prediction: {e}")
            return 0.5  # Default risk score
    
    def _get_feature_vector(self, features: Dict[str, Any], channel: str) -> list:
        """Get feature vector in consistent order for the channel"""
        if channel == 'email':
            feature_names = [
                'text_length', 'word_count', 'avg_word_length', 'has_links', 'has_attachments',
                'urgency_score', 'financial_terms', 'threat_indicators',
                'sender_domain_suspicious', 'subject_suspicious'
            ]
            # Add NLP features if available
            if NLTK_AVAILABLE:
                feature_names += ['sentiment_compound', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral']
            # spaCy features
            if 'spacy_nlp' in self.nlp_models:
                feature_names += ['entity_count', 'noun_count', 'verb_count', 'adjective_count']
        elif channel == 'transaction':
            feature_names = [
                'amount', 'amount_log', 'is_high_value', 'is_negative', 'location_distance',
                'is_foreign', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_holiday'
            ]
        elif channel == 'social_media':
            feature_names = [
                'content_length', 'hashtag_count', 'mention_count', 'link_count', 'suspicious_link_count',
                'follower_count', 'follower_log', 'is_verified', 'account_age_days', 'engagement_rate'
            ]
        elif channel == 'webpage':
            feature_names = [
                'url_length', 'has_https', 'has_ip', 'num_subdomains', 'is_shortened',
                'phishing_keywords', 'suspicious_tld', 'content_length', 'form_count',
                'external_link_count', 'script_count', 'suspicious_script_count'
            ]
        else:
            feature_names = list(features.keys())
        return [features.get(name, 0) for name in feature_names]

    def _predict_email_risk(self, features: Dict[str, Any]) -> float:
        """Predict email risk using ML model"""
        print(f"[DEBUG] Email prediction - Features keys: {list(features.keys())}")
        
        model = self.ml_models.get('email_classifier')
        if model is not None:
            print(f"[DEBUG] ML model found: {type(model)}")
            # For text models, pass raw text to the pipeline
            content = features.get('raw_content') or features.get('content')
            if not content:
                content = ''
            print(f"[DEBUG] Email content length: {len(content)}")
            X = [content]
            try:
                proba = model.predict_proba(X)[0][1]  # Probability of fraud
                risk_score = float(proba)
                print(f"[DEBUG] ML prediction - Raw proba: {proba}, Risk score: {risk_score}")
                # Ensure we get meaningful risk scores
                if risk_score < 0.1:
                    # If ML gives very low score, check if it's actually suspicious
                    if features.get('urgency_score', 0) > 1 or features.get('threat_indicators', 0) > 2:
                        risk_score = max(risk_score, 0.4)  # Boost suspicious cases
                        print(f"[DEBUG] Boosted risk score to: {risk_score}")
                return risk_score
            except Exception as e:
                print(f"[DEBUG] ML email predict error: {e}")
                # Enhanced fallback with better risk assessment
                risk_score = 0.0
                risk_score += features.get('urgency_score', 0) * 0.25
                risk_score += features.get('financial_terms', 0) * 0.2
                risk_score += features.get('threat_indicators', 0) * 0.3
                risk_score += features.get('has_links', 0) * 0.15
                risk_score += features.get('sender_domain_suspicious', 0) * 0.35
                risk_score += features.get('subject_suspicious', 0) * 0.25
                sentiment_compound = features.get('sentiment_compound', 0)
                if sentiment_compound < -0.3:
                    risk_score += 0.2
                print(f"[DEBUG] Fallback risk score: {risk_score}")
                return min(risk_score, 1.0)
        else:
            print(f"[DEBUG] No ML model found, using rule-based fallback")
        
        # Enhanced rule-based fallback
        risk_score = 0.0
        risk_score += features.get('urgency_score', 0) * 0.25
        risk_score += features.get('financial_terms', 0) * 0.2
        risk_score += features.get('threat_indicators', 0) * 0.3
        risk_score += features.get('has_links', 0) * 0.15
        risk_score += features.get('sender_domain_suspicious', 0) * 0.35
        risk_score += features.get('subject_suspicious', 0) * 0.25
        sentiment_compound = features.get('sentiment_compound', 0)
        if sentiment_compound < -0.3:
            risk_score += 0.2
        print(f"[DEBUG] Rule-based risk score: {risk_score}")
        return min(risk_score, 1.0)

    def _predict_transaction_risk(self, features: Dict[str, Any]) -> float:
        """Predict transaction risk using ML model"""
        model = self.ml_models.get('transaction_classifier')
        if model is not None:
            X = [self._get_feature_vector(features, 'transaction')]
            try:
                proba = model.predict_proba(X)[0][1]
                risk_score = float(proba)
                # Ensure we get meaningful risk scores for suspicious transactions
                if risk_score < 0.1:
                    amount = features.get('amount', 0)
                    if amount > 10000 or amount < 0 or features.get('is_foreign', 0):
                        risk_score = max(risk_score, 0.5)  # Boost suspicious transactions
                return risk_score
            except Exception as e:
                print(f"ML transaction predict error: {e}")
                # Enhanced fallback with better risk assessment
                risk_score = 0.0
                amount = features.get('amount', 0)
                if amount > 10000:
                    risk_score += 0.4
                elif amount < 0:
                    risk_score += 0.5
                if features.get('is_foreign', 0):
                    risk_score += 0.3
                if features.get('location_distance', 0) > 1000:
                    risk_score += 0.35
                if features.get('is_weekend', 0):
                    risk_score += 0.15
                if features.get('hour_of_day', 12) < 6 or features.get('hour_of_day', 12) > 22:
                    risk_score += 0.2
                return min(risk_score, 1.0)
        # Enhanced rule-based fallback
        risk_score = 0.0
        amount = features.get('amount', 0)
        if amount > 10000:
            risk_score += 0.4
        elif amount < 0:
            risk_score += 0.5
        if features.get('is_foreign', 0):
            risk_score += 0.3
        if features.get('location_distance', 0) > 1000:
            risk_score += 0.35
        if features.get('is_weekend', 0):
            risk_score += 0.15
        if features.get('hour_of_day', 12) < 6 or features.get('hour_of_day', 12) > 22:
            risk_score += 0.2
        return min(risk_score, 1.0)

    def _predict_social_risk(self, features: Dict[str, Any]) -> float:
        """Predict social media risk using ML model"""
        model = self.ml_models.get('social_media_classifier')
        if model is not None:
            # For text models, pass raw text to the pipeline
            content = features.get('raw_content') or features.get('content')
            if not content:
                content = ''
            X = [content]
            try:
                proba = model.predict_proba(X)[0][1]
                risk_score = float(proba)
                # Ensure we get meaningful risk scores for suspicious social media
                if risk_score < 0.1:
                    if (features.get('follower_count', 0) < 10 or 
                        features.get('suspicious_link_count', 0) > 0 or
                        not features.get('is_verified', 0)):
                        risk_score = max(risk_score, 0.45)  # Boost suspicious social media
                return risk_score
            except Exception as e:
                print(f"ML social predict error: {e}")
                # Enhanced fallback with better risk assessment
                risk_score = 0.0
                if features.get('follower_count', 0) < 10:
                    risk_score += 0.4
                if not features.get('is_verified', 0):
                    risk_score += 0.3
                risk_score += features.get('suspicious_link_count', 0) * 0.25
                risk_score += features.get('hashtag_count', 0) * 0.1
                if features.get('engagement_rate', 0) < 0.01:
                    risk_score += 0.2
                return min(risk_score, 1.0)
        # Enhanced rule-based fallback
        risk_score = 0.0
        if features.get('follower_count', 0) < 10:
            risk_score += 0.4
        if not features.get('is_verified', 0):
            risk_score += 0.3
        risk_score += features.get('suspicious_link_count', 0) * 0.25
        risk_score += features.get('hashtag_count', 0) * 0.1
        if features.get('engagement_rate', 0) < 0.01:
            risk_score += 0.2
        return min(risk_score, 1.0)
    
    def _predict_webpage_risk(self, features: Dict[str, Any]) -> float:
        model = self.ml_models.get('webpage_classifier')
        if model is not None:
            url = features.get('raw_url') or features.get('url', '')
            content = features.get('raw_content') or features.get('content', '')
            X = [url + ' ' + content]
            try:
                proba = model.predict_proba(X)[0][1]
                risk_score = float(proba)
                if risk_score < 0.1:
                    if features.get('is_shortened', 0) or features.get('phishing_keywords', 0):
                        risk_score = max(risk_score, 0.5)
                return risk_score
            except Exception as e:
                print(f"ML webpage predict error: {e}")
                risk_score = 0.0
                risk_score += features.get('is_shortened', 0) * 0.3
                risk_score += features.get('phishing_keywords', 0) * 0.3
                risk_score += features.get('suspicious_tld', 0) * 0.2
                risk_score += features.get('has_ip', 0) * 0.2
                risk_score += features.get('form_count', 0) * 0.1
                return min(risk_score, 1.0)
        # Enhanced rule-based fallback
        risk_score = 0.0
        risk_score += features.get('is_shortened', 0) * 0.3
        risk_score += features.get('phishing_keywords', 0) * 0.3
        risk_score += features.get('suspicious_tld', 0) * 0.2
        risk_score += features.get('has_ip', 0) * 0.2
        risk_score += features.get('form_count', 0) * 0.1
        return min(risk_score, 1.0)
    
    def _predict_generic_risk(self, features: Dict[str, Any]) -> float:
        """Generic risk prediction"""
        return 0.5
    
    def train_model(self, channel: str, training_data: List[Dict[str, Any]]):
        """Train ML model with new data"""
        if not training_data:
            return
        print(f"🔄 Training {channel} model with {len(training_data)} samples...")
        channel_to_model = {
            'email': 'email_classifier',
            'transaction': 'transaction_classifier',
            'social_media': 'social_media_classifier',
            'webpage': 'webpage_classifier'
        }
        model_name = channel_to_model.get(channel, channel)
        X = []
        y = []
        for sample in training_data:
            features = self.extract_features(sample['data'], channel)
            if channel == 'email':
                content = sample['data'].get('content', '')
                features['raw_content'] = content
                X.append(content)
            elif channel == 'social_media':
                content = sample['data'].get('content', '')
                features['raw_content'] = content
                X.append(content)
            elif channel == 'webpage':
                url = sample['data'].get('url', '')
                content = sample['data'].get('content', '')
                features['raw_url'] = url
                features['raw_content'] = content
                X.append(url + ' ' + content)
            else:
                feature_vector = self._get_feature_vector(features, channel)
                X.append(feature_vector)
            y.append(1 if sample['is_fraud'] else 0)
        # Only convert to np.array for transaction (numeric) models
        if channel == 'transaction':
            X = np.array(X)
        y = np.array(y)
        print(f"📊 Feature vector shape: {np.array(X).shape if channel == 'transaction' else len(X)}")
        print(f"📊 Labels shape: {y.shape}")
        print(f"📊 Fraud samples: {sum(y)}, Legitimate samples: {len(y) - sum(y)}")
        print(f"📊 Model name: {model_name}")
        if model_name in self.ml_models:
            try:
                self.ml_models[model_name].fit(X, y)
                y_pred = self.ml_models[model_name].predict(X)
                accuracy = accuracy_score(y, y_pred)
                if len(X) > 0:
                    sample_pred = self.ml_models[model_name].predict_proba([X[0]])[0]
                    print(f"📊 Sample prediction probabilities: {sample_pred}")
                self.model_performance[channel] = {
                    'accuracy': accuracy,
                    'trained_at': datetime.now().isoformat(),
                    'samples': len(training_data),
                    'fraud_samples': int(sum(y)),
                    'legitimate_samples': int(len(y) - sum(y)),
                    'model_used': model_name
                }
                print(f"✅ {channel} model trained with {accuracy:.3f} accuracy")
                print(f"📊 Model performance saved: {self.model_performance[channel]}")
            except Exception as e:
                print(f"❌ Error training {channel} model: {e}")
                self.model_performance[channel] = {
                    'accuracy': 0.0,
                    'trained_at': datetime.now().isoformat(),
                    'samples': len(training_data),
                    'error': str(e)
                }
        else:
            print(f"⚠️ No ML model found for channel: {channel} (model: {model_name})")
            print(f"📊 Available models: {list(self.ml_models.keys())}")
            self.model_performance[channel] = {
                'accuracy': 0.5,
                'trained_at': datetime.now().isoformat(),
                'samples': len(training_data),
                'method': 'rule-based'
            }
    
    def save_models(self, filepath: str):
        """Save trained models"""
        model_data = {
            'ml_models': self.ml_models,
            'scalers': self.scalers,
            'performance': self.model_performance
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Models saved to {filepath}")
    
    def load_models(self, filepath: str):
        """Load trained models"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.ml_models = model_data['ml_models']
            self.scalers = model_data['scalers']
            self.model_performance = model_data['performance']
            
            print(f"📂 Models loaded from {filepath}")
        except FileNotFoundError:
            print(f"⚠️ No saved models found at {filepath}")
    
    # Helper methods
    def _calculate_urgency_score(self, text: str) -> float:
        """Calculate urgency score in text"""
        urgency_words = ['urgent', 'immediate', 'now', 'quick', 'fast', 'hurry', 'asap']
        text_lower = text.lower()
        return sum(1 for word in urgency_words if word in text_lower) / len(urgency_words)
    
    def _count_financial_terms(self, text: str) -> int:
        """Count financial terms in text"""
        financial_words = ['account', 'password', 'verify', 'confirm', 'secure', 'bank', 'credit', 'payment']
        text_lower = text.lower()
        return sum(1 for word in financial_words if word in text_lower)
    
    def _count_threat_indicators(self, text: str) -> int:
        """Count threat indicators in text"""
        threat_words = ['suspended', 'blocked', 'terminated', 'legal', 'police', 'court', 'action']
        text_lower = text.lower()
        return sum(1 for word in threat_words if word in text_lower)
    
    def _check_sender_domain(self, sender: str) -> int:
        """Check if sender domain is suspicious"""
        suspicious_domains = ['noreply', 'support', 'security', 'verify', 'fake']
        return int(any(domain in sender.lower() for domain in suspicious_domains))
    
    def _analyze_subject(self, subject: str) -> int:
        """Analyze subject line for suspicious patterns"""
        suspicious_patterns = ['urgent', 'verify', 'suspended', 'account', 'action']
        return int(any(pattern in subject.lower() for pattern in suspicious_patterns))
    
    def _is_suspicious_link(self, link: str) -> bool:
        """Check if link is suspicious"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'goo.gl', 'is.gd', 't.co']
        return any(domain in link.lower() for domain in suspicious_domains)
    
    def _calculate_engagement_rate(self, profile: Dict[str, Any]) -> float:
        """Calculate engagement rate"""
        followers = profile.get('followers', 1)
        likes = profile.get('likes', 0)
        comments = profile.get('comments', 0)
        return (likes + comments) / followers if followers > 0 else 0
    
    def _extract_hour(self, timestamp: str) -> int:
        """Extract hour from timestamp"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.hour
        except:
            return 12
    
    def _extract_day_of_week(self, timestamp: str) -> int:
        """Extract day of week from timestamp"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.weekday()
        except:
            return 0
    
    def _is_weekend(self, timestamp: str) -> bool:
        """Check if timestamp is on weekend"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.weekday() >= 5
        except:
            return False
    
    def _is_holiday(self, timestamp: str) -> bool:
        """Check if timestamp is on holiday (simplified)"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            # Simplified holiday check
            return dt.month == 12 and dt.day in [25, 26] or dt.month == 1 and dt.day == 1
        except:
            return False 