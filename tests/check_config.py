#!/usr/bin/env python3
"""
Configuration diagnostic script for EchoLink
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_configuration():
    """Check EchoLink configuration without exposing sensitive data"""
    print("🔍 EchoLink Configuration Diagnostic")
    print("=" * 40)
    
    try:
        from src.echolink.config.settings import settings
        
        # Check ElevenLabs configuration
        print("📢 ElevenLabs Configuration:")
        
        api_key = settings.elevenlabs_api_key
        voice_id = settings.elevenlabs_voice_id
        
        if not api_key:
            print("❌ API Key: Not set")
        elif api_key == "your_elevenlabs_api_key_here":
            print("❌ API Key: Still has placeholder value")
        elif len(api_key) < 10:
            print("❌ API Key: Too short (likely invalid)")
        else:
            print(f"✅ API Key: Set (length: {len(api_key)} chars)")
        
        if not voice_id or voice_id == "default_voice_id_here":
            print("❌ Voice ID: Using placeholder value")
        else:
            print(f"✅ Voice ID: {voice_id}")
        
        # Check OpenAI configuration
        print("\n🧠 OpenAI Configuration:")
        openai_key = settings.openai_api_key
        
        if not openai_key:
            print("❌ API Key: Not set")
        elif openai_key == "your_openai_api_key_here":
            print("❌ API Key: Still has placeholder value")
        else:
            print(f"✅ API Key: Set (length: {len(openai_key)} chars)")
        
        print(f"✅ Model: {settings.openai_model}")
        print(f"✅ Provider: {settings.summarization_provider}")
        
        # Check other settings
        print("\n⚙️ Other Settings:")
        print(f"✅ Voice Speed: {settings.voice_speed}")
        print(f"✅ Voice Volume: {settings.voice_volume}")
        print(f"✅ Monitor Enabled: {settings.clipboard_monitor_enabled}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

if __name__ == "__main__":
    check_configuration()
