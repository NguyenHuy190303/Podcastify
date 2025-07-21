"""
Text-to-Speech service integrations for OpenAI and Google Cloud
"""
import os
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import asyncio
import aiohttp

# TTS API imports
import openai
from google.cloud import texttospeech

logger = logging.getLogger(__name__)

@dataclass
class TTSRequest:
    """Represents a TTS request"""
    text: str
    voice: str
    model: Optional[str] = None
    speed: float = 1.0
    
@dataclass
class TTSResponse:
    """Represents a TTS response"""
    audio_data: bytes
    format: str
    duration: Optional[float] = None
    error: Optional[str] = None

class TTSService(ABC):
    """Abstract base class for TTS services"""
    
    @abstractmethod
    async def synthesize_speech(self, request: TTSRequest) -> TTSResponse:
        """Synthesize speech from text"""
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate service configuration"""
        pass

class OpenAITTSService(TTSService):
    """OpenAI Text-to-Speech service implementation"""
    
    def __init__(self, api_key: str, model: str = "tts-1-hd", voice: str = "alloy"):
        self.api_key = api_key
        self.model = model
        self.voice = voice
        self.client = openai.OpenAI(api_key=api_key)
        
        # Rate limiting
        self.requests_per_minute = 50
        self.request_times = []
    
    async def synthesize_speech(self, request: TTSRequest) -> TTSResponse:
        """Synthesize speech using OpenAI TTS"""
        try:
            # Rate limiting
            await self._wait_for_rate_limit()
            
            response = self.client.audio.speech.create(
                model=request.model or self.model,
                voice=request.voice or self.voice,
                input=request.text,
                speed=request.speed
            )
            
            audio_data = response.content
            
            return TTSResponse(
                audio_data=audio_data,
                format="mp3",
                duration=None  # OpenAI doesn't provide duration
            )
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return TTSResponse(
                audio_data=b"",
                format="mp3",
                error=str(e)
            )
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get OpenAI available voices"""
        return [
            {"name": "alloy", "description": "Neutral, balanced voice"},
            {"name": "echo", "description": "Male voice"},
            {"name": "fable", "description": "British accent"},
            {"name": "onyx", "description": "Deep male voice"},
            {"name": "nova", "description": "Female voice"},
            {"name": "shimmer", "description": "Soft female voice"}
        ]
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration"""
        try:
            # Test with a simple request
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input="Test"
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI config validation failed: {e}")
            return False
    
    async def _wait_for_rate_limit(self):
        """Implement rate limiting"""
        now = time.time()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # If we're at the limit, wait
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.request_times.append(now)

class GoogleTTSService(TTSService):
    """Google Cloud Text-to-Speech service implementation"""
    
    def __init__(self, credentials_path: str, language_code: str = "en-US", 
                 voice_name: str = "en-US-Wavenet-D"):
        self.credentials_path = credentials_path
        self.language_code = language_code
        self.voice_name = voice_name
        
        # Set up credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = texttospeech.TextToSpeechClient()
        
        # Rate limiting
        self.requests_per_minute = 100
        self.request_times = []
    
    async def synthesize_speech(self, request: TTSRequest) -> TTSResponse:
        """Synthesize speech using Google Cloud TTS"""
        try:
            # Rate limiting
            await self._wait_for_rate_limit()
            
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=request.text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=request.voice or self.voice_name
            )
            
            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=request.speed
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return TTSResponse(
                audio_data=response.audio_content,
                format="mp3",
                duration=None  # Google doesn't provide duration directly
            )
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return TTSResponse(
                audio_data=b"",
                format="mp3",
                error=str(e)
            )
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get Google Cloud available voices"""
        try:
            voices = self.client.list_voices()
            voice_list = []
            
            for voice in voices.voices:
                if voice.language_codes[0].startswith('en'):  # English voices only
                    voice_list.append({
                        "name": voice.name,
                        "language": voice.language_codes[0],
                        "gender": voice.ssml_gender.name,
                        "description": f"{voice.name} ({voice.ssml_gender.name})"
                    })
            
            return voice_list
            
        except Exception as e:
            logger.error(f"Error getting Google voices: {e}")
            return []
    
    def validate_config(self) -> bool:
        """Validate Google Cloud configuration"""
        try:
            # Test with a simple request
            synthesis_input = texttospeech.SynthesisInput(text="Test")
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            return True
            
        except Exception as e:
            logger.error(f"Google config validation failed: {e}")
            return False
    
    async def _wait_for_rate_limit(self):
        """Implement rate limiting"""
        now = time.time()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # If we're at the limit, wait
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.request_times.append(now)

class TTSManager:
    """Manages multiple TTS services"""
    
    def __init__(self):
        self.services: Dict[str, TTSService] = {}
        self.default_service = None
    
    def add_service(self, name: str, service: TTSService):
        """Add a TTS service"""
        self.services[name] = service
        if self.default_service is None:
            self.default_service = name
    
    def set_default_service(self, name: str):
        """Set the default TTS service"""
        if name in self.services:
            self.default_service = name
        else:
            raise ValueError(f"Service '{name}' not found")
    
    async def synthesize_speech(self, text: str, service_name: Optional[str] = None,
                              voice: Optional[str] = None, speed: float = 1.0) -> TTSResponse:
        """Synthesize speech using specified or default service"""
        service_name = service_name or self.default_service
        
        if service_name not in self.services:
            raise ValueError(f"Service '{service_name}' not found")
        
        service = self.services[service_name]
        request = TTSRequest(text=text, voice=voice or "", speed=speed)
        
        return await service.synthesize_speech(request)
    
    def get_available_services(self) -> List[str]:
        """Get list of available service names"""
        return list(self.services.keys())
    
    def validate_all_services(self) -> Dict[str, bool]:
        """Validate all configured services"""
        results = {}
        for name, service in self.services.items():
            results[name] = service.validate_config()
        return results
