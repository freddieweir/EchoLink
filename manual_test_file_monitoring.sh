#!/bin/bash
# Manual testing script for EchoLink file monitoring
# This script demonstrates the manual testing commands from the specification

echo "🗂️ EchoLink File Monitoring Manual Test Script"
echo "=================================================="

# Create test output file location
OUTPUT_FILE="${HOME}/cursor_output.json"
TEXT_OUTPUT_FILE="${HOME}/cursor_output.txt"

echo "📝 Testing JSON format..."
echo "Creating test JSON entry..."

# Manual JSON testing (from specification)
cat << JSONEOF >> "$OUTPUT_FILE"
{
  "timestamp": "$(date -Iseconds)",
  "type": "response", 
  "content": "This is a test response from Cursor using the file monitoring system. It should be automatically detected and spoken.",
  "request_id": "test-$(date +%s)",
  "metadata": {
    "word_count": 20,
    "code_blocks": 0,
    "test": true
  }
}
JSONEOF

echo "✅ Added JSON test data to: $OUTPUT_FILE"

echo ""
echo "📝 Testing text format..."
echo "Creating test text entry..."

# Manual text testing (from specification) 
echo "[$(date)] RESPONSE: This is a test response from Cursor in text format" >> "$TEXT_OUTPUT_FILE"

echo "✅ Added text test data to: $TEXT_OUTPUT_FILE"

echo ""
echo "🔧 Configuration:"
echo "For JSON format monitoring, add to your .env file:"
echo "  FILE_MONITOR_ENABLED=true"
echo "  CURSOR_OUTPUT_FILE=$OUTPUT_FILE"
echo "  CURSOR_OUTPUT_FORMAT=json"
echo ""
echo "For text format monitoring, add to your .env file:"
echo "  FILE_MONITOR_ENABLED=true"
echo "  CURSOR_OUTPUT_FILE=$TEXT_OUTPUT_FILE"
echo "  CURSOR_OUTPUT_FORMAT=text"

echo ""
echo "🚀 To test:"
echo "  1. Update your .env file with the settings above"
echo "  2. Run: python echolink.py"
echo "  3. Start file monitoring from the menu"
echo "  4. Run this script again to add more test content"
echo "  5. EchoLink should detect and speak the new content"

echo ""
echo "📊 Current file sizes:"
if [ -f "$OUTPUT_FILE" ]; then
    echo "  JSON file: $(wc -c < "$OUTPUT_FILE") bytes"
else
    echo "  JSON file: Not created yet"
fi

if [ -f "$TEXT_OUTPUT_FILE" ]; then
    echo "  Text file: $(wc -c < "$TEXT_OUTPUT_FILE") bytes"
else
    echo "  Text file: Not created yet"
fi

echo ""
echo "🔄 To add more test content, run this script again!"
