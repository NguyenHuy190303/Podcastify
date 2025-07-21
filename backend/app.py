"""
Main Flask application for Podcastify
"""
import os
import uuid
import asyncio
import logging
import time
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import threading
from typing import Dict, Any

# Import our modules
from config.config import Config
from backend.pdf_processor import PDFProcessor
from backend.content_filter import ContentFilter
from backend.tts_services import TTSManager, OpenAITTSService, GoogleTTSService
from backend.audio_processor import AudioProcessor, AudioMetadata, AudioChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend')
app.config.from_object(Config)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global managers
tts_manager = TTSManager()
pdf_processor = PDFProcessor()
content_filter = ContentFilter()
audio_processor = AudioProcessor(app.config['OUTPUT_FOLDER'])

# Job tracking
active_jobs: Dict[str, Dict[str, Any]] = {}

def initialize_tts_services():
    """Initialize TTS services based on configuration"""
    try:
        # Initialize OpenAI TTS
        if Config.OPENAI_API_KEY:
            openai_service = OpenAITTSService(
                api_key=Config.OPENAI_API_KEY,
                model=Config.OPENAI_MODEL,
                voice=Config.OPENAI_VOICE
            )
            tts_manager.add_service("openai", openai_service)
            logger.info("OpenAI TTS service initialized")
        
        # Initialize Google TTS
        if Config.GOOGLE_CLOUD_CREDENTIALS and os.path.exists(Config.GOOGLE_CLOUD_CREDENTIALS):
            google_service = GoogleTTSService(
                credentials_path=Config.GOOGLE_CLOUD_CREDENTIALS,
                language_code=Config.GOOGLE_LANGUAGE_CODE,
                voice_name=Config.GOOGLE_VOICE_NAME
            )
            tts_manager.add_service("google", google_service)
            logger.info("Google TTS service initialized")
        
        # Set default service
        tts_manager.set_default_service(Config.DEFAULT_TTS_SERVICE)
        
        # Validate services
        validation_results = tts_manager.validate_all_services()
        for service, is_valid in validation_results.items():
            if is_valid:
                logger.info(f"{service} TTS service validated successfully")
            else:
                logger.warning(f"{service} TTS service validation failed")
        
    except Exception as e:
        logger.error(f"Error initializing TTS services: {e}")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": tts_manager.get_available_services(),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle PDF file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
        file.save(upload_path)
        
        # Extract basic metadata
        metadata = pdf_processor.get_book_metadata(upload_path)
        
        # Store job info
        active_jobs[job_id] = {
            "id": job_id,
            "filename": filename,
            "upload_path": upload_path,
            "metadata": metadata,
            "status": "uploaded",
            "progress": 0,
            "created_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "job_id": job_id,
            "filename": filename,
            "metadata": metadata
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/convert', methods=['POST'])
def start_conversion():
    """Start PDF to audio conversion"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        settings = data.get('settings', {})
        
        if job_id not in active_jobs:
            return jsonify({"error": "Job not found"}), 404
        
        # Update job with settings
        active_jobs[job_id].update({
            "settings": settings,
            "status": "processing"
        })
        
        # Start conversion in background thread
        thread = threading.Thread(
            target=process_conversion,
            args=(job_id, settings)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({"message": "Conversion started", "job_id": job_id})
        
    except Exception as e:
        logger.error(f"Conversion start error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status/<job_id>')
def get_job_status(job_id):
    """Get job status"""
    if job_id not in active_jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = active_jobs[job_id]
    return jsonify({
        "job_id": job_id,
        "status": job.get("status"),
        "progress": job.get("progress", 0),
        "message": job.get("message", ""),
        "error": job.get("error"),
        "output_file": job.get("output_file")
    })

@app.route('/api/download/<job_id>')
def download_file(job_id):
    """Download converted audio file"""
    if job_id not in active_jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = active_jobs[job_id]
    if job.get("status") != "completed":
        return jsonify({"error": "Conversion not completed"}), 400
    
    output_file = job.get("output_file")
    if not output_file or not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 404
    
    return send_file(
        output_file,
        as_attachment=True,
        download_name=f"{job['filename'].rsplit('.', 1)[0]}.mp3"
    )

@app.route('/api/services')
def get_services():
    """Get available TTS services and voices"""
    services = {}

    for service_name in tts_manager.get_available_services():
        service = tts_manager.services[service_name]
        services[service_name] = {
            "name": service_name,
            "voices": service.get_available_voices()
        }

    return jsonify(services)

@app.route('/api/jobs')
def list_jobs():
    """List all active jobs"""
    jobs = []
    for job_id, job_data in active_jobs.items():
        jobs.append({
            "job_id": job_id,
            "filename": job_data.get("filename"),
            "status": job_data.get("status"),
            "progress": job_data.get("progress", 0),
            "created_at": job_data.get("created_at")
        })
    return jsonify(jobs)

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def cancel_job(job_id):
    """Cancel a job"""
    if job_id in active_jobs:
        active_jobs[job_id]["status"] = "cancelled"
        return jsonify({"message": "Job cancelled"})
    return jsonify({"error": "Job not found"}), 404

def process_conversion(job_id: str, settings: Dict[str, Any]):
    """Process PDF to audio conversion with enhanced error handling"""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            job = active_jobs[job_id]

            # Check if job was cancelled
            if job.get("status") == "cancelled":
                logger.info(f"Job {job_id} was cancelled")
                return

            upload_path = job["upload_path"]

            def update_progress(message: str, progress: float):
                job["message"] = message
                job["progress"] = progress
                socketio.emit('progress_update', {
                    'job_id': job_id,
                    'message': message,
                    'progress': progress
                })

                # Check for cancellation during processing
                if job.get("status") == "cancelled":
                    raise Exception("Job was cancelled by user")
        
        update_progress("Extracting text from PDF...", 0.1)
        
        # Extract text from PDF
        pages = pdf_processor.extract_text_from_pdf(upload_path)
        
        update_progress("Filtering content...", 0.2)
        
        # Filter content
        filtered_pages = content_filter.filter_pages(pages, app.config)
        
        update_progress("Detecting chapters...", 0.3)
        
        # Detect chapters
        sections = pdf_processor.detect_chapters(filtered_pages)
        filtered_sections = content_filter.filter_sections(sections, app.config)
        
        update_progress("Preparing text for speech synthesis...", 0.4)
        
        # Prepare text chunks
        all_chunks = []
        for section in filtered_sections:
            text_chunks = pdf_processor.chunk_text_for_tts(
                section.content, 
                app.config['MAX_CHUNK_SIZE']
            )
            
            for chunk_text in text_chunks:
                all_chunks.append({
                    'text': chunk_text,
                    'chapter': section.title
                })
        
        update_progress(f"Converting {len(all_chunks)} text chunks to speech...", 0.5)
        
        # Convert to speech with retry logic
        audio_chunks = []
        service_name = settings.get('tts_service', app.config['DEFAULT_TTS_SERVICE'])
        voice = settings.get('voice')
        speed = settings.get('speed', 1.0)

        for i, chunk in enumerate(all_chunks):
            progress = 0.5 + (i / len(all_chunks)) * 0.3
            update_progress(f"Synthesizing speech {i+1}/{len(all_chunks)}", progress)

            # Retry TTS with exponential backoff
            tts_retry_count = 0
            max_tts_retries = 3

            while tts_retry_count < max_tts_retries:
                try:
                    # Use asyncio for TTS
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    response = loop.run_until_complete(
                        tts_manager.synthesize_speech(
                            chunk['text'],
                            service_name=service_name,
                            voice=voice,
                            speed=speed
                        )
                    )

                    loop.close()

                    if response.error:
                        raise Exception(f"TTS error: {response.error}")

                    audio_chunks.append(AudioChunk(
                        audio_data=response.audio_data,
                        text=chunk['text'],
                        chapter=chunk['chapter']
                    ))
                    break  # Success, exit retry loop

                except Exception as tts_error:
                    tts_retry_count += 1
                    if tts_retry_count >= max_tts_retries:
                        raise Exception(f"TTS failed after {max_tts_retries} retries: {tts_error}")

                    # Exponential backoff
                    wait_time = 2 ** tts_retry_count
                    update_progress(f"TTS retry {tts_retry_count}/{max_tts_retries} in {wait_time}s...", progress)
                    time.sleep(wait_time)
        
        update_progress("Combining audio chunks...", 0.8)
        
        # Combine audio
        combined_audio = audio_processor.combine_audio_chunks(
            audio_chunks,
            app.config['CHAPTER_PAUSE_DURATION'],
            lambda msg, prog: update_progress(msg, 0.8 + prog * 0.15)
        )
        
        update_progress("Exporting final MP3...", 0.95)
        
        # Create output filename
        output_filename = f"{job_id}_{job['filename'].rsplit('.', 1)[0]}.mp3"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Create metadata
        metadata = AudioMetadata(
            title=job["metadata"]["title"],
            author=job["metadata"]["author"],
            album=job["metadata"]["title"],
            year=job["metadata"].get("creation_date", "")[:4] if job["metadata"].get("creation_date") else None,
            genre="Audiobook"
        )
        
        # Export MP3
        audio_processor.export_mp3(
            combined_audio,
            output_path,
            metadata,
            app.config['AUDIO_BITRATE'],
            lambda msg, prog: update_progress(msg, 0.95 + prog * 0.05)
        )
        
        # Update job status
        job.update({
            "status": "completed",
            "progress": 100,
            "message": "Conversion completed successfully",
            "output_file": output_path,
            "completed_at": datetime.now().isoformat()
        })
        
            socketio.emit('conversion_complete', {
                'job_id': job_id,
                'output_file': output_filename
            })
            return  # Success, exit retry loop

        except Exception as e:
            retry_count += 1
            logger.error(f"Conversion error for job {job_id} (attempt {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                # Final failure
                job.update({
                    "status": "failed",
                    "error": str(e),
                    "message": f"Conversion failed after {max_retries} attempts: {str(e)}"
                })

                socketio.emit('conversion_error', {
                    'job_id': job_id,
                    'error': str(e)
                })
                return
            else:
                # Retry with backoff
                wait_time = 5 * retry_count
                job.update({
                    "message": f"Retrying conversion in {wait_time}s (attempt {retry_count + 1}/{max_retries})",
                    "progress": 0
                })

                socketio.emit('progress_update', {
                    'job_id': job_id,
                    'message': job["message"],
                    'progress': 0
                })

                time.sleep(wait_time)

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Initialize services
    initialize_tts_services()
    
    # Run the app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
