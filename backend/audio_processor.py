"""
Audio processing module for combining TTS chunks and generating final MP3
"""
import os
import io
import logging
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TRCK
import tempfile

logger = logging.getLogger(__name__)

@dataclass
class AudioChunk:
    """Represents a chunk of audio with metadata"""
    audio_data: bytes
    text: str
    chapter: Optional[str] = None
    start_time: Optional[float] = None
    duration: Optional[float] = None

@dataclass
class AudioMetadata:
    """Metadata for the final audio file"""
    title: str
    author: str
    album: Optional[str] = None
    year: Optional[str] = None
    genre: str = "Audiobook"
    track_number: Optional[int] = None
    total_tracks: Optional[int] = None
    description: Optional[str] = None

class AudioProcessor:
    """Handles audio processing and MP3 generation"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.temp_dir = tempfile.mkdtemp()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def combine_audio_chunks(self, chunks: List[AudioChunk], 
                           chapter_pause_duration: float = 2.0,
                           progress_callback: Optional[Callable] = None) -> AudioSegment:
        """Combine multiple audio chunks into a single audio file"""
        try:
            combined_audio = AudioSegment.empty()
            total_chunks = len(chunks)
            
            for i, chunk in enumerate(chunks):
                if progress_callback:
                    progress_callback(f"Processing chunk {i+1}/{total_chunks}", 
                                    (i / total_chunks) * 0.8)  # 80% for combining
                
                # Convert bytes to AudioSegment
                audio_segment = AudioSegment.from_file(
                    io.BytesIO(chunk.audio_data), 
                    format="mp3"
                )
                
                # Add the audio chunk
                combined_audio += audio_segment
                
                # Add pause between chapters if this chunk ends a chapter
                if (i < len(chunks) - 1 and 
                    chunk.chapter and 
                    chunks[i + 1].chapter and 
                    chunk.chapter != chunks[i + 1].chapter):
                    
                    pause = AudioSegment.silent(duration=int(chapter_pause_duration * 1000))
                    combined_audio += pause
                    logger.info(f"Added {chapter_pause_duration}s pause after chapter: {chunk.chapter}")
            
            if progress_callback:
                progress_callback("Audio combination complete", 0.8)
            
            return combined_audio
            
        except Exception as e:
            logger.error(f"Error combining audio chunks: {e}")
            raise
    
    def export_mp3(self, audio: AudioSegment, output_path: str, 
                   metadata: AudioMetadata, bitrate: str = "192k",
                   progress_callback: Optional[Callable] = None) -> str:
        """Export audio as MP3 with metadata"""
        try:
            if progress_callback:
                progress_callback("Exporting MP3...", 0.8)
            
            # Export as MP3
            audio.export(
                output_path,
                format="mp3",
                bitrate=bitrate,
                tags={
                    "title": metadata.title,
                    "artist": metadata.author,
                    "album": metadata.album or metadata.title,
                    "date": metadata.year or "",
                    "genre": metadata.genre
                }
            )
            
            if progress_callback:
                progress_callback("Adding detailed metadata...", 0.9)
            
            # Add more detailed metadata using mutagen
            self._add_detailed_metadata(output_path, metadata)
            
            if progress_callback:
                progress_callback("Export complete", 1.0)
            
            logger.info(f"MP3 exported successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting MP3: {e}")
            raise
    
    def _add_detailed_metadata(self, file_path: str, metadata: AudioMetadata):
        """Add detailed ID3 metadata to MP3 file"""
        try:
            audio_file = MP3(file_path, ID3=ID3)
            
            # Add ID3 tag if it doesn't exist
            if audio_file.tags is None:
                audio_file.add_tags()
            
            # Set metadata
            audio_file.tags.add(TIT2(encoding=3, text=metadata.title))
            audio_file.tags.add(TPE1(encoding=3, text=metadata.author))
            
            if metadata.album:
                audio_file.tags.add(TALB(encoding=3, text=metadata.album))
            
            if metadata.year:
                audio_file.tags.add(TDRC(encoding=3, text=metadata.year))
            
            audio_file.tags.add(TCON(encoding=3, text=metadata.genre))
            
            if metadata.track_number:
                track_text = str(metadata.track_number)
                if metadata.total_tracks:
                    track_text += f"/{metadata.total_tracks}"
                audio_file.tags.add(TRCK(encoding=3, text=track_text))
            
            audio_file.save()
            
        except Exception as e:
            logger.error(f"Error adding detailed metadata: {e}")
    
    def create_chapter_markers(self, chunks: List[AudioChunk]) -> List[Dict]:
        """Create chapter markers for the audio file"""
        chapters = []
        current_time = 0.0
        current_chapter = None
        chapter_start = 0.0
        
        for chunk in chunks:
            if chunk.chapter and chunk.chapter != current_chapter:
                # End previous chapter
                if current_chapter:
                    chapters.append({
                        "title": current_chapter,
                        "start_time": chapter_start,
                        "end_time": current_time
                    })
                
                # Start new chapter
                current_chapter = chunk.chapter
                chapter_start = current_time
            
            # Estimate duration (rough calculation)
            if chunk.duration:
                current_time += chunk.duration
            else:
                # Estimate based on text length (rough: 150 words per minute)
                word_count = len(chunk.text.split())
                estimated_duration = (word_count / 150) * 60
                current_time += estimated_duration
        
        # Add final chapter
        if current_chapter:
            chapters.append({
                "title": current_chapter,
                "start_time": chapter_start,
                "end_time": current_time
            })
        
        return chapters
    
    def split_by_chapters(self, audio: AudioSegment, chapters: List[Dict],
                         output_dir: str, base_filename: str,
                         metadata: AudioMetadata) -> List[str]:
        """Split audio into separate files by chapter"""
        chapter_files = []
        
        try:
            for i, chapter in enumerate(chapters):
                start_ms = int(chapter["start_time"] * 1000)
                end_ms = int(chapter["end_time"] * 1000)
                
                chapter_audio = audio[start_ms:end_ms]
                
                # Create chapter filename
                chapter_filename = f"{base_filename}_chapter_{i+1:02d}.mp3"
                chapter_path = os.path.join(output_dir, chapter_filename)
                
                # Create chapter metadata
                chapter_metadata = AudioMetadata(
                    title=chapter["title"],
                    author=metadata.author,
                    album=metadata.album,
                    year=metadata.year,
                    genre=metadata.genre,
                    track_number=i + 1,
                    total_tracks=len(chapters)
                )
                
                # Export chapter
                self.export_mp3(chapter_audio, chapter_path, chapter_metadata)
                chapter_files.append(chapter_path)
                
                logger.info(f"Created chapter file: {chapter_filename}")
            
            return chapter_files
            
        except Exception as e:
            logger.error(f"Error splitting by chapters: {e}")
            raise
    
    def get_audio_info(self, file_path: str) -> Dict:
        """Get information about an audio file"""
        try:
            audio = AudioSegment.from_mp3(file_path)
            
            return {
                "duration": len(audio) / 1000.0,  # seconds
                "channels": audio.channels,
                "frame_rate": audio.frame_rate,
                "sample_width": audio.sample_width,
                "file_size": os.path.getsize(file_path)
            }
            
        except Exception as e:
            logger.error(f"Error getting audio info: {e}")
            return {}
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup_temp_files()
