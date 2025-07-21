#!/usr/bin/env python3
"""
Podcastify Launcher Script
Simple script to start the application with proper checks
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if basic requirements are met"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required (current: {sys.version_info.major}.{sys.version_info.minor})")
    
    # Check if .env file exists
    if not Path(".env").exists():
        issues.append(".env file not found (copy from .env.example and configure)")
    
    # Check if required directories exist
    for directory in ["uploads", "output"]:
        if not Path(directory).exists():
            Path(directory).mkdir(exist_ok=True)
    
    # Try importing key modules
    try:
        import flask
        import fitz
        import pydub
        import openai
    except ImportError as e:
        issues.append(f"Missing dependency: {e}")
    
    return issues

def print_banner():
    """Print application banner"""
    print("""
🎧 Podcastify - PDF to Audio Converter
=====================================

Transform your PDF books into high-quality audiobooks
using AI-powered text-to-speech technology.

""")

def print_startup_info():
    """Print startup information"""
    print("🚀 Starting Podcastify...")
    print("📍 Server will be available at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)

def main():
    """Main launcher function"""
    print_banner()
    
    # Check requirements
    issues = check_requirements()
    if issues:
        print("❌ Setup issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nPlease fix these issues before running the application.")
        print("Run 'python install.py' for setup assistance.")
        sys.exit(1)
    
    print("✅ Requirements check passed")
    
    # Start the application
    try:
        print_startup_info()
        
        # Import and run the Flask app
        from backend.app import app, socketio, initialize_tts_services
        
        # Ensure directories exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
        
        # Initialize services
        initialize_tts_services()
        
        # Run the app
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Check the error message above and ensure all requirements are met.")

if __name__ == "__main__":
    main()
