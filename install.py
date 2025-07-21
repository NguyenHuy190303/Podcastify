#!/usr/bin/env python3
"""
Podcastify Installation Script
Helps set up the application with proper dependencies and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("🎧 Podcastify Installation Script")
    print("=" * 40)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\n🎵 Checking FFmpeg installation...")
    try:
        subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        return False

def install_ffmpeg_instructions():
    """Provide FFmpeg installation instructions"""
    system = platform.system().lower()
    
    print("\n📋 FFmpeg Installation Instructions:")
    print("-" * 35)
    
    if system == "windows":
        print("Windows:")
        print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
        print("2. Extract to C:\\ffmpeg")
        print("3. Add C:\\ffmpeg\\bin to your PATH environment variable")
        print("4. Restart your command prompt")
    
    elif system == "darwin":  # macOS
        print("macOS:")
        print("1. Install Homebrew if not already installed:")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Install FFmpeg:")
        print("   brew install ffmpeg")
    
    elif system == "linux":
        print("Linux (Ubuntu/Debian):")
        print("   sudo apt-get update && sudo apt-get install ffmpeg")
        print("\nLinux (CentOS/RHEL):")
        print("   sudo yum install ffmpeg")
        print("\nLinux (Arch):")
        print("   sudo pacman -S ffmpeg")
    
    print("\nAfter installing FFmpeg, run this script again to verify.")

def setup_environment():
    """Set up environment configuration"""
    print("\n⚙️ Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ Created .env file from template")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ No .env.example file found")
        return False
    
    print("\n📝 Please edit the .env file with your API credentials:")
    print("   - OPENAI_API_KEY: Your OpenAI API key")
    print("   - GOOGLE_CLOUD_CREDENTIALS: Path to your Google Cloud credentials JSON")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["uploads", "output"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def validate_installation():
    """Validate the installation"""
    print("\n🔍 Validating installation...")
    
    # Check if main modules can be imported
    try:
        from backend.app import app
        print("✅ Backend modules can be imported")
    except ImportError as e:
        print(f"❌ Failed to import backend modules: {e}")
        return False
    
    # Check if config can be loaded
    try:
        from config.config import Config
        errors = Config.validate_config()
        if errors:
            print("⚠️ Configuration warnings:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ Configuration is valid")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Installation Complete!")
    print("=" * 25)
    print("\nNext steps:")
    print("1. Edit the .env file with your API credentials")
    print("2. Run the application:")
    print("   python backend/app.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nFor help and documentation, see README.md")

def main():
    """Main installation process"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python dependencies
    if not install_dependencies():
        print("\n❌ Installation failed at dependency installation")
        sys.exit(1)
    
    # Check FFmpeg
    if not check_ffmpeg():
        install_ffmpeg_instructions()
        print("\n⚠️ Please install FFmpeg and run this script again")
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        print("\n❌ Failed to set up environment")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Validate installation
    if not validate_installation():
        print("\n❌ Installation validation failed")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
