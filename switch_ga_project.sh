#!/bin/bash
# Google Analytics Project Switcher
# Usage: ./switch_ga_project.sh <project_name>

PROJECT_NAME=$1
CREDENTIALS_PATH="/Users/utkugulden/.config/gcloud/${PROJECT_NAME}_credentials.json"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./switch_ga_project.sh <project_name>"
    echo "Example: ./switch_ga_project.sh my_project_a"
    echo ""
    echo "Available projects:"
    ls -1 /Users/utkugulden/.config/gcloud/*_credentials.json 2>/dev/null | sed 's|.*/||' | sed 's|_credentials.json||' || echo "No project credentials found"
    exit 1
fi

if [ ! -f "$CREDENTIALS_PATH" ]; then
    echo "❌ Credentials file not found: $CREDENTIALS_PATH"
    echo ""
    echo "To create credentials for this project:"
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Select project: $PROJECT_NAME"
    echo "3. Enable Google Analytics Admin API and Data API"
    echo "4. Create OAuth credentials"
    echo "5. Save as: $CREDENTIALS_PATH"
    exit 1
fi

# Update Gemini settings
cat > ~/.gemini/settings.json << EOF
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "/Users/utkugulden/.local/pipx/venvs/google-analytics-mcp/bin/python",
      "args": [
        "-m",
        "analytics_mcp.server"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "$CREDENTIALS_PATH"
      }
    }
  },
  "selectedAuthType": "oauth-personal"
}
EOF

echo "✅ Switched to project: $PROJECT_NAME"
echo "📁 Credentials file: $CREDENTIALS_PATH"
echo ""
echo "🚀 You can now launch Gemini CLI: gemini"
echo "🧪 Test the connection: python3 test_setup.py" 