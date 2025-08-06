# Google Cloud Project Switching Guide

## 🔄 How to Switch Between Different Google Cloud Projects

### **Method 1: Multiple Credential Files (Recommended)**

1. **Create separate credential files for each project:**

```bash
# For Project A
cp /Users/utkugulden/.config/gcloud/application_default_credentials.json /Users/utkugulden/.config/gcloud/project_a_credentials.json

# For Project B  
cp /Users/utkugulden/.config/gcloud/application_default_credentials.json /Users/utkugulden/.config/gcloud/project_b_credentials.json
```

2. **Update Gemini settings for different projects:**

**For Project A:**
```json
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "/Users/utkugulden/.local/pipx/venvs/google-analytics-mcp/bin/python",
      "args": [
        "-m",
        "analytics_mcp.server"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/utkugulden/.config/gcloud/project_a_credentials.json"
      }
    }
  },
  "selectedAuthType": "oauth-personal"
}
```

**For Project B:**
```json
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "/Users/utkugulden/.local/pipx/venvs/google-analytics-mcp/bin/python",
      "args": [
        "-m",
        "analytics_mcp.server"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/utkugulden/.config/gcloud/project_b_credentials.json"
      }
    }
  },
  "selectedAuthType": "oauth-personal"
}
```

### **Method 2: Environment Variable Override**

You can also set the environment variable when launching Gemini CLI:

```bash
# For Project A
GOOGLE_APPLICATION_CREDENTIALS="/Users/utkugulden/.config/gcloud/project_a_credentials.json" gemini

# For Project B
GOOGLE_APPLICATION_CREDENTIALS="/Users/utkugulden/.config/gcloud/project_b_credentials.json" gemini
```

### **Method 3: Quick Switch Script**

Create a script to quickly switch between projects:

```bash
#!/bin/bash
# save as ~/switch_ga_project.sh

PROJECT_NAME=$1
CREDENTIALS_PATH="/Users/utkugulden/.config/gcloud/${PROJECT_NAME}_credentials.json"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./switch_ga_project.sh <project_name>"
    echo "Example: ./switch_ga_project.sh my_project_a"
    exit 1
fi

if [ ! -f "$CREDENTIALS_PATH" ]; then
    echo "Credentials file not found: $CREDENTIALS_PATH"
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

echo "Switched to project: $PROJECT_NAME"
echo "Credentials file: $CREDENTIALS_PATH"
echo "You can now launch Gemini CLI: gemini"
```

**Usage:**
```bash
chmod +x ~/switch_ga_project.sh
./switch_ga_project.sh my_project_a
```

### **Method 4: Install gcloud CLI (Most Flexible)**

1. **Install gcloud CLI:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

2. **Authenticate and switch projects:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

3. **List available projects:**
```bash
gcloud projects list
```

4. **Switch between projects:**
```bash
gcloud config set project PROJECT_ID_A
# or
gcloud config set project PROJECT_ID_B
```

## 🔧 **Important Notes:**

1. **API Enablement**: Make sure both Google Analytics Admin API and Data API are enabled in each project
2. **Permissions**: Ensure your account has access to Google Analytics properties in each project
3. **Credentials**: Each project may need separate OAuth credentials or service account keys
4. **Testing**: Always test the connection after switching projects

## 🧪 **Testing Project Switch:**

After switching projects, test with:
```bash
python3 test_setup.py
```

This will verify that the MCP server can connect with the new project credentials.

## 📝 **Best Practices:**

- **Naming Convention**: Use descriptive names for credential files (e.g., `production_credentials.json`, `staging_credentials.json`)
- **Backup**: Keep backups of your original credentials
- **Documentation**: Document which projects correspond to which credential files
- **Security**: Ensure credential files have proper permissions (600) 