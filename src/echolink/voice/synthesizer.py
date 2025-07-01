"""
Voice Synthesizer Module

This module handles text-to-speech conversion using ElevenLabs API
"""

import io
import tempfile
from pathlib import Path
from typing import Optional, Union
from elevenlabs import generate, save, Voice, VoiceSettings
from pydub import AudioSegment
from pydub.playback import play
import logging

from ..config.settings import settings


logger = logging.getLogger(__name__)


class VoiceSynthesizer:
    """Handles text-to-speech synthesis using ElevenLabs"""
    
    def __init__(self, api_key: Optional[str] = None, voice_id: Optional[str] = None):
        """Initialize the voice synthesizer
        
        Args:
            api_key: ElevenLabs API key (defaults to settings)
            voice_id: Voice ID to use (defaults to settings)
        """
        self.api_key = api_key or settings.elevenlabs_api_key
        self.voice_id = voice_id or settings.elevenlabs_voice_id
        
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required")
        
        # Configure voice settings
        self.voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True
        )
    
    def synthesize_text(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """Convert text to speech audio
        
        Args:
            text: Text to convert to speech
            voice_id: Override default voice ID
            
        Returns:
            Audio data as bytes
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Use provided voice_id or fall back to instance default
            use_voice_id = voice_id or self.voice_id
            
            logger.info(f"Synthesizing text: {text[:50]}...")
            
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=use_voice_id,
                    settings=self.voice_settings
                ),
                api_key=self.api_key
            )
            
            return audio
            
        except Exception as e:
            logger.error(f"Failed to synthesize text: {e}")
            raise
    
    def play_text(self, text: str, voice_id: Optional[str] = None) -> None:
        """Convert text to speech and play it immediately
        
        Args:
            text: Text to convert and play
            voice_id: Override default voice ID
        """
        try:
            audio_data = self.synthesize_text(text, voice_id)
            
            # Create a temporary file to play the audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file.flush()
                
                # Load and play the audio
                audio_segment = AudioSegment.from_mp3(temp_file.name)
                
                # Apply volume adjustment
                if settings.voice_volume != 1.0:
                    volume_db = 20 * (settings.voice_volume - 1)  # Convert to dB
                    audio_segment = audio_segment + volume_db
                
                play(audio_segment)
                
                # Clean up
                Path(temp_file.name).unlink()
                
        except Exception as e:
            logger.error(f"Failed to play text: {e}")
            raise
    
    def save_text_as_audio(self, text: str, output_path: Union[str, Path], 
                          voice_id: Optional[str] = None) -> None:
        """Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            output_path: Path to save the audio file
            voice_id: Override default voice ID
        """
        try:
            audio_data = self.synthesize_text(text, voice_id)
            
            # Save the audio file
            with open(output_path, 'wb') as f:
                f.write(audio_data)
                
            logger.info(f"Audio saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise
    
    def get_available_voices(self) -> list:
        """Get list of available voices from ElevenLabs
        
        Returns:
            List of available voice information
        """
        try:
            from elevenlabs import voices
            
            voice_list = voices(api_key=self.api_key)
            return voice_list
            
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            return []
    
    def test_synthesis(self) -> bool:
        """Test if voice synthesis is working
        
        Returns:
            True if synthesis test passes, False otherwise
        """
        try:
            test_text = "EchoLink voice synthesis test."
            self.synthesize_text(test_text)
            logger.info("Voice synthesis test passed")
            return True
            
        except Exception as e:
            logger.error(f"Voice synthesis test failed: {e}")
            return False 