@echo off
echo.
echo ========================================
echo 🤖 Installing Advanced AI Dependencies
echo ========================================
echo.

echo 📦 Installing basic ML libraries...
pip install numpy==1.24.3 scikit-learn==1.3.0 pandas==2.0.3 matplotlib==3.7.2 seaborn==0.12.2 joblib==1.3.1

echo.
echo 🧠 Installing Deep Learning libraries...
pip install tensorflow==2.13.0

echo.
echo 📝 Installing NLP libraries...
pip install nltk==3.8.1 transformers==4.30.2

echo.
echo 🔧 Installing spaCy...
pip install spacy==3.6.0
python -m spacy download en_core_web_sm

echo.
echo ✅ AI dependencies installed successfully!
echo.
echo 🚀 You can now run the platform with advanced AI capabilities:
echo    python app.py
echo.
pause 