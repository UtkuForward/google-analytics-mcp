# Google Analytics MCP Server Setup Guide

## Prerequisites ✅
- ✅ Python 3.9+ (You have 3.9.6)
- ✅ pipx (You have 1.7.1)
- ✅ Google Analytics MCP Server (Installed)
- ✅ Gemini CLI (You have it installed)

## Step 1: Google Cloud Project Setup

### 1.1 Create/Select Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. **Note your Project ID** (you'll need this)

### 1.2 Enable Required APIs
Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library) and enable:
- **Google Analytics Admin API**
- **Google Analytics Data API**

### 1.3 Set up Authentication

#### Option A: OAuth 2.0 Client (Personal Use)
1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the JSON file
5. Save it as `~/google-analytics-credentials.json`

#### Option B: Service Account (Production)
1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "Service Account"
3. Name: `analytics-mcp-service`
4. Grant "Google Analytics Read Only" role
5. Create key (JSON) and download
6. Save it as `~/google-analytics-service-account.json`

## Step 2: Configure Gemini CLI

### 2.1 Create Gemini Settings
Create or edit `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "google-analytics-mcp",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "~/google-analytics-credentials.json"
      }
    }
  }
}
```

**Note:** Replace the path with your actual credentials file path.

## Step 3: Test the Setup

### 3.1 Launch Gemini CLI
```bash
gemini
```

### 3.2 Test MCP Server
In Gemini CLI, type:
```
/mcp
```

You should see `analytics-mcp` listed.

### 3.3 Test Commands
Try these sample prompts:
- "what can the analytics-mcp server do?"
- "Give me details about my Google Analytics property"
- "what are the most popular events in my Google Analytics property in the last 180 days?"

## Troubleshooting

### Common Issues:
1. **Authentication Error**: Make sure your credentials file path is correct
2. **API Not Enabled**: Verify both APIs are enabled in Google Cloud Console
3. **Permission Error**: Ensure your account has access to Google Analytics properties

### Verify Installation:
```bash
# Check if MCP server is installed
which google-analytics-mcp

# Check Gemini settings
cat ~/.gemini/settings.json
```

## Next Steps
Once setup is complete, you can:
1. Query your Google Analytics data
2. Run reports
3. Get real-time analytics
4. Access custom dimensions and metrics

## Useful Commands
- `get_account_summaries`: List your GA accounts
- `get_property_details`: Get property information
- `run_report`: Run custom reports
- `run_realtime_report`: Get real-time data
- `get_custom_dimensions_and_metrics`: View custom data 