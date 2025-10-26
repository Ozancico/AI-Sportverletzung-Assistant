from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid
from openai import OpenAI
import openai
import requests
import logging
from logging.handlers import RotatingFileHandler
import time
from collections import deque

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportverletzung_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Logging Setup ---
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.log')
if not os.path.exists(LOG_FILE):
    # create empty file
    with open(LOG_FILE, 'a'):
        pass

root_logger = logging.getLogger()
if not root_logger.handlers:
    root_logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    root_logger.addHandler(file_handler)
    # keep Flask default console logs as-is

# Provider-Konfiguration (OpenAI, Hugging Face, Cohere)
USE_LOCAL = os.getenv('USE_LOCAL', '0') == '1'
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# Hugging Face
PROVIDER = os.getenv('PROVIDER', '').lower()
USE_HF = os.getenv('USE_HF', '0').lower() in ['1', 'true', 'yes'] or PROVIDER == 'huggingface'
HF_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
HF_MODEL = os.getenv('HF_MODEL', 'dbmdz/german-gpt2')

# Cohere
USE_COHERE = os.getenv('USE_COHERE', '0').lower() in ['1', 'true', 'yes'] or PROVIDER == 'cohere'
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
COHERE_MODEL = os.getenv('COHERE_MODEL', 'command-r-plus')

# OpenAI-Client initialisieren (immer verfügbar)
if USE_LOCAL or OPENAI_BASE_URL:
    # Lokaler/OpenAI-kompatibler Endpoint (z. B. Ollama unter http://localhost:11434/v1)
    client = OpenAI(
        base_url=OPENAI_BASE_URL or 'http://localhost:11434/v1',
        api_key=os.getenv('OPENAI_API_KEY', 'ollama')
    )
else:
    # Standard: OpenAI Cloud
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
Du bist eine freundliche, respektvolle und nicht-diskriminierende KI, die sich ausschließlich auf **Sportverletzungen** spezialisiert.  
Deine Aufgabe ist es, Menschen dabei zu helfen, Verletzungen aus Sport, Bewegung oder Training besser zu verstehen – auf eine sichere, empathische und sachlich fundierte Weise.

🩺 **Regeln & Verhalten:**
1. Du beantwortest **nur** Fragen zu Sportverletzungen, sportbedingten Schmerzen oder Beschwerden, Reha und Prävention.  
2. Wenn eine Frage **nicht** mit Sportverletzungen zu tun hat, antworte höflich:
   > „Ich bin auf Sportverletzungen spezialisiert – bitte stelle eine Frage zu diesem Thema."  
3. Du gibst **keine individuellen Diagnosen**, verschreibst **keine Medikamente oder Rezepte** und stellst **keine Behandlungspläne** auf.  
4. Du erklärst **nur allgemeine Informationen**, typische Symptome, Ursachen, Prävention und Reha-Prinzipien.  
5. Du bleibst **neutral, respektvoll und inklusiv**. Keine diskriminierende, wertende oder geschlechtsspezifische Sprache.  
6. Verwende **klare, freundliche und leicht verständliche Sprache** – wie ein sportmedizinischer Coach, nicht wie ein Arzt.  
7. Kein Smalltalk, keine Themen außerhalb des Sports, keine psychologischen oder ernährungsbezogenen Ratschläge.  

🧩 **Struktur deiner Antworten (wenn passend):**
- **Mögliche Ursache:** kurze allgemeine Erklärung  
- **Typische Symptome:** Stichpunkte oder kurze Beschreibung  
- **Was du tun kannst:** allgemeine Empfehlungen, Selbsthilfemaßnahmen, wann ärztliche Abklärung sinnvoll ist  
- **Prävention:** Tipps zu Aufwärmen, Technik, Trainingsgestaltung  

Dein Ziel:  
Hilf den Nutzer*innen, Sportverletzungen besser zu verstehen, deren Ursachen zu erkennen und vorzubeugen – **ohne medizinische Beratung zu ersetzen.**

**Sicherheitshinweise:**
- Gib **niemals** medizinische Diagnosen, Medikamentennamen, Dosierungen oder Therapieanweisungen.  
- Wenn jemand nach Medikamenten, Salben, Rezepten oder Behandlungsplänen fragt, antworte höflich:
  > „Ich kann keine medizinischen oder pharmazeutischen Empfehlungen geben. Bitte wende dich an eine medizinische Fachperson."  
- Verwende stets **inklusive, respektvolle Sprache** (z. B. „Sportler*innen", „Betroffene Person").  
- Achte auf einen **positiven, unterstützenden und sachlichen Ton**.  
- Wenn du unsicher bist, erinnere die Person daran, dass du keine medizinische Beratung ersetzt.  

**Beispiele für Selbsthilfe-Empfehlungen:**
- RICE-Methode (Rest, Ice, Compression, Elevation)
- Dehnübungen und sanfte Bewegungen
- Schonung und Pausierung
- Wann ein Arzt aufgesucht werden sollte
- Aufwärm- und Cool-Down-Übungen
"""

### --- Simple in-memory rate limiting ---
RATE_LIMIT_MAX = int(os.getenv('RATE_LIMIT_MAX', '10'))  # max requests
RATE_LIMIT_WINDOW_SEC = int(os.getenv('RATE_LIMIT_WINDOW_SEC', '60'))  # per window seconds
user_request_timestamps = {}

def rate_limited(user_key: str) -> bool:
    """Returns True if the user is currently rate limited."""
    now = time.time()
    dq = user_request_timestamps.get(user_key)
    if dq is None:
        dq = deque()
        user_request_timestamps[user_key] = dq
    # purge old timestamps
    while dq and now - dq[0] > RATE_LIMIT_WINDOW_SEC:
        dq.popleft()
    if len(dq) >= RATE_LIMIT_MAX:
        return True
    dq.append(now)
    return False

def get_client_ip():
    # simple IP retrieval; behind proxies consider X-Forwarded-For
    return request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown')

def moderate_text_openai(text: str) -> tuple[bool, str]:
    """Return (is_blocked, reason). If OpenAI moderation unavailable, return (False, '')."""
    try:
        # Using OpenAI Moderations (if key present)
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return False, ''
        # Older v1/moderations style via client.moderations
        moderation = client.moderations.create(model="omni-moderation-latest", input=text)
        result = moderation.results[0]
        if getattr(result, 'flagged', False):
            return True, 'Content flagged by moderation.'
        return False, ''
    except Exception:
        # do not block on moderation errors
        return False, ''

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

def _format_history_as_messages(history_items):
    """Hilfsfunktion: Konvertiert gespeicherte Historie in Chat-Nachrichten."""
    messages = []
    for item in history_items:
        # Reihenfolge: zuerst Nutzerfrage, dann Assistentenantwort
        if item.question:
            messages.append({"role": "user", "content": item.question})
        if item.answer:
            messages.append({"role": "assistant", "content": item.answer})
    return messages

def _format_history_as_prompt(system_prompt, history_messages, new_user_question):
    """Hilfsfunktion: Baut einen zusammenhängenden Prompt für nicht-Chat-APIs (HF/Cohere-Fallback)."""
    lines = [system_prompt.strip(), "", "Verlauf:"]
    for m in history_messages:
        role = m.get("role", "user")
        content = (m.get("content") or "").strip()
        if not content:
            continue
        prefix = "Nutzer" if role == "user" else "Assistent"
        lines.append(f"{prefix}: {content}")
    lines.append("")
    lines.append(f"Nutzerfrage: {new_user_question.strip()}")
    lines.append("Antwort:")
    return "\n".join(lines)

def get_ai_response(question, user_language='de', history_items=None):
    """Antwort des konfigurierten KI-Providers abrufen."""
    history_items = history_items or []
    history_messages = _format_history_as_messages(history_items)
    # Hugging Face Inference API
    if USE_HF:
        if not HF_API_KEY:
            return (
                "Hugging Face API-Key fehlt. Bitte setzen Sie 'HUGGINGFACE_API_KEY' in der .env-Datei."
            )
        api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        # Für reine Textgeneratoren kombinieren wir Systemhinweis + Verlauf + Nutzerfrage
        prompt = _format_history_as_prompt(SPORT_INJURY_SYSTEM_PROMPT, history_messages, question)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 400,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 401:
                return (
                    "Hugging Face Authentifizierungsfehler (401). Bitte API-Key prüfen."
                )
            if resp.status_code == 429:
                return (
                    "Hugging Face Rate-Limit erreicht (429). Bitte später erneut versuchen."
                )
            if not resp.ok:
                return (
                    f"Hugging Face Fehler: {resp.status_code}. Bitte später erneut versuchen."
                )
            data = resp.json()
            # Mögliche Antwortformate: [{"generated_text": "..."}] oder {"error": "..."}
            if isinstance(data, dict) and data.get("error"):
                return "Hugging Face Antwortfehler: " + str(data.get("error"))
            if isinstance(data, list) and data and isinstance(data[0], dict):
                text = data[0].get("generated_text") or data[0].get("summary_text")
                if text:
                    return text.strip()
            # Fallback
            return "Die Antwort des Modells konnte nicht interpretiert werden."
        except Exception:
            return "Es ist ein technischer Fehler (Hugging Face) aufgetreten. Bitte später erneut versuchen."

    # Cohere API
    if USE_COHERE:
        if not COHERE_API_KEY:
            return (
                "Cohere API-Key fehlt. Bitte setzen Sie 'COHERE_API_KEY' in der .env-Datei."
            )
        try:
            import cohere  # optionaler Import, nur falls konfiguriert
            co = cohere.Client(api_key=COHERE_API_KEY)
            # Prompt mit Verlauf
            prompt = _format_history_as_prompt(SPORT_INJURY_SYSTEM_PROMPT, history_messages, question)
            # Neuere Cohere SDKs nutzen Chat
            try:
                chat_resp = co.chat(model=COHERE_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.7)
                # SDK-Formate variieren leicht nach Version
                text = getattr(chat_resp, 'text', None) or getattr(chat_resp, 'message', None)
                if isinstance(text, str) and text.strip():
                    return text.strip()
                # Manche Versionen liefern 'output_text'
                text_alt = getattr(chat_resp, 'output_text', None)
                if isinstance(text_alt, str) and text_alt.strip():
                    return text_alt.strip()
            except Exception:
                # Fallback auf generieren
                gen = co.generate(prompt=prompt, model=COHERE_MODEL, max_tokens=500, temperature=0.7)
                generations = getattr(gen, 'generations', None)
                if generations and len(generations) > 0 and getattr(generations[0], 'text', None):
                    return generations[0].text.strip()
            return "Die Antwort des Cohere-Modells konnte nicht interpretiert werden."
        except Exception:
            return "Es ist ein technischer Fehler (Cohere) aufgetreten. Bitte später erneut versuchen."

    # OpenAI (Standard)
    try:
        # Debug: API-Key prüfen
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"API Key vorhanden: {bool(api_key)}")
        print(f"API Key Länge: {len(api_key) if api_key else 0}")
        
        # Nachrichten: System + Verlauf + aktuelle Frage
        messages = [{"role": "system", "content": SPORT_INJURY_SYSTEM_PROMPT}] + history_messages + [
            {"role": "user", "content": question}
        ]
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except openai.APIStatusError as e:
        code = getattr(e, 'status_code', None)
        if code == 401:
            return (
                "Leider konnte Ihre Anfrage nicht verarbeitet werden (Auth-Fehler).\n"
                "Bitte prüfen Sie den API-Key in der .env-Datei."
            )
        if code == 429:
            return (
                "Aktuell ist das API-Kontingent erschöpft (429).\n"
                "Bitte Billing prüfen oder später erneut versuchen."
            )
        return "Ein unerwarteter API-Fehler ist aufgetreten. Bitte später erneut versuchen."
    except Exception as e:
        print(f"OpenAI API Fehler: {e}")  # Debug-Ausgabe
        return f"Es ist ein technischer Fehler aufgetreten: {str(e)}"

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
    
    # Rate limit: key per session + IP
    client_ip = get_client_ip()
    rl_key = f"{user.user_id}:{client_ip}"
    if rate_limited(rl_key):
        logging.warning(f"Rate limit exceeded for {rl_key}")
        return jsonify({'error': 'Zu viele Anfragen. Bitte kurz warten.'}), 429
    
    # Moderation
    is_blocked, reason = moderate_text_openai(question)
    if is_blocked:
        logging.info(f"Prompt blocked by moderation: {reason}")
        return jsonify({'error': 'Die Anfrage wurde aus Moderationsgründen blockiert.'}), 400
    
    # Historie laden (letzte 10 Einträge in chronologischer Reihenfolge)
    history_items = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.timestamp.asc()).limit(10).all()
    
    # Generate AI response mit Verlauf
    answer = get_ai_response(question, user.language, history_items)
    
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
