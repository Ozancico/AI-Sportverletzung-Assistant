from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportverletzung_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Init OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default='de')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Sport injury specific prompts
SPORT_INJURY_SYSTEM_PROMPT = """
Du bist ein spezialisierter AI-Assistent für Sportverletzungen. Deine Aufgabe ist es, Nutzern bei Fragen zu sportlichen Verletzungen zu helfen.

WICHTIGE HINWEISE:
- Du stellst KEINE medizinischen Diagnosen
- Du ersetzt KEINEN Arztbesuch
- Bei ernsten Symptomen verweist du IMMER an einen Arzt
- Du gibst nur allgemeine Empfehlungen und erste Einschätzungen

Deine Antworten sollten:
1. Professionell und hilfreich sein
2. Auf Deutsch verfasst werden
3. Erste Einschätzungen geben
4. Selbsthilfe-Empfehlungen anbieten (Dehnung, Schonung, Eis, etc.)
5. Bei Unsicherheit zur ärztlichen Untersuchung raten
6. Strukturiert und verständlich formuliert sein

Beispiele für Selbsthilfe-Empfehlungen:
- RICE-Methode (Rest, Ice, Compression, Elevation)
- Dehnübungen
- Schonung
- Schmerzmittel (mit Hinweis auf Packungsbeilage)
- Wann ein Arzt aufgesucht werden sollte
"""

def get_or_create_user():
    """Get or create a user based on the session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user = User.query.filter_by(user_id=session['user_id']).first()
    if not user:
        user = User(user_id=session['user_id'], language='de')
        db.session.add(user)
        db.session.commit()
    
    return user

def get_ai_response(question, user_language='de'):
    """Get a response from the OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SPORT_INJURY_SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage: {str(e)}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for AI conversations"""
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Bitte geben Sie eine Frage ein.'}), 400
    
    # Get or create user
    user = get_or_create_user()
    
    # Generate AI response
    answer = get_ai_response(question, user.language)
    
    # Save chat history
    chat_id = str(uuid.uuid4())
    chat_history = ChatHistory(
        chat_id=chat_id,
        user_id=user.id,
        question=question,
        answer=answer
    )
    db.session.add(chat_history)
    db.session.commit()
    
    return jsonify({
        'answer': answer,
        'chat_id': chat_id,
        'timestamp': chat_history.timestamp.isoformat()
    })

@app.route('/history')
def history():
    """Display chat history"""
    user = get_or_create_user()
    chat_histories = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.timestamp.desc()).limit(20).all()
    
    return render_template('history.html', chat_histories=chat_histories)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, host='0.0.0.0', port=port)
