from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models.lightweight_ai import LightweightAI
from models.user import db, User
import os
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
# Use Railway Postgres if available, fallback to SQLite for local dev

db_url = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=["*"])
db.init_app(app)
ai = LightweightAI()

with app.app_context():
    db.create_all()
    print("Tables created! Using database:", app.config['SQLALCHEMY_DATABASE_URI'])

@app.route("/")
def home():
    return render_template('index.html')

# --- User Authentication Endpoints ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})

@app.route('/user/data', methods=['GET', 'POST'])
def user_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.data = request.json.get('data', '')
        db.session.commit()
        return jsonify({'message': 'Data saved'})
    return jsonify({'data': user.data or ''})

# --- Fraud Detection Endpoints ---
@app.route("/analyze/email", methods=["POST"])
def analyze_email():
    try:
        data = request.json or {}
        email_content = data.get('content', '')
        result = ai.analyze_email(email_content)
        return jsonify(result)
    except Exception as e:
        print(f"Error in email analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze/transaction", methods=["POST"])
def analyze_transaction():
    try:
        data = request.json or {}
        result = ai.analyze_transaction(data)
        return jsonify(result)
    except Exception as e:
        print(f"Error in transaction analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze/social_media", methods=["POST"])
def analyze_social_media():
    try:
        data = request.json or {}
        post_content = data.get('content', '')
        result = ai.analyze_social_media(post_content)
        return jsonify(result)
    except Exception as e:
        print(f"Error in social media analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/test")
def test():
    return jsonify({"status": "API is working!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)