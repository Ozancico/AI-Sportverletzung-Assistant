# 🚀 Schnellstart-Anleitung

## In 5 Minuten zum laufenden AI-Sportverletzung-Assistant

### 1. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 2. Environment konfigurieren
```bash
cp .env.example .env
```

Bearbeiten Sie die `.env` Datei und fügen Sie Ihren OpenAI API Key hinzu:
```
OPENAI_API_KEY=ihr_echter_api_key_hier
```

### 3. Anwendung starten
```bash
python run.py
```

### 4. Im Browser öffnen
```
http://localhost:5000
```

## 🎯 Erste Schritte

1. **Testen Sie die Schnellfragen** in der Sidebar
2. **Stellen Sie eine eigene Frage** über das Chat-Interface
3. **Schauen Sie sich den Chat-Verlauf** an

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "OpenAI API Key nicht gefunden"
- Überprüfen Sie die `.env` Datei
- Stellen Sie sicher, dass der API Key korrekt ist

### "Port 5000 bereits belegt"
```bash
# Anderen Port verwenden
python app.py --port 5001
```

## 📱 Features testen

- ✅ Chat-Interface
- ✅ Schnellfragen
- ✅ Chat-Verlauf
- ✅ Responsive Design
- ✅ AI-Antworten

## 🆘 Hilfe benötigt?

Schauen Sie in die [README.md](README.md) für detaillierte Informationen.
