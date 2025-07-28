#!/usr/bin/env python3
"""
Script to download SwagLabs mobile applications from GitHub releases.
"""

import os
import sys
import requests
from pathlib import Path
import colorlog
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup colored logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# App download URLs
APPS_CONFIG = {
    "android": {
        "url": os.getenv("ANDROID_APP_APK_LINK"),
        "filename": os.getenv("ANDROID_APP_APK_FILENAME"),
        "destination": "apps/android/"
    },
    "ios": {
        "url": os.getenv("IOS_APP_ZIP_LINK"),
        "filename": os.getenv("IOS_APP_FILENAME_ZIP"),
        "destination": "apps/ios/"
    }
}

class AppDownloader:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent
        logger.info(f"📁 Base directory: {self.base_dir}")
    
    def create_directories(self):
        """Create necessary directories for apps"""
        for platform_config in APPS_CONFIG.values():
            dest_dir = self.base_dir / platform_config["destination"]
            dest_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"📂 Created directory: {dest_dir}")
    
    def download_file(self, url, destination):
        """Download file from URL to destination"""
        try:
            logger.info(f"🔽 Downloading: {url}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\r💾 Progress: {progress:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            logger.info(f"✅ Downloaded: {destination}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"❌ Failed to download {url}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False
    
    def download_apps(self, platforms=None):
        """Download apps for specified platforms or all platforms"""
        if platforms is None:
            platforms = list(APPS_CONFIG.keys())
        
        logger.info(f"🚀 Starting download for platforms: {platforms}")
        self.create_directories()
        
        success_count = 0
        total_count = len(platforms)
        
        for platform in platforms:
            if platform not in APPS_CONFIG:
                logger.warning(f"⚠️ Unknown platform: {platform}")
                continue
            
            config = APPS_CONFIG[platform]
            destination = self.base_dir / config["destination"] / config["filename"]
            
            # Skip if file already exists
            if destination.exists():
                logger.info(f"📱 App already exists: {destination}")
                success_count += 1
                continue
            
            # Download the file
            if self.download_file(config["url"], destination):
                success_count += 1
        
        # Summary
        logger.info(f"📊 Download Summary: {success_count}/{total_count} successful")
        
        if success_count == total_count:
            logger.info("🎉 All downloads completed successfully!")
            return True
        else:
            logger.error("❌ Some downloads failed!")
            return False
    
    def list_downloaded_apps(self):
        """List all downloaded applications"""
        logger.info("📱 Downloaded Applications:")
        
        for platform, config in APPS_CONFIG.items():
            dest_dir = self.base_dir / config["destination"]
            
            if dest_dir.exists():
                files = list(dest_dir.glob("*"))
                if files:
                    logger.info(f"  {platform.upper()}:")
                    for file in files:
                        if file.is_file():
                            size_mb = file.stat().st_size / (1024 * 1024)
                            logger.info(f"    📦 {file.name} ({size_mb:.1f} MB)")
                else:
                    logger.info(f"  {platform.upper()}: No files found")
            else:
                logger.info(f"  {platform.upper()}: Directory not found")

def main():
    """Main function - simplified for test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download SwagLabs mobile applications")
    parser.add_argument(
        "--platform", 
        choices=["android", "ios", "all"], 
        default="all",
        help="Platform to download (default: all)"
    )
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List downloaded applications"
    )
    
    args = parser.parse_args()
    
    downloader = AppDownloader()
    
    if args.list:
        downloader.list_downloaded_apps()
        return
    
    # Determine platforms to download
    if args.platform == "all":
        platforms = list(APPS_CONFIG.keys())
    else:
        platforms = [args.platform]
    
    # Download apps
    success = downloader.download_apps(platforms)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 