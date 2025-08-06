#!/usr/bin/env python3
"""
Test script to verify Google Analytics MCP server setup
"""

import json
import os
import subprocess
import sys

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    if version.major == 3 and 9 <= version.minor < 14:
        print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.9-3.13)")
        return False

def check_mcp_server():
    """Check if MCP server is installed"""
    try:
        result = subprocess.run(['which', 'google-analytics-mcp'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Google Analytics MCP server found at: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Google Analytics MCP server not found")
        return False

def check_gemini_cli():
    """Check if Gemini CLI is installed"""
    try:
        result = subprocess.run(['gemini', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Gemini CLI version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Gemini CLI not found")
        return False

def check_gemini_settings():
    """Check if Gemini settings are configured"""
    settings_path = os.path.expanduser("~/.gemini/settings.json")
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            
            if 'mcpServers' in settings and 'analytics-mcp' in settings['mcpServers']:
                mcp_config = settings['mcpServers']['analytics-mcp']
                expected_command = '/Users/utkugulden/.local/pipx/venvs/google-analytics-mcp/bin/python'
                expected_args = ['-m', 'analytics_mcp.server']
                
                if (mcp_config.get('command') == expected_command and 
                    mcp_config.get('args') == expected_args):
                    print("✅ Gemini settings configured correctly for analytics-mcp")
                    return True
                else:
                    print(f"❌ Gemini settings mismatch:")
                    print(f"   Expected command: {expected_command}")
                    print(f"   Actual command: {mcp_config.get('command')}")
                    print(f"   Expected args: {expected_args}")
                    print(f"   Actual args: {mcp_config.get('args')}")
                    return False
            else:
                print("❌ analytics-mcp not found in Gemini settings")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid JSON in Gemini settings file")
            return False
    else:
        print("❌ Gemini settings file not found")
        return False

def check_google_credentials():
    """Check if Google Cloud credentials exist"""
    # Get the credentials path from Gemini settings
    settings_path = os.path.expanduser("~/.gemini/settings.json")
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            creds_path = settings['mcpServers']['analytics-mcp']['env']['GOOGLE_APPLICATION_CREDENTIALS']
        except:
            creds_path = "/Users/utkugulden/.config/gcloud/application_default_credentials.json"
    else:
        creds_path = "/Users/utkugulden/.config/gcloud/application_default_credentials.json"
    
    if os.path.exists(creds_path):
        print(f"✅ Google Cloud credentials found at: {creds_path}")
        return True
    else:
        print("❌ Google Cloud credentials not found")
        return False

def test_mcp_server_functionality():
    """Test if the MCP server can start and respond"""
    try:
        env = os.environ.copy()
        env['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/utkugulden/.config/gcloud/application_default_credentials.json"
        
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
            print("✅ MCP server responds correctly")
            return True
        else:
            print("❌ MCP server failed to respond properly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def main():
    """Run all checks"""
    print("🔍 Checking Google Analytics MCP Server Setup...\n")
    
    checks = [
        check_python_version(),
        check_mcp_server(),
        check_gemini_cli(),
        check_gemini_settings(),
        check_google_credentials(),
        test_mcp_server_functionality()
    ]
    
    print("\n" + "="*50)
    if all(checks):
        print("🎉 All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Launch Gemini CLI: gemini")
        print("2. Type '/mcp' to see available MCP servers")
        print("3. You should see analytics-mcp listed and connected (green)")
        print("4. Try: 'what can the analytics-mcp server do?'")
    else:
        print("❌ Some checks failed. Please review the setup instructions.")
        print("\nSee setup_instructions.md for detailed setup steps.")

if __name__ == "__main__":
    main() 