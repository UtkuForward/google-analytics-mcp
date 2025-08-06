#!/usr/bin/env python3
"""
Script to fix Google Cloud credentials format
"""

import json
import os
import subprocess
import sys

def create_adc_credentials():
    """Create Application Default Credentials from OAuth client"""
    
    # Path to the OAuth client credentials
    oauth_file = "/Users/utkugulden/.config/gcloud/test-forward-project_credentials.json"
    adc_file = "/Users/utkugulden/.config/gcloud/test-forward-project_adc.json"
    
    if not os.path.exists(oauth_file):
        print(f"❌ OAuth credentials file not found: {oauth_file}")
        return False
    
    try:
        # Read the OAuth client credentials
        with open(oauth_file, 'r') as f:
            oauth_creds = json.load(f)
        
        # Extract the installed credentials
        if 'installed' in oauth_creds:
            installed = oauth_creds['installed']
            
            # Create ADC format credentials
            adc_creds = {
                "type": "authorized_user",
                "client_id": installed['client_id'],
                "client_secret": installed['client_secret'],
                "quota_project_id": installed['project_id'],
                "refresh_token": None  # This will be set during authentication
            }
            
            # Save the ADC credentials
            with open(adc_file, 'w') as f:
                json.dump(adc_creds, f, indent=2)
            
            print(f"✅ Created ADC credentials file: {adc_file}")
            print(f"📊 Project ID: {installed['project_id']}")
            
            return adc_file
            
        else:
            print("❌ No 'installed' credentials found in OAuth file")
            return False
            
    except Exception as e:
        print(f"❌ Error creating ADC credentials: {e}")
        return False

def authenticate_with_gcloud():
    """Use gcloud to authenticate and create proper ADC"""
    
    print("🔐 Setting up authentication with gcloud...")
    
    # Check if gcloud is available
    try:
        result = subprocess.run(['which', 'gcloud'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ gcloud CLI not found. Installing...")
            # Install gcloud CLI
            subprocess.run(['curl', 'https://sdk.cloud.google.com', '|', 'bash'], shell=True)
            print("✅ gcloud CLI installed. Please restart your terminal and run this script again.")
            return False
    except:
        print("❌ Could not check for gcloud CLI")
        return False
    
    # Set the credentials file
    oauth_file = "/Users/utkugulden/.config/gcloud/test-forward-project_credentials.json"
    
    try:
        # Use gcloud to authenticate with the OAuth client
        cmd = [
            'gcloud', 'auth', 'application-default', 'login',
            '--client-id-file=' + oauth_file,
            '--scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform'
        ]
        
        print("🔐 Running gcloud authentication...")
        print("This will open a browser window for authentication.")
        print("Please complete the authentication process.")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Authentication successful!")
            return True
        else:
            print(f"❌ Authentication failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return False

def update_gemini_settings(credentials_file):
    """Update Gemini settings to use the new credentials"""
    
    settings_path = os.path.expanduser("~/.gemini/settings.json")
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Update the credentials path
        settings['mcpServers']['analytics-mcp']['env']['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(f"✅ Updated Gemini settings to use: {credentials_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating Gemini settings: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Google Cloud Credentials for test-forward-project")
    print("=" * 60)
    
    # Try to authenticate with gcloud first
    if authenticate_with_gcloud():
        # Update Gemini settings to use the default ADC
        default_adc = "/Users/utkugulden/.config/gcloud/application_default_credentials.json"
        if update_gemini_settings(default_adc):
            print("\n🎉 Credentials fixed successfully!")
            print("You can now use Gemini CLI with your test-forward-project.")
            return True
    
    # Fallback: create ADC format manually
    print("\n🔄 Trying alternative method...")
    adc_file = create_adc_credentials()
    
    if adc_file and update_gemini_settings(adc_file):
        print("\n🎉 Credentials created successfully!")
        print("Note: You may need to authenticate manually.")
        return True
    
    print("\n❌ Could not fix credentials automatically.")
    print("Please try the manual authentication process.")
    return False

if __name__ == "__main__":
    main() 