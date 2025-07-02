# EchoLink Setup Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- ElevenLabs API account

### Installation

```bash
# 1. Clone and navigate to EchoLink
cd EchoLink

# 2. Create virtual environment
python -m venv ~/venv/echolink
source ~/venv/echolink/bin/activate  # macOS/Linux
# OR: ~/venv/echolink/Scripts/activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp config.example.env .env
# Edit .env with your API keys
```

## Configuration

### Required API Keys

#### ElevenLabs (Required)
1. Visit [ElevenLabs](https://elevenlabs.io/)
2. Create account and get API key
3. Add to `.env`:
   ```env
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_VOICE_ID=default  # or specific voice ID
   ```

#### OpenAI (Optional - for AI summarization)
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Generate API key
3. Add to `.env`:
   ```env
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### Configuration Options

#### Voice Settings
```env
VOICE_SPEED=1.0          # Speech rate (0.5-2.0)
VOICE_VOLUME=0.8         # Volume level (0.0-1.0)
```

#### Monitoring Settings
```env
CLIPBOARD_MONITOR_ENABLED=true
CLIPBOARD_MONITOR_INTERVAL=1.0    # Check every N seconds
MIN_TEXT_LENGTH=50                # Minimum chars to process
```

#### Summarization Settings
```env
SUMMARIZATION_ENABLED=true
SUMMARIZATION_PROVIDER=ollama     # ollama, openai, simple
MAX_SUMMARY_LENGTH=150            # Max chars in summary
```

#### UI Settings
```env
CLI_THEME=dark                    # dark or light
CLI_COLORS_ENABLED=true          # Enable colorful UI
DEBUG_MODE=false                 # Enable debug logging
```

## Testing Installation

### Basic Test
```bash
python tests/test_basic.py
```

### API Tests
```bash
# Test ElevenLabs connection
python tests/test_elevenlabs.py

# Test OpenAI (if configured)
python tests/test_openai.py

# Test Ollama (if running)
python tests/test_ollama.py
```

### Configuration Check
```bash
python tests/check_config.py
```

## Running EchoLink

```bash
# Activate virtual environment
source ~/venv/echolink/bin/activate

# Launch EchoLink
python echolink.py
```

## Voice Configuration

### Finding Voice IDs
1. Run EchoLink
2. Go to Settings → Voice Settings → Select Voice
3. Browse available voices and their IDs
4. Update `ELEVENLABS_VOICE_ID` in `.env`

### Testing Voice
- Use "Test Voice" option in main menu
- Adjust volume and speed in voice settings

## Directory Structure
```
EchoLink/
├── echolink.py          # Main application
├── src/echolink/        # Source code
├── tests/               # Test files
├── Docs/                # Documentation
│   ├── SECURITY.md      # Security guidelines
│   ├── SETUP.md         # This file
│   └── specs/           # Feature specifications
├── requirements.txt     # Dependencies
└── .env                 # Your configuration
```

## Next Steps

After successful setup:
1. **Start monitoring**: Use "Start Voice Monitoring" in main menu
2. **Copy text**: Copy any text to hear it spoken
3. **Adjust settings**: Configure voice, speed, and monitoring options
4. **Review security**: Check `Docs/SECURITY.md` for best practices

## Need Help?

- Check `Docs/TROUBLESHOOTING.md` for common issues
- Run diagnostic tests in `tests/` directory
- Review logs in generated `.log` files
- Ensure API keys are valid and have sufficient credits 