# EchoLink - Voice Interface for Cursor AI

Transform Cursor's AI responses into voice summaries with EchoLink! This tool listens to your clipboard, summarizes AI responses, and speaks them aloud using high-quality voice synthesis.

## Features

🎙️ **Real-time Voice Synthesis**: Converts text to speech using ElevenLabs API  
📋 **Clipboard Monitoring**: Automatically detects new text from Cursor AI  
🧠 **Smart Summarization**: AI-powered text summarization for better listening  
🎨 **Rich CLI Interface**: Colorful, ADHD-friendly UI with arrow key navigation  
⚙️ **Configurable Settings**: Customize voice, monitoring, and UI preferences  
🚀 **Easy Setup**: Simple configuration and installation process  

## Quick Start

🚀 **New to EchoLink?** Start with our comprehensive [Setup Guide](Docs/SETUP.md)

### 1. Installation

```bash
# Clone and setup
cd EchoLink
python -m venv ~/venv/echolink
source ~/venv/echolink/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example configuration
cp config.example.env .env

# Edit .env and add your API keys:
# ELEVENLABS_API_KEY=your_api_key_here
# OPENAI_API_KEY=your_openai_key_here (optional)
```

### 3. Run

```bash
# Test basic functionality
python tests/test_basic.py

# Launch EchoLink
python echolink.py
```

📖 **Need help?** Check [Troubleshooting Guide](Docs/TROUBLESHOOTING.md) for common issues.

## Usage

### Interactive Menu

Use arrow keys (↑/↓) to navigate, Enter to select:

- 🚀 **Start Voice Monitoring**: Begin listening to clipboard
- ⚙️ **Settings**: Configure voice and monitoring options  
- 🎤 **Test Voice**: Test voice synthesis
- 📊 **Status**: View detailed system status
- ❓ **Help**: Show navigation help

### Workflow

1. **Start Monitoring**: Select "Start Voice Monitoring" from the menu
2. **Copy Text**: Copy any text from Cursor AI to your clipboard
3. **Listen**: EchoLink automatically speaks the summarized content
4. **Continue**: Keep working while EchoLink provides audio feedback

## Configuration Options

### API Keys (Required)

```env
# ElevenLabs (Required for voice synthesis)
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=default

# OpenAI (Optional, for AI summarization)
OPENAI_API_KEY=your_key_here
```

### Voice Settings

```env
VOICE_SPEED=1.0          # Speech speed (0.5-2.0)
VOICE_VOLUME=0.8         # Volume level (0.0-1.0)
```

### Monitoring Settings

```env
CLIPBOARD_MONITOR_ENABLED=true
CLIPBOARD_MONITOR_INTERVAL=1.0    # Check interval in seconds
MIN_TEXT_LENGTH=50                # Minimum text length to process
```

### UI Settings

```env
CLI_THEME=dark           # dark or light
CLI_COLORS_ENABLED=true  # Enable colorful interface
```

## Architecture

```
EchoLink/
├── echolink.py              # Main application entry point
├── src/echolink/            # Source code modules
│   ├── config/              # Configuration management
│   ├── core/                # Core functionality (monitoring, summarization)
│   ├── voice/               # Voice synthesis (ElevenLabs integration)
│   └── ui/                  # User interface (Rich CLI)
├── tests/                   # Test files and diagnostics
├── Docs/                    # 📚 Comprehensive documentation
│   ├── SETUP.md            # Installation and configuration guide
│   ├── TROUBLESHOOTING.md  # Common issues and solutions
│   ├── SECURITY.md         # Security guidelines and best practices
│   ├── specs/              # Feature specifications and roadmap
│   └── templates/          # Documentation templates
├── requirements.txt         # Core dependencies
├── config.example.env       # Configuration template
└── .env                    # Your configuration file
```

## Key Components

### 🎙️ VoiceSynthesizer
- ElevenLabs API integration
- High-quality text-to-speech
- Configurable voice settings
- Audio playback and file saving

### 📋 TextMonitor  
- Real-time clipboard monitoring
- Duplicate detection and filtering
- Configurable monitoring intervals
- Thread-safe operation

### 🧠 TextSummarizer
- AI-powered summarization (OpenAI)
- Fallback rule-based summarization
- Text cleaning and optimization
- Voice-friendly text processing

### 🎨 CLI Interface
- Rich colors and layouts
- Arrow key navigation
- ADHD-friendly design
- Real-time status updates
- Emoji-enhanced menus

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
source ~/venv/echolink/bin/activate

# Reinstall dependencies
pip install -r requirements-core.txt
```

### API Issues
- Verify API keys in `.env` file
- Check ElevenLabs account quota
- Test with voice synthesis test feature

### Voice Playback Issues
- Check system audio settings
- Verify pydub dependencies
- Test with different voice settings

## Development

### Running Tests
```bash
python tests/test_basic.py      # Basic functionality tests
python tests/test_elevenlabs.py # Test ElevenLabs API connection
python tests/test_openai.py     # Test OpenAI integration
python tests/test_ollama.py     # Test Ollama integration
python tests/check_config.py    # Check configuration
```

### Adding Features
The modular architecture makes it easy to extend:
- Add new voice providers in `voice/`
- Implement new monitoring sources in `core/`
- Create additional UI components in `ui/`

## Future Enhancements

📋 **Detailed specifications available in [Docs/specs/](Docs/specs/)**

- **[File Monitoring](Docs/specs/1-file-monitoring-system.md)**: Replace clipboard with automated file-based detection (8-12 hours)
- **[Two-way Voice](Docs/specs/2-two-way-voice-communication.md)**: Speech-to-text for voice commands back to Cursor (12-17 hours)
- **Multiple Voice Providers**: Support for more TTS services
- **Advanced Filtering**: Smart content detection and filtering
- **Custom Voice Training**: Personalized voice models
- **Integration Plugins**: Direct Cursor extension integration

## License

This project is developed for personal use with Cursor AI. Ensure compliance with ElevenLabs and OpenAI terms of service.

## Support

### 📚 Documentation
- **[Setup Guide](Docs/SETUP.md)** - Complete installation and configuration
- **[Troubleshooting](Docs/TROUBLESHOOTING.md)** - Common issues and solutions  
- **[Security Guide](Docs/SECURITY.md)** - Security guidelines and best practices
- **[Documentation Index](Docs/README.md)** - Full documentation overview

### 🔧 Diagnostics
1. Run `python tests/test_basic.py` to verify setup
2. Check logs in generated `.log` files for debugging
3. Verify API key configuration in `.env`
4. Use `python tests/check_config.py` for configuration check

---

**Enjoy hands-free AI assistance with EchoLink!** 🎙️✨

