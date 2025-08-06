#!/bin/bash
# Setup script for test-forward-project

echo "🔧 Setting up Google Analytics MCP for 'test-forward-project'"
echo "=========================================================="
echo ""

# Check if credentials file exists
CREDENTIALS_FILE="/Users/utkugulden/.config/gcloud/test-forward-project_credentials.json"

if [ ! -s "$CREDENTIALS_FILE" ]; then
    echo "❌ Credentials file is empty or doesn't exist: $CREDENTIALS_FILE"
    echo ""
    echo "📋 Please follow these steps:"
    echo ""
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Make sure you're in the 'test-forward-project' project"
    echo "3. Navigate to: APIs & Services > Credentials"
    echo "4. Click 'Create Credentials' > 'OAuth 2.0 Client IDs'"
    echo "5. Choose 'Desktop application'"
    echo "6. Name it: 'Analytics MCP Client'"
    echo "7. Download the JSON file"
    echo "8. Save it as: $CREDENTIALS_FILE"
    echo ""
    echo "After downloading the credentials file, run this script again."
    exit 1
fi

echo "✅ Credentials file found: $CREDENTIALS_FILE"
echo ""

# Set proper permissions
chmod 600 "$CREDENTIALS_FILE"
echo "✅ Set proper file permissions"

# Switch to the new project
echo ""
echo "🔄 Switching to test-forward-project..."
./switch_ga_project.sh test-forward-project

echo ""
echo "🧪 Testing the connection..."
python3 test_setup.py

echo ""
echo "🎉 Setup complete! You can now:"
echo "1. Launch Gemini CLI: gemini"
echo "2. Type '/mcp' to see your connected analytics-mcp server"
echo "3. Start querying your test-forward-project Google Analytics data!" 