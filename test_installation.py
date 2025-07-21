#!/usr/bin/env python3
"""
Test script to verify Podcastify installation
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    modules = [
        ("flask", "Flask"),
        ("fitz", "PyMuPDF"),
        ("pydub", "pydub"),
        ("openai", "OpenAI"),
        ("google.cloud.texttospeech", "Google Cloud TTS"),
        ("mutagen", "mutagen"),
        ("socketio", "Flask-SocketIO")
    ]
    
    failed_imports = []
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            failed_imports.append(name)
    
    return len(failed_imports) == 0, failed_imports

def test_backend_modules():
    """Test if backend modules can be imported"""
    print("\n🔧 Testing backend modules...")
    
    backend_modules = [
        ("backend.pdf_processor", "PDF Processor"),
        ("backend.content_filter", "Content Filter"),
        ("backend.tts_services", "TTS Services"),
        ("backend.audio_processor", "Audio Processor"),
        ("config.config", "Configuration")
    ]
    
    failed_modules = []
    
    for module, name in backend_modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed_modules.append(name)
    
    return len(failed_modules) == 0, failed_modules

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing directories...")
    
    directories = [
        "uploads",
        "output",
        "backend",
        "frontend",
        "config"
    ]
    
    missing_dirs = []
    
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/")
            missing_dirs.append(directory)
    
    return len(missing_dirs) == 0, missing_dirs

def test_files():
    """Test if required files exist"""
    print("\n📄 Testing required files...")
    
    files = [
        "requirements.txt",
        ".env.example",
        "backend/app.py",
        "frontend/index.html",
        "frontend/style.css",
        "frontend/script.js",
        "config/config.py"
    ]
    
    missing_files = []
    
    for file_path in files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config.config import Config
        
        # Test basic config loading
        print(f"✅ Configuration loaded")
        
        # Check for .env file
        if Path(".env").exists():
            print("✅ .env file exists")
        else:
            print("⚠️ .env file not found (copy from .env.example)")
        
        # Validate config
        errors = Config.validate_config()
        if errors:
            print("⚠️ Configuration issues:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ Configuration validation passed")
        
        return True, []
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False, [str(e)]

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔬 Testing basic functionality...")
    
    try:
        # Test PDF processor
        from backend.pdf_processor import PDFProcessor
        pdf_processor = PDFProcessor()
        print("✅ PDF Processor initialization")
        
        # Test content filter
        from backend.content_filter import ContentFilter
        content_filter = ContentFilter()
        print("✅ Content Filter initialization")
        
        # Test TTS manager
        from backend.tts_services import TTSManager
        tts_manager = TTSManager()
        print("✅ TTS Manager initialization")
        
        # Test audio processor
        from backend.audio_processor import AudioProcessor
        audio_processor = AudioProcessor()
        print("✅ Audio Processor initialization")
        
        return True, []
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False, [str(e)]

def main():
    """Run all tests"""
    print("🎧 Podcastify Installation Test")
    print("=" * 35)
    
    all_passed = True
    all_issues = []
    
    # Run tests
    tests = [
        ("Module Imports", test_imports),
        ("Backend Modules", test_backend_modules),
        ("Directories", test_directories),
        ("Required Files", test_files),
        ("Configuration", test_configuration),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    for test_name, test_func in tests:
        passed, issues = test_func()
        if not passed:
            all_passed = False
            all_issues.extend(issues)
    
    # Summary
    print("\n" + "=" * 35)
    if all_passed:
        print("🎉 All tests passed! Installation looks good.")
        print("\nYou can now run the application with:")
        print("   python backend/app.py")
    else:
        print("❌ Some tests failed. Issues found:")
        for issue in all_issues:
            print(f"   - {issue}")
        print("\nPlease fix these issues and run the test again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
