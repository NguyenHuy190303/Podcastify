"""
Configuration settings for Podcastify application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_CLOUD_CREDENTIALS = os.getenv('GOOGLE_CLOUD_CREDENTIALS')  # Path to JSON file
    
    # Application settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'output'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # TTS Settings
    DEFAULT_TTS_SERVICE = 'openai'  # 'openai' or 'google'
    OPENAI_VOICE = 'alloy'  # alloy, echo, fable, onyx, nova, shimmer
    OPENAI_MODEL = 'tts-1-hd'  # tts-1 or tts-1-hd
    GOOGLE_VOICE_NAME = 'en-US-Wavenet-D'
    GOOGLE_LANGUAGE_CODE = 'en-US'
    
    # Audio settings
    AUDIO_FORMAT = 'mp3'
    AUDIO_BITRATE = '192k'
    CHAPTER_PAUSE_DURATION = 2.0  # seconds
    
    # Processing settings
    MAX_CHUNK_SIZE = 4000  # characters per TTS request
    CONCURRENT_REQUESTS = 3  # number of parallel TTS requests
    
    # Content filtering settings
    SKIP_TOC = True
    SKIP_ACKNOWLEDGMENTS = True
    SKIP_COPYRIGHT = True
    SKIP_INDEX = True
    SKIP_BIBLIOGRAPHY = True
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY environment variable is required")
            
        if not cls.GOOGLE_CLOUD_CREDENTIALS:
            errors.append("GOOGLE_CLOUD_CREDENTIALS environment variable is required")
            
        return errors
