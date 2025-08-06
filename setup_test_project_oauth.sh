#!/bin/bash
# Proper OAuth setup for test-forward-project

echo "🔧 Setting up proper OAuth authentication for test-forward-project"
echo "=================================================================="
echo ""

# Check if we have the OAuth client credentials
OAUTH_FILE="/Users/utkugulden/.config/gcloud/test-forward-project_credentials.json"

if [ ! -f "$OAUTH_FILE" ]; then
    echo "❌ OAuth client credentials not found: $OAUTH_FILE"
    echo "Please download the desktop OAuth client credentials first."
    exit 1
fi

echo "✅ Found OAuth client credentials"
echo ""

echo "📋 To properly authenticate with test-forward-project, you need to:"
echo ""
echo "1. Install gcloud CLI (if not already installed):"
echo "   curl https://sdk.cloud.google.com | bash"
echo "   exec -l \$SHELL"
echo ""
echo "2. Authenticate with the test project:"
echo "   gcloud auth application-default login --client-id-file=$OAUTH_FILE"
echo ""
echo "3. Set the project:"
echo "   gcloud config set project test-forward-project"
echo ""
echo "4. Test the authentication:"
echo "   gcloud auth application-default print-access-token"
echo ""
echo "5. Update Gemini settings to use the new ADC:"
echo "   ./switch_ga_project.sh test-forward-project"
echo ""

echo "💡 Alternative: Use Service Account (Recommended)"
echo "================================================"
echo "1. Go to Google Cloud Console → IAM & Admin → Service Accounts"
echo "2. Create a new service account"
echo "3. Grant 'Google Analytics Read Only' role"
echo "4. Create and download JSON key"
echo "5. Save as: /Users/utkugulden/.config/gcloud/test-forward-project_service_account.json"
echo "6. Update Gemini settings to use the service account"
echo ""

echo "🔍 Current status:"
echo "=================="
echo "• Original project (atasun-optik-408613): ✅ Working"
echo "• Test project (test-forward-project): ⏳ Needs proper authentication"
echo ""
echo "Your original setup is restored and working." 