"""
Smart content filtering to identify and skip non-essential book sections
"""
import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from backend.pdf_processor import PageContent, BookSection
import logging

logger = logging.getLogger(__name__)

@dataclass
class FilterResult:
    """Result of content filtering"""
    should_skip: bool
    reason: str
    confidence: float  # 0.0 to 1.0

class ContentFilter:
    """Filters out non-essential content from books"""
    
    def __init__(self):
        self.copyright_keywords = {
            'copyright', 'published', 'isbn', 'edition', 'printing', 'publisher',
            'all rights reserved', 'no part of this publication', 'library of congress',
            'cataloging-in-publication', 'printed in', 'first published'
        }
        
        self.acknowledgment_keywords = {
            'acknowledgment', 'acknowledgement', 'thanks to', 'grateful to',
            'dedication', 'dedicated to', 'in memory of', 'special thanks',
            'would like to thank', 'gratitude', 'appreciation'
        }
        
        self.toc_keywords = {
            'contents', 'table of contents', 'chapter', 'part i', 'part ii',
            'appendix', 'index', 'bibliography', 'preface', 'introduction'
        }
        
        self.index_keywords = {
            'index', 'bibliography', 'references', 'works cited', 'further reading',
            'suggested reading', 'notes', 'endnotes', 'footnotes'
        }
        
        self.promotional_keywords = {
            'praise for', 'reviews', 'also by', 'about the author', 'other books',
            'from the reviews', 'acclaim for', 'what readers are saying',
            'testimonials', 'endorsements'
        }
    
    def filter_pages(self, pages: List[PageContent], config: Dict) -> List[PageContent]:
        """Filter pages based on content analysis"""
        filtered_pages = []
        
        for page in pages:
            filter_result = self.analyze_page(page, config)
            
            if not filter_result.should_skip:
                filtered_pages.append(page)
            else:
                logger.info(f"Skipping page {page.page_number}: {filter_result.reason} "
                          f"(confidence: {filter_result.confidence:.2f})")
        
        return filtered_pages
    
    def analyze_page(self, page: PageContent, config: Dict) -> FilterResult:
        """Analyze a single page to determine if it should be skipped"""
        text = page.text.lower()
        
        # Skip very short pages (likely not main content)
        if page.word_count < 50:
            return FilterResult(True, "Too few words", 0.9)
        
        # Check for copyright/publication info
        if config.get('SKIP_COPYRIGHT', True):
            copyright_score = self._calculate_keyword_score(text, self.copyright_keywords)
            if copyright_score > 0.3:
                return FilterResult(True, "Copyright/publication page", copyright_score)
        
        # Check for acknowledgments
        if config.get('SKIP_ACKNOWLEDGMENTS', True):
            ack_score = self._calculate_keyword_score(text, self.acknowledgment_keywords)
            if ack_score > 0.2:
                return FilterResult(True, "Acknowledgments/dedication", ack_score)
        
        # Check for table of contents
        if config.get('SKIP_TOC', True):
            toc_score = self._calculate_toc_score(text)
            if toc_score > 0.4:
                return FilterResult(True, "Table of contents", toc_score)
        
        # Check for index/bibliography
        if config.get('SKIP_INDEX', True):
            index_score = self._calculate_keyword_score(text, self.index_keywords)
            if index_score > 0.3:
                return FilterResult(True, "Index/bibliography", index_score)
        
        # Check for promotional content
        if config.get('SKIP_BIBLIOGRAPHY', True):
            promo_score = self._calculate_keyword_score(text, self.promotional_keywords)
            if promo_score > 0.3:
                return FilterResult(True, "Promotional content", promo_score)
        
        # Check page position (first/last pages often contain metadata)
        position_score = self._analyze_page_position(page, text)
        if position_score > 0.7:
            return FilterResult(True, "Likely metadata page", position_score)
        
        return FilterResult(False, "Main content", 0.0)
    
    def _calculate_keyword_score(self, text: str, keywords: Set[str]) -> float:
        """Calculate how much text matches given keywords"""
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        matches = 0
        for keyword in keywords:
            matches += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
        
        # Normalize by text length
        score = min(matches / (word_count / 100), 1.0)
        return score
    
    def _calculate_toc_score(self, text: str) -> float:
        """Special scoring for table of contents detection"""
        # Look for patterns typical of TOC
        patterns = [
            r'chapter\s+\d+.*\d+$',  # Chapter X ... page number
            r'part\s+[ivx]+.*\d+$',   # Part I ... page number
            r'^\d+\s+[A-Z].*\d+$',    # Number Title ... page number
            r'\.{3,}',                # Dots leading to page numbers
        ]
        
        lines = text.split('\n')
        pattern_matches = 0
        
        for line in lines:
            line = line.strip()
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    pattern_matches += 1
                    break
        
        # If many lines match TOC patterns, likely a TOC
        if len(lines) > 0:
            return min(pattern_matches / len(lines) * 2, 1.0)
        return 0.0
    
    def _analyze_page_position(self, page: PageContent, text: str) -> float:
        """Analyze if page position suggests metadata"""
        # First few pages often contain publication info
        if page.page_number <= 5:
            # Look for typical front matter indicators
            front_indicators = ['copyright', 'published', 'isbn', 'edition']
            score = self._calculate_keyword_score(text, set(front_indicators))
            return min(score * 2, 1.0)  # Boost score for early pages
        
        return 0.0
    
    def filter_sections(self, sections: List[BookSection], config: Dict) -> List[BookSection]:
        """Filter book sections based on content"""
        filtered_sections = []
        
        for section in sections:
            if self._should_keep_section(section, config):
                # Clean the section content
                section.content = self._clean_section_content(section.content)
                filtered_sections.append(section)
            else:
                logger.info(f"Skipping section: {section.title}")
        
        return filtered_sections
    
    def _should_keep_section(self, section: BookSection, config: Dict) -> bool:
        """Determine if a section should be kept"""
        title_lower = section.title.lower()
        content_lower = section.content.lower()
        
        # Skip based on title
        skip_titles = []
        if config.get('SKIP_ACKNOWLEDGMENTS', True):
            skip_titles.extend(['acknowledgment', 'dedication', 'thanks'])
        if config.get('SKIP_TOC', True):
            skip_titles.extend(['contents', 'table of contents'])
        if config.get('SKIP_INDEX', True):
            skip_titles.extend(['index', 'bibliography', 'references'])
        
        for skip_title in skip_titles:
            if skip_title in title_lower:
                return False
        
        # Skip very short sections (likely not main content)
        if len(section.content.split()) < 100:
            return False
        
        return True
    
    def _clean_section_content(self, content: str) -> str:
        """Clean section content for better TTS"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove page numbers
        content = re.sub(r'\n\s*\d+\s*\n', '\n', content)
        
        # Remove common artifacts
        content = re.sub(r'\[.*?\]', '', content)  # Remove bracketed content
        content = re.sub(r'\(page \d+\)', '', content)  # Remove page references
        
        # Clean up punctuation for better speech
        content = re.sub(r'([.!?])\s*([.!?])+', r'\1', content)  # Remove repeated punctuation
        
        return content.strip()
