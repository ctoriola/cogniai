from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models.lightweight_ai import LightweightAI
from models.user import db, User
import os
import urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
# Use Railway Postgres if available, fallback to SQLite for local dev

import os
print("RAW DATABASE_URL:", repr(os.environ.get('DATABASE_URL')))
db_url = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=["*"])
db.init_app(app)
ai = LightweightAI()

with app.app_context():
    db.create_all()
    print("Tables created! Using database:", app.config['SQLALCHEMY_DATABASE_URI'])
    # Print user table schema for confirmation
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = inspector.get_columns('user')
    print("User table columns:")
    for col in columns:
        print(f"  {col['name']}: {col['type']}")

import os
print("ENV VARS:", dict(os.environ))

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

@app.route('/admin/create', methods=['POST'])
def create_admin():
    """Create an admin user (first admin only)"""
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    # Check if any admin exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        return jsonify({'error': 'Admin user already exists'}), 403
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=data['username'], is_admin=True)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Admin user created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin_user()
        return jsonify({
            'message': 'Login successful',
            'is_admin': user.is_admin_user()
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return jsonify({'message': 'Logged out'})

@app.route('/user/data', methods=['GET', 'POST'])
def user_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user = db.session.get(User, session['user_id'])
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

# --- Admin Dashboard Endpoints ---
@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard - requires admin privileges"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin_user():
        return jsonify({'error': 'Admin access required'}), 403
    
    return render_template('admin_dashboard.html')

@app.route("/admin/api/health")
def admin_api_health():
    """Admin endpoint to check API health - requires admin privileges"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin_user():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    # Check AI model
    try:
        test_result = ai.analyze_email("Test email")
        ai_status = "Working"
    except Exception as e:
        ai_status = f"Error: {str(e)}"
    
    return jsonify({
        "database": db_status,
        "ai_model": ai_status,
        "timestamp": datetime.now().isoformat(),
        "uptime": "Running"
    })

@app.route("/admin/api/user-stats")
def admin_user_stats():
    """Admin endpoint to get user statistics - requires admin privileges"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin_user():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        total_users = User.query.count()
        
        # Get recent signups (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_signups = User.query.filter(User.id >= 1).count()  # Simplified for now
        
        # Get user activity (users with data)
        active_users = User.query.filter(User.data.isnot(None)).count()
        
        # Get admin count
        admin_count = User.query.filter_by(is_admin=True).count()
        
        return jsonify({
            "total_users": total_users,
            "recent_signups": recent_signups,
            "active_users": active_users,
            "admin_users": admin_count,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)