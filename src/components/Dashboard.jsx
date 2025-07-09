import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { AlertTriangle, Shield, Activity, TrendingUp, Users, DollarSign, Mail, CreditCard } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalAlerts: 0,
    highRiskAlerts: 0,
    emailAlerts: 0,
    transactionAlerts: 0,
    totalLoss: 0,
    preventedLoss: 0
  });
  
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [riskTrend, setRiskTrend] = useState([]);
  const [channelDistribution, setChannelDistribution] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, alertsRes, trendRes, distributionRes] = await Promise.all([
        axios.get('/api/dashboard/stats'),
        axios.get('/api/dashboard/recent-alerts'),
        axios.get('/api/dashboard/risk-trend'),
        axios.get('/api/dashboard/channel-distribution')
      ]);

      setStats(statsRes.data);
      setRecentAlerts(alertsRes.data);
      setRiskTrend(trendRes.data);
      setChannelDistribution(distributionRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk >= 0.8) return '#ef4444';
    if (risk >= 0.6) return '#f59e0b';
    return '#10b981';
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Fraud Detection Dashboard</h1>
        <div className="last-updated">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon high-risk">
            <AlertTriangle size={24} />
          </div>
          <div className="metric-content">
            <h3>Total Alerts</h3>
            <p className="metric-value">{stats.totalAlerts}</p>
            <p className="metric-change positive">+12% from yesterday</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon critical">
            <Shield size={24} />
          </div>
          <div className="metric-content">
            <h3>High Risk Alerts</h3>
            <p className="metric-value">{stats.highRiskAlerts}</p>
            <p className="metric-change negative">+5% from yesterday</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon email">
            <Mail size={24} />
          </div>
          <div className="metric-content">
            <h3>Email Alerts</h3>
            <p className="metric-value">{stats.emailAlerts}</p>
            <p className="metric-change positive">-8% from yesterday</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon transaction">
            <CreditCard size={24} />
          </div>
          <div className="metric-content">
            <h3>Transaction Alerts</h3>
            <p className="metric-value">{stats.transactionAlerts}</p>
            <p className="metric-change positive">-3% from yesterday</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon loss">
            <DollarSign size={24} />
          </div>
          <div className="metric-content">
            <h3>Total Loss</h3>
            <p className="metric-value">${stats.totalLoss.toLocaleString()}</p>
            <p className="metric-change negative">+15% from yesterday</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon prevented">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <h3>Prevented Loss</h3>
            <p className="metric-value">${stats.preventedLoss.toLocaleString()}</p>
            <p className="metric-change positive">+22% from yesterday</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <h3>Risk Trend (Last 24 Hours)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={riskTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="emailRisk" stroke="#8884d8" name="Email Risk" />
              <Line type="monotone" dataKey="transactionRisk" stroke="#82ca9d" name="Transaction Risk" />
              <Line type="monotone" dataKey="combinedRisk" stroke="#ff7300" name="Combined Risk" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3>Alert Distribution by Channel</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={channelDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {channelDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="recent-alerts">
        <h3>Recent High-Risk Alerts</h3>
        <div className="alerts-list">
          {recentAlerts.map((alert, index) => (
            <div key={index} className={`alert-item ${alert.riskLevel}`}>
              <div className="alert-header">
                <span className="alert-type">{alert.type}</span>
                <span className="alert-time">{new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
              <div className="alert-content">
                <p className="alert-description">{alert.description}</p>
                <div className="alert-metrics">
                  <span className="risk-score" style={{ color: getRiskColor(alert.riskScore) }}>
                    Risk: {alert.riskScore.toFixed(2)}
                  </span>
                  {alert.amount && (
                    <span className="amount">Amount: ${alert.amount.toLocaleString()}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 