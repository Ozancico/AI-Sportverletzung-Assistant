# 🏋️‍♂️ AI-Sportverletzung-Assistant

Ein intelligenter Chatbot, der Sportlern bei Fragen zu sportlichen Verletzungen hilft und erste Einschätzungen sowie Selbsthilfe-Empfehlungen bietet.

## 📋 Projektübersicht

Der AI-Sportverletzung-Assistant ist eine Web-Anwendung, die mithilfe von OpenAI's GPT-Modell spezialisierte Beratung für Sportverletzungen anbietet. Die Anwendung ist darauf ausgelegt, schnelle und zugängliche Hilfestellung für Hobbysportler und Athleten zu bieten.

### ⚠️ Wichtiger Hinweis
**Dieser Assistant ersetzt keine ärztliche Beratung!** Bei ernsten Symptomen sollten Sie immer einen Arzt aufsuchen.

## 🚀 Features

- **Intelligente Beratung**: AI-gestützte Antworten zu Sportverletzungen
- **Selbsthilfe-Empfehlungen**: RICE-Methode, Dehnübungen, Schonung
- **Chat-Verlauf**: Speicherung und Anzeige vorheriger Unterhaltungen
- **Responsive Design**: Funktioniert auf Desktop und Mobile
- **Schnellfragen**: Vordefinierte Fragen für häufige Probleme
- **Mehrsprachig**: Optimiert für deutsche Sprache

## 🛠️ Technologie-Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Datenbank**: SQLite
- **AI**: OpenAI GPT-3.5-turbo
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome

## 📦 Installation

### Voraussetzungen
- Python 3.8 oder höher
- OpenAI API Key

### Schritt-für-Schritt Anleitung

1. **Repository klonen**
   ```bash
   git clone https://github.com/ihr-username/ai-sportverletzung-assistant.git
   cd ai-sportverletzung-assistant
   ```

2. **Virtuelles Environment erstellen**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # oder
   .venv\Scripts\activate     # Windows
   ```

3. **Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables konfigurieren**
   ```bash
   cp .env.example .env
   ```
   
   Bearbeiten Sie die `.env` Datei und fügen Sie Ihren OpenAI API Key hinzu:
   ```
   OPENAI_API_KEY=ihr_openai_api_key_hier
   SECRET_KEY=ihr_sicherer_secret_key
   ```

5. **Anwendung starten**
   ```bash
   python app.py
   ```

6. **Im Browser öffnen**
   ```
   http://localhost:5000
   ```

## 🔧 Konfiguration

### Environment Variables

| Variable | Beschreibung | Erforderlich |
|----------|--------------|--------------|
| `OPENAI_API_KEY` | Ihr OpenAI API Key | ✅ Ja |
| `SECRET_KEY` | Flask Secret Key für Sessions | ✅ Ja |
| `FLASK_DEBUG` | Debug Mode (True/False) | ❌ Nein |

### OpenAI API Key erhalten

1. Besuchen Sie [OpenAI Platform](https://platform.openai.com/)
2. Erstellen Sie ein Konto oder loggen Sie sich ein
3. Gehen Sie zu "API Keys"
4. Erstellen Sie einen neuen API Key
5. Kopieren Sie den Key in Ihre `.env` Datei

## 📊 Datenbank Schema

```sql
-- User Tabelle
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(100),
    language VARCHAR(10) DEFAULT 'de',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Chat History Tabelle
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    chat_id VARCHAR(36) NOT NULL,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

## 🎯 Verwendung

### Chat-Interface
1. Öffnen Sie die Anwendung im Browser
2. Beschreiben Sie Ihre Sportverletzung oder stellen Sie eine Frage
3. Der AI-Assistant wird eine strukturierte Antwort geben
4. Bei Unsicherheit wird zur ärztlichen Untersuchung geraten

### Schnellfragen
Nutzen Sie die vordefinierten Schnellfragen für häufige Probleme:
- Knieschmerzen nach dem Laufen
- Geschwollenes Sprunggelenk
- Muskelkater
- Rückenschmerzen nach dem Training

### Chat-Verlauf
Alle Unterhaltungen werden automatisch gespeichert und können über den "Verlauf"-Button eingesehen werden.

## ��️ Projektstruktur

```
ai-sportverletzung-assistant/
├── app.py                 # Haupt-Flask-Anwendung
├── requirements.txt       # Python Dependencies
├── .env.example          # Environment Variables Template
├── .env                  # Environment Variables (nicht in Git)
├── .gitignore           # Git Ignore Rules
├── README.md            # Diese Datei
├── templates/           # HTML Templates
│   ├── index.html       # Hauptseite
│   └── history.html     # Chat-Verlauf Seite
└── static/             # Statische Dateien
    ├── css/
    │   └── style.css    # Custom Styles
    └── js/
        └── chat.js      # Chat JavaScript
```

## 🔒 Sicherheit

- API Keys werden in `.env` Dateien gespeichert (nicht in Git)
- Session-basierte Benutzerverwaltung
- Input-Validierung und Sanitization
- Keine Speicherung sensibler medizinischer Daten

## 🚀 Deployment

### Lokale Entwicklung
```bash
python app.py
```

### Produktions-Deployment
Für Produktions-Deployment empfehlen wir:
- Gunicorn als WSGI Server
- Nginx als Reverse Proxy
- PostgreSQL als Datenbank
- HTTPS mit SSL-Zertifikat

Beispiel Gunicorn Konfiguration:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Beitragen

1. Fork das Repository
2. Erstellen Sie einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📝 Lizenz

Dieses Projekt steht unter der MIT Lizenz. Siehe `LICENSE` Datei für Details.

## 🆘 Support

Bei Problemen oder Fragen:
1. Überprüfen Sie die [Issues](https://github.com/ihr-username/ai-sportverletzung-assistant/issues)
2. Erstellen Sie ein neues Issue mit detaillierter Beschreibung
3. Kontaktieren Sie uns über [E-Mail](mailto:support@example.com)

## 🗺️ Roadmap

### Version 1.1
- [ ] Mehrsprachige Unterstützung (EN, FR, ES)
- [ ] Erweiterte Schnellfragen
- [ ] Export-Funktion für Chat-Verlauf

### Version 1.2
- [ ] RAG-Integration für medizinische Quellen
- [ ] Benutzer-Authentifizierung
- [ ] Mobile App (React Native)

### Version 2.0
- [ ] Integration mit Fitness-Trackern
- [ ] Präventive Beratung
- [ ] Community-Features

## 📊 Statistiken

- **Entwicklungszeit**: 3 Monate
- **Starttermin**: 01.09.2025
- **Geplantes Ende**: 01.12.2025
- **Programmiersprache**: Python, JavaScript
- **Framework**: Flask

## 🙏 Danksagungen

- OpenAI für die GPT API
- Bootstrap für das CSS Framework
- Font Awesome für die Icons
- Flask Community für das Web Framework

---

**Entwickelt mit ❤️ für die Sport-Community**
