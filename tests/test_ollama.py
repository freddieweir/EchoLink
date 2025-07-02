#!/usr/bin/env python3
"""
Ollama connectivity test for EchoLink

This script tests the connection to Ollama and summarization functionality.
"""

import sys
import requests
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_ollama_connection():
    """Test connection to Ollama server"""
    print("🦙 Testing Ollama Connection...")
    
    # Try different common URLs for VM to host communication
    test_urls = [
        "http://host.docker.internal:11434",
        "http://localhost:11434",
        "http://192.168.1.100:11434",  # Common home network IP
        "http://10.0.2.2:11434",       # VirtualBox default host IP
    ]
    
    for url in test_urls:
        try:
            print(f"  Trying: {url}")
            response = requests.get(f"{url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                print(f"  ✅ Connected to Ollama at {url}")
                print(f"  📦 Available models: {len(models.get('models', []))}")
                
                for model in models.get('models', []):
                    print(f"    - {model['name']}")
                
                return url
            else:
                print(f"  ❌ HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Connection failed: {e}")
    
    print("  💡 Try configuring Ollama to listen on all interfaces:")
    print("     OLLAMA_HOST=0.0.0.0:11434 ollama serve")
    return None

def test_ollama_summarization(base_url: str, model: str = "llama2"):
    """Test Ollama summarization functionality"""
    print(f"\n🧠 Testing Ollama Summarization with {model}...")
    
    test_text = """
    This is a longer test text that should be summarized by Ollama. 
    It contains multiple sentences and provides a good test for the 
    summarization functionality. The system should be able to take 
    this text and create a shorter, more concise version that captures 
    the main points while being suitable for text-to-speech conversion.
    """
    
    prompt = f"""Please summarize the following text in a conversational way that's suitable for text-to-speech. 
Keep it under 150 characters and make it sound natural when spoken aloud:

{test_text}

Summary:"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 100
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        summary = result.get("response", "").strip()
        
        print(f"  ✅ Summarization successful!")
        print(f"  📊 Original: {len(test_text)} chars")
        print(f"  📊 Summary: {len(summary)} chars")
        print(f"  📝 Result: {summary}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Summarization failed: {e}")
        return False

def test_echolink_ollama():
    """Test EchoLink with Ollama configuration"""
    print(f"\n🎙️ Testing EchoLink Ollama Integration...")
    
    try:
        from src.echolink.config.settings import settings
        from src.echolink.core.summarizer import TextSummarizer
        
        print(f"  Provider: {settings.summarization_provider}")
        print(f"  URL: {settings.ollama_base_url}")
        print(f"  Model: {settings.ollama_model}")
        
        # Test summarizer
        summarizer = TextSummarizer()
        test_text = "This is a test of the EchoLink summarization system using Ollama for local processing."
        
        summary = summarizer.summarize_text(test_text)
        print(f"  ✅ EchoLink summarization works!")
        print(f"  📝 Result: {summary}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ EchoLink Ollama test failed: {e}")
        return False

def main():
    """Run Ollama tests"""
    print("🦙 EchoLink Ollama Test Suite")
    print("=" * 40)
    
    # Test connection
    ollama_url = test_ollama_connection()
    
    if not ollama_url:
        print("\n❌ Cannot connect to Ollama. Check your setup:")
        print("  1. Is Ollama running on your main machine?")
        print("  2. Is it listening on 0.0.0.0:11434? (OLLAMA_HOST=0.0.0.0:11434)")
        print("  3. Can your VM reach your main machine's network?")
        print("  4. Try updating OLLAMA_BASE_URL in your .env file")
        return 1
    
    # Test summarization
    if not test_ollama_summarization(ollama_url):
        print("❌ Ollama summarization test failed")
        return 1
    
    # Test EchoLink integration
    if not test_echolink_ollama():
        print("❌ EchoLink integration test failed")
        return 1
    
    print("\n" + "=" * 40)
    print("🎉 All Ollama tests passed!")
    print("\n💡 Ready to use EchoLink with Ollama:")
    print("   1. Update SUMMARIZATION_PROVIDER=ollama in .env")
    print("   2. Set OLLAMA_BASE_URL to the working URL above")
    print("   3. Run: python echolink.py")
    
    return 0

if __name__ == "__main__":
    exit(main()) 