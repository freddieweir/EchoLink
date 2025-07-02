"""
Text Summarizer Module

This module handles text summarization and processing to make content
more suitable for voice synthesis and conversational delivery.
"""

import re
import logging
from typing import Optional
import openai
import requests
import json

from ..config.settings import settings


logger = logging.getLogger(__name__)


class TextSummarizer:
    """Handles text summarization and processing for voice synthesis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the text summarizer
        
        Args:
            api_key: OpenAI API key (defaults to settings)
        """
        self.api_key = api_key or settings.openai_api_key
        self.openai_client = None
        
        if self.api_key and settings.summarization_provider == 'openai':
            try:
                self.openai_client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
        
        # Log which summarization provider is being used
        logger.info(f"Text summarizer initialized with provider: {settings.summarization_provider}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for better processing
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove markdown formatting for voice
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)  # Code
        text = re.sub(r'#{1,6}\s*', '', text)  # Headers
        
        # Remove URLs (but keep the domain for context)
        text = re.sub(r'https?://([^\s]+)', r'website \1', text)
        
        # Clean up common code artifacts
        text = re.sub(r'```[\s\S]*?```', '[code block]', text)
        text = re.sub(r'`[^`]*`', '[code]', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        return text.strip()
    
    def should_summarize(self, text: str) -> bool:
        """Determine if text should be summarized based on length and settings
        
        Args:
            text: Text to evaluate
            
        Returns:
            True if text should be summarized
        """
        if not settings.summarization_enabled:
            return False
        
        # Don't summarize very short text
        if len(text) < settings.min_text_length * 2:
            return False
        
        # Summarize if text is longer than max_summary_length * 2
        return len(text) > settings.max_summary_length * 2
    
    def simple_summarize(self, text: str) -> str:
        """Simple rule-based summarization without AI
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
        """
        sentences = re.split(r'[.!?]+', text)
        
        # Filter out very short sentences
        meaningful_sentences = [
            s.strip() for s in sentences 
            if len(s.strip()) > 10
        ]
        
        if not meaningful_sentences:
            return text[:settings.max_summary_length] + "..."
        
        # Take first and last sentences for context
        if len(meaningful_sentences) == 1:
            summary = meaningful_sentences[0]
        elif len(meaningful_sentences) == 2:
            summary = ". ".join(meaningful_sentences)
        else:
            summary = f"{meaningful_sentences[0]}. ... {meaningful_sentences[-1]}"
        
        # Ensure it's not too long
        if len(summary) > settings.max_summary_length:
            summary = summary[:settings.max_summary_length] + "..."
        
        return summary
    
    def ai_summarize(self, text: str) -> Optional[str]:
        """Use OpenAI to summarize text intelligently
        
        Args:
            text: Text to summarize
            
        Returns:
            AI-generated summary or None if failed
        """
        if not self.openai_client:
            logger.debug("OpenAI client not available for AI summarization")
            return None
        
        try:
            prompt = f"""Please summarize the following text in a conversational way that's suitable for text-to-speech. 
Keep it under {settings.max_summary_length} characters and make it sound natural when spoken aloud:

{text}

Summary:"""

            response = self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise, conversational summaries suitable for text-to-speech."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Ensure summary isn't too long
            if len(summary) > settings.max_summary_length:
                summary = summary[:settings.max_summary_length] + "..."
            
            logger.info(f"AI summarization successful: {len(text)} -> {len(summary)} chars")
            return summary
            
        except Exception as e:
            logger.error(f"AI summarization failed: {e}")
            return None
    
    def ollama_summarize(self, text: str) -> Optional[str]:
        """Use Ollama to summarize text intelligently
        
        Args:
            text: Text to summarize
            
        Returns:
            Ollama-generated summary or None if failed
        """
        try:
            prompt = f"""Please summarize the following text in a conversational way that's suitable for text-to-speech. 
Keep it under {settings.max_summary_length} characters and make it sound natural when spoken aloud:

{text}

Summary:"""

            # Prepare the request to Ollama
            payload = {
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100  # Limit response length
                }
            }
            
            # Make request to Ollama API
            response = requests.post(
                f"{settings.ollama_base_url}/api/generate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            summary = result.get("response", "").strip()
            
            # Ensure summary isn't too long
            if len(summary) > settings.max_summary_length:
                summary = summary[:settings.max_summary_length] + "..."
            
            logger.info(f"Ollama summarization successful: {len(text)} -> {len(summary)} chars")
            return summary
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Ollama summarization failed: {e}")
            return None
    
    def summarize_text(self, text: str) -> str:
        """Summarize text using the best available method
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
        """
        if not text or not text.strip():
            return ""
        
        # Clean the text first
        cleaned_text = self.clean_text(text)
        
        # Check if summarization is needed
        if not self.should_summarize(cleaned_text):
            return cleaned_text
        
        logger.info(f"Summarizing text ({len(cleaned_text)} chars) using {settings.summarization_provider}")
        
        # Choose summarization method based on provider setting
        if settings.summarization_provider == 'ollama':
            ollama_summary = self.ollama_summarize(cleaned_text)
            if ollama_summary:
                return ollama_summary
            logger.info("Ollama summarization failed, falling back to simple summarization")
        
        elif settings.summarization_provider == 'openai':
            # Try OpenAI summarization
            openai_summary = self.ai_summarize(cleaned_text)
            if openai_summary:
                return openai_summary
            logger.info("OpenAI summarization failed, falling back to simple summarization")
        
        # Fall back to simple summarization for 'simple' provider or when AI fails
        logger.info("Using simple rule-based summarization")
        return self.simple_summarize(cleaned_text)
    
    def process_for_voice(self, text: str) -> str:
        """Process text specifically for voice synthesis
        
        Args:
            text: Text to process
            
        Returns:
            Voice-optimized text
        """
        # First summarize if needed
        processed_text = self.summarize_text(text)
        
        # Additional voice optimizations
        
        # Replace common abbreviations with full words
        replacements = {
            r'\bdr\b': 'doctor',
            r'\bmr\b': 'mister',
            r'\bmrs\b': 'missus',
            r'\bms\b': 'miss',
            r'\betc\b': 'etcetera',
            r'\bvs\b': 'versus',
            r'\bw/\b': 'with',
            r'\bw/o\b': 'without',
            r'\be\.g\.\b': 'for example',
            r'\bi\.e\.\b': 'that is',
        }
        
        for pattern, replacement in replacements.items():
            processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
        
        # Add pauses for better speech flow
        processed_text = re.sub(r'([.!?])\s*([A-Z])', r'\1... \2', processed_text)
        
        # Ensure it ends with proper punctuation
        if processed_text and not processed_text[-1] in '.!?':
            processed_text += '.'
        
        return processed_text
    
    def get_summary_stats(self, original: str, summary: str) -> dict:
        """Get statistics about the summarization
        
        Args:
            original: Original text
            summary: Summarized text
            
        Returns:
            Dictionary with summarization statistics
        """
        return {
            "original_length": len(original),
            "summary_length": len(summary),
            "compression_ratio": len(summary) / len(original) if original else 0,
            "reduction_percentage": (1 - len(summary) / len(original)) * 100 if original else 0,
            "ai_available": self.openai_client is not None,
            "settings": {
                "max_summary_length": settings.max_summary_length,
                "min_text_length": settings.min_text_length,
                "summarization_enabled": settings.summarization_enabled
            }
        } 