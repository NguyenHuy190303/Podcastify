#!/usr/bin/env python3
"""
Podcastify Demo Script
Demonstrates core functionality without the web interface
"""

import os
import asyncio
from pathlib import Path

# Import our modules
from backend.pdf_processor import PDFProcessor
from backend.content_filter import ContentFilter
from backend.tts_services import TTSManager, OpenAITTSService
from backend.audio_processor import AudioProcessor, AudioMetadata, AudioChunk
from config.config import Config

def create_sample_pdf_text():
    """Create a sample text that simulates PDF content"""
    return """
Chapter 1: Introduction

This is a sample chapter from a book. It contains the main content that we want to convert to audio.

The text processing system will identify this as valuable content and include it in the final audiobook.

Chapter 2: Main Content

Here is another chapter with more substantial content. This demonstrates how the system handles multiple chapters and creates appropriate breaks between them.

The smart filtering system will preserve this content while removing unnecessary sections.

Acknowledgments

The author would like to thank everyone who contributed to this work. This section would normally be filtered out by the content filtering system.

Index

A - Apple, 15
B - Book, 23
C - Chapter, 45

This index section would also be filtered out automatically.
"""

async def demo_conversion():
    """Demonstrate the conversion process"""
    print("🎧 Podcastify Demo")
    print("=" * 20)
    
    # Check if API key is available
    if not Config.OPENAI_API_KEY:
        print("❌ OpenAI API key not found in environment")
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    print("✅ API key found")
    
    # Initialize components
    print("\n📦 Initializing components...")
    pdf_processor = PDFProcessor()
    content_filter = ContentFilter()
    audio_processor = AudioProcessor()
    
    # Initialize TTS service
    tts_manager = TTSManager()
    openai_service = OpenAITTSService(
        api_key=Config.OPENAI_API_KEY,
        model="tts-1",  # Use faster model for demo
        voice="alloy"
    )
    tts_manager.add_service("openai", openai_service)
    
    print("✅ Components initialized")
    
    # Simulate PDF processing
    print("\n📄 Processing sample content...")
    sample_text = create_sample_pdf_text()
    
    # Simulate content filtering
    print("🔍 Applying content filters...")
    
    # Split into sections (simulate chapter detection)
    sections = sample_text.split("Chapter")
    filtered_sections = []
    
    for i, section in enumerate(sections):
        if section.strip() and not any(keyword in section.lower() for keyword in 
                                     ['acknowledgments', 'index', 'bibliography']):
            if i > 0:  # Skip empty first section
                filtered_sections.append(f"Chapter{section}")
    
    print(f"✅ Filtered to {len(filtered_sections)} main sections")
    
    # Prepare text chunks
    print("\n✂️ Chunking text for TTS...")
    all_chunks = []
    
    for section in filtered_sections:
        chunks = pdf_processor.chunk_text_for_tts(section, 500)  # Smaller chunks for demo
        for chunk in chunks:
            all_chunks.append({
                'text': chunk,
                'chapter': f"Chapter {len(all_chunks) // 2 + 1}"
            })
    
    print(f"✅ Created {len(all_chunks)} text chunks")
    
    # Convert to speech
    print("\n🎵 Converting to speech...")
    audio_chunks = []
    
    for i, chunk in enumerate(all_chunks):
        print(f"   Processing chunk {i+1}/{len(all_chunks)}")
        
        response = await tts_manager.synthesize_speech(
            chunk['text'],
            service_name="openai",
            voice="alloy",
            speed=1.0
        )
        
        if response.error:
            print(f"❌ TTS error: {response.error}")
            return
        
        audio_chunks.append(AudioChunk(
            audio_data=response.audio_data,
            text=chunk['text'],
            chapter=chunk['chapter']
        ))
    
    print("✅ Speech synthesis complete")
    
    # Combine audio
    print("\n🔗 Combining audio chunks...")
    combined_audio = audio_processor.combine_audio_chunks(
        audio_chunks,
        chapter_pause_duration=1.0  # Shorter pause for demo
    )
    
    print("✅ Audio combination complete")
    
    # Export MP3
    print("\n💾 Exporting MP3...")
    output_path = "output/demo_audiobook.mp3"
    
    metadata = AudioMetadata(
        title="Demo Audiobook",
        author="Podcastify Demo",
        album="Demo Collection",
        genre="Audiobook"
    )
    
    final_path = audio_processor.export_mp3(
        combined_audio,
        output_path,
        metadata,
        bitrate="128k"  # Lower bitrate for demo
    )
    
    print(f"✅ Demo audiobook created: {final_path}")
    
    # Get audio info
    audio_info = audio_processor.get_audio_info(final_path)
    if audio_info:
        duration_min = audio_info.get('duration', 0) / 60
        file_size_mb = audio_info.get('file_size', 0) / (1024 * 1024)
        print(f"📊 Duration: {duration_min:.1f} minutes")
        print(f"📊 File size: {file_size_mb:.1f} MB")
    
    print("\n🎉 Demo complete!")
    print(f"You can play the generated file: {final_path}")

def main():
    """Run the demo"""
    try:
        # Ensure output directory exists
        Path("output").mkdir(exist_ok=True)
        
        # Run the demo
        asyncio.run(demo_conversion())
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure you have:")
        print("1. Installed all dependencies (pip install -r requirements.txt)")
        print("2. Set up your OpenAI API key in .env file")
        print("3. Installed FFmpeg")

if __name__ == "__main__":
    main()
