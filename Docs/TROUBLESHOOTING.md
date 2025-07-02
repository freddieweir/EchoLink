# EchoLink Troubleshooting Guide

## Common Issues & Solutions

### Installation Issues

#### Import Errors
**Problem**: `ModuleNotFoundError` when running EchoLink

**Solutions**:
```bash
# Ensure virtual environment is activated
source ~/venv/echolink/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Virtual Environment Issues
**Problem**: Can't activate virtual environment

**Solutions**:
```bash
# Recreate virtual environment
rm -rf ~/venv/echolink
python -m venv ~/venv/echolink
source ~/venv/echolink/bin/activate
pip install -r requirements.txt
```

### API Issues

#### ElevenLabs API Errors
**Problem**: "Failed to initialize voice synthesizer"

**Solutions**:
1. **Check API Key**:
   ```bash
   # Verify key is set
   python tests/test_elevenlabs.py
   ```

2. **Verify Key Format**:
   - Should start with alphanumeric characters
   - No extra spaces or quotes in `.env`

3. **Check Account Status**:
   - Log into ElevenLabs dashboard
   - Verify API quota/credits
   - Check if key is still valid

#### OpenAI API Errors
**Problem**: Summarization fails with OpenAI

**Solutions**:
1. **Switch to Ollama**:
   ```env
   SUMMARIZATION_PROVIDER=ollama
   ```

2. **Check API Key**:
   ```bash
   python tests/test_openai.py
   ```

3. **Verify Credits**: Check OpenAI billing dashboard

### Voice Issues

#### No Audio Output
**Problem**: Voice synthesis succeeds but no sound

**Solutions**:
1. **Check System Audio**:
   - Verify speakers/headphones connected
   - Check system volume levels
   - Test with other audio applications

2. **Audio Dependencies**:
   ```bash
   # macOS
   brew install portaudio
   
   # Linux
   sudo apt-get install portaudio19-dev
   
   # Reinstall audio packages
   pip uninstall pydub
   pip install pydub
   ```

3. **Audio Format Issues**:
   - Try different audio backend
   - Check if MP3 codecs are installed

#### Voice Too Fast/Slow
**Problem**: Speech rate not comfortable

**Solutions**:
```env
# Adjust in .env file
VOICE_SPEED=1.0    # Normal speed
VOICE_SPEED=0.8    # Slower
VOICE_SPEED=1.2    # Faster
```

#### Wrong Voice
**Problem**: Using default voice instead of preferred

**Solutions**:
1. **Get Available Voices**:
   - Run EchoLink → Settings → Voice Settings → Select Voice
   - Note the voice ID you want

2. **Update Configuration**:
   ```env
   ELEVENLABS_VOICE_ID=your_preferred_voice_id
   ```

### Monitoring Issues

#### Clipboard Not Detected
**Problem**: Copied text not automatically processed

**Solutions**:
1. **Check Settings**:
   ```env
   CLIPBOARD_MONITOR_ENABLED=true
   CLIPBOARD_MONITOR_INTERVAL=1.0
   ```

2. **Text Length**:
   ```env
   MIN_TEXT_LENGTH=20  # Reduce if needed
   ```

3. **Manual Test**:
   - Copy some text
   - Check if it appears in clipboard: `python -c "import pyperclip; print(pyperclip.paste())"`

4. **Permissions**:
   - macOS: Grant clipboard access if prompted
   - Linux: Install `xclip` or `xsel`

#### Text Processed Multiple Times
**Problem**: Same text spoken repeatedly

**Solutions**:
- This is normal duplicate detection
- Clear cache: Restart EchoLink
- Check `processed_count` in status

### Performance Issues

#### High CPU Usage
**Problem**: EchoLink using too much CPU

**Solutions**:
```env
# Increase monitoring interval
CLIPBOARD_MONITOR_INTERVAL=2.0

# Disable unnecessary features
SUMMARIZATION_ENABLED=false
DEBUG_MODE=false
```

#### Slow Startup
**Problem**: EchoLink takes long to start

**Solutions**:
1. **Check Network**: ElevenLabs API requires internet
2. **API Response Time**: Try different voice ID
3. **Local Dependencies**: Ensure all packages installed

### Configuration Issues

#### Settings Not Loading
**Problem**: Changes to `.env` not taking effect

**Solutions**:
1. **Restart EchoLink**: Configuration loaded at startup
2. **Check File Location**: `.env` should be in EchoLink root directory
3. **Syntax Check**:
   ```env
   # Correct format
   ELEVENLABS_API_KEY=your_key_here
   
   # Incorrect (quotes not needed)
   ELEVENLABS_API_KEY="your_key_here"
   ```

#### Missing Configuration File
**Problem**: `.env` file not found

**Solutions**:
```bash
# Copy example configuration
cp config.example.env .env

# Edit with your settings
nano .env  # or your preferred editor
```

## Diagnostic Commands

### System Information
```bash
# Python version
python --version

# Package versions
pip list | grep -E "(elevenlabs|openai|rich|pydub)"

# Environment check
python tests/check_config.py
```

### API Testing
```bash
# Test all APIs
python tests/test_basic.py
python tests/test_elevenlabs.py
python tests/test_openai.py
python tests/test_ollama.py
```

### Debug Mode
```env
# Enable detailed logging
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## Getting Help

### Log Files
- Check `.log` files for detailed error messages
- Enable `DEBUG_MODE` for more information

### Common Log Messages
- `"API key not configured"` → Check `.env` file
- `"Connection failed"` → Check internet/API status
- `"Audio device not found"` → Check audio setup

### Support Resources
1. **Configuration**: Check `Docs/SETUP.md`
2. **Security**: Review `Docs/SECURITY.md` 
3. **Features**: See specifications in `Docs/specs/`
4. **Tests**: Run diagnostic tests in `tests/` directory

### Reporting Issues
When seeking help, provide:
1. **Error message** (from logs or console)
2. **Operating system** and Python version
3. **Configuration** (without API keys)
4. **Steps to reproduce** the issue 