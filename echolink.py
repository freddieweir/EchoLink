#!/usr/bin/env python3
"""
EchoLink - Voice Interface for Cursor AI

Main entry point for the EchoLink application.
This tool converts Cursor's AI responses into voice summaries.
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.echolink.config.settings import settings
from src.echolink.ui.cli import CLIInterface
from src.echolink.voice.synthesizer import VoiceSynthesizer
from src.echolink.core.monitor import TextMonitor
from src.echolink.core.summarizer import TextSummarizer


class EchoLinkApp:
    """Main EchoLink application"""
    
    def __init__(self):
        """Initialize the EchoLink application"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.ui = CLIInterface()
        self.voice_synthesizer = None
        self.text_monitor = TextMonitor()
        self.text_summarizer = TextSummarizer()
        
        # Application state
        self.monitoring_active = False
        self.processed_count = 0
        
        self.logger.info("EchoLink application initialized")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = getattr(logging, settings.log_level, logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('echolink.log'),
                logging.StreamHandler() if settings.debug_mode else logging.NullHandler()
            ]
        )
    
    def initialize_voice_synthesizer(self) -> bool:
        """Initialize the voice synthesizer
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if not settings.elevenlabs_api_key:
                self.logger.warning("ElevenLabs API key not configured")
                return False
            
            self.voice_synthesizer = VoiceSynthesizer()
            
            # Test the synthesizer
            if self.voice_synthesizer.test_synthesis():
                self.logger.info("Voice synthesizer initialized successfully")
                self.ui.update_status(api_connected=True)
                return True
            else:
                self.logger.error("Voice synthesizer test failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to initialize voice synthesizer: {e}")
            return False
    
    def on_text_detected(self, text: str):
        """Handle text detected by the monitor
        
        Args:
            text: The detected text
        """
        try:
            self.logger.info(f"Processing detected text: {text[:50]}...")
            
            # Update UI status
            self.processed_count += 1
            self.ui.update_status(
                processed_count=self.processed_count,
                last_processed=datetime.now()
            )
            
            # Process text for voice
            processed_text = self.text_summarizer.process_for_voice(text)
            
            if not processed_text.strip():
                self.logger.warning("No text to synthesize after processing")
                return
            
                         # Synthesize and play voice
             if self.voice_synthesizer is not None:
                 self.voice_synthesizer.play_text(processed_text)
                 self.logger.info("Voice synthesis completed")
             else:
                 self.logger.warning("Voice synthesizer not available")
                
        except Exception as e:
            self.logger.error(f"Error processing detected text: {e}")
    
    def start_monitoring(self):
        """Start text monitoring"""
        try:
            if self.monitoring_active:
                self.ui.show_message("Monitoring is already active!", "Warning", "warning")
                return
            
            # Initialize voice synthesizer if not done
            if not self.voice_synthesizer:
                self.ui.show_progress("Initializing voice synthesizer")
                if not self.initialize_voice_synthesizer():
                    self.ui.show_message(
                        "Failed to initialize voice synthesizer. Check your API keys and settings.",
                        "Error",
                        "error"
                    )
                    return
            
            # Set up text callback
            self.text_monitor.add_text_callback(self.on_text_detected)
            
            # Start monitoring
            self.ui.show_progress("Starting clipboard monitoring")
            self.text_monitor.start_clipboard_monitoring()
            
            self.monitoring_active = True
            self.ui.update_status(monitoring=True)
            
            self.ui.show_message(
                "Voice monitoring started! Copy text to hear it spoken.",
                "Success",
                "success"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.ui.show_message(f"Failed to start monitoring: {e}", "Error", "error")
    
    def stop_monitoring(self):
        """Stop text monitoring"""
        try:
            if not self.monitoring_active:
                return
            
            self.text_monitor.stop_monitoring()
            self.monitoring_active = False
            self.ui.update_status(monitoring=False)
            
            self.logger.info("Monitoring stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
    
    def test_voice(self):
        """Test voice synthesis"""
        try:
            if not self.voice_synthesizer:
                self.ui.show_progress("Initializing voice synthesizer")
                if not self.initialize_voice_synthesizer():
                    self.ui.show_message(
                        "Failed to initialize voice synthesizer. Check your API keys.",
                        "Error",
                        "error"
                    )
                    return
            
            test_text = "Hello! This is a test of the EchoLink voice synthesis system. Everything is working correctly."
            
            self.ui.show_progress("Testing voice synthesis")
            self.voice_synthesizer.play_text(test_text)
            
            self.ui.show_message("Voice test completed!", "Success", "success")
            
        except Exception as e:
            self.logger.error(f"Voice test failed: {e}")
            self.ui.show_message(f"Voice test failed: {e}", "Error", "error")
    
    def handle_menu_action(self, action: str) -> bool:
        """Handle menu actions from the UI
        
        Args:
            action: The action to handle
            
        Returns:
            True to continue running, False to exit
        """
        try:
            if action == "start_monitoring":
                self.start_monitoring()
                
            elif action == "settings_menu":
                self.ui.change_menu("settings")
                
            elif action == "test_voice":
                self.test_voice()
                
            elif action == "show_status":
                self.show_detailed_status()
                
            elif action == "show_help":
                # Help is shown in the UI layout
                pass
                
            elif action == "back":
                self.ui.change_menu("back")
                
            elif action == "exit":
                return False
                
            elif action == "voice_settings":
                self.ui.show_message("Voice settings not yet implemented", "Info", "info")
                
            elif action == "monitor_settings":
                self.ui.show_message("Monitor settings not yet implemented", "Info", "info")
                
            elif action == "ui_settings":
                self.ui.show_message("UI settings not yet implemented", "Info", "info")
                
            elif action == "api_settings":
                self.ui.show_message("API settings not yet implemented", "Info", "info")
                
            else:
                self.logger.warning(f"Unknown action: {action}")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error handling action '{action}': {e}")
            self.ui.show_message(f"Error: {e}", "Error", "error")
            return True
    
    def show_detailed_status(self):
        """Show detailed status information"""
        try:
            # Get monitoring status
            monitor_status = self.text_monitor.get_monitoring_status()
            
            status_lines = [
                f"Monitoring: {'🟢 Active' if self.monitoring_active else '🔴 Inactive'}",
                f"API Connected: {'🟢 Yes' if self.voice_synthesizer else '🔴 No'}",
                f"Processed Count: 📝 {self.processed_count}",
                f"Active Callbacks: {monitor_status['active_callbacks']}",
                f"Text Cache Size: {monitor_status['processed_texts_count']}",
                "",
                "Settings:",
                f"  Clipboard Monitor: {'✅' if monitor_status['settings']['enabled'] else '❌'}",
                f"  Monitor Interval: {monitor_status['settings']['interval']}s",
                f"  Min Text Length: {monitor_status['settings']['min_text_length']} chars",
                f"  Summarization: {'✅' if settings.summarization_enabled else '❌'}",
                f"  Debug Mode: {'✅' if settings.debug_mode else '❌'}",
            ]
            
            status_text = "\n".join(status_lines)
            self.ui.show_message(status_text, "Detailed Status", "info")
            
        except Exception as e:
            self.logger.error(f"Error showing status: {e}")
            self.ui.show_message(f"Error getting status: {e}", "Error", "error")
    
    def run(self):
        """Run the main application"""
        try:
            self.logger.info("Starting EchoLink application")
            
            # Show welcome message
            self.ui.show_message(
                "Welcome to EchoLink! Configure your API keys in .env file for full functionality.",
                "Welcome",
                "info"
            )
            
            # Run the UI
            self.ui.run_interface(self.handle_menu_action)
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            self.ui.show_message(f"Unexpected error: {e}", "Error", "error")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            self.logger.info("Cleaning up EchoLink application")
            self.stop_monitoring()
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point"""
    try:
        app = EchoLinkApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 