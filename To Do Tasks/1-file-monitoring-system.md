# File Monitoring System

## Overview
Replace clipboard monitoring with file-based monitoring for more reliable Cursor AI integration. This approach eliminates the dependency on manual copying and enables true automation.

## Current Problem
- Requires manual Cmd+C to copy text from Cursor
- Clipboard can be overwritten by other applications
- No way to distinguish Cursor content from other clipboard content
- User must remember to copy responses

## Proposed Solution
Monitor specific files that Cursor (or scripts) write to, automatically process new content, and speak it via ElevenLabs.

## Implementation Plan

### Phase 1: Core File Monitoring
```python
# New module: src/echolink/core/file_monitor.py
class FileMonitor:
    def __init__(self):
        self.watched_files = {}
        self.file_observer = None
    
    def watch_file(self, file_path: str, callback: Callable):
        """Monitor a file for changes and trigger callback on new content"""
    
    def detect_new_content(self, file_path: str) -> str:
        """Detect only newly appended content since last check"""
```

### Phase 2: Cursor Integration Options

#### Option A: Cursor Extension (Recommended)
- Create VS Code/Cursor extension that automatically writes AI responses to JSON file
- Extension triggers on AI completion, appends to `~/cursor_output.json`
- Rich metadata: timestamp, content type, word count, code blocks, language detection

#### Option B: AppleScript/Automation
- Monitor Cursor window for AI responses
- Automatically extract and write to file when response completes
- Works without needing to develop extension

#### Option C: API Bridge
- EchoLink runs local HTTP server (localhost:8080)
- Cursor extension/script POSTs responses to EchoLink
- More robust than file-based but requires network setup

### Phase 3: Enhanced Processing
```python
# Enhanced content detection for JSON format
class CursorContentProcessor:
    def parse_cursor_output(self, content: str) -> dict:
        """Parse JSON cursor output and extract meaningful content"""
        try:
            data = json.loads(content.strip())
            return {
                "content": data.get("content", ""),
                "type": data.get("type", "unknown"),
                "timestamp": data.get("timestamp", ""),
                "metadata": data.get("metadata", {}),
                "should_speak": self.should_speak_content(data)
            }
        except json.JSONDecodeError:
            # Fallback to text parsing
            return self.parse_text_format(content)
        
    def should_speak_content(self, data: dict) -> bool:
        """Determine if content should be spoken based on type and metadata"""
        content_type = data.get("type", "")
        metadata = data.get("metadata", {})
        
        # Skip code-only responses if setting is disabled
        if content_type == "code" and not settings.speak_code_responses:
            return False
            
        # Skip if mostly code blocks
        if metadata.get("code_blocks", 0) > 3 and len(data.get("content", "")) < 200:
            return False
            
        return True
```

## Technical Details

### File Formats

#### Primary Format: JSON (Recommended)
```json
{
  "timestamp": "2025-01-01T10:30:18Z",
  "type": "response",
  "content": "Recursion is a programming technique where a function calls itself...",
  "request_id": "uuid-4a2f-b3c1-9d8e",
  "metadata": {
    "word_count": 85,
    "code_blocks": 1,
    "language": "python",
    "cursor_session": "session-abc123"
  }
}
```

#### Alternative: Simple Text Format
```
# ~/cursor_output.txt format (fallback):
[2025-01-01 10:30:15] REQUEST: How do I implement recursion?
[2025-01-01 10:30:18] RESPONSE: Recursion is a programming technique where...
```

### Configuration Options
```env
# New .env settings
FILE_MONITOR_ENABLED=true
CURSOR_OUTPUT_FILE=~/cursor_output.json
CURSOR_OUTPUT_FORMAT=json  # json or text
WATCH_FILE_INTERVAL=0.5
CONTENT_FILTER_ENABLED=true
SPEAK_CODE_RESPONSES=false
SPEAK_EXPLANATIONS=true
PARSE_METADATA=true
```

### Watchdog Integration
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CursorFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == self.cursor_output_file:
            self.process_new_content()
```

## Benefits
- ✅ **Fully Automated**: No manual copying required
- ✅ **Reliable**: Doesn't depend on clipboard state
- ✅ **Contextual**: Can include metadata about requests/responses
- ✅ **Selective**: Filter what content gets spoken
- ✅ **Persistent**: File-based history for debugging
- ✅ **Extensible**: Easy to add multiple file sources

## Implementation Steps

### Step 1: Basic File Monitoring (2-3 hours)
1. Create `FileMonitor` class with watchdog
2. Add file monitoring option to settings
3. Implement new content detection (track file position)
4. Update CLI to toggle file vs clipboard monitoring

### Step 2: Cursor Integration (4-6 hours)
1. Create simple AppleScript to extract Cursor responses
2. Test file writing and EchoLink detection
3. Add content parsing and filtering
4. Update configuration options

### Step 3: Advanced Features (2-4 hours)
1. Enhanced JSON parsing with metadata extraction
2. Content type classification (code, explanation, error, etc.)
3. Multiple file monitoring (different AI tools)
4. Smart filtering based on metadata (word count, code blocks, language)

## Testing Plan
```bash
# Manual JSON testing
echo '{"timestamp":"'$(date -Iseconds)'","type":"response","content":"This is a test response from Cursor","request_id":"test-123","metadata":{"word_count":8,"code_blocks":0}}' >> ~/cursor_output.json

# Manual text testing (fallback)
echo "[$(date)] RESPONSE: This is a test response from Cursor" >> ~/cursor_output.txt

# Automated testing
python tests/test_file_monitor.py
python tests/test_json_parser.py

# Integration testing
# Use real Cursor session with AppleScript automation
```

## Future Enhancements
- Monitor multiple files (different AI tools)
- Smart content classification (code, explanation, error, etc.)
- Response quality scoring
- Integration with other editors (VS Code, Vim, etc.)
- Cursor plugin that directly calls EchoLink API

## Success Criteria
- [ ] EchoLink detects new file content within 1 second
- [ ] Correctly parses Cursor response format
- [ ] Filters out unwanted content (code-only responses)
- [ ] Speaks meaningful responses automatically
- [ ] Zero manual intervention required for basic workflow 