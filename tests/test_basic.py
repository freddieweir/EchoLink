#!/usr/bin/env python3
"""
Basic test script for EchoLink

This script tests the core functionality without requiring API keys.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.echolink.config.settings import settings
        print("✅ Settings module imported successfully")
        
        from src.echolink.core.monitor import TextMonitor
        print("✅ TextMonitor imported successfully")
        
        from src.echolink.core.summarizer import TextSummarizer
        print("✅ TextSummarizer imported successfully")
        
        # Voice synthesizer will fail without API key, that's expected
        try:
            from src.echolink.voice.synthesizer import VoiceSynthesizer
            print("✅ VoiceSynthesizer imported successfully")
        except Exception as e:
            print(f"⚠️  VoiceSynthesizer import warning: {e}")
        
        try:
            from src.echolink.ui.cli import CLIInterface
            print("✅ CLIInterface imported successfully")
        except Exception as e:
            print(f"⚠️  CLIInterface import warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without API dependencies"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test settings
        from src.echolink.config.settings import settings
        print(f"✅ Settings loaded - Debug mode: {settings.debug_mode}")
        
        # Test text monitor
        from src.echolink.core.monitor import TextMonitor
        monitor = TextMonitor()
        status = monitor.get_monitoring_status()
        print(f"✅ TextMonitor created - Status: {status['clipboard_monitoring']}")
        
        # Test text summarizer
        from src.echolink.core.summarizer import TextSummarizer
        summarizer = TextSummarizer()
        
        test_text = "This is a test text for the summarizer. It should be processed correctly and cleaned up for voice synthesis."
        cleaned = summarizer.clean_text(test_text)
        print(f"✅ TextSummarizer working - Cleaned {len(test_text)} -> {len(cleaned)} chars")
        
        # Test text processing
        processed = summarizer.process_for_voice(test_text)
        print(f"✅ Text processing working - Output: {processed[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n🧪 Testing configuration...")
    
    try:
        from src.echolink.config.settings import settings
        
        print(f"✅ Clipboard monitoring: {settings.clipboard_monitor_enabled}")
        print(f"✅ Summarization: {settings.summarization_enabled}")
        print(f"✅ Max summary length: {settings.max_summary_length}")
        print(f"✅ CLI colors: {settings.cli_colors_enabled}")
        
        # Check if API keys are configured
        has_elevenlabs = bool(settings.elevenlabs_api_key)
        has_openai = bool(settings.openai_api_key)
        
        print(f"🔑 ElevenLabs API: {'✅ Configured' if has_elevenlabs else '❌ Not configured'}")
        print(f"🔑 OpenAI API: {'✅ Configured' if has_openai else '❌ Not configured'}")
        
        if not has_elevenlabs:
            print("💡 Add ELEVENLABS_API_KEY to .env file for voice synthesis")
        
        if not has_openai:
            print("💡 Add OPENAI_API_KEY to .env file for AI summarization")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎙️ EchoLink Basic Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_basic_functionality() 
    all_passed &= test_configuration()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All basic tests passed! EchoLink is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Copy config.example.env to .env")
        print("   2. Add your ElevenLabs API key to .env")
        print("   3. Run: python echolink.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 