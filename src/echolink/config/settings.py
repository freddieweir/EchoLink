"""
EchoLink Configuration Settings

This module handles all configuration loading from environment variables
with proper defaults and validation.
"""

import os
from pathlib import Path
from typing import Optional, Union
from dotenv import load_dotenv


class EchoLinkSettings:
    """Central configuration management for EchoLink"""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize settings by loading from environment file"""
        self._load_env_file(env_file)
        self._validate_required_settings()
    
    def _load_env_file(self, env_file: Optional[str] = None):
        """Load environment variables from .env file"""
        if env_file:
            env_path = Path(env_file)
        else:
            # Look for .env in current directory and parent directories
            current_dir = Path.cwd()
            env_path = current_dir / ".env"
            
            # If not found, check parent directories
            while not env_path.exists() and current_dir.parent != current_dir:
                current_dir = current_dir.parent
                env_path = current_dir / ".env"
        
        if env_path.exists():
            load_dotenv(env_path)
    
    def _validate_required_settings(self):
        """Validate that required settings are present"""
        required_settings = [
            'ELEVENLABS_API_KEY',
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not getattr(self, setting.lower(), None):
                missing_settings.append(setting)
        
        if missing_settings:
            raise ValueError(
                f"Missing required settings: {', '.join(missing_settings)}. "
                "Please check your .env file or environment variables."
            )
    
    # ElevenLabs API Configuration
    @property
    def elevenlabs_api_key(self) -> str:
        return os.getenv('ELEVENLABS_API_KEY', '')
    
    @property
    def elevenlabs_voice_id(self) -> str:
        return os.getenv('ELEVENLABS_VOICE_ID', 'default')
    
    # OpenAI API Configuration
    @property
    def openai_api_key(self) -> str:
        return os.getenv('OPENAI_API_KEY', '')
    
    @property
    def openai_model(self) -> str:
        return os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Voice Settings
    @property
    def voice_speed(self) -> float:
        return float(os.getenv('VOICE_SPEED', '1.0'))
    
    @property
    def voice_volume(self) -> float:
        return float(os.getenv('VOICE_VOLUME', '0.8'))
    
    # Monitor Settings
    @property
    def clipboard_monitor_enabled(self) -> bool:
        return os.getenv('CLIPBOARD_MONITOR_ENABLED', 'true').lower() == 'true'
    
    @property
    def clipboard_monitor_interval(self) -> float:
        return float(os.getenv('CLIPBOARD_MONITOR_INTERVAL', '1.0'))
    
    # UI Settings
    @property
    def cli_theme(self) -> str:
        return os.getenv('CLI_THEME', 'dark')
    
    @property
    def cli_colors_enabled(self) -> bool:
        return os.getenv('CLI_COLORS_ENABLED', 'true').lower() == 'true'
    
    # Summarization Settings
    @property
    def summarization_enabled(self) -> bool:
        return os.getenv('SUMMARIZATION_ENABLED', 'true').lower() == 'true'
    
    @property
    def max_summary_length(self) -> int:
        return int(os.getenv('MAX_SUMMARY_LENGTH', '150'))
    
    @property
    def min_text_length(self) -> int:
        return int(os.getenv('MIN_TEXT_LENGTH', '50'))
    
    # Debug Settings
    @property
    def debug_mode(self) -> bool:
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO').upper()


# Global settings instance
settings = EchoLinkSettings() 