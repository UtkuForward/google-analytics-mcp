# Google Analytics MCP Server Setup ✅

This repository contains a fully configured Google Analytics MCP (Model Context Protocol) server that allows you to query your Google Analytics data through natural language using Gemini CLI.

## 🎉 Setup Complete!

Your Google Analytics MCP server is now fully configured and ready to use!

### What's Working:
- ✅ Python 3.9.6 (compatible)
- ✅ Google Analytics MCP server installed
- ✅ Gemini CLI 0.1.15 installed
- ✅ Gemini settings configured
- ✅ Google Cloud credentials configured
- ✅ MCP server responds correctly

## 🚀 How to Use

### 1. Launch Gemini CLI
```bash
gemini
```

### 2. Access MCP Servers
In Gemini CLI, type:
```
/mcp
```

You should see `analytics-mcp` listed and connected (green status).

### 3. Start Querying Your Data
Try these sample prompts:

**Basic Information:**
- `"what can the analytics-mcp server do?"`
- `"Give me details about my Google Analytics property"`

**Account & Property Info:**
- `"List my Google Analytics accounts"`
- `"Show me my Google Analytics properties"`

**Reports & Analytics:**
- `"what are the most popular events in my Google Analytics property in the last 180 days?"`
- `"were most of my users in the last 6 months logged in?"`
- `"Show me real-time user activity"`
- `"What are my custom dimensions and metrics?"`

## 🛠️ Available Tools

The MCP server provides these tools:

### Account & Property Management
- `get_account_summaries` - List your GA accounts and properties
- `get_property_details` - Get detailed property information
- `list_google_ads_links` - List Google Ads account links

### Reporting
- `run_report` - Run custom Google Analytics reports
- `run_realtime_report` - Get real-time analytics data
- `get_custom_dimensions_and_metrics` - View custom dimensions and metrics

## 📁 Files Created

- `setup_instructions.md` - Detailed setup guide
- `test_setup.py` - Verification script
- `~/.gemini/settings.json` - Gemini CLI configuration

## 🔧 Configuration Details

### Gemini Settings
Located at: `~/.gemini/settings.json`
```json
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "pipx",
      "args": [
        "run",
        "--spec",
        "git+https://github.com/googleanalytics/google-analytics-mcp.git",
        "google-analytics-mcp"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/utkugulden/.config/gcloud/application_default_credentials.json"
      }
    }
  },
  "selectedAuthType": "oauth-personal"
}
```

### Google Cloud Credentials
- Location: `/Users/utkugulden/.config/gcloud/application_default_credentials.json`
- Type: OAuth 2.0 Personal Account
- Scopes: Google Analytics Read-Only

## 🧪 Testing

Run the verification script anytime to check your setup:
```bash
python3 test_setup.py
```

## 🔗 Useful Links

- [Google Analytics MCP Repository](https://github.com/googleanalytics/google-analytics-mcp)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Analytics Admin API](https://developers.google.com/analytics/devguides/config/admin/v1)
- [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)

## 🆘 Troubleshooting

### Common Issues:

1. **MCP Server Disconnected**
   - Run: `python3 test_setup.py` to verify setup
   - Check Gemini settings: `cat ~/.gemini/settings.json`

2. **Authentication Errors**
   - Verify credentials exist: `ls -la /Users/utkugulden/.config/gcloud/application_default_credentials.json`
   - Re-authenticate with Google Cloud if needed

3. **API Not Enabled**
   - Enable Google Analytics Admin API and Data API in Google Cloud Console

### Getting Help:
- Check the `setup_instructions.md` file for detailed setup steps
- Run the test script to identify issues
- Ensure all prerequisites are met

---

**Happy Analytics! 📊** Your Google Analytics data is now accessible through natural language queries in Gemini CLI.
