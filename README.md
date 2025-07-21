# 🎧 Podcastify - PDF to Audio Converter

Ứng dụng web hiện đại chuyển đổi sách PDF thành podcast audio chất lượng cao sử dụng AI Text-to-Speech với giao diện pastel đẹp mắt.

![Podcastify Preview](https://via.placeholder.com/800x400/6366F1/FFFFFF?text=Podcastify+Preview)

## ✨ Features

### Core Functionality
- **PDF to MP3 Conversion**: Convert entire PDF books to high-quality audio files
- **Dual TTS Integration**: Support for both OpenAI TTS and Google Cloud Text-to-Speech
- **Smart Content Filtering**: Automatically skip irrelevant sections like:
  - Publication information and copyright pages
  - Acknowledgments and dedications
  - Table of contents (optional)
  - Index and bibliography
  - Promotional content

### Audio Features
- **High-Quality Output**: Generate MP3 files with customizable bitrate
- **Chapter Detection**: Automatically detect and separate chapters
- **Intelligent Pauses**: Add appropriate breaks between chapters
- **Rich Metadata**: Embed book title, author, and chapter information
- **Voice Customization**: Choose from multiple voices and adjust speech speed

### User Experience
- **Web-Based Interface**: Modern, responsive design that works on all devices
- **Real-Time Progress**: Live updates during conversion process
- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Batch Processing**: Convert multiple PDFs (coming soon)
- **Error Recovery**: Robust error handling with retry mechanisms

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Google Cloud Text-to-Speech API credentials (optional)
- FFmpeg (for audio processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Podcastify
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API credentials**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

4. **Install FFmpeg**
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

### Configuration

Edit the `.env` file with your API credentials:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Google Cloud credentials (optional)
GOOGLE_CLOUD_CREDENTIALS=path/to/your/google-credentials.json

# Application secret key (optional)
SECRET_KEY=your_secret_key_here
```

### Running the Application

```bash
python backend/app.py
```

Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### Basic Conversion

1. **Upload PDF**: Drag and drop or click to select your PDF file
2. **Review Metadata**: Check the extracted book information
3. **Configure Settings**:
   - Choose TTS service (OpenAI or Google)
   - Select voice and speech speed
   - Configure content filtering options
4. **Start Conversion**: Click "Start Conversion" and monitor progress
5. **Download**: Download your generated audiobook when complete

### Advanced Settings

#### TTS Services
- **OpenAI TTS**: Fast, high-quality voices with natural speech patterns
- **Google Cloud TTS**: Wide variety of voices with SSML support

#### Content Filtering
- **Skip Table of Contents**: Remove navigation pages
- **Skip Acknowledgments**: Remove dedication and thanks sections
- **Skip Copyright**: Remove publication and legal information
- **Skip Index**: Remove reference sections and bibliography

#### Audio Quality
- **Bitrate**: 192k (default) for optimal quality/size balance
- **Chapter Pauses**: 2-second breaks between chapters
- **Speed Control**: 0.5x to 2.0x playback speed

## 🏗️ Architecture

### Backend Components
- **Flask API**: RESTful endpoints for file upload and processing
- **PDF Processor**: Text extraction using PyMuPDF
- **Content Filter**: Smart filtering using heuristic analysis
- **TTS Services**: Abstracted interface for multiple TTS providers
- **Audio Processor**: MP3 generation with metadata embedding

### Frontend Components
- **Responsive Web UI**: Modern interface with real-time updates
- **WebSocket Integration**: Live progress tracking
- **File Management**: Drag-and-drop upload with validation

### Technology Stack
- **Backend**: Python, Flask, PyMuPDF, pydub
- **Frontend**: HTML5, CSS3, JavaScript, Socket.IO
- **APIs**: OpenAI TTS, Google Cloud Text-to-Speech
- **Audio**: FFmpeg, mutagen for metadata

## 🔧 Configuration Options

### Application Settings (`config/config.py`)

```python
# TTS Settings
DEFAULT_TTS_SERVICE = 'openai'  # 'openai' or 'google'
OPENAI_VOICE = 'alloy'  # Voice selection
OPENAI_MODEL = 'tts-1-hd'  # Quality model

# Audio Settings
AUDIO_BITRATE = '192k'  # Output quality
CHAPTER_PAUSE_DURATION = 2.0  # Seconds between chapters

# Processing Settings
MAX_CHUNK_SIZE = 4000  # Characters per TTS request
CONCURRENT_REQUESTS = 3  # Parallel processing
```

## 🛠️ Development

### Project Structure
```
Podcastify/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── pdf_processor.py    # PDF text extraction
│   ├── content_filter.py   # Smart content filtering
│   ├── tts_services.py     # TTS API integrations
│   └── audio_processor.py  # Audio generation
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
├── config/
│   └── config.py           # Configuration settings
├── uploads/                # Temporary PDF storage
├── output/                 # Generated audio files
└── requirements.txt        # Python dependencies
```

### Adding New TTS Services

1. Implement the `TTSService` abstract class
2. Add service initialization in `app.py`
3. Update frontend service selection

### Extending Content Filtering

1. Add new keyword sets in `ContentFilter`
2. Implement detection heuristics
3. Update configuration options

## 🐛 Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Install FFmpeg and ensure it's in your system PATH

**"API key invalid"**
- Verify your API keys in the `.env` file
- Check API key permissions and quotas

**"PDF extraction failed"**
- Ensure PDF is not password-protected
- Try with a different PDF file

**"Conversion stuck"**
- Check API rate limits
- Monitor network connectivity
- Review server logs for errors

### Performance Optimization

- Use `tts-1` model for faster processing
- Reduce `MAX_CHUNK_SIZE` for better memory usage
- Adjust `CONCURRENT_REQUESTS` based on API limits

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation for TTS services

---

**Made with ❤️ for audiobook enthusiasts**
