# Omni-Channel AI Scam & Fraud Detection Platform

A comprehensive fraud detection system using **Machine Learning**, **Deep Learning**, and **Natural Language Processing** to detect scams and fraud across multiple communication channels.

## 🚀 Features

### **Multi-Channel Detection**
- **Email Analysis** - Phishing detection with advanced NLP
- **Social Media** - Scam post and fake profile detection
- **Bank Transactions** - Fraudulent payment detection
- **Web Pages** - Phishing site detection
- **Messaging Apps** - Scam message detection
- **Voice Calls** - Phone scam detection

### **Advanced AI/ML Capabilities**
- **Hugging Face Models** - Pre-trained transformers for fraud detection
- **Machine Learning Models** - Random Forest, Gradient Boosting
- **Deep Learning** - LSTM, Bidirectional layers (when TensorFlow available)
- **Natural Language Processing** - Comprehensive text analysis
- **Real-time Processing** - Instant threat assessment
- **Multi-modal Fusion** - Combined analysis across channels

### **Enhanced NLP Processing** 🧠
The system now includes comprehensive **Natural Language Processing** capabilities:

#### **Linguistic Pattern Analysis**
- **Urgency Indicators** - Detects urgent language patterns
- **Authority Indicators** - Identifies fake authority claims
- **Financial Pressure** - Recognizes debt/payment threats
- **Reward Indicators** - Spots fake prize/giveaway language
- **Personal Information Requests** - Detects SSN/credit card requests
- **Emotional Manipulation** - Identifies family/emergency manipulation
- **Action Verbs** - Recognizes suspicious verification requests

#### **Entity Recognition**
- **Organizations** - Detects fake company mentions
- **Government Entities** - Identifies fake IRS/FBI claims
- **Financial Institutions** - Recognizes fake bank references
- **Personal Names** - Extracts name patterns

#### **Sentiment Analysis**
- **Compound Sentiment** - Overall emotional tone
- **Positive/Negative/Neutral** - Detailed sentiment breakdown
- **Emotional Manipulation** - Detects emotional pressure tactics

#### **Readability & Complexity Metrics**
- **Flesch Reading Ease** - Text complexity assessment
- **Sentence Length Analysis** - Structural complexity
- **Word Complexity** - Vocabulary difficulty
- **Grammar Error Detection** - Writing quality assessment

#### **Text Pattern Analysis**
- **URL Detection** - Identifies suspicious links
- **Phone Number Patterns** - Extracts contact information
- **Email Patterns** - Recognizes email addresses
- **Currency Patterns** - Detects monetary amounts
- **Time Pressure** - Identifies deadline language

## 🏗️ Architecture

### **Backend (Flask)**
```
📧 Email → 🧠 NLP Analysis → 🤖 ML Model → ⚠️ Risk Score
💳 Transaction → 🤖 ML Model → ⚠️ Risk Score  
📱 Social Media → 🧠 NLP Analysis → 🤖 ML Model → ⚠️ Risk Score
```

### **Frontend (React Dashboard)**
- **Real-time monitoring** of all channels
- **Risk score visualization** and trends
- **Alert management** and recommendations
- **Performance metrics** for each model

## 🎯 How It Works

### **1. Multi-Channel Input**
The system analyzes data from multiple sources:
- **Emails** (phishing detection with NLP)
- **Social Media** (scam posts, fake profiles with linguistic analysis)
- **Bank Transactions** (fraudulent payments)
- **Web Pages** (phishing sites)
- **Messaging Apps** (scam messages)
- **Voice Calls** (phone scams)

### **2. Advanced AI/ML Processing**
For each input, the system:
- **Extracts comprehensive features** using NLP and ML
- **Uses trained ML models** to predict risk scores
- **Combines multiple signals** for better accuracy
- **Generates detailed alerts** with linguistic analysis

### **3. Three Types of AI Models**
- **Email Classifier**: Detects phishing emails using advanced NLP
- **Transaction Classifier**: Identifies fraudulent transactions using numerical patterns
- **Social Media Classifier**: Finds scam posts and fake profiles using linguistic analysis

## 🔧 Technical Architecture

### **Hugging Face Integration** 🤖
The system now uses **pre-trained Hugging Face models** to reduce deployment size and improve accuracy:

#### **Models Used**
- **`cardiffnlp/twitter-roberta-base-sentiment-latest`** - Sentiment analysis
- **`microsoft/DialoGPT-medium`** - Text classification for fraud detection
- **`dslim/bert-base-NER`** - Named Entity Recognition
- **`facebook/bart-large-mnli`** - Zero-shot classification
- **`ProsusAI/finbert`** - Financial text analysis (optional)
- **`j-hartmann/emotion-english-distilroberta-base`** - Emotion detection (optional)

#### **Benefits**
- **Smaller Deployment**: No need to upload large model files
- **Better Accuracy**: State-of-the-art pre-trained models
- **Faster Deploys**: Only code is deployed, models downloaded at runtime
- **Automatic Updates**: Models are always up-to-date

### **NLP Processing Pipeline**
```
Text Input → Hugging Face Models → Linguistic Analysis → Entity Recognition → Sentiment Analysis → Readability Metrics → Risk Assessment
```

### **ML Model Pipeline**
```
Features → HF Models + ML Models → Risk Score → Threat Level → Alert Generation
```

## 📊 API Endpoints

### **Analysis Endpoints**
- `POST /analyze/email` - Email analysis with NLP
- `POST /analyze/transaction` - Transaction analysis
- `POST /analyze/social_media` - Social media analysis with NLP
- `POST /analyze/multi_modal` - Combined analysis

### **NLP Analysis Endpoints** 🧠
- `POST /api/nlp/analyze` - Comprehensive NLP analysis
- `POST /api/nlp/compare` - Compare multiple texts

### **AI Management**
- `GET /api/ai/status` - AI system status
- `POST /api/ai/train` - Train models
- `POST /api/ai/save` - Save trained models
- `POST /api/ai/load` - Load saved models

### **Dashboard**
- `GET /dashboard` - Main dashboard
- `GET /api/dashboard/stats` - Real-time statistics
- `GET /api/dashboard/alerts` - Recent alerts

## 🎯 Real-World Example

**Scenario**: Someone receives a suspicious email
```
📧 Email: "URGENT: Your account is suspended. Click here to verify!"
🧠 NLP Analysis: 
   - Urgency indicators: 2 ✓
   - Authority claims: 1 ✓
   - Financial pressure: 1 ✓
   - Personal info requests: 1 ✓
   - Sentiment: Negative ✓
   - Readability: Low (suspicious) ✓
⚠️ Result: 85% risk score, HIGH threat level
💡 Recommendation: "Do not click links. Contact bank directly."
```

## 🔄 Current Status
- ✅ **All 3 ML models trained** (Email, Transaction, Social Media)
- ✅ **Enhanced NLP processing** with linguistic analysis
- ✅ **100% accuracy** on training data
- ✅ **Real-time processing** working
- ✅ **Dashboard** showing live statistics
- ✅ **API endpoints** ready for use

## 🎉 Benefits

### **Proactive Protection**
- **Advanced NLP Detection**: Identifies subtle linguistic fraud patterns
- **Multi-Channel Coverage**: Monitors all communication channels
- **AI-Powered Accuracy**: Learns and improves over time
- **Real-time Alerts**: Instant notifications of suspicious activity
- **User-Friendly**: Easy-to-understand risk scores and recommendations

### **Enhanced NLP Capabilities**
- **Linguistic Pattern Recognition**: Detects fraud-specific language
- **Entity Recognition**: Identifies fake organizations and authorities
- **Sentiment Analysis**: Understands emotional manipulation
- **Readability Assessment**: Evaluates text complexity and quality
- **Multi-text Comparison**: Compares multiple texts for risk assessment

## 🚀 Getting Started

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Test Hugging Face AI System (Optional)**
```bash
python test_huggingface_ai.py
```

### **3. Start the Platform**
```bash
python app.py
```

### **4. Access the Dashboard**
- **Dashboard**: http://localhost:5000/dashboard
- **API**: http://localhost:5000
- **Test**: http://localhost:5000/test

### **5. Train Models (Optional)**
```bash
python train_models.py
```

## 🧠 NLP Analysis Examples

### **Comprehensive Text Analysis**
```python
import requests

response = requests.post('http://localhost:5000/api/nlp/analyze', json={
    'text': 'URGENT: Your account is SUSPENDED! Click here to verify!',
    'type': 'comprehensive'
})

result = response.json()
print(f"Risk Level: {result['analysis']['risk_level']}")
print(f"Fraud Indicators: {result['analysis']['fraud_indicators']['total_fraud_indicators']}")
print(f"Sentiment: {result['analysis']['sentiment_analysis']['compound']}")
```

### **Multi-text Comparison**
```python
response = requests.post('http://localhost:5000/api/nlp/compare', json={
    'texts': [
        'URGENT: Your account is SUSPENDED!',
        'Thank you for your purchase.',
        '🎉 WIN FREE iPhone! Share this post!'
    ]
})

comparisons = response.json()['comparisons']
for comp in comparisons:
    print(f"Risk: {comp['risk_score']:.1f}% - {comp['text_preview']}")
```

## 📈 Performance Metrics

The system provides comprehensive performance tracking:
- **Model Accuracy**: Real-time accuracy metrics
- **Processing Speed**: Analysis time measurements
- **Risk Distribution**: Threat level statistics
- **Channel Performance**: Per-channel effectiveness
- **NLP Feature Analysis**: Linguistic pattern effectiveness

This system essentially acts as a **smart security guard** that watches over all your digital communications and financial transactions, using advanced **AI, ML, and NLP** to spot patterns that humans might miss! 