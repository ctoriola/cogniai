@echo off
echo.
echo ========================================
echo 🚨 Omni-Channel AI Scam & Fraud Detection Platform
echo ========================================
echo.

echo 📦 Installing dependencies...
pip install flask==2.3.3 flask-cors==4.0.0 requests==2.31.0

echo.
echo 🚀 Starting the platform...
echo.
echo 📊 API Server: http://localhost:5000
echo 🧪 Test API: http://localhost:5000/test
echo 📈 Dashboard: http://localhost:5000/dashboard
echo 🌐 Home: http://localhost:5000/
echo.
echo 💡 Press Ctrl+C to stop the server
echo.

python app.py

pause 