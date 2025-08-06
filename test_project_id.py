#!/usr/bin/env python3
"""
Test script to verify the current Google Cloud project ID
"""

import json
import os
import subprocess
import sys

def check_credentials_file():
    """Check which credentials file is currently being used"""
    settings_path = os.path.expanduser("~/.gemini/settings.json")
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            
            mcp_config = settings.get('mcpServers', {}).get('analytics-mcp', {})
            credentials_path = mcp_config.get('env', {}).get('GOOGLE_APPLICATION_CREDENTIALS')
            
            if credentials_path:
                print(f"📁 Current credentials file: {credentials_path}")
                
                if os.path.exists(credentials_path):
                    # Read the credentials file to extract project info
                    with open(credentials_path, 'r') as f:
                        creds = json.load(f)
                    
                    # Extract project ID from different credential types
                    project_id = None
                    
                    # Check for OAuth 2.0 client credentials
                    if 'client_id' in creds:
                        print(f"🔑 Credential type: OAuth 2.0 Client ID")
                        print(f"🆔 Client ID: {creds['client_id']}")
                        
                        # Try to extract project ID from client ID
                        if 'quota_project_id' in creds:
                            project_id = creds['quota_project_id']
                            print(f"📊 Project ID: {project_id}")
                        elif 'project_id' in creds:
                            project_id = creds['project_id']
                            print(f"📊 Project ID: {project_id}")
                        else:
                            print("⚠️  No project_id found in credentials")
                    
                    # Check for web OAuth credentials (like your test-forward-project)
                    elif 'web' in creds:
                        web_creds = creds['web']
                        print(f"🔑 Credential type: OAuth 2.0 Web Client")
                        print(f"🆔 Client ID: {web_creds.get('client_id', 'N/A')}")
                        if 'project_id' in web_creds:
                            project_id = web_creds['project_id']
                            print(f"📊 Project ID: {project_id}")
                        else:
                            print("⚠️  No project_id found in web credentials")
                    
                    # Check for installed OAuth credentials (desktop application)
                    elif 'installed' in creds:
                        installed_creds = creds['installed']
                        print(f"🔑 Credential type: OAuth 2.0 Desktop Client")
                        print(f"🆔 Client ID: {installed_creds.get('client_id', 'N/A')}")
                        if 'project_id' in installed_creds:
                            project_id = installed_creds['project_id']
                            print(f"📊 Project ID: {project_id}")
                        else:
                            print("⚠️  No project_id found in installed credentials")
                    
                    # Check for service account credentials
                    elif 'project_id' in creds:
                        project_id = creds['project_id']
                        print(f"🔑 Credential type: Service Account")
                        print(f"📊 Project ID: {project_id}")
                    
                    else:
                        print("⚠️  Could not determine credential type or project ID")
                    
                    return project_id
                else:
                    print(f"❌ Credentials file not found: {credentials_path}")
                    return None
            else:
                print("❌ No credentials path found in Gemini settings")
                return None
                
        except json.JSONDecodeError:
            print("❌ Invalid JSON in Gemini settings file")
            return None
    else:
        print("❌ Gemini settings file not found")
        return None

def test_mcp_server_project():
    """Test the MCP server to see what project it's using"""
    try:
        env = os.environ.copy()
        
        # Get credentials path from settings
        settings_path = os.path.expanduser("~/.gemini/settings.json")
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        credentials_path = settings['mcpServers']['analytics-mcp']['env']['GOOGLE_APPLICATION_CREDENTIALS']
        env['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        # Test MCP server initialization
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        }
        
        process = subprocess.Popen(
            ["/Users/utkugulden/.local/pipx/venvs/google-analytics-mcp/bin/python", "-m", "analytics_mcp.server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        
        init_json = json.dumps(init_message) + "\n"
        stdout, stderr = process.communicate(input=init_json, timeout=10)
        
        if process.returncode == 0 and "Google Analytics Server" in stdout:
            print("✅ MCP server is working with current credentials")
            return True
        else:
            print("❌ MCP server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def list_available_projects():
    """List all available project credential files"""
    gcloud_dir = "/Users/utkugulden/.config/gcloud"
    print("\n📋 Available project credentials:")
    print("=" * 40)
    
    if os.path.exists(gcloud_dir):
        for file in os.listdir(gcloud_dir):
            if file.endswith('_credentials.json'):
                project_name = file.replace('_credentials.json', '')
                print(f"• {project_name}")
    else:
        print("No gcloud directory found")

def main():
    """Main test function"""
    print("🔍 Testing Google Cloud Project ID")
    print("=" * 40)
    
    # Check current credentials
    project_id = check_credentials_file()
    
    # Test MCP server
    print("\n🧪 Testing MCP server connection...")
    mcp_working = test_mcp_server_project()
    
    # List available projects
    list_available_projects()
    
    print("\n" + "=" * 40)
    if project_id:
        print(f"✅ Currently using project: {project_id}")
    else:
        print("⚠️  Could not determine current project ID")
    
    if mcp_working:
        print("✅ MCP server is working correctly")
    else:
        print("❌ MCP server has issues")
    
    print("\n💡 To switch projects, use:")
    print("   ./switch_ga_project.sh <project_name>")

if __name__ == "__main__":
    main() 