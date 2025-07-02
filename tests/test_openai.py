#!/usr/bin/env python3
"""
OpenAI integration test for EchoLink
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_openai_summarization():
    """Test OpenAI summarization functionality"""
    print("🧠 Testing OpenAI Summarization...")
    
    try:
        from src.echolink.core.summarizer import TextSummarizer
        from src.echolink.config.settings import settings
        
        print(f"  Provider: {settings.summarization_provider}")
        print(f"  Model: {settings.openai_model}")
        print(f"  API Key: {'✅ Set' if settings.openai_api_key else '❌ Missing'}")
        
        # Test summarizer
        summarizer = TextSummarizer()
        
        test_text = """
        This is a comprehensive test of the EchoLink voice interface system. The application 
        is designed to work with Cursor AI by monitoring the clipboard for new text content, 
        processing and summarizing that content using AI, and then converting it to speech 
        using ElevenLabs voice synthesis. This allows users to receive audio feedback from 
        their AI assistant, making the coding experience more accessible and efficient.
        """
        
        print(f"  📊 Original text: {len(test_text)} characters")
        
        # Test summarization
        summary = summarizer.summarize_text(test_text.strip())
        
        print(f"  📊 Summary: {len(summary)} characters")
        print(f"  📝 Result: {summary}")
        
        print("  ✅ OpenAI summarization working!")
        return True
        
    except Exception as e:
        print(f"  ❌ OpenAI test failed: {e}")
        return False

def main():
    """Run OpenAI integration tests"""
    print("🧠 EchoLink OpenAI Integration Test")
    print("=" * 40)
    
    if test_openai_summarization():
        print("\n" + "=" * 40)
        print("🎉 OpenAI integration working perfectly!")
        print("\n💡 Ready to use EchoLink:")
        print("   python echolink.py")
        return 0
    else:
        print("❌ OpenAI test failed.")
        return 1

if __name__ == "__main__":
    exit(main())
