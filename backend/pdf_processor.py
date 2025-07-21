"""
PDF text extraction and processing module
"""
import fitz  # PyMuPDF
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class PageContent:
    """Represents content from a single PDF page"""
    page_number: int
    text: str
    word_count: int
    has_images: bool
    font_sizes: List[float]
    
@dataclass
class BookSection:
    """Represents a section of the book"""
    title: str
    start_page: int
    end_page: int
    content: str
    section_type: str  # 'chapter', 'preface', 'appendix', etc.

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self):
        self.pages: List[PageContent] = []
        self.sections: List[BookSection] = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> List[PageContent]:
        """Extract text from PDF file with metadata"""
        try:
            doc = fitz.open(pdf_path)
            pages = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                
                # Get font information
                blocks = page.get_text("dict")
                font_sizes = []
                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                font_sizes.append(span.get("size", 12))
                
                # Check for images
                has_images = len(page.get_images()) > 0
                
                page_content = PageContent(
                    page_number=page_num + 1,
                    text=text.strip(),
                    word_count=len(text.split()),
                    has_images=has_images,
                    font_sizes=font_sizes
                )
                pages.append(page_content)
                
            doc.close()
            self.pages = pages
            return pages
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    def detect_chapters(self, pages: List[PageContent]) -> List[BookSection]:
        """Detect chapter boundaries using heuristics"""
        sections = []
        current_section = None
        
        for page in pages:
            text = page.text
            
            # Look for chapter indicators
            chapter_patterns = [
                r'^CHAPTER\s+\d+',
                r'^Chapter\s+\d+',
                r'^PART\s+[IVX]+',
                r'^Part\s+[IVX]+',
                r'^\d+\.\s+[A-Z]',  # Numbered sections
            ]
            
            for pattern in chapter_patterns:
                match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
                if match:
                    # End previous section
                    if current_section:
                        current_section['end_page'] = page.page_number - 1
                        sections.append(BookSection(**current_section))
                    
                    # Start new section
                    title = self._extract_chapter_title(text, match.start())
                    current_section = {
                        'title': title,
                        'start_page': page.page_number,
                        'end_page': page.page_number,
                        'content': '',
                        'section_type': 'chapter'
                    }
                    break
            
            # Add content to current section
            if current_section:
                current_section['content'] += text + '\n'
        
        # Close final section
        if current_section:
            current_section['end_page'] = pages[-1].page_number
            sections.append(BookSection(**current_section))
        
        self.sections = sections
        return sections
    
    def _extract_chapter_title(self, text: str, start_pos: int) -> str:
        """Extract chapter title from text starting at position"""
        lines = text[start_pos:].split('\n')
        title_lines = []
        
        for line in lines[:3]:  # Look at first 3 lines
            line = line.strip()
            if line and not line.isdigit():
                title_lines.append(line)
            if len(title_lines) >= 2:  # Usually title is 1-2 lines
                break
                
        return ' '.join(title_lines) if title_lines else "Untitled Chapter"
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers (simple heuristic)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove headers/footers (repeated text patterns)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 3:  # Skip very short lines that might be artifacts
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def get_book_metadata(self, pdf_path: str) -> Dict[str, str]:
        """Extract metadata from PDF"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()
            
            return {
                'title': metadata.get('title', 'Unknown Title'),
                'author': metadata.get('author', 'Unknown Author'),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', '')
            }
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {
                'title': 'Unknown Title',
                'author': 'Unknown Author',
                'subject': '',
                'creator': '',
                'producer': '',
                'creation_date': '',
                'modification_date': ''
            }
    
    def chunk_text_for_tts(self, text: str, max_chunk_size: int = 4000) -> List[str]:
        """Split text into chunks suitable for TTS processing"""
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence would exceed limit, start new chunk
            if len(current_chunk) + len(sentence) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # Sentence itself is too long, split by words
                    words = sentence.split()
                    for word in words:
                        if len(current_chunk) + len(word) > max_chunk_size:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = word
                            else:
                                chunks.append(word)  # Single word longer than limit
                        else:
                            current_chunk += " " + word if current_chunk else word
            else:
                current_chunk += ". " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
