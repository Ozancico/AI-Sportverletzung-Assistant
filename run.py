#!/usr/bin/env python3
"""
AI-Sportverletzung-Assistant Launcher Script
Starts the application with automatic dependency checking
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python Version: {sys.version.split()[0]}")

def check_virtual_env():
    """Check if virtual environment is active"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
    else:
        print("⚠️  Warning: No virtual environment active")
        print("   Recommendation: python -m venv .venv && source .venv/bin/activate")

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import flask
        import openai
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and is configured"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Copy .env.example to .env and configure it")
        return False
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("⚠️  Warning: OpenAI API Key not configured!")
            print("   Edit the .env file and add your API key")
            return False
    
    print("✅ .env file is configured")
    return True

def main():
    """Main function"""
    print("🏋️‍♂️ AI-Sportverletzung-Assistant")
    print("=" * 50)
    
    # Checks
    check_python_version()
    check_virtual_env()
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_file():
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your OpenAI API key")
        print("3. Run this script again")
        sys.exit(1)
    
    # Determine port from environment variables, default to 5000
    port_env = os.getenv('PORT') or os.getenv('FLASK_RUN_PORT')
    try:
        port = int(port_env) if port_env else 5000
    except ValueError:
        port = 5000

    print("\n🚀 Starting application...")
    print(f"   Open http://localhost:{port} in your browser")
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start Flask application
    try:
        from app import app, db
        # Ensure database tables exist
        with app.app_context():
            db.create_all()
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
