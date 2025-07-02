"""
Text Monitor Module

This module handles monitoring and capturing text from various sources
like clipboard, file system, or direct input for voice synthesis.
"""

import time
import threading
from typing import Callable, Optional, Set
import pyperclip
import logging
from datetime import datetime

from ..config.settings import settings


logger = logging.getLogger(__name__)


class TextMonitor:
    """Monitors various text sources and triggers callbacks when new text is detected"""
    
    def __init__(self):
        """Initialize the text monitor"""
        self.clipboard_content: str = ""
        self.monitoring: bool = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.text_callbacks: Set[Callable[[str], None]] = set()
        self.processed_texts: Set[str] = set()  # To avoid processing duplicates
        
    def add_text_callback(self, callback: Callable[[str], None]) -> None:
        """Add a callback function that will be called when new text is detected
        
        Args:
            callback: Function that takes text as parameter
        """
        self.text_callbacks.add(callback)
        logger.debug(f"Added text callback: {callback.__name__}")
    
    def remove_text_callback(self, callback: Callable[[str], None]) -> None:
        """Remove a text callback
        
        Args:
            callback: Callback function to remove
        """
        self.text_callbacks.discard(callback)
        logger.debug(f"Removed text callback: {callback.__name__}")
    
    def _notify_callbacks(self, text: str) -> None:
        """Notify all registered callbacks with new text
        
        Args:
            text: The text to send to callbacks
        """
        if not text.strip():
            return
        
        # Check minimum text length
        if len(text.strip()) < settings.min_text_length:
            logger.debug(f"Text too short ({len(text)} chars), skipping")
            return
        
        # Avoid processing the same text multiple times
        text_hash = str(hash(text.strip().lower()))
        if text_hash in self.processed_texts:
            logger.debug("Text already processed, skipping")
            return
        
        self.processed_texts.add(text_hash)
        
        # Limit the size of processed_texts to prevent memory issues
        if len(self.processed_texts) > 1000:
            # Remove oldest entries (this is a simple approach)
            self.processed_texts = set(list(self.processed_texts)[-500:])
        
        logger.info(f"New text detected ({len(text)} chars): {text[:50]}...")
        
        for callback in self.text_callbacks:
            try:
                callback(text)
            except Exception as e:
                logger.error(f"Error in text callback {callback.__name__}: {e}")
    
    def _monitor_clipboard(self) -> None:
        """Monitor clipboard for changes (runs in separate thread)"""
        logger.info("Starting clipboard monitoring")
        
        # Get initial clipboard content
        try:
            self.clipboard_content = pyperclip.paste()
        except Exception as e:
            logger.warning(f"Failed to get initial clipboard content: {e}")
            self.clipboard_content = ""
        
        while self.monitoring:
            try:
                current_content = pyperclip.paste()
                
                # Check if clipboard content has changed
                if current_content != self.clipboard_content:
                    self.clipboard_content = current_content
                    
                    # Filter out very short or empty content
                    if current_content and len(current_content.strip()) >= settings.min_text_length:
                        self._notify_callbacks(current_content)
                
                # Sleep before checking again
                time.sleep(settings.clipboard_monitor_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring clipboard: {e}")
                time.sleep(1)  # Wait a bit before retrying
    
    def start_clipboard_monitoring(self) -> None:
        """Start monitoring clipboard for text changes"""
        if not settings.clipboard_monitor_enabled:
            logger.info("Clipboard monitoring is disabled in settings")
            return
        
        if self.monitoring:
            logger.warning("Clipboard monitoring is already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_clipboard,
            daemon=True,
            name="ClipboardMonitor"
        )
        self.monitor_thread.start()
        logger.info("Clipboard monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop all monitoring activities"""
        if not self.monitoring:
            return
        
        logger.info("Stopping text monitoring")
        self.monitoring = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
            if self.monitor_thread.is_alive():
                logger.warning("Monitor thread did not stop gracefully")
    
    def process_manual_text(self, text: str) -> None:
        """Manually process text (not from monitoring)
        
        Args:
            text: Text to process
        """
        logger.info(f"Processing manual text: {text[:50]}...")
        self._notify_callbacks(text)
    
    def clear_processed_cache(self) -> None:
        """Clear the cache of processed texts"""
        self.processed_texts.clear()
        logger.info("Cleared processed text cache")
    
    def get_monitoring_status(self) -> dict:
        """Get current monitoring status
        
        Returns:
            Dictionary with monitoring status information
        """
        return {
            "clipboard_monitoring": self.monitoring,
            "active_callbacks": len(self.text_callbacks),
            "processed_texts_count": len(self.processed_texts),
            "thread_alive": self.monitor_thread.is_alive() if self.monitor_thread else False,
            "settings": {
                "enabled": settings.clipboard_monitor_enabled,
                "interval": settings.clipboard_monitor_interval,
                "min_text_length": settings.min_text_length
            }
        } 