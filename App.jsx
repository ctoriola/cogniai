import React, { useState } from 'react';
import './App.css';

function App() {
  const [emailContent, setEmailContent] = useState('');
  const [transactionData, setTransactionData] = useState({
    amount: 0,
    frequency: 1,
    location_variance: 0,
    timestamp: new Date().toISOString()
  });
  const [results, setResults] = useState({});
  const [correlation, setCorrelation] = useState(null);

  const analyzeEmail = async () => {
    const response = await fetch('http://localhost:5000/analyze/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: emailContent })
    });
    const data = await response.json();
    setResults(prev => ({ ...prev, email: data }));
  };

  const analyzeTransaction = async () => {
    const response = await fetch('http://localhost:5000/analyze/transaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(transactionData)
    });
    const data = await response.json();
    setResults(prev => ({ ...prev, transaction: data }));
  };

  const correlateEvents = async () => {
    const response = await fetch('http://localhost:5000/correlate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ events: results })
    });
    const data = await response.json();
    setCorrelation(data);
  };

  return (
    <div className="dashboard">
      <h1>Omni-Channel Fraud Detection</h1>
      
      <div className="channel-section">
        <h2>Email Analysis</h2>
        <textarea
          value={emailContent}
          onChange={e => setEmailContent(e.target.value)}
          placeholder="Paste email content"
          rows={6}
        />
        <button onClick={analyzeEmail}>Analyze Email</button>
        
        {results.email && (
          <div className={`result-card ${results.email.risk_score > 0.7 ? 'high-risk' : 'low-risk'}`}>
            <h3>Email Analysis Result</h3>
            <p>Risk Score: <strong>{results.email.risk_score.toFixed(4)}</strong></p>
            <p>Sentiment: {results.email.sentiment} ({results.email.sentiment_score.toFixed(2)})</p>
            <div>
              <h4>Key Risk Indicators:</h4>
              <ul>
                {results.email.top_risk_features.map(([token, score], i) => (
                  <li key={i}>{token}: {score.toFixed(4)}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      <div className="channel-section">
        <h2>Transaction Analysis</h2>
        <div className="input-group">
          <label>Amount:</label>
          <input 
            type="number" 
            value={transactionData.amount}
            onChange={e => setTransactionData({...transactionData, amount: parseFloat(e.target.value)})}
          />
        </div>
        <div className="input-group">
          <label>Frequency (txn/hr):</label>
          <input 
            type="number" 
            value={transactionData.frequency}
            onChange={e => setTransactionData({...transactionData, frequency: parseFloat(e.target.value)})}
          />
        </div>
        <button onClick={analyzeTransaction}>Analyze Transaction</button>
        
        {results.transaction && (
          <div className={`result-card ${results.transaction.is_fraud ? 'high-risk' : 'low-risk'}`}>
            <h3>Transaction Analysis</h3>
            <p>Anomaly Score: <strong>{results.transaction.anomaly_score.toFixed(4)}</strong></p>
            <p>Fraud Detected: {results.transaction.is_fraud ? 'YES' : 'NO'}</p>
            <div>
              <h4>Feature Importance:</h4>
              <ul>
                {Object.entries(results.transaction.feature_importance).map(([feature, importance]) => (
                  <li key={feature}>{feature}: {importance.toFixed(4)}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      <div className="correlation-section">
        <button onClick={correlateEvents}>Correlate Events</button>
        
        {correlation && (
          <div className="result-card">
            <h3>Multi-Channel Correlation</h3>
            <p>Combined Risk Score: <strong>{correlation.combined_risk_score.toFixed(4)}</strong></p>
            <p>Channels Correlated: {correlation.correlated_events.join(', ')}</p>
            <div>
              <h4>Reasons:</h4>
              <ul>
                {correlation.reasons.map((reason, i) => (
                  <li key={i}>{reason}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;