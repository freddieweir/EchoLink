# Two-Way Voice Communication

## Overview
Add speech-to-text capability to EchoLink, enabling users to speak responses back to Cursor AI for truly hands-free interaction. This completes the conversation loop: Cursor speaks → User speaks → Cursor responds.

## Current State
- ✅ **Cursor → User**: Text responses converted to speech
- ❌ **User → Cursor**: Manual typing required

## Proposed Solution
Implement voice input system that transcribes speech to text and sends it back to Cursor automatically.

## Implementation Plan

### Phase 1: Basic Speech-to-Text
```python
# New module: src/echolink/voice/listener.py
class VoiceListener:
    def __init__(self):
        self.microphone = None
        self.recognizer = None
        self.listening = False
    
    def start_listening(self, hotkey: str = "F12"):
        """Start listening for voice input on hotkey press"""
    
    def transcribe_audio(self, audio_data) -> str:
        """Convert audio to text using OpenAI Whisper or alternative"""
```

### Phase 2: Integration Options

#### Option A: Hotkey Activation (Recommended)
- Press `F12` → Start recording
- Speak command/question  
- Release `F12` → Stop recording, transcribe, send to Cursor
- Visual/audio feedback during recording

#### Option B: Continuous Listening
- Always listening for wake phrase: "Hey EchoLink"
- After wake phrase, listen for command
- Automatic end-of-speech detection
- More natural but battery intensive

#### Option C: Push-to-Talk Button
- Physical button or GUI button
- Click and hold to record
- Release to process
- Good for privacy/control

### Phase 3: Command Processing
```python
class VoiceCommandProcessor:
    def parse_voice_command(self, transcribed_text: str) -> dict:
        """Parse voice input and determine action"""
        # Commands:
        # "Ask Cursor: how do I implement recursion?"
        # "Tell Cursor to explain this code"
        # "Send to Cursor: refactor this function"
        
    def send_to_cursor(self, text: str, method: str = "clipboard"):
        """Send processed text back to Cursor"""
        # Options: clipboard, file, HTTP API
```

## Technical Implementation

### Speech Recognition Options

#### Option 1: OpenAI Whisper (Recommended)
```python
import openai

def transcribe_with_whisper(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"  # or auto-detect
        )
    return transcript.text
```

**Pros**: High accuracy, works offline (if using local Whisper), supports many languages
**Cons**: Requires OpenAI API credits or local model

#### Option 2: Google Speech Recognition
```python
import speech_recognition as sr

def transcribe_with_google(audio_data) -> str:
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
```

**Pros**: Free, good accuracy, real-time
**Cons**: Requires internet connection

#### Option 3: Apple Speech (macOS only)
```python
# Using macOS Speech Recognition framework
import subprocess

def transcribe_with_apple_speech(audio_file: str) -> str:
    # Use built-in macOS speech recognition
    result = subprocess.run([
        'osascript', '-e', 
        f'tell application "Speech Recognition Server" to listen for "{audio_file}"'
    ])
```

**Pros**: Native macOS integration, privacy-focused
**Cons**: macOS only, limited API

### Audio Capture
```python
import pyaudio
import wave

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
    
    def start_recording(self):
        """Start recording audio from microphone"""
        
    def stop_recording(self) -> str:
        """Stop recording and save to temp file"""
        
    def get_audio_devices(self):
        """List available microphone devices"""
```

### Hotkey Management
```python
import keyboard  # or pynput

class HotkeyManager:
    def __init__(self):
        self.hotkeys = {}
        
    def register_hotkey(self, key: str, callback: Callable):
        """Register a hotkey for voice activation"""
        # F12 for push-to-talk
        # Ctrl+Shift+V for voice command
        
    def setup_push_to_talk(self, key: str = "F12"):
        """Setup push-to-talk functionality"""
```

## User Workflows

### Workflow 1: Push-to-Talk
1. User presses and holds `F12`
2. EchoLink shows "🎤 Recording..." in UI
3. User speaks: "Ask Cursor how to implement binary search"
4. User releases `F12`
5. EchoLink transcribes speech
6. Sends "How to implement binary search" to Cursor (clipboard/file)
7. Cursor responds → EchoLink speaks the response

### Workflow 2: Command Mode
1. User presses `F11` (command mode)
2. EchoLink listens for complete sentence
3. User speaks: "Explain this error message"
4. EchoLink detects silence, transcribes
5. Sends command to Cursor
6. Full voice conversation continues

### Workflow 3: Continuous Conversation
1. File monitoring detects Cursor response
2. EchoLink speaks response
3. Automatically starts listening for user reply
4. User speaks follow-up question
5. Loop continues for natural conversation

## Configuration Options

### New .env Settings
```env
# Voice Input Settings
VOICE_INPUT_ENABLED=true
SPEECH_RECOGNITION_PROVIDER=whisper  # whisper, google, apple
PUSH_TO_TALK_KEY=F12
RECORDING_TIMEOUT=30
AUTO_LISTEN_AFTER_RESPONSE=false

# Audio Settings  
MICROPHONE_DEVICE_INDEX=0
AUDIO_SAMPLE_RATE=16000
AUDIO_CHUNK_SIZE=1024

# Command Processing
VOICE_COMMAND_PREFIX="ask cursor"  # "ask cursor: how do I..."
AUTO_SEND_TO_CURSOR=true
CURSOR_INPUT_METHOD=clipboard  # clipboard, file, api
```

### UI Integration
```python
# Update CLI menus
"voice_input": {
    "title": "🎤 Voice Input Settings",
    "options": [
        {"label": "🎙️ Test Microphone", "action": "test_microphone"},
        {"label": "⚙️ Configure Hotkeys", "action": "hotkey_settings"},
        {"label": "🗣️ Speech Recognition", "action": "speech_settings"},
        {"label": "↩️ Back", "action": "back"}
    ]
}
```

## Implementation Steps

### Step 1: Basic Voice Recording (3-4 hours)
1. Add audio recording with pyaudio
2. Implement push-to-talk with keyboard hotkeys
3. Create temporary audio file management
4. Add microphone testing functionality

### Step 2: Speech Recognition (2-3 hours)
1. Integrate OpenAI Whisper API
2. Add Google Speech Recognition as fallback
3. Implement transcription error handling
4. Add configuration options for providers

### Step 3: Cursor Integration (3-4 hours)
1. Parse voice commands for Cursor context
2. Implement text sending (clipboard method first)
3. Add command filtering and validation
4. Test complete conversation workflow

### Step 4: Advanced Features (4-6 hours)
1. Automatic listening after responses
2. Voice activity detection (stop on silence)
3. Multiple hotkey support
4. Audio feedback (beeps, status sounds)

## Dependencies
```txt
# Add to requirements.txt
pyaudio>=0.2.11          # Audio recording
SpeechRecognition>=3.10.0 # Speech recognition
pynput>=1.7.6            # Hotkey management (alternative to keyboard)
```

## Testing Plan
```python
# Unit tests
def test_audio_recording():
    """Test audio recording and file creation"""

def test_speech_transcription():
    """Test transcription with sample audio files"""

def test_hotkey_registration():
    """Test hotkey activation and deactivation"""

# Integration tests  
def test_voice_to_cursor_workflow():
    """Test complete voice input → Cursor workflow"""
```

## Privacy & Security Considerations
- ⚠️ **Audio Privacy**: Voice data sent to OpenAI/Google
- ✅ **Local Option**: Use local Whisper model for privacy
- ✅ **Push-to-Talk**: User controls when recording happens
- ✅ **Audio Cleanup**: Delete temporary audio files
- ✅ **Opt-in**: Voice features disabled by default

## Success Criteria
- [ ] Record clear audio from microphone
- [ ] Accurately transcribe speech to text (>90% accuracy)
- [ ] Send transcribed text to Cursor automatically
- [ ] Complete voice conversation loop works end-to-end
- [ ] Hotkey activation works reliably
- [ ] Privacy controls implemented (local processing option)
- [ ] Seamless integration with existing EchoLink features

## Future Enhancements
- Voice command shortcuts ("Code review", "Explain", "Debug")
- Speaker identification for multi-user scenarios
- Custom voice models/training
- Integration with other AI tools beyond Cursor
- Voice-controlled EchoLink settings ("Slower", "Louder")
- Real-time transcription display
- Voice conversation history/logging 