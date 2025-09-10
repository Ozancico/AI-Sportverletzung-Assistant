#!/usr/bin/env python3
"""
AI-Sportverletzung-Assistant Launcher Script
Startet die Anwendung mit automatischer Dependency-Überprüfung
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Überprüft die Python Version"""
    if sys.version_info < (3, 8):
        print("❌ Fehler: Python 3.8 oder höher ist erforderlich!")
        print(f"   Aktuelle Version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python Version: {sys.version.split()[0]}")

def check_virtual_env():
    """Überprüft ob ein virtuelles Environment aktiv ist"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtuelles Environment ist aktiv")
    else:
        print("⚠️  Warnung: Kein virtuelles Environment aktiv")
        print("   Empfehlung: python -m venv .venv && source .venv/bin/activate")

def check_dependencies():
    """Überprüft ob alle Dependencies installiert sind"""
    try:
        import flask
        import openai
        import dotenv
        print("✅ Alle Dependencies sind installiert")
        return True
    except ImportError as e:
        print(f"❌ Fehlende Dependencies: {e}")
        print("   Führen Sie aus: pip install -r requirements.txt")
        return False

def check_env_file():
    """Überprüft ob .env Datei existiert und konfiguriert ist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env Datei nicht gefunden!")
        print("   Kopieren Sie .env.example zu .env und konfigurieren Sie es")
        return False
    
    # Überprüfe ob API Key gesetzt ist
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("⚠️  Warnung: OpenAI API Key nicht konfiguriert!")
            print("   Bearbeiten Sie die .env Datei und fügen Sie Ihren API Key hinzu")
            return False
    
    print("✅ .env Datei ist konfiguriert")
    return True

def main():
    """Hauptfunktion"""
    print("🏋️‍♂️ AI-Sportverletzung-Assistant")
    print("=" * 50)
    
    # Überprüfungen
    check_python_version()
    check_virtual_env()
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_file():
        print("\n📝 Setup-Anleitung:")
        print("1. Kopieren Sie .env.example zu .env")
        print("2. Bearbeiten Sie .env und fügen Sie Ihren OpenAI API Key hinzu")
        print("3. Führen Sie dieses Script erneut aus")
        sys.exit(1)
    
    print("\n🚀 Starte Anwendung...")
    print("   Öffnen Sie http://localhost:5000 in Ihrem Browser")
    print("   Drücken Sie Ctrl+C zum Beenden")
    print("=" * 50)
    
    # Starte die Flask-Anwendung
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Anwendung beendet")
    except Exception as e:
        print(f"\n❌ Fehler beim Starten: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
