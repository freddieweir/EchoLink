#!/usr/bin/env python3
"""
Direct ElevenLabs API test
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_elevenlabs_direct():
    """Test ElevenLabs API directly"""
    print("🎙️ Testing ElevenLabs API Directly")
    print("=" * 40)
    
    try:
        from src.echolink.config.settings import settings
        from elevenlabs.client import ElevenLabs
        
        print(f"API Key Length: {len(settings.elevenlabs_api_key)} chars")
        print(f"Voice ID: {settings.elevenlabs_voice_id}")
        
        # Create client
        client = ElevenLabs(api_key=settings.elevenlabs_api_key)
        
        # Test 1: Get available voices
        print("\n🎭 Testing: Get available voices...")
        try:
            voices = client.voices.get_all()
            print(f"✅ Found {len(voices.voices)} voices")
            
            # Check if our voice ID exists
            our_voice = None
            for voice in voices.voices:
                if voice.voice_id == settings.elevenlabs_voice_id:
                    our_voice = voice
                    break
            
            if our_voice:
                print(f"✅ Voice '{our_voice.name}' found and accessible")
            else:
                print(f"⚠️  Voice ID '{settings.elevenlabs_voice_id}' not found in available voices")
                print("Available voices:")
                for voice in voices.voices[:5]:  # Show first 5
                    print(f"  - {voice.name} ({voice.voice_id})")
        
        except Exception as e:
            print(f"❌ Failed to get voices: {e}")
            return False
        
        # Test 2: Synthesize a short text
        print("\n🔊 Testing: Text synthesis...")
        try:
            test_text = "Hello world"
            audio = client.text_to_speech.convert(
                text=test_text,
                voice_id=settings.elevenlabs_voice_id
            )
            
            # Convert to bytes to test
            audio_bytes = b"".join(audio)
            print(f"✅ Synthesis successful! Generated {len(audio_bytes)} bytes of audio")
            return True
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ ElevenLabs test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_elevenlabs_direct()
    if success:
        print("\n🎉 ElevenLabs is working correctly!")
    else:
        print("\n❌ ElevenLabs test failed. Check your API key and voice ID.")
