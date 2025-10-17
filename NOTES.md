### 🏋️‍♂️ Projekt: AI-Beratung für Sportverletzungen

- Kurzbeschreibung: Flask-Webapp mit KI-gestützter Beratung zu Sportverletzungen (DE), Chat-Verlauf, modernem UI (Dark-Mode, Avatare, Copy, Timestamps), optionalen KI-Providern.

## ⏰ Projektdaten
- Starttermin: 10.09.2024
- Voraussichtliches Enddatum: 01.12.2025
- Tatsächliches Enddatum: [später eintragen]

## 🔗 Repository
- GitHub: https://github.com/Ozancico/AI-Sportverletzung-Assistant
- Status: Öffentlich, vollständiger Code + Doku

## ✅ Projektstatus (V1)
- V1 vollständig implementiert und getestet
- Bereit für: lokale Nutzung, Präsentation, optionales Deployment

## 🧩 Features (V1)
- Chat mit Verlaufsspeicherung (SQLite)
- Dark-Mode Toggle (persistiert)
- Avatare (User/Assistant), Copy-Buttons, Timestamps
- Schnellfragen (Quick Actions)
- Rate-Limiting und Moderations-Check (optional)
- Healthcheck-Endpoint
- Provider-Flexibilität: OpenAI-kompatibel, optional Hugging Face/Cohere

## 🧱 Tech-Stack
- Backend: Flask, Flask‑SQLAlchemy, SQLite
- Frontend: Bootstrap 5, Custom CSS/JS
- KI: OpenAI SDK (kompatible Endpoints), optional HF/Cohere
- Prod-Start: Gunicorn (Procfile/Dockerfile vorhanden)

## 🗄️ Datenbank-Schema
- User: id, user_id, name, language, created_at
- ChatHistory: id, chat_id, user_id, question, answer, timestamp
- Technik: SQLite, SQLAlchemy ORM, Session-basierte Nutzer-Identifikation

## 🏗️ Architektur (Kurz)
User (Browser)
→ Frontend (HTML/CSS/JS)
→ Flask API (`/chat`, `/history`, `/api/health`)
→ KI‑Provider (OpenAI/HF/Cohere)
→ Datenbank (SQLite: User, ChatHistory)
→ [optional] Medizinische Quellen via RAG (V2)

## 📊 Vergleich (Ansätze)
| Ansatz | Vorteil | Nachteil |
| --- | --- | --- |
| ChatGPT direkt | Sehr gute Antworten | Geringe Domänenkontrolle |
| Eigene KI trainieren | Hohe Spezialisierung | Hoher Trainingsaufwand |
| Hybrider Ansatz (GPT + DB) | Gute Balance ✅ | Mehr Architektur-Komplexität |

Gewählt: Hybrider Ansatz (OpenAI-kompatibel) + SQLite

## 🖼️ Screenshots
- Platzhalter: [Später UI-Screens einfügen]

## 🎥 Demo / Folien
- Video (3–5 Min): Problem → Lösung → Live-Demo → Nächste Schritte
- Folien (3–5 Slides): Motivation, Lösung, Architektur, Demo-Bild, Roadmap

## 📚 Lernschwerpunkte
- Grundlagen KI/LLMs, NLP
- API-Integration, Prompting, strukturierte Antworten
- GenAI-Ethik (keine Diagnosen, nur Empfehlungen)
- [V2] RAG für medizinische Quellen

## 🌍 Ressourcen
- OpenAI Doku: https://platform.openai.com/docs
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- WHO Leitlinien: https://www.who.int/

## 🛣️ Roadmap & Meilensteine
V1 (erreicht)
- BA_1: Flask Backend Setup – ✅
- DB_1: SQLite/SQLAlchemy – ✅
- AI_1: OpenAI-Integration – ✅
- FE_1: Responsives Frontend + Dark-Mode – ✅
- DOC_1: README/Quickstart – ✅
- GIT_1: Öffentliches Repo – ✅

V2 (geplant)
- RAG_1: RAG für Quellenrecherche – 🔄
- AUTH_1: Nutzer-Accounts – 🔄
- MOBILE_1: Mobile App / PWA – 🔄
- API_1: REST-Doku (OpenAPI) – 🔄
- DEPLOY_1: Produktives Deployment/Monitoring – 🔄

## 🛠️ Lokale Nutzung (Kurz)
- Setup: Python 3.12, `pip install -r requirements.txt`
- Env: `.env` aus `.env.example` erstellen
- Start (Dev): `python run.py`
- Start (Prod lokal): `gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:5000 app:app`

## ⚠️ Hinweise (macOS)
- Port 5000 belegt (AirPlay): Systemeinstellungen → Allgemein → AirDrop & Handoff → AirPlay‑Empfänger deaktivieren oder anderen Port nutzen

## 🗣️ Gesprächsnotiz (Lehrerfrage WMI)
- WMI nicht implementiert (keine Windows-spezifischen Pakete wie `wmi`/`pywin32`)
- Plattformunabhängige Web-App mit HTTP‑APIs und SQLite


